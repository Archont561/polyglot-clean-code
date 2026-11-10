---
id: PCC-23
title: Add Go and Java toolchains and a compiled corpus
status: Done
assignee: []
created_date: '2026-11-11 02:10'
updated_date: '2026-11-11 03:05'
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
- [x] #1 Pin the Go and Java toolchains in `pixi.toml` and let the relock bot refresh the lock.
- [x] #2 Ship the corpus under `presets/ast-grep/pedantic/examples` and compile it in CI.
- [x] #3 Assert the exact Pedantic findings on every CI run.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Keep the corpus small and dependency-free: Go uses `log/slog` from the standard library and Java uses `java.util.logging`, so the compilation needs no third-party artifacts. The assertion compares a counted map against a constant, so a rule that stops matching fails the build instead of passing quietly.
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
`pixi.toml` pins `go = ">=1.23,<2"` and `openjdk = ">=21,<22"`. The relock bot did the solve, not a hand edit: commit `1afdd13 chore(lock): refresh lockfiles for #13` took the lock from 53 to 90 conda blobs and resolved `go-1.27.3` and `openjdk-21.0.10`.

The corpus ships under `presets/ast-grep/pedantic/examples`: a Go module with `clean` and `dirty` packages, and two Java classes. Both avoid third-party artifacts on purpose — `log/slog` and `java.util.logging` — so the compile step needs nothing beyond the toolchains.

`doit examples` runs in three actions: `go build ./...` in the module, `javac` over the Java sources into `dist/java-classes`, and a counted comparison against `{pcc-s01-print-go: 2, pcc-s01-print-java: 3, pcc-s07-empty-catch-java: 1}`; a rule that stops matching fails the build instead of passing quietly. It is a `policy` dependency, so `ci` runs it.

Verified by the green `Fresh scaffold checks` run 42895881474 on `1afdd13`: `pixi run --locked doit ci` passed with the toolchains installed, so the corpus compiles and the findings match. Local substitutes covered the rest — `ast-grep test` 4/7/13, Alint 22 rules, markdownlint 0, rude clean.

The published transport took the cost: 165 blobs at 477.2 MiB packed against 1530.6 MiB unpacked, up from 126 blobs at 223.5 MiB, with OpenJDK as the largest blob at 177.8 MiB. `docs/guides/offline-sandbox.md` carries the new baseline. A slimmer JDK, or moving the compilers into a second environment, is the obvious follow-up if the transport size ever matters.
<!-- SECTION:FINAL_SUMMARY:END -->
