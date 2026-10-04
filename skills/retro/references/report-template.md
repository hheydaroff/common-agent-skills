# Report template

Show this in chat. Do not save it to the repo unless the user asks (then `<cwd>/docs/report_retro-YYYY-MM-DD.md`; the metrics comment is only needed in that case).

```markdown
# Retro — <folder name> — YYYY-MM-DD

<!-- retro-metrics: {paste aggregate.metrics as single-line JSON} -->

**Scope:** <cwd>, last N sessions (<first date> → <last date>), flags: <flags>
**Sample note:** <only if <5 sessions: numbers are anecdotal>

## Snapshot
| Metric | Prev | Now |
|---|---|---|
| sessions / cost total / cost per session | | |
| nav calls before first edit (median) | | |
| corrections per session | | |
| tool error rate | | |
| unverified code rate | | |
| compactions per session | | |
(omit Prev column if no previous retro)

## Previous proposals
| # | Proposal | Status | Evidence |
|---|---|---|---|
(✅ worked / ➖ no change / ❌ worse / ⏳ not applied)

## Proposals
### 1. <imperative title>  — home: <repo-navigability|process|automation|skill|rule|tooling|growth>
- **Finding:** one sentence.
- **Evidence:** session `<8-char id>` <date>: quote or numbers (from excerpt/digest).
- **Fix:** exact change (file, text to add/remove/replace).
- **Replaces/removes:** what gets deleted or why nothing can.
- **Expected metric movement:** which metric should drop.
- **Status:** proposed

(≤10, ordered by expected payoff ÷ effort)

## Growth observations
Patterns in how work was requested/verified, each with evidence. No advice without numbers.

## Repo health
Short list from `repo` (missing PRD/SPEC, tests, CI, stale pointers, AGENTS.md length).

## Not acted on
Flags checked and dismissed as false positives (one line each), so the next retro does not re-raise them.
```
