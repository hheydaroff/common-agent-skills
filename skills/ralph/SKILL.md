---
name: ralph
description: Launch and manage an autonomous Ralph Loop in a separate terminal pane. Supports cmux and tmux — auto-detects the environment. Runs pi in a task-execution loop against a SPEC.md or tasks.json while the current session monitors progress. Use when user says "run ralph", "start ralph loop", "autonomous loop", "run tasks autonomously", "AFK mode", or wants pi to execute a task file unattended in a background terminal.
---

# Ralph Loop

Launch an autonomous pi loop in a dedicated terminal pane. The current session spawns and monitors the loop — checking progress, reporting status, and intervening if needed.

Supports **cmux** and **tmux** — auto-detects which is available.

## Prerequisites

- Running inside cmux OR tmux (at least one must be available)
- A task source file exists: `SPEC.md`, `tasks.json`, or user-specified file
- `pi` CLI available in PATH

## 1. Detect Environment

```bash
# Check cmux first (preferred)
if cmux identify --json 2>/dev/null; then
  MUX="cmux"
# Then tmux
elif [ -n "$TMUX" ]; then
  MUX="tmux"
else
  echo "❌ No terminal multiplexer detected (need cmux or tmux)"
  # Ask user to start one
fi
```

## 2. Locate Task File

```bash
# Auto-detect source file
if [ -f "SPEC.md" ]; then
  SOURCE="SPEC.md"
elif [ -f "tasks.json" ]; then
  SOURCE="tasks.json"
elif [ -f "PRD.md" ]; then
  SOURCE="PRD.md"
else
  # Ask user which file to use
  echo "No task file found"
fi
```

## 3. Spawn Ralph Terminal

### cmux

```bash
# Create a right-side split
cmux new-pane --type terminal --direction right
# Output: { "pane": "pane:3", "surface": "surface:5" }

# Rename for clarity
cmux rename-tab --surface surface:<N> "🤖 Ralph"
```

### tmux

```bash
# Create a right-side split (horizontal split = side by side)
tmux split-window -h -d -P -F '#{pane_id}'
# Output: %<N> (pane ID)

# Optionally name it
tmux select-pane -t %<N> -T "🤖 Ralph"
```

## 4. Launch the Loop

Build the command (same for both multiplexers):

**IMPORTANT:**
- `pi -p` requires `@file` references as separate arguments before the prompt text
- Do NOT capture output with `result=$(...)` — let pi stream directly to the terminal so the user can see what's happening
- Check `progress.txt` for the completion marker after each iteration instead

```bash
RALPH_CMD="cd $(pwd) && RALPH_MAX=20 RALPH_SOURCE=$SOURCE bash -c '
PROGRESS=progress.txt
[[ ! -f \$RALPH_SOURCE ]] && echo \"❌ Missing: \$RALPH_SOURCE\" && exit 1
[[ ! -f \$PROGRESS ]] && touch \$PROGRESS
echo \"🤖 Ralph Loop | Max: \$RALPH_MAX | Source: \$RALPH_SOURCE\"
for ((i=1; i<=\$RALPH_MAX; i++)); do
  echo \"\"
  echo \"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\"
  echo \"🔄 [\$i/\$RALPH_MAX] Running...\"
  echo \"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\"
  pi -p @\$RALPH_SOURCE @\$PROGRESS \"Find the next incomplete task and implement it. Verify it works. Commit your changes. Update progress.txt marking the task DONE. ONLY ONE TASK. If all tasks are done, write RALPH_COMPLETE to progress.txt.\"
  if grep -q \"RALPH_COMPLETE\" \$PROGRESS 2>/dev/null; then
    echo \"\"
    echo \"✅ All tasks complete after \$i iterations\"
    exit 0
  fi
  sleep 3
done
echo \"🛑 Max iterations reached\"
'"
```

**Key details:**
- `pi -p` output streams live to the terminal — user sees tool calls, edits, test runs in real time
- `@SPEC.md` and `@progress.txt` are separate arguments to `pi -p`, NOT inside the prompt string
- Completion is detected by grepping `progress.txt` for `RALPH_COMPLETE` (pi writes it when all tasks done)
- No output capture (`$()`) — that's what hides the live output

### Send to cmux

```bash
cmux send --surface surface:<N> "$RALPH_CMD"
cmux send-key --surface surface:<N> enter
```

### Send to tmux

```bash
tmux send-keys -t %<N> "$RALPH_CMD" Enter
```

## 5. Monitor Progress

### cmux

```bash
# Read terminal output
cmux read-screen --surface surface:<N> --lines 30

# Check progress file
cat progress.txt
```

### tmux

```bash
# Capture pane output
tmux capture-pane -t %<N> -p -S -30

# Check progress file
cat progress.txt
```

**Monitoring cadence:**
- Check every 30-60 seconds during active execution
- Report to user: which task is running, how many completed
- Alert if errors appear in the terminal output

## 6. Report Status

When user asks "how's ralph doing?" or similar:

1. Read the ralph terminal screen (method depends on MUX)
2. Read `progress.txt`
3. Summarize: tasks completed, current task, any errors

## 7. Intervene if Needed

### cmux

```bash
cmux send-key --surface surface:<N> ctrl+c
```

### tmux

```bash
tmux send-keys -t %<N> C-c
```

## 8. Completion

### cmux

```bash
cmux trigger-flash --surface surface:<N>
cmux notify --title "🤖 Ralph Complete" --body "All tasks finished"
```

### tmux

```bash
tmux display-message "🤖 Ralph Complete — all tasks finished"
# Optionally highlight the pane
tmux select-pane -t %<N>
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
3. Spawn a new terminal pane to the right
4. Send the loop script with MAX=15, SOURCE=SPEC.md
5. Confirm: "Ralph is running in the right pane. I'll monitor progress.txt and check in periodically."
6. Periodically read screen + progress.txt, report back
7. Notify when done

## Tips

**DO:**
- Always detect the multiplexer first
- Store the pane/surface ID for the session so you can monitor later
- Read the screen to check for errors without interrupting
- Notify/flash when done so user notices
- Offer to show progress when user checks in

**DON'T:**
- Run ralph in the current terminal (defeats the purpose)
- Forget to press enter after sending the command
- Poll too aggressively (every 5s) — wastes resources
- Leave a stuck ralph running without telling the user
- Assume cmux — always check and fall back to tmux
