# Attribution

Adapted from **Matt Pocock's skills** — https://github.com/mattpocock/skills
MIT License, Copyright (c) 2026 Matt Pocock. Vendored 2026-04 (repo commit f5cf969),
adapted to this repo's conventions (frontmatter, references/ layout, pi tooling).

## What was adapted
- Upstream `engineering/tdd`: red-green-refactor loop, vertical slices
  (one test → one implementation), tests at public seams.

## Local modifications
- Expanded locally with references/; the ralph skill builds tasks through it.

## Upstream status (checked 2026-08-10)
Upstream rewritten around **pre-agreed seams** ("no test at an unconfirmed seam"),
a **tautological-test** anti-pattern, and new `tests.md` + `mocking.md` references.
**Synced 2026-08-10:** seams block + tautological tests ported; our richer local
sections (browser TDD, bug-fix pattern, coverage table) kept.
