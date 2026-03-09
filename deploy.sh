#!/usr/bin/env bash
# deploy.sh — sync skills/ to all tool-specific locations
#
# Usage:
#   bash deploy.sh           additive — adds/updates skills, never deletes
#   CLEAN=1 bash deploy.sh   full replace for Claude (use only when repo is complete)
#
# Deploy targets:
#   ~/.agents/skills/     Pi reads this natively — always clean-synced (it IS the canonical copy)
#   ~/.claude/skills/     Claude Code — additive by default, CLEAN=1 for full replace
#   ~/.codex/skills/      Codex — always additive, .system/ never touched
#
# Never edit skills directly in the deploy targets.

set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_DIR="$REPO_DIR/skills"

# Colours
GREEN='\033[0;32m'
DIM='\033[2m'
RESET='\033[0m'

ok()  { echo -e "${GREEN}✓${RESET} $*"; }
dim() { echo -e "${DIM}$*${RESET}"; }

echo ""
echo "Deploying from: $SKILLS_DIR"
echo ""

# ── ~/.agents/skills/ ─────────────────────────────────────────────────────────
# Full sync. Pi reads this directory natively (no further config needed).
# Always uses --delete here since this IS the canonical location and should
# mirror the repo exactly.
TARGET_AGENTS="$HOME/.agents/skills"
mkdir -p "$TARGET_AGENTS"
rsync -a --delete \
  --exclude='.git/' \
  --exclude='deploy.sh' \
  --exclude='setup.sh' \
  --exclude='README.md' \
  --exclude='.gitignore' \
  "$SKILLS_DIR/" "$TARGET_AGENTS/"
ok "~/.agents/skills/"

# ── ~/.claude/skills/ ─────────────────────────────────────────────────────────
# Additive by default. Pass --clean to do a full replace (removes skills no
# longer in the repo). Only use --clean once the repo is your complete source
# of truth — it will delete anything in ~/.claude/skills/ not in skills/.
TARGET_CLAUDE="$HOME/.claude/skills"
mkdir -p "$TARGET_CLAUDE"
if [ "${CLEAN:-0}" = "1" ]; then
  rsync -a --delete \
    --exclude='.git/' \
    "$SKILLS_DIR/" "$TARGET_CLAUDE/"
  ok "~/.claude/skills/  (clean sync)"
else
  rsync -a \
    --exclude='.git/' \
    "$SKILLS_DIR/" "$TARGET_CLAUDE/"
  ok "~/.claude/skills/  (additive)"
fi

# ── ~/.codex/skills/ ──────────────────────────────────────────────────────────
# Additive only — never delete, never touch .system/ (Codex internals).
TARGET_CODEX="$HOME/.codex/skills"
if [ -d "$TARGET_CODEX" ]; then
  rsync -a \
    --exclude='.git/' \
    --exclude='.system/' \
    "$SKILLS_DIR/" "$TARGET_CODEX/"
  ok "~/.codex/skills/  (additive, .system/ preserved)"
else
  dim "~/.codex/skills/ not found — skipped"
fi

echo ""
dim "Pi reads ~/.agents/skills/ natively — no extra config needed."
echo ""
echo "Done. Commit and push your changes:"
dim "  cd $REPO_DIR"
dim "  git add -A && git commit -m \"update: skill-name\" && git push"
echo ""
