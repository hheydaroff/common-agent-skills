---
name: spec-to-tasks
description: Convert approved SPEC.md into tasks.json for Ralph Loop execution. Use after user has an approved SPEC.md, says "convert spec to tasks", "generate tasks.json", "prepare for Ralph Loop", or wants machine-executable task format.
---

# SPEC to Tasks Conversion

Convert human-readable SPEC.md into machine-executable tasks.json.

## Prerequisites

SPEC.md must exist in the project root (or user-specified location) with:
- `# Feature Spec: [Name]` title
- `## Acceptance Criteria` table (Given/When/Then)
- `## Atomic Tasks` with `### TASK N:` blocks
- `## Dependency Chain` showing phases

If missing, tell user: "SPEC.md not found. Generate one first — from a PRD via whatever PRD-to-spec workflow you use, or author it manually."

## Workflow

### 1. Read & Validate SPEC

Read `SPEC.md` (or user-specified file). Verify these sections exist:
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
- **verification**: from `**Verification:**` line, or infer from category (see patterns below)
- **status**: always `"pending"`

### 4. Write tasks.json

Write the complete JSON file to `tasks.json` in the project root (or user-specified path).

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
> "Created `tasks.json` with N tasks. Ready for autonomous execution (e.g., ralph loop)."

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

## Verification Patterns

Infer verification command from category if not explicitly specified:

| Category | Command Pattern |
|----------|-----------------|
| Backend (Node) | `npm test src/api/[name].test.ts` |
| Backend (Python) | `uv run -m pytest tests/test_[name].py` |
| Frontend | `npm test src/components/[Name].test.tsx` |
| Integration | `npm run test:e2e` |

Override if the SPEC task has a `**Verification:**` field — use that instead.
