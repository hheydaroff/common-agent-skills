---
name: design-an-interface
description: Generate multiple radically different interface designs for a module using parallel exploration. Use when user wants to design an API, explore interface options, compare module shapes, or mentions "design it twice".
---

# Design an Interface

Based on "Design It Twice" from *A Philosophy of Software Design*: your first idea is unlikely to be the best. Generate multiple radically different designs, then compare.

## Workflow

### 1. Gather Requirements

Before designing, understand:

- [ ] What problem does this module solve?
- [ ] Who are the callers? (other modules, external users, tests)
- [ ] What are the key operations?
- [ ] Any constraints? (performance, compatibility, existing patterns)
- [ ] What should be hidden inside vs exposed?

Ask: "What does this module need to do? Who will use it?"

If inside a repo, explore existing code to understand current patterns and conventions.

### 2. Generate 3+ Radically Different Designs

Each design must take a **fundamentally different approach**, not variations on the same idea. Assign a different constraint to force divergence:

- **Design A — Minimal**: Minimize method count — aim for 1-3 methods max
- **Design B — Flexible**: Maximize flexibility — support many use cases and extension
- **Design C — Optimized**: Optimize for the most common case, make it trivial
- **Design D (optional)**: Take inspiration from a specific paradigm or well-known library

For each design, produce:

1. **Interface signature** — types, methods, parameters
2. **Usage example** — how callers actually use it in practice
3. **What it hides** — complexity kept internal
4. **Trade-offs** — what you gain and what you give up

### 3. Present Designs

Show each design sequentially so the user can absorb each approach before comparison. Use real code signatures and realistic usage examples.

### 4. Compare Designs

After showing all designs, compare them on these criteria from *A Philosophy of Software Design*:

- **Interface simplicity**: Fewer methods, simpler params = easier to learn and use correctly
- **Depth**: Small interface hiding significant complexity = deep module (good). Large interface with thin implementation = shallow module (avoid)
- **General-purpose vs specialized**: Flexibility vs focus. Can it handle future use cases without changes?
- **Implementation efficiency**: Does the interface shape allow efficient internals? Or force awkward implementation?
- **Ease of correct use vs ease of misuse**: Can the caller do the wrong thing?

Discuss trade-offs in **prose, not tables**. Highlight where designs diverge most.

### 5. Synthesize

Often the best design combines insights from multiple options. Ask:

- "Which design best fits your primary use case?"
- "Any elements from other designs worth incorporating?"

Produce a final recommended interface that synthesizes the best aspects.

## Anti-Patterns

- Don't let designs be similar — enforce radical difference via constraints
- Don't skip comparison — the value is in contrast
- Don't implement — this is purely about interface shape
- Don't evaluate based on implementation effort — evaluate based on caller experience
- Don't present a table comparison first — let the user absorb each design individually
