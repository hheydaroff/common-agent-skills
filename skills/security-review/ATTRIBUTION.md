# Attribution

Adapted from **cloudflare/security-audit-skill** - https://github.com/cloudflare/security-audit-skill
MIT License, Copyright (c) 2025-2026 Cloudflare, Inc. Vendored 2026-10 (shallow clone of `main`), adapted to this
repo's conventions (frontmatter, flat `references/`, pi tooling).

## What was adapted
- Upstream `skills/security-audit/SKILL.md`: operating modes, execution safety, boundary-and-result
  principle, source visibility, verdict discipline, severity anchors, anti-patterns.
- `ATTACK-CLASSES.md` and the 10 domain companions (AI-AND-LLM, CLIENT-SIDE, CLOUD-AND-DEPLOYMENT,
  DATA-ISOLATION-AND-LIFECYCLE, DESKTOP-MOBILE-AND-LOCAL-IPC, MEMORY-SAFETY-AND-BINARY,
  PROTOCOLS-RPC-AND-MESSAGING, RESOURCE-EXHAUSTION-AND-AVAILABILITY, SUPPLY-CHAIN-AND-RELEASE,
  WEB-PROTOCOL-AND-AUTH): copied verbatim to `references/`.
- `RECONNAISSANCE.md`, `HUNTING.md`, `VALIDATION-AND-REPORTING.md`: condensed into
  `references/audit-workflow.md` (hunting method and candidate gate verbatim, except the execution paragraph).

## Local modifications
- Files renamed to flat lowercase (`domain-*.md`); the companion links in `attack-classes.md` are plain
  filenames so SKILL -> ref -> ref chains do not exist.
- Delegation mapped to `herdr-subagent`; sequential fallback when not in Herdr.
- Default execution is source-only; sandboxed execution only when the user grants one.
- **Not imported:** `report-schema.json`, `validate-findings.cjs`, `validate-coverage-ledger.cjs` (+ tests),
  the coverage-ledger JSON model (replaced by a unit list in `architecture.md`), the agent-invocation
  budget arithmetic, and the fd-level artifact-promotion procedure. Reports are `findings.json` +
  `REPORT.md` only, checked by hand.
