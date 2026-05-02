---
name: ralph-loop
description: Launch and manage an autonomous Ralph Loop in a separate cmux terminal pane. Runs pi in a task-execution loop against a SPEC.md or tasks.json while the current session monitors progress. Use when user says "run ralph", "start ralph loop", "autonomous loop", "run tasks autonomously", "AFK mode", or wants pi to execute a task file unattended in a background terminal.
---

# Ralph Loop (cmux-managed)

Launch an autonomous pi loop in a dedicated cmux terminal pane. The current session spawns and monitors the loop — checking progress, reporting status, and intervening if needed.

## Prerequisites

- Running inside cmux (verify with `cmux identify --json`)
- A task source file exists: `SPEC.md`, `tasks.json`, or user-specified file
- `pi` CLI available in PATH

## Process

### 1. Verify Environment

```bash
# Confirm we're in cmux
cmux identify --json

# Confirm task file exists
ls SPEC.md tasks.json 2>/dev/null
```

If no task file found, ask the user which file to use.

### 2. Spawn Ralph Terminal

Create a new split pane for the ralph loop:

```bash
# Create a right-side split for ralph
cmux new-pane --type terminal --direction right

# Note the new surface ID from output
# Example output: { "pane": "pane:3", "surface": "surface:5" }
```

Rename the tab for clarity:

```bash
cmux rename-tab --surface surface:<N> "🤖 Ralph Loop"
```

### 3. Launch the Loop

Send the ralph command to the new surface. Use the inline script — do NOT depend on ralph.sh existing in the project:

```bash
cmux send --surface surface:<N> "cd $(pwd) && RALPH_MAX=20 RALPH_SOURCE=SPEC.md bash -c '
PROGRESS=progress.txt
[[ ! -f \$RALPH_SOURCE ]] && echo \"❌ Missing: \$RALPH_SOURCE\" && exit 1
[[ ! -f \$PROGRESS ]] && touch \$PROGRESS
echo \"🤖 Ralph Loop | Max: \$RALPH_MAX | Source: \$RALPH_SOURCE\"
for ((i=1; i<=\$RALPH_MAX; i++)); do
  echo \"🔄 [\$i/\$RALPH_MAX] Running...\"
  result=\$(pi -p \"@\$RALPH_SOURCE @\$PROGRESS
1. Find the next incomplete task and implement it.
2. Verify it works.
3. Commit your changes.
4. Update progress.txt.
ONLY ONE TASK.
If all done, output <promise>COMPLETE</promise>.\")
  echo \"\$result\"
  if [[ \"\$result\" == *\"<promise>COMPLETE</promise>\"* ]]; then
    echo \"✅ Complete after \$i iterations\"
    exit 0
  fi
  sleep 3
done
echo \"🛑 Max iterations reached\"
'"
```

Then press Enter:

```bash
cmux send-key --surface surface:<N> enter
```

### 4. Monitor Progress

Periodically check on the ralph terminal:

```bash
# Read the terminal output
cmux read-screen --surface surface:<N> --lines 30

# Check progress.txt for task completion status
cat progress.txt
```

**Monitoring cadence:**
- Check every 30-60 seconds during active execution
- Report to user: which task is running, how many completed
- Alert user if errors appear in the terminal output

### 5. Report Status

When user asks "how's ralph doing?" or similar:

1. Read the ralph terminal screen
2. Read progress.txt
3. Summarize: tasks completed, current task, any errors

### 6. Intervene if Needed

If ralph gets stuck or errors out:

```bash
# Send Ctrl+C to stop
cmux send-key --surface surface:<N> ctrl+c

# Optionally restart with adjusted parameters
```

### 7. Cleanup

When ralph completes or user says stop:

```bash
# Flash the surface to get attention
cmux trigger-flash --surface surface:<N>

# Notify
cmux notify --title "🤖 Ralph Complete" --body "All tasks finished" --surface surface:<N>
```

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| Source file | `SPEC.md` or `tasks.json` (whichever exists) | Task definition file |
| Max iterations | 20 | Loop cap to prevent runaway |
| Direction | right | Split direction for new pane |

If user specifies these, adjust accordingly.

## Example Interaction

User: "run ralph on SPEC.md with 15 iterations"

1. Verify cmux + file existence
2. `cmux new-pane --type terminal --direction right` → get surface ID
3. `cmux rename-tab --surface surface:N "🤖 Ralph Loop"`
4. Send the loop script targeting SPEC.md with MAX=15
5. Confirm to user: "Ralph is running in the right pane (surface:N). I'll monitor progress.txt and check in periodically."
6. Periodically read screen + progress.txt, report back

## Tips

**DO:**
- Always verify cmux context first
- Store the surface ID for the session so you can monitor later
- Use `read-screen` to check for errors without interrupting
- Flash + notify when done so user notices
- Offer to show progress when user checks in

**DON'T:**
- Run ralph in the current terminal (defeats the purpose)
- Forget to press enter after sending the command
- Poll too aggressively (every 5s) — wastes resources
- Leave a stuck ralph running without telling the user
