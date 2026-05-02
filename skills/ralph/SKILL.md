---
name: ralph
description: Launch and manage an autonomous Ralph Loop in a separate terminal pane. Supports cmux and tmux — auto-detects the environment. Runs pi with full TUI visibility per task, auto-exits between iterations for fresh context. Use when user says "run ralph", "start ralph loop", "autonomous loop", "run tasks autonomously", "AFK mode", or wants pi to execute a task file unattended in a background terminal.
---

# Ralph Loop

Launch an autonomous pi loop in a dedicated terminal pane. Each iteration shows the **full pi TUI** (tool calls, diffs, bash output) and auto-exits when done, giving fresh context per task.

Supports **cmux** and **tmux** — auto-detects which is available.

## Prerequisites

- Running inside cmux OR tmux (at least one must be available)
- A task source file exists: `SPEC.md`, `tasks.json`, or user-specified file
- `pi` CLI available in PATH

## How It Works

1. Background watcher monitors `progress.txt` for changes
2. `pi` runs interactively (full TUI) with the task prompt
3. When pi updates `progress.txt` (task done), watcher sends `/exit`
4. Pi exits cleanly, loop checks for completion, starts next iteration

This gives: **full TUI visibility + fresh context per task + automatic progression**.

## 1. Detect Environment

```bash
# Check cmux first (preferred)
if cmux identify --json 2>/dev/null; then
  MUX="cmux"
elif [ -n "$TMUX" ]; then
  MUX="tmux"
else
  echo "❌ No terminal multiplexer detected (need cmux or tmux)"
fi
```

## 2. Locate Task File

```bash
if [ -f "SPEC.md" ]; then
  SOURCE="SPEC.md"
elif [ -f "tasks.json" ]; then
  SOURCE="tasks.json"
elif [ -f "PRD.md" ]; then
  SOURCE="PRD.md"
fi
```

## 3. Spawn Ralph Terminal

### cmux

```bash
cmux new-pane --type terminal --direction right
# Output: OK surface:<N> pane:<N> workspace:<N>

cmux rename-tab --surface surface:<N> "🤖 Ralph"
```

### tmux

```bash
tmux split-window -h -d -P -F '#{pane_id}'
# Output: %<N>

tmux select-pane -t %<N> -T "🤖 Ralph"
```

## 4. Write and Launch the Loop Script

Write `ralph-tui.sh` to the project directory, then execute it in the ralph pane:

```bash
#!/bin/bash
# ralph-tui.sh - Ralph loop with full pi TUI + auto-exit
# Each iteration runs ONE task in a fresh pi session with full TUI visibility.
# Usage: ./ralph-tui.sh [max_iterations] [source_file]

set -e

MAX=${1:-20}
SOURCE=${2:-SPEC.md}
PROGRESS="progress.txt"

# Detect surface for self-exit
if command -v cmux &>/dev/null && cmux identify --json &>/dev/null; then
  SURFACE=$(cmux identify --json | python3 -c "import sys,json; print(json.load(sys.stdin)['caller']['surface_ref'])")
  MUX="cmux"
elif [ -n "$TMUX" ]; then
  PANE_ID=$(tmux display-message -p '#{pane_id}')
  MUX="tmux"
else
  echo "❌ Need cmux or tmux for auto-exit TUI mode"
  exit 1
fi

[[ ! -f "$SOURCE" ]] && echo "❌ Missing: $SOURCE" && exit 1
[[ ! -f "$PROGRESS" ]] && touch "$PROGRESS"

echo "🤖 Ralph Loop | Max: $MAX | Source: $SOURCE | MUX: $MUX"
echo ""

send_exit() {
  sleep 2
  if [ "$MUX" = "cmux" ]; then
    cmux send --surface "$SURFACE" "/exit"
    cmux send-key --surface "$SURFACE" enter
  else
    tmux send-keys -t "$PANE_ID" "/exit" Enter
  fi
}

for ((i=1; i<=MAX; i++)); do
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "🔄 [$i/$MAX] Starting task..."
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  # Snapshot progress before pi runs
  PREV=$(cat "$PROGRESS")

  # Background watcher: when progress.txt changes, send /exit to pi
  (
    while true; do
      sleep 3
      CURR=$(cat "$PROGRESS" 2>/dev/null)
      if [ "$CURR" != "$PREV" ]; then
        send_exit
        break
      fi
    done
  ) &
  WATCHER=$!

  # Run pi interactively (full TUI) with STRICT single-task prompt
  pi @"$SOURCE" @"$PROGRESS" "You are in a loop. Implement EXACTLY ONE task — the next incomplete task only. Do NOT continue to other tasks. Steps: 1) Identify the next incomplete task from progress.txt 2) Implement it 3) Verify it works 4) Commit 5) Update progress.txt marking ONLY that task as DONE. If this was the LAST task (all are now DONE), also add RALPH_COMPLETE as the final line. STOP after updating progress.txt. Do NOT proceed to any other task."

  # Clean up watcher (|| true prevents set -e from killing the loop)
  kill $WATCHER 2>/dev/null || true
  wait $WATCHER 2>/dev/null || true

  # Check if all done
  if grep -q "RALPH_COMPLETE" "$PROGRESS" 2>/dev/null; then
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "✅ All tasks complete after $i iterations!"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    exit 0
  fi

  sleep 2
done

echo "🛑 Max iterations ($MAX) reached"
exit 1
```
  fi

  sleep 2
done

echo "🛑 Max iterations ($MAX) reached"
exit 1
```

### Send to cmux

```bash
cmux send --surface surface:<N> "cd $(pwd) && ./ralph-tui.sh 20 SPEC.md"
cmux send-key --surface surface:<N> enter
```

### Send to tmux

```bash
tmux send-keys -t %<N> "cd $(pwd) && ./ralph-tui.sh 20 SPEC.md" Enter
```

## 5. Monitor Progress

### cmux

```bash
cmux read-screen --surface surface:<N> --lines 30
cat progress.txt
```

### tmux

```bash
tmux capture-pane -t %<N> -p -S -30
cat progress.txt
```

## 6. Intervene if Needed

### cmux

```bash
cmux send-key --surface surface:<N> ctrl+c
```

### tmux

```bash
tmux send-keys -t %<N> C-c
```

## 7. Completion

### cmux

```bash
cmux trigger-flash --surface surface:<N>
cmux notify --title "🤖 Ralph Complete" --body "All tasks finished"
```

### tmux

```bash
tmux display-message "🤖 Ralph Complete — all tasks finished"
```

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| Source file | Auto-detect (`SPEC.md` > `tasks.json` > `PRD.md`) | Task definition file |
| Max iterations | 20 | Loop cap to prevent runaway |
| Direction | right | Split direction for new pane |

## Example Interaction

User: "run ralph on SPEC.md with 15 iterations"

1. Detect multiplexer (cmux or tmux)
2. Verify task file exists
3. Write `ralph-tui.sh` to the project
4. Spawn a new terminal pane to the right, rename it
5. Send `./ralph-tui.sh 15 SPEC.md` to the pane
6. Confirm: "Ralph is running in the right pane. Full TUI visible — you can watch tool calls, diffs, and commits live. I'll check in periodically."

## Tips

**DO:**
- Always write the script file first, then execute it (avoids shell quoting hell)
- Store the surface/pane ID for monitoring later
- Use `read-screen` to check for errors without interrupting
- Notify/flash when done so user notices

**DON'T:**
- Send the loop as a one-liner via cmux send (quoting will break)
- Run ralph in the current terminal (defeats the purpose)
- Poll too aggressively from the managing session
- Leave a stuck ralph running without telling the user
