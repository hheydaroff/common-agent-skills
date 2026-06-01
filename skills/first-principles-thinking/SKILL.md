---
name: first-principles-thinking
description: "Decompose any topic, system, or decision to its fundamental truths and rebuild understanding from scratch. Use when user says \"from first principles\", \"break this down\", \"why does this work\", \"challenge my assumptions\", \"decompose this\", \"what's really going on here\", or wants to understand something deeply rather than accept conventional explanations."
---

# First-Principles Thinking

Strip away assumptions, conventions, and analogies. Reduce the subject to its irreducible truths, then rebuild understanding from those atoms.

**Core distinction:** Most reasoning is by *analogy* ("X is like Y, so do what Y did"). First-principles reasoning asks: "What is actually true here, independent of what others have done?" The goal is *owned* understanding — not borrowed conclusions.

## Reference Files

| File | When to load |
|------|--------------|
| [techniques.md](references/techniques.md) | Always load — contains Socratic Questioning, Five Whys, Constraint Mapping, and Inversion methods |

## Rules

- **Never accept "that's just how it's done."** Every convention is a hypothesis to test.
- **Name every assumption explicitly** before challenging it.
- **Calibrate depth.** 1-2 levels deeper is often enough. Atomic decomposition only for breakthrough problems.
- **Rebuild, don't just tear down.** Deconstruction without reconstruction is useless.
- **Stay concrete.** Ground every element in observable reality or testable claims.
- **Be interactive.** Ask probing questions — don't monologue. The user's reasoning is the material.

## Process

### Step 1: Frame the Subject

```
SUBJECT: [topic / system / decision / belief]
GOAL: [understand / decide / innovate / challenge]
DEPTH: [surface (1-2 levels) | deep (to fundamentals) | atomic (irreducible truths)]
```

Framing determines the solution space. Spend time here. If unclear, use Socratic clarification questions.

### Step 2: Map Existing Reasoning

Before challenging anything, make current thinking visible:
- What does the user (or convention) currently believe?
- What analogies are in use? ("It's like Uber for X")
- What precedents are being relied on? ("Google does it this way")
- What is assumed to be fixed that might be variable?

### Step 3: Decompose

Choose technique based on the situation (see references/techniques.md):
- **Unclear thinking** → Socratic Questioning
- **Symptoms masking root cause** → Five Whys
- **"It can't be done" beliefs** → Constraint Mapping
- **Stuck on forward reasoning** → Inversion
- **Complex systems** → Combine all

For each layer, ask: Is this true or just familiar? What evidence? When does it break?

### Step 4: Identify Fundamentals

What remains after assumptions are stripped:
- Physical/mathematical constraints that cannot be violated
- Definitional truths (what the thing *is*, not how it's currently done)
- Empirically verified facts (with sources)
- True dependencies vs. accidental coupling

### Step 5: Rebuild from Fundamentals

Given *only* the first principles:
- What's the simplest explanation/solution?
- What would you build with zero knowledge of existing approaches?
- Where does convention add unnecessary complexity?
- What new possibilities become visible?

### Step 6: Synthesize Insight

Connect decomposition back to action. What shifts the frame?

## Output Format

```markdown
# First-Principles Analysis: [Subject]

## Current Reasoning (as-is)
[How it's currently understood — including analogies and precedents relied on]

## Assumptions Surfaced
1. [Assumption]: [evidence for/against] → **TRUE / FALSE / CONDITIONAL**
2. ...

## Fundamental Truths
1. [Irreducible truth — survives all decomposition]
2. ...

## Rebuilt Understanding
[Fresh explanation/solution from fundamentals ONLY. No convention or authority.]

## New Possibilities
- [What opens up when false assumptions drop]

## Key Insight
[One paragraph — the frame shift]
```

## Depth Calibration

| Situation | Depth | Example |
|-----------|-------|---------|
| Routine decision | 1 level deeper | "Why weekly meetings?" |
| Design choice | 2-3 levels + constraints | "Why REST?" |
| Strategy / major bet | Full decomposition | "What business are we in?" |
| Paradigm challenge | Atomic | "Why do batteries cost what they cost?" |

## When NOT to Use This

- **Analogy is genuinely valid** — building a CRUD app doesn't need HTTP decomposed
- **Time pressure dominates** — use heuristics now, decompose later
- **Domain is well-understood** and not being challenged
- **Trivial stakes** — don't go atomic on lunch decisions

## Domain Adaptation

- **Technical:** Fundamentals = physics, info theory, complexity. "Is this architecture essential or inherited?"
- **Business:** Fundamentals = customer needs, unit economics, hard regulations. "How the market works vs. how incumbents want it to work?"
- **Decisions:** Fundamentals = actual goals, real constraints, measurable outcomes. "Am I optimizing the right variable?"
- **Learning:** Fundamentals = definitions, axioms, observations. "Can I derive this, or just recognize the words?"

## Anti-Patterns

| Trap | Correction |
|------|------------|
| "It's like Uber for X" | "Forget Uber. What problem, for whom?" |
| "Google does it this way" | "Google has different constraints. What are yours?" |
| "We've always done it this way" | "If you started today, would you?" |
| "We can't do X" | "Physics, or policy?" |
| Going atomic on trivial questions | "Is this actually high-stakes?" |
| Tearing down without rebuilding | "Given these truths, what DO we build?" |
