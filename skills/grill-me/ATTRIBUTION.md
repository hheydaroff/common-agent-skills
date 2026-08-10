# Attribution

Adapted from **Matt Pocock's skills** — https://github.com/mattpocock/skills
MIT License, Copyright (c) 2026 Matt Pocock. Vendored 2026-04 (repo commit f5cf969),
adapted to this repo's conventions (frontmatter, references/ layout, pi tooling).

## What was adapted
- The relentless-interview engine from upstream `productivity/grill-me`.
- Doc side-effects (ADR / glossary creation) from upstream `engineering/grill-with-docs`,
  merged into this skill (our commit 7fada0a).

## Local modifications
- Rewritten frontmatter with "Use when…" triggers; format blocks moved to references/.
- Upstream kept grill-with-docs separate; we merged it.

## Upstream status (checked 2026-08-10)
Upstream split the engine into `grilling` (frontier-rounds: numbered questions with
recommended answers, sub-agent fact-gathering) + thin `grill-me` wrapper + separate
`grill-with-docs`. **Synced 2026-08-10:** frontier-rounds engine ported into this
skill; we deliberately keep the merged grill-with-docs side effects and a single skill.
