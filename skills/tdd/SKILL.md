---
name: tdd
description: "Test-driven development with red-green-refactor loop. Use when user wants TDD, test-first development, or mentions \"red-green-refactor\"."
---

# Test-Driven Development

## Philosophy

**Core principle**: Tests should verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't.

**Good tests** are integration-style: they exercise real code paths through public APIs. They describe _what_ the system does, not _how_ it does it. A good test reads like a specification — "user can checkout with valid cart" tells you exactly what capability exists. These tests survive refactors because they don't care about internal structure.

**Bad tests** are coupled to implementation. They mock internal collaborators, test private methods, or verify through external means (like querying a database directly instead of using the interface). The warning sign: your test breaks when you refactor, but behavior hasn't changed. If you rename an internal function and tests fail, those tests were testing implementation, not behavior.

See [references/tests.md](references/tests.md) for examples and [references/mocking.md](references/mocking.md) for mocking guidelines.

## Seams — where tests go

A **seam** is the public boundary you test at: the interface where you observe behavior without reaching inside. Tests live at seams, never against internals.

**Test only at pre-agreed seams.** Before writing any test, write down the seams under test and confirm them with the user. No test is written at an unconfirmed seam. You can't test everything — agreeing the seams up front is how testing effort lands on the critical paths and complex logic instead of every edge case.

Ask: "What's the public interface, and which seams should we test?"

## Anti-Pattern: Horizontal Slices

**DO NOT write all tests first, then all implementation.** This is "horizontal slicing" — treating RED as "write all tests" and GREEN as "write all code."

This produces **bad tests**:

- Tests written in bulk test _imagined_ behavior, not _actual_ behavior
- You end up testing the _shape_ of things (data structures, function signatures) rather than user-facing behavior
- Tests become insensitive to real changes — they pass when behavior breaks, fail when behavior is fine
- You outrun your headlights, committing to test structure before understanding the implementation

**Correct approach**: Vertical slices via tracer bullets. One test → one implementation → repeat. Each test responds to what you learned from the previous cycle.

```
WRONG (horizontal):
  RED:   test1, test2, test3, test4, test5
  GREEN: impl1, impl2, impl3, impl4, impl5

RIGHT (vertical):
  RED→GREEN: test1→impl1
  RED→GREEN: test2→impl2
  RED→GREEN: test3→impl3
```

## Workflow

### 1. Planning

When exploring the codebase, use the project's domain glossary so that test names and interface vocabulary match the project's language, and respect ADRs in the area you're touching.

Before writing any code:

- [ ] Confirm with user what interface changes are needed
- [ ] Confirm the seams under test (prioritize — you can't test everything)
- [ ] Identify opportunities for deep modules (small interface, deep implementation — see [references/deep-modules.md](references/deep-modules.md))
- [ ] Design interfaces for testability (see [references/interface-design.md](references/interface-design.md))
- [ ] List the behaviors to test (not implementation steps)
- [ ] Get user approval on the plan

Ask: "What should the public interface look like? Which behaviors are most important to test?"

### 2. Tracer Bullet

Write ONE test that confirms ONE thing about the system:

```
RED:   Write test for first behavior → test fails
GREEN: Write minimal code to pass → test passes
```

This is your tracer bullet — proves the path works end-to-end.

### 3. Incremental Loop

For each remaining behavior:

```
RED:   Write next test → fails
GREEN: Minimal code to pass → passes
```

Rules:

- One test at a time
- Only enough code to pass current test
- Don't anticipate future tests
- Keep tests focused on observable behavior

### 4. Refactor

After all tests pass, look for refactor candidates (see [references/refactoring.md](references/refactoring.md)):

- [ ] Extract duplication
- [ ] Deepen modules (move complexity behind simple interfaces)
- [ ] Apply SOLID principles where natural
- [ ] Consider what new code reveals about existing code
- [ ] Run tests after each refactor step

**Never refactor while RED.** Get to GREEN first.

## Checklist Per Cycle

```
[ ] Test describes behavior, not implementation
[ ] Test uses public interface only
[ ] Test would survive internal refactor
[ ] Code is minimal for this test
[ ] No speculative features added
```

## Bug Fix Pattern (Prove-It)

When fixing a bug, always reproduce with a test FIRST:

```
1. Write a test that demonstrates the bug (must FAIL with current code)
2. Confirm the test fails (proves the bug exists)
3. Fix the code
4. Confirm the test passes (proves the fix works)
5. The test becomes a regression guard forever
```

Never fix a bug without a failing test first — otherwise you can’t prove you fixed it, and it can regress silently.

## Coverage Scenarios

For every function or component, consider:

| Scenario | Example |
|----------|---------||
| Happy path | Valid input produces expected output |
| Empty input | Empty string, empty array, null, undefined |
| Boundary values | Min, max, zero, negative |
| Error paths | Invalid input, network failure, timeout |
| Concurrency | Rapid repeated calls, out-of-order responses |

## Browser TDD (UI Components)

For browser-based code, TDD can be combined with runtime verification:

1. **Write failing test** (component test with Testing Library or E2E with Playwright)
2. **Implement** the component/feature
3. **Verify in browser** — use DevTools or browser-tools to confirm:
   - DOM renders correctly
   - Console has no errors/warnings
   - Network requests fire correctly
   - Layout doesn't shift (CLS)
4. **Green** — test passes AND browser confirms behavior

This bridges the gap between test-passing and actually-works-in-browser. Tests can pass while the UI is visually broken (z-index, overflow, animation timing). Browser verification catches what tests miss.

## Test Naming

Test names should read like specifications:

```typescript
// Good: describes behavior in plain English
describe('TaskService', () => {
  it('creates a task with valid input', () => {});
  it('rejects tasks with empty titles', () => {});
  it('assigns the creating user as owner', () => {});
});

// Bad: describes implementation
describe('TaskService', () => {
  it('calls repository.save', () => {});
  it('validates the DTO', () => {});
});
```
