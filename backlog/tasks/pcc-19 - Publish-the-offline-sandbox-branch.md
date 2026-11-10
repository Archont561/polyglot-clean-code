---
id: PCC-19
title: Publish the offline sandbox branch
status: Done
assignee: []
created_date: '2026-11-10 18:05'
updated_date: '2026-11-10 18:15'
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
- [x] #5 Confirm the publisher run on `main` and the `sandbox/developer-linux-64` branch after the merge.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Read the plan in `pixi-sandbox.toml`, regenerate the three owned files with `pixi-sandbox init`, then verify the workflow shape. The publisher force-pushes the orphan branch, so the branch is the verification artifact, not a committed tree.
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added `pixi-sandbox.toml`, the generated `publish-sandbox.yml` and `relock.yml`, and the generated `restore.sh`. Scoped the root `pcc-r02-workflow-run-single-line` rule to `ci.yml` and `release.yml` so the generated publisher keeps its checksum-verified bootstrap step. Added `docs/guides/offline-sandbox.md`, updated the README, the documentation index, the repository layout, the agent guide, the contributing guide, and the changelog. Verification: Markdown and JSON structure checks, Alint 22/22 on the root policy, and the guard, relock, and dispatch steps in run 42871079274, which relocked `pixi.lock` on the pull request and exposed the pre-merge dispatch limit for a workflow that exists only in the change. Publisher proof after the merge: dispatched run 42872400210 completed green through `setup-pixi`, the release bootstrap, `Pack, verify, and publish`, and the diagnostic upload; it pushed `sandbox/developer-linux-64` at 84ac7d7 as `pixi-sandbox[bot]`, an orphan snapshot commit for schema 5. The manifest records source commit 5e8b62d, a `lock_sha256` equal to `sha256sum pixi.lock`, 126 blobs at 223.5 MiB packed against 871.3 MiB unpacked, a largest blob of 48.2 MiB against the 95 MiB default, and matching SHA-256 digests for `files.json`, both bundled tools (Pixi 0.84.1 and Pixi Sandbox 0.9.0, both static), and a six-blob spot check. `restore.sh` resolves `sandbox/developer-linux-64` from `pixi-sandbox.toml` before it fetches. The first attempt, run 42871745374, failed in `setup-pixi` with `Cannot cache without running install`; the re-rendered `cache: false` in 5e8b62d matches the plan and fixed it.
<!-- SECTION:FINAL_SUMMARY:END -->
