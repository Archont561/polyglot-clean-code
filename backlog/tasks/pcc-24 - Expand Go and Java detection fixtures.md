---
id: PCC-24
title: Expand Go and Java detection fixtures
status: Done
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
- [x] #3 Verify the examples compile and checks pass in CI; document the results and limits.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Add dependency-free files to the existing compiled corpus. Annotate each expected diagnostic at its start line and compare the full multiset of locations and rule IDs against the scan output.
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added clean and flawed, dependency-free Go and Java examples for direct print variants, structured logging, formatted strings, handled exceptions, and empty catches. Each expected finding carries a marker at its start line; the comparison includes file, line and rule ID, and rejects unexpected and missing diagnostics separately. The expanded corpus has 13 expected findings (5 Go print, 6 Java print, and 2 Java empty-catch). Java `System.out.printf` remains outside the current rule scope; this synthetic corpus is not a real-world false-positive measurement.

The native ast-grep tests passed for all three presets (4, 7, and 13). Local scans matched all 13 markers; Rude, Alint and markdownlint passed. CI run 42899194473 passed on commit `99f1a8d`, compiling both languages with the pinned toolchains and running the full check suite.
<!-- SECTION:FINAL_SUMMARY:END -->
