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

### 1. Validate SPEC

Read `SPEC.md` (or user-specified file). Verify required sections exist:

```python
required = ["# Feature Spec:", "## Atomic Tasks", "### TASK"]
```

If validation fails, list missing sections.

### 2. Run Conversion

```bash
uv run .claude/skills/spec-to-tasks/scripts/spec_to_tasks.py
```

With custom paths:
```bash
uv run .claude/skills/spec-to-tasks/scripts/spec_to_tasks.py [spec_path] [output_path]
```

### 3. Report Results

Script outputs summary:
```
✅ Created tasks.json: N tasks in M phases

| ID       | Phase | Category | Title                    | Deps |
|----------|-------|----------|--------------------------|------|
| TASK-001 | 1     | Backend  | Create API endpoint      | None |
| TASK-002 | 2     | Frontend | Build form UI            | 001  |
```

### 4. Next Step

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
      "estimate": "4-5 hours",
      "verification": "npm test ...",
      "status": "pending"
    }
  ]
}
```

## Verification Patterns

Script infers from category:

| Category | Command Pattern |
|----------|------------------|

## Task Types

| Type | Meaning | Ralph Loop Behavior |
|------|---------|---------------------|
| AFK | Can be implemented and merged without human interaction | Execute autonomously |
| HITL | Requires human input (architectural decision, design review, approval) | Pause and prompt user |

The `type` field is extracted from the `**Type:**` line in each SPEC.md task block. Defaults to `AFK` if not specified.

## Verification Patterns

| Category | Command Pattern |
|----------|-----------------|
| Backend (Node) | `npm test src/api/[name].test.ts` |
| Backend (Python) | `uv run -m pytest tests/test_[name].py` |
| Frontend | `npm test src/components/[Name].test.tsx` |
| Integration | `npm run test:e2e` |

Override in SPEC.md if needed by adding `**Verification:**` field to tasks.
