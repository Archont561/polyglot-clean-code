---
id: PCC-10
title: Add Go and Java structural rules
status: Done
assignee: []
created_date: '2026-11-10 14:30'
updated_date: '2026-11-11 01:20'
labels: []
dependencies: []
priority: medium
type: task
ordinal: 10000
milestone: ''
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add Go and Java structural rules as part of the reusable Clean Code preset distribution. Evidence, acceptance criteria, and verification stay in this record.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Inspect Archont561 evidence for Go and Java before proposing a rule.
- [x] #2 Add paired valid and invalid ast-grep cases for each new rule.
- [x] #3 Measure false-positive counts before enabling Pedantic.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
The first step is the evidence, and it changes the shape of the answer: no `Archont561` repository is written in Go or Java, so neither language has first-party code to measure against. Extend the two canonical IDs that already rest on shipped doctrine instead of inventing new concepts, land them in Pedantic only, and measure them on a synthetic corpus before claiming anything.
<!-- SECTION:PLAN:END -->

## Rule inventory

| ID | Tool | Title | Confidence | Native IDs |
| --- | --- | --- | --- | --- |
| `PCC-S01` | ast-grep | Structured logging instead of debug prints in library code | deterministic | pcc-s01-print-python, pcc-s01-console-log-ts, pcc-s01-println-rust, pcc-s01-print-go, pcc-s01-print-java |
| `PCC-S07` | ast-grep | No empty catch blocks | deterministic | pcc-s07-empty-catch-ts, pcc-s07-empty-catch-java |

Both canonical IDs keep their existing titles, confidence, and messages, and both already exist in the register through PCC-16, PCC-17, and PCC-18. This task adds native implementations rather than new canonical rules, which keeps the count at 30 and leaves every earlier register entry valid.

## Rule details

### `PCC-S01` — Structured logging instead of debug prints in library code

- Message: `[PCC-S01] Replace debug printing in library code with the project's logger.`
- Source: `Archont561 explicit-output convention; doc-2 CC9xx documentation/observability rules`
- Evidence limit: no first-party Go or Java code exists, so the Go and Java implementations extend the Python, TypeScript, and Rust rule rather than resting on measured evidence of their own.
- Positive: `slog.Info("starting", "port", port)` in Go; `LOG.info("starting {}", port)` in Java.
- Negative: `fmt.Println("starting")` in Go; `System.out.println("starting")`, `System.err.println(...)`, and `error.printStackTrace()` in Java.
- Implementations: `pcc-s01-print-python`, `pcc-s01-console-log-ts`, `pcc-s01-println-rust`, `pcc-s01-print-go`, `pcc-s01-print-java`
- Scoping: `cmd/**`, `main.go`, `src/test/**`, `vendor/**`, `testdata/**`, and `build/**` are ignored, because printing is the output of an entrypoint and test trees and vendored code are not maintained in place.

### `PCC-S07` — No empty catch blocks

- Message: `[PCC-S07] Handle, translate or rethrow a caught error; an empty catch hides the failure.`
- Source: `doc-2 CC309 broad exception swallowed; the fail-fast family`
- Positive: a Java catch block that logs or rethrows the failure.
- Negative: `catch (IOException error) {}` and `catch (IOException error) { }`.
- Implementations: `pcc-s07-empty-catch-ts`, `pcc-s07-empty-catch-java`

## Verification

<!-- SECTION:VERIFICATION:BEGIN -->
### Evidence

The GitHub API lists twenty-four public `Archont561` repositories; their primary languages are Python, TypeScript, Rust, and Astro. There is no Go repository and no Java repository, so AC #1 resolves to a negative: neither language has first-party code to sample. The rules therefore reuse the shipped `PCC-S01` and `PCC-S07` doctrine, stay in Pedantic, and make no prevalence claim.

### Native rule tests

`ast-grep test --skip-snapshot-tests` in `presets/ast-grep/pedantic` runs thirteen test files. The three new ones pair three valid and three invalid cases for Go, three valid and four invalid for Java printing, and two valid and two invalid for the empty catch. All thirteen files pass.

One trap is worth recording. The first Go rule used `pattern: fmt.Println($$$ARGS)`, and the test harness accepted it while a real `.go` file matched nothing: tree-sitter-go parses bare `pkg.Func(x)` as a type conversion, so the compiled pattern had the wrong shape. `ast-grep run -l go -p 'fmt.Println($$$A)' --debug-query=ast` shows `type_conversion_expression` instead of `call_expression`. The rule now matches `kind: call_expression` with a `has: field: function` regex, and the test cases wrap their snippets in a function so the harness exercises the same shape as production code.

### False-positive measurement

A synthetic corpus outside the repository held four files: a Go service using `log/slog` and a Java service using slf4j, each paired with a deliberately flawed counterpart.

| Tree | `pcc-s01-print-go` | `pcc-s01-print-java` | `pcc-s07-empty-catch-java` | Total |
| --- | --- | --- | --- | --- |
| Deliberately flawed | 2 | 3 | 1 | 6 |
| Idiomatic | 0 | 0 | 0 | 0 |

The flawed Go file produced one finding per `fmt.Println` and `fmt.Printf` call and none for `fmt.Fprintf`, which is the correct split. The flawed Java file produced `System.out.println`, `System.err.println`, `printStackTrace`, and the empty catch, and nothing for the handled catch. The idiomatic files produced no findings at all, so the measured false-positive count is zero on this corpus.

### Toolchains

`go` and `javac` are absent from this sandbox, and conda-forge is not reachable from it, so the compilers were not installed. They would not strengthen the result: ast-grep matches on tree-sitter syntax trees, an unparsable snippet fails the native test, and a compiler would prove that the sample program builds rather than that the rule generalizes. A compile step becomes useful when a real Go or Java consumer supplies a corpus that must remain buildable, which is not the case here.
<!-- SECTION:VERIFICATION:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Go and Java now have structural coverage, and the route there is more useful than the rules themselves.

The evidence step answered AC #1 negatively: across twenty-four public `Archont561` repositories the primary languages are Python, TypeScript, Rust, and Astro, with no Go or Java code anywhere. Rather than invent thresholds with nothing to measure them against, the task extended two canonical IDs that already rest on shipped doctrine. `PCC-S01` gained `pcc-s01-print-go` and `pcc-s01-print-java`, the latter covering `printStackTrace()` as well as `System.out` and `System.err`; `PCC-S07` gained `pcc-s07-empty-catch-java`. All three rules live in the Pedantic ast-grep project, keep the existing titles, messages, and `error` severity, and add no new canonical ID, so the register stays at 30 rules and every earlier entry remains accurate.

The most valuable finding was a rule-design trap. The first Go rule used `pattern: fmt.Println($$$ARGS)`; the native test harness passed it, but a real `.go` file matched nothing, because tree-sitter-go parses a bare `pkg.Func(x)` as a type conversion rather than a call. `--debug-query=ast` shows `type_conversion_expression`. The rule now matches `kind: call_expression` with a `has: field: function` regex, and the test snippets wrap their calls in a function so the harness exercises production-shaped code. A snippet-only test suite would have shipped a dead rule.

AC #3 is measured rather than asserted. A synthetic corpus outside the repository paired a Go service on `log/slog` and a Java service on slf4j with deliberately flawed twins:

| Tree | `pcc-s01-print-go` | `pcc-s01-print-java` | `pcc-s07-empty-catch-java` | Total |
| --- | --- | --- | --- | --- |
| Deliberately flawed | 2 | 3 | 1 | 6 |
| Idiomatic | 0 | 0 | 0 | 0 |

`ast-grep test` runs thirteen pedantic test files, all passing, and CI on PR #12 (run [42893675912](https://github.com/Archont561/polyglot-clean-code/actions/runs/42893675912)) re-ran them inside the locked Pixi environment, which is the real proof that the pinned ast-grep 0.51.1 accepts the `call_expression` rule. Root Alint passes 22 of 22, and the three Alint presets pass 16, 21, and 25.

No toolchain was installed. `go` and `javac` are absent from this sandbox and conda-forge is unreachable from it, so the compiler question was answered by reasoning rather than by `pixi add`: structural rules match tree-sitter syntax, an unparsable snippet already fails the native test, and a compiler would validate the sample program instead of the rule. That judgement is written into [`docs/architecture/scan-findings.md`](../../docs/architecture/scan-findings.md) together with the evidence gap, so a future Go or Java consumer knows the first real false-positive baseline is still owed.

`CHANGELOG.md` grew an `## Unreleased` section for the first time since the `v0.1.0` tag, which also corrected one post-release bullet that had been filed under the published version. With this task Done, every task in the backlog is complete.
<!-- SECTION:FINAL_SUMMARY:END -->
