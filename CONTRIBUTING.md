# Contributing

## Setup

```sh
pixi install
pixi run --locked bun install --frozen-lockfile
pixi run --locked doit install-hooks
```

## Change workflow

1. Select a Backlog.md task with `pixi run --locked doit backlog`.
2. Read the rule register in `docs/concepts/rule-register.md`.
3. Add evidence from an Archont561 repository to the matching backlog task.
4. Edit the native config under `presets/` and add paired examples to the task.
5. Edit `README.md` directly when a README change is needed.
6. Verify with `pixi run --locked doit ci`.
7. Close the task with its final summary and verification notes.

## Offline sandbox

`pixi-sandbox.toml` reviews the plan that publishes `sandbox/developer-linux-64`. Change the plan there, then regenerate the owned files and commit them together:

```sh
pixi-sandbox init
pixi-sandbox init --check
```

`publish-sandbox.yml`, `relock.yml`, and `restore.sh` belong to the generator. A direct edit is drift, and the next `init` overwrites it. See [`docs/guides/offline-sandbox.md`](docs/guides/offline-sandbox.md).

## Commit messages

Convco accepts `feat`, `fix`, `perf`, `docs`, and `revert` as visible types. Internal types are hidden from the changelog. Use one of the scopes in `.versionrc`: `rules`, `presets`, `config`, `ci`, `deps`, `docs`, `lock`, `tests`, `release`, or `automation`. `lock` belongs to the generated relock bot.

```text
feat(rules): add an immutable-reference rule
test(presets): cover the strict severity ladder
```

## Rule proposals

A proposal needs a canonical ID, source evidence, a message with one concrete action, a confidence class, a first preset, and paired examples. A false-positive reduction needs a positive example that used to fail. Native configs are edited directly and reviewed with the backlog task. See [`docs/concepts/rule-register.md`](docs/concepts/rule-register.md) and [`docs/concepts/engine-limits.md`](docs/concepts/engine-limits.md).
