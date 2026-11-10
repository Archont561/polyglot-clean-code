# Pixi tasks

`pixi.toml` delegates the task surface to doit.

| Pixi task | Command |
| --- | --- |
| `do` | `doit` |
| `bun-install` | `bun install --frozen-lockfile` |
| `backlog` | `bun x --bun --no-install backlog task list --plain` |

There is no README render task and no catalogue validation task. `README.md` is hand-maintained, and the rule register lives in `backlog/tasks/`. The `bun-install` task runs inside the Pixi environment; call it with `pixi run bun-install`. Use `pixi run --locked` in hooks and CI.
