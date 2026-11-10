---
id: PCC-24
title: Expand Go and Java detection fixtures
status: In Progress
assignee: []
created_date: '2026-11-10 21:00'
labels: []
dependencies: [PCC-23]
priority: medium
type: task
ordinal: 24000
milestone: ''
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Expand the compiled Go and Java examples and check whether the Pedantic rules detect the intended issues without flagging clean examples.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Add clean and flawed Go and Java examples covering print variants and handled and empty catches.
- [x] #2 Assert individual rule IDs and locations, including the absence of unexpected findings.
- [ ] #3 Verify the examples compile and checks pass in CI; document the results and limits.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Add dependency-free files to the existing compiled corpus. Annotate each expected diagnostic at its start line and compare the full multiset of locations and rule IDs against the scan output.
<!-- SECTION:PLAN:END -->
