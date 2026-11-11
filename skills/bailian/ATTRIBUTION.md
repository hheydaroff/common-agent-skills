# Attribution

Content under `references/` and `scripts/` is vendored from the Alibaba Cloud Model Studio (Bailian)
skills published with `bailian-cli` (https://github.com/modelstudioai/cli, Apache-2.0, see `LICENSE`),
as installed by `bl skill init` (CLI/skills version 2.8.5).

Local modifications:
- Twelve separate `bailian-*` skills merged into one router skill; each skill's `SKILL.md` body became
  `references/<topic>.md` (frontmatter removed), companion files were flattened to `references/<topic>-<name>.md`.
- Auto-generated command references (`reference/*`) became `references/cmd-<topic>-<group>.md`.
- Relative links rewritten to the flat layout; `scripts/wait.sh` -> `scripts/train-deploy-wait.sh`;
  `model-recommend` script paths point at `<skill-dir>/scripts/model-recommend/`.
- `bailian-docs-llm-wiki` data (~32 MB) is not vendored; it stays in `~/.bailian/skills/bailian-docs-llm-wiki/`.
- README files and `evals/` were dropped.
