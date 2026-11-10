# polyglot-clean-code

Opinionated, reusable Clean Code presets for polyglot repositories. The distribution ships curated native configuration for **Alint**, **Vale**, **ast-grep**, and **Semgrep**. It introduces no new linter, no preset generator, and no custom CLI.

Version 0.1.0 is maintained under the MIT license.

## Quick start

Choose one preset per tool and point its native CLI at that config.

```sh
alint check . -c presets/alint/strict.yml
vale --no-global --config=presets/vale/strict.ini docs/
ast-grep --config presets/ast-grep/strict/sgconfig.yml scan .
semgrep scan --config presets/semgrep/strict.yml .
```

To add the presets to another repository, follow [`docs/guides/adopting-presets.md`](docs/guides/adopting-presets.md). Consumers pin a release tag after `PCC-12` or a full commit SHA today.

## What ships

| Preset | Policy |
| --- | --- |
| Recommended | Locked repository shape, canonical prose, debug-output boundaries, unsafe Rust blocks, and high-confidence security patterns |
| Strict | Adds least-privilege CI, error handling, dependency timeouts, configuration boundaries, and advisory prose |
| Pedantic | Adds paired-test policy, Conventional Commit values, empty catch blocks, bare Python handlers, immutable references, and heading checks |

All four engines expose all three presets. The 30 canonical `PCC-*` rules are recorded in three To Do backlog tasks, one per preset. See [`docs/concepts/rule-register.md`](docs/concepts/rule-register.md).

| Confidence | Recommended | Strict | Pedantic |
| --- | --- | --- | --- |
| Critical | error | error | error |
| Deterministic | warning | error | error |
| Heuristic | off | info | warning |

Numeric complexity metrics stay in `rude-clean-code`; see [`docs/concepts/engine-limits.md`](docs/concepts/engine-limits.md).

## Documentation

The maintained documents live under `docs/`. Start with [`docs/README.md`](docs/README.md).

| Area | Documents |
| --- | --- |
| Concepts | [`rule-register.md`](docs/concepts/rule-register.md), [`rule-contract.md`](docs/concepts/rule-contract.md), [`engine-limits.md`](docs/concepts/engine-limits.md) |
| Architecture | [`overview.md`](docs/architecture/overview.md), [`scan-findings.md`](docs/architecture/scan-findings.md) |
| Guides | [`development-setup.md`](docs/guides/development-setup.md), [`adopting-presets.md`](docs/guides/adopting-presets.md), [`running-the-checks.md`](docs/guides/running-the-checks.md), [`offline-sandbox.md`](docs/guides/offline-sandbox.md) |
| Reference | [`rule-matrix.md`](docs/reference/rule-matrix.md), [`repository-layout.md`](docs/reference/repository-layout.md), [`pixi-tasks.md`](docs/reference/pixi-tasks.md) |
| Development | [`documentation.md`](docs/development/documentation.md) |

## Validation

Maintained Markdown is checked by **Vale** for prose, **markdownlint-cli2** for Markdown structure, and **Alint** for repository and documentation structure (`PCC-R02` and `PCC-R04`). `doit docs` runs the prose and Markdown checks; `doit policy` and `doit ci` add Alint, the native engine tests, workflow checks, and a Rude pass with the Clean Code plugin over every tracked Python file. The plugin lints this repository's own Python; the distribution still ships no linter. See [`docs/development/documentation.md`](docs/development/documentation.md) and [`docs/guides/running-the-checks.md`](docs/guides/running-the-checks.md).

`README.md` is hand-maintained. Edit it directly; no template, generator, or `check-readme` task exists.

## Repository harness

Pixi locks the environment, Bun locks developer CLIs, doit owns every task, Convco checks commits, and Backlog.md records work. Bootstrap and verify:

```sh
pixi install
pixi run --locked bun install --frozen-lockfile
pixi run --locked doit ci
```

## Offline sandbox

`pixi-sandbox.toml` reviews the publish plan and the three generated files act on it: `.github/workflows/publish-sandbox.yml` packs the locked environment, verifies the transport, and pushes the `sandbox/developer-linux-64` orphan branch; `.github/workflows/relock.yml` refreshes `pixi.lock` for a manifest edit made without network access; and `scripts/restore.sh` restores the branch on an airlocked host. The bundle covers `linux-64` and the `default` environment.

```sh
gh workflow run publish-sandbox.yml --ref main
bash scripts/restore.sh
pixi install --frozen --offline
```

The publisher carries `contents: read` at the workflow level and `contents: write` only on the publishing job. A hand edit to a generated file is drift, not a fix: run `pixi-sandbox init` and commit its output. See [`docs/guides/offline-sandbox.md`](docs/guides/offline-sandbox.md).

## Dev loop

Start with `PCC-16` after the remote is updated. Work one rule at a time, update the matching backlog task, and run `doit ci`. `PCC-17` and `PCC-18` follow. See [`backlog/tasks/`](backlog/tasks/).

## Scope

This repository distributes configuration and rules. It does not install linting engines, replace an existing linter, or provide a wrapper CLI. See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the rule-proposal workflow.
