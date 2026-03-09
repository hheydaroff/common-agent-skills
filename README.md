# common-agent-skills

A unified home for agent skills that works across AI coding tools — Pi, Claude Code, Codex, and any tool following the [Agent Skills standard](https://agentskills.io).

## The Problem

When you use multiple AI agents, each tool has its own skills directory. The same skill ends up as 3 copies, edits drift, and backup means backing up N places.

## The Solution

One repo. One place to edit. One deploy command.

```
~/development/common-agent-skills/skills/   ← edit here
        ↓ deploy.sh
~/.agents/skills/       Pi (native support)
~/.claude/skills/       Claude Code
~/.codex/skills/        Codex
```

## Install

```bash
git clone git@github.com:hheydaroff/common-agent-skills ~/development/common-agent-skills
bash ~/development/common-agent-skills/setup.sh
```

That's it. Your skills are live across all tools.

## Workflow

```bash
# 1. Add or edit a skill
vim ~/development/common-agent-skills/skills/<skill-name>/SKILL.md

# 2. Deploy to all tools
bash ~/development/common-agent-skills/deploy.sh

# 3. Commit
git add -A && git commit -m "add: skill-name" && git push
```

## Included Skills

| Skill | Description |
|---|---|
| `skill-manager` | Teaches any agent how to add, edit, deploy, and manage skills in this repo |

## Adding Your Own Skills

Skills follow the [Agent Skills standard](https://agentskills.io/specification) — a `SKILL.md` with `name` and `description` frontmatter:

```
skills/
  my-skill/
    SKILL.md        ← required
    scripts/        ← optional helper scripts
    references/     ← optional docs loaded on-demand
```

## Tool Support

| Tool | How skills are loaded |
|---|---|
| [Pi](https://github.com/badlogic/pi-mono) | Reads `~/.agents/skills/` natively |
| [Claude Code](https://claude.ai/code) | Deployed to `~/.claude/skills/` |
| [Codex](https://github.com/openai/codex) | Deployed to `~/.codex/skills/` (additive, `.system/` preserved) |

## Requirements

- bash
- rsync
- One or more of: Pi, Claude Code, Codex
