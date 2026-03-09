# Task Template Reference

## Full Task Template

```
═══════════════════════════════════════════════════════════

TASK [#]: [Action Verb] [Component/Feature]

Description:
[What needs to be built - be specific, not vague]

Acceptance Criteria:
- [ ] Specific criterion from SPEC AC list
- [ ] Another criterion this task satisfies

Technical Details:
- Language/framework: [tech]
- External dependencies: [APIs, libraries]
- Database changes: [migrations needed]
- API endpoints: [routes affected]

Test Cases:
✓ Happy: [normal expected behavior]
✓ Error: [what happens when X fails]
✓ Edge: [boundary conditions, limits]

Dependencies:
- Blocks: [Task #s that can't start until this completes]
- Blocked by: [Task #s that must complete first]

Estimated Hours: [4-8 recommended]

Definition of Done:
- [ ] Code written and reviewed
- [ ] All test cases passing
- [ ] Works on target environment
- [ ] Documentation updated (if needed)

═══════════════════════════════════════════════════════════
```

## Example: Login Feature Tasks

### Backend Tasks

**TASK 1: Create Authentication API Endpoint**
- Description: Implement POST /api/auth/login accepting email/password, returning JWT on success
- Satisfies: AC1 (valid login), AC2 (invalid credentials error)
- Tests: Valid creds → 200 + token | Invalid → 401 | Missing fields → 400
- Dependencies: None (can start immediately)
- Estimate: 5-6 hours

**TASK 2: Implement Password Hashing**
- Description: Configure bcrypt (cost ≥10), hash on store, verify on login
- Satisfies: Security requirement (passwords never stored plaintext)
- Tests: Hash produces salt | Verify correct password | Reject incorrect
- Dependencies: TASK 1
- Estimate: 3-4 hours

**TASK 3: Implement Rate Limiting**
- Description: Track failed attempts per email, lock after 5 failures for 15 min
- Satisfies: AC3 (lockout after 5 attempts)
- Tests: 1-4 failures allow retry | 5th triggers lock | Unlock after 15 min
- Dependencies: TASK 1, 2
- Estimate: 5-7 hours

**TASK 4: Create JWT Generation & Validation**
- Description: Generate tokens with user ID + 30-min expiry, validate middleware
- Satisfies: AC4 (session timeout)
- Tests: Valid token grants access | Expired → 401 | Tampered → 401
- Dependencies: TASK 1
- Estimate: 4-5 hours

### Frontend Tasks

**TASK 5: Build Login Form UI**
- Description: Create form with email input, password input, submit button, error display
- Satisfies: AC5 (form renders), AC6 (responsive)
- Tests: All fields render | Mobile layout works | Keyboard navigation
- Dependencies: None (can parallel with backend)
- Estimate: 3-4 hours

**TASK 6: Add Client-Side Validation**
- Description: Validate email format, password min 8 chars, show inline errors
- Satisfies: AC7 (client validation)
- Tests: Invalid email shows error | Short password shows error | Valid clears
- Dependencies: TASK 5
- Estimate: 2-3 hours

**TASK 7: Connect Form to API**
- Description: Wire submission to POST /api/auth/login, handle success/error/loading
- Satisfies: AC1, AC2, AC8 (loading state)
- Tests: Success → redirect | Error → show message | Loading → spinner
- Dependencies: TASK 1, 5, 6
- Estimate: 4-5 hours

### Integration Tasks

**TASK 8: Implement Token Storage**
- Description: Store JWT in httpOnly cookie, attach to all requests, auto-logout on expiry
- Satisfies: AC4 (session persistence), AC9 (auto-logout)
- Tests: Token persists reload | Expired triggers logout | Cleared on manual logout
- Dependencies: TASK 4, 7
- Estimate: 4-5 hours

**TASK 9: Write Integration Tests**
- Description: Test full flow: form → API → DB → token
- Satisfies: All ACs (verification)
- Tests: Happy path | Invalid creds | Rate limit | Token expiry
- Dependencies: TASK 1-8
- Estimate: 5-6 hours

**TASK 10: Security Audit**
- Description: Audit for SQL injection, XSS, CSRF; verify HTTPS; check logs for passwords
- Satisfies: Security requirements
- Tests: Injection attempts fail | XSS sanitized | HTTPS enforced
- Dependencies: TASK 1-8
- Estimate: 6-8 hours

## Dependency Chain Visualization

```
PHASE 1 (Parallel - Week 1):
├─ TASK 1: API endpoint ─────────────┐
├─ TASK 5: Form UI ──────────────────┼─┐
└─ TASK 6: Form validation ──────────┼─┤
                                     │ │
PHASE 2 (Parallel - Week 2):         │ │
├─ TASK 2: Password hashing (→1) ────┤ │
├─ TASK 4: JWT (→1) ─────────────────┤ │
└─ TASK 7: Connect form (→1,5,6) ────┼─┘
                                     │
PHASE 3 (Sequential - Week 3):       │
├─ TASK 3: Rate limiting (→1,2) ─────┤
├─ TASK 8: Token storage (→4,7) ─────┤
├─ TASK 9: Integration tests (→1-8) ─┤
└─ TASK 10: Security audit (→1-8) ───┘
```

## INVEST Checklist

Before coding, verify each task passes:

| Criterion | Question | Pass? |
|-----------|----------|-------|
| **I**ndependent | Can complete without waiting for unfinished tasks? | |
| **N**egotiable | Team can discuss scope and adjust? | |
| **V**aluable | Delivers user-facing or technical value? | |
| **E**stimable | Can estimate hours/story points? | |
| **S**mall | Completable in 1-2 days (4-8 hours)? | |
| **T**estable | Has clear pass/fail test cases? | |

## Common Pitfalls

| Pitfall | Example | Fix |
|---------|---------|-----|
| **Too Big** | "Build entire login" | Split: form, validation, API, token |
| **Vague AC** | "User should be able to login" | "Valid credentials return 200 + JWT" |
| **Missing Errors** | Only happy path | Add: invalid input, timeout, server error |
| **Sequential Everything** | Task 2 waits for Task 1 | Parallelize: frontend + backend |
| **Mixed Concerns** | Hashing + form + API in one | Separate: hash service, form UI, endpoint |
| **No Estimates** | "Implement auth" | "Implement auth endpoint (5-6 hours)" |
