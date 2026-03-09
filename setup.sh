#!/usr/bin/env bash
# setup.sh — bootstrap common-agent-skills on a new machine
#
# Run once after cloning the repo:
#   git clone git@github.com:hheydaroff/common-agent-skills ~/development/common-agent-skills
#   bash ~/development/common-agent-skills/setup.sh

set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

# Colours
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
DIM='\033[2m'
BOLD='\033[1m'
RESET='\033[0m'

ok()   { echo -e "${GREEN}✓${RESET} $*"; }
warn() { echo -e "${YELLOW}!${RESET} $*"; }
dim()  { echo -e "${DIM}$*${RESET}"; }
bold() { echo -e "${BOLD}$*${RESET}"; }

echo ""
bold "common-agent-skills setup"
dim  "repo: $REPO_DIR"
echo ""

# ── 1. Make scripts executable ─────────────────────────────────────────────────
chmod +x "$REPO_DIR/deploy.sh"
ok "deploy.sh is executable"

# ── 2. Create ~/.agents/skills/ if missing ────────────────────────────────────
if [ ! -d "$HOME/.agents/skills" ]; then
  mkdir -p "$HOME/.agents/skills"
  ok "created ~/.agents/skills/"
else
  ok "~/.agents/skills/ already exists"
fi

# ── 3. Run deploy to populate all tool directories ────────────────────────────
echo ""
dim "Running deploy..."
echo ""
bash "$REPO_DIR/deploy.sh"

# ── 4. Summary ────────────────────────────────────────────────────────────────
echo ""
bold "Setup complete."
echo ""
echo "Your skills are now live in:"
dim "  ~/.agents/skills/     ← Pi reads this natively"
dim "  ~/.claude/skills/     ← Claude Code"
dim "  ~/.codex/skills/      ← Codex (if installed)"
echo ""
echo "Workflow going forward:"
dim "  1. Edit skills in: $REPO_DIR/skills/"
dim "  2. Run: bash $REPO_DIR/deploy.sh"
dim "  3. Commit: git add -A && git commit -m '...' && git push"
echo ""
echo "To back up your skills:"
dim "  cd $REPO_DIR && git push"
echo ""
