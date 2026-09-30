# PR Body Template

Use this for a structural or multi-file change when the repo has no PR template.
**If the repo has `.github/pull_request_template.md` (or a Bitbucket equivalent),
that wins** — follow its structure and take only the discipline rules below.
For a small single-concern PR, plain prose is still the right body; don't force
three headings onto a two-line fix.

---

## Structure

```markdown
[{TICKET}]({url})  | [{related plan/doc}]({url})

## Why the change

{Exactly one sentence: the problem this solves and what becomes possible after it ships.}

## Special things to note

- {1–3 bullets. `- None.` when there are none.}

## Change outline

{The smallest combination of views below that explains the implementation.}
```

Header line is optional: include ticket/plan/PR links only when you actually
have them, otherwise omit the header entirely.

## Discipline rules

- **Why the change** is *exactly one sentence*. Not two, not a paragraph.
- **Special things to note** is 1–3 bullets, prioritising reviewer warnings,
  migrations, compatibility constraints, deliberate omissions, and surprising
  decisions. Write `- None.` when there are none — never drop the section
  silently, a reviewer reads an absent section as "you forgot to look".
- **Do not expand the body beyond this template.** No implementation narrative,
  no rationale essay, no changelog. Rationale that a reviewer can't reconstruct
  from the diff belongs in *Special things to note*, one bullet at a time.
- Write as one human talking to another: no jargon, no slang, no AI/bot
  attribution trailers.

## Change outline — view menu

A compact structural view, **not** prose and **not** a file-by-file changelog.
Include only the views that help explain *this* PR; omit headings for views that
did not change. Pick from:

| View | Show |
|---|---|
| Contract | changed SQL tables, important columns/relationships, endpoint request/response shapes |
| Types | new or changed data structures that are key to the implementation |
| Behaviour | concise pseudocode for the changed logic |
| Files | shallow file tree with the changed responsibilities annotated |
| UI | component-tree changes, including important hooks/state and package boundaries |
| Flow | call-tree, call-stack, control-flow, or data-flow changes |

Use `diff` blocks for a focused change to an existing shape. Use a complete
language-tagged (` ```sql `, ` ```ts `, ` ```text `) block when the shape is
mostly new, when omitted context would hide ownership or order, or when the
reviewer needs a copyable target.

The shape vocabulary and worked examples for every one of these views live in
the `visual-explainer` skill's `references/inline-shapes.md` — same ladder,
smallest view that carries the point.

## Ordering

Tell the story in the order that makes it easiest to understand. It may make
sense to show files first, or to establish a data structure, SQL table, or API
contract first. All views and subheadings are optional — name and order them
based on the change rather than following a fixed template.
