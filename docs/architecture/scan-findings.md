# Archont561 scan findings

## Method

The GitHub REST API listed 20 public repositories on 2026-11-10. Eight repositories were cloned and inspected in depth: `rude-clean-code`, `PyShellForge`, `qgis-sdk`, `bun-test-utils`, `playtest`, `artifactspec`, `skills`, and `gh-meta`. The other repositories were checked through manifests, descriptions, language metadata, and issue records.

## Convergence

| Convention | Evidence | Preset consequence |
| --- | --- | --- |
| Pixi is the environment of record | `pixi.toml`, `pixi.lock`, and `[activation.env] PYTHONPATH` in Python and Rust repositories | `PCC-R01` requires the manifest and lock together |
| doit is the single task registry | `automation/dodo.py` and `doit.cfg` in `rude-clean-code`; root `dodo.py` in PyShellForge | `PCC-R02` requires the registry and one-line workflow `run` steps |
| Developer CLIs are pinned | `package.json`, `bun.lock`, `skills-lock.json`, `lefthook.yml`, and `.versionrc` | `PCC-R03` requires pinned Bun, hooks, and Convco state |
| Documentation is a maintained tree | `AGENTS.md`, `docs/guides/`, `docs/reference/`, `docs/architecture/`, `docs/development/`, and Backlog.md documents | `PCC-R04` requires entrypoints; Vale rules guard terminology and prose |
| CI has a narrow trust boundary | `permissions: contents: read`, SHA-pinned actions, `persist-credentials: false`, and one-line steps | `PCC-R05` checks workflow values and issue forms |
| Generated state is excluded | `.gitignore`, Ruff exclusions, `codecov.yml`, and `clean_code_budget.json` gates | `PCC-R06` and `PCC-R07` enforce hygiene and paired tests |
| Commit vocabulary is explicit | `.versionrc` with scope regex and hidden internal types | `PCC-R08` checks Convco types and Backlog.md statuses |

All eight deep clones contain `pixi.lock`, `lefthook.yml`, and `AGENTS.md`. Python-heavy repositories contain `.alint.yml`, `.vale.ini`, `.versionrc`, and `codecov.yml`. TypeScript and Rust leaning repositories drop Python lint files but keep Pixi, hooks, agent instructions, and feature tests. The Recommended Alint preset no longer encodes the original skills-lock checks, because skills and the Python test tree are no longer part of the scaffold; the Strict and Pedantic presets keep them until their own refreshes.

## Rude Clean Code precedent

The implemented plugin has nine deterministic rules:

| Code | Limit |
| --- | --- |
| `CC101` FunctionTooLong | 30 lines |
| `CC102` TooManyParameters | 5 parameters |
| `CC103` TooManyReturns | 5 returns |
| `CC104` TooManyLocals | 10 locals |
| `CC201` ClassTooLarge | 200 lines |
| `CC202` TooManyMethods | 15 methods |
| `CC301` ExcessiveNesting | depth 4 |
| `CC302` ExcessiveBooleanOperands | 3 operands |
| `CC303` ExcessiveBranching | 10 branches |

Every diagnostic states a measured value, a limit, and a suggested action. Counts do not descend into nested scopes. Heuristic rules are INFO, deterministic structural rules are WARNING, and nothing is ERROR by default. qgis-sdk writes those thresholds explicitly in `[tool.rude]` and baselines legacy findings in `clean_code_budget.json`.

Doc-2 proposes `CC001`–`CC910` across module organization, functions, classes, readability, naming, cohesion, coupling, dependencies, patterns, and documentation. Project-scope checks are deferred until the engine supports them. That discipline became the rule contract in this repository: stable IDs, explicit scope, measured messages, paired examples, and no fabricated analysis.

## Language conventions

Rust workspaces in `gh-meta` and `playtest` use `unsafe_code = "forbid"`, `unused_must_use = "deny"`, and Clippy pedantic. `deny.toml` bans wildcard dependencies and unknown sources. These facts produced `PCC-S02`, `PCC-S03`, `PCC-P07`, and `PCC-P08`.

TypeScript repositories use Biome with a two-space formatter, double quotes, and a recommended linter baseline. Python repositories keep Ruff in `ruff.toml`, with `I` and `PTH` as the common extension. `mypy.ini` enables `check_untyped_defs` and `warn_unused_ignores`. The presets do not ban `noExplicitAny`, because Archont561 disables that Biome rule in `bun-test-utils`.

Vale styles are vendored. `Project/Terms.yml` enforces product names, `Microsoft/Spacing.yml` checks sentence spacing, `write-good/Weasel.yml` is advisory, and `accept.txt` records accepted tokens. Warnings are advisory; errors fail.

## Resulting rule placement

| Engine | Best fit | Canonical family |
| --- | --- | --- |
| Alint | Files, config values, workflow values, repository shape | `PCC-R01`–`PCC-R08` |
| Vale | Terminology, spacing, prose evidence, links, headings | `PCC-D01`–`PCC-D06` |
| ast-grep | Language-aware structure in Python, TypeScript, and Rust | `PCC-S01`–`PCC-S08` |
| Semgrep | Pattern-based fail-fast, security, config references, and annotated markers | `PCC-P01`–`PCC-P08` |

The split follows the evidence. A repository convention belongs to Alint. A syntax-tree shape belongs to ast-grep. A cross-language pattern belongs to Semgrep. A prose rule belongs to Vale. The boundary against numeric AST metrics is documented in [`docs/concepts/engine-limits.md`](../concepts/engine-limits.md).
