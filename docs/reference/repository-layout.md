# Repository layout

```text
polyglot-clean-code/
├── presets/
│   ├── alint/                    # Recommended, Strict, and Pedantic configs
│   ├── vale/                     # Ini files and vendored style trees
│   ├── ast-grep/                 # Three self-contained ast-grep projects
│   │   └── pedantic/examples/    # Compiled Go and Java corpus for the new rules
│   └── semgrep/                  # Composed presets, per-rule files, and fixtures
├── automation/
│   └── dodo.py                   # Only automation file; single task registry
├── backlog/
│   ├── config.yml
│   └── tasks/                    # Rule register and open dev-loop work
├── docs/                         # Architecture, concepts, guides, and reference
├── .github/                      # CI, release, sandbox publisher, and issue templates
├── pixi.toml / pixi.lock         # Environment of record
├── pixi-sandbox.toml             # Reviewed publish plan for the offline sandbox
├── scripts/
│   └── restore.sh                # Generated airlock launcher
└── package.json / bun.lock       # Developer CLIs
```

There is no `presets/catalogue.yml`, no root `tests/`, no `automation/contracts.py`, no README template, and no Python test tree. The only shell file is the generated `scripts/restore.sh` launcher, which Pixi Sandbox owns; `publish-sandbox.yml`, `relock.yml`, and `scripts/restore.sh` are regenerated with `pixi-sandbox init --script-path scripts/restore.sh`, and `pixi-sandbox.toml` stays hand-reviewed. Root `.alint.yml` and `.vale.ini` dogfood the fresh repository policy. The backlog tasks are the reviewed rule register. The shipped Alint presets remain product configs for a full consumer harness rather than this scaffold: Recommended, Strict, and Pedantic all check `docs/concepts/rule-register.md`, and none of them carries a historical `docs/reference/rules.md` or `automation/fixtures/` path.
