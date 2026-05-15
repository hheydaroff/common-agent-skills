---
name: documentation-and-adrs
description: "Record architectural decisions and project documentation. Use when making significant technical decisions, choosing between approaches, changing public APIs, shipping features, or when you need to capture context that future engineers and agents will need. Triggers: 'write an ADR', 'document this decision', 'why did we choose X', 'create docs'."
---

# Documentation and ADRs

Document decisions, not just code. The most valuable documentation captures the *why* — the context, constraints, and trade-offs that led to a decision. Code shows *what* was built; documentation explains *why it was built this way* and *what alternatives were considered*.

## When to Use

- Making a significant architectural decision
- Choosing between competing approaches
- Adding or changing a public API
- Shipping a feature that changes user-facing behavior
- Onboarding new team members (or agents) to the project
- When you find yourself explaining the same thing repeatedly

**When NOT to use:** Don't document obvious code. Don't add comments that restate what the code says. Don't write docs for throwaway prototypes.

## Architecture Decision Records (ADRs)

ADRs capture the reasoning behind significant technical decisions. They're the highest-value documentation you can write.

### When to Write an ADR

- Choosing a framework, library, or major dependency
- Designing a data model or database schema
- Selecting an authentication strategy
- Deciding on an API architecture (REST vs. GraphQL vs. tRPC)
- Choosing between build tools, hosting platforms, or infrastructure
- Any decision that would be expensive to reverse

### ADR Template

Store ADRs in `docs/decisions/` (or `docs/adr/`) with sequential numbering:

```markdown
# ADR-001: [Decision Title]

## Status
Accepted | Superseded by ADR-XXX | Deprecated

## Date
YYYY-MM-DD

## Context
[What problem are we facing? What constraints exist?
What forces are at play that make this decision necessary?]

## Decision
[What we decided and why. Be specific — name the thing.]

## Alternatives Considered

### [Alternative A]
- Pros: [...]
- Cons: [...]
- Rejected because: [specific reason]

### [Alternative B]
- Pros: [...]
- Cons: [...]
- Rejected because: [specific reason]

## Consequences
[What follows from this decision? Both positive and negative.
What becomes easier? What becomes harder? What new constraints exist?]
```

### ADR Lifecycle

```
PROPOSED → ACCEPTED → (SUPERSEDED or DEPRECATED)
```

- **Don't delete old ADRs.** They capture historical context.
- When a decision changes, write a new ADR that references and supersedes the old one.
- ADRs are append-only by nature — the decision log is a timeline.

### Example ADR

```markdown
# ADR-003: Use Zod for Runtime Validation

## Status
Accepted

## Date
2025-06-15

## Context
We need runtime validation at API boundaries. TypeScript types are erased
at runtime, so we need something that validates actual data shapes.
Currently using manual `if` checks which are inconsistent and incomplete.

## Decision
Use Zod for all API input validation and external data parsing.

## Alternatives Considered

### io-ts
- Pros: FP-oriented, good TypeScript inference
- Cons: Steeper learning curve, less intuitive API for team
- Rejected: Team velocity matters more than FP purity

### Joi
- Pros: Battle-tested, rich validation rules
- Cons: TypeScript support is bolted on, types don't infer from schema
- Rejected: We want schema-first type inference

### Manual validation
- Pros: No dependency, full control
- Cons: Inconsistent, incomplete, no type inference
- Rejected: Already causing bugs from missing validations

## Consequences
- All API routes validate input with Zod schemas
- Types are inferred from schemas (single source of truth)
- External API responses are parsed through Zod before use
- Team needs to learn Zod API (low barrier, good docs)
- Bundle size increases ~13KB (acceptable for the safety gained)
```

## Inline Documentation

### When to Comment

Comment the *why*, not the *what*:

```typescript
// BAD: Restates the code
// Increment counter by 1
counter += 1;

// GOOD: Explains non-obvious intent
// Rate limit uses a sliding window — reset at window boundary,
// not on a fixed schedule, to prevent burst attacks at edges
if (now - windowStart > WINDOW_SIZE_MS) {
  counter = 0;
  windowStart = now;
}
```

### When NOT to Comment

```typescript
// Don't comment self-explanatory code
function calculateTotal(items: CartItem[]): number {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

// Don't leave TODO comments for things you should just do now
// TODO: add error handling  ← Just add it

// Don't leave commented-out code
// const oldImplementation = () => { ... }  ← Delete it, git has history
```

### Document Known Gotchas

```typescript
/**
 * IMPORTANT: Must be called before first render.
 * If called after hydration, causes FOUC because
 * theme context isn't available during SSR.
 *
 * See ADR-003 for full design rationale.
 */
export function initializeTheme(theme: Theme): void { ... }
```

## API Documentation

### Inline with Types (Preferred for TypeScript)

```typescript
/**
 * Creates a new task.
 *
 * @param input - Task creation data (title required, description optional)
 * @returns The created task with server-generated ID and timestamps
 * @throws {ValidationError} If title is empty or exceeds 200 characters
 * @throws {AuthenticationError} If the user is not authenticated
 *
 * @example
 * const task = await createTask({ title: 'Buy groceries' });
 */
export async function createTask(input: CreateTaskInput): Promise<Task> { ... }
```

### OpenAPI for REST APIs

When building REST APIs, maintain an OpenAPI spec alongside the implementation. The spec is the contract — implementation follows.

## README Structure

Every project needs a README that answers "how do I use this?":

```markdown
# Project Name

One-paragraph description.

## Quick Start
1. Clone, install, configure, run

## Commands
| Command | Description |
|---------|-------------|
| `npm run dev` | Development server |
| `npm test` | Run tests |
| `npm run build` | Production build |

## Architecture
Brief overview + link to ADRs for details.

## Contributing
Standards, PR process, what to read first.
```

## Changelog Maintenance

For shipped features, maintain a changelog:

```markdown
# Changelog

## [1.2.0] - 2025-01-20
### Added
- Task sharing between team members (#123)

### Fixed
- Duplicate tasks on rapid create clicks (#125)

### Changed
- Task list loads 50 items per page (was 20) (#126)
```

Use [Keep a Changelog](https://keepachangelog.com) format. Categories: Added, Changed, Deprecated, Removed, Fixed, Security.

## Documentation for AI Agents

Special considerations for agent-readable documentation:

- **Rules files** (CLAUDE.md, `.pi/` config) — Document conventions so agents follow them
- **Spec files** — Keep specs updated so agents build the right thing
- **ADRs** — Help agents understand why past decisions were made (prevents re-deciding settled questions)
- **Inline gotchas** — Prevent agents from falling into known traps
- **CONTEXT.md** — Domain glossary so agents use correct terminology

## Process

When this skill is invoked:

1. **Identify what needs documenting** — Is it a decision (ADR), API (inline docs), or project knowledge (README/guide)?
2. **Gather context** — Read the relevant code, understand constraints, identify alternatives considered
3. **Write the doc** — Use the appropriate template above
4. **Place it correctly** — ADRs in `docs/decisions/`, API docs inline, guides in `docs/`
5. **Link it** — Reference from relevant code comments and other docs

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The code is self-documenting" | Code shows what. It doesn't show why, what was rejected, or what constraints apply. |
| "We'll write docs when the API stabilizes" | APIs stabilize faster when you document them. The doc is the first test of the design. |
| "Nobody reads docs" | Agents do. Future engineers do. Your 3-months-later self does. |
| "ADRs are overhead" | A 10-minute ADR prevents a 2-hour debate about the same decision 6 months later. |
| "Comments get outdated" | Comments on *why* are stable. Comments on *what* get outdated — that's why you only write the former. |

## Red Flags

- Architectural decisions with no written rationale
- Public APIs with no documentation or types
- README that doesn't explain how to run the project
- Commented-out code instead of deletion
- TODO comments that have been there for weeks
- No ADRs in a project with significant choices

## Verification

After documenting:

- [ ] ADRs exist for all significant architectural decisions
- [ ] Each ADR lists alternatives considered with reasons for rejection
- [ ] README covers quick start, commands, and architecture overview
- [ ] API functions have parameter and return type documentation
- [ ] Known gotchas are documented inline where they matter
- [ ] No commented-out code remains
- [ ] Documentation is committed alongside the code it describes
