# Rule contract

A rule is a contract, not a preference. The same contract applies to every tool and every preset. The contract is recorded in `backlog/tasks/`, not in a catalogue file.

## Canonical record

Each canonical rule stores:

- `id`: a stable `PCC-...` key;
- `tool`: Alint, Vale, ast-grep, or Semgrep;
- `title` and `message`: one actionable description;
- `source`: evidence from an Archont561 repository;
- `confidence`: `critical`, `deterministic`, or `heuristic`;
- `min_preset`: the first preset that exposes the rule;
- `examples`: positive and negative cases;
- `implementations`: one or more native rules with lowercase `pcc-` IDs.

The canonical ID appears in every message. Native IDs add a language or mechanism suffix. The canonical ID is the shared policy key; the native ID is what a CLI prints.

## Detection contract

Doc-2 from `rude-clean-code` defines the parent philosophy:

1. Diagnostics state a measured value, a limit, and a suggested action.
2. Counts do not descend into nested scopes.
3. Heuristic findings are advisory; deterministic findings can fail a gate.
4. Autofix is offered only where the rewrite is provably safe.
5. Project-scope analysis is deferred rather than faked.
6. Every rule has a positive and a negative example.

Alint, Vale, ast-grep, and Semgrep do not expose numeric function or class metrics. Pattern rules in this repository therefore state the concrete action and the offending construct. Numeric thresholds remain in the Rude plugin. The backlog rule register records both the evidence and the boundary. See [Rule register](rule-register.md) and [Engine limits versus Rude Clean Code](engine-limits.md).

## Severity ladder

| Confidence | Recommended | Strict | Pedantic |
| --- | --- | --- | --- |
| Critical | error | error | error |
| Deterministic | warning | error | error |
| Heuristic | off | info | warning |

Native equivalents: Alint `warning`/`error`, Vale `suggestion`/`warning`/`error`, ast-grep `info`/`warning`/`error`, and Semgrep `INFO`/`WARNING`/`ERROR`. Alint has no info level, so advisory maps to `warning`. See [`docs/reference/rule-matrix.md`](../reference/rule-matrix.md).

## Example contract

| Engine | Positive example | Negative example |
| --- | --- | --- |
| Alint | Recorded in the backlog task | Recorded in the backlog task |
| Vale | Recorded in the backlog task | Recorded in the backlog task |
| ast-grep | `valid` cases in `presets/ast-grep/<preset>/rule-tests/` | `invalid` cases in `presets/ast-grep/<preset>/rule-tests/` |
| Semgrep | `ok:` targets in `presets/semgrep/fixtures/<preset>/` | `ruleid:` targets in `presets/semgrep/fixtures/<preset>/` |

ast-grep uses its native `test` command. Semgrep fixtures are annotated targets reviewed with the backlog task. Alint and Vale examples live in the task record rather than a Python fixture tree.

## Customization

Change the native config under `presets/` and the matching backlog task together. Add evidence, examples, and native implementations. Run `pixi run --locked doit ci`. A rule without paired examples fails review.
