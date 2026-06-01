# Decomposition Techniques

## 1. Socratic Questioning (6 types)

Use to systematically expose the structure of someone's thinking:

| Type | Purpose | Example questions |
|------|---------|-------------------|
| **Clarification** | Define terms precisely | "What exactly do you mean by X?" / "Can you give an example?" |
| **Probing assumptions** | Surface hidden premises | "What are you taking for granted here?" / "Why do you believe that's true?" |
| **Probing evidence** | Test the foundation | "What evidence supports this?" / "How do you know?" |
| **Viewpoints** | Escape single-perspective | "Who would disagree, and why?" / "What's the opposing view?" |
| **Implications** | Follow consequences | "If that's true, what follows?" / "What would happen if you're wrong?" |
| **Meta-questions** | Question the question itself | "Why is this the right question to ask?" / "What would a better question be?" |

**Usage:** Start broad (clarification), then probe assumptions, then test evidence. Use viewpoints when the user seems trapped in one frame. Use meta-questions when you suspect the wrong problem is being solved.

## 2. Five Whys

Use to drill past symptoms to root causes. Ask "why?" repeatedly until you hit a truth that cannot be reduced further:

```
Statement: "We need microservices"
Why? → "To scale independently"
Why? → "Because our monolith is slow to deploy"
Why? → "Because deploys take 45 minutes"
Why? → "Because the test suite runs everything"
Why? → "Because modules are coupled"
FUNDAMENTAL: The problem is coupling, not architecture style.
```

**Tips:**
- Don't stop at comfortable answers — the first 2 "whys" are usually still symptoms
- Branch when multiple causes exist at one level — don't force a single chain
- Distinguish "why does this happen?" (causal) from "why do we believe this?" (epistemic)
- Stop when you hit something that's either: a law of nature, a definitional truth, or a directly observable fact

## 3. Constraint Mapping

Separate hard constraints from soft ones:

| Type | Nature | Can be changed? | Examples |
|------|--------|----------------|----------|
| **Hard** (physics/math/logic) | Fundamental laws | No | Speed of light, thermodynamics, P≠NP, CAP theorem |
| **Regulatory** (law/compliance) | Legal requirements | Expensive, slow | GDPR, building codes, financial regulations |
| **Conventional** (industry/habit) | "Best practices" | Yes — this is where breakthroughs live | "Batteries cost $600/kWh", "rockets are disposable", "you need a degree" |
| **Self-imposed** (assumptions) | Internal beliefs | Immediately | "Users won't pay", "we must use X framework", "it's too complex" |

**The key move:** Most people treat conventional and self-imposed constraints as hard. The breakthrough almost always lives in reclassifying something from "hard" to "conventional."

**Process:**
1. List every constraint the user mentions or implies
2. For each one, ask: "What happens if this weren't true?"
3. Classify: hard, regulatory, conventional, or self-imposed
4. Focus energy on challenging the conventional and self-imposed ones

## 4. Inversion

Instead of asking "how do I achieve X?", ask "what would guarantee I fail at X?" Then avoid those things.

```
Goal: "Build a successful product"
Inverted: "How would I guarantee failure?"
→ Build something nobody asked for
→ Ignore user feedback
→ Optimize for metrics that don't correlate with value
→ Add complexity before proving the core works

THEREFORE: Do the opposite of each.
```

**When to use:** When forward reasoning produces only incremental ideas. Inversion often reveals non-obvious fundamentals.

## Combining Techniques

For maximum decomposition power, combine:

1. **Start with Constraint Mapping** to see the full landscape
2. **Apply Five Whys** to the constraints classified as "conventional" — why does everyone believe this?
3. **Use Socratic Questioning** to probe the user's own reasoning within the remaining space
4. **Finish with Inversion** to stress-test the rebuilt solution

This combination moves from landscape → depth → precision → validation.
