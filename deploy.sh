#!/usr/bin/env bash
# deploy.sh — sync skills/ to all tool-specific locations
#
# Run this after adding or editing any skill:
#   bash ~/development/common-agent-skills/deploy.sh
#
# Deploy targets:
#   ~/.agents/skills/     Pi reads this natively (Agent Skills standard)
#   ~/.claude/skills/     Claude Code
#   ~/.codex/skills/      Codex (additive only — preserves .system/)
#
# This script is the only thing that writes to those directories.
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
# Full sync. Claude Code has no system subdirectories to protect.
TARGET_CLAUDE="$HOME/.claude/skills"
mkdir -p "$TARGET_CLAUDE"
rsync -a --delete \
  --exclude='.git/' \
  "$SKILLS_DIR/" "$TARGET_CLAUDE/"
ok "~/.claude/skills/"

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
