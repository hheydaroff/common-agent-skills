---
name: grill-me
description: Stress-test a plan or design through relentless interviewing until reaching shared understanding. Use when user wants to be grilled on their plan, stress-test a design, poke holes in an idea, or says "grill me", "challenge my plan", "what am I missing".
---

# Grill Me

Interview the user relentlessly about every aspect of their plan until reaching shared understanding. Walk down each branch of the decision tree, resolving dependencies between decisions one-by-one.

## Rules

- Ask questions **one at a time** — never batch
- For each question, **provide your recommended answer** so the user can agree, disagree, or refine
- If a question can be answered by **exploring the codebase**, do that instead of asking
- Resolve dependency branches in order — don't jump ahead to decisions that depend on unresolved ones
- Be thorough but not adversarial — the goal is shared understanding, not gotchas

## Question Areas

Cover all branches of the decision tree. Typical areas include:

- **Problem clarity**: Is the problem well-defined? Are we solving the right thing?
- **Scope**: What's in? What's explicitly out? Where are the boundaries fuzzy?
- **Users/actors**: Who benefits? Who's affected? Edge-case personas?
- **Architecture**: What components are involved? How do they interact?
- **Data flow**: What goes in, what comes out, what's stored, what's ephemeral?
- **Error handling**: What can go wrong? What's the recovery path?
- **Security**: Who can access what? What's the threat model?
- **Performance**: What are the bottlenecks? What are acceptable latencies?
- **Dependencies**: External services? Libraries? Team coordination?
- **Testing**: How will you know it works? What's hard to test?
- **Migration/rollout**: How do you get from here to there safely?
- **Unknowns**: What don't you know yet? What assumptions are you making?

## Process

1. Read the plan (file, conversation context, or ask user to describe it)
2. If inside a repo, explore relevant code to ground your questions
3. Read existing documentation for domain awareness (see below)
4. Start with the highest-leverage question — the one where a wrong assumption would waste the most effort
5. For each answer, probe deeper if it reveals new branches
6. When a branch is fully resolved, move to the next
7. Summarize resolved decisions periodically so nothing gets lost
8. When all branches are resolved, present a final summary of all decisions made

## Domain Awareness

During codebase exploration, look for existing documentation:

- `CONTEXT.md` (or `CONTEXT-MAP.md` + per-context `CONTEXT.md` files)
- `docs/adr/` (Architecture Decision Records)

If these exist, read them. They inform your questions and provide terminology to challenge against. If they don't exist, proceed silently — don't flag their absence.

### Challenge Against the Glossary

When the user uses a term that conflicts with existing language in `CONTEXT.md`, call it out immediately:
> "Your glossary defines 'cancellation' as X, but you seem to mean Y — which is it?"

### Sharpen Fuzzy Language

When the user uses vague or overloaded terms, propose a precise canonical term:
> "You're saying 'account' — do you mean the Customer or the User? Those are different things."

### Discuss Concrete Scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about boundaries between concepts.

### Cross-Reference with Code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it:
> "Your code cancels entire Orders, but you just said partial cancellation is possible — which is right?"

## Inline Documentation Updates

As decisions crystallize during the session, update documentation immediately — don't batch.

### Update CONTEXT.md

When a term is resolved, add or update it in `CONTEXT.md` right there. Create the file lazily if it doesn't exist. Format:

```markdown
# [Context Name]

[One or two sentence description of what this context is.]

## Language

**[Term]**:
[Concise definition — one sentence max. What it IS, not what it does.]
_Avoid_: [aliases that should not be used]

## Relationships

- An **Order** produces one or more **Invoices**

## Example Dialogue

> **Dev:** "When a **Customer** places an **Order**..."

## Flagged Ambiguities

- "[term]" was used to mean both X and Y — resolved: [resolution]
```

Rules for CONTEXT.md:
- Be opinionated — pick one canonical term, list others as aliases to avoid
- Keep definitions tight — one sentence max
- Only include terms meaningful to domain experts (not generic programming concepts)
- Show relationships with bold term names and cardinality
- Include an example dialogue showing terms used precisely

### Offer ADRs Sparingly

Only offer to create an ADR when **all three** are true:

1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without context** — a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. ADRs live in `docs/adr/` with sequential numbering (`0001-slug.md`). Create the directory lazily.

ADR format — keep it minimal:
```markdown
# [Short title of the decision]

[1-3 sentences: what's the context, what did we decide, and why.]
```

What qualifies for an ADR:
- Architectural shape decisions
- Integration patterns between contexts
- Technology choices that carry lock-in
- Boundary and scope decisions
- Deliberate deviations from the obvious path
- Constraints not visible in the code
- Rejected alternatives when the rejection is non-obvious

## Multi-Context Repos

If `CONTEXT-MAP.md` exists at the root, the repo has multiple contexts:

```markdown
# Context Map

## Contexts
- [Ordering](./src/ordering/CONTEXT.md) — receives and tracks customer orders
- [Billing](./src/billing/CONTEXT.md) — generates invoices and processes payments

## Relationships
- **Ordering → Billing**: Ordering emits `OrderPlaced` events; Billing consumes them
```

Infer which context the current topic relates to. If unclear, ask.

## Output

After the grill session, offer to save a **Decision Log**:

```markdown
# Decision Log: [Plan Name]

**Date:** [YYYY-MM-DD]

## Resolved Decisions

1. **[Decision area]**: [What was decided and why]
2. **[Decision area]**: [What was decided and why]
...

## Open Questions

- [Anything still unresolved]

## Assumptions

- [Key assumptions the plan depends on]

## Documentation Updated

- CONTEXT.md: [terms added/updated]
- ADRs created: [list if any]
```
