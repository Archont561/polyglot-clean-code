---
id: PCC-18
title: Refresh Pedantic preset rules
status: To Do
assignee: []
created_date: '2026-11-10 18:30'
updated_date: '2026-11-10 18:30'
labels: []
dependencies: [PCC-17]
priority: medium
type: task
ordinal: 18000
milestone: ''
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Continue the dev loop after PCC-17 is Done. This task holds the 9 canonical rules first exposed in the Pedantic preset. The native configs under `presets/` remain the shipped product; this task is the reviewed rule register. No catalogue file and no generator are used.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Review every listed `PCC-*` ID against its native config under `presets/`.
- [ ] #2 Confirm the `[PCC-...]` message prefix, confidence, and native severity for each rule.
- [ ] #3 Update the native config and this task in the same change; keep paired positive and negative examples.
- [ ] #4 Run `pixi run --locked doit ci` and record the verification evidence here.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Work one ID at a time. Read the rule details below, open the matching native config, adjust the rule, then update this task. Finish with `doit ci`. Close the first dev loop when this task is Done.
<!-- SECTION:PLAN:END -->

## Rule inventory

| ID | Tool | Title | Confidence | Native IDs |
| --- | --- | --- | --- | --- |
| `PCC-R07` | alint | Every custom rule has paired tests | heuristic | pcc-r07-rule-test-dirs |
| `PCC-R08` | alint | Conventional Commit and Backlog policy values | deterministic | pcc-r08-convco-types, pcc-r08-backlog-statuses |
| `PCC-D05` | vale | No placeholder prose | heuristic | pcc-d05-placeholders |
| `PCC-D06` | vale | Meaningful headings | deterministic | pcc-d06-generic-headings |
| `PCC-S06` | ast-grep | Configuration at the boundary | deterministic | pcc-s06-process-env-ts |
| `PCC-S07` | ast-grep | No empty TypeScript catch blocks | deterministic | pcc-s07-empty-catch-ts |
| `PCC-S08` | ast-grep | No bare Python except with pass | deterministic | pcc-s08-bare-except-python |
| `PCC-P07` | semgrep | Immutable dependency and action references | critical | pcc-p07-immutable-references |
| `PCC-P08` | semgrep | Rust workspace lints stay forbidding | critical | pcc-p08-rust-unsafe-lint |

## Rule details

### `PCC-R07` — Every custom rule has paired tests

- Message: `[PCC-R07] Every distributed rule needs a positive test target and a negative test target beside its config.`
- Source: `rude-clean-code pytest-bdd/hypothesis test layout; doc-2 detection contracts`
- Positive: `rule test directories and paired fixture directories exist`
- Negative: `a rule exists without a negative example`
- Implementations: `pcc-r07-rule-test-dirs` (file_exists)

### `PCC-R08` — Conventional Commit and Backlog policy values

- Message: `[PCC-R08] Keep Conventional Commit types and Backlog statuses inside their approved vocabularies.`
- Source: `rude-clean-code/.versionrc and backlog/config.yml; PyShellForge and qgis-sdk equivalents`
- Positive: `.versionrc uses approved types and backlog/config.yml uses approved statuses`
- Negative: `.versionrc declares an unapproved commit type`
- Implementations: `pcc-r08-convco-types` (yaml_path_matches), `pcc-r08-backlog-statuses` (yaml_path_matches)

### `PCC-D05` — No placeholder prose

- Message: `[PCC-D05] Replace placeholders with a decision, a task reference or a concrete statement.`
- Source: `doc-2 CC903 (markers need a reference) and Archont561 backlog-first documentation`
- Positive: `The release checklist is recorded in PCC-4.`
- Negative: `TBD. Lorem ipsum and coming soon text.`
- Implementations: `pcc-d05-placeholders`

### `PCC-D06` — Meaningful headings

- Message: `[PCC-D06] Replace a generic heading with a heading that names the decision or procedure.`
- Source: `Archont561 documentation tree and doc-2 explicitness principle`
- Positive: `## Development setup`
- Negative: `## Misc stuff`
- Implementations: `pcc-d06-generic-headings`

### `PCC-S06` — Configuration at the boundary

- Message: `[PCC-S06] Read process.env at the entrypoint and inject a typed configuration object into library code.`
- Source: `doc-2 CC7xx config-driven dependency rules and Archont561 activation.env boundary`
- Positive: `const port = config.port;`
- Negative: `const port = process.env.PORT;`
- Implementations: `pcc-s06-process-env-ts`

### `PCC-S07` — No empty TypeScript catch blocks

- Message: `[PCC-S07] Handle, translate or rethrow a caught error; an empty catch hides the failure.`
- Source: `doc-2 CC309 broad exception swallowed and fail-fast family`
- Positive: `catch (error) { logger.error(error); }`
- Negative: `catch (error) {}`
- Implementations: `pcc-s07-empty-catch-ts`

### `PCC-S08` — No bare Python except with pass

- Message: `[PCC-S08] Catch a specific exception and handle it explicitly; never discard a bare exception.`
- Source: `doc-2 CC309 broad exception swallowed and CC310 exception chaining`
- Positive: `except ValueError as error: raise RuntimeError('invalid') from error`
- Negative: `except: pass`
- Implementations: `pcc-s08-bare-except-python`

### `PCC-P07` — Immutable dependency and action references

- Message: `[PCC-P07] Replace wildcard dependency versions and mutable action tags with a lockfile or full commit SHA.`
- Source: `gh-meta/deny.toml bans wildcards; Archont561 workflows pin actions to full SHAs`
- Positive: `version = "1.2.3"; uses: actions/checkout@<40-char-sha>`
- Negative: `version = "*"; uses: actions/checkout@v7`
- Implementations: `pcc-p07-immutable-references`

### `PCC-P08` — Rust workspace lints stay forbidding

- Message: `[PCC-P08] Keep unsafe_code forbidden in Rust workspace lints; do not downgrade it to warn or allow.`
- Source: `gh-meta/Cargo.toml and playtest/Cargo.toml [workspace.lints.rust] unsafe_code = "forbid"`
- Positive: `unsafe_code = "forbid"`
- Negative: `unsafe_code = "warn"`
- Implementations: `pcc-p08-rust-unsafe-lint`

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Open. Record verification evidence and the final summary when the work is complete.
<!-- SECTION:FINAL_SUMMARY:END -->
