---
name: how
description: "Use for \"how does X work\", code walkthroughs before changing something, and placement / ownership / layering questions (\"where should this live\", \"which package owns this\", \"is this the right layer\"). Explains subsystem architecture, runtime flow, onboarding mental models. Can critique architecture. Use the why skill for motivation."
---

# How

Explore the codebase to answer "how does X work?" questions. Produce clear architectural explanations at the level of a senior engineer onboarding onto a subsystem. Enough to build a working mental model, not annotated source code.

Companion to the `why` skill: `how` answers what the code does and how it works; `why` answers what forces shaped it.

Two modes:

1. **Explain** (default). Explore the codebase and produce a clear explanation.
2. **Critique.** Explain first, then spawn multiple models to independently identify architectural issues.

All subagents run via the pi `subagent` tool (`agent: generalPurpose` — confirm with `subagent({ action: "list" })`). Explorers/critics fan out in a single parallel `subagent` call (`tasks: [...]`); the explainer is a single call. Subagents are read-only here: they use `read`/`ffgrep`/`fffind` and must never write, edit, or commit. Use a fast model for explorers; a stronger/thinking model for the explainer and critics.

## Explain Mode

### Step 1 — Understand the Question and Assess Complexity

Parse what the user is asking about:

- "How does the rate limiter work?" — a subsystem
- "How do we handle billing for on-demand usage?" — a feature flow
- "How is the auth service structured?" — an architectural overview
- "Walk me through what happens when a user submits a form" — a runtime trace

Identify the scope. If ambiguous, state your best-guess interpretation before exploring. Don't ask — let the user redirect if you're off.

**Assess complexity to decide the approach:**

- **Simple** (a single module, a small utility, a narrow question like "how does function X work"): skip explorer agents; the explainer explores and explains in a single pass. Go to Step 2b.
- **Complex** (a subsystem spanning multiple files/services, a cross-cutting feature, a full architectural overview): spawn parallel explorer agents first, then hand off to the explainer. Go to Step 2a.

When in doubt, lean simple. You can always spawn explorers if the explainer hits a wall.

### Step 2a — Explore (complex questions only)

Decompose the question into 2-4 parallel exploration angles, each a distinct slice so explorers don't duplicate work. Example split for "how does the rate limiter work?":

- Explorer 1: data model and state management
- Explorer 2: request path and enforcement
- Explorer 3: configuration and metrics infrastructure

The right decomposition depends on the question. Narrow questions: 2 explorers. Broad subsystems: up to 4.

Spawn all explorers in a single parallel `subagent` call, fast model. Each explorer task is the base prompt from `references/explorer-prompt.md` plus a specific angle naming its slice. Each explorer should:
- Start broad: `fffind` for relevant directories, `ffgrep` for key types/interfaces/class names.
- Follow the thread: from an entry point, trace the call chain (callers, callees, data flow, type definitions).
- Read the actual code (`read`), don't guess from file names.
- Stop when it can describe the full path from input to output (or trigger to effect) without hand-waving any step.
- Note things that are surprising, non-obvious, or that a newcomer would get wrong.

Each explorer returns structured findings: components found, flow traced, files read, anything non-obvious. Overlap is fine; the explainer reconciles. Then go to Step 3.

### Step 2b — Direct Explain (simple questions)

Spawn a single `subagent` (stronger/thinking model) that explores and explains in one pass. It does its own exploration (`fffind`, `ffgrep`, `read`) and writes the explanation directly. Use `references/explainer-prompt.md` for the communication style and output format — same structure, just no explorer findings as input. Then go to Step 4.

### Step 3 — Synthesize (complex questions only)

Once all explorers return, spawn a single `subagent` (stronger/thinking model) to synthesize their findings into one coherent explanation. It gets all explorers' findings and writes the human-facing explanation (output format below), using `references/explainer-prompt.md` for the full prompt template. It reconciles overlapping findings, resolves contradictions (by re-checking code read-only), and weaves the slices into a unified picture.

### Step 4 — Present

Present the explainer's output. You may lightly edit for clarity or add conversational context, but don't substantially rewrite — the explainer's communication is the product.

### Output Format

Adapt to the question; not every section is needed every time.

- **Overview.** 1-2 paragraphs: what it is, what it does, why it exists. Enough to decide whether to keep reading.
- **Key Concepts.** The important types, services, or abstractions, briefly defined. Just the ones needed to follow the rest.
- **How It Works.** The core. Walk through the flow: what triggers it, what happens step by step, where data goes, the decision points. Prose, not pseudocode. Reference specific files and functions; don't dump code blocks unless a snippet is genuinely necessary. Add a mermaid or ASCII diagram when it clarifies a multi-component flow.
- **Where Things Live.** A brief map of the relevant files/directories needed to start working in this area.
- **Gotchas.** Non-obvious or surprising things, historical context that explains weirdness, known sharp edges.

## Critique Mode

Triggered when the user asks for architectural issues, problems, or improvements — not just understanding.

### Step 1 — Explain First

Run the full Explain flow above (Steps 1-4). You must understand the architecture before critiquing it.

### Step 2 — Spawn Critics

After the explanation is complete, spawn multiple architectural critics in a single parallel `subagent` call, each on a **different model** (e.g. your strongest thinking model plus one or two others) so you get independent perspectives. Each critic task uses `references/critic-prompt.md` and gets:
1. The explanation from Step 1 (so they don't re-explore).
2. The relevant file paths (so they can read the actual code).
3. The architectural critique rubric from `references/critique-rubric.md`.

Escalate any critic to a deeper-reasoning model when the architecture warrants it.

### Step 3 — Lead Judgment

You're a pragmatic lead, not an aggregator. Categorize findings:
- **Act on.** Architectural problems worth fixing now.
- **Consider.** Real concerns, but the cost/benefit is unclear.
- **Noted.** Valid observations, low priority.
- **Dismissed.** Wrong, missing context, or style preference.

Present the explanation first (from Step 1), then the critique verdict below it. The explanation should stand on its own; someone who just wants to understand the system shouldn't wade through critique.

## Reference Files

| File | When to load |
|---|---|
| `references/explorer-prompt.md` | Composing each explorer subagent's task prompt (complex questions, Step 2a). |
| `references/explainer-prompt.md` | Composing the explainer subagent's task prompt (Step 2b / Step 3) — communication style + output format. |
| `references/critic-prompt.md` | Composing each critic subagent's task prompt (Critique Mode, Step 2). |
| `references/critique-rubric.md` | The architectural-critique rubric handed to every critic. |
