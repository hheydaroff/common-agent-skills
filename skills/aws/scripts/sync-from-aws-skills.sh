#!/usr/bin/env bash
# Re-sync the `aws` skill's domain references from the locally installed AWS skill pack.
#
# Use after `aws` (the AWS agent-skills installer) ships new skill versions:
#   bash scripts/sync-from-aws-skills.sh            # sync from ~/.agents/skills
#   bash scripts/sync-from-aws-skills.sh --source ~/.claude/skills
#
# Then review the diff, run ../../validate-skills.sh, deploy, and commit.
set -euo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
exec uv run --quiet python "$here/sync-from-aws-skills.py" "$@"