---
id: PCC-12
title: Publish the first release
status: Done
assignee: []
created_date: '2026-11-10 14:30'
updated_date: '2026-11-10 21:20'
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
- [x] #1 Verify the tag against pixi.toml.
- [x] #2 Render the Convco changelog.
- [x] #3 Attach the preset archives to the release.
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
The first release is published: [`v0.1.0`](https://github.com/Archont561/polyglot-clean-code/releases/tag/v0.1.0) on the `main` merge commit `411099d`. The tag is annotated and points at the merge of PR #8.

Acceptance criteria:

1. The tag matches `pixi.toml`. `doit build-release` compares `v0.1.0` with `[workspace] version = "0.1.0"`, and the same function rejects `v0.2.0` with `Tag 'v0.2.0' does not match workspace version '0.1.0'`.
2. The Convco changelog is rendered. The release workflow ran `pixi run --locked doit build-release`, which wrote the Convco output to `dist/release-notes.md`, and that file became the release body: 2014 characters with a `## v0.1.0 (2026-11-10)` section and per-commit links.
3. The preset archives are attached. The release carries four tarballs and the checksum file:

| Asset | Size | SHA-256 |
| --- | --- | --- |
| `polyglot-clean-code-presets-alint-0.1.0.tar.gz` | 1919 B | `b76a7fad…ebd7a` |
| `polyglot-clean-code-presets-vale-0.1.0.tar.gz` | 2283 B | `cfba1b39…28c25` |
| `polyglot-clean-code-presets-ast-grep-0.1.0.tar.gz` | 3975 B | `ec50b6e5…0e07` |
| `polyglot-clean-code-presets-semgrep-0.1.0.tar.gz` | 3087 B | `c0f0187a…78caa` |
| `SHA256SUMS-0.1.0.txt` | 456 B | — |

The published digests, read back through the GitHub API, are identical to a local `doit presets-archive` run, so the archives are reproducible byte for byte and a consumer can verify a download against `SHA256SUMS-0.1.0.txt`.

Workflow evidence: release run [42885452582](https://github.com/Archont561/polyglot-clean-code/actions/runs/42885452582) on tag `v0.1.0`. The `Validate tag and changelog` job passed in 26 seconds, including `doit build-release` and `doit ci`; the `Publish release assets` job passed in 23 seconds, including `doit build-release` and `gh release create`. The publishing job is the only writer in the repository, and its `contents: write` is job-scoped so the workflow-level `contents: read` stays intact.

Consumer adoption now has a stable pin: [`docs/guides/adopting-presets.md`](../../docs/guides/adopting-presets.md) names `v0.1.0` as the tag selector and the release assets as the download path for a consumer that does not use a submodule. The procedure lives in [`docs/guides/running-the-checks.md`](../../docs/guides/running-the-checks.md). With PCC-12 Done, PCC-10 is the remaining open task.
<!-- SECTION:FINAL_SUMMARY:END -->
