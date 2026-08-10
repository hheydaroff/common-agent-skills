# Attribution

Adapted from **Matt Pocock's skills** — https://github.com/mattpocock/skills
MIT License, Copyright (c) 2026 Matt Pocock. Vendored 2026-05 (repo commit cb28fa2),
adapted to this repo's conventions (frontmatter, references/ layout, pi tooling).

## What was adapted
- Upstream `triage` state machine: bug/enhancement categories ×
  needs-triage / needs-info / ready-for-agent / ready-for-human / wontfix states.

## Upstream status (checked 2026-08-10)
Upstream added `AGENT-BRIEF.md` (durable agent briefs), an `.out-of-scope/`
knowledge base, and external-PR coverage ("a PR is an issue with attached code").
**Synced 2026-08-10:** PR coverage deltas, the PR agent-brief example, and the
"already implemented" guard ported. We skipped upstream's issue-tracker
setup-skill dependency (tracker-agnostic instead).
