---
name: create-pi-extension
description: "Create pi coding-agent extensions (custom tools, slash commands, shortcuts, event handlers, system prompt mods, TUI rendering). Use when user wants to build, scaffold, modify, or debug a pi extension."
---

# Create Pi Extension

Pi extensions are TypeScript files (or npm packages) that hook into the agent lifecycle. They add custom tools the LLM can call, slash commands for the user, event handlers, UI widgets, and more.

## Where Extensions Live

| Location | Scope |
|---|---|
| `~/.pi/agent/extensions/` | Global — every session |
| `.pi/extensions/` in project | Project-scoped |
| `--extension <file>` CLI flag | One-off |
| `extensions` array in `settings.json` | Configured paths |

## Scaffolding a New Extension

Use the scaffold script to generate a ready-to-edit TypeScript file:

```bash
# Scaffold a single-file extension
bash <skill-dir>/scripts/scaffold.sh my-extension

# Scaffold a package extension (with package.json + tsconfig)
bash <skill-dir>/scripts/scaffold.sh my-extension --package
```

## Quick Start: Minimal Tool

```typescript
import { Type } from "@sinclair/typebox";
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

export default function (pi: ExtensionAPI) {
  pi.registerTool({
    name: "greet",
    label: "Greet",
    description: "Greet a person by name",
    parameters: Type.Object({
      name: Type.String({ description: "Person to greet" }),
    }),
    async execute(_id, params, _signal, _onUpdate, _ctx) {
      return {
        content: [{ type: "text", text: `Hello, ${params.name}!` }],
        details: { greeted: params.name },
      };
    },
  });
}
```

Save as `my-extension.ts` and run:

```bash
pi --extension ./my-extension.ts
```

## Extension Anatomy

Every extension exports a **default function** that receives `pi: ExtensionAPI`:

```typescript
export default function (pi: ExtensionAPI) {
  // Register tools, commands, events...
}
```

All setup happens synchronously inside this function (or inside async event handlers). The function runs once at startup.

## Key Building Blocks

### 1. Register a Tool (LLM-callable)

```typescript
import { Type } from "@sinclair/typebox";
import { StringEnum } from "@earendil-works/pi-ai";   // ← required for enums (Google compat)

pi.registerTool({
  name: "my_tool",          // snake_case
  label: "My Tool",         // Human-readable
  description: "Shown to the LLM — be specific",
  parameters: Type.Object({
    action: StringEnum(["read", "write"] as const),
    path: Type.Optional(Type.String()),
  }),
  async execute(toolCallId, params, signal, onUpdate, ctx) {
    // Stream progress
    onUpdate?.({ content: [{ type: "text", text: "Working..." }] });

    // Signal errors by throwing
    if (!params.path) throw new Error("path is required for write");

    return {
      content: [{ type: "text", text: "Done" }],   // Sent to LLM
      details: { result: "..." },                   // For rendering & state
    };
  },
});
```

### 2. Register a Slash Command (user-callable)

```typescript
pi.registerCommand("my-cmd", {
  description: "What this command does",
  handler: async (args, ctx) => {
    ctx.ui.notify(`Running with args: ${args}`, "info");
  },
});
```

User types `/my-cmd optional args` in the chat.

### 3. Handle Events

```typescript
// Modify system prompt each turn
pi.on("before_agent_start", async (event) => {
  return { systemPrompt: event.systemPrompt + "\n\nAlways be concise." };
});

// Block dangerous bash commands
pi.on("tool_call", async (event, ctx) => {
  if (event.toolName === "bash" && event.input.command.includes("rm -rf /")) {
    return { block: true, reason: "Refusing to delete root" };
  }
});

// Run setup once per session
pi.on("session_start", async (_event, ctx) => {
  ctx.ui.notify("Extension ready", "info");
});
```

### 4. State Management (session-branch-safe)

Store state in tool result `details` so it survives branching and reloads:

```typescript
let items: string[] = [];

pi.on("session_start", async (_event, ctx) => {
  items = [];
  for (const entry of ctx.sessionManager.getBranch()) {
    if (entry.type === "message" && entry.message.role === "toolResult"
        && entry.message.toolName === "my_tool") {
      items = entry.message.details?.items ?? [];
    }
  }
});

pi.registerTool({
  name: "my_tool",
  // ...
  async execute(_id, _params, _signal, _onUpdate, _ctx) {
    items.push("new item");
    return {
      content: [{ type: "text", text: "Added" }],
      details: { items: [...items] },  // ← persisted in session
    };
  },
});
```

### 5. Custom TUI Rendering

```typescript
import { Text } from "@earendil-works/pi-tui";

pi.registerTool({
  // ...
  renderCall(args, theme) {
    return new Text(
      theme.fg("toolTitle", theme.bold("my_tool ")) + theme.fg("muted", args.action),
      0, 0  // padding — the Box wrapper handles it
    );
  },
  renderResult(result, { expanded, isPartial }, theme) {
    if (isPartial) return new Text(theme.fg("warning", "Working..."), 0, 0);
    if (result.details?.error) return new Text(theme.fg("error", result.details.error), 0, 0);
    return new Text(theme.fg("success", "✓ Done"), 0, 0);
  },
});
```

## Common Patterns

See [references/patterns-reference.md](references/patterns-reference.md) for copy-paste patterns:
- Stateful extension with session reconstruction
- System prompt injection (pirate mode style)
- Permission gate (block dangerous tool calls)
- UI dialogs (select, confirm, input)
- Widgets and status bar
- Run shell commands from an extension
- Keyboard shortcuts
- CLI flags
- Inter-extension event bus

## Full API Reference

See [references/api-reference.md](references/api-reference.md) for the complete API surface:
- All `pi.*` methods
- All events with their payloads and return types
- `ctx.ui` methods
- TypeBox schema tips
- Output truncation utilities

## Important Rules

1. **Use `StringEnum` from `@earendil-works/pi-ai`** for string union params — `Type.Union`/`Type.Literal` breaks Google models.
2. **Throw to signal tool errors** — returning a value never sets `isError`. Thrown errors are caught and reported to the LLM automatically.
3. **Truncate large output** — use `truncateHead`/`truncateTail` from `@earendil-works/pi-coding-agent`. Limit to 50 KB / 2000 lines.
4. **State goes in `details`** — don't use external files for session state; store in tool result details so branching works correctly.
5. **Check `ctx.hasUI`** before calling dialogs in commands — they're no-ops in print/JSON mode.
6. **Use relative paths** when referencing scripts or assets in this skill.

## Examples Directory

All official examples live at:
```
/opt/homebrew/lib/node_modules/@earendil-works/pi-coding-agent/examples/extensions/
```

Key files to read:
- `hello.ts` — minimal tool
- `todo.ts` — stateful tool + custom rendering + command
- `pirate.ts` — system prompt modification via command + event
- `permission-gate.ts` — blocking tool calls
- `plan-mode/` — complex multi-feature extension
