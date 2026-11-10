# Preset matrix

The 30 canonical rules are grouped by first preset in `backlog/tasks/`. Recommended exposes 11 rules, Strict adds 10, and Pedantic adds 9. Higher presets inherit lower rules and never weaken severity.

| Confidence | Recommended | Strict | Pedantic |
| --- | --- | --- | --- |
| Critical | error | error | error |
| Deterministic | warning | error | error |
| Heuristic | off | info | warning |

| Tool | info | warning | error |
| --- | --- | --- | --- |
| alint | warning | warning | error |
| vale | suggestion | warning | error |
| ast-grep | info | warning | error |
| semgrep | INFO | WARNING | ERROR |

`off` means the rule is absent from that preset. `info` is advisory. The native mapping is recorded in the backlog tasks and implemented directly in the configs under `presets/`. See [`docs/concepts/rule-register.md`](../concepts/rule-register.md).
