---
id: PCC-10
title: Add Go and Java structural rules
status: In Progress
assignee: []
created_date: '2026-11-10 14:30'
updated_date: '2026-11-11 00:55'
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
Open. Record verification evidence when the work is complete.
<!-- SECTION:FINAL_SUMMARY:END -->
