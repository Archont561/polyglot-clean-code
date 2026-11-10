---
id: PCC-20
title: Lint Python with Rude and the Clean Code plugin
status: Done
assignee: []
created_date: '2026-11-10 22:10'
updated_date: '2026-11-10 23:05'
labels: []
dependencies: []
priority: medium
type: task
ordinal: 20000
milestone: ''
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The presets defer numeric Clean Code limits to an AST engine. This task applies that engine to this repository's own Python: `rude` with the `rude-clean-code` plugin, pinned in the Pixi environment and wired into the policy chain.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Pin `rude` and `rude-clean-code` as PyPI dependencies and record the Rude configuration.
- [x] #2 Run the plugin over the hand-written Python and fix every finding.
- [x] #3 Wire the lint into `doit policy` and document the change.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Add the dependencies to `pixi.toml`, let the relock bot refresh `pixi.lock`, and keep `automation/` the only Python target because the Semgrep fixtures are deliberately invalid. Fix the findings with helper extraction rather than raising a threshold.
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
The AST engine the presets defer to now lints this repository's own Python.

- `pixi.toml` pins `rude==0.1a4` and `rude-clean-code==0.1.0` under `[pypi-dependencies]`. This sandbox has no Pixi and no conda-forge access, so the `relock` bot produced the `pixi.lock` refresh in `22a2359` (run [42887252796](https://github.com/Archont561/polyglot-clean-code/actions/runs/42887252796): guard failed on the stale lock, relock succeeded and pushed the bot commit).
- `doit lint-python` runs `rude check --max-line-length 88 automation` and sits in both `policy` and `pre-commit`, so `doit ci` and the Lefthook hook cover it. The target is `automation/` alone because `presets/semgrep/fixtures/` must stay invalid for the shipped Semgrep rules.
- The width is a command-line flag, not a configuration file. `.gitignore` excludes `pyproject.toml` on purpose, so an initial attempt at committing one was ignored and the first CI run linted at the default 79 characters. The fix moved the width into the task and was verified in CI.
- Every finding was fixed by extraction rather than a raised threshold: `build_preset_archives` split into `_reproducible_entry`, `_add_entry`, `_archive_tool`, `_pack_preset`, and `_write_checksums` for `CC101`, `CC104`, and `CC301`; `check_commit_messages` gained a named `_has_commit_range` predicate for `CC302`; and one 90-character line was wrapped for `E501`.

Evidence:

| Run | Result |
| --- | --- |
| `rude check automation` before | `CC101`, `CC104`, `CC301`, `CC302`, and 14 `E501` errors |
| `rude check --max-line-length 88 automation` after | `All checks passed` |
| Rebuilt release archives | digests identical to the published `v0.1.0` assets |
| Job-per-task probe (run 42887517767) | `lint-python` was the only failing task; `alint`, `lint-prose`, `docs-lint`, `actionlint`, `ast-grep-test`, `semgrep-validate`, and `backlog` all passed |
| CI on the final head (run [42888214603](https://github.com/Archont561/polyglot-clean-code/actions/runs/42888214603)) | `Fresh scaffold checks` succeeded, including `doit ci` with the new task |

Two process notes worth keeping. The probe workflow was the only way to see a failing task, because this sandbox cannot download Actions logs; it reported through check-run annotations, which the API exposes. Its commits also used the scope `diagnose`, which `.versionrc` does not allow, so the Conventional Commit step rejected the range; those commits were dropped before the merge and the remaining history uses only allowed scopes.

Documentation: `doit lint-python` appears in [`docs/guides/running-the-checks.md`](../../docs/guides/running-the-checks.md), [`docs/concepts/engine-limits.md`](../../docs/concepts/engine-limits.md) records the dogfooding split, and `README.md` keeps the promise that the distribution still ships no linter.
<!-- SECTION:FINAL_SUMMARY:END -->
