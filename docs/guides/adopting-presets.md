# Adopting presets

This guide is for a consumer repository that wants the curated native configs without adopting this project's development harness. The distribution is plain files; it adds no CLI and no generator.

## Naming

| Item | Name | Rule |
| --- | --- | --- |
| Upstream repository | `Archont561/polyglot-clean-code` | Keep the product name in lowercase kebab-case, without `-dev`, a version, or a tool list. It matches `rude-clean-code` in the same owner namespace. |
| Consumer checkout | `vendor/clean-code-presets` | Name the directory after the artifact, not the upstream repository. Use `third_party/clean-code-presets` when that convention already exists. |
| Published package, if added later | `@archont561/clean-code-presets` | A scoped name says what ships: presets. The current `polyglot-clean-code-dev` in `package.json` is a private developer manifest, not the distribution name. |
| Preset root in commands | `$PRESETS` | A shell variable that points at the copied `presets/` directory. Set it once after installation. |
| Pin selector | `$PIN` | A release tag after `PCC-12`, or a full commit SHA today. |

Avoid a root-level `presets/` directory in the consumer: it collides with existing config and makes the origin of each file ambiguous. Avoid `-generator`, `-configs`, and `-dev` in the checkout name. The four engines read native files, not the upstream repository name.

If the upstream repository is renamed, only the remote URL changes. The consumer path, `$PRESETS`, and `$PIN` stay stable.

## Add the distribution

A submodule records a commit in the superproject, not a tag name. A tag is a readable selector for that commit; the gitlink stores the SHA. Moving a tag later does not move a consumer that already committed the gitlink.

At the time of writing, no release tag exists yet; `backlog/tasks/pcc-12` is open. Set `$PIN` to a full commit SHA today. After the first release, set it to a tag such as `v0.1.0`. The release workflow accepts tags matching `v*`, and `doit build-release` checks the tag against the version in `pixi.toml`. Check `git ls-remote --tags https://github.com/Archont561/polyglot-clean-code.git` before choosing a tag.

```sh
PIN=v0.1.0
# Until PCC-12 publishes a tag, use a full commit SHA instead:
# PIN=<full-commit-sha>
```

### Pinned submodule

Use this when the consumer wants reproducible updates. A full clone keeps tags and older commits available.

```sh
git submodule add --name clean-code-presets \
  https://github.com/Archont561/polyglot-clean-code.git \
  vendor/clean-code-presets
git -C vendor/clean-code-presets fetch --tags origin
git -C vendor/clean-code-presets checkout "$PIN"
git add .gitmodules vendor/clean-code-presets
git submodule status
PRESETS=vendor/clean-code-presets/presets
```

`git submodule status` prints the pinned SHA and the tag when `$PIN` is a tag. Do not pass `--depth 1` when `$PIN` is a tag or an older commit: a shallow clone of the default branch tip may not contain that object. For a shallow checkout, add with `--depth 1`, then run `git -C vendor/clean-code-presets fetch --depth 1 origin tag "$PIN"` before checkout.

In CI, run `git submodule update --init --recursive` before the lint steps. Do not add `--remote`: it moves the submodule to the tracked branch tip instead of the pinned commit. A submodule keeps the whole upstream tree, so `$PRESETS` includes the extra `presets/` segment.

### Flat vendored copy

Use this when the consumer does not want a submodule. The same `$PIN` applies.

```sh
git clone https://github.com/Archont561/polyglot-clean-code.git /tmp/pcc-upstream
git -C /tmp/pcc-upstream checkout "$PIN"
mkdir -p vendor/clean-code-presets
printf '%s\n' "$PIN" > vendor/clean-code-presets/UPSTREAM.pin
cp -R /tmp/pcc-upstream/presets/. vendor/clean-code-presets/
PRESETS=vendor/clean-code-presets
```

Record the selector in `UPSTREAM.pin` and review it during the next update. A flat copy has no extra `presets/` segment.

## What to copy

Only `presets/` is the distribution. Do not copy `automation/`, `docs/`, `backlog/`, `.github/`, `pixi.toml`, `pixi.lock`, `package.json`, or `bun.lock`. Those files maintain this repository and are not needed by a consumer.

No catalogue file ships. The rule register lives in `backlog/tasks/`; consumers copy only `presets/`.

Do not run `pixi install`, `bun install`, or `doit` in the consumer repository. The upstream `pixi.toml` and `package.json` belong to the maintenance harness.

## Install the engines

The consumer installs Alint, Vale, ast-grep, and Semgrep through its own package manager, container, or CI action. Pin versions in the consumer's lockfile. The distribution does not install engines and does not provide a wrapper.

## Point each engine at one preset

Choose one level per tool. The commands below use Recommended and assume `$PRESETS` is exported in the consumer shell.

```sh
alint check . -c "$PRESETS/alint/recommended.yml"
vale --no-global --config="$PRESETS/vale/recommended.ini" docs/
ast-grep --config "$PRESETS/ast-grep/recommended/sgconfig.yml" scan .
semgrep scan --config "$PRESETS/semgrep/recommended.yml" .
```

Keep each preset tree intact: Vale resolves `StylesPath` relative to the `.ini` file, and ast-grep resolves `ruleDirs` relative to `sgconfig.yml`. The Semgrep preset YAML is self-contained. Semgrep prefixes rule IDs with the config path when it loads a nested config, so capture the emitted ID with `semgrep --json` before writing a baseline entry.

## Alint in an arbitrary repository

Alint is the repository-shape engine. `PCC-R01`–`PCC-R04` require the Archont561 harness: `pixi.toml`, `pixi.lock`, `automation/dodo.py`, `doit.cfg`, `package.json`, `bun.lock`, `lefthook.yml`, `.versionrc`, `docs/concepts/rule-register.md`, and the other documentation entrypoints. A fresh consumer that runs `alint check . -c "$PRESETS/alint/recommended.yml"` without those files will report each missing path before any code rule runs. Alint Recommended and Strict no longer check `skills-lock.json`; the Pedantic preset keeps that check until PCC-18 lands.

Choose one of three paths:

1. Adopt the harness files, then enable Alint Recommended.
2. Keep a hand-authored local Alint config outside `vendor/clean-code-presets` with only the rules that apply to the consumer. Leave the vendored preset untouched.
3. Defer Alint. Vale, ast-grep, and Semgrep work in an arbitrary repository without the harness.

Alint Recommended and Strict check `docs/concepts/rule-register.md`. The Pedantic preset still retains the historical `docs/reference/rules.md` and `automation/fixtures/` checks. These are product rules for a full Archont561 harness, not checks on this repository's fresh scaffold; the root `.alint.yml` checks the register and the three backlog tasks instead. Do not lower severity inside the vendored preset to make the first run pass. See [`docs/concepts/engine-limits.md`](../concepts/engine-limits.md) for the boundary between repository shape and source metrics.

## Staged rollout

1. Start with Vale Recommended, ast-grep Recommended, and Semgrep Recommended. Fix prose, structural, and security findings using the canonical IDs in `backlog/tasks/`.
2. Decide the Alint path above, then enable Alint Recommended or keep the local override.
3. Move one tool at a time to Strict. Add the consumer's own path ignores in a local override, not in the vendored preset.
4. Move to Pedantic after false-positive counts are measured. Heuristics become warnings there.
5. Keep a baseline for legacy findings when a repository needs gradual adoption.

## Legacy baseline example

The qgis-sdk repository records legacy diagnostics in `clean_code_budget.json` rather than deleting them. A consumer can follow the same pattern in a local baseline file without weakening the distributed presets:

```json
{
  "pcc-s03-unwrap-rust": {
    "allow": ["crates/legacy/src/parser.rs:42"],
    "reason": "Recorded in the repository migration decision"
  }
}
```

Keep the canonical `PCC-S03` ID and the native `pcc-s03-unwrap-rust` ID unchanged. Suppress only the listed path in a local override, and remove the entry when its migration decision closes. Do not lower severity in a copied preset or introduce a new CLI to interpret the file. Semgrep emits rule IDs namespaced by the config path, so use the exact ID from `semgrep --json` when a baseline key targets a Semgrep rule.

## Local overrides

A consumer keeps overrides in its own repository, outside `vendor/clean-code-presets`. Edit a copied config or add a local config that points at the vendored styles and rules; never edit the vendored files in place. Keep canonical IDs and evidence unchanged, and remove an override when the migration decision closes.

A maintainer of this distribution changes the native config and the matching backlog task in the same review. Use a branch or fork so the canonical IDs and Archont561 evidence stay reviewable. Numeric complexity metrics remain in `rude-clean-code`; see [`docs/concepts/engine-limits.md`](../concepts/engine-limits.md).

## CI wiring

Call one native command per engine from the consumer's CI. Keep workflow `run` steps on one line and SHA-pin third-party actions. Use read-only `permissions: contents: read` in GitHub Actions workflows.

```yaml
- run: alint check . -c "$PRESETS/alint/strict.yml"
- run: vale --no-global --config="$PRESETS/vale/strict.ini" docs/
- run: ast-grep --config "$PRESETS/ast-grep/strict/sgconfig.yml" scan .
- run: semgrep scan --config "$PRESETS/semgrep/strict.yml" .
```

Export `$PRESETS` once in the job, or replace it with the literal path. Initialize the submodule before these steps when the pinned submodule mode is used. In this repository, `doit policy` and `doit ci` validate the native engines and the maintained documentation. Vale checks prose and Alint checks repository and documentation structure.

## Updating

Move `$PIN` to the next tag or commit, then re-run the four commands and review the diff before merging. For a submodule, run `git -C vendor/clean-code-presets fetch --tags origin`, check out the new `$PIN`, and stage the gitlink. For a flat copy, refresh `UPSTREAM.pin` and replace only `vendor/clean-code-presets`. Keep `git submodule update --init --recursive` in CI without `--remote`, and do not let a local override silently mask a new upstream rule.

## Verification in this repository

`pixi run --locked doit docs` checks this guide with Vale and markdownlint-cli2. `pixi run --locked doit ci` also checks Alint structure, the native engine tests, and the maintained documentation. Vale checks prose and Alint checks repository and documentation structure. The example commands were run from a clean consumer directory with only the vendored `presets/` tree present. The tag-pin sequence was exercised against a local two-commit repository with a `v0.1.0` tag, where `git submodule status` reported the tagged SHA.
