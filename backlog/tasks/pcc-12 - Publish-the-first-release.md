---
id: PCC-12
title: Publish the first release
status: In Progress
assignee: []
created_date: '2026-11-10 14:30'
updated_date: '2026-11-10 21:05'
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
The tag `v0.1.0` matches the workspace version already declared in `pixi.toml`. The release path needs three pieces before the tag is worth pushing: a reproducible archive task, a publish job that uploads the assets, and a rendered changelog to use as the release body. Then push the tag and record what GitHub reports back.
<!-- SECTION:PLAN:END -->

## Verification

<!-- SECTION:VERIFICATION:BEGIN -->
`pixi.toml` declares `version = "0.1.0"` under `[workspace]`. `doit build-release --ref v0.1.0` compares the tag against that value with the `v` prefix removed, and a mismatched tag stops the run:

| Run | Result |
| --- | --- |
| `build_release("v0.1.0")` | `Release validation passed for version 0.1.0` |
| `build_release("v0.2.0")` | `Tag 'v0.2.0' does not match workspace version '0.1.0'` |

The Convco rendering was stubbed locally because Convco is a Pixi dependency and this sandbox has no Pixi. The stub proves the plumbing: `build_release` writes the rendered output to `dist/release-notes.md` and fails when Convco prints nothing. The real render happens in the release workflow.

`doit presets-archive` writes four tarballs and a checksum file into `dist/`, which is gitignored:

| Asset | Size |
| --- | --- |
| `polyglot-clean-code-presets-alint-0.1.0.tar.gz` | 1919 bytes |
| `polyglot-clean-code-presets-vale-0.1.0.tar.gz` | 2283 bytes |
| `polyglot-clean-code-presets-ast-grep-0.1.0.tar.gz` | 3975 bytes |
| `polyglot-clean-code-presets-semgrep-0.1.0.tar.gz` | 3087 bytes |

A second run produced byte-identical archives, so the release assets are reproducible. Each archive carries paths relative to `presets/`, for example `alint/pedantic.yml`.

The publish job is the only place in this repository with `contents: write`, and it is job-scoped: the workflow-level `permissions: contents: read` still satisfies `pcc-r05-workflow-contents-read`, the pinned `uses:` SHAs satisfy `pcc-r05-pin-actions-to-sha`, and both `run:` steps stay single-line for `pcc-r02-workflow-run-single-line`. `.alint.yml` (22 rules) and all three presets pass with the new workflow in the tree.
<!-- SECTION:VERIFICATION:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Open. Record verification evidence when the work is complete.
<!-- SECTION:FINAL_SUMMARY:END -->
