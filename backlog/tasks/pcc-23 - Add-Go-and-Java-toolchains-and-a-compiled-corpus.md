---
id: PCC-23
title: Add Go and Java toolchains and a compiled corpus
status: In Progress
assignee: []
created_date: '2026-11-11 02:10'
updated_date: '2026-11-11 02:10'
labels: []
dependencies: [PCC-10]
priority: medium
type: task
ordinal: 23000
milestone: ''
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
PCC-10 measured the Go and Java rules on a corpus that lived outside the repository, which made the measurement unrepeatable. This task pins the toolchains, ships the corpus, and turns the measurement into a CI assertion.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Pin the Go and Java toolchains in `pixi.toml` and let the relock bot refresh the lock.
- [ ] #2 Ship the corpus under `presets/ast-grep/pedantic/examples` and compile it in CI.
- [ ] #3 Assert the exact Pedantic findings on every CI run.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Keep the corpus small and dependency-free: Go uses `log/slog` from the standard library and Java uses `java.util.logging`, so the compilation needs no third-party artifacts. The assertion compares a counted map against a constant, so a rule that stops matching fails the build instead of passing quietly.
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Open. Record verification evidence when the work is complete.
<!-- SECTION:FINAL_SUMMARY:END -->
