---
name: spec-to-tasks
description: "Convert approved SPEC.md into tasks.json for Ralph Loop. Use when user says \"convert spec to tasks\", \"generate tasks.json\", or wants machine-executable task format."
---

# SPEC to Tasks Conversion

Convert human-readable SPEC.md into machine-executable tasks.json.

## Prerequisites

SPEC file must exist at `docs/SPEC_*.md` (or user-specified location; also checks `SPEC.md` at the repo root) with:
- `# Feature Spec: [Name]` title
- `## Acceptance Criteria` table (Given/When/Then)
- `## Atomic Tasks` with `### TASK N:` blocks
- `## Dependency Chain` showing phases

If missing, tell user: "SPEC file not found in `docs/`. Generate one first — from a PRD via whatever PRD-to-spec workflow you use, or author it manually."

## Workflow

### 1. Read & Validate SPEC

Read the SPEC from `docs/SPEC_*.md` (or a user-specified file; fall back to `SPEC.md` at the repo root). Verify these sections exist:
- `# Feature Spec:` title
- `## Atomic Tasks` section
- `### TASK` blocks (at least one)

If validation fails, list missing sections and stop.

### 2. Extract Metadata

From the SPEC, extract:
- **Feature slug**: kebab-case from the title (e.g., "User Auth Flow" → `user-auth-flow`)
- **Feature title**: the full title
- **Phase count**: from `## Dependency Chain` or inferred from task phases
- **Acceptance criteria**: from `## Acceptance Criteria` table

### 3. Convert Each Task Block

For each `### TASK N:` block, extract:
- **id**: `TASK-001`, `TASK-002`, etc.
- **phase**: from `**Phase:**` line or dependency chain position
- **category**: from `**Category:**` line (Backend, Frontend, Integration, etc.)
- **type**: from `**Type:**` line — `AFK` (default) or `HITL`
- **title**: the task heading text
- **description**: body text / details
- **satisfies**: which acceptance criteria IDs this task covers
- **testCases**: extract happy path, error, and edge cases if specified
- **dependencies**: from `**Depends on:**` line → array of task IDs
- **verification**: the single runnable **proof-of-work command** for this task (see Proof-of-Work below). From `**Verification:**` line, or infer from category.
- **status**: always `"pending"`

**Every task MUST have a proof-of-work command and MUST be independently usable** — see the two hard rules below. If a task can't satisfy both, it's mis-scoped: split or merge it before writing tasks.json.

### 4. Write tasks.json

Write the complete JSON file to `docs/tasks.json` (create `docs/` if missing; or a user-specified path).

### 5. Report Results

Print a summary table:

```
✅ Created tasks.json: N tasks in M phases

| ID       | Phase | Category | Title                    | Deps |
|----------|-------|----------|--------------------------|------|
| TASK-001 | 1     | Backend  | Create API endpoint      | None |
| TASK-002 | 2     | Frontend | Build form UI            | 001  |
```

### 6. Next Step

Tell user:
> "Created `docs/tasks.json` with N tasks. Ready for autonomous execution (e.g., ralph loop)."

## tasks.json Schema

```json
{
  "meta": {
    "feature": "slug",
    "featureTitle": "Feature Name",
    "source": "SPEC.md",
    "createdAt": "ISO-timestamp",
    "taskCount": 10,
    "phaseCount": 3
  },
  "config": {
    "branchName": "feat/slug",
    "maxRetriesPerTask": 3,
    "completionPromise": "<promise>COMPLETE</promise>"
  },
  "acceptanceCriteria": [
    {"id": "AC1", "given": "...", "when": "...", "then": "..."}
  ],
  "tasks": [
    {
      "id": "TASK-001",
      "phase": 1,
      "category": "Backend",
      "type": "AFK",
      "title": "Task title",
      "description": "Details",
      "satisfies": ["AC1"],
      "testCases": {"happy": "...", "error": "...", "edge": "..."},
      "dependencies": [],
      "verification": "npm test ...",
      "status": "pending"
    }
  ]
}
```

## Task Types

| Type | Meaning | Ralph Loop Behavior |
|------|---------|---------------------|
| AFK | Can be implemented and merged without human interaction | Execute autonomously |
| HITL | Requires human input (architectural decision, design review, approval) | Pause and prompt user |

The `type` field is extracted from the `**Type:**` line in each SPEC.md task block. Defaults to `AFK` if not specified.

## Proof-of-Work (verification field)

Every task's `verification` is a **single runnable command that exits 0 on pass, non-zero on fail** — not "a test exists," an actual pass/fail proof. The autonomous loop runs exactly this command to decide if the task is done.

Infer from category if not explicitly specified:

| Category | Command Pattern |
|----------|-----------------|
| Backend (Node) | `npm test -- src/api/[name].test.ts` |
| Backend (Python) | `uv run pytest tests/test_[name].py --no-cov` |
| Frontend (has test runner) | `npm test -- src/components/[Name].test.tsx` |
| Frontend (eslint-only, no runner) | `npm run build && npm run typecheck` + documented manual check |
| Integration | `npm run test:e2e -- [spec]` |

Override with the SPEC task's `**Verification:**` field if present.

### Gotchas the proof-of-work command must handle

1. **Strip per-test coverage gates.** An isolated task proof runs a subset of the suite, so a suite-wide coverage threshold makes it fail spuriously. Add `--no-cov` (pytest) / `--coverage=false` (jest) / equivalent so the single-task command proves *that task's* behavior, not global coverage.
2. **No asserting test exists yet? Add one.** For config/temp/plumbing changes with no natural test, the task's first deliverable is the asserting test itself — one test that fails before the change and passes after. The proof-of-work command runs that test. Don't accept "manually verified" when a cheap assert is possible.
3. **Layer has no test runner? Don't drag in a framework for one change.** Fall back to `build + typecheck` **plus** an inspectable artifact (e.g. an exported `const` the change sets) **plus** a one-line documented manual check in the task. Adding Jest/Vitest to an eslint-only frontend just to prove one change is over-engineering — the build/typecheck + manual check is the lazy proof.

## Independent Usability (hard rule)

Each task must be a **working, independently testable solution** — after it completes, that feature is usable on its own to solve its problem, with no "but first you also need TASK-X." A task is not just "a slice of a feature"; it must stand up and run by itself once its declared `dependencies` are done.

When converting, reject/flag any task where:
- The feature can't be exercised until a *later* task lands (hidden forward dependency → merge them or reorder).
- It only makes sense combined with a sibling (→ they're one task).
- Its proof-of-work command can't run without something not in its `dependencies`.

Every declared dependency must be an *earlier* task. If a task needs something to be usable, that something is either a listed dependency or part of this task.
