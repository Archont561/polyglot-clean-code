# Architecture overview

The repository has three layers and no runtime wrapper.

## Rule register layer

`backlog/tasks/` holds three To Do preset tasks. They record 30 canonical `PCC-*` rules, grouped by the preset that first exposes them. Each rule stores an ID, title, message, Archont561 evidence, confidence, first preset, paired examples, and native implementation IDs. There is no `presets/catalogue.yml` and no contract helper module. See [`docs/concepts/rule-register.md`](../concepts/rule-register.md).

## Native layer

Each preset is self-contained under `presets/`. Alint files use `version: 1` rules. Vale ini files point at a preset-specific vendored style tree. ast-grep projects contain `sgconfig.yml`, `rules/`, and `rule-tests/`. Semgrep preset files compose native rules with metadata and annotated fixtures under `presets/semgrep/fixtures/`.

## Automation layer

`automation/dodo.py` is the only file under `automation/`. It owns every local check, hook, and CI entrypoint. Pixi locks the environment. Bun locks Backlog.md and markdownlint-cli2. Lefthook and GitHub Actions call doit through one-line commands. Convco checks commit messages. Vale checks prose, markdownlint-cli2 checks Markdown structure, and Alint checks repository and documentation structure.

## Design boundary

Project-wide metrics, inheritance graphs, line counts, returns, locals, and method counts belong to a dedicated AST plugin. The four engines here express structure, prose, patterns, and configuration. A rule that cannot be expressed honestly is deferred rather than faked. The rule register is defined in [Rule register](../concepts/rule-register.md); the boundary is detailed in [Engine limits versus Rude Clean Code](../concepts/engine-limits.md).
