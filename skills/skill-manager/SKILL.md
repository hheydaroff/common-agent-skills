---
name: skill-manager
description: "Manage the common-agent-skills repository. Use when adding, editing, removing, or deploying skills across Pi, Claude Code, and Codex."
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
   description: What this skill does and when to use it. Be specific about triggers.
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

## Skill Structure

```
skill-name/
├── SKILL.md              # Main instructions (required, keep under 150 lines)
├── references/           # Detailed docs (if SKILL.md would exceed 150 lines)
│   ├── guide.md
│   └── examples.md
└── scripts/              # Utility scripts (deterministic operations only)
    └── helper.sh
```

### When to Split Files
- SKILL.md exceeds ~150 lines → move detail into `references/`
- Content has distinct domains (e.g. fundamentals vs advanced)
- Scripts save tokens vs generating the same code repeatedly

### Artifact Output Convention

If a skill generates a document/artifact (PRD, spec, plan, glossary, report, diagram, dashboard, etc.), write it into the repo's `docs/` folder with the type in the filename: `docs/TYPE_descriptor.md` (e.g. `docs/PRD_checkout-2026-07.md`, `docs/SPEC_auth.md`, `docs/planning_*.md`, `docs/report_integration-*.md`). Create `docs/` if missing; fall back to `~/` only when there is no repo. Skills that **read** another skill's artifact must look in `docs/` first, then fall back to the repo root so older projects keep working. Exception: repo-root convention files read by many tools (`CONTEXT.md`, `AGENTS.md`, `README.md`) stay at root.

### Reference Routing (required if you have references/)

The model cannot search or guess reference filenames. SKILL.md **must** contain an explicit routing table:

```markdown
## Reference Files

| File | When to load |
|------|--------------|
| [deep-dive.md](references/deep-dive.md) | User asks to analyze a stock |
| [options.md](references/options.md) | User asks about options strategy |
| [macro.md](references/macro.md) | User asks about sector/macro outlook |
```

Without this, the model either loads everything (wasteful) or guesses from filenames (unreliable).

## Description Requirements

The description is **the only thing agents see** when deciding which skill to load. It’s surfaced in the system prompt alongside all other installed skills.

**Format:**
- Max 1024 characters
- First sentence: what it does
- Second sentence: "Use when [specific triggers/keywords]"
- Include trigger phrases the user might say

**Good:**
```
Find deepening opportunities in a codebase — refactors that turn shallow modules
into deep ones for better testability. Use when user wants to improve architecture,
find refactoring opportunities, or make a codebase more testable.
```

**Bad:**
```
Helps improve code.
```

## Frontmatter Validation & Common Errors

The frontmatter between the `---` fences is **YAML**. The single most common
skill-loading failure is an **unquoted `description` that contains a colon**:

```yaml
# BROKEN — YAML reads "Triggers:" as a nested mapping and errors with
# "Nested mappings are not allowed in compact mappings"
description: Does a thing. Triggers: 'foo', 'bar'.

# FIXED — wrap the whole value in double quotes
description: "Does a thing. Triggers: 'foo', 'bar'."
```

**Always double-quote a description** if it contains any of: `:` `#` `'` `"`
`[` `]` `{` `}` `,` `&` `*` `|` `>` `@`, or starts with a special char.
Single quotes (apostrophes like `what's`) are safe **inside** double quotes.

### Skill-name conflicts

Pi scans multiple skill directories (`~/.agents/skills/`, `~/.pi/agent/skills/`,
project `.agents/skills/`, configured vault skills). The **same `name` in two
scanned dirs = a conflict** and pi reports it. When a skill is moved into this
repo from a local dir, delete the old copy (e.g. a stray
`~/.pi/agent/skills/<name>/`). The repo deploys only to `~/.agents`, `~/.claude`,
`~/.codex` — never to `~/.pi/agent/skills/`.

### Validate before deploy

`deploy.sh` runs `validate-skills.sh` automatically and **fails fast** on bad
frontmatter or duplicate names. To check manually:

```bash
bash ~/development/common-agent-skills/validate-skills.sh
```

It parses every `SKILL.md` with the exact `yaml` parser pi uses, and verifies
`name` matches the directory, `description` exists and is ≤1024 chars, and no
name is declared twice.

## Quality Checklist (before committing)

- [ ] Description includes trigger phrases ("Use when...")
- [ ] SKILL.md under 150 lines (split if larger)
- [ ] No time-sensitive info that will go stale
- [ ] Consistent terminology throughout
- [ ] Concrete examples or workflows included
- [ ] References at most one level deep (no reference chains)
- [ ] Scripts are deterministic (validation, formatting — not AI-generated each time)
- [ ] Tested: does the skill actually trigger when expected?

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
