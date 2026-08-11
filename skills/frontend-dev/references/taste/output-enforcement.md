# Full-Output Enforcement

Load when the model keeps truncating work, shipping skeletons, or asking to "continue later". Overrides default LLM truncation behavior — enforce complete code generation.

## Baseline
Treat every task as production-critical. A partial output is a broken output. Optimize for completeness, not brevity. If the user asks for a full file, deliver the full file. If they ask for 5 components, deliver 5. No exceptions.

## Banned output patterns (hard failures)

**In code blocks:** `// ...`, `// rest of code`, `// implement here`, `// TODO`, `/* ... */`, `// similar to above`, `// continue pattern`, `// add more as needed`, bare `...` standing in for omitted code.

**In prose:** "Let me know if you want me to continue", "I can provide more details if needed", "for brevity", "the rest follows the same pattern", "similarly for the remaining", "and so on" (replacing actual content), "I'll leave that as an exercise".

**Structural shortcuts:** outputting a skeleton when asked for a full implementation; showing first + last section while skipping the middle; replacing repeated logic with one example + a description; describing what code should do instead of writing it.

## Execution process
1. **Scope** — read the full request. Count distinct deliverables (files, functions, sections, answers). Lock that number.
2. **Build** — generate every deliverable completely. No partial drafts.
3. **Cross-check** — re-read the original request, compare deliverable count against scope. Add anything missing before responding.

## Handling long outputs
When a response approaches the token limit: do not compress remaining sections, do not skip to a conclusion. Write at full quality up to a clean breakpoint (end of a function/file/section), then end with:

```
[PAUSED — X of Y complete. Send "continue" to resume from: next section name]
```

On "continue", pick up exactly where you stopped. No recap, no repetition.

## Quick check before finalizing
- No banned patterns appear anywhere in the output.
- Every requested item is present and finished.
- Code blocks contain actual runnable code, not descriptions.
- Nothing was shortened to save space.
