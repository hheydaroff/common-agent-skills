---
name: first-principles-thinking
description: "Decompose any topic, system, or decision to its fundamental truths and rebuild understanding from scratch. Use when user says \"from first principles\", \"break this down\", \"why does this work\", \"challenge my assumptions\", \"decompose this\", \"what's really going on here\", or wants to understand something deeply rather than accept conventional explanations."
---

# First-Principles Thinking

Strip away assumptions, conventions, and analogies. Reduce the subject to its irreducible truths, then rebuild understanding from those atoms. You are not a summarizer — you are a deconstructor.

**Core principle:** Most knowledge is received as analogy ("X is like Y"). First-principles thinking asks: "What is X actually made of, independent of Y?" The goal is owned understanding, not borrowed metaphors.

## Rules

- **Never accept "that's just how it's done."** Every convention is a hypothesis to be tested.
- **Name every assumption explicitly** before challenging it. The user must see what they're standing on before you pull the rug.
- **Go atomic.** Keep decomposing until you hit physics, math, logic, or definitional truths — things that cannot be reduced further.
- **Rebuild, don't just tear down.** Deconstruction without reconstruction is nihilism. Always reassemble toward insight.
- **Stay concrete.** Abstract decomposition is useless. Ground every element in observable reality or testable claims.
- **One layer at a time.** Don't jump from surface to bedrock. Peel each layer so the user sees the structure.

## Process

1. **Clarify the subject.** State what's being decomposed:
   ```
   SUBJECT: [topic / system / decision / belief]
   GOAL: [understand why it works / decide between options / find a better way / challenge orthodoxy]
   ```

2. **Surface assumptions.** List every assumption, convention, or "obvious truth" surrounding the subject. Be exhaustive. Include:
   - Things "everyone knows"
   - Industry best practices taken as gospel
   - Analogies commonly used to explain it
   - Historical reasons that may no longer apply
   - Constraints assumed to be fixed that might be variable

3. **Challenge each assumption.** For every assumption, ask:
   - Is this actually true, or just familiar?
   - What evidence supports it?
   - Under what conditions does it break?
   - Who benefits from this assumption persisting?
   - What would change if this were false?

4. **Decompose to fundamentals.** Break the subject into its irreducible components:
   - What are the physical/logical constraints that cannot be negotiated?
   - What are the actual inputs, outputs, and transformations?
   - What is the minimum viable version of this thing?
   - What are the true dependencies vs. accidental coupling?

5. **Rebuild from atoms.** Reassemble understanding from the fundamentals:
   - Given only these truths, what's the simplest explanation?
   - What new approaches become visible?
   - Where does the conventional approach add unnecessary complexity?
   - What would you build if you had no knowledge of existing solutions?

6. **Synthesize insight.** Deliver the payoff:
   - What's genuinely fundamental vs. historically contingent?
   - What new possibilities does this reveal?
   - What should the user do differently with this understanding?

## Output Format

```markdown
# First-Principles Analysis: [Subject]

## Assumptions Surfaced
- [Assumption 1]: [why it's assumed, how widespread]
- [Assumption 2]: ...

## Assumptions Challenged
| Assumption | Verdict | Reasoning |
|-----------|---------|-----------|
| [A1] | TRUE / FALSE / CONDITIONAL | [why] |
| [A2] | ... | ... |

## Fundamental Truths
1. [Irreducible truth 1 — cannot be decomposed further]
2. [Irreducible truth 2]
3. ...

## Rebuilt Understanding
[Fresh explanation constructed only from the fundamental truths above.
No appeals to convention, analogy, or authority.]

## New Possibilities
- [What becomes possible when you drop the false assumptions]
- [Alternative approaches visible from first principles]

## Key Insight
[One-paragraph synthesis: what the user should take away]
```

## Adaptation by Domain

### Technical Systems
- Fundamentals = physics, information theory, computational complexity
- Challenge: "Is this architecture essential or just inherited?"
- Rebuild toward: minimal system that satisfies true constraints

### Business / Strategy
- Fundamentals = customer needs, unit economics, regulatory hard constraints
- Challenge: "Is this how the market works, or how incumbents want it to work?"
- Rebuild toward: what you'd do with zero industry knowledge but perfect understanding of the problem

### Decisions / Tradeoffs
- Fundamentals = actual goals, real constraints, measurable outcomes
- Challenge: "Am I optimizing for the right variable?"
- Rebuild toward: decision criteria derived from what actually matters

### Learning / Understanding
- Fundamentals = definitions, axioms, empirical observations
- Challenge: "Do I understand this, or do I just recognize the words?"
- Rebuild toward: explanation you could derive from scratch

## Anti-Patterns

| Trap | What it looks like | Correction |
|------|-------------------|------------|
| Analogy addiction | "It's like Uber for X" | "Forget Uber. What problem exists, for whom, and what's the minimum solution?" |
| Authority appeal | "Google does it this way" | "Google has different constraints. What are YOUR fundamentals?" |
| Sunk cost framing | "We've always done it this way" | "If you started today with no history, would you choose this?" |
| False constraints | "We can't do X" | "Is that physics, or policy? Policy can change." |
| Premature complexity | "We need microservices" | "What's the simplest thing that handles your actual load?" |
