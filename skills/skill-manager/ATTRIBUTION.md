# Attribution

Adapted from **nicobailon/skill-diet** — https://github.com/nicobailon/skill-diet
MIT License, Copyright (c) Nico Bailon. Harvested 2026-10-27 (repo commit `5f41df1`).

Deliberately not vendored as a separate skill: its job — keeping skills lean and correct
— is this skill's job, so it lands as one reference here.

## What was adapted

`references/lean-authoring.md`:
- the level ladder (`description` → `SKILL.md` → `references/` → the tool's help → the
  tool's replies and errors) and the two extra levels for skills that teach a tool;
- the edit ladder that stops at the first step handling the change;
- the commit budget (size before → after, offset growth with a cut);
- the four cuts, the drift rule, and the `disable-model-invocation` opt-out.

All rewritten against this repo's conventions (pi frontmatter, `references/` layout,
`validate-skills.sh`, deploy targets).

## Not taken

- The upstream diet harness: `scripts/eval.mjs check`, `references/adapter.md`,
  calibration, and the before/after/no-skill scoring. **The checked-in upstream repo does
  not contain it** — `references/diet.md` links `tool-skills.md` and `eval.md`, and
  `SKILL.md` calls `scripts/eval.mjs`, none of which exist in the tree. Re-check upstream
  before trying to import it.
- The whole-skill rewrite workflow past the outline in the reference (needs that harness).