---
name: triage-issue
description: Triage a bug or issue by exploring the codebase to find root cause, then create a fix plan with TDD cycles. Use when user reports a bug, wants to investigate a problem, mentions "triage", or wants to diagnose and plan a fix.
---

# Triage Issue

Investigate a reported problem, find its root cause, and produce a fix plan with TDD cycles. This is a mostly hands-off workflow — minimize questions to the user.

## Process

### 1. Capture the Problem

Get a brief description of the issue from the user. If they haven't provided one, ask ONE question: "What's the problem you're seeing?"

Do NOT ask follow-up questions yet. Start investigating immediately.

### 2. Explore and Diagnose

Deeply investigate the codebase. Your goal is to find:

- **Where** the bug manifests (entry points, UI, API responses)
- **What** code path is involved (trace the flow)
- **Why** it fails (the root cause, not just the symptom)
- **What** related code exists (similar patterns, tests, adjacent modules)

Look at:
- Related source files and their dependencies
- Existing tests (what's tested, what's missing)
- Recent changes to affected files (`git log` on relevant files)
- Error handling in the code path
- Similar patterns elsewhere in the codebase that work correctly

### 3. Identify the Fix Approach

Based on your investigation, determine:

- The minimal change needed to fix the root cause
- Which modules/interfaces are affected
- What behaviors need to be verified via tests
- Whether this is a regression, missing feature, or design flaw

### 4. Design TDD Fix Plan

Create a concrete, ordered list of RED-GREEN cycles. Each cycle is one vertical slice:

- **RED**: Describe a specific test that captures the broken/missing behavior
- **GREEN**: Describe the minimal code change to make that test pass

Rules:
- Tests verify behavior through public interfaces, not implementation details
- One test at a time, vertical slices (NOT all tests first, then all code)
- Each test should survive internal refactors
- Include a final refactor step if needed
- **Durability**: Describe behaviors and contracts, not internal structure. Tests assert on observable outcomes (API responses, UI state, user-visible effects), not internal state. A good suggestion reads like a spec; a bad one reads like a diff.

### 5. Create the Fix Plan

Save as a file and/or create a GitHub issue.

**File output:**
```
TRIAGE-[IssueName]-[YYYY-MM-DD].md
```

**GitHub issue (if requested):**
```bash
gh issue create --title "Bug: [Title]" --body-file TRIAGE-[IssueName]-[YYYY-MM-DD].md
```

## Fix Plan Template

```markdown
# Triage: [Issue Title]

**Date:** [YYYY-MM-DD]
**Severity:** [Critical / High / Medium / Low]

## Problem

- **What happens** (actual behavior)
- **What should happen** (expected behavior)
- **How to reproduce** (if applicable)

## Root Cause Analysis

What was found during investigation:
- The code path involved
- Why the current code fails
- Any contributing factors

Do NOT include specific file paths, line numbers, or implementation details that couple to current code layout. Describe modules, behaviors, and contracts instead. The plan should remain useful even after major refactors.

## TDD Fix Plan

1. **RED**: Write a test that [describes expected behavior]
   **GREEN**: [Minimal change to make it pass]

2. **RED**: Write a test that [describes next behavior]
   **GREEN**: [Minimal change to make it pass]

...

**REFACTOR**: [Any cleanup needed after all tests pass]

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] All new tests pass
- [ ] Existing tests still pass
```

After creating the plan, print a one-line summary of the root cause.

## Tips

- Start investigating immediately — don't interview the user
- Trace from symptom to root cause, don't guess
- Check `git log` on affected files for recent regressions
- Look for similar patterns that work correctly — they reveal what's different
- Keep the fix plan durable: describe behaviors, not file paths
