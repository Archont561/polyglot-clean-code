# Documentation standard

## Source of truth

Write maintained documentation under `docs/`, `backlog/tasks/`, and root Markdown files. `README.md` is hand-maintained; edit it directly. The rule register lives in three To Do backlog tasks, one per preset. Concept notes live in `docs/concepts/rule-register.md` and `docs/concepts/engine-limits.md`. Vale checks the prose of `docs/`, the root Markdown files, and `presets/README.md`; markdownlint-cli2 additionally checks `backlog/tasks/` and the preset Markdown trees.

## Vale policy

Use `Pixi`, `Bun`, `Convco`, `Backlog.md`, `Alint`, `Vale`, `ast-grep`, `Semgrep`, and `markdownlint-cli2` with canonical spelling. Use `GitHub Actions` for the product name. Write `https://` links. Use one space after sentence punctuation. State measured values instead of vague intensifiers. Name a task reference when a decision is pending.

Vale styles are vendored per preset. The root `.vale.ini` uses the Strict style tree. `doit lint-prose` checks maintained documents and excludes reference tables from prose rules because they quote negative examples.

## Markdown policy

markdownlint-cli2 runs through Bun. Long reference tables are allowed. Heading duplication and inline HTML are disabled. Every maintained document starts with a level-one heading or Backlog.md frontmatter.

## Structure policy

Alint checks repository and documentation structure through `PCC-R02` and `PCC-R04`: maintained entrypoints, a single doit registry, and one-line workflow `run` steps. `doit policy` and `doit ci` include the Alint check. Vale checks prose and markdownlint-cli2 checks Markdown syntax; all three run over maintained documents.

## Task records

Backlog.md tasks need an ID, title, status, acceptance criteria, implementation plan, and final summary. Do not mark a criterion complete without evidence. Use `--plain` for CLI reads in non-interactive shells.
