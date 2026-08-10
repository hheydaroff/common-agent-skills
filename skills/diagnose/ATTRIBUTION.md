# Attribution

Adapted from **Matt Pocock's skills** — https://github.com/mattpocock/skills
MIT License, Copyright (c) 2026 Matt Pocock. Vendored 2026-06 (repo commit 5831f46),
adapted to this repo's conventions (frontmatter, references/ layout, pi tooling).

## What was adapted
- Upstream `diagnose` (renamed upstream to `diagnosing-bugs`): the 6-phase
  diagnosis loop (feedback loop → reproduce+minimise → hypothesise → instrument →
  fix+regression test → cleanup) and `scripts/hitl-loop.template.sh`.

## Upstream status (checked 2026-08-10)
Upstream added a **Redact section** (v1.2.3: write `<REDACTED>`, build loops
against env vars, quote only signal lines) which our copy lacks.
