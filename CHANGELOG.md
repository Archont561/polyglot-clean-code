# Changelog

All notable changes to polyglot-clean-code are documented here.

## Unreleased

- Added an offline sandbox lane: a reviewed `pixi-sandbox.toml` plan plus the generated publisher, relock workflow, and `restore.sh` launcher that publish `sandbox/developer-linux-64`.
- Scoped the single-line workflow rule to the hand-maintained workflows so generated Pixi Sandbox files stay byte-identical to the generator's output.
- Documented sandbox publishing, restore, and regeneration in `docs/guides/offline-sandbox.md`.

## 0.1.0

- Added 30 curated canonical rules across Alint, Vale, ast-grep, and Semgrep.
- Added Recommended, Strict, and Pedantic presets for each tool under `presets/`.
- Added positive and negative examples, native ast-grep tests, and annotated Semgrep fixtures.
- Added Pixi, Bun, Convco, Backlog.md, doit, Lefthook, Vale, Alint, and markdownlint-cli2.
- Removed the catalogue, the README generator, skills, and the Python test tree.
- Moved the 30 rule records into three To Do backlog tasks, one per preset.
- Kept `automation/dodo.py` as the only automation file.
- Replaced the generated README with a hand-maintained brief README.
- Documented the backlog rule register, engine limits, consumer adoption, and tag pinning.
