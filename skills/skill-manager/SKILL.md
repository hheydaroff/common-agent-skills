---
name: skill-manager
description: Manage the unified agent skills repository (common-agent-skills). Use when adding, editing, removing, or deploying skills across tools (Pi, Claude Code, Codex). Covers where the source of truth lives, how to create a skill, how to deploy, and the git workflow.
---

# Skill Manager

## Source of Truth

All skills live in one place:

```
~/development/common-agent-skills/skills/
```

This is a git repository. **Never edit skills directly in the deploy targets** — changes there will be overwritten on the next deploy.

Deploy targets (written to by deploy.sh, never edited directly):
- `~/.agents/skills/` — Pi reads this natively
- `~/.claude/skills/` — Claude Code
- `~/.codex/skills/` — Codex

## Adding a New Skill

1. Create a directory in the skills folder:
   ```bash
   mkdir ~/development/common-agent-skills/skills/<skill-name>
   ```

2. Create `SKILL.md` following the Agent Skills spec:
   ```markdown
   ---
   name: skill-name
   description: What this skill does and when to use it. Be specific.
   ---

   # Skill Name

   Instructions here...
   ```

3. Deploy and commit:
   ```bash
   bash ~/development/common-agent-skills/deploy.sh
   cd ~/development/common-agent-skills
   git add -A && git commit -m "add: skill-name" && git push
   ```

## Editing an Existing Skill

1. Edit the file:
   ```
   ~/development/common-agent-skills/skills/<skill-name>/SKILL.md
   ```

2. Deploy and commit:
   ```bash
   bash ~/development/common-agent-skills/deploy.sh
   cd ~/development/common-agent-skills
   git add -A && git commit -m "update: skill-name" && git push
   ```

## Removing a Skill

1. Delete the directory:
   ```bash
   rm -rf ~/development/common-agent-skills/skills/<skill-name>
   ```

2. Deploy and commit (deploy.sh uses --delete for Claude and agents dirs):
   ```bash
   bash ~/development/common-agent-skills/deploy.sh
   cd ~/development/common-agent-skills
   git add -A && git commit -m "remove: skill-name" && git push
   ```

## Commit Message Convention

```
add: skill-name        new skill
update: skill-name     changes to existing skill
remove: skill-name     deleted skill
fix: skill-name        bug fix in scripts or instructions
chore: description     deploy.sh, setup.sh, README changes
```

## What Lives Here vs Elsewhere

| Content | Location | Managed by |
|---|---|---|
| Universal skills | `~/development/common-agent-skills/skills/` | This repo |
| Pi extensions | `~/.pi/agent/extensions/` | Separately |
| Claude commands | `~/.claude/commands/` | Separately |
| Codex superpowers | `~/.codex/superpowers/` | Separately |
| Project skills | `.agents/skills/` in each project repo | Each project |

## On a New Machine

```bash
git clone git@github.com:hheydaroff/common-agent-skills ~/development/common-agent-skills
bash ~/development/common-agent-skills/setup.sh
```
