#!/bin/bash
# ralph.sh - Autonomous task loop for pi
# Usage: ./ralph.sh [max_iterations] [source_file]

set -e

MAX=${1:-20}
SOURCE=${2:-SPEC.md}
PROGRESS="progress.txt"

[[ ! -f "$SOURCE" ]] && echo "❌ Missing: $SOURCE" && exit 1
[[ ! -f "$PROGRESS" ]] && touch "$PROGRESS"

echo "🤖 Ralph Loop | Max: $MAX | Source: $SOURCE"

for ((i=1; i<=MAX; i++)); do
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "🔄 [$i/$MAX] Running..."
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  # Gather recent git history for context on what's already been done
  RECENT_COMMITS=$(git log --oneline -5 2>/dev/null || echo "(no commits yet)")

  pi -p @"$SOURCE" @"$PROGRESS" "You are in a loop. Here are the last 5 commits for context on what's already been done:

$RECENT_COMMITS

Implement EXACTLY ONE task — the next incomplete task only. Do NOT continue to other tasks. Steps: 1) Identify the next incomplete task from progress.txt 2) Implement it 3) Verify it works 4) Commit 5) Update progress.txt marking ONLY that task as DONE. If this was the LAST task (all are now DONE), also add RALPH_COMPLETE as the final line. STOP after updating progress.txt."

  if grep -q "RALPH_COMPLETE" "$PROGRESS" 2>/dev/null; then
    echo ""
    echo "✅ All tasks complete after $i iterations!"
    exit 0
  fi

  sleep 3
done

echo "🛑 Max iterations ($MAX) reached"
exit 1
