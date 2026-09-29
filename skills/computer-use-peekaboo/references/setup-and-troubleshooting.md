# Setup, Hosts, and Troubleshooting

Verified on macOS 27.0, Peekaboo 4.6.0, pi running inside Ghostty under herdr.

## Install

```bash
brew install openclaw/tap/peekaboo     # CLI only — this is all an agent needs
peekaboo --version
```

The npm package is still published as `@steipete/peekaboo` while the repo lives at
`openclaw/Peekaboo`; the registry name lags the maintainer move. **Don't use
`npx -y @steipete/peekaboo mcp`** in an MCP config — the registry tarball trails the brew
formula and each launch hits the network. Point at the brew binary instead.

`Peekaboo.app` (menu-bar GUI, GitHub releases) is optional. Its release tags can lag the brew
CLI, and a version-skewed app/CLI pair risks a Bridge handshake mismatch. Skip it unless you
want the permission-onboarding UI.

## Permissions (TCC)

Three separate grants are needed, and each is checked **where the work runs**:

| Permission | Checked by | Needed for |
|---|---|---|
| Screen Recording | the host that captures | `see` pixels, `capture` |
| Accessibility | the host that reads AX | `see --tree`, `click --on`, `set-value` |
| Event Synthesizing (macOS 26+) | the host that sends events | `type`, `press`, coordinate clicks |

Grant them to the **binary**, not to your terminal:

System Settings → Privacy & Security → each pane → `+` → **⌘⇧G** → `/opt/homebrew/bin/peekaboo`

One entry covers both the CLI and the Bridge daemon (same executable) and survives changing
terminals. Granting the terminal app instead leaves the daemon denied, and denying it produces
failures that look like app bugs rather than permission bugs.

Then **restart the daemons** — they are long-lived (`--idle-timeout 300s`) and cache the denial:

```bash
pkill -f "peekaboo daemon"
peekaboo permissions status        # bridge host + local runtime, both must be Granted
```

`permissions status` reports the Bridge host and the local runtime separately; they need not
match. `open "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"`
jumps straight to the pane.

## No AI provider is required

`aiProviders` in `~/.peekaboo/config.json` and `agent.defaultModel` feed **only**
`peekaboo agent` — Peekaboo's own built-in natural-language loop. When pi is the agent, pi
calls `see`/`click`/`type` directly and no credential is ever read. Every command in this
skill runs with an empty `~/.peekaboo/credentials`.

Bedrock is not in the provider list (OpenAI, Anthropic, Grok, Google, MiniMax, Kimi,
OpenRouter, Ollama, LM Studio). If you ever do want `peekaboo agent`, the LM Studio slot is
the only generic OpenAI-compatible base URL and it is hardcoded to `http://localhost:1234/v1`
— point `bedrock-access-gateway` there and use `--model lmstudio/openai/<model-id>`.

When wiring Peekaboo as an MCP server, deny the model-backed tools so a missing provider can't
produce confusing failures:

```json
{ "command": "peekaboo", "args": ["mcp"],
  "env": { "PEEKABOO_DISABLE_TOOLS": "agent,analyze,verify_state" } }
```

## The `targetNotFound ... window minimized` trap

The single most misleading error. It looks like broken permissions or a broken daemon. It is
neither.

```
Desktop observation target was not found: shareable window for Microsoft PowerPoint.
Candidates: #0 id=19080 '<untitled>' 1400x850 alpha=1.00 reason=window minimized; …
```

ScreenCaptureKit can only share windows on the **active screen/Space**. When no window of the
target app is currently on screen, every candidate is reported `reason=window minimized` —
often with `alpha=1.00`, which is what makes it look like a bug. Diagnose with the AX view,
which disagrees with SCK here:

```bash
peekaboo window list --app "Microsoft PowerPoint" --json \
  | jq -r '.data.windows[] | "id=\(.window_id) on_screen=\(.is_on_screen) \(.window_title)"'
```

If all are `on_screen=false`, bring one on screen and retry:

```bash
peekaboo app focus --app "Microsoft PowerPoint" --foreground
# or: peekaboo window focus --window-id <id> --foreground
# or: peekaboo space switch …      (space list itself needs --no-remote)
```

`reason=window minimized` is also literal for genuinely minimized windows — restore them with
`peekaboo window restore`.

Field names in `window list --json` are `window_title` and a nested `bounds` object, not `title`.

## Host selection: Bridge daemon vs local runtime

Prefer the Bridge daemon (default). It keeps TCC grants in one place, survives your terminal
restarting, and is what the upstream guide recommends for SSH/launchd sessions.

`--no-remote` (or `PEEKABOO_NO_REMOTE=1`) forces caller-local execution. Treat it as a
**diagnostic**, not a default: upstream warns that `--no-remote --capture-engine cg` outside an
active Aqua session can return wallpaper-only or redacted pixels *while still reporting
success*. If you use it, open the PNG and look at it.

`--capture-engine classic` (alias `cg`) avoids in-process ScreenCaptureKit. Useful when another
app holds SCK, though Peekaboo's own coordination is scoped to its processes — Chrome, Zoom,
OBS etc. do not block capture.

Some commands are local-only: `space list` refuses on a remote host with
`remote Space support is not implemented`.

## AX reads on huge trees

Office apps expose very large AX trees. `see` can fail with
`AX tree incomplete at incomplete accessibility read`. Read AX without pixels:

```bash
peekaboo see --app "Microsoft PowerPoint" --tree --no-screenshot
```

Raising `PEEKABOO_AX_MAX_DEPTH` / `PEEKABOO_AX_MAX_ELEMENTS` / `PEEKABOO_AX_MAX_CHILDREN`
does not reliably fix it; dropping the screenshot does.

**`--web-focus` is not a read flag.** It performs an AXPress web-content focus retry — a
desktop mutation — which stales the snapshot and makes a tree-only `see` return zero elements:

```
tree-only see failed after its conditional desktop mutation result was returned
Snapshot is stale: AX-only see could not bind its elements to an exact process-generation receipt
```

Never combine it with a plain observation.

## Verifying captures

`sips -g pixelWidth -g pixelHeight <path>` checks dimensions only — it cannot tell a real
capture from wallpaper. Open the image and look at it.

## Ranking: when Peekaboo is the right tool

| Package | Stars | Use it when |
|---|---|---|
| `openclaw/Peekaboo` | 5.2k | **Default.** Pixels + AX + native agent flows, MIT, brew, actively pushed |
| `steipete/macos-automator-mcp` | 845 | Pure AppleScript/JXA scripting with a knowledge base; no pixels |
| `domdomegg/computer-use-mcp` | 381 | Rust, Windows + macOS from one server |
| `mediar-ai/mcp-server-macos-use` | 356 | Stale (last push Apr 2026) |
| `CursorTouch/MacOS-MCP` | 187 | AX-only, vision optional, `uvx macos-mcp` |
| `klemensms/mcp-computer-use` | beta | Governance: action allowlist, rate limits, secret rejection on `type_text`, JSONL audit log. Needs full Xcode |

Dead ends (≤2 stars, do not build on): `macpoint`, `mac-native-pptx-mcp`,
`onixhdz/computer-use-mcp`.

If the target is a **browser page**, don't use Peekaboo — use Playwright/CDP. Peekaboo is for
native app chrome, menus, dialogs, and non-browser desktop UI.
