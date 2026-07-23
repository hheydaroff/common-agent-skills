---
name: integration-test
description: "Verify a whole feature works end-to-end after autonomous execution finishes — that all completed tasks actually compose, not just pass in isolation. Derives scenarios from SPEC.md acceptance criteria, runs them through the real public interface, reports pass/fail, and feeds failures back as fix tasks. Use after ralph/AFK loop completes, or when user says \"does it all work together\", \"integration test\", \"end-to-end test\", \"smoke test the build\", \"verify the whole feature\"."
---

# Integration Test

Ralph (and any per-task loop) proves each task with its own `verification` command — in **isolation**. Green-across-the-board does NOT prove the tasks *compose*. TASK-001's API and TASK-004's UI can each pass their own test and still not talk to each other.

This skill closes that gap: one end-to-end pass that exercises the **assembled feature** through its real public interface, from the user's point of view.

## The one idea

**The acceptance criteria already ARE the integration spec.** `SPEC.md` has a `## Acceptance Criteria` table of Given/When/Then rows. Each row is one end-to-end scenario written in prose. Don't invent test scenarios — derive them from the acceptance criteria. That's the lazy, correct source of truth.

| Layer | Question it answers | Who owns it |
|-------|---------------------|-------------|
| Per-task `verification` | "Does this task's unit work?" | ralph / spec-to-tasks |
| **Integration test (this skill)** | "Do all the tasks work *together*?" | this skill |

## When to run

- After the loop signals completion (`RALPH_COMPLETE` in `progress.txt`, or all `tasks.json` statuses `DONE`).
- Any time the user wants a final "does the whole thing actually work" check.

## Workflow

### 1. Load the contract

Read `SPEC.md` → `## Acceptance Criteria` (Given/When/Then rows). If `tasks.json` exists, read it too — every `acceptanceCriteria[]` entry is an integration scenario. These rows are the test list. If there is no acceptance-criteria section, fall back to the **smoke test** (below).

### 2. Detect how the assembled thing runs

Reuse the project's existing setup — never add a framework. Look for, in order:
- An existing e2e/integration script: `test:e2e`, `test:integration`, `e2e`, `cypress`, `playwright` in `package.json`; a `tests/integration/` or `e2e/` dir; `pytest -m integration`.
- A dev server / entry point to boot: `npm run dev`, `npm start`, `docker compose up`, a `main`/`app` entry.
- `scripts/integration-check.sh` in this skill auto-detects and runs the above; use it when you don't want to hand-detect.

### 3. Write ONE integration suite from the acceptance criteria

One test per acceptance-criteria row, each exercising the **real, running system** through its public surface — start the app, hit the actual HTTP endpoint, drive the actual UI, read the actual DB through the app. Not through internal function calls, not with the collaborators mocked out. This is the opposite of the isolated per-task proofs.

Reuse whatever runner already exists (jest/vitest/pytest/playwright). If the project has none and can't boot a testable surface, go to smoke test.

Independence matters: judge behavior against the acceptance criteria, not against what the task claimed. The point is a second, skeptical look — "does it *actually* do this?" — not a re-run of the builder's own tests.

### 4. Run and report

Run the suite (or `scripts/integration-check.sh`). Emit a compact report — write it to `integration-report.md`:

```
# Integration Report — <feature>  (<timestamp>)

| AC   | Scenario                          | Result |
|------|-----------------------------------|--------|
| AC1  | user checks out with valid cart   | ✅ PASS |
| AC2  | checkout blocked on empty cart    | ❌ FAIL |

FAIL AC2: POST /checkout returned 500 (expected 400). Cart service never
rejects empty carts — TASK-003 validates client-side only.
```

### 5. Close the loop (self-correct)

For each failing AC, the fix is a new task, not a manual patch here:
- Append a task to `tasks.json` (status `pending`) or a line to `progress.txt` describing the failing scenario + observed vs expected, and mark the feature not-complete (remove/negate `RALPH_COMPLETE`).
- Re-run ralph. Its per-task loop fixes the composition bug, then this skill runs again. Green integration report = truly done.

If the user isn't running a loop, just hand them the report and the failing scenarios.

## Smoke test (fallback — no runner, or "just check it boots")

The minimum that catches gross breakage (a.k.a. build-verification test):

1. Build: `npm run build` / `npm run typecheck` / `cargo build` — must exit 0.
2. Boot: start the app / server; confirm it comes up without crashing.
3. One critical path: hit the single most important endpoint or page (the app's reason to exist) and confirm a sane response.
4. Tear down. Report pass/fail on those three.

A smoke test proves "it assembles and starts," not "every scenario works." Say which one you ran.

## Rules

- **Derive, don't invent.** Scenarios come from acceptance criteria. No acceptance criteria → smoke test, and say so.
- **Real interface only.** Mocking the collaborators turns an integration test back into a unit test — the exact thing that already passed. Boot the real thing.
- **Don't add a test framework** to prove composition. Reuse the runner, or smoke-test with build+boot.
- **Failures become tasks**, fed back to the loop — don't silently fix them here (that hides the composition bug from the record).
- One report file (`integration-report.md`), pass/fail per AC, one line of evidence per failure.
