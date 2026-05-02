---
name: prd-to-spec
description: Convert PRD.md into structured SPEC.md with atomic development tasks. Use when user has a PRD and says "convert to spec", "create spec from PRD", "PRD to tasks", "prepare for Ralph Loop", or wants a development-ready task breakdown with user stories, acceptance criteria, and INVEST-compliant atomic tasks.
---

# PRD to SPEC Conversion

Convert comprehensive PRD into structured SPEC.md with atomic, testable development tasks using vertical-slice decomposition.

## Process (7 Steps)

### 1. Read PRD

Read `PRD.md` (or user-specified file). Extract:
- Project name and objective
- Target user/persona
- All features and requirements
- Tech stack and constraints
- Success criteria
- Out of scope items

If PRD is missing critical info, ask user ONE clarifying question at a time.

### 2. Explore Codebase (if applicable)

If inside an existing repo, explore it to understand:
- Current architecture and layers (schema, API, services, UI)
- Existing patterns and conventions
- Test infrastructure and prior art

This grounds the decomposition in reality rather than abstract planning.

### 3. Write User Story

Convert primary requirement into user-centric story:

```
As a [user type/persona]
I want [specific action/capability]
So that [business value/outcome]
```

Answer these:
- WHO is using this? (customer, admin, guest, API consumer)
- WHAT are they trying to do? (specific action)
- WHY do they want this? (business value)

### 4. Define Acceptance Criteria

Write testable conditions using Given-When-Then format:

| # | Given (precondition) | When (action) | Then (outcome) |
|---|----------------------|---------------|----------------|
| AC1 | I'm on login page | I enter valid credentials | I see dashboard |
| AC2 | I'm on login page | I enter invalid password | I see error message |

**Checklist:**
- [ ] Each AC is independent (testable alone)
- [ ] Each AC has clear pass/fail condition
- [ ] No vague words ("should", "maybe", "nice to have")
- [ ] All edge cases covered (errors, timeouts, boundaries)

### 5. Identify Technical Components

List affected systems:

```
Frontend:
- [UI components, forms, displays]

Backend:
- [API endpoints, services, middleware]

Database:
- [Tables, schemas, migrations]

Infrastructure:
- [HTTPS, CORS, caching, external services]
```

### 6. Decompose into Vertical Slices

Break the work into **tracer-bullet vertical slices**. Each slice is a thin end-to-end path that cuts through ALL integration layers (schema → API → UI → tests), NOT a horizontal slice of one layer.

**Vertical slice rules:**
- Each slice delivers a narrow but COMPLETE path through every layer
- A completed slice is demoable or verifiable on its own
- Prefer many thin slices over few thick ones
- Each slice should map to one or more acceptance criteria

**Classify each slice:**
- **AFK** — Can be implemented and merged without human interaction (prefer this)
- **HITL** — Requires human input: architectural decision, design review, external approval

**Supplementary decomposition methods** (use within slices if helpful):

- **Workflow Steps**: Sequential user actions (navigate → enter data → submit → validate → respond)
- **CRUD**: Data operations (Create, Read, Update, Delete)
- **Business Rules**: Scenarios (happy path, error path, security path, edge path)
- **Platform**: Different contexts (desktop, mobile, API)

### 7. Quiz the User

**Before finalizing**, present the proposed breakdown as a numbered list. For each slice show:

- **Title**: Short descriptive name
- **Type**: HITL / AFK
- **Blocked by**: Which other slices must complete first
- **User stories covered**: Which acceptance criteria this addresses

Ask the user:
- "Does the granularity feel right? (too coarse / too fine)"
- "Are the dependency relationships correct?"
- "Should any slices be merged or split further?"
- "Are the correct slices marked as HITL and AFK?"

**Iterate until the user approves the breakdown.** Only then proceed to write SPEC.md.

### 8. Create Atomic Tasks

From the approved slices, create tasks that satisfy **INVEST**:
- **I**ndependent - completable without waiting for others
- **N**egotiable - can discuss and adjust scope
- **V**aluable - delivers business value
- **E**stimable - team can estimate effort
- **S**mall - 4-8 hours (1-2 days max)
- **T**estable - clear pass/fail criteria

**Task format:**

```
### TASK N: [Action Verb] [Component]

**Description:** [What to build — end-to-end behavior, not layer-by-layer]

**Type:** AFK | HITL

**Satisfies:** AC1, AC2

**Test Cases:**
- ✓ Happy: [normal expected behavior]
- ✓ Error: [what if X fails?]
- ✓ Edge: [boundary conditions]

**Dependencies:** [Task #s that must complete first, or "None"]

**Estimate:** [4-8 hours]
```

## Output: SPEC.md

Write to `SPEC.md` in the project root (or next to the PRD file if it lives elsewhere):

```markdown
# Feature Spec: [Feature Name]

> **Source:** [PRD filename] | **Created:** [YYYY-MM-DD]

## User Story

As a [persona]
I want [action]
So that [value]

## Acceptance Criteria

| # | Given | When | Then |
|---|-------|------|------|
| AC1 | [precondition] | [action] | [outcome] |
| AC2 | [precondition] | [action] | [outcome] |

## Technical Components

**Frontend:** [list]
**Backend:** [list]
**Database:** [list]
**Infrastructure:** [list]

## Vertical Slices

Summary of the approved slice breakdown with dependency relationships.

## Atomic Tasks

### TASK 1: [Action Verb] [Component]
**Description:** [specific end-to-end behavior]
**Type:** AFK
**Satisfies:** AC1
**Test Cases:**
- ✓ Happy: [scenario]
- ✓ Error: [scenario]
- ✓ Edge: [scenario]
**Dependencies:** None
**Estimate:** [hours]

### TASK 2: [Action Verb] [Component]
...

## Dependency Chain

```
PHASE 1 (Parallel):
├─ TASK 1: [name] (AFK)
├─ TASK 2: [name] (AFK)
└─ TASK 3: [name] (HITL)

PHASE 2 (Depends on Phase 1):
├─ TASK 4: [name] (AFK, needs 1, 2)
└─ TASK 5: [name] (AFK, needs 1)

PHASE 3 (Sequential):
└─ TASK 6: [name] (AFK, needs 4, 5)
```

## Out of Scope

[From PRD or clarified with user]

## Completion Promise

When ALL acceptance criteria pass: `<promise>COMPLETE</promise>`
```

## Optional: GitHub Issue Output

If the user requests GitHub issues in addition to (or instead of) SPEC.md:

Create issues in dependency order (blockers first) so you can reference real issue numbers:

```bash
gh issue create --title "TASK N: [Title]" --body "## What to build
[End-to-end behavior description]

## Type
AFK | HITL

## Acceptance criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Blocked by
- #<issue-number> (or 'None - can start immediately')

## Test cases
- ✓ Happy: [scenario]
- ✓ Error: [scenario]
- ✓ Edge: [scenario]"
```

Do NOT close or modify any parent issue.

## Post-Creation

Tell user:
> "SPEC.md created. Review the tasks and acceptance criteria. When approved, convert the SPEC into whatever machine-readable task format your execution pipeline uses (e.g., a `tasks.json` for a task-runner loop)."

## Tips

**DO:**
- Decompose as vertical slices first, then refine within slices
- Classify every task as AFK or HITL
- Quiz the user on the breakdown BEFORE writing SPEC.md
- Write ACs with specific, measurable outcomes ("returns 401 status")
- Keep tasks 4-8 hours max
- List all dependencies upfront
- Include happy path AND error cases
- Group related tasks in same phase
- Describe end-to-end behavior, not layer-by-layer implementation

**DON'T:**
- Create horizontal tasks ("build all API endpoints", "style all pages")
- Mix frontend + backend in one task
- Create tasks > 8 hours (break down further)
- Write vague ACs ("user should see something")
- Forget security, accessibility, error handling
- Create 100% sequential dependencies (parallelize where possible)
- Skip the user quiz step — always validate before finalizing
