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
3. Start with the highest-leverage question — the one where a wrong assumption would waste the most effort
4. For each answer, probe deeper if it reveals new branches
5. When a branch is fully resolved, move to the next
6. Summarize resolved decisions periodically so nothing gets lost
7. When all branches are resolved, present a final summary of all decisions made

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
```
