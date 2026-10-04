---
name: retro
description: "Session retrospective for pi. /retro reads the last N coding-agent sessions for the CURRENT folder (or a scope you name) and shows (in chat, never saved to the repo) a report of evidence-backed improvements to repo navigability, process (PRD/SPEC/tests/CI/automation), skills, memory/rules, cost and your own habits. Report only; applies changes when asked. Use for '/retro', 'retrospective', 'review my last sessions', 'where does the agent waste time in this repo', 'what should I improve in my workflow'."
---

# /retro

Mine past pi sessions, find friction, propose fixes. **Report only. Never edit anything until the user asks; the report is shown in chat, not saved.**

Sessions: `~/.pi/agent/sessions/<cwd-with-dashes>/*.jsonl` (can be 65 MB: never read raw, always go through the script).
Run scripts with `uv run python` (bare python is intercepted):

```bash
R=~/.agents/skills/retro/scripts/retro.py
uv run python $R digest  [scope flags]        # repo health + per-session signals + aggregate + delta vs previous retro
uv run python $R excerpt <session-id> [--kinds user,corrections,errors,blocks,nav,final] [--max 15]
uv run python $R outcome [scope flags] [--window 3d]   # git follow-ups per session
```

## Scope: default = current folder only

No arguments → `--cwd $PWD --last 10` (subfolders included, other projects and worktrees excluded, the running session skipped). Translate the user's wording:

| User says | Flags |
|---|---|
| `/retro` | *(defaults)* |
| "last 25", "more" | `--last 25` |
| "this week", "since Monday", "2 weeks" | `--since 7d` / `14d` / `YYYY-MM-DD` |
| "include worktrees / branches" | `--worktrees` (herdr worktrees of this repo) |
| "only this folder, not subfolders" | `--no-subdirs` |
| "that session", an id | `--session <id>` |
| "across everything / all projects" | `--all-projects` (only when explicitly asked) |
| "focus on X" (navigation, cost, process…) | same digest; spend the analysis on that lens |

If the folder has no sessions, say so and offer the nearest alternatives (`--worktrees`, parent folder, `--all-projects`); do not widen silently.

## Procedure

1. **Digest.** Run `digest` with the scope. Read the output (it is small). `previous_retro` is only set if the user keeps saved reports; normally it is null, so skip trends.
2. **Shortlist 3–6 sessions** that look worst: highest `nav_before_first_edit`, `corrections`, `tool_errors`, `security_blocks`, `edit_churn`, `code_edited_no_verify`, `repeated_prompts`, `compactions`, top cost.
3. **Verify with `excerpt`** before claiming anything. A pre-pass flag is a lead, not a finding (regex corrections are noisy: "don't"/"again" appear in normal requests). Drop false positives.
4. **Outcome** (only if the user wants it or sessions are older than the window): run `outcome`; reverts, `fix:` commits and follow-up sessions on the same files mean the session's result did not hold.
5. **Classify** each surviving finding into one home and write the proposal (see [playbook](references/playbook.md): signal → cause → fix table, and the seven homes).
6. **Show the report** in chat using [report-template.md](references/report-template.md). Do NOT write it to the repo or any file (user does not store AI improvement notes in project repos). Only save if the user explicitly asks; then use `<cwd>/docs/report_retro-YYYY-MM-DD.md` with the `<!-- retro-metrics -->` line so later runs get trends.
7. **End** by asking which proposals to apply.

## Rules

- ≤10 proposals, each: **finding → evidence (session id + quote or numbers) → fix → where it lands**. No evidence, no proposal.
- Never quote secrets. The script redacts; still skim what you paste. Do not paste raw logs.
- Prefer deleting/consolidating over adding: a proposal that adds a rule must say what it replaces or why nothing can.
- Small samples (<5 sessions) → say the numbers are anecdotal.
- If a previous saved report exists, mark its proposals as ✅ worked / ➖ no change / ❌ got worse / ⏳ not applied, using the `previous_retro.compare` deltas.
- Growth section is about the user's habits (prompting, spec-first, verification, model/cost choices), stated as observations with evidence, not advice-by-numbers.

## When the user says "apply / improve / do #2"

Only then edit. Per home:
- **Repo files** (AGENTS.md, README, docs, scripts, CI): edit in the repo; show the diff; do not commit unless asked.
- **Skills**: edit the source in `~/development/common-agent-skills/skills/<name>/` (never the deploy targets), run `bash validate-skills.sh` and `bash deploy.sh`.
- **Memory/rules**: `vault_memory` (atomic, one topic per file).
- **Automation** (cron, hooks, scripts): propose the exact artifact and confirm before creating; cron only on explicit request.
After applying, say which proposals are done.

## Reference Files

| File | When to load |
|------|--------------|
| [playbook.md](references/playbook.md) | Step 5: turning signals into proposals, the seven homes, growth lens, false-positive list |
| [report-template.md](references/report-template.md) | Step 6: showing the report |
