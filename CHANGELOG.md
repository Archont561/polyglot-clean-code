# Changelog

All notable changes to polyglot-clean-code are documented here.

## Unreleased

- Moved the generated airlock launcher to `scripts/restore.sh` and pointed the publisher's generator input at the new path.
- Added the Go and Java toolchains to the Pixi environment and a compiled example corpus under `presets/ast-grep/pedantic/examples`, wired into `doit examples` so the Pedantic findings are asserted on every CI run.

- Extended `PCC-S01` to Go and Java and `PCC-S07` to Java: `pcc-s01-print-go`, `pcc-s01-print-java`, and `pcc-s07-empty-catch-java` ship in the Pedantic ast-grep project with paired `valid`/`invalid` cases.
- Measured the new rules on a synthetic corpus: six expected findings on the deliberately flawed files, zero findings on the idiomatic `slog` and slf4j files.
- Added `rude` and `rude-clean-code` to the Pixi environment and wired `doit lint-python` into the policy chain, so every tracked Python file is checked against the Clean Code limits at a line width of 88, with the deliberately invalid Semgrep fixtures excluded by pathspec.

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
- Added an offline sandbox lane: a reviewed `pixi-sandbox.toml` plan plus the generated publisher, relock workflow, and `restore.sh` launcher that publish `sandbox/developer-linux-64`.
- Scoped the single-line workflow rule to the hand-maintained workflows so generated Pixi Sandbox files stay byte-identical to the generator's output.
- Refreshed the Alint Pedantic preset: dropped the retired `skills-lock.json` checks, renamed `pcc-r04-rule-reference` to `pcc-r04-rule-register`, excluded the generated Pixi Sandbox workflows from the single-line rule, and split `pcc-r07-rule-test-dirs` into per-family rules, for 25 rules.
- Refreshed the Alint Strict preset: dropped the retired `skills-lock.json` checks, renamed `pcc-r04-rule-reference` to `pcc-r04-rule-register`, and excluded the generated Pixi Sandbox workflows from the single-line rule, for 21 rules.
- Refreshed the Alint Recommended preset: dropped the retired `skills-lock.json` checks, renamed `pcc-r04-rule-reference` to `pcc-r04-rule-register`, and pointed it at `docs/concepts/rule-register.md`, for 16 rules.
- Excluded the generated `publish-sandbox.yml` and `relock.yml` from the Alint Recommended single-line rule so the preset passes on this repository and on consumers that adopt Pixi Sandbox.
- Documented sandbox publishing, restore, and regeneration in `docs/guides/offline-sandbox.md`.
- Fixed the generated publisher cache flag: the rendered workflow now carries `setup_pixi_cache = false` from `pixi-sandbox.toml`, so `setup-pixi` no longer rejects `run-install: false` with `cache: true`.
- Added `doit presets-archive`, which packs every preset tree into a byte-reproducible tarball beside a `SHA256SUMS-0.1.0.txt` file.
- Added a release publish job that attaches the preset archives, the checksum file, and the rendered Convco changelog to the GitHub Release for a `v*` tag.
- Published the first release as `v0.1.0`.
