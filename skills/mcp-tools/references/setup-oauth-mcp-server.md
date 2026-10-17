# Setup OAuth MCP Server in Pi

Pi's **built-in MCP** (docs: `docs/mcp.md` in the pi package). The old `pi-mcp-adapter`, `/mcp-auth`, `mcp({ connect })` and `~/.pi/agent/mcp-oauth/` are gone. If an installed extension registers `/mcp` (like `pi-mcp-adapter`) it silently replaces the built-in support.

## When to Use

Adding an OAuth-protected HTTP MCP server (Figma, Linear, Notion, Sentry, GitHub...) or debugging a failed sign-in.

## Config

User servers: `~/.pi/agent/mcp.json` (project: `.pi/mcp.json`, only after project trust). Run `/reload` after editing.

```json
{ "mcpServers": {
  "sentry": { "url": "https://mcp.sentry.dev/mcp" }
} }
```

Most servers need nothing else: pi registers itself by dynamic client registration. Add an `oauth` block only when needed:

| Situation | Add under `"oauth"` |
|---|---|
| Server blocks dynamic registration (HTTP 403 on registration) | `"clientId"`, `"clientSecret": "${ENV_VAR}"`, optionally `"callbackPort"` |
| Server only whitelists a known client name | `"clientName": "Claude Code"` |
| Server supports Client ID Metadata Documents | `"clientRegistration": "cimd"` (cannot combine with `clientId`/`clientName`) |
| Sign-in opens a page that does not exist (wrong or missing authorization server) | `"authServerMetadataUrl": "<.well-known/openid-configuration URL>"` |

Bearer-token servers: use `headers` instead, e.g. `"Authorization": "Bearer ${TOKEN}"`. OAuth applies only to HTTP servers **without** an `Authorization` header. Tool names are `mcp__<server>__<tool>`.

## Sign in

1. `/mcp` → select the server → "Sign in", or `/mcp login <server>` (also `pi mcp login <server>` outside the TUI). Browser opens; approve consent. Over SSH, paste the redirected URL into the sign-in screen.
2. `/mcp reconnect <server>` if tools do not appear. A running session picks up new credentials on its next turn.
3. `/mcp logout <server>` deletes stored credentials (`~/.pi/agent/mcp-auth.json`).

## Debugging

| Symptom | Cause / fix |
|---|---|
| `/mcp` shows "needs sign-in" | Run `/mcp login <server>`. |
| HTTP 403 on registration | Dynamic client registration is blocked: register an OAuth app and set `oauth.clientId`/`clientSecret`. |
| `Invalid scope: <name>` | The app registered with the provider lacks that scope; enable it in the provider's developer portal. The scope must match the server's `/.well-known/oauth-protected-resource`. |
| Stale 403 / loop after a failed attempt | `/mcp logout <server>`, then `/mcp login <server>`. |
| Tools missing in codemode | Check `/mcp` state; `searchTools("<server>")` waits for all servers. Server names allow only letters, digits, `_`, `-`. |
| `Cannot find module './proxy-modes.ts'` | `pi-mcp-adapter` leftover in `~/.pi/agent/npm`; remove it. |

## Diagnosing a new server (unauthenticated probe)

Use the `bash` tool for these probes only if outbound curl works in your environment; otherwise rely on `/mcp` status.

```bash
curl -s https://api.example.com/.well-known/oauth-protected-resource | python3 -m json.tool
curl -s https://api.example.com/.well-known/oauth-authorization-server | python3 -m json.tool
# Look for: registration_endpoint (absent = pre-registered app needed), scopes_supported
```
