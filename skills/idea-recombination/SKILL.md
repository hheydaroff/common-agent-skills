---
name: idea-recombination
description: "Generate novel ideas by creatively recombining existing frameworks, patterns, or ideas. Use when user wants to find a new idea at the intersection of old ones, or when solution-ideator Discovery/Decision modes produce uninspired results. Triggers: 'combine these ideas', 'what emerges from X + Y', 'novel recombination', 'creative synthesis', 'invert this framework'."
---

# Idea Recombination

Innovation often comes not from inventing something new, but from combining two old ideas in a way neither individually suggests. This skill is a structured creative technique: take N existing frameworks, map them onto orthogonal axes, invert arrows, and find the novel idea at the intersection.

---

## When to use this skill

| Situation | Action |
|---|---|
| 2+ frameworks/patterns/ideas exist, user wants something new from them | Run the full process |
| Solution-ideator Discovery produced "meh" solutions | Feed the top opportunities + frameworks here |
| Solution-ideator Decision survivors all feel incremental | Run recombination on the losing branches + constraints |
| "What if we inverted X?" / "What's the opposite of this pattern?" | Fast-path: skip to Step 3 (inversion), use the single framework |
| User has a single framework and wants to break out of its assumptions | Fast-path: Step 3 inversion only, generate anti-framework |

**Decline conditions:**

| Situation | Redirect |
|---|---|
| Only one idea, no framework to combine with | Solution-ideator Discovery mode first — generate more ideas |
| Problem is purely technical (API design, module split) | Interface-design exploration |
| User wants validation, not generation | Grill-me or writing-review |
| User already has a clear novel idea and wants to build it | Skip to spec / just build |

---

## Step 1 — Gather the ingredients

Ask:

> "What are the 2-4 existing ideas, frameworks, or patterns you want to recombine? Give me the name and the core insight of each."

For each ingredient, extract:
- **Name** — what it's called
- **Core insight** — the one-sentence thesis
- **Arrow** — what direction does the causality flow? (e.g., SDD: spec → code, Memory Architecture: store → update → retrieve, Harness-First: human writes for agent reader)

If the user is coming from solution-ideator, pull the frameworks + patterns from the Discovery/Decision artifact.

**Minimum: 2 ingredients. Maximum: 4.** More than 4 creates combinatorial explosion without more insight.

---

## Step 2 — Map onto orthogonal axes

Pick 2-3 axes that span the recombination space. Same rules as Decision mode:
- Orthogonal — moving along one doesn't force a move along another
- Decision-relevant — different positions produce genuinely different ideas
- Both ends viable

Present the axes and ask the user to confirm or adjust:

```
Axis 1: [dimension]        Left ◄────────────────────► Right
Axis 2: [dimension]        Left ◄────────────────────► Right
Axis 3: [dimension]        Left ◄────────────────────► Right
```

**Hard cap: 3 axes.**

---

## Step 3 — Invert

This is the creative engine. For each ingredient, ask: **what happens if we invert its arrow?**

| Ingredient | Original arrow | Inverted arrow |
|---|---|---|
| SDD | spec → code | code → spec (behavior discovers intent) |
| Memory Architecture | store → retrieve | forget → re-derive (what's cheaper to lose?) |
| Harness-First | human writes for agent | agent writes for human (agent-readable → human-readable) |

Rules:
- Invert at least one ingredient. More inversions = more novelty, but also more risk of nonsense.
- If an inversion produces an obviously absurd idea, keep it — absurd ideas are often adjacent to breakthroughs.
- Don't skip inversion. It's the step that separates recombination from mere combination.

---

## Step 4 — Find the intersection

For each axis combination (max 8 cells), generate one idea. The idea must:
- **Not be obvious from any single ingredient alone** — it must require the combination
- **Incorporate at least one inversion** from Step 3
- **Be concretely describable** — not "a platform for X," but "a thing that does Y when Z happens"

Present as a grid or list. Mark which ideas are:
- ⭐ **Novel** — genuinely new, neither ingredient suggests it alone
- 🔄 **Incremental** — useful but predictable from the combination
- 🤪 **Weird** — possibly nonsense, possibly breakthrough

The "weird" ones are often the most valuable. Don't filter them out.

---

## Step 5 — Select the winner

Score using three levels: `✓` / `~` / `✗`.

| Criterion | Weight |
|---|---|
| Novelty — neither ingredient alone suggests this | `MUST` |
| Coherence — the idea holds together, not just wordplay | `MUST` |
| Actionability — could build a prototype in 2 weeks | `SHOULD` |
| Surprise — makes you go "huh, that's interesting" | `SHOULD` |

Recommend the top idea with:
- **Why it's novel** — what specific inversion + combination creates the new thing
- **What it gives up** — every inversion sacrifices something the original framework provided
- **Smallest prototype** — the 2-week experiment to validate it's not just wordplay

---

## Step 6 — Save artifact

Save as `docs/planning_recombination-[slug]-[YYYY-MM-DD].md` in the repo's `docs/` folder. If not in a git repo, fall back to the current working directory.

Artifact structure:

```markdown
---
type: recombination
ingredients: [list]
date: YYYY-MM-DD
---

# Idea Recombination: [title]

## Ingredients
[one-paragraph each: name, core insight, arrow]

## Axes
[the 2-3 axes with left/right poles]

## Inversions
[per-ingredient: original → inverted]

## Generated Ideas
[grid or list, with novelty/weird tags]

## Winner
[recommendation with why, what's given up, smallest prototype]

## Rejected
[one-line per rejected idea with reason]
```

---

## Step 7 — Recommend next step

| Outcome | Next step |
|---|---|
| Novel idea found, coherent, actionable | Write a spec / PRD |
| Novel idea found, but coherence is shaky | Run solution-ideator Decision mode on it |
| Idea is interesting but needs more ingredients | Run again with different frameworks |
| Nothing novel emerged | The ingredients may be too similar — try with more distant domains |
| Weird idea that might be breakthrough | Build the 2-week prototype, don't spec it first |

---

## Rules

- **Never skip inversion.** It's the step that separates recombination from mere combination.
- **Never reject "weird" ideas.** The absurd ones are often adjacent to breakthroughs.
- **Never exceed 4 ingredients or 3 axes.** Combinatorial explosion produces noise, not insight.
- **Never let an idea survive that's obvious from a single ingredient.** The whole point is the intersection.
- **Minimum 2 ingredients.** One ingredient is just "invert this" — that's the fast-path, not recombination.
- **Output must be concrete.** "A platform for X" is not a recombination, it's a vibe.

---

## Fast-path: Single-framework inversion

If the user has only one framework and wants to break its assumptions:

1. State the framework's core arrow
2. Invert it — what's the anti-framework?
3. Ask: "What would have to be true for the anti-framework to be correct?"
4. The answer is the novel idea

Example:
- Framework: "Specs should be written before code" (SDD)
- Inversion: "Code should be written before specs"
- Question: "What would have to be true for code-first to be correct?"
- Answer: "The spec is discovered, not declared — behavior is the source of truth, the spec is a lagging indicator"

This fast-path is also useful as a warm-up before full recombination.

---

## Examples

_Coming soon — see solution-ideator references for the pattern._

---

## Relationship to solution-ideator

| solution-ideator mode | How idea-recombination fits |
|---|---|
| **Discovery** | Run after OST produces solutions. Feed the frameworks + patterns into recombination to find hybrids the OST didn't suggest. |
| **Decision** | Run after pruning. Feed the losing branches + constraints — sometimes the best idea is a recombination of two "rejected" approaches. |

Idea-recombination can also be called standalone — it doesn't require solution-ideator. But they compose well: OST discovers what's worth solving, Decision picks how, Recombination finds the novel third option neither mode produced.