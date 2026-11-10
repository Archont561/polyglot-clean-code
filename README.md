# Offline sandbox (orphan branch)

Built 2026-11-10T20:39:10Z from commit `99d92bf` for platform `linux-64`.
`pixi.lock` sha256 `cda0a4189960e17bc5eb625e8e4306cd3eeae3caa5510686ca30bc2990eebe8c`.

The verified self-bootstrap binary is stored at `.pixi-sandbox/tools/linux-64/pixi-sandbox`. The branch root intentionally contains documentation only.

| env | platform | packed | unpacked | files |
| --- | --- | ---: | ---: | ---: |
| `default` | linux-64 | 477.2 MiB | 1530.6 MiB | 165 |


## Restore on the disconnected machine

```bash
./.pixi-sandbox/tools/linux-64/pixi-sandbox doctor --branch-location . --verify
./.pixi-sandbox/tools/linux-64/pixi-sandbox restore --branch-location . --output-path <project> --force
# then, from <project> with no network, use pixi as the sole entrypoint:
pixi install --frozen --offline
pixi run --frozen -- cargo build --offline
```

Every manifest blob is verified before it is written into the working tree.
