# Interface Design

When exploring alternative interfaces for a chosen deepening candidate. Based on "Design It Twice" (Ousterhout) — your first idea is unlikely to be the best.

Uses the vocabulary in [language.md](language.md).

## Process

### 1. Frame the Problem Space

Before generating designs, write a user-facing explanation:

- The constraints any new interface would need to satisfy
- The dependencies it would rely on, and which category they fall into (see [deepening.md](deepening.md))
- A rough illustrative code sketch to ground the constraints — not a proposal, just to make constraints concrete

### 2. Generate 3+ Radically Different Designs

Each must produce a **radically different** interface for the deepened module. Give each a different design constraint:

- Design 1: "Minimize the interface — aim for 1–3 entry points max. Maximise leverage per entry point."
- Design 2: "Maximise flexibility — support many use cases and extension."
- Design 3: "Optimise for the most common caller — make the default case trivial."
- Design 4 (if applicable): "Design around ports & adapters for cross-seam dependencies."

Each design outputs:

1. Interface (types, methods, params — plus invariants, ordering, error modes)
2. Usage example showing how callers use it
3. What the implementation hides behind the seam
4. Dependency strategy and adapters
5. Trade-offs — where leverage is high, where it's thin

### 3. Present and Compare

Present designs sequentially so the user can absorb each one, then compare in prose. Contrast by **depth** (leverage at interface), **locality** (where change concentrates), and **seam placement**.

Give your recommendation: which design is strongest and why. If elements from different designs combine well, propose a hybrid. Be opinionated — the user wants a strong read, not a menu.
