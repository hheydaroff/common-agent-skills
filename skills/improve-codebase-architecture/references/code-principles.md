# Code Principles

The north star. When deepening modules or placing seams, these constraints define what "good" looks like at the code level.

## The 10 Rules

### 1. One file, one idea
If you can't say what the file does in one sentence, split it.

### 2. Name from the domain
Code reads like the problem's vocabulary, not like a programming textbook. If the domain calls it "evac", don't call it `relocateNodeToSecondaryHeap`.

### 3. Earn every line
Delete it. Did anything break? Did anything slow down? No? It shouldn't have been there.

### 4. Comments prove
Say WHY. Show the math. Show the invariant. If you're explaining WHAT the code does, rewrite the code until you don't need to.

```python
# BAD
# increment the counter
count += 1

# GOOD
# overflow wraps to 0 — callers expect modular arithmetic
count = (count + 1) & 0xFF
```

### 5. Data is the design
Pick the simplest representation. The algorithm follows from the structure. Flat arrays beat nested objects. Tuples beat classes. Strings beat enums when there are only two values.

### 6. No speculative abstraction
Add a layer only when you have 3+ concrete cases that genuinely differ. One case = inline it. Two cases = maybe a function. Three cases = maybe a parameter. Never an interface until proven necessary.

### 7. Constants have names, and they live at the top

```typescript
const CHUNK_SIZE = 4096;
const MAX_DEPTH = 64;
const FLUSH_MS = 100;
```

Not in a config file. Not scattered. Not unnamed.

### 8. Small correct pieces that compose
Not one function with many flags. Not one class with many modes. Small things that plug together. The caller decides composition, not the callee.

### 9. The proof ships with the code
Tests, invariants, references, algebraic laws — next to what they verify. External docs rot. Inline proofs survive.

### 10. Understand until inevitable
If the code feels "designed", you don't understand the problem well enough yet. When understanding is complete, the code writes itself and brevity is the byproduct.

## Applying During Architecture Improvement

When evaluating module depth and seam placement:

- **#1 + #8** — A deep module does one thing well and composes. If a module does two things, it's two modules pretending.
- **#5** — The simplest data representation often reveals the natural module boundaries. Over-wrapped data creates shallow modules.
- **#6** — A seam with one adapter is speculative. Don't deepen toward hypothetical flexibility. Deepen toward proven complexity.
- **#3 + Deletion test** — If removing a module doesn't increase complexity elsewhere, it was shallow.
- **#2** — Module names from the domain language are deep by nature. Generic names (`Manager`, `Service`, `Handler`) signal shallow modules that lack a clear concept.
- **#9** — Invariants at module boundaries should be stated explicitly, not inferred from tests in another file.

## Red Flags (Architecture Edition)

| Violation | What it signals |
|-----------|----------------|
| #1 broken — module does 3 things | Split candidate |
| #2 broken — `DataProcessor`, `ServiceHelper` | No clear domain concept → likely shallow |
| #5 broken — nested config objects to do simple things | Interface complexity exceeding implementation |
| #6 broken — AbstractFactory with one impl | Speculative seam → inline until needed |
| #8 broken — one god-module with flags | Decomposition candidate |
