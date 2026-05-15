---
name: prototype
description: "Build throwaway prototypes to answer design questions. Two modes: terminal app for state/logic, or multiple UI variations. Use when user says \"prototype this\", \"let me play with it\", wants to sanity-check a model, or explore design options."
---

# Prototype

A prototype is **throwaway code that answers a question**. The question decides the shape.

## Pick a Branch

Identify which question is being answered — from the user's prompt, code context, or by asking:

- **"Does this logic / state model feel right?"** → [LOGIC branch](#logic-branch). Build a tiny interactive terminal app that pushes the state machine through hard-to-reason-about cases.
- **"What should this look like?"** → [UI branch](#ui-branch). Generate several radically different UI variations on a single route, switchable via a floating bar or URL param.

If ambiguous and user isn't reachable, default to whichever matches surrounding code (backend module → logic; page/component → UI) and state the assumption.

## Rules (Both Branches)

1. **Throwaway and clearly marked.** Place prototype code near where it'll be used (for context), but name it obviously — `prototype-*`, `_proto_*`, or a `prototypes/` dir. Never mix with production code.
2. **One command to run.** Whatever the project already uses — `pnpm dev`, `python script.py`, `bun run`. Zero setup friction.
3. **No persistence by default.** State lives in memory. If the question involves a database, use a scratch file with "PROTOTYPE" in the name.
4. **Skip the polish.** No tests, no error handling beyond what makes it runnable, no abstractions. Speed of learning > code quality.
5. **Surface the state.** After every action, print/render the full relevant state so the user sees what changed.
6. **Delete or absorb when done.** Once the question is answered, either delete the prototype or fold the validated decision into real code. Don't leave it rotting.

## Logic Branch

Build a **minimal interactive terminal app** that lets the user push a state machine / data model through scenarios.

### What to Build

```
┌─────────────────────────────────┐
│  State: { ... current state }   │
│                                 │
│  Actions:                       │
│    1. Do X                      │
│    2. Do Y                      │
│    3. Trigger edge case Z       │
│    4. Reset                     │
│    q. Quit                      │
│                                 │
│  > _                            │
└─────────────────────────────────┘
```

### Guidelines

- Model the **real domain types** — don't simplify away the complexity you're testing
- Include edge cases as explicit menu options (the whole point is testing them)
- Print full state after every transition — no hidden mutations
- Add a "reset" action to quickly restart scenarios
- Use the project's language (from `CONTEXT.md` if it exists)

### Good Candidates for Logic Prototypes

- State machines (order lifecycle, subscription states, auth flows)
- Complex validation rules (can user X do Y given Z?)
- Data model relationships (does this schema handle the edge case?)
- Algorithm behavior (does the scoring/ranking produce sensible output?)
- Concurrency scenarios (what happens when A and B fire simultaneously?)

## UI Branch

Generate **3+ radically different designs** for the same screen/component, viewable on a single route with a switcher.

### What to Build

- A single route (e.g. `/prototype` or existing page with `?variant=` param)
- 3+ variations that take **fundamentally different approaches** (not just color changes)
- A floating bottom bar or URL params to switch between variants
- Each variant labeled clearly: "Variant A: Card Grid", "Variant B: Timeline", etc.

### Guidelines

- **Radically different** means different layout, information hierarchy, or interaction model — not tweaks
- Use the project's existing component library / design system if one exists
- Each variant should be self-contained (no shared state between variants)
- Include realistic data (not "Lorem ipsum") so the user can judge information density
- If the project has a `CONTEXT.md`, use domain terminology in the UI

### Good Candidates for UI Prototypes

- New pages where layout isn't obvious
- Dashboard designs (what data goes where?)
- Form flows (wizard vs single page vs progressive disclosure?)
- Navigation structures (sidebar vs tabs vs breadcrumbs?)
- Data-heavy views (table vs cards vs timeline vs kanban?)

## When Done

The **answer** is the only deliverable worth keeping from a prototype:

1. State what you learned: "The state machine breaks when X happens before Y — we need a guard."
2. Capture the decision: commit message, ADR, or comment in the real code.
3. Delete the prototype files (or let the user do it).

If the prototype produced a code snippet that encodes a decision better than prose (a state machine definition, a type shape, a schema), that snippet can graduate to the real codebase — but rewrite it properly (with tests, error handling, etc).
