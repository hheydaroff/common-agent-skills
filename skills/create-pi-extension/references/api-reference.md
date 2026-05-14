# Pi Extension API Reference

Complete API surface for pi extensions.

## Imports

```typescript
import type { ExtensionAPI, ExtensionContext } from "@earendil-works/pi-coding-agent";
import { Type } from "@sinclair/typebox";
import { StringEnum } from "@earendil-works/pi-ai";
import { Text } from "@earendil-works/pi-tui";
import {
  truncateHead, truncateTail, truncateLine,
  formatSize, DEFAULT_MAX_BYTES, DEFAULT_MAX_LINES,
  isToolCallEventType, isBashToolResult,
  createBashTool, createReadTool,
} from "@earendil-works/pi-coding-agent";
```

---

## ExtensionAPI (`pi`)

### pi.registerTool(definition)

Register a tool the LLM can call.

```typescript
pi.registerTool({
  name: "my_tool",           // snake_case, matches function call name
  label: "My Tool",          // shown in TUI header
  description: "...",        // shown to LLM in system prompt
  promptSnippet: "...",      // optional short override for system prompt entry
  promptGuidelines: ["..."], // optional bullets added to Guidelines section
  parameters: Type.Object({
    action: StringEnum(["list", "add"] as const),  // ALWAYS use StringEnum for enums
    text: Type.Optional(Type.String()),
  }),

  async execute(toolCallId, params, signal, onUpdate, ctx) {
    // Check cancellation
    if (signal?.aborted) return { content: [{ type: "text", text: "Cancelled" }] };

    // Stream progress
    onUpdate?.({ content: [{ type: "text", text: "Working..." }] });

    // Throw to signal errors (sets isError=true, reported to LLM)
    if (!params.text) throw new Error("text required");

    return {
      content: [{ type: "text", text: "Result text for LLM" }],
      details: { /* arbitrary data for rendering & state reconstruction */ },
    };
  },

  // Optional custom TUI rendering
  renderCall(args, theme) { return new Text("...", 0, 0); },
  renderResult(result, { expanded, isPartial }, theme) { return new Text("...", 0, 0); },
});
```

### pi.registerCommand(name, options)

Register a slash command (`/name`).

```typescript
pi.registerCommand("my-cmd", {
  description: "What it does",
  getArgumentCompletions: (prefix) => [{ value: "dev", label: "dev" }],
  handler: async (args, ctx) => {
    // ctx is ExtensionCommandContext (extends ExtensionContext)
    ctx.ui.notify("Done", "info");
  },
});
```

`ExtensionCommandContext` extras (only in commands, not event handlers):
- `ctx.waitForIdle()` — wait for agent to finish streaming
- `ctx.newSession(options?)` — create a new session
- `ctx.fork(entryId)` — fork from a specific entry
- `ctx.navigateTree(targetId, options?)` — jump to a tree node
- `ctx.reload()` — reload all extensions, skills, prompts

### pi.on(event, handler)

Subscribe to lifecycle events. See **Events** section below.

### pi.registerShortcut(shortcut, options)

```typescript
pi.registerShortcut("ctrl+shift+p", {
  description: "Toggle something",
  handler: async (ctx) => { ctx.ui.notify("Toggled!", "info"); },
});
```

### pi.registerFlag(name, options)

Register a CLI flag, then read with `pi.getFlag("--name")`.

```typescript
pi.registerFlag("verbose", { description: "Enable verbose mode", type: "boolean", default: false });
if (pi.getFlag("--verbose")) { /* ... */ }
```

### pi.sendMessage(message, options?)

Inject a custom (non-user) message.

```typescript
pi.sendMessage(
  { customType: "my-ext", content: "Status", display: true, details: {} },
  { deliverAs: "followUp", triggerTurn: false }
);
// deliverAs: "steer" | "followUp" | "nextTurn"
```

### pi.sendUserMessage(content, options?)

Send a user message as if typed.

```typescript
pi.sendUserMessage("Summarize the last change");
pi.sendUserMessage("Focus on errors", { deliverAs: "steer" }); // during streaming
```

### pi.exec(command, args, options?)

Run a shell command.

```typescript
const result = await pi.exec("git", ["status"], { signal, timeout: 5000 });
// result.stdout, result.stderr, result.code, result.killed
```

### pi.getActiveTools() / pi.getAllTools() / pi.setActiveTools(names)

```typescript
const active = pi.getActiveTools();       // ["read", "bash", ...]
const all    = pi.getAllTools();           // [{ name, description }, ...]
pi.setActiveTools(["read", "bash"]);      // restrict to read-only
```

### pi.appendEntry(customType, data?)

Persist extension state that survives reload (not in LLM context).

```typescript
pi.appendEntry("my-ext-state", { count: 42 });
```

### pi.setModel(model) / pi.getThinkingLevel() / pi.setThinkingLevel(level)

```typescript
const model = ctx.modelRegistry.find("anthropic", "claude-sonnet-4-5");
if (model) await pi.setModel(model);
pi.setThinkingLevel("high"); // "off" | "minimal" | "low" | "medium" | "high" | "xhigh"
```

### pi.registerProvider(name, config) / pi.unregisterProvider(name)

Register a custom or proxy model provider.

```typescript
pi.registerProvider("my-proxy", {
  baseUrl: "https://proxy.example.com",
  apiKey: "MY_API_KEY",
  api: "anthropic-messages",
  models: [{ id: "claude-sonnet-4-20250514", name: "Claude Sonnet (proxy)", ... }],
});
```

### pi.registerMessageRenderer(customType, renderer)

Custom TUI renderer for messages sent via `pi.sendMessage()`.

```typescript
pi.registerMessageRenderer("my-ext", (message, { expanded }, theme) => {
  return new Text(theme.fg("accent", message.content), 0, 0);
});
```

### pi.events

Shared event bus between extensions.

```typescript
pi.events.on("my:event", (data) => { /* ... */ });
pi.events.emit("my:event", { payload: 42 });
```

### pi.getCommands()

Get all slash commands (extensions + templates + skills).

```typescript
const cmds = pi.getCommands();
// [{ name, description, source: "extension"|"prompt"|"skill", path? }]
```

---

## Events

### Lifecycle

| Event | When | Can return |
|---|---|---|
| `session_start` | Session loads | — |
| `session_switch` | User navigates to a different session | — |
| `session_fork` | Session forked | — |
| `session_tree` | Branch navigation inside current session | — |
| `session_shutdown` | Session ends | — |
| `before_agent_start` | Before LLM turn starts | `{ systemPrompt }` |
| `agent_start` | LLM response starts streaming | — |
| `turn_end` | LLM turn finishes | — |

#### before_agent_start — modify system prompt

```typescript
pi.on("before_agent_start", async (event) => {
  return { systemPrompt: event.systemPrompt + "\n\nExtra instructions." };
});
```

### Tool Events

#### tool_call — intercept before execution (can block)

```typescript
import { isToolCallEventType } from "@earendil-works/pi-coding-agent";

pi.on("tool_call", async (event, ctx) => {
  if (isToolCallEventType("bash", event)) {
    if (event.input.command.includes("rm -rf /")) {
      return { block: true, reason: "Refusing to delete root" };
    }
  }
});
```

#### tool_result — modify result after execution

```typescript
pi.on("tool_result", async (event, ctx) => {
  // Can return partial patch: { content?, details?, isError? }
  return { content: [{ type: "text", text: "Modified: " + event.content[0]?.text }] };
});
```

### Input Event

```typescript
pi.on("input", async (event, ctx) => {
  // event.text, event.images, event.source ("interactive"|"rpc"|"extension")

  // Transform before expansion
  if (event.text.startsWith("?q "))
    return { action: "transform", text: `Answer briefly: ${event.text.slice(3)}` };

  // Handle without agent
  if (event.text === "ping") {
    ctx.ui.notify("pong", "info");
    return { action: "handled" };
  }

  return { action: "continue" };
});
```

### Model Event

```typescript
pi.on("model_select", (event, ctx) => {
  const next = `${event.model.provider}/${event.model.id}`;
  ctx.ui.setStatus("model", next);
});
```

### Session Guard Events

```typescript
pi.on("session_before_switch", async (event, ctx) => {
  const ok = await ctx.ui.confirm("Switch session?", "Unsaved work will be lost");
  if (!ok) return { cancel: true };
});
// Also: session_before_fork, session_before_compact, session_before_tree
```

### User Bash Event

```typescript
pi.on("user_bash", (event, ctx) => {
  // event.command, event.excludeFromContext, event.cwd
  // return { operations } or { result }
});
```

---

## ExtensionContext (`ctx`)

Available in all event handlers and tool execute functions.

```typescript
ctx.ui           // UI methods (see below)
ctx.hasUI        // false in print/JSON mode
ctx.cwd          // current working directory
ctx.sessionManager.getEntries()    // all session entries
ctx.sessionManager.getBranch()     // current branch entries
ctx.sessionManager.getLeafId()     // current leaf entry ID
ctx.modelRegistry                  // access to registered models
ctx.model                          // current active model
ctx.isIdle()                       // is agent idle?
ctx.abort()                        // abort current agent turn
ctx.getContextUsage()              // { tokens, maxTokens } or null
ctx.compact(options?)              // trigger compaction
ctx.getSystemPrompt()              // current system prompt
ctx.shutdown()                     // graceful shutdown
```

---

## ctx.ui Methods

```typescript
// Notifications (non-blocking)
ctx.ui.notify("Message", "info");         // "info" | "warning" | "error"

// Dialogs (blocking, await them)
const choice = await ctx.ui.select("Pick:", ["A", "B", "C"]);       // string | undefined
const ok     = await ctx.ui.confirm("Delete?", "Cannot be undone"); // boolean
const name   = await ctx.ui.input("Enter name:", "placeholder");    // string | undefined
const text   = await ctx.ui.editor("Edit text:", "prefill");        // string | undefined

// Dialogs with timeout
const ok = await ctx.ui.confirm("Continue?", "Auto-cancels in 5s", { timeout: 5000 });

// Status bar
ctx.ui.setStatus("my-ext", "Processing...");
ctx.ui.setStatus("my-ext", undefined);  // clear

// Widgets
ctx.ui.setWidget("my-widget", ["Line 1", "Line 2"]);               // above editor
ctx.ui.setWidget("my-widget", ["Line 1"], { placement: "belowEditor" });
ctx.ui.setWidget("my-widget", undefined);                           // clear
ctx.ui.setWidget("my-widget", (tui, theme) => new Text("...", 0, 0));

// Editor
ctx.ui.setEditorText("Prefill the editor");
const current = ctx.ui.getEditorText();
ctx.ui.pasteToEditor("paste content");

// Working message during streaming
ctx.ui.setWorkingMessage("Thinking deeply...");
ctx.ui.setWorkingMessage();  // restore default

// Terminal title
ctx.ui.setTitle("pi - my project");

// Theme
const themes = ctx.ui.getAllThemes();
ctx.ui.setTheme("light");

// Custom component (replaces editor until done() called)
const result = await ctx.ui.custom<boolean>((tui, theme, keybindings, done) => {
  const text = new Text("Press Enter or Escape", 1, 1);
  text.onKey = (key) => {
    if (key === "return")  done(true);
    if (key === "escape")  done(false);
    return true;
  };
  return text;
});
```

---

## Output Truncation (Required for large output)

```typescript
import {
  truncateHead, truncateTail, formatSize,
  DEFAULT_MAX_BYTES, DEFAULT_MAX_LINES,
} from "@earendil-works/pi-coding-agent";

async execute(toolCallId, params, signal, onUpdate, ctx) {
  const raw = await runSomethingThatProducesLotsOfOutput();

  const truncation = truncateHead(raw, {
    maxLines: DEFAULT_MAX_LINES,  // 2000
    maxBytes: DEFAULT_MAX_BYTES,  // 50 KB
  });

  let output = truncation.content;
  if (truncation.truncated) {
    output += `\n\n[Truncated: showed ${truncation.outputLines}/${truncation.totalLines} lines `
            + `(${formatSize(truncation.outputBytes)} of ${formatSize(truncation.totalBytes)})]`;
  }

  return { content: [{ type: "text", text: output }] };
}
```

Use `truncateHead` when the beginning matters (search results, file reads).  
Use `truncateTail` when the end matters (logs, command output).

---

## Session Entry Types

```typescript
for (const entry of ctx.sessionManager.getBranch()) {
  if (entry.type === "message") {
    const msg = entry.message;
    if (msg.role === "toolResult" && msg.toolName === "my_tool") {
      const state = msg.details?.myState;
    }
  }
}
```

Entry types: `"message"`, `"custom"`, `"summary"`, `"branch-summary"`, `"label"`.

---

## Package Extension (with npm deps)

For complex extensions, create a directory with `package.json`:

```
my-extension/
├── package.json
├── tsconfig.json        # optional
└── index.ts             # export default function(pi)
```

```json
{
  "name": "my-extension",
  "version": "1.0.0",
  "main": "index.ts",
  "dependencies": {
    "@sinclair/typebox": "^0.34.0"
  }
}
```

Run `npm install` in the directory, then load with:

```bash
pi --extension ./my-extension/
```

---

## Official Examples

Located at:
```
/opt/homebrew/lib/node_modules/@earendil-works/pi-coding-agent/examples/extensions/
```

| File | What it shows |
|---|---|
| `hello.ts` | Minimal tool |
| `pirate.ts` | System prompt injection via command |
| `todo.ts` | Stateful tool + custom rendering + command |
| `permission-gate.ts` | Block tool calls with confirm dialog |
| `protected-paths.ts` | Block writes to paths |
| `status-line.ts` | Footer status indicator |
| `model-status.ts` | React to model changes |
| `input-transform.ts` | Transform user input |
| `dynamic-tools.ts` | Register tools after startup |
| `truncated-tool.ts` | Output truncation with ripgrep |
| `tool-override.ts` | Override built-in `read` tool |
| `ssh.ts` | Remote execution via SSH |
| `plan-mode/` | Full plan-mode implementation |
| `with-deps/` | Package extension with npm deps |
