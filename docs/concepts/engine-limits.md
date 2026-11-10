# Engine limits versus Rude Clean Code

`rude-clean-code` is a Python AST plugin. It parses a project, walks scopes, counts constructs, and emits a diagnostic with a measured value, a limit, and a suggested action. Alint, Vale, ast-grep, and Semgrep are native configuration engines. This repository uses them for what they can express honestly and defers numeric complexity analysis to the dedicated plugin.

## What Rude Clean Code measures

The delivered plugin has nine deterministic rules. Each has a `check()` function, a rationale docstring, `severity=WARNING`, and no default autofix.

| Rule | Measured value | Limit |
| --- | --- | --- |
| `CC101` | Function lines | 30 |
| `CC102` | Function parameters | 5 |
| `CC103` | Return statements | 5 |
| `CC104` | Local variables | 10 |
| `CC201` | Class lines | 200 |
| `CC202` | Class methods | 15 |
| `CC301` | Nesting depth | 4 |
| `CC302` | Boolean operands | 3 |
| `CC303` | Branch count | 10 |

Doc-2 extends this into a detection contract for `CC001`–`CC910`: deterministic structural findings are warnings, heuristic findings are advisory, nothing is an error by default, counts do not descend into nested scopes, autofix appears only for provably safe rewrites, and project-scope analysis is deferred rather than guessed. `qgis-sdk` records legacy diagnostics in `clean_code_budget.json` so a baseline can shrink over time.

## What each engine can and cannot do

| Engine | Native scope | Why numeric CC rules do not fit |
| --- | --- | --- |
| Alint | File existence, structured JSON/YAML/TOML assertions, repository shape | No source parser, no symbol table, no control-flow graph, and no cross-file aggregation |
| Vale | Prose, terminology, links, spacing, headings | It reads text, not code; it cannot see a function, class, or branch at all |
| ast-grep | Tree-sitter structural patterns with `valid`/`invalid` cases | It matches syntax shapes but does not count lines, locals, returns, methods, nesting depth, or branches across scopes |
| Semgrep | Patterns, regexes, metadata, and some dataflow/taint analysis | It can find a construct or a flow, but it does not expose a project-wide complexity metric or a class/method inventory |

## Ignored paths

Alint's tree walk honours `.gitignore`, and no rule-level switch reads the tracked set reliably: in alint 0.22.0, `git_tracked_only: true` raised an analysis failure outside a Git repository and did not fire on force-added paths. `pcc-r06-no-tracked-artifacts` therefore reports `.env`, `.DS_Store`, `dist/`, `build/`, and `.venv/` only when a consumer leaves those paths unignored. `alint check --no-gitignore` shows the findings that the ignore file hides.

A pattern such as "an empty `except` block" is a structural match. A diagnostic such as "`CC101`: this function is 47 lines, the limit is 30, split it" needs a parser that can define a function boundary, count physical or logical lines, and report a number. None of the four native configs provides that measurement layer.

## What this repository does instead

| Rude Clean Code concept | Translation here |
| --- | --- |
| Measured value and limit | A concrete action and the offending construct in the `[PCC-...]` message |
| Deterministic WARNING | `critical` or `deterministic` confidence with the shared severity ladder |
| Heuristic INFO | `heuristic` confidence, absent in Recommended, advisory in Strict, warning in Pedantic |
| Paired positive/negative examples | Examples in the backlog rule register, ast-grep `valid`/`invalid` cases, Semgrep `ok:`/`ruleid:` targets |
| No default autofix | Presets report findings; they do not rewrite consumer code |
| Deferred project scope | No fabricated line, return, local, method, or inheritance counts |
| Baseline budget | `docs/guides/adopting-presets.md` documents a local baseline pattern; the distribution does not ship a budget file |

The rule families reflect evidence that these engines can check: locked Pixi manifests and docs in Alint, canonical prose in Vale, debug output and unsafe Rust in ast-grep, and swallowed exceptions or immutable references in Semgrep. The numeric thresholds stay in `rude-clean-code`. A rule that cannot be expressed honestly is deferred rather than faked; see [`docs/concepts/rule-contract.md`](rule-contract.md) and [`docs/architecture/overview.md`](../architecture/overview.md).

This repository now dogfoods that split. `rude` and `rude-clean-code` are pinned in `pixi.toml` under `[pypi-dependencies]`, `pyproject.toml` sets the Rude `E501` width to 88, and `doit lint-python` runs the plugin over `automation/`, where the only hand-written Python lives. The presets still ship no numeric threshold: a consumer that wants `CC101`-`CC303` installs the plugin itself, exactly as this repository does for its own automation code.

## Open work

`backlog/tasks/pcc-10` records Go and Java structural rules with measured false-positive counts before Pedantic. It does not propose adding an AST metric plugin here. If a future project needs `CC101`–`CC303`, install `rude-clean-code` or an equivalent AST plugin alongside these presets; do not ask Alint, Vale, ast-grep, or Semgrep to imitate it.
