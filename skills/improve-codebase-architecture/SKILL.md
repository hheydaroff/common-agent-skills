---
name: improve-codebase-architecture
description: "Find deepening opportunities that turn shallow modules into deep ones. Use when user wants to improve architecture, find refactoring opportunities, or make code more testable and AI-navigable."
---

# Improve Codebase Architecture

Surface architectural friction and propose **deepening opportunities** — refactors that turn shallow modules into deep ones. The aim is testability, maintainability, and AI-navigability (agents navigate better when modules are deep and named using domain language).

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

**Scope before you scan — YAGNI.** Deepening a module pays off by making future changes to it easier, so put extra weight on the parts of the codebase that have recently changed. Decide *where* to look before you look:

- If the user named a direction — a module, a subsystem, a pain point — take it, and skip the inference below.
- Otherwise, walk back a good stretch of the commit history (`git log --oneline`) to find the codebase's hot spots — the files and areas that keep coming up — and let those paths pull your attention first. If the changes are scattered with no clear hot spot, widen the net.

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

### 2. Present Candidates as an HTML Report

Write a self-contained HTML file to the OS temp directory so nothing lands in the repo. Resolve the temp dir from `$TMPDIR`, falling back to `/tmp`, and write to `<tmpdir>/architecture-review-<timestamp>.html` so each run gets a fresh file. Open it for the user — `open <path>` on macOS, `xdg-open <path>` on Linux — and tell them the absolute path.

The report uses **Tailwind via CDN** for layout and styling, and **Mermaid via CDN** for diagrams where a graph/flow/sequence reliably communicates the structure. Mix Mermaid with hand-crafted CSS/SVG visuals — use Mermaid when relationships are graph-shaped (call graphs, dependencies, sequences), and hand-built divs/SVG when you want something more editorial (mass diagrams, cross-sections). Each candidate gets a **before/after visualisation**. Be visual.

For each candidate, render a card with:

- **Files** — which files/modules are involved
- **Problem** — why the current architecture is causing friction
- **Solution** — plain English description of what would change
- **Benefits** — explained in terms of locality and leverage, and how tests would improve
- **Before / After diagram** — side-by-side, custom-drawn, illustrating the shallowness and the deepening
- **Recommendation strength** — one of `Strong`, `Worth exploring`, `Speculative`, rendered as a badge

End the report with a **Top recommendation** section: which candidate you'd tackle first and why.

See [references/html-report.md](references/html-report.md) for the full HTML scaffold, diagram patterns, and styling guidance.

**Use CONTEXT.md vocabulary for the domain, and glossary vocabulary for the architecture.** If `CONTEXT.md` defines "Order," talk about "the Order intake module" — not "the FooBarHandler."

**ADR conflicts**: if a candidate contradicts an existing ADR, only surface it when the friction is real enough to warrant revisiting. Mark it clearly (e.g. _"contradicts ADR-0007 — but worth reopening because…"_).

Do NOT propose interfaces yet. After the file is written, ask the user: "Which of these would you like to explore?"

### 3. Grilling Loop

Once the user picks a candidate, run the **grill-me** skill to walk the decision tree with them — constraints, dependencies, the shape of the deepened module, what sits behind the seam, what tests survive.

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
- [references/html-report.md](references/html-report.md) — HTML report scaffold, diagram patterns, and styling guidance
- [references/deepening.md](references/deepening.md) — How to deepen modules safely given dependencies
- [references/interface-design.md](references/interface-design.md) — "Design It Twice" pattern for interface exploration
- [references/code-principles.md](references/code-principles.md) — 10 authoring constraints defining what "good" looks like at the code level
