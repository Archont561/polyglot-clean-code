# Rule register

The rule register lives in `backlog/tasks/`, not in a catalogue file and not in generated code. Three To Do tasks hold the 30 canonical `PCC-*` rules, grouped by the preset that first exposes them.

| Task | Preset | Rules |
| --- | --- | --- |
| `PCC-16` | Recommended | 11 |
| `PCC-17` | Strict | 10 |
| `PCC-18` | Pedantic | 9 |

Each task records the ID, tool, title, message, Archont561 source, confidence, paired positive and negative examples, and native implementation IDs. The native configs under `presets/` remain the shipped product. A rule change touches one native config and one backlog task in the same review. No generator writes configs, and no Python test tree compares a catalogue with the configs.

## Severity ladder

| Confidence | Recommended | Strict | Pedantic |
| --- | --- | --- | --- |
| Critical | error | error | error |
| Deterministic | warning | error | error |
| Heuristic | off | info | warning |

Native equivalents: Alint `warning`/`error`, Vale `suggestion`/`warning`/`error`, ast-grep `info`/`warning`/`error`, and Semgrep `INFO`/`WARNING`/`ERROR`. Alint has no native info level, so canonical advisory maps to `warning`. See [`docs/reference/rule-matrix.md`](../reference/rule-matrix.md).

## Why backlog tasks

The backlog is the scaffold for the next dev loop. A task is reviewable, has acceptance criteria, and records verification evidence. It keeps the repository fresh without a second machine-readable contract. Start with `PCC-16` after the remote is updated; `PCC-17` and `PCC-18` follow.
