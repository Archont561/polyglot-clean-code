---
id: PCC-22
title: Move the airlock launcher into scripts/
status: In Progress
assignee: []
created_date: '2026-11-11 02:10'
updated_date: '2026-11-11 02:10'
labels: []
dependencies: [PCC-19]
priority: low
type: task
ordinal: 22000
milestone: ''
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The generated launcher sat at the repository root and made the root look like it owned a shell script. It moves to `scripts/restore.sh`. The launcher path is a `pixi-sandbox init` input, so the move is a plan-and-generator change rather than a file rename.

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Move the generated launcher and keep its stamp and executable bit.
- [ ] #2 Update the generator input the publisher records and every document that names the path.
- [ ] #3 Verify the launcher still resolves the repository root from its new location.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
The launcher resolves `ROOT` with `git rev-parse --show-toplevel`, so its own location does not matter to its logic. What does matter is the `--script-path` value the publisher passes to `pixi-sandbox upgrade`; regenerate with the same value after this change.
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Open. Record verification evidence when the work is complete.
<!-- SECTION:FINAL_SUMMARY:END -->
