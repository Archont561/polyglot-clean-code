---
id: PCC-22
title: Move the airlock launcher into scripts/
status: Done
assignee: []
created_date: '2026-11-11 02:10'
updated_date: '2026-11-11 03:05'
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
- [x] #1 Move the generated launcher and keep its stamp and executable bit.
- [x] #2 Update the generator input the publisher records and every document that names the path.
- [x] #3 Verify the launcher still resolves the repository root from its new location.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
The launcher resolves `ROOT` with `git rev-parse --show-toplevel`, so its own location does not matter to its logic. What does matter is the `--script-path` value the publisher passes to `pixi-sandbox upgrade`; regenerate with the same value after this change.
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
The launcher lives at `scripts/restore.sh` with its stamp (`pixi-sandbox-version: 0.9.0`) and its `100755` mode intact; `git mv` recorded the move as a rename, so the file's history follows it.

The publisher's `upgrade` step now passes `--script-path scripts/restore.sh`, and every document that named the path follows: `README.md`, `AGENTS.md`, `CONTRIBUTING.md`, `docs/guides/offline-sandbox.md`, and `docs/reference/repository-layout.md`. The offline guide states the regeneration value next to the "never edit them by hand" rule, because the path is a generator input rather than a file the tool searches for.

`sh -n scripts/restore.sh` parses, and the launcher derives its root from `git rev-parse --show-toplevel`, so nothing about its behaviour depended on sitting at the top level.

One consequence worth recording: the publisher takes the launcher path as input, so the next `pixi-sandbox init` for this repository must be run with `--script-path scripts/restore.sh`. Regenerating without it puts the launcher back at the root and the working tree disagrees with the publisher.

Verified by the green `Fresh scaffold checks` run 42895881474 on `1afdd13`, which covers the move because the tracked tree no longer carries a root launcher.
<!-- SECTION:FINAL_SUMMARY:END -->
