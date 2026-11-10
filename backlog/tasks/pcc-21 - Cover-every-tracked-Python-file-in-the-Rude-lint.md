---
id: PCC-21
title: Cover every tracked Python file in the Rude lint
status: In Progress
assignee: []
created_date: '2026-11-10 23:40'
updated_date: '2026-11-10 23:40'
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
- [ ] #1 Lint every tracked Python file instead of one hard-coded directory.
- [ ] #2 Keep the deliberately invalid Semgrep fixtures out of the lint.
- [ ] #3 Document the coverage rule and record the evidence.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Read the list from `git ls-files '*.py'` with an `:(exclude)` pathspec for `presets/semgrep/fixtures/**`, then pass the files to Rude. Fail loudly if the list is empty rather than falling back to the whole tree, which would pull the fixtures back in.
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Open. Record verification evidence when the work is complete.
<!-- SECTION:FINAL_SUMMARY:END -->
