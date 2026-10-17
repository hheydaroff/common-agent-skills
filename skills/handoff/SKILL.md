---
name: handoff
description: "Compact the current conversation into a handoff document so a fresh agent can pick up the work: a new pi session, a herdr subagent, a lane worker, Claude Code or Codex. Use when the user says 'handoff', 'write a handoff', 'save the session state', 'continue this in a new session', 'context is almost full', 'pass this to another agent', 'I'm stopping here, pick it up tomorrow', or when a long task must survive a session break, a model switch or a machine switch. Records the source session file so the next agent can recover exact evidence, points at existing artifacts instead of duplicating them, names the skills to load next, routes durable facts to vault memory, and prints the resume commands. NOT for compressing context inside the current session (/compact), exporting the raw transcript (/export), mining past sessions for friction (retro), or briefing new parallel work (parallel-agent-lanes)."
---

# Handoff

One markdown file that lets a fresh agent continue this work without re-discovering it, plus the commands that resume.

Adapted from `skills/productivity/handoff` in [mattpocock/skills](https://github.com/mattpocock/skills) (MIT) — see `ATTRIBUTION.md`. Upstream's five rules are kept; the session / memory / skills mechanics are this environment's.

## Two ways to continue — pick one and say which

| Mode | When | Cost |
|---|---|---|
| **Resume the session** (`pi --session`, `/import`) | Same human, same machine, same tool; the history is trustworthy | Exact, no doc needed |
| **Fresh agent + this doc** | Different tool (Claude Code, Codex), different machine/container, different model, or the session is huge / already compacted | The doc is the only context |

Write the doc in both cases — it is the thing a human can read — but in resume mode keep it short and let the session carry the detail.

## Not this skill

| The user actually wants | Use |
|---|---|
| Free context in THIS session and keep going | `/compact [instructions]` |
| The raw transcript as HTML/JSONL, or a share link | `/export`, `/share` |
| "Where do I waste time" across past sessions | `retro` |
| A brief for NEW parallel work in a worktree | `parallel-agent-lanes` |
| A permanent record of a decision | `documentation-and-adrs` |

## Steps

### 1. Fix the purpose of the next session
`/skill:handoff <text>` (pi) or `/handoff <text>` (Claude Code) appends `<text>` as that purpose. If none was given and it is not obvious from the conversation, ask one question — "what will the next session be used for?" — and wait. The purpose filters everything downstream: a handoff for "finish the migration" carries different weight than one for "review this PR".

### 2. Get ground truth — never write this from memory of the chat
```bash
DIR="${TMPDIR:-/tmp}"; DIR="${DIR%/}"
SLUG=$(basename "$(git rev-parse --show-toplevel 2>/dev/null || pwd)")
OUT="$DIR/handoff-$SLUG-$(date +%Y%m%d-%H%M).md"; echo "$OUT"
git status --short; git log --oneline -10; git diff --stat
echo "session: ${PI_SESSION_FILE:-unknown} (${PI_SESSION_ID:-?})"
```
Record what was **observed**: uncommitted files, real commit shas, the actual failing output, the exact command that reproduces it. `$PI_SESSION_FILE` / `$PI_SESSION_ID` are set inside pi; if empty, ask the user to run `/session`.

If the session was already compacted, the in-context summary has lost detail. Recover it before writing with `session_query` on `$PI_SESSION_FILE` (or `session_search` for one exact error string), and mark reconstructed parts as such in the doc.

### 3. Write to `$OUT` — the OS temp dir, not the workspace
Upstream rule, kept: a handoff is ephemeral task state, and the workspace is a repo that gets committed, rsync'd and deployed. Print the absolute path in chat when done.

**Exception:** your temp dir is invisible to an agent running in another worktree, container or machine (herdr lanes, CI, a colleague). Then put it where both sides can read it — a repo path the user agreed to (gitignore it if it must not be committed), a Confluence/Jira page, or paste the text straight into `herdr agent prompt`.

### 4. Split durable from ephemeral
The doc dies with the task. Anything that outlives it — a project fact, an environment quirk, a decision, a user preference — goes to `vault_memory` (`write` a new atomic file, or `update` the existing one), and the doc just names that memory. Skip this and every future session re-learns the same thing.

### 5. Redact
No API keys, tokens, passwords, credential-bearing connection strings, customer data or PII. Reference secrets by name and location (`profile X in ~/.aws/credentials`, `env var Y`) instead of value. Assume the doc gets pasted into another tool.

### 6. Fill the template
Keep it under ~150 lines. A long handoff gets skimmed, and skimming loses the blocker.

```markdown
# Handoff — <slug> — <YYYY-MM-DD HH:MM>

**Next session's purpose:** <one line, from step 1>
**Continue by:** <resume the session | fresh agent + this doc>
**Source session:** `<absolute .jsonl path>` (id `<…>`)
**Repo state:** branch `<…>` @ `<sha>`, <N> uncommitted files

## Goal
<the outcome the user wants, not the task list>

## Constraints & Preferences
- <rules the user stated: never push without approval, keep it minimal, output language, …>

## Progress
### Done
- [x] <what> — evidence: <path / command / sha>
### In Progress
- [ ] <exactly where it stopped: file, function, the pending edit>
### Blocked
- <blocker · what was already tried · what would unblock it>

## Key Decisions
- **<decision>**: <rationale, and what was rejected>

## Next Steps
1. <concrete enough to start without reading anything else>

## Critical Context
- <the 3–7 facts without which the next step goes wrong: ports, env quirks, the failing test name, the reproduce command>

## Artifacts — read these, they are not repeated here
- `path/to/SPEC.md` — <what it settles>
- commit `<sha>` / PR <url> — <what it contains>
- vault memory `<name>` — <durable facts>

## Suggested skills for the next agent
- `<skill-name>` — <why> (`~/.agents/skills/<skill-name>/SKILL.md`)

## Files
<read-files>
path/one.ts
</read-files>
<modified-files>
path/two.ts
</modified-files>
```

Rules inside the template, from upstream:
- **Do not duplicate** what already lives in specs, plans, ADRs, issues, commits or diffs — reference by path or URL.
- **Do include a "Suggested skills" section** naming what the next agent should load.
- Verify every name you list actually exists, or the next agent hunts a ghost:
  ```bash
  for s in <skill-a> <skill-b>; do [ -e ~/.agents/skills/$s/SKILL.md ] || echo "MISSING $s"; done
  ```

### 7. Print the resume block in chat
```bash
pi --session "<path>"   # reopen that exact session with full history
pi --fork    "<path>"   # branch off it, leave the original untouched
pi --continue           # newest session for this cwd
pi -p "$(cat <handoff.md>)"   # headless one-shot seeded with the doc
```
Other tools: `claude` / `codex` in the same cwd, then point them at the handoff path (they have no access to pi's session files). In-session: `/import <path>` loads a JSONL session.

Finish with the two-line summary: the handoff path, and the first thing the next agent should do.
