---
id: PCC-10
title: Add Go and Java structural rules
status: To Do
assignee: []
created_date: '2026-11-10 14:30'
updated_date: '2026-11-10 18:30'
labels: []
dependencies: []
priority: medium
type: task
ordinal: 10000
milestone: ''
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add Go and Java structural rules as part of the reusable Clean Code preset distribution. Evidence, acceptance criteria, and verification stay in this record.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Inspect Archont561 evidence for Go and Java before proposing a rule.
- [ ] #2 Add paired valid and invalid ast-grep cases for each new rule.
- [ ] #3 Measure false-positive counts before enabling Pedantic.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Review `docs/concepts/rule-register.md`, update the native config and the matching backlog task together, then run `pixi run --locked doit ci`.
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Open. Record verification evidence when the work is complete.
<!-- SECTION:FINAL_SUMMARY:END -->
