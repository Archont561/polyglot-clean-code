---
id: PCC-21
title: Cover every tracked Python file in the Rude lint
status: Done
assignee: []
created_date: '2026-11-10 23:40'
updated_date: '2026-11-11 00:05'
labels: []
dependencies: [PCC-20]
priority: medium
type: task
ordinal: 21000
milestone: ''
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
PCC-20 scoped the Rude lint to `automation/` because Rude has no path-exclusion option and the Semgrep fixtures must stay invalid. That scoping hides any Python file added elsewhere, so this task derives the target list from the Git index instead.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Lint every tracked Python file instead of one hard-coded directory.
- [x] #2 Keep the deliberately invalid Semgrep fixtures out of the lint.
- [x] #3 Document the coverage rule and record the evidence.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Read the list from `git ls-files '*.py'` with an `:(exclude)` pathspec for `presets/semgrep/fixtures/**`, then pass the files to Rude. Fail loudly if the list is empty rather than falling back to the whole tree, which would pull the fixtures back in.
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
The lint no longer has a hard-coded target.

`tracked_python_files()` reads `git ls-files '*.py'` with an `:(exclude)` pathspec built from `PYTHON_EXCLUDES`, and `lint_python()` passes that list to `rude check --max-line-length 88`. The tree currently holds 14 tracked Python files: `automation/dodo.py` is in scope and the 13 Semgrep fixtures are excluded, because those files are deliberately invalid for the shipped rules and are asserted by Semgrep rather than by Rude. A new Python file anywhere in the tree joins the lint with no task edit. An empty list prints a message instead of falling back to the whole tree, which would immediately pull the fixtures back in.

Evidence:

| Run | Result |
| --- | --- |
| Clean tree, refreshed task | `All checks passed` |
| `scripts/probe.py` with an unused import, old command (`rude check --max-line-length 88 automation`) | `All checks passed`, which is the coverage gap |
| The same file with the new task | `scripts/probe.py:1:7: F401 'os' imported but unused` |
| `git ls-files '*.py'` | 14 files, 1 in scope, 13 excluded by pathspec |
| CI on the change (run [42891556748](https://github.com/Archont561/polyglot-clean-code/actions/runs/42891556748)) | `Fresh scaffold checks` passed with the new task in `doit ci` |
| `alint check . -c .alint.yml --fail-on-warning` | 22 of 22 |

The probe file was created with `git add -N` so the index listed it without a commit, then removed with `git rm --cached`, which is why the final tree carries no trace of it.

Documentation: [`docs/guides/running-the-checks.md`](../../docs/guides/running-the-checks.md) names tracked-file coverage, [`docs/concepts/engine-limits.md`](../../docs/concepts/engine-limits.md) explains the pathspec exclusion and the empty-list guard, and `README.md` matches. The remaining open task is PCC-10.
<!-- SECTION:FINAL_SUMMARY:END -->
