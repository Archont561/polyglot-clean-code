"""Fresh task registry for polyglot-clean-code.

This is the only file under `automation/`. It owns every local check, hook,
and CI entrypoint. The rule register lives in `backlog/tasks/`; the shipped
product is the native config under `presets/`.
"""

from __future__ import annotations

import gzip
import hashlib
import os
import subprocess
import tarfile
import tomllib
from collections.abc import Sequence
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

DOIT_CONFIG: dict[str, Any] = {
    "default_tasks": ["ci"],
    "verbosity": 2,
    "backend": "sqlite3",
    "dep_file": str(ROOT / ".doit.db"),
}

PRESETS = ("recommended", "strict", "pedantic")

RELEASE_ARCHIVES = ("alint", "vale", "ast-grep", "semgrep")

PRESETS_ROOT = ROOT / "presets"

# The lint covers every tracked Python file, because Rude has no path-exclusion
# option. The Semgrep fixtures are excluded by pathspec: they are deliberately
# invalid targets for the shipped rules. The width is passed on the command line
# because this repository ships no `pyproject.toml`; `.gitignore` keeps Python
# project metadata out on purpose.
PYTHON_EXCLUDES = ("presets/semgrep/fixtures",)
PYTHON_LINE_LENGTH = "88"

VALE_TARGETS = (
    "README.md",
    "AGENTS.md",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
    "presets/README.md",
    "docs",
)

MARKDOWN_TARGETS = (
    "README.md",
    "AGENTS.md",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
    "presets/**/*.md",
    "docs/**/*.md",
    "backlog/**/*.md",
)

ZERO_SHA = "0" * 40


def _env(extra: dict[str, str] | None = None) -> dict[str, str]:
    env = os.environ.copy()
    env.setdefault("SEMGREP_SEND_METRICS", "off")
    env.setdefault("SEMGREP_ENABLE_VERSION_CHECK", "0")
    env.setdefault("NO_COLOR", "1")
    if extra:
        env.update(extra)
    return env


def _run(
    args: Sequence[str],
    *,
    cwd: Path = ROOT,
    check: bool = True,
    capture: bool = False,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args),
        cwd=cwd,
        env=_env(),
        check=check,
        text=True,
        capture_output=capture,
    )


def _workflow_files() -> list[str]:
    return sorted(
        str(path.relative_to(ROOT))
        for path in (ROOT / ".github/workflows").glob("*.yml")
    )


def _git_is_commit(ref: str) -> bool:
    if not ref or not (ROOT / ".git").exists():
        return False
    return (
        subprocess.run(
            ["git", "cat-file", "-e", f"{ref}^{{commit}}"],
            cwd=ROOT,
            capture_output=True,
            check=False,
        ).returncode
        == 0
    )


def _resolve_commit_base(base: str) -> str:
    if base and base != ZERO_SHA:
        return base
    if _git_is_commit("HEAD^"):
        result = subprocess.run(
            ["git", "rev-parse", "HEAD^"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    if not (ROOT / ".git").exists():
        return ""
    result = subprocess.run(
        ["git", "rev-list", "--max-parents=0", "HEAD"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    roots = result.stdout.splitlines()
    return roots[0].strip() if roots else ""


def validate_ast_grep_tests() -> None:
    """Run native ast-grep valid/invalid tests for every preset."""
    for preset in PRESETS:
        _run(
            ["ast-grep", "test", "--skip-snapshot-tests", "-c", "sgconfig.yml"],
            cwd=ROOT / f"presets/ast-grep/{preset}",
        )
    print("ast-grep native rule tests passed for every preset.")


def validate_semgrep_configs() -> None:
    """Validate every composed Semgrep preset."""
    for preset in PRESETS:
        _run(
            [
                "semgrep",
                "scan",
                "--validate",
                "--config",
                f"presets/semgrep/{preset}.yml",
                "--metrics=off",
            ]
        )
    print("Semgrep preset configurations are valid.")


def _has_commit_range(base: str, head: str) -> bool:
    """Report whether both ends of a Convco range exist in this checkout."""
    if not base or not head:
        return False
    return _git_is_commit(base) and _git_is_commit(head)


def check_commit_messages(base: str = "", head: str = "") -> None:
    """Validate a commit range with Convco when Git history exists."""
    resolved_base = _resolve_commit_base(base)
    if not _has_commit_range(resolved_base, head):
        print("No complete commit range available; skipping the Convco range check.")
        return
    _run(["convco", "check", f"{resolved_base}..{head}"])


def tracked_python_files() -> list[str]:
    """List tracked Python files, minus the deliberately invalid Semgrep fixtures."""
    pathspecs = ["*.py", *(f":(exclude){prefix}/**" for prefix in PYTHON_EXCLUDES)]
    listing = _run(["git", "ls-files", *pathspecs], capture=True).stdout
    return listing.split()


def lint_python() -> None:
    """Run Rude over every tracked Python file."""
    files = tracked_python_files()
    if not files:
        print("No tracked Python files to lint.")
        return
    command = ["rude", "check", "--max-line-length", PYTHON_LINE_LENGTH]
    _run([*command, *files])


def workspace_version() -> str:
    """Return the version declared in `pixi.toml`."""
    manifest = tomllib.loads((ROOT / "pixi.toml").read_text(encoding="utf-8"))
    return str(manifest["workspace"]["version"])


def _reproducible_entry(archive: tarfile.TarFile, path: Path) -> tarfile.TarInfo:
    """Return a tar entry with normalised owner and timestamp metadata."""
    info = archive.gettarinfo(str(path), arcname=str(path.relative_to(PRESETS_ROOT)))
    info.uid = 0
    info.gid = 0
    info.uname = ""
    info.gname = ""
    info.mtime = 0
    return info


def _add_entry(archive: tarfile.TarFile, path: Path) -> None:
    """Copy one preset path into an archive as a file or a directory entry."""
    info = _reproducible_entry(archive, path)
    if not info.isfile():
        archive.addfile(info)
        return
    with path.open("rb") as handle:
        archive.addfile(info, handle)


def _archive_tool(tool: str, target: Path) -> None:
    """Write one deterministic archive for a single preset tree."""
    stream = gzip.GzipFile(str(target), "wb", mtime=0)
    archive = tarfile.open(fileobj=stream, mode="w", format=tarfile.PAX_FORMAT)
    # Enter the stream first so it closes after the tar trailer is written.
    with stream, archive:
        for path in sorted((PRESETS_ROOT / tool).rglob("*")):
            _add_entry(archive, path)


def _pack_preset(tool: str, dist: Path, version: str) -> Path:
    """Build the archive for one tool and return its path."""
    target = dist / f"polyglot-clean-code-presets-{tool}-{version}.tar.gz"
    _archive_tool(tool, target)
    return target


def _write_checksums(archives: list[Path], dist: Path, version: str) -> Path:
    """Write a SHA-256 manifest for the archives and return its path."""
    lines = [
        f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}"
        for path in archives
    ]
    checksums = dist / f"SHA256SUMS-{version}.txt"
    checksums.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return checksums


def build_preset_archives() -> None:
    """Pack every preset tree into a reproducible archive beside a checksum file."""
    version = workspace_version()
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    archives = [_pack_preset(tool, dist, version) for tool in RELEASE_ARCHIVES]
    checksums = _write_checksums(archives, dist, version)
    print(f"Packed {len(archives)} preset archives and wrote {checksums.name}.")


def build_release(ref_name: str = "") -> None:
    """Check an optional release tag and render the Convco changelog."""
    version = workspace_version()
    if ref_name and ref_name.removeprefix("v") != version:
        raise RuntimeError(
            f"Tag {ref_name!r} does not match workspace version {version!r}"
        )
    changelog = _run(["convco", "changelog"], capture=True)
    if not changelog.stdout.strip():
        raise RuntimeError("convco changelog produced no output")
    notes = ROOT / "dist" / "release-notes.md"
    notes.parent.mkdir(exist_ok=True)
    notes.write_text(changelog.stdout, encoding="utf-8")
    print(
        f"Release validation passed for version {version}; "
        f"notes at dist/{notes.name}."
    )


def install_hooks() -> None:
    """Install or verify Lefthook hooks."""
    check = _run(["lefthook", "check-install"], check=False, capture=True)
    if check.returncode == 0:
        print("Lefthook hooks are installed.")
        return
    _run(["lefthook", "install"])
    _run(["lefthook", "check-install"])


def task_bun_install() -> dict[str, Any]:
    """Install frozen Bun developer CLIs."""
    return {
        "basename": "bun-install",
        "actions": [["bun", "install", "--frozen-lockfile"]],
    }


def task_docs_lint() -> dict[str, Any]:
    """Lint maintained Markdown with markdownlint-cli2."""
    return {
        "basename": "docs-lint",
        "task_dep": ["bun-install"],
        "actions": [
            [
                "bun",
                "x",
                "--bun",
                "--no-install",
                "markdownlint-cli2",
                *MARKDOWN_TARGETS,
            ]
        ],
    }


def task_lint_prose() -> dict[str, Any]:
    """Lint maintained Markdown prose with Vale."""
    return {
        "basename": "lint-prose",
        "actions": [["vale", "--no-global", "--config=.vale.ini", *VALE_TARGETS]],
    }


def task_alint() -> dict[str, Any]:
    """Dogfood the fresh root Alint repository policy."""
    return {
        "basename": "alint",
        "actions": [["alint", "check", ".", "-c", ".alint.yml", "--fail-on-warning"]],
    }


def task_ast_grep_test() -> dict[str, Any]:
    """Run native ast-grep rule tests for every preset."""
    return {"basename": "ast-grep-test", "actions": [validate_ast_grep_tests]}


def task_semgrep_validate() -> dict[str, Any]:
    """Validate composed Semgrep configurations."""
    return {"basename": "semgrep-validate", "actions": [validate_semgrep_configs]}


def task_actionlint() -> dict[str, Any]:
    """Lint GitHub Actions workflows."""
    return {"basename": "actionlint", "actions": [["actionlint", *_workflow_files()]]}


def task_backlog() -> dict[str, Any]:
    """List Backlog.md tasks in a non-interactive format."""
    return {
        "basename": "backlog",
        "task_dep": ["bun-install"],
        "actions": [
            ["bun", "x", "--bun", "--no-install", "backlog", "task", "list", "--plain"]
        ],
    }


def task_lint_commit() -> dict[str, Any]:
    """Validate one Conventional Commit message from stdin."""
    return {
        "basename": "lint-commit",
        "actions": [["convco", "check", "--from-stdin", "--strip"]],
    }


def task_check_commit_messages() -> dict[str, Any]:
    """Validate an incoming Convco commit range."""
    return {
        "basename": "check-commit-messages",
        "params": [
            {
                "name": "base",
                "long": "base",
                "type": str,
                "default": "",
                "env_var": "COMMIT_BASE",
                "help": "Base commit SHA.",
            },
            {
                "name": "head",
                "long": "head",
                "type": str,
                "default": "",
                "env_var": "COMMIT_HEAD",
                "help": "Head commit SHA.",
            },
        ],
        "actions": [check_commit_messages],
    }


def task_presets_archive() -> dict[str, Any]:
    """Pack the preset trees into reproducible release archives."""
    return {"basename": "presets-archive", "actions": [build_preset_archives]}


def task_build_release() -> dict[str, Any]:
    """Validate a release tag, render the changelog, and pack the presets."""
    return {
        "basename": "build-release",
        "task_dep": ["presets-archive"],
        "params": [
            {
                "name": "ref_name",
                "long": "ref",
                "type": str,
                "default": "",
                "env_var": "GITHUB_REF_NAME",
                "help": "Git tag name, for example v0.1.0.",
            }
        ],
        "actions": [build_release],
    }


def task_lint_python() -> dict[str, Any]:
    """Lint every tracked Python file with Rude and the Clean Code plugin."""
    return {"basename": "lint-python", "actions": [lint_python]}


def task_install_hooks() -> dict[str, Any]:
    """Install or verify Lefthook hooks."""
    return {"basename": "install-hooks", "actions": [install_hooks]}


def task_test() -> dict[str, Any]:
    """Run the fresh policy chain."""
    return {"basename": "test", "task_dep": ["policy"], "actions": None}


def task_pre_commit() -> dict[str, Any]:
    """Run pre-commit checks."""
    return {
        "basename": "pre-commit",
        "task_dep": [
            "alint",
            "lint-prose",
            "lint-python",
            "docs-lint",
            "actionlint",
            "ast-grep-test",
            "semgrep-validate",
            "backlog",
        ],
        "actions": None,
    }


def task_policy() -> dict[str, Any]:
    """Run the full local policy chain."""
    return {
        "basename": "policy",
        "task_dep": [
            "alint",
            "lint-prose",
            "lint-python",
            "docs-lint",
            "actionlint",
            "ast-grep-test",
            "semgrep-validate",
            "backlog",
        ],
        "actions": None,
    }


def task_docs() -> dict[str, Any]:
    """Run documentation checks."""
    return {
        "basename": "docs",
        "task_dep": ["docs-lint", "lint-prose"],
        "actions": None,
    }


def task_ci() -> dict[str, Any]:
    """Run the full local CI chain."""
    return {
        "basename": "ci",
        "task_dep": ["policy", "docs", "check-commit-messages"],
        "actions": None,
    }
