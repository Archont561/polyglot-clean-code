---
id: PCC-12
title: Publish the first release
status: To Do
assignee: []
created_date: '2026-11-10 14:30'
updated_date: '2026-11-10 18:30'
labels: []
dependencies: []
priority: low
type: task
ordinal: 12000
milestone: ''
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Publish the first release as part of the reusable Clean Code preset distribution. Evidence, acceptance criteria, and verification stay in this record.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Verify the tag against pixi.toml.
- [ ] #2 Render the Convco changelog.
- [ ] #3 Attach the preset archives to the release.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Review `docs/concepts/rule-register.md`, update the native config and the matching backlog task together, then run `pixi run --locked doit ci`.
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Open. Record verification evidence when the work is complete.
<!-- SECTION:FINAL_SUMMARY:END -->
