---
name: parallel-agent-lanes
description: "Orchestrate several autonomous coding agents in parallel on one repo: git worktree + branch + private ports/database per lane (herdr panes running pi), written briefs, lock protocol for shared browser/Mac GUI, sequential merges with in-lane conflict resolution, LANE-RESULT reports, and a pre-push gate between merges. Use when asked to fan work out to lanes/worktrees/agents, run an AFK multi-task wave, watch and merge lane branches, or write a lane brief. Proven on the Slaide v2 repo (tools/lanes, docs/v2/LANES.md)."
---

# Parallel agent lanes

## When to Use
A backlog of tasks that touch mostly separate files and each take 1–4 h, no human at the keyboard, and a repo with a real gate (pre-push hook). Not for one small fix: a single lane costs more than doing it inline.

If the repo already has `docs/v2/LANES.md` + `tools/lanes/` (smartai-slaidePPT), use them: they are the canonical, maintained version of this skill.

## Steps
1. **One lane = one worktree + branch + port triplet + database.** `git worktree add ../wt/<TASK> -b v2/<TASK> <base>`; install deps; symlink big gitignored inputs (don't copy); copy certs. Never share a DATA_DIR/database name between lanes; share only the Postgres server.
2. **Write the brief** (≤ 1 page): lane name/branch/base sha/ports/DB, context with evidence, numbered tasks each with the acceptance evidence, locks needed, close steps. Rules go in one repo doc every brief points to (`read RULES + brief, nobody is at the keyboard, decide and record, end with LANE-RESULT: PASS|FAIL|PARTIAL <task> <sha>`).
3. **Launch**: herdr tab in the worktree, `herdr agent start <lane-name> --kind pi --pane <p> -- --model <stable model>`, wait ~6 s (retry once), `herdr agent prompt`. Prefer a stable provider for multi-hour lanes; stagger starts (concurrent init loses prompts).
4. **Watch** by polling `herdr agent list` in ≤ 300 s calls; idle ≠ done — read `.lane-report/<TASK>.md` and the LANE-RESULT line. A lane waiting for permission is nudged: continue without asking, retry smaller.
5. **Shared GUI/browser**: `mkdir /tmp/<proj>/browser.lock` (owner file, backoff, release on every path); a lane needing two locks takes both or none. Separate private stacks for API-only tests so only pane tests contend.
6. **Merge sequentially** in dependency order. Conflict → abort, tell the lane to merge the base INTO its branch (append-only blocks: keep both; generated files: take theirs and regenerate), resubmit. After each merge run the full gate in the background (long gates exceed tool timeouts) and require exit 0 before the next merge.
7. **Speculative lanes** may build on an unapproved draft contract branch: no merge to base, commits must not touch frozen paths, only the freeze-guard failure on inherited draft commits is allowed.
8. **Fix lanes** (defects found by proofs): defect class, RED test at the shared layer, no scenario/prompt special-casing, held-out proof ≥ 10 cases before/after.
9. **Clean up**: remove merged worktrees with `git worktree remove` (judge "merged" with `git cherry`, hashes change after history rewrites), drop lane databases, prune private-stack data dirs, move conclusions from lane reports into the docs they affect.

## Gotchas
- Timeouts on every GUI call (macOS has no `timeout`); keep all files inside the worktree; avoid short names/commands the security layer mistakes for network tools; write scripts with the file tool, not heredoc+sed.
- Stale dev stacks from another checkout hold the default ports and serve old code — check listeners and cwd before trusting a run.
- Lane reports for runs that failed the briefed sequence must say how the condition was forced.
- Re-test "obvious" fixes on the real host: the D-02 layout graft passed all unit tests and still triggered a repair dialog in PowerPoint for Mac.
- Expect 1–2 session restarts per 4 h (auto-update, content filter on one provider): keep a fallback model and a restart recipe.
