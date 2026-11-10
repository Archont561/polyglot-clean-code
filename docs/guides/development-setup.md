# Development setup

## Requirements

Pixi 0.84.1 or newer is enough. It installs Bun 1.4.2, Python, Alint, Vale, ast-grep, Semgrep, Convco, Lefthook, doit, actionlint, and shellcheck. The Bun manifest then installs Backlog.md and markdownlint-cli2 from npm.

This setup maintains the distribution. A consumer repository installs the four engines itself and vendors only `presets/`; see [`adopting-presets.md`](adopting-presets.md).

## Bootstrap

```sh
pixi install
pixi run --locked bun install --frozen-lockfile
pixi run --locked doit install-hooks
```

`pixi.lock` is the environment of record. `bun.lock` pins developer CLIs. Do not delete a lockfile to repair a check; update it in the same change.

## First verification

```sh
pixi run --locked doit docs
pixi run --locked doit policy
pixi run --locked doit ci
```

If an external linter binary is missing, run commands through `pixi run --locked`.

## Editor support

Vale styles are vendored under `presets/vale/styles/<preset>/`; no network sync is needed. ast-grep projects are self-contained and can be opened from their preset directory. The rule register lives in `backlog/tasks/`.
