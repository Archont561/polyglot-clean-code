# Documentation

Start with the [root README](../README.md) for the quick start and the documentation index. The rule register, architecture notes, and guides are linked below.

## Concepts

- [Rule register](concepts/rule-register.md)
- [Rule contract](concepts/rule-contract.md)
- [Engine limits versus Rude Clean Code](concepts/engine-limits.md)
- [Architecture overview](architecture/overview.md)
- [Archont561 scan findings](architecture/scan-findings.md)

## Guides

- [Development setup](guides/development-setup.md)
- [Adopting presets](guides/adopting-presets.md)
- [Running the checks](guides/running-the-checks.md)
- [Offline sandbox](guides/offline-sandbox.md)

## Reference

- [Curated preset matrix](reference/rule-matrix.md)
- [Repository layout](reference/repository-layout.md)
- [Pixi tasks](reference/pixi-tasks.md)
- [Documentation standard](development/documentation.md)

## Validation

Vale checks prose in maintained Markdown, markdownlint-cli2 checks Markdown structure, and Alint checks repository and documentation structure through `PCC-R02` and `PCC-R04`. `doit docs`, `doit policy`, and `doit ci` run these checks. The documentation standard is in [`development/documentation.md`](development/documentation.md).
