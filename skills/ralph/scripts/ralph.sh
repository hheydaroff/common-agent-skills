#!/bin/bash
# ralph.sh - Autonomous task loop for pi
# Usage: ./ralph.sh [max_iterations] [source_file]

set -e

MAX=${1:-20}
SOURCE=${2:-SPEC.md}
PROGRESS="progress.txt"
TASK_TIMEOUT=${RALPH_TIMEOUT:-900}  # 15 minutes (in seconds), override with RALPH_TIMEOUT env var
MAX_RETRIES=${RALPH_RETRIES:-3}     # Max retries per task on timeout

[[ ! -f "$SOURCE" ]] && echo "❌ Missing: $SOURCE" && exit 1
[[ ! -f "$PROGRESS" ]] && touch "$PROGRESS"

echo "🤖 Ralph Loop | Max: $MAX | Source: $SOURCE | Timeout: ${TASK_TIMEOUT}s | Retries: $MAX_RETRIES"

# Run pi with timeout. Returns 0 on success, 1 on timeout.
run_with_timeout() {
  local pid
  local exit_code

  # Run pi in background
  pi -p @"$SOURCE" @"$PROGRESS" "$1" &
  pid=$!

  # Watchdog: wait up to TASK_TIMEOUT seconds
  local elapsed=0
  while kill -0 "$pid" 2>/dev/null; do
    if (( elapsed >= TASK_TIMEOUT )); then
      echo ""
      echo "⏰ TIMEOUT after ${TASK_TIMEOUT}s — killing task (PID: $pid)"
      kill -TERM "$pid" 2>/dev/null
      sleep 2
      kill -9 "$pid" 2>/dev/null
      wait "$pid" 2>/dev/null
      return 1
    fi
    sleep 5
    elapsed=$((elapsed + 5))
  done

  wait "$pid"
  exit_code=$?
  return $exit_code
}

for ((i=1; i<=MAX; i++)); do
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "🔄 [$i/$MAX] Running..."
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  # Gather recent git history for context on what's already been done
  RECENT_COMMITS=$(git log --oneline -5 2>/dev/null || echo "(no commits yet)")

  PROMPT="You are in a loop. Here are the last 5 commits for context on what's already been done:

$RECENT_COMMITS

Implement EXACTLY ONE task — the next incomplete task only. Do NOT continue to other tasks. Steps: 1) Identify the next incomplete task from progress.txt 2) Implement it 3) Verify it works 4) Commit 5) Update progress.txt marking ONLY that task as DONE. If this was the LAST task (all are now DONE), also add RALPH_COMPLETE as the final line. STOP after updating progress.txt."

  # Attempt the task with retries on timeout
  attempt=0
  task_succeeded=false
  while (( attempt <= MAX_RETRIES )); do
    if (( attempt > 0 )); then
      echo "🔁 Retry $attempt/$MAX_RETRIES (previous attempt timed out)"
    fi

    if run_with_timeout "$PROMPT"; then
      task_succeeded=true
      break
    else
      attempt=$((attempt + 1))
      if (( attempt > MAX_RETRIES )); then
        echo "❌ Task failed after $MAX_RETRIES retries (timeout). Skipping."
        echo "[ITERATION $i] TIMEOUT — task could not complete within ${TASK_TIMEOUT}s after $((MAX_RETRIES + 1)) attempts" >> "$PROGRESS"
      else
        sleep 5
      fi
    fi
  done

  if grep -q "RALPH_COMPLETE" "$PROGRESS" 2>/dev/null; then
    echo ""
    echo "✅ All tasks complete after $i iterations!"
    exit 0
  fi

  sleep 3
done

echo "🛑 Max iterations ($MAX) reached"
exit 1
