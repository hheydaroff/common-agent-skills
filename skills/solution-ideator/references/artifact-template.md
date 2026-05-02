# Artifact Template

Saved as `SOLUTION-TREE-[slug]-[YYYY-MM-DD].md` at repo root (or `~/solution-trees/` outside a repo).

```markdown
# Solution Tree: [Problem Statement]

**Date:** YYYY-MM-DD
**Input type:** problem | solution | ambiguous | multi-problem
**Mode:** full-ideation | solution-evaluation
**Decision reversibility:** one-way | two-way

## Problem / Solution Statement

[Verbatim from user input, trimmed for readability.]

## Underlying Problem (if input was a solution)

[The problem the skill extracted and the user confirmed. Skip this
section if input was a problem, or flag a warning if user skipped
problem validation in solution-evaluation mode.]

## Constraints

### MUST (hard — pruning triggers)
- [constraint 1]
- [constraint 2]

### SHOULD (soft — scoring penalties)
- [constraint 1]
- [constraint 2]

### Success Criteria
- [what "solved" looks like in 6 months, from the user]

### Assumptions (flagged)
- [any constraint the user declined to specify; flagged `⚠️ assumed`]

## Axes

1. **[Axis 1]** — [one-line justification]
2. **[Axis 2]** — [one-line justification]
3. **[Axis 3]** — [one-line justification, if present]

## Branches

### Surviving

- **Branch A: [name]** — [approach at level 1]
  - A1: [concrete implementation variant at level 2]
- **Branch B: [name]**
  - B1: [concrete implementation variant]

### Pruned

- **Branch C: [name]** — ❌ violates `MUST: [constraint]`
- **Branch D: [name]** — ❌ violates `MUST: [constraint]`

### Borderline (survived with penalty)

- **Branch E: [name]** — ⚠ violates `SHOULD: [constraint]`

## Evaluation

|                              | Branch A | Branch B | Branch E |
|------------------------------|----------|----------|----------|
| Hits success criteria        | ✓        | ✓        | ~        |
| SHOULD: [constraint]         | ✓        | ✗        | ~        |
| SHOULD: [constraint]         | ✓        | ✓        | ~        |
| Reversibility                | ~ hard   | ✗ v.hard | ✓ easy   |
| Implementation cost          | M        | L        | S        |

### Per-branch narrative

**Branch A** — [one paragraph explaining the trade-off in the user's
own language. What it gives. What it costs. Why it does or doesn't
fit the specific situation.]

**Branch B** — [one paragraph]

**Branch E** — [one paragraph]

## Recommendation: Branch [X]

**Why this one:**
[2–4 sentences tying directly to the user's success criteria and
constraints. No generic pros.]

**What you're giving up:**
- [concrete thing]
- [concrete thing]

**When you'd revisit this decision:**
- [specific measurable trigger]
- [specific measurable trigger]

## Rejected Alternatives (ADR-ready)

- **Branch [Y]:** [one-line reason citing specific constraint]
- **Branch [Z]:** [one-line reason]
- **Branch [pruned]:** violates `MUST: [constraint]`

## Next Step

**Recommended next activity:** formalise into a PRD/spec | design the interface (generate alternatives) | pressure-test via grilling | none

**Why:** [one sentence]

**Carry forward (don't re-ask):**
- Success criteria: [...]
- MUST constraints: [...]
- Chosen approach: [Branch X]
- Rejected approaches and reasons: see above
```
