---
name: request-refactor-plan
description: Create a detailed refactor plan with tiny safe commits via user interview. Use when user wants to plan a refactor, create a refactoring RFC, break a refactor into safe incremental steps, or says "plan a refactor", "refactor plan", "how should I refactor this".
---

# Refactor Plan Creator

Create a thorough, safe refactor plan through developer interview, codebase exploration, and incremental commit planning. Following Martin Fowler's advice: "make each refactoring step as small as possible, so that you can always see the program working."

## Process

Steps may be skipped if unnecessary for the specific case.

### 1. Understand the Problem

Ask the user for a long, detailed description of:
- The problem they want to solve
- Any potential ideas for solutions
- What's painful about the current state

### 2. Explore the Codebase

Explore the repo to:
- Verify the user's assertions about the current state
- Understand the architecture and patterns in play
- Map the blast radius — what code is affected?

### 3. Consider Alternatives

Ask whether they have considered other options. Present alternatives yourself:
- "Have you considered [approach X]? It would [trade-off]."
- "Another option is [approach Y], which avoids [problem] but introduces [cost]."

Ensure the chosen approach is the right one before planning it.

### 4. Interview on Implementation

Be extremely detailed and thorough. Cover:
- Exact scope: what changes, what stays
- Module boundaries: which interfaces change, which are preserved
- Data migration: any schema or data format changes
- Backwards compatibility: can this be rolled out incrementally?
- Error handling: what new failure modes are introduced?

### 5. Hammer Out Scope

Work out the **exact boundary**:
- What you plan to change
- What you plan to **not** change (and why)
- What's deferred to a follow-up

### 6. Assess Test Coverage

Look in the codebase for test coverage of the affected area:
- Are there existing tests? What kind? (unit, integration, e2e)
- Is coverage sufficient to refactor safely?
- If coverage is insufficient, ask: "What are your plans for testing? Should we add tests before refactoring?"

### 7. Plan Tiny Commits

Break the implementation into the **smallest possible commits**. Each commit must:
- Leave the codebase in a **working, passing state**
- Be independently reviewable
- Make exactly one logical change

Think in terms of:
1. Preparatory refactors (make the change easy)
2. The actual change (now that it's easy)
3. Cleanup (remove old code paths, dead code)

### 8. Create the Refactor Plan

Save as a file and/or create a GitHub issue.

**File output:**
```
REFACTOR-[Name]-[YYYY-MM-DD].md
```

**GitHub issue (if requested):**
```bash
gh issue create --title "Refactor: [Title]" --body-file REFACTOR-[Name]-[YYYY-MM-DD].md
```

## Refactor Plan Template

```markdown
# Refactor Plan: [Title]

**Date:** [YYYY-MM-DD]
**Status:** Draft

## Problem Statement

The problem the developer is facing, from the developer's perspective.

## Solution

The proposed solution, from the developer's perspective.

## Commits

A LONG, detailed implementation plan in plain English. Each commit should be the tiniest possible step that leaves the codebase in a working state.

1. **[Commit title]**: [What changes and why. What stays working.]
2. **[Commit title]**: [What changes and why. What stays working.]
3. ...

## Decision Document

Implementation decisions made, including:
- Modules that will be built/modified
- Interfaces that will change
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contract changes
- Specific interactions

Do NOT include specific file paths or code snippets — they go stale fast.

## Testing Decisions

- What makes a good test here (test external behavior, not implementation details)
- Which modules will be tested
- Prior art (similar test patterns already in the codebase)
- Tests to add before refactoring (if coverage is insufficient)

## Out of Scope

What is explicitly NOT part of this refactor.

## Risks

- What could go wrong
- Rollback strategy
- How to detect problems early

## Further Notes

Any additional context or references.
```

## Tips

**DO:**
- Explore the codebase before planning — don't trust descriptions alone
- Make commits absurdly small — if in doubt, split further
- Ensure each commit passes all tests
- Add preparatory tests before refactoring if coverage is thin
- Consider the rollback path for each step

**DON'T:**
- Include file paths or code snippets in the plan (they go stale)
- Plan big-bang commits that change everything at once
- Skip the alternatives discussion — the best refactor might be "don't"
- Assume test coverage is sufficient — verify it
- Mix refactoring with feature work in the same plan
