---
name: ralph
description: Launch and manage an autonomous Ralph Loop in a separate terminal pane. Supports cmux and tmux — auto-detects the environment. Runs pi in a task-execution loop against a SPEC.md or tasks.json while the current session monitors progress. Use when user says "run ralph", "start ralph loop", "autonomous loop", "run tasks autonomously", "AFK mode", or wants pi to execute a task file unattended in a background terminal.
---

# Ralph Loop

Launch an autonomous pi loop in a dedicated terminal pane. Each iteration runs `pi -p` for one task with fresh context, then checks completion.

Supports **cmux** and **tmux** — auto-detects which is available.

## Prerequisites

- Running inside cmux OR tmux (at least one must be available)
- A task source file exists: `SPEC.md`, `tasks.json`, or user-specified file
- `pi` CLI available in PATH

## 1. Detect Environment

```bash
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

Write `ralph.sh` to the project directory, then execute it in the ralph pane:

```bash
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

  pi -p @"$SOURCE" @"$PROGRESS" "You are in a loop. Implement EXACTLY ONE task — the next incomplete task only. Do NOT continue to other tasks. Steps: 1) Identify the next incomplete task from progress.txt 2) Implement it 3) Verify it works 4) Commit 5) Update progress.txt marking ONLY that task as DONE. If this was the LAST task (all are now DONE), also add RALPH_COMPLETE as the final line. STOP after updating progress.txt."

  if grep -q "RALPH_COMPLETE" "$PROGRESS" 2>/dev/null; then
    echo ""
    echo "✅ All tasks complete after $i iterations!"
    exit 0
  fi

  sleep 3
done

echo "🛑 Max iterations ($MAX) reached"
exit 1
```

**Key details:**
- `@SPEC.md` and `@progress.txt` are separate arguments to `pi -p`, NOT inside the prompt string
- Completion is detected by grepping `progress.txt` for `RALPH_COMPLETE`
- The prompt is strict: EXACTLY ONE task per iteration, fresh context each time

### Send to cmux

```bash
cmux send --surface surface:<N> "cd $(pwd) && ./ralph.sh 20 SPEC.md"
cmux send-key --surface surface:<N> enter
```

### Send to tmux

```bash
tmux send-keys -t %<N> "cd $(pwd) && ./ralph.sh 20 SPEC.md" Enter
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
3. Write `ralph.sh` to the project
4. Spawn a new terminal pane to the right, rename it
5. Send `./ralph.sh 15 SPEC.md` to the pane
6. Confirm: "Ralph is running in the right pane. I'll check progress.txt periodically."

## Tips

**DO:**
- Always write the script file first, then execute it (avoids shell quoting issues)
- Store the surface/pane ID for monitoring later
- Use `read-screen` or `cat progress.txt` to check status

**DON'T:**
- Send the loop as a one-liner via cmux send (quoting will break)
- Run ralph in the current terminal (defeats the purpose)
- Leave a stuck ralph running without telling the user
