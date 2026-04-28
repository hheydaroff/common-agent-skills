---
name: improve-codebase-architecture
description: Find deepening opportunities in a codebase — refactors that turn shallow modules into deep ones for better testability and maintainability. Use when user wants to improve architecture, find refactoring opportunities, consolidate tightly-coupled modules, or make a codebase more testable.
---

# Improve Codebase Architecture

Surface architectural friction and propose **deepening opportunities** — refactors that turn shallow modules into deep ones. The aim is testability and maintainability.

## Glossary

Use these terms exactly in every suggestion. Consistent language is the point — don't drift into "component," "service," "API," or "boundary." Full definitions in [references/language.md](references/language.md).

- **Module** — anything with an interface and an implementation (function, class, package, slice)
- **Interface** — everything a caller must know to use the module: types, invariants, error modes, ordering, config. Not just the type signature.
- **Implementation** — the code inside
- **Depth** — leverage at the interface: a lot of behaviour behind a small interface. **Deep** = high leverage. **Shallow** = interface nearly as complex as the implementation.
- **Seam** — where an interface lives; a place behaviour can be altered without editing in place
- **Adapter** — a concrete thing satisfying an interface at a seam
- **Leverage** — what callers get from depth
- **Locality** — what maintainers get from depth: change, bugs, knowledge concentrated in one place

Key principles:

- **Deletion test**: imagine deleting the module. If complexity vanishes, it was a pass-through. If complexity reappears across N callers, it was earning its keep.
- **The interface is the test surface.**
- **One adapter = hypothetical seam. Two adapters = real seam.**

This skill is informed by the project's domain model — `CONTEXT.md` and any `docs/adr/`. The domain language gives names to good seams; ADRs record decisions the skill should not re-litigate.

## Process

### 1. Explore

Read existing documentation first:

- `CONTEXT.md` (or `CONTEXT-MAP.md` + each `CONTEXT.md` in a multi-context repo)
- Relevant ADRs in `docs/adr/`

If any of these files don't exist, proceed silently — don't flag their absence.

Then explore the codebase organically and note where you experience friction:

- Where does understanding one concept require bouncing between many small modules?
- Where are modules **shallow** — interface nearly as complex as the implementation?
- Where have pure functions been extracted just for testability, but the real bugs hide in how they're called (no **locality**)?
- Where do tightly-coupled modules leak across their seams?
- Which parts of the codebase are untested, or hard to test through their current interface?

Apply the **deletion test** to anything you suspect is shallow: would deleting it concentrate complexity, or just move it?

### 2. Present Candidates

Present a numbered list of deepening opportunities. For each candidate:

- **Files** — which files/modules are involved
- **Problem** — why the current architecture is causing friction
- **Solution** — plain English description of what would change
- **Benefits** — explained in terms of locality and leverage, and how tests would improve

**Use CONTEXT.md vocabulary for the domain, and glossary vocabulary for the architecture.** If `CONTEXT.md` defines "Order," talk about "the Order intake module" — not "the FooBarHandler."

**ADR conflicts**: if a candidate contradicts an existing ADR, only surface it when the friction is real enough to warrant revisiting. Mark it clearly (e.g. _"contradicts ADR-0007 — but worth reopening because…"_).

Do NOT propose interfaces yet. Ask the user: "Which of these would you like to explore?"

### 3. Grilling Loop

Once the user picks a candidate, drop into a grilling conversation. Walk the design tree with them — constraints, dependencies, the shape of the deepened module, what sits behind the seam, what tests survive.

Side effects happen inline as decisions crystallize:

- **Naming a deepened module after a concept not in CONTEXT.md?** Add the term — maintain the domain glossary.
- **Sharpening a fuzzy term during conversation?** Update CONTEXT.md right there.
- **User rejects the candidate with a load-bearing reason?** Offer to record it as an ADR so future reviews don't re-suggest it. Only when the reason would actually be needed by a future explorer.

### 4. Design the Interface

When ready to explore interfaces for the deepened module, generate 3+ radically different designs (see [references/interface-design.md](references/interface-design.md)):

- Each design takes a fundamentally different approach
- Compare by **depth** (leverage at interface), **locality** (where change concentrates), and **seam placement**
- Give your recommendation — be opinionated

### 5. Plan the Deepening

For the chosen design, classify dependencies and plan accordingly (see [references/deepening.md](references/deepening.md)):

| Dependency type | Strategy |
|---|---|
| In-process (pure computation) | Merge modules, test directly |
| Local-substitutable (has test stand-in) | Deepen with internal seam, test with stand-in |
| Remote but owned (your services) | Port + adapter pattern |
| True external (third-party) | Inject as port, mock in tests |

**Testing strategy**: Replace, don't layer. Old unit tests on shallow modules become waste once tests at the deepened interface exist — delete them.

## References

- [references/language.md](references/language.md) — Full vocabulary definitions and principles
- [references/deepening.md](references/deepening.md) — How to deepen modules safely given dependencies
- [references/interface-design.md](references/interface-design.md) — "Design It Twice" pattern for interface exploration
