---
id: PCC-17
title: Refresh Strict preset rules
status: In Progress
assignee: []
created_date: '2026-11-10 18:30'
updated_date: '2026-11-10 19:40'
labels: []
dependencies: [PCC-16]
priority: medium
type: task
ordinal: 17000
milestone: ''
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Continue the dev loop after PCC-16 is Done. This task holds the 10 canonical rules first exposed in the Strict preset. The native configs under `presets/` remain the shipped product; this task is the reviewed rule register. No catalogue file and no generator are used.
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
Work one ID at a time. Read the rule details below, open the matching native config, adjust the rule, then update this task. Finish with `doit ci`. Move to PCC-18 when this task is Done.
<!-- SECTION:PLAN:END -->

## Rule inventory

| ID | Tool | Title | Confidence | Native IDs |
| --- | --- | --- | --- | --- |
| `PCC-R05` | alint | Least-privilege, immutable CI | critical | pcc-r05-workflow-contents-read, pcc-r05-pin-actions-to-sha, pcc-r05-issue-forms, pcc-r05-blank-issues-disabled |
| `PCC-R06` | alint | No generated or secret artifacts in source control | critical | pcc-r06-no-tracked-artifacts |
| `PCC-D03` | vale | Evidence instead of weasel words | heuristic | pcc-d03-weasel-words |
| `PCC-D04` | vale | Secure, portable links | deterministic | pcc-d04-link-hygiene |
| `PCC-S03` | ast-grep | Propagate Rust fallible results | deterministic | pcc-s03-unwrap-rust |
| `PCC-S04` | ast-grep | No Python module-level global mutation | deterministic | pcc-s04-global-python |
| `PCC-S05` | ast-grep | No nested conditional expressions | heuristic | pcc-s05-nested-ternary-ts |
| `PCC-P04` | semgrep | Network calls declare a timeout | deterministic | pcc-p04-requests-timeout-python |
| `PCC-P05` | semgrep | Preserve exception causes | deterministic | pcc-p05-exception-chaining-python |
| `PCC-P06` | semgrep | Task markers carry a reference | heuristic | pcc-p06-unreferenced-markers |

The Strict preset also ships the six native IDs first exposed in Recommended (`PCC-R01`–`PCC-R04`). Strict raises their level to `error`, which the severity ladder permits, and the refresh carried the PCC-16 wording, the rule-register rename, and the generated-workflow exclusions into the Strict copies. The authoritative details for those IDs stay in PCC-16.

## Rule details

### `PCC-R05` — Least-privilege, immutable CI

- Message: `[PCC-R05] Declare read-only workflow permissions and pin third-party actions to full commit SHAs.`
- Source: `rude-clean-code/.github/workflows/ci.yml; qgis-sdk workflows; gh-meta/deny.toml pinning discipline`
- Positive: `workflow declares permissions.contents: read and uses a 40-character action SHA`
- Negative: `workflow uses a mutable @v7 tag`
- Implementations: `pcc-r05-workflow-contents-read` (yaml_path_equals), `pcc-r05-pin-actions-to-sha` (yaml_path_matches), `pcc-r05-issue-forms` (file_exists), `pcc-r05-blank-issues-disabled` (yaml_path_equals)

### `PCC-R06` — No generated or secret artifacts in source control

- Message: `[PCC-R06] Keep environment files, dependency caches and build outputs out of the repository.`
- Source: `rude-clean-code/.gitignore and ruff.toml exclusions; alint hygiene conventions`
- Positive: `no .env, dependency cache or dist directory is present`
- Negative: `.env and dist/ are committed`
- Implementations: `pcc-r06-no-tracked-artifacts` (file_absent)

### `PCC-D03` — Evidence instead of weasel words

- Message: `[PCC-D03] Replace vague intensifiers with a measurable statement.`
- Source: `rude-clean-code/.vale/styles/write-good/Weasel.yml and doc-2 measurable diagnostics`
- Positive: `The suite completes in twelve seconds.`
- Negative: `The suite is very fast and obviously correct.`
- Implementations: `pcc-d03-weasel-words`

### `PCC-D04` — Secure, portable links

- Message: `[PCC-D04] Use HTTPS links and avoid machine-local URLs in maintained documentation.`
- Source: `Archont561 CI link checks and vendored documentation conventions`
- Positive: Read `https://docs.astral.sh/ruff/`.
- Negative: Open `http://localhost:3000` or `http://example.invalid`.
- Implementations: `pcc-d04-link-hygiene`

### `PCC-S03` — Propagate Rust fallible results

- Message: `[PCC-S03] Do not call unwrap in production code; return the error with ? or map it explicitly.`
- Source: `gh-meta/Cargo.toml unused_must_use = "deny" and Clippy pedantic; playtest Rust code`
- Positive: `let value = result?;`
- Negative: `let value = result.unwrap();`
- Implementations: `pcc-s03-unwrap-rust`

### `PCC-S04` — No Python module-level global mutation

- Message: `[PCC-S04] Pass state explicitly instead of mutating module globals from a function.`
- Source: `rude-clean-code doc-2 CC308 global statement and own-scope analysis`
- Positive: `Return a value from an explicit function.`
- Negative: `A function declares a global name.`
- Implementations: `pcc-s04-global-python`

### `PCC-S05` — No nested conditional expressions

- Message: `[PCC-S05] Extract nested conditional expressions into a named decision function or explicit branches.`
- Source: `rude-clean-code doc-2 CC306 nested ternary and CC301 excessive nesting`
- Positive: `const value = ready ? 1 : 2;`
- Negative: `const value = ready ? (ok ? 1 : 2) : 3;`
- Implementations: `pcc-s05-nested-ternary-ts`

### `PCC-P04` — Network calls declare a timeout

- Message: `[PCC-P04] Set an explicit timeout on requests calls so a stalled dependency cannot hang the process.`
- Source: `Archont561 fail-fast automation and doc-2 CC310/CC311 error-boundary rules`
- Positive: `requests.get(url, timeout=10)`
- Negative: `requests.get(url)`
- Implementations: `pcc-p04-requests-timeout-python`

### `PCC-P05` — Preserve exception causes

- Message: `[PCC-P05] Use raise ... from ... when translating an exception so the original cause remains visible.`
- Source: `doc-2 CC310 missing raise ... from; rude-clean-code BDD diagnostics`
- Positive: `raise RuntimeError('invalid') from error`
- Negative: `raise RuntimeError('invalid')`
- Implementations: `pcc-p05-exception-chaining-python`

### `PCC-P06` — Task markers carry a reference

- Message: `[PCC-P06] Attach a task or issue reference to an unfinished-work marker so it can be tracked.`
- Source: `doc-2 CC903 TODO without reference and Archont561 Backlog.md convention`
- Positive: `# Follow-up: PCC-42 reference recorded`
- Negative: `# Unfinished marker without a reference`
- Implementations: `pcc-p06-unreferenced-markers`

## Verification

<!-- SECTION:VERIFICATION:BEGIN -->
Every Strict rule keeps its `[PCC-...]` prefix. Deterministic IDs (`PCC-R05`, `PCC-R06`, `PCC-D04`, `PCC-S03`, `PCC-S04`, `PCC-P04`, `PCC-P05`) sit at `error` in Alint and ast-grep and at `ERROR` in Semgrep, which is the Strict column of [`docs/reference/rule-matrix.md`](../../docs/reference/rule-matrix.md). The heuristic IDs are `warning` in Vale and ast-grep (`PCC-D03`, `PCC-S05`, `PCC-P06`) and `off` in Semgrep, where the preset ships no heuristic rule.

`presets/alint/strict.yml` now holds 21 rules instead of 23. The two skills-lock checks are gone, `pcc-r04-rule-reference` became `pcc-r04-rule-register`, the `PCC-R03` and `PCC-R04` messages match the refreshed Recommended preset, and `pcc-r02-workflow-run-single-line` excludes the two workflows that `pixi-sandbox init` generates. At `error` level those exclusions matter: without them a consumer that adopts Pixi Sandbox fails its own preset.

| Run | Target | Result |
| --- | --- | --- |
| Positive | this repository, refreshed preset | `✓ All 21 rule(s) passed.` |
| Positive | this repository, pre-refresh preset | `5 errors` in three rules: `pcc-r03-skills-lock`, `pcc-r04-rule-reference`, and `pcc-r02-workflow-run-single-line` three times on the generated workflows |
| Contrast | this repository, exclusions stripped | `3 errors`, all `pcc-r02-workflow-run-single-line` |
| Negative | `bun.lock` removed | `pcc-r03-bun-lock` only |
| Negative | `docs/concepts/rule-register.md` removed | `pcc-r04-rule-register` only |
| Negative | multi-line `run:` in `ci.yml` | `pcc-r02-workflow-run-single-line` only |
| Negative | SHA pin replaced with `actions/checkout@v7` | `pcc-r05-pin-actions-to-sha` only |
| Negative | `permissions: contents: read` removed from `ci.yml` | `pcc-r05-workflow-contents-read` only |

`PCC-R06` needs a note. Alint's tree walk honours `.gitignore`, and every path this rule names (`.env`, `.DS_Store`, `dist/**`, `build/**`, `.venv/**`) is gitignored in the Archont561 layout, so the rule stays quiet on a clean checkout and fires only when a consumer leaves those paths unignored. The same tree reports three findings under `--no-gitignore`, which proves the rule and the paths are sound. `git_tracked_only: true` is not a workaround: it did not fire on force-added paths in this build and raises an analysis failure outside a Git repository. The preset therefore keeps the walk-based default, and [`docs/concepts/engine-limits.md`](../../docs/concepts/engine-limits.md) records the boundary.
<!-- SECTION:VERIFICATION:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Open. Record verification evidence and the final summary when the work is complete.
<!-- SECTION:FINAL_SUMMARY:END -->
