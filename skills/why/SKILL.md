---
name: why
description: "Use for 'why does X work this way', 'why we picked Y', design rationale, regressions, postmortems, or data-backed thresholds. Discovers available MCPs via the pi gateway and queries each evidence category (source control, issue tracker, docs, chat, observability, error tracking, analytics) in parallel via subagents, then returns a cited read on decisions and tradeoffs."
---

# Why

Investigate the motivation and intent behind code. Why was it built this way? What edge cases were considered? What product, business, or operational constraints shaped the design? What alternatives were rejected, and why?

`why` answers what forces led to the code's shape — distinct from what the code does and how it works.

## How this skill works

Historical context spreads across seven evidence categories: source control history, issue/ticket tracking, long-form documents, real-time team chat, infrastructure observability, error/exception tracking, and product analytics warehouses. You cannot predict from the question alone which one holds the answer, so the skill enumerates available MCPs at run time (via the pi `mcp` gateway), maps each to a category, queries all available ones in parallel through subagents, then synthesizes with explicit confidence calibration. Null results from searched categories are first-class evidence; report them alongside positive findings. **The default is coverage, not minimalism.**

## Operating Posture

Operate as a careful, cautious, precise investigator — a detective piecing together a historical case from fragmentary records. When the record is thin, say so. This posture is the working method, not a disclaimer.

- **Evidence before narrative.** Collect the pieces first, then see what story they support. Never pick a story and recruit the evidence that fits it.
- **Precision over polish.** Prefer the exact quote and citation over a smooth paraphrase. A reader should be able to follow any claim back to its source in under a minute.
- **Consider what you haven't seen.** The evidence you find is a sample. Ask what you'd expect to see if an alternative explanation were true, and whether you looked for it.
- **Name the gaps.** If a thread goes cold or a source isn't searchable, document the gap. Don't paper it over with an authoritative-sounding guess.
- **Hedge on purpose.** When evidence is indirect, your language should signal it ("appears to", "likely", "suggests"). This is a feature of the output, not a stylistic choice.
- **No shortcut by code-reading.** The code tells you what it does, rarely why it exists. Resist inferring intent from code shape.

## Core Epistemics

This skill builds a **patchwork understanding** from fragmented historical evidence. Tickets go stale. Threads get deleted. Commit messages lie. The original author may have left. Be ruthlessly honest about what you know versus what you're inferring.

- **Cite everything.** Every claim about intent references a specific commit hash, PR number, ticket ID, doc URL, chat permalink, or code comment. If you can't cite it, it's inference, label it as such.
- **Prefer "appears to" over "because".** Reserve confident language for direct, explicit evidence.
- **Surface contradictions.** If two sources disagree, show both.
- **Acknowledge gaps.** An honest "we couldn't find out why" beats a confident guess.
- **Multiple hypotheses are valid.** When evidence fits several stories, present them all.
- **Beware rationalization.** Don't retrofit intent onto code that may have been written for reasons that no longer apply.

Load `references/epistemics.md` for the full confidence framework and phrasing guide. The synthesizer must follow it.

## Step 1 — Understand the Target and the Question

Parse what the user is asking. The **target** is usually a chunk of code, a pattern, a feature, or a named design decision. The **question** is usually one of: design rationale ("why designed this way?"), tradeoff/alternatives ("why X instead of Y?"), defensive reasoning ("what edge cases motivated this?"), external forcing function ("what business/product constraint led to this?"), dead-code ("why does this still exist?"), or a broad archaeological sweep ("history of X?").

If the target is vague, make your best guess from conversation context (open files, recent edits, what was just discussed). State your interpretation briefly so the user can redirect, then proceed.

## Step 2 — Establish the Code Anchor

Before spawning investigators, anchor the investigation in concrete code. Build this inline with `bash`/`read` — it's cheap, and every investigator needs it. You need the file path(s) and line range(s), the key symbols, an initial commit list, and PR numbers from merge commits.

```bash
git blame -L <start>,<end> <file>          # last-touch commits for target lines
git log --follow -p -- <file>               # full file history through renames
git log --oneline -20 -- <file>             # recent commits, PR numbers visible
git log -1 --format=%B <commit>             # extract PR number from a message
gh pr view <number> --json title,body,author,createdAt,mergedAt,labels,closingIssuesReferences,comments,reviews
```

Capture this as **seed context** (file paths, symbols, commits, PR numbers, linked ticket IDs) and pass it to every investigator so they don't rediscover it.

## Step 3 — Discover MCPs and Spawn Parallel Investigators

**Default to the full parallel investigation.** You cannot tell from the question which category holds the answer, so look across every available category in parallel.

### Discover

Enumerate connected MCP servers with `mcp({})`. For each server, use `mcp({ server })` / `mcp({ search })` to inspect its tools, then map it to **one** evidence category:

1. Source control history (always available via git + `gh`)
2. Issue / ticket tracker
3. Long-form documents
4. Real-time team chat
5. Infrastructure observability
6. Error / exception tracking
7. Product analytics warehouse

Classify using the server name, tool names, and descriptions. If a server could fit two categories, pick its primary evidence and record the ambiguity. Aim for a complete **coverage map**, not a minimal one — a null result is a useful fact.

### Spawn

Launch one investigator per category that has a matching MCP, **in a single `subagent` parallel call** so they run concurrently. One investigator per category — each specializes in one tool's query vocabulary. Don't pool MCPs into one agent, and don't chase cross-source links (record them as leads for the owning investigator).

Use the `subagent` tool, parallel mode (`tasks: [...]`), agent `generalPurpose` (confirm with `subagent({ action: "list" })`). Investigators need MCP + bash + read access and must not write/commit (posture, enforced by prompt). Use a fast model for investigators; reserve a stronger/thinking model for the synthesizer (Step 4).

Each investigator task is built from:
1. The base prompt in `references/investigator-prompt.md`
2. The category playbook in `references/sources/<source>.md` (see `references/source-playbook.md` for the index + how pi calls MCPs)
3. `references/sources/incident-postmortem.md` **if the target looks defensive** (null checks, retries, timeouts, rate limiting, feature flags, egress guards, OOM handlers)
4. The code anchor from Step 2
5. The user's original question

### When to skip an investigator

Only skip with an **explicit written justification** for the "Sources Consulted" section. Two valid reasons: (a) **no MCP available** for that category here (flag as a gap, not a choice), or (b) the source is **provably irrelevant** (a high bar — e.g. "Error tracking skipped: target is a build-time script with no runtime path"). "Probably won't have anything" is not sufficient — run the search and let the null result speak. The cost of an empty investigator is one subagent; the cost of missing a real design doc is a wrong answer.

## Step 4 — Synthesize

Spawn one synthesizer subagent (single `subagent` call, a stronger/thinking model). It must be able to read code (`read`/`ffgrep`/`bash`) and spot-verify citations through the `mcp` gateway, but must not write or mutate state. Give it:
1. All investigator findings (including nulls and skipped categories with reasons)
2. The code anchor from Step 2
3. The user's original question
4. `references/epistemics.md`
5. `references/synthesizer-prompt.md` (output format lives here)

## Step 5 — Present

Present the synthesizer's output. You may lightly edit for clarity, but **do not rewrite the confidence language** — the epistemic framing is the product. Dropping hedges to sound authoritative is the exact failure mode this skill prevents.

## Output Format

Keep the confidence separation intact. Sections: **The Question** · **The Code in Question** · **What We Found (direct evidence, cited)** · **What We Can Reasonably Infer (hedged, inference chain visible)** · **Competing Hypotheses** (skip if a clear answer) · **What We Don't Know** (explicit gaps + empty searches) · **Sources Consulted** (one line per investigator, including the empty ones and the skipped-with-reason ones — this is the coverage map).

Format each Sources Consulted line as: `- <Source>: <what was searched>. <what was found, or "no relevant results," or "skipped. reason">.` If the `why` is a precursor to changing the code, convert the findings into a Preserve / Change / Avoid / Risk constraint set after the sources block. Full templates and examples are in `references/synthesizer-prompt.md`.

## Common Failure Modes to Avoid

- **Confident storytelling** — a bullet with no citation goes in "inferred" or "hypotheses," not "what we found."
- **Citing the code as evidence for its own intent** — that's mechanics, not motivation.
- **Recency bias** — the newest commit isn't authoritative; trace back.
- **Sycophantic agreement** — if the user embeds a hypothesis, treat it as a candidate and check evidence independently.
- **Skipping the gaps section** — an honest accounting of what you couldn't find is part of the value.
- **Skipping investigators by anticipation** — a null result is a data point; a skipped search is a blind spot.
- **Collapsing investigators into one agent** — always one investigator per category.

## Reference Files

| File | When to load |
|---|---|
| `references/epistemics.md` | Building the answer / synthesizing — confidence tiers + phrasing guide. The synthesizer must follow it. |
| `references/investigator-prompt.md` | Composing each investigator subagent's task prompt. |
| `references/source-playbook.md` | Mapping discovered MCPs to categories; how pi calls MCPs via the gateway. Index of the playbooks below. |
| `references/sources/code-archaeology.md` | Source control investigator (git + `gh`). |
| `references/sources/linear.md` | Issue/ticket tracker investigator (Linear → adapt for Jira/GitHub Issues/Plane/Shortcut). |
| `references/sources/notion.md` | Long-form docs investigator (Notion → adapt for Confluence/Google Docs/Coda). |
| `references/sources/slack.md` | Real-time chat investigator (Slack → adapt for Discord/Teams/Mattermost). |
| `references/sources/datadog.md` | Infra observability investigator (Datadog → adapt for New Relic/Honeycomb/Grafana/Splunk). |
| `references/sources/sentry.md` | Error/exception tracking investigator (Sentry → adapt for Rollbar/Bugsnag/Airbrake). |
| `references/sources/databricks.md` | Product analytics warehouse investigator (Databricks → adapt for Snowflake/BigQuery/ClickHouse/dbt). |
| `references/sources/incident-postmortem.md` | Cross-cutting — add to an investigator when the target code looks defensive. |
| `references/synthesizer-prompt.md` | Composing the synthesizer subagent's task prompt; full output format + quality checklist. |
