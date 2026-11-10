# Running the checks

All automation lives in `automation/dodo.py`. Run tasks through the locked Pixi environment.

| Task | Purpose |
| --- | --- |
| `doit docs` | Run Vale prose and markdownlint-cli2 checks |
| `doit policy` | Run Alint, prose, Markdown, native engine tests, workflow lint, and Backlog.md |
| `doit ci` | Run the full local CI chain |
| `doit alint` | Check this repository with its root Alint config |
| `doit lint-prose` | Run Vale over maintained documents |
| `doit lint-python` | Run Rude with the Clean Code plugin over every tracked Python file |
| `doit docs-lint` | Run markdownlint-cli2 |
| `doit ast-grep-test` | Run native ast-grep rule tests for every preset |
| `doit examples` | Compile the Go and Java corpus and assert the Pedantic findings |
| `doit semgrep-validate` | Validate every Semgrep preset |
| `doit actionlint` | Lint GitHub Actions workflows |
| `doit backlog` | List Backlog.md tasks |
| `doit lint-commit` | Validate one Convco message from stdin |
| `doit check-commit-messages` | Validate an incoming commit range |
| `doit build-release` | Validate a release tag, render the Convco changelog, and pack the presets |
| `doit presets-archive` | Pack every preset tree into a reproducible archive |
| `doit install-hooks` | Install or verify Lefthook hooks |
| `doit pre-commit` | Run the pre-commit chain |
| `doit test` | Alias for `doit policy` |

Examples:

```sh
pixi run --locked doit ci
pixi run --locked doit docs
pixi run --locked doit policy
echo "fix(rules): reduce a false positive" | pixi run --locked doit lint-commit
```

## Go and Java examples

The Pedantic example corpus has clean and deliberately flawed Go and Java files.
`doit examples` compiles both languages and compares every scan result with an
`// expect: <rule-id>` marker on the diagnostic start line. Unmarked lines must
not produce findings. The fixtures exercise the direct print variants and empty
Java catches; they do not establish real-world false-positive rates. Java
`System.out.printf` is intentionally outside the current print rule.

## Releasing

1. Set `version` in `pixi.toml` and move the pending `CHANGELOG.md` entries under that version.
2. Merge the change on `main`, then tag the merge commit: `git tag v0.1.0 && git push origin v0.1.0`.
3. The release workflow validates the tag against `pixi.toml`, runs `doit ci`, and then publishes a GitHub Release that carries `polyglot-clean-code-presets-<tool>-<version>.tar.gz` for Alint, Vale, ast-grep, and Semgrep, a `SHA256SUMS-<version>.txt` file, and the rendered Convco changelog as the release body.

`doit build-release` checks the tag against the workspace version and renders the changelog to `dist/release-notes.md`; `doit presets-archive` writes the archives into `dist/`, which is gitignored and reproducible byte for byte. Both tasks are safe to run locally before the tag exists.

There is no `validate-catalogue`, `render-readme`, `check-readme`, `coverage`, or Python test task. The rule register is reviewed through `backlog/tasks/`.
