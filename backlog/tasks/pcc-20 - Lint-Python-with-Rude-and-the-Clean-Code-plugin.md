---
id: PCC-20
title: Lint Python with Rude and the Clean Code plugin
status: In Progress
assignee: []
created_date: '2026-11-10 22:10'
updated_date: '2026-11-10 22:10'
labels: []
dependencies: []
priority: medium
type: task
ordinal: 20000
milestone: ''
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The presets defer numeric Clean Code limits to an AST engine. This task applies that engine to this repository's own Python: `rude` with the `rude-clean-code` plugin, pinned in the Pixi environment and wired into the policy chain.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Pin `rude` and `rude-clean-code` as PyPI dependencies and record the Rude configuration.
- [ ] #2 Run the plugin over the hand-written Python and fix every finding.
- [ ] #3 Wire the lint into `doit policy` and document the change.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Add the dependencies to `pixi.toml`, let the relock bot refresh `pixi.lock`, and keep `automation/` the only Python target because the Semgrep fixtures are deliberately invalid. Fix the findings with helper extraction rather than raising a threshold.
<!-- SECTION:PLAN:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Open. Record verification evidence when the work is complete.
<!-- SECTION:FINAL_SUMMARY:END -->
