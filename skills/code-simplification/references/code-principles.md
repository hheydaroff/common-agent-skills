# Code Principles

The target state. When simplifying code, these are the constraints that define "done."

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

## Applying During Simplification

When simplifying, ask for each piece of code:

1. Can I explain this file in one sentence? (#1)
2. Would a domain expert recognize these names? (#2)
3. Can I delete any line without consequence? (#3)
4. Do my comments say things the code can't? (#4)
5. Is this the simplest representation? (#5)
6. Am I preserving an abstraction I've only seen used once? (#6)
7. Are magic numbers named and visible? (#7)
8. Could this be two composable things instead of one configurable thing? (#8)
9. Is the proof here or somewhere else? (#9)
10. Does the result feel forced or inevitable? (#10)

## Flag Violations by Number

When reviewing, cite specific violations:

- "This violates #3 — what breaks if we delete it?"
- "Violates #6 — we have one case, inline it."
- "Violates #4 — this comment restates the code. Replace with WHY."
- "Violates #2 — `processData` tells me nothing. What domain concept is this?"
- "Violates #8 — this function has 4 boolean flags. Split it."
