---
name: prd-to-spec
description: Convert PRD.md into structured SPEC.md with atomic development tasks. Use when user has a PRD and says "convert to spec", "create spec from PRD", "PRD to tasks", "prepare for Ralph Loop", or wants a development-ready task breakdown with user stories, acceptance criteria, and INVEST-compliant atomic tasks.
---

# PRD to SPEC Conversion

Convert comprehensive PRD into structured SPEC.md with atomic, testable development tasks.

## Process (6 Steps)

### 1. Read PRD

Read `PRD.md` (or user-specified file). Extract:
- Project name and objective
- Target user/persona
- All features and requirements
- Tech stack and constraints
- Success criteria
- Out of scope items

If PRD is missing critical info, ask user ONE clarifying question at a time.

### 2. Write User Story

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

### 3. Define Acceptance Criteria

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

### 4. Identify Technical Components

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

### 5. Decompose into Workflows

Choose ONE decomposition method:

**Method A: Workflow Steps** (Sequential actions)
```
1. User navigates to page
2. User enters data
3. User submits form
4. System validates
5. System processes
6. System responds
```

**Method B: CRUD** (Data operations)
```
Create: User creates new [entity]
Read: System retrieves [entity]
Update: User modifies [entity]
Delete: User removes [entity]
```

**Method C: Business Rules** (Scenarios)
```
Happy Path: Valid input → Success
Error Path: Invalid input → Error message
Security Path: Rate limit exceeded → Lockout
Edge Path: Timeout → Graceful degradation
```

**Method D: Platform** (Different contexts)
```
Desktop: Full form with all fields
Mobile: Responsive simplified form
API: Programmatic access
```

### 6. Create Atomic Tasks

Each task must satisfy **INVEST**:
- **I**ndependent - completable without waiting for others
- **N**egotiable - can discuss and adjust scope
- **V**aluable - delivers business value
- **E**stimable - team can estimate effort
- **S**mall - 4-8 hours (1-2 days max)
- **T**estable - clear pass/fail criteria

See [references/task-template.md](references/task-template.md) for detailed template and examples.

**Task format:**

```
### TASK N: [Action Verb] [Component]

**Description:** [What to build - specific]

**Satisfies:** AC1, AC2

**Test Cases:**
- ✓ Happy: [normal expected behavior]
- ✓ Error: [what if X fails?]
- ✓ Edge: [boundary conditions]

**Dependencies:** [Task #s that must complete first, or "None"]

**Estimate:** [4-8 hours]
```

## Output: SPEC.md

Write to `scripts/ralph/SPEC.md` (create directories if needed):

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

## Decomposition ([Method Used])

[Breakdown using chosen method]

## Atomic Tasks

### TASK 1: [Action Verb] [Component]
**Description:** [specific]
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
├─ TASK 1: [name]
├─ TASK 2: [name]
└─ TASK 3: [name]

PHASE 2 (Depends on Phase 1):
├─ TASK 4: [name] (needs 1, 2)
└─ TASK 5: [name] (needs 1)

PHASE 3 (Sequential):
└─ TASK 6: [name] (needs 4, 5)
```

## Out of Scope

[From PRD or clarified with user]

## Completion Promise

When ALL acceptance criteria pass: `<promise>COMPLETE</promise>`
```

## Post-Creation

Tell user:
> "SPEC.md created at `scripts/ralph/SPEC.md`. Review the tasks and acceptance criteria. When approved, run `/spec-to-tasks` to generate machine-readable tasks.json for Ralph Loop execution."

## Tips

**DO:**
- Write ACs with specific, measurable outcomes ("returns 401 status")
- Keep tasks 4-8 hours max
- List all dependencies upfront
- Include happy path AND error cases
- Group related tasks in same phase

**DON'T:**
- Mix frontend + backend in one task
- Create tasks > 8 hours (break down further)
- Write vague ACs ("user should see something")
- Forget security, accessibility, error handling
- Create 100% sequential dependencies (parallelize where possible)
