---
id: PCC-16
title: Refresh Recommended preset rules
status: In Progress
assignee: []
created_date: '2026-11-10 18:30'
updated_date: '2026-11-10 19:05'
labels: []
dependencies: []
priority: high
type: task
ordinal: 16000
milestone: ''
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Start the dev loop here after the remote is updated. This task holds the 11 canonical rules first exposed in the Recommended preset. The native configs under `presets/` remain the shipped product; this task is the reviewed rule register. No catalogue file and no generator are used.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Review every listed `PCC-*` ID against its native config under `presets/`.
- [x] #2 Confirm the `[PCC-...]` message prefix, confidence, and native severity for each rule.
- [x] #3 Update the native config and this task in the same change; keep paired positive and negative examples.
- [ ] #4 Run `pixi run --locked doit ci` and record the verification evidence here.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Work one ID at a time. Read the rule details below, open the matching native config, adjust the rule, then update this task. Finish with `doit ci`. Move to PCC-17 when this task is Done.
<!-- SECTION:PLAN:END -->

## Rule inventory

| ID | Tool | Title | Confidence | Native IDs |
| --- | --- | --- | --- | --- |
| `PCC-R01` | alint | Locked Pixi environment | critical | pcc-r01-pixi-manifest, pcc-r01-pixi-lock |
| `PCC-R02` | alint | One automation registry | deterministic | pcc-r02-dodo-file, pcc-r02-doit-config, pcc-r02-workflow-run-single-line |
| `PCC-R03` | alint | Pinned developer CLIs and commit policy | deterministic | pcc-r03-package-manifest, pcc-r03-bun-lock, pcc-r03-hooks, pcc-r03-convco, pcc-r03-bun-package-manager |
| `PCC-R04` | alint | Documentation and agent entrypoints | deterministic | pcc-r04-readme, pcc-r04-agents, pcc-r04-contributing, pcc-r04-docs-index, pcc-r04-development-guide, pcc-r04-rule-register |
| `PCC-D01` | vale | Canonical product and tool names | critical | pcc-d01-canonical-terms |
| `PCC-D02` | vale | One space after sentence punctuation | deterministic | pcc-d02-punctuation-spacing |
| `PCC-S01` | ast-grep | Structured logging instead of debug prints in library code | deterministic | pcc-s01-print-python, pcc-s01-console-log-ts, pcc-s01-println-rust |
| `PCC-S02` | ast-grep | Rust workspace forbids unsafe code | critical | pcc-s02-unsafe-rust |
| `PCC-P01` | semgrep | Swallowed exceptions | critical | pcc-p01-swallowed-exception-python |
| `PCC-P02` | semgrep | No dynamic execution or unsafe deserialization | critical | pcc-p02-unsafe-dynamic-python |
| `PCC-P03` | semgrep | No shell=True subprocess calls | critical | pcc-p03-shell-true-python |

## Rule details

### `PCC-R01` — Locked Pixi environment

- Message: `[PCC-R01] Keep pixi.toml and pixi.lock together; the lockfile is the environment of record.`
- Source: `rude-clean-code/pixi.toml; PyShellForge; qgis-sdk; artifactspec; gh-meta`
- Positive: `pixi.toml and pixi.lock are both committed`
- Negative: `pixi.toml is committed without pixi.lock`
- Implementations: `pcc-r01-pixi-manifest` (file_exists), `pcc-r01-pixi-lock` (file_exists)

### `PCC-R02` — One automation registry

- Message: `[PCC-R02] Keep automation in automation/dodo.py through doit.cfg and single-line workflow run steps.`
- Source: `rude-clean-code/automation/dodo.py, doit.cfg and .github/workflows/ci.yml; PyShellForge dodo.py`
- Positive: `dodo.py, doit.cfg and a one-line workflow run step are present`
- Negative: `workflow embeds logic in a multiline run block`
- Implementations: `pcc-r02-dodo-file` (file_exists), `pcc-r02-doit-config` (file_exists), `pcc-r02-workflow-run-single-line` (yaml_path_matches)
- Scope note: the single-line rule excludes `.github/workflows/publish-sandbox.yml` and `.github/workflows/relock.yml`, which `pixi-sandbox init` generates with a checksum-verified bootstrap step. Hand-maintained workflows stay in scope.

### `PCC-R03` — Pinned developer CLIs and commit policy

- Message: `[PCC-R03] Pin Bun developer CLIs, hooks and Conventional Commit configuration.`
- Source: `rude-clean-code/package.json, bun.lock, lefthook.yml and .versionrc`
- Positive: `package.json, bun.lock, lefthook.yml and .versionrc are present`
- Negative: `bun.lock is absent`
- Implementations: `pcc-r03-package-manifest` (file_exists), `pcc-r03-bun-lock` (file_exists), `pcc-r03-hooks` (file_exists), `pcc-r03-convco` (file_exists), `pcc-r03-bun-package-manager` (json_path_matches)
- Retired: `pcc-r03-skills-lock` and `pcc-r03-skills-lock-version` checked `skills-lock.json`, which the current scaffold does not ship. The root `.alint.yml` had already dropped them; this refresh makes the shipped preset agree with the scaffold it documents.

### `PCC-R04` — Documentation and agent entrypoints

- Message: `[PCC-R04] Maintain README, AGENTS, contributing guidance, a documentation index, and a rule register.`
- Source: `rude-clean-code/docs tree, AGENTS.md, CONTRIBUTING.md; qgis-sdk and artifactspec docs trees`
- Positive: `README.md, AGENTS.md, CONTRIBUTING.md, docs/README.md and docs/concepts/rule-register.md are present`
- Negative: `docs/concepts/rule-register.md is missing`
- Implementations: `pcc-r04-readme` (file_exists), `pcc-r04-agents` (file_exists), `pcc-r04-contributing` (file_exists), `pcc-r04-docs-index` (file_exists), `pcc-r04-development-guide` (file_exists), `pcc-r04-rule-register` (file_exists)
- Renamed: `pcc-r04-rule-reference` required `docs/reference/rules.md`, which no longer exists. The register of record is `docs/concepts/rule-register.md`, and the renamed rule matches the root `.alint.yml` ID and message.

### `PCC-D01` — Canonical product and tool names

- Message: `[PCC-D01] Use the canonical tool or product name instead of an alias.`
- Native message template: `Use '%s' instead of '%s'.`
- Source: `rude-clean-code/.vale/styles/Project/Terms.yml and accept.txt`
- Positive: `Use Pixi, Bun, ast-grep, Semgrep, Vale and Alint.`
- Negative: `Use github actions, astgrep and semgrep.`
- Implementations: `pcc-d01-canonical-terms`

### `PCC-D02` — One space after sentence punctuation

- Message: `[PCC-D02] Use exactly one space after sentence punctuation.`
- Native message template: `'%s' should have one space.`
- Source: `rude-clean-code/.vale/styles/Microsoft/Spacing.yml`
- Positive: `One sentence. Another sentence.`
- Negative: `One sentence.  Another sentence.`
- Implementations: `pcc-d02-punctuation-spacing`

### `PCC-S01` — Structured logging instead of debug prints in library code

- Message: `[PCC-S01] Replace debug printing in library code with the project's logger.`
- Source: `Archont561 explicit-output convention; doc-2 CC9xx documentation/observability rules`
- Positive: `logger.info("ready"); log::info!("ready");`
- Negative: `print("ready"); console.log("ready");; println!("ready");`
- Implementations: `pcc-s01-print-python`, `pcc-s01-console-log-ts`, `pcc-s01-println-rust`

### `PCC-S02` — Rust workspace forbids unsafe code

- Message: `[PCC-S02] Unsafe blocks are forbidden; express the operation through a reviewed safe abstraction.`
- Source: `gh-meta/Cargo.toml [workspace.lints.rust] unsafe_code = "forbid"; playtest/Cargo.toml`
- Positive: `A safe function with no unsafe block.`
- Negative: `An unsafe block around a raw operation.`
- Implementations: `pcc-s02-unsafe-rust`

### `PCC-P01` — Swallowed exceptions

- Message: `[PCC-P01] Handle, translate or rethrow the exception; pass in an except block hides the failure.`
- Source: `doc-2 CC309 broad exception swallowed; Archont561 fail-fast automation`
- Positive: `except ValueError as error: raise RuntimeError('invalid') from error`
- Negative: `except ValueError: pass`
- Implementations: `pcc-p01-swallowed-exception-python`

### `PCC-P02` — No dynamic execution or unsafe deserialization

- Message: `[PCC-P02] Avoid eval, exec, pickle and unsafe YAML loading; use a typed parser such as ast.literal_eval or yaml.safe_load.`
- Source: `Semgrep security baseline and Archont561 explicitness/locked-dependency principle`
- Positive: `ast.literal_eval(text); yaml.safe_load(text)`
- Negative: `eval(text); yaml.load(text)`
- Implementations: `pcc-p02-unsafe-dynamic-python`

### `PCC-P03` — No shell=True subprocess calls

- Message: `[PCC-P03] Pass an argument list without shell=True so command arguments cannot be reinterpreted by a shell.`
- Source: `Semgrep security baseline and Archont561 fail-fast command automation`
- Positive: `subprocess.run(['git', 'status'], check=True)`
- Negative: `subprocess.run('git status', shell=True)`
- Implementations: `pcc-p03-shell-true-python`

## Verification

<!-- SECTION:VERIFICATION:BEGIN -->
Every canonical ID keeps its `[PCC-...]` message prefix. The native levels match the severity ladder in [`docs/reference/rule-matrix.md`](../../docs/reference/rule-matrix.md): Critical is `error` in every engine, Deterministic is `warning` in Alint and `error` in ast-grep and Semgrep, and the Vale pair keeps `error` and `warning` as recorded below.

| Canonical ID | Confidence | Native rule | Native level | Prefix |
| --- | --- | --- | --- | --- |
| `PCC-R01` | critical | `pcc-r01-pixi-manifest`, `pcc-r01-pixi-lock` | `error` | present |
| `PCC-R02` | deterministic | `pcc-r02-dodo-file`, `pcc-r02-doit-config`, `pcc-r02-workflow-run-single-line` | `warning` | present |
| `PCC-R03` | deterministic | five rules, see details | `warning` | present |
| `PCC-R04` | deterministic | six rules, see details | `warning` | present |
| `PCC-D01` | critical | `pcc-d01-canonical-terms` | `error` | present |
| `PCC-D02` | deterministic | `pcc-d02-punctuation-spacing` | `warning` | present |
| `PCC-S01` | deterministic | `pcc-s01-print-python`, `pcc-s01-console-log-ts`, `pcc-s01-println-rust` | `warning` | present |
| `PCC-S02` | critical | `pcc-s02-unsafe-rust` | `error` | present |
| `PCC-P01` | critical | `pcc-p01-swallowed-exception-python` | `ERROR` | present |
| `PCC-P02` | critical | `pcc-p02-unsafe-dynamic-python` | `ERROR` | present |
| `PCC-P03` | critical | `pcc-p03-shell-true-python` | `ERROR` | present |

The three Semgrep rules also carry `metadata.pcc_confidence: critical` and `metadata.pcc_canonical_severity: error`, which agree with the `[PCC-P0x]` prefix.

### Alint behaviour

The preset was exercised against a stand-in Archont561 harness that commits `pixi.toml`, `pixi.lock`, `automation/dodo.py`, `doit.cfg`, `package.json`, `bun.lock`, `lefthook.yml`, `.versionrc`, `README.md`, `AGENTS.md`, `CONTRIBUTING.md`, `docs/README.md`, `docs/guides/development-setup.md`, `docs/concepts/rule-register.md`, and a one-line `ci.yml`.

| Run | Config | Result |
| --- | --- | --- |
| Positive | refreshed `presets/alint/recommended.yml` | `✓ All 16 rule(s) passed.`, exit 0 |
| Positive | pre-refresh preset from `2410d25` | `2 warnings`, exit 1: `pcc-r03-skills-lock`, `pcc-r04-rule-reference` |
| Negative | `bun.lock` removed | `pcc-r03-bun-lock` warning only |
| Negative | `docs/concepts/rule-register.md` removed | `pcc-r04-rule-register` warning only |
| Negative | `pixi.lock` removed | `pcc-r01-pixi-lock` error only |
| Negative | multi-line `run:` in `ci.yml` | `pcc-r02-workflow-run-single-line` warning only |

The pre-refresh run is the false-positive evidence: both retired names fire on a harness that has no skills lock. The refreshed preset reports the same harness clean and still fires each surviving rule when its target is removed.

This repository passes the refreshed preset unchanged (`✓ All 16 rule(s) passed.`), which also confirms that the two generated Pixi Sandbox workflows are excluded from the single-line rule while hand-maintained workflows remain in scope.
<!-- SECTION:VERIFICATION:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Open. Record verification evidence and the final summary when the work is complete.
<!-- SECTION:FINAL_SUMMARY:END -->
