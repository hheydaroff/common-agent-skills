# AGENTS.md

Source of truth for agent skills (Pi, Claude Code, Codex). Edit here, never in `~/.agents/skills` etc.

- Layout: `skills/<name>/SKILL.md` (+ `scripts/`, `references/`). Only directories belong in `skills/`; `validate-skills.sh` fails on loose files.
- Loop: edit → `bash validate-skills.sh` → `bash deploy.sh` → commit. CI (`.github/workflows`) runs the same validation.
- Commit only when asked. Never push without approval.
- Adding an import from an external repo: extend the closest existing skill first (reference file or section); a new skill only if the use case differs. State non-goals up front.
- Some skills live only in `~/.pi/agent/skills/` (e.g. `merge-external-skills`, `jira-via-docker-gateway`); they are not in this repo.
- Run Python via `uv run python`; `curl` to outbound hosts is blocked in pi, use codemode MCP tools (`mcp__docker_gateway__web_fetch_exa`).
- More: `skills/skill-manager/SKILL.md`.
