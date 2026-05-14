#!/usr/bin/env bash
# scaffold.sh — Generate a pi extension boilerplate
#
# Usage:
#   bash scaffold.sh <name>           # Single-file extension: <name>.ts
#   bash scaffold.sh <name> --package # Package extension: <name>/index.ts + package.json

set -euo pipefail

NAME="${1:-}"
MODE="${2:-}"

if [[ -z "$NAME" ]]; then
  echo "Usage: bash scaffold.sh <extension-name> [--package]"
  echo ""
  echo "  extension-name   lowercase, hyphens allowed (e.g. my-extension)"
  echo "  --package        scaffold a directory with package.json instead of single file"
  exit 1
fi

# Validate name: lowercase letters, numbers, hyphens only
if [[ ! "$NAME" =~ ^[a-z0-9][a-z0-9-]*[a-z0-9]$|^[a-z0-9]$ ]]; then
  echo "Error: extension name must be lowercase letters, numbers, and hyphens (no leading/trailing hyphens)"
  exit 1
fi

# Convert hyphenated name to camelCase function name (macOS-compatible)
FUNC_NAME=$(echo "$NAME" | awk -F'-' '{
  result = ""
  for (i = 1; i <= NF; i++) {
    word = $i
    result = result toupper(substr(word,1,1)) substr(word,2)
  }
  print result
}')Extension

# ─────────────────────────────────────────────────────────
# SINGLE FILE MODE
# ─────────────────────────────────────────────────────────
if [[ "$MODE" != "--package" ]]; then
  OUT="${NAME}.ts"

  if [[ -f "$OUT" ]]; then
    echo "Error: $OUT already exists"
    exit 1
  fi

  cat > "$OUT" <<TSEOF
/**
 * ${NAME} — Pi Extension
 *
 * Load with: pi --extension ./${OUT}
 * Or copy to: ~/.pi/agent/extensions/${OUT}
 */

import { Type } from "@sinclair/typebox";
import { StringEnum } from "@earendil-works/pi-ai";
import type { ExtensionAPI, ExtensionContext } from "@earendil-works/pi-coding-agent";
import { Text } from "@earendil-works/pi-tui";

export default function ${FUNC_NAME}(pi: ExtensionAPI) {
  // ── State (reconstructed from session on load/branch) ──────────────────
  // let myState = [];

  // const reconstruct = (ctx: ExtensionContext) => {
  //   myState = [];
  //   for (const entry of ctx.sessionManager.getBranch()) {
  //     if (entry.type === "message" && entry.message.role === "toolResult"
  //         && entry.message.toolName === "my_tool") {
  //       myState = entry.message.details?.state ?? [];
  //     }
  //   }
  // };

  // pi.on("session_start",  async (_e, ctx) => reconstruct(ctx));
  // pi.on("session_switch", async (_e, ctx) => reconstruct(ctx));
  // pi.on("session_fork",   async (_e, ctx) => reconstruct(ctx));
  // pi.on("session_tree",   async (_e, ctx) => reconstruct(ctx));

  // ── Tool (LLM-callable) ────────────────────────────────────────────────
  pi.registerTool({
    name: "${NAME//-/_}",
    label: "${NAME}",
    description: "TODO: describe what this tool does",
    parameters: Type.Object({
      // action: StringEnum(["list", "add"] as const),
      input: Type.String({ description: "TODO: describe this parameter" }),
    }),

    async execute(_toolCallId, params, signal, onUpdate, _ctx) {
      // Check for cancellation
      if (signal?.aborted) {
        return { content: [{ type: "text", text: "Cancelled" }] };
      }

      // Stream progress
      onUpdate?.({ content: [{ type: "text", text: "Working..." }] });

      // Throw to signal errors to the LLM
      // if (!params.input) throw new Error("input is required");

      return {
        content: [{ type: "text", text: \`Result: \${params.input}\` }],
        details: { input: params.input },
      };
    },

    renderCall(args, theme) {
      return new Text(
        theme.fg("toolTitle", theme.bold("${NAME//-/_} ")) + theme.fg("muted", args.input ?? ""),
        0, 0
      );
    },

    renderResult(result, { expanded, isPartial }, theme) {
      if (isPartial) return new Text(theme.fg("warning", "⏳ Working..."), 0, 0);
      const text = result.content[0];
      const msg = text?.type === "text" ? text.text : "";
      return new Text(theme.fg("success", "✓ ") + theme.fg("muted", msg), 0, 0);
    },
  });

  // ── Command (user-callable via /${NAME}) ───────────────────────────────
  pi.registerCommand("${NAME}", {
    description: "TODO: describe this command",
    handler: async (_args, ctx) => {
      if (!ctx.hasUI) {
        ctx.ui.notify("/${NAME} requires interactive mode", "error");
        return;
      }
      ctx.ui.notify("${NAME} command ran!", "info");
    },
  });

  // ── Events ─────────────────────────────────────────────────────────────
  // Modify system prompt each turn:
  // pi.on("before_agent_start", async (event) => {
  //   return { systemPrompt: event.systemPrompt + "\n\nExtra instructions." };
  // });

  // Intercept tool calls:
  // pi.on("tool_call", async (event, ctx) => {
  //   return undefined; // or { block: true, reason: "..." }
  // });
}
TSEOF

  echo "✓ Created: $OUT"
  echo ""
  echo "Load it:"
  echo "  pi --extension ./${OUT}"
  echo ""
  echo "Or install globally:"
  echo "  cp ${OUT} ~/.pi/agent/extensions/"
  exit 0
fi

# ─────────────────────────────────────────────────────────
# PACKAGE MODE
# ─────────────────────────────────────────────────────────
if [[ -d "$NAME" ]]; then
  echo "Error: directory '$NAME' already exists"
  exit 1
fi

mkdir -p "$NAME"

# index.ts
cat > "$NAME/index.ts" <<TSEOF
/**
 * ${NAME} — Pi Extension (package)
 *
 * Setup:  cd ${NAME} && npm install
 * Load:   pi --extension ./${NAME}/
 * Global: copy directory to ~/.pi/agent/extensions/
 */

import { Type } from "@sinclair/typebox";
import { StringEnum } from "@earendil-works/pi-ai";
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
import { Text } from "@earendil-works/pi-tui";

export default function ${FUNC_NAME}(pi: ExtensionAPI) {
  pi.registerTool({
    name: "${NAME//-/_}",
    label: "${NAME}",
    description: "TODO: describe what this tool does",
    parameters: Type.Object({
      input: Type.String({ description: "TODO: describe this parameter" }),
    }),

    async execute(_toolCallId, params, signal, onUpdate, _ctx) {
      if (signal?.aborted) return { content: [{ type: "text", text: "Cancelled" }] };
      onUpdate?.({ content: [{ type: "text", text: "Working..." }] });

      return {
        content: [{ type: "text", text: \`Result: \${params.input}\` }],
        details: { input: params.input },
      };
    },

    renderCall(args, theme) {
      return new Text(
        theme.fg("toolTitle", theme.bold("${NAME//-/_} ")) + theme.fg("muted", args.input ?? ""),
        0, 0
      );
    },

    renderResult(result, { isPartial }, theme) {
      if (isPartial) return new Text(theme.fg("warning", "⏳ Working..."), 0, 0);
      const text = result.content[0];
      const msg = text?.type === "text" ? text.text : "";
      return new Text(theme.fg("success", "✓ ") + theme.fg("muted", msg), 0, 0);
    },
  });

  pi.registerCommand("${NAME}", {
    description: "TODO: describe this command",
    handler: async (_args, ctx) => {
      ctx.ui.notify("${NAME} command ran!", "info");
    },
  });
}
TSEOF

# package.json
cat > "$NAME/package.json" <<JSONEOF
{
  "name": "${NAME}",
  "version": "1.0.0",
  "description": "Pi extension: ${NAME}",
  "main": "index.ts",
  "dependencies": {
    "@sinclair/typebox": "^0.34.0"
  }
}
JSONEOF

# tsconfig.json
cat > "$NAME/tsconfig.json" <<JSONEOF
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "esModuleInterop": true
  },
  "include": ["*.ts"]
}
JSONEOF

# README.md
cat > "$NAME/README.md" <<MDEOF
# ${NAME}

A pi coding-agent extension.

## Setup

\`\`\`bash
cd ${NAME} && npm install
\`\`\`

## Load

\`\`\`bash
pi --extension ./${NAME}/
\`\`\`

## Install globally

\`\`\`bash
cp -r ${NAME}/ ~/.pi/agent/extensions/
\`\`\`
MDEOF

echo "✓ Created package: ${NAME}/"
echo ""
echo "Next steps:"
echo "  cd ${NAME} && npm install"
echo "  pi --extension ./${NAME}/"
