# Attribution — aws

## Upstream source

The 24 AWS domains are a verbatim consolidation of the AWS agent skills installed by the
AWS skills installer (`aws` CLI "Configure AWS skills and the AWS MCP server" prompt), which
fetches them from **https://github.com/aws/agent-toolkit-for-aws** (`skills/`).

- Upstream repository: <https://github.com/aws/agent-toolkit-for-aws>
- Installed at: `~/.agents/skills/<name>/` (and copies in `~/.claude`, `~/.cursor`, `~/.kiro`,
  `~/.pi/agent/skills`)
- Per-skill upstream versions at import time (from each `.aws-skill-metadata`):
  `amazon-bedrock` v8, `aws-ai-ml` v6, `aws-auth` v1, `aws-billing-and-cost-management` v1,
  `aws-blocks` v2, `aws-cdk` v2, `aws-cloudformation` v3, `aws-compute` v2,
  `aws-containers` v6, `aws-database` v3, `aws-deployment` v1, `aws-iam` v3,
  `aws-messaging-and-streaming` v4, `aws-networking` v2, `aws-observability` v11,
  `aws-sdk-js-v3-usage` v1, `aws-sdk-python-usage` v1, `aws-sdk-swift-usage` v1,
  `aws-security` v1, `aws-serverless` v5, `aws-storage` v1,
  `aws-well-architected-review` v2, `launch-with-aws` v5, `signing-in-to-aws` v1.
- License: the installer copies no LICENSE file into the skill directories, so the terms are
  whatever the upstream repository carries — check it before redistributing outside this
  personal skills repo.

## Local modifications

Content is preserved verbatim; the mechanical changes are:

- Each upstream `SKILL.md` became `references/<domain>/INDEX.md` with its YAML frontmatter
  stripped and a two-line header naming the upstream skill and version.
- Every internal markdown link was rewritten to be relative to this skill's root
  (`references/<domain>/...`) so the preserved nested reference trees stay reachable.
- The "AWS MCP `retrieve_skill` vs local install" guardrail section in 24 `SKILL.md` files
  was replaced with a local-install-only note (no AWS MCP server is configured here).
- `SKILL.md` (the router) and `ATTRIBUTION.md` are new.

## Local additions (not from AWS)

- `references/cost-projection/INDEX.md` — the user's own `aws-cost-projection` skill
  (multi-account cost collection + growth projections for reseller negotiation).
- `references/bedrock/references/prompt-caching-typescript-workflow.md` — the user's own
  `bedrock-prompt-caching` skill (TypeScript `ConverseStreamCommand` recipe); the
  authoritative mechanics stay in the upstream `references/prompt-caching.md`.

## Refreshing

After `deploy.sh`, `~/.agents/skills/` holds only this consolidated skill, so a re-sync needs
fresh upstream copies first:

1. Run the AWS skills installer again and let it install the 24 AWS skills into
   `~/.agents/skills/`.
2. `bash scripts/sync-from-aws-skills.sh` — re-copies the domains, re-applies the
   transformations above, and exits non-zero if any local link stops resolving.
3. Review the diff, `bash deploy.sh` (removes the loose upstream copies again), commit.

The sync skips domains whose upstream directory is missing, so `references/cost-projection/`
and the local prompt-caching addition survive a re-sync.