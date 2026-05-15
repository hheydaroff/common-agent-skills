---
name: solution-ideator
description: "Explore what to build (Opportunity Solution Tree) or how (decision tree). Two modes: Discovery maps outcomes to opportunities/solutions; Decision prunes alternatives against constraints. Use when user says \"brainstorm options\", \"explore solutions\", \"OST\", or has a vague problem."
---

# Solution Ideator

Two modes under one roof:

- **Discovery mode** (Opportunity Solution Tree) — Start from a business outcome, map customer opportunities, generate solutions per opportunity, design experiments to validate. Use when the *problem worth solving* is unclear.
- **Decision mode** — Start from a known problem, generate solution approaches along orthogonal axes, prune against hard constraints, score survivors, and recommend one path. Use when the *problem is clear* but the *approach* is not.

Both modes produce a saved artifact. Discovery mode can hand off to Decision mode when you need to pick *how* to implement the winning solution.

---

## When to use this skill

| Situation | Mode |
|---|---|
| "What should we build next?" / unclear which problem to solve | Discovery |
| Business metric to improve + customer research available | Discovery |
| Mapping opportunities for a product outcome | Discovery |
| Shapeless technical problem, no approach chosen | Decision |
| "Should we build X or buy Y?" | Decision |
| Evaluating an already-chosen solution against alternatives | Decision |

**Decline conditions** (warn, don't block):

| Situation | Redirect |
|---|---|
| Problem is well-framed and approach is obvious | Skip to writing a product spec, or just build |
| Module-level API design question | Interface-design exploration (generate alternative API shapes, compare) |
| User has a plan and wants it pressure-tested | Structured grilling session |
| Debugging / "why is this slow?" | Disciplined diagnosis loop |

> "This looks like [type], not solution-ideation. A different workflow is a better fit (e.g., [brief activity description]). Proceed anyway?"

---

## Step 0 — Route

Read the user's input. Ask:

> "Are you looking to (a) discover what's worth building — map an outcome to opportunities and solutions, (b) decide how to build something — compare technical approaches to a known problem, or (c) evaluate a solution you've already picked against alternatives?"

Three modes:

- **(a) → Discovery mode** (OST)
- **(b) → Decision mode** (technical tree)
- **(c) → Decision mode** in solution-evaluation variant

If the input clearly maps to one mode, state which and proceed. Only ask if ambiguous.

---

# Discovery Mode (Opportunity Solution Tree)

Based on Teresa Torres' *Continuous Discovery Habits*. Prevents teams from jumping to solutions by forcing them to first map the opportunity space.

## D1. Define the desired outcome

Ask:

> "What's the single measurable outcome you're pursuing? (e.g., 'increase 7-day retention to 40%', 'reduce support tickets by 30%'). This should come from your OKRs or product strategy."

Requirements for a good outcome:
- **Measurable** — has a number or observable state change
- **Singular** — one metric, not a bundle
- **Time-bound** — implies a timeframe
- **Within team's influence** — not a pure business metric the team can't move

If the user gives a vague outcome ("improve onboarding"), push for specificity:

> "Can you make that measurable? What does 'improved onboarding' look like in numbers — completion rate, time-to-value, activation %?"

## D2. Map opportunities (3–7)

From provided research (interviews, analytics, feedback, surveys), identify customer opportunities. These are **needs, pain points, or desires** — not features.

Framing rules:
- Always from the customer's perspective: "I struggle to…", "I wish I could…", "I don't understand why…"
- Never solution-shaped: ❌ "Add a dashboard" → ✓ "I can't see how I'm progressing"
- Group related opportunities under a parent if they share a theme

If the user has no research, ask:

> "What do you know about your users' struggles related to this outcome? Interviews, support tickets, analytics drop-offs, NPS comments — anything."

If truly nothing exists, flag it:

> ⚠️ No customer research available. Opportunities below are hypotheses, not validated. Treat the entire tree as speculative until you run discovery interviews.

Present opportunities in a numbered list with one-line evidence citation per opportunity.

## D3. Prioritize opportunities

Score each opportunity using **Opportunity Score**:

```
Score = Importance × (1 − Satisfaction)
```

- **Importance** (0–1): How much does this matter to the customer's job-to-be-done?
- **Satisfaction** (0–1): How well is this currently solved (by you or competitors)?

High importance + low satisfaction = biggest opportunity gap.

If quantitative data isn't available, use qualitative tiers:

| Tier | Meaning |
|------|---------|
| 🔴 High opportunity | High importance, low satisfaction |
| 🟡 Medium opportunity | Mixed signals |
| 🟢 Low opportunity | Already well-served or low importance |

Ask the user to confirm the top 2–3 opportunities to pursue. Don't proceed with more than 3.

## D4. Generate solutions (3+ per opportunity)

For each prioritized opportunity, brainstorm **at least 3 solutions**. Ideate from multiple perspectives:

- **PM perspective** — process/flow changes, positioning, packaging
- **Designer perspective** — UX patterns, information architecture, progressive disclosure
- **Engineer perspective** — technical capabilities that enable new experiences

Additionally, apply **divergent thinking lenses** to force non-obvious ideas:

| Lens | Prompt |
|------|--------|
| **Inversion** | "What if we did the opposite?" |
| **Constraint removal** | "What if budget/time/tech weren't factors?" |
| **Audience shift** | "What if this were for [different user]?" |
| **Combination** | "What if we merged this with [adjacent idea]?" |
| **Simplification** | "What's the version that's 10x simpler?" |
| **10x version** | "What would this look like at massive scale?" |
| **Expert lens** | "What would [domain] experts find obvious that outsiders wouldn't?" |

Pick 2-3 lenses per opportunity to push past conventional thinking.

Rules:
- Never commit to the first idea. The "compare and contrast" principle is non-negotiable.
- Solutions should be genuinely different approaches, not variants of the same idea.
- Include at least one "weird" or unconventional option — it often sparks the best hybrid.

Present as a tree:

```
Opportunity: "I can't tell if I'm making progress"
├── S1: Visual progress bar with milestones (Designer)
├── S2: Weekly email digest with metrics delta (PM)
├── S3: AI-generated "progress narrative" from activity data (Engineer)
└── S4: Peer comparison — "you're ahead of 60% of users at this stage" (PM)
```

## D5. Design experiments

For the most promising 1–2 solutions per opportunity, design a fast validation experiment.

Each experiment specifies:

| Field | Content |
|-------|---------|
| **Assumption being tested** | The riskiest assumption (Value / Usability / Viability / Feasibility) |
| **Hypothesis** | "We believe [solution] will [outcome] for [segment] because [reason]" |
| **Method** | Prototype test, fake-door, Wizard of Oz, concierge, survey, data analysis, etc. |
| **Metric** | What you measure |
| **Success threshold** | Minimum bar to proceed (e.g., "≥40% click the fake door") |
| **Timeline** | How long to run |
| **Skin-in-the-game?** | Does the test require real commitment from participants? (prefer yes) |

Prefer experiments where participants have "skin in the game" (Alberto Savoia) — time, money, or reputation — over opinion-based validation ("would you use this?" is nearly worthless).

## D6. Visualize the full tree

Present the complete OST:

```
🎯 Outcome: [measurable outcome]
│
├── 🔴 Opportunity 1: "[customer framing]"  (Score: 0.72)
│   ├── Solution A: [description]
│   │   └── Experiment: [method] → success if [threshold]
│   ├── Solution B: [description]
│   │   └── Experiment: [method] → success if [threshold]
│   └── Solution C: [description]
│
├── 🔴 Opportunity 2: "[customer framing]"  (Score: 0.65)
│   ├── Solution D: [description]
│   ├── Solution E: [description]
│   │   └── Experiment: [method] → success if [threshold]
│   └── Solution F: [description]
│
└── 🟡 Opportunity 3: "[customer framing]"  (Score: 0.48)
    ├── Solution G: [description]
    └── Solution H: [description]
```

## D7. Save artifact

Save as `OST-[slug]-[YYYY-MM-DD].md`. Location: repo root if inside a git repo, else `~/solution-trees/`.

Full artifact structure in [references/ost-artifact-template.md](references/ost-artifact-template.md).

## D8. Recommend next step

| Outcome | Next step |
|---|---|
| Top solution identified, need to decide *how* to implement | Transition to **Decision mode** (below) for technical approach |
| Experiments designed, ready to validate | Run the experiments — come back with results |
| Opportunities unclear, need more research | Run discovery interviews focused on the outcome |
| Single obvious solution survived | Skip to product spec / just build |

Handoff format:

> "Discovery complete. Top opportunity: **[opportunity]**. Most promising solution: **[solution]**. Next step: [activity]. See `OST-[slug]-[date].md`."

If transitioning to Decision mode, carry forward:
- The chosen opportunity (becomes the "problem" input)
- The solution candidates (become pre-seeded branches)
- Any constraints discovered during discovery

---

# Decision Mode

Start here when the problem is known and you need to pick an implementation approach.

## Step 1 — Classify input

If not already routed from Step 0, classify:

- **`problem`** — shapeless or semi-framed problem, no approach chosen.
- **`solution`** — user has a proposed solution, wants alternatives + comparison.
- **`from-discovery`** — transitioned from Discovery mode (opportunity + solutions already defined).

**For `solution` input**, extract the underlying problem:

> "Your proposed solution: **X**. My read of the underlying problem: **Y**. Confirm or correct before I generate alternatives."

The user's original solution becomes a **non-privileged branch**. No incumbency credit.

**For `from-discovery` input**, restate:

> "From discovery: solving opportunity **[X]** to drive outcome **[Y]**. Pre-seeded solutions: [list]. I'll add more branches and evaluate all equally."

## Step 2 — Gather constraints (up to 4 questions, one at a time)

Skip any question already answered (especially if coming from Discovery mode). Never proceed with zero constraints.

1. **Success criteria** — "What does 'solved' look like in 6 months? Metrics, user behaviours, or team outcomes."
2. **Hard constraints** — "What's non-negotiable? Stack, budget, timeline, compliance, team skills, infra."
3. **Existing context** — "Prior art — previous attempts, integrations, things that already failed?"
4. **Decision reversibility** — "One-way door or two-way door? How expensive to change course in 3 months?"

Tag each constraint:

- **`MUST`** — hard. Violating = branch dies in pruning.
- **`SHOULD`** — soft. Violating = scoring penalty, branch survives.

Ask per constraint:

> "'No external SaaS' — is that a `MUST` (kills any branch) or a `SHOULD` (preference, violable if alternative is much better)?"

If user declines to specify: tag everything `SHOULD`, flag assumptions in artifact.

## Step 3 — Propose axes (4–6 candidates → user picks 2–3)

Generate 4–6 candidate solution axes. Each must pass three tests:

1. **Orthogonal** — moving along axis X doesn't force a move along axis Y.
2. **Decision-relevant** — user would make a different choice depending on position.
3. **Spans viable space** — both ends are viable given constraints.

Reference menu (use domain-specific axes when they fit better):
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

**Hard cap: 3 axes.** Resist 4+. Avoid lazy axes ("simple vs. complex").

Present candidates and ask user to pick 2–3.

## Step 4 — Expand the tree (2 levels deep)

For each combination of axis positions, generate a concrete branch:

- **Level 1**: the approach (defined by axis positions)
- **Level 2**: one concrete implementation variant per approach

Never go deeper than 2 levels.

If coming `from-discovery`, map pre-seeded solutions onto the axis grid. Add new branches to fill gaps.

## Step 5 — Prune

Apply pruning rules:

1. Any branch violating a `MUST` → pruned with specific constraint cited.
2. List **every** pruned branch with its killer. Silent drops are banned.
3. User can override any prune.
4. If >50% pruned → surface it: "Constraints may be over-specified, or axes are wrong. Re-pick?"
5. Minimum survivors: 2. If only 1 survives → exit cleanly with the answer.

## Step 6 — Evaluate survivors

Score using three levels only: `✓` / `~` / `✗`. **Never numeric scores.**

Rubric rows:
- Hits success criteria
- Each `SHOULD` constraint
- Reversibility (one-way cost)
- Implementation cost (S / M / L)

After the table: **one paragraph per branch** explaining the trade-off in the user's own language.

## Step 7 — Recommend

Format:

```markdown
## Recommendation: Branch [X]

**Why this one:** [2–4 sentences tying to success criteria + constraints]

**What you're giving up:**
- [concrete thing]
- [concrete thing]

**When you'd revisit this decision:**
- [specific measurable trigger]
- [specific measurable trigger]

**Rejected alternatives (ADR-ready):**
- Branch Y: [one-line reason citing constraint]
- Branch Z: [one-line reason]
```

The "when you'd revisit" section is non-optional — it makes the decision auditable later.

## Step 8 — Save artifact

Save as `SOLUTION-TREE-[slug]-[YYYY-MM-DD].md`. Location: repo root if inside a git repo, else `~/solution-trees/`.

Full artifact structure in [references/artifact-template.md](references/artifact-template.md).

## Step 9 — Recommend next step

| Session outcome | Suggested next activity |
|---|---|
| Approach chosen, need product spec | Formalise into a PRD |
| Approach chosen, API-shape problem | Design the interface (generate alternatives, compare) |
| User wants to pressure-test | Run a grilling session on the recommendation |
| Approach chosen, straightforward | Just build |
| Need to validate before committing | Design experiments (loop back to Discovery D5) |

Handoff format:

> "Approach settled: **[recommendation]**. Suggested next step: [activity]. Don't re-ask: [list]. See `SOLUTION-TREE-[slug]-[date].md`."

---

## Rules (both modes)

- **One question at a time.** Never batch.
- **Never silently drop a branch.** Every pruned option is logged with its killer.
- **Never use numeric scores** in Decision mode. Three levels only: `✓` / `~` / `✗`.
- **Never auto-invoke the next step.** Suggest, don't chain.
- **Never proceed with zero constraints** (Decision mode) or zero outcome (Discovery mode).
- **Never exceed 3 axes.** 8 leaves is already a lot.
- **Never go deeper than 2 tree levels** in Decision mode.
- **Never privilege the user's original solution.** It competes equally.
- **Opportunities are not features.** Frame from customer's perspective (Discovery mode).
- **At least 3 solutions per opportunity** before choosing (Discovery mode).

---

## Examples

- Decision mode: [references/example-transactional-email.md](references/example-transactional-email.md)
- Discovery mode: [references/example-retention-ost.md](references/example-retention-ost.md)
