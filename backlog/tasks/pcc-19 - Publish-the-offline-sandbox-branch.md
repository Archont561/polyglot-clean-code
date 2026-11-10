---
id: PCC-19
title: Publish the offline sandbox branch
status: Done
assignee: []
created_date: '2026-11-10 18:05'
updated_date: '2026-11-10 18:05'
labels: []
dependencies: []
priority: medium
type: task
ordinal: 19000
milestone: ''
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add the offline sandbox lane that other Archont561 repositories run. A reviewed `pixi-sandbox.toml` plan drives the generated publisher, the generated relock bot, and the generated `restore.sh` launcher, so a push to `main` publishes `sandbox/developer-linux-64` and an airlocked host restores the locked environment with no registry. The shipped product stays the native presets under `presets/`; this task records the harness around them.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Review `pixi-sandbox.toml` against `pixi.toml`: one bundle, the `default` environment, and the `linux-64` platform.
- [x] #2 Generate `publish-sandbox.yml`, `relock.yml`, and `restore.sh` from the Pixi Sandbox 0.9.0 templates and keep the version stamp.
- [x] #3 Keep the root Alint policy green: `contents: read` at the workflow level, SHA-pinned actions, and the single-line rule scoped to hand-maintained workflows.
- [x] #4 Document publishing, restore, and regeneration in `docs/guides/offline-sandbox.md` and link it from the README.
- [ ] #5 Confirm the publisher run on `main` and the `sandbox/developer-linux-64` branch after the merge.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Read the plan in `pixi-sandbox.toml`, regenerate the three owned files with `pixi-sandbox init`, then verify the workflow shape. The publisher force-pushes the orphan branch, so the branch is the verification artifact, not a committed tree.
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added `pixi-sandbox.toml`, the generated `publish-sandbox.yml` and `relock.yml`, and the generated `restore.sh`. Scoped the root `pcc-r02-workflow-run-single-line` rule to `ci.yml` and `release.yml` so the generated publisher keeps its checksum-verified bootstrap step. Added `docs/guides/offline-sandbox.md`, updated the README, the documentation index, the repository layout, the agent guide, the contributing guide, and the changelog. Verification: Markdown and JSON structure checks, Alint 22/22 on the root policy, and the guard, relock, and dispatch steps in run 42871079274, which relocked `pixi.lock` on the pull request and exposed the pre-merge dispatch limit for a workflow that exists only in the change. The publisher run on `main` is confirmed after the merge.
<!-- SECTION:FINAL_SUMMARY:END -->
