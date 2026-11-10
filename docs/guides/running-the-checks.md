# Running the checks

All automation lives in `automation/dodo.py`. Run tasks through the locked Pixi environment.

| Task | Purpose |
| --- | --- |
| `doit docs` | Run Vale prose and markdownlint-cli2 checks |
| `doit policy` | Run Alint, prose, Markdown, native engine tests, workflow lint, and Backlog.md |
| `doit ci` | Run the full local CI chain |
| `doit alint` | Check this repository with its root Alint config |
| `doit lint-prose` | Run Vale over maintained documents |
| `doit docs-lint` | Run markdownlint-cli2 |
| `doit ast-grep-test` | Run native ast-grep rule tests for every preset |
| `doit semgrep-validate` | Validate every Semgrep preset |
| `doit actionlint` | Lint GitHub Actions workflows |
| `doit backlog` | List Backlog.md tasks |
| `doit lint-commit` | Validate one Convco message from stdin |
| `doit check-commit-messages` | Validate an incoming commit range |
| `doit build-release` | Validate a release tag and Convco changelog output |
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

There is no `validate-catalogue`, `render-readme`, `check-readme`, `coverage`, or Python test task. The rule register is reviewed through `backlog/tasks/`.
