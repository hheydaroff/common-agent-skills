# AGENTS.md

Source of truth for agent skills (Pi, Claude Code, Codex). Edit here, never in `~/.agents/skills` etc.

- Layout: `skills/<name>/SKILL.md` (+ `scripts/`, `references/`). Only directories belong in `skills/`; `validate-skills.sh` fails on loose files.
- Loop: edit → `bash validate-skills.sh` → `bash deploy.sh` → commit. CI (`.github/workflows`) runs the same validation.
- Commit only when asked. Never push without approval.
- Adding an import from an external repo: extend the closest existing skill first (reference file or section); a new skill only if the use case differs. State non-goals up front.
- Some skills live only in `~/.pi/agent/skills/` (e.g. `merge-external-skills`, `jira-via-docker-gateway`); they are not in this repo. Importing/harvesting from an external repo: load `merge-external-skills` first (it settles scope before any cloning). Do not look for it under `skills/`.
- `validate-skills.sh` checks frontmatter/names only; it does not run skill scripts. After editing anything under `scripts/` or a `.mjs`/`.sh`, smoke-run it once before committing.
- Run Python via `uv run python`; `curl` to outbound hosts is blocked in pi, use codemode MCP tools (`mcp__docker_gateway__web_fetch_exa`). In pi, MCP means the built-in `mcp__<server>__<tool>` tools via codemode; the old `mcp({tool})` gateway and `pi-mcp-adapter` are gone.
- More: `skills/skill-manager/SKILL.md`.
