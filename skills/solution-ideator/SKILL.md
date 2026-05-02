---
name: solution-ideator
description: Expand a shapeless problem (or an already-chosen solution) into a pruned tree of alternative approaches, score survivors against user-declared constraints, and recommend one path with an ADR-ready rejected-alternatives log. Use when user says "brainstorm options", "explore solutions", "should I build X or Y", "what are the alternatives", "ideate on this problem", or presents a vague problem with no obvious approach yet.
---

# Solution Ideator

Expand a problem into solution approaches, prune branches that violate hard constraints, score survivors, and recommend one path. Output is designed to feed a downstream product-spec, interface-design, or grilling workflow — whichever applies.

## When to use this skill

| Situation | Fit |
|---|---|
| Shapeless problem, no approach chosen yet | ✓ yes |
| "Should we build X or buy Y?" | ✓ yes |
| Evaluating an already-chosen solution against alternatives | ✓ yes (solution-evaluation mode) |
| Problem is well-framed and approach is obvious | ✗ skip to writing a product spec, or just build |
| Module-level API design question | ✗ do an interface-design exploration instead (generate alternative API shapes, compare) |
| User has a plan and wants it pressure-tested | ✗ run a structured grilling session on the plan |
| Debugging / "why is this slow?" | ✗ use a disciplined diagnosis loop (reproduce → minimise → hypothesise → fix) |

Before starting, check decline conditions. If a redirect matches, surface it:

> "This looks like [type], not solution-ideation. A different workflow is a better fit (e.g., [brief activity description]). Proceed anyway?"

Decline rules are **warnings, not blocks**. User can override. But state them — routing help is part of the skill's job.

## Process

### 1. Classify input (always ask, never guess)

Read the user's input. Then ask one question:

> "Are you asking me to (a) explore solutions to a problem, (b) evaluate a solution you've already picked, or (c) something else? The framing matters — I handle them differently."

Four input types:

- **`problem`** — shapeless or semi-framed problem, no approach chosen.
- **`solution`** — user has a proposed solution, wants alternatives + comparison.
- **`ambiguous`** — ask one clarifying question before proceeding.
- **`multi-problem`** — user dumped several tangled problems. Ask which one they want to ideate on; do not proceed with more than one.

**For `solution` input**, do not skip the problem-validation step. Extract the underlying problem and state back:

> "Your proposed solution: **X**. My read of the underlying problem: **Y**. Confirm or correct before I generate alternatives."

The user's original solution becomes a **non-privileged branch** in the tree. It competes on the same rubric as newly-generated branches. No incumbency credit.

If the user insists on evaluating their solution without problem validation, proceed — but flag it in the final artifact:

> ⚠️ Ran in solution-evaluation mode. The underlying problem was not validated. If the problem is wrong, the recommendation is wrong.

### 2. Gather constraints (up to 4 questions, one at a time)

Skip any question the user already answered. Never proceed with zero constraints — at minimum, ask about success criteria.

Ask from this fixed menu:

1. **Success criteria** — "What does 'solved' look like in 6 months? Be specific — metrics, user behaviours, or team outcomes."
2. **Hard constraints** — "What's non-negotiable? Stack, budget, timeline, compliance, team skills, infra."
3. **Existing context** — "Is there prior art here — a previous attempt, a system this has to integrate with, something that already failed?"
4. **Decision reversibility** — "Is this a one-way door or a two-way door? How expensive is it to change course in 3 months?"

**For every constraint mentioned, tag it**:

- **`MUST`** — hard. Violating = branch dies in pruning.
- **`SHOULD`** — soft. Violating = scoring penalty, branch survives.

Ask the user per constraint:

> "'No external SaaS' — is that a `MUST` (kills any branch that uses SaaS) or a `SHOULD` (preference, can be violated if the alternative is much better)?"

If the user says "I don't know, just generate the tree", proceed with everything tagged `SHOULD` and flag assumptions in the artifact.

### 3. Propose axes (4–6 candidates → user picks 2–3)

Generate 4–6 candidate solution axes. For each axis, provide a one-line justification showing it passes three tests:

1. **Orthogonal** — moving along axis X doesn't force a move along axis Y.
2. **Decision-relevant** — the user would make a different choice depending on axis position.
3. **Spans viable space** — both ends are viable given the constraints.

Reference menu (not exhaustive — use domain-specific axes when they fit better):

- build vs. buy vs. integrate
- synchronous vs. asynchronous
- centralised vs. distributed
- human-in-the-loop vs. fully automated
- generic vs. domain-specific
- server-side vs. client-side vs. edge
- stateful vs. stateless
- batch vs. streaming
- push vs. pull
- config-driven vs. code-driven

**Hard cap at 3 axes.** 3 × 2 = 8 leaves is already a lot to evaluate. Resist 4+.

Avoid lazy axes: "simple vs. complex", "fast vs. slow", "good vs. bad" — these aren't axes, they're evaluation criteria.

Present the candidates:

```
Candidate axes:
1. Build vs. buy vs. integrate — determines where implementation effort goes
2. Synchronous vs. asynchronous — affects user perception and failure modes
3. Per-tenant vs. shared — affects cost model and isolation guarantees
4. Provider-specific vs. abstracted — affects lock-in and migration cost
5. Real-time vs. batched — affects latency and operational complexity

Which 2–3 do you want the tree to span?
```

### 4. Expand the tree (2 levels deep, always)

For each combination of axis positions, generate a concrete branch. Two levels:

- **Level 1**: the approach (defined by axis positions).
- **Level 2**: one concrete implementation variant per approach.

Do not go deeper than 2 levels — deeper trees become unreadable and the model hallucinates filler at level 3+.

Example with 2 axes (build-vs-buy, sync-vs-async):

```
Branch A: Build + synchronous
  → A1: In-process HTTP call with retry middleware
Branch B: Build + asynchronous
  → B1: Queue + background worker (Redis/SQS)
Branch C: Buy + synchronous
  → C1: Call SaaS API directly from request handler
Branch D: Buy + asynchronous
  → D1: SaaS provider's webhook-based flow
```

If the user's original input was a `solution`, include their solution as one of the branches — fit it into the axes. Do not invent a special slot for it.

### 5. Prune (never silently drop)

Apply pruning rules:

1. **Any branch violating a `MUST`** → pruned with the specific constraint cited.
2. **List every pruned branch** with its killer. Silent drops are banned.
3. **User can override any prune.** "Actually keep branch C alive" → branch returns, evaluated against a relaxed constraint (noted in artifact).
4. **If >50% of branches are pruned**, stop and surface it:

   > "5 of 8 branches died on `MUST: on-prem only`. Constraints may be over-specified, or the axes are wrong. Want to re-pick axes?"

5. **Minimum survivors: 2.** If only 1 branch survives, exit cleanly:

   > "Only one branch survived the constraints. You already have your answer: **X**. The others died on: [list with reasons]. Nothing to ideate — no recommendation needed."

Pruning output format:

```
Branch                           Status        Reason
───────────────────────────────  ───────────  ─────────────────────────
Build + sync                     ✓ survives
Build + async                    ✓ survives
Buy + sync                       ❌ pruned    violates MUST: on-prem only
Buy + async                      ❌ pruned    violates MUST: on-prem only
Integrate OSS + sync             ✓ survives
Integrate OSS + async            ⚠ borderline violates SHOULD: minimise
                                              operational surface
                                              (penalty applied in eval)
```

### 6. Evaluate survivors (thin rubric + narrative)

Score each surviving branch against the Q2 criteria, using three levels only — `✓` / `~` / `✗`. **Never numeric scores.** Numeric precision is fiction.

Rubric axes (reuse constraints from step 2):

- Hits success criteria
- Each `SHOULD` constraint (one row per)
- Reversibility (one-way cost)
- Implementation cost (S / M / L — not hours)

Example:

```
                              Branch A       Branch B       Branch E
                              (build+sync)   (build+async)  (integrate)
────────────────────────────  ─────────────  ─────────────  ─────────────
Hits success criteria         ✓              ✓              ~
SHOULD: minimise ops surface  ✓              ✗              ~
SHOULD: team knows stack      ✓              ✓              ~
Reversibility                 ~ hard         ✗ very hard    ✓ easy
Implementation cost           M              L              S
```

After the table, write **one paragraph per branch** explaining the trade-off in the user's own language. The table is the skeleton; the narrative carries the insight. Without narrative, a ✓✓✓ branch can look like a winner when it isn't.

### 7. Recommend (with revisit triggers)

Pick one branch. Format:

```markdown
## Recommendation: Branch B (build + async via Redis queue)

**Why this one:** [2–4 sentences tying to the user's specific
success criteria and constraints — not generic pros like "scalable".]

**What you're giving up:**
- [concrete thing]
- [concrete thing]

**When you'd revisit this decision:**
- [specific trigger — e.g., "if queue depth regularly exceeds 10k"]
- [specific trigger — e.g., "if team grows beyond 2 backend engineers"]

**Rejected alternatives (ADR-ready):**
- Branch A (build + sync): [one-line reason, citing specific constraint]
- Branch E (integrate OSS): [one-line reason]
- Branch C (buy + sync, pruned): violates MUST: on-prem only
- Branch D (buy + async, pruned): violates MUST: on-prem only
```

The **"when you'd revisit"** section is non-optional. It's what makes the decision auditable 6 months later — the rejection reasons become conditionally invalid when the triggers fire.

### 8. Save artifact

Always save. No opt-out. Deterministic filename:

```
SOLUTION-TREE-[slug]-[YYYY-MM-DD].md
```

Location: repo root if inside a git repo, else `~/solution-trees/`. Slug derived from the problem statement — user can override.

Full artifact structure in [references/artifact-template.md](references/artifact-template.md).

### 9. Recommend next step (never auto-invoke)

End the session with a suggested next activity:

| Session outcome | Suggested next activity |
|---|---|
| Approach chosen, need product spec | Formalise the approach into a PRD / product spec |
| Approach chosen, it's an API-shape problem | Design the module's interface (ideally by generating alternatives and comparing) |
| User wants to pressure-test the recommendation | Run a structured grilling session on the recommendation |
| Approach chosen, implementation is straightforward | Just build |
| Exit case ("already had your answer") | Nothing to do |

If the user has a skill or established workflow for the suggested activity, they should use it. If not, describe the activity in plain terms so they can run it manually.

Handoff message format:

> "Approach settled: **[recommendation]**. Suggested next step: [activity]. These are decided — don't re-ask: [list]. See `SOLUTION-TREE-[slug]-[date].md`."

The "don't re-ask" list is the real handoff payload. Without it, the next step burns a round-trip rediscovering what this session already resolved.

## Rules

- **One question at a time.** Never batch. User provides their recommended answer per question.
- **Never silently drop a branch.** Every pruned option is logged with its killer.
- **Never use numeric scores.** Three levels only: `✓` / `~` / `✗`.
- **Never auto-invoke the next step.** Suggest, don't chain.
- **Never proceed with zero constraints.** Success criteria at minimum.
- **Never exceed 3 axes.** 8 leaves is already a lot.
- **Never go deeper than 2 tree levels.** Deeper → hallucinated filler.
- **Never privilege the user's original solution** in solution-mode. It competes equally.

## Example Walkthrough

See [references/example-transactional-email.md](references/example-transactional-email.md) for a complete session on "we need to send transactional email from our app" — from input classification through recommendation and handoff.
