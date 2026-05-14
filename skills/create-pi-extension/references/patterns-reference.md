# Pi Extension Patterns Reference

Copy-paste patterns for the most common extension scenarios.

---

## Pattern 1 — Minimal Tool

```typescript
import { Type } from "@sinclair/typebox";
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

export default function (pi: ExtensionAPI) {
  pi.registerTool({
    name: "greet",
    label: "Greet",
    description: "Greet a person by name",
    parameters: Type.Object({
      name: Type.String({ description: "Name to greet" }),
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

---

## Pattern 2 — Slash Command

```typescript
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

export default function (pi: ExtensionAPI) {
  pi.registerCommand("stats", {
    description: "Show session entry count",
    handler: async (_args, ctx) => {
      const count = ctx.sessionManager.getEntries().length;
      ctx.ui.notify(`${count} entries in this session`, "info");
    },
  });
}
```

---

## Pattern 3 — System Prompt Injection (toggle via command)

```typescript
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

export default function (pi: ExtensionAPI) {
  let enabled = false;

  pi.registerCommand("concise", {
    description: "Toggle concise mode",
    handler: async (_args, ctx) => {
      enabled = !enabled;
      ctx.ui.notify(enabled ? "Concise mode ON" : "Concise mode OFF", "info");
    },
  });

  pi.on("before_agent_start", async (event) => {
    if (!enabled) return undefined;
    return {
      systemPrompt: event.systemPrompt + "\n\nIMPORTANT: Keep all responses under 3 sentences.",
    };
  });
}
```

---

## Pattern 4 — Permission Gate (block dangerous commands)

```typescript
import { isToolCallEventType } from "@earendil-works/pi-coding-agent";
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

export default function (pi: ExtensionAPI) {
  pi.on("tool_call", async (event, ctx) => {
    if (!isToolCallEventType("bash", event)) return undefined;

    const danger = ["rm -rf /", "sudo rm", "> /etc/passwd"];
    const isDangerous = danger.some((d) => event.input.command.includes(d));

    if (isDangerous) {
      const ok = await ctx.ui.confirm(
        "Dangerous command",
        `Allow: ${event.input.command}?`
      );
      if (!ok) return { block: true, reason: "User denied dangerous command" };
    }
  });
}
```

---

## Pattern 5 — Stateful Tool (reconstructed on reload/branch)

```typescript
import { Type } from "@sinclair/typebox";
import { StringEnum } from "@earendil-works/pi-ai";
import type { ExtensionAPI, ExtensionContext } from "@earendil-works/pi-coding-agent";

interface Item { id: number; text: string; }
interface ToolDetails { items: Item[]; nextId: number; }

export default function (pi: ExtensionAPI) {
  let items: Item[] = [];
  let nextId = 1;

  const reconstruct = (ctx: ExtensionContext) => {
    items = [];
    nextId = 1;
    for (const entry of ctx.sessionManager.getBranch()) {
      if (entry.type !== "message") continue;
      const msg = entry.message;
      if (msg.role === "toolResult" && msg.toolName === "list_tool") {
        const d = msg.details as ToolDetails | undefined;
        if (d) { items = d.items; nextId = d.nextId; }
      }
    }
  };

  pi.on("session_start",  async (_e, ctx) => reconstruct(ctx));
  pi.on("session_switch", async (_e, ctx) => reconstruct(ctx));
  pi.on("session_fork",   async (_e, ctx) => reconstruct(ctx));
  pi.on("session_tree",   async (_e, ctx) => reconstruct(ctx));

  pi.registerTool({
    name: "list_tool",
    label: "List Tool",
    description: "Add or list items",
    parameters: Type.Object({
      action: StringEnum(["list", "add"] as const),
      text: Type.Optional(Type.String()),
    }),
    async execute(_id, params, _signal, _onUpdate, _ctx) {
      if (params.action === "add") {
        if (!params.text) throw new Error("text required for add");
        items.push({ id: nextId++, text: params.text });
      }
      return {
        content: [{ type: "text", text: items.map((i) => `${i.id}: ${i.text}`).join("\n") || "empty" }],
        details: { items: [...items], nextId } as ToolDetails,
      };
    },
  });
}
```

---

## Pattern 6 — Custom Tool Rendering

```typescript
import { Text } from "@earendil-works/pi-tui";
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

export default function (pi: ExtensionAPI) {
  pi.registerTool({
    name: "status_tool",
    label: "Status Tool",
    description: "Returns a status",
    parameters: {},
    async execute() {
      return {
        content: [{ type: "text", text: "OK" }],
        details: { status: "ok", count: 42 },
      };
    },
    renderCall(_args, theme) {
      return new Text(theme.fg("toolTitle", theme.bold("status_tool")), 0, 0);
    },
    renderResult(result, { expanded, isPartial }, theme) {
      if (isPartial) return new Text(theme.fg("warning", "⏳ Working..."), 0, 0);
      if (result.details?.status === "error")
        return new Text(theme.fg("error", "✗ " + result.details.message), 0, 0);

      let text = theme.fg("success", "✓ OK") + theme.fg("dim", ` (${result.details?.count})`);
      if (expanded && result.details) {
        text += "\n" + theme.fg("dim", JSON.stringify(result.details, null, 2));
      }
      return new Text(text, 0, 0);
    },
  });
}
```

---

## Pattern 7 — UI Dialogs

```typescript
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

export default function (pi: ExtensionAPI) {
  pi.registerCommand("pick", {
    description: "Interactive model picker",
    handler: async (_args, ctx) => {
      if (!ctx.hasUI) {
        ctx.ui.notify("/pick requires interactive mode", "error");
        return;
      }

      const env = await ctx.ui.select("Choose environment:", ["dev", "staging", "prod"]);
      if (!env) return; // user cancelled

      const ok = await ctx.ui.confirm("Deploy?", `Deploy to ${env}?`);
      if (!ok) return;

      const tag = await ctx.ui.input("Image tag:", "latest");
      if (!tag) return;

      ctx.ui.notify(`Deploying ${tag} to ${env}...`, "info");
      // do the actual work...
    },
  });
}
```

---

## Pattern 8 — Status Bar Widget

```typescript
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

export default function (pi: ExtensionAPI) {
  pi.on("session_start", async (_event, ctx) => {
    ctx.ui.setStatus("my-ext", "ready");
  });

  pi.on("before_agent_start", async (_event, ctx) => {
    ctx.ui.setStatus("my-ext", "thinking...");
  });

  pi.on("turn_end", async (_event, ctx) => {
    ctx.ui.setStatus("my-ext", "idle");
  });

  pi.on("session_shutdown", async (_event, ctx) => {
    ctx.ui.setStatus("my-ext", undefined); // clear
  });
}
```

---

## Pattern 9 — Run Shell Commands

```typescript
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

export default function (pi: ExtensionAPI) {
  pi.on("session_start", async (_event, ctx) => {
    const result = await pi.exec("git", ["log", "--oneline", "-5"], { timeout: 3000 });
    if (result.code === 0) {
      ctx.ui.notify(`Recent commits:\n${result.stdout}`, "info");
    }
  });
}
```

---

## Pattern 10 — CLI Flag

```typescript
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

export default function (pi: ExtensionAPI) {
  pi.registerFlag("read-only", {
    description: "Disable write/edit/bash tools",
    type: "boolean",
    default: false,
  });

  pi.on("session_start", async (_event, _ctx) => {
    if (pi.getFlag("--read-only")) {
      pi.setActiveTools(["read", "grep", "find", "ls"]);
    }
  });
}
```

Usage:
```bash
pi --extension ./my-extension.ts --read-only
```

---

## Pattern 11 — Keyboard Shortcut

```typescript
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

export default function (pi: ExtensionAPI) {
  let compact = false;

  pi.registerShortcut("ctrl+shift+c", {
    description: "Toggle compact mode",
    handler: async (ctx) => {
      compact = !compact;
      ctx.ui.notify(compact ? "Compact ON" : "Compact OFF", "info");
    },
  });
}
```

---

## Pattern 12 — Output Truncation

```typescript
import { Type } from "@sinclair/typebox";
import {
  truncateHead, formatSize,
  DEFAULT_MAX_BYTES, DEFAULT_MAX_LINES,
} from "@earendil-works/pi-coding-agent";
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

export default function (pi: ExtensionAPI) {
  pi.registerTool({
    name: "search_files",
    label: "Search Files",
    description: "Search files with ripgrep",
    parameters: Type.Object({ pattern: Type.String() }),
    async execute(_id, params, signal, _onUpdate, _ctx) {
      const result = await pi.exec("rg", ["--json", params.pattern], { signal });
      const raw = result.stdout;

      const truncation = truncateHead(raw, {
        maxLines: DEFAULT_MAX_LINES,
        maxBytes: DEFAULT_MAX_BYTES,
      });

      let output = truncation.content;
      if (truncation.truncated) {
        output +=
          `\n\n[Output truncated: ${truncation.outputLines} of ${truncation.totalLines} lines` +
          ` (${formatSize(truncation.outputBytes)} of ${formatSize(truncation.totalBytes)})]`;
      }

      return { content: [{ type: "text", text: output }] };
    },
  });
}
```

---

## Pattern 13 — Multiple Tools with Shared State

```typescript
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

export default function (pi: ExtensionAPI) {
  let connection: { query: (sql: string) => Promise<string>; close: () => void } | null = null;

  pi.registerTool({
    name: "db_connect",
    label: "DB Connect",
    description: "Connect to database",
    parameters: {},
    async execute() {
      // connection = await createDbConnection();
      return { content: [{ type: "text", text: "Connected" }] };
    },
  });

  pi.registerTool({
    name: "db_query",
    label: "DB Query",
    description: "Run a SQL query",
    parameters: { sql: String },
    async execute(_id, params) {
      if (!connection) throw new Error("Not connected. Call db_connect first.");
      const rows = await connection.query(params.sql);
      return { content: [{ type: "text", text: rows }] };
    },
  });

  pi.on("session_shutdown", async () => {
    connection?.close();
    connection = null;
  });
}
```

---

## Pattern 14 — Inter-Extension Event Bus

```typescript
// Extension A — emits
export default function (pi: ExtensionAPI) {
  pi.registerTool({
    name: "broadcast",
    label: "Broadcast",
    description: "Broadcast an event to other extensions",
    parameters: { message: String },
    async execute(_id, params) {
      pi.events.emit("my-ext:message", { text: params.message });
      return { content: [{ type: "text", text: "Broadcasted" }] };
    },
  });
}

// Extension B — listens
export default function (pi: ExtensionAPI) {
  pi.events.on("my-ext:message", (data) => {
    console.log("Received:", data.text);
  });
}
```
