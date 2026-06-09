---
name: setup-oauth-mcp-server
description: Configure and authenticate an OAuth-protected MCP server in pi. Covers mcp.json ServerEntry fields, the correct OAuth flow (/mcp-auth TUI command), debugging 405/403/invalid-scope errors, clearing stale OAuth state, and the difference between dynamic client registration (DCR) vs pre-registered apps. Use when adding a new HTTP MCP server that requires OAuth, when /mcp-auth fails with cryptic errors, or when mcp({ connect }) keeps returning 405 or 403.
---

# Setup OAuth MCP Server in Pi

## When to Use

Adding any OAuth-protected MCP server to pi — Figma, Linear, Notion, GitHub, etc.
Also use when debugging failed `/mcp-auth` or `mcp({ connect })` calls.

## mcp.json Field Reference

Pi uses `pi-mcp-adapter`. The `ServerEntry` type has **no `type` field** — `"type": "http"` is silently ignored. Correct fields:

```json
"my-server": {
  "url": "https://api.example.com/mcp",
  "auth": "oauth",
  "oauth": {
    "clientId": "YOUR_CLIENT_ID",
    "clientSecret": "YOUR_CLIENT_SECRET",
    "redirectUri": "http://localhost:7777/oauth/callback",
    "scope": "requested-scope"
  }
}
```

For bearer token servers:
```json
"my-server": {
  "url": "https://api.example.com/mcp",
  "auth": "bearer",
  "bearerToken": "TOKEN_VALUE"
}
```

Config lives at: `~/.pi/agent/mcp.json`

## OAuth Flow

`mcp({ connect: "server" })` does NOT trigger OAuth. It will loop with 405 errors if no OAuth state exists.

**Correct sequence:**
1. `/mcp-auth <server-name>` — in the pi TUI (requires interactive session, opens browser)
2. Complete OAuth consent in browser
3. `/mcp reconnect <server-name>` — reconnect with the stored token

The OAuth callback server binds to **port 7777**. The `redirectUri` in both your OAuth app registration and `mcp.json` must be exactly:
```
http://localhost:7777/oauth/callback
```

## Debugging Auth Failures

### `SSE error: Non-200 status code (405)`
No OAuth state exists yet. Run `/mcp-auth <server>` first. The adapter tries StreamableHTTP → needs auth → falls to SSE → 405.

### `HTTP 403: ... "Forbidden" is not valid JSON`
The server's dynamic client registration (DCR) endpoint is locked. You need a **pre-registered OAuth app** with `clientId` + `clientSecret`. Add them to `mcp.json` under `oauth: {}`. DCR is skipped when `clientId` is present.

### `Invalid scope: <scope-name>`
The OAuth app registered with the provider doesn't have that scope enabled. Go to the provider's developer portal and add the scope to your app. The scope string must match exactly what the server's `/.well-known/oauth-protected-resource` returns.

### Loops or stale 403 after a previously failed auth attempt
Clear cached OAuth state:
```bash
# Find the hash dir for the server
ls ~/.pi/agent/mcp-oauth/

# Remove the specific server's cached state
rm ~/.pi/agent/mcp-oauth/<hash>/tokens.json
rmdir ~/.pi/agent/mcp-oauth/<hash>
```
Then retry `/mcp-auth <server>`.

## Diagnosing a New Server

```bash
# 1. Check what the server returns unauthenticated
curl -si -X POST https://api.example.com/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","clientInfo":{"name":"test","version":"1.0"},"capabilities":{}},"id":1}'
# Look for: www-authenticate header, scopes, authorization_uri

# 2. Fetch OAuth discovery
curl -s https://api.example.com/.well-known/oauth-protected-resource | python3 -m json.tool
curl -s https://api.example.com/.well-known/oauth-authorization-server | python3 -m json.tool
# Look for: registration_endpoint, scopes_supported, authorization_endpoint

# 3. Test DCR (will tell you if pre-registered app is required)
curl -si -X POST <registration_endpoint> \
  -H "Content-Type: application/json" \
  -d '{"client_name":"test","redirect_uris":["http://localhost:7777/oauth/callback"],"grant_types":["authorization_code"],"scope":"<scope>"}'
# 403 = DCR blocked, need pre-registered clientId
# 201 = DCR works, no clientId needed in mcp.json
```

## Verifying Connection

```bash
mcp({ connect: "server-name" })   # after /mcp-auth succeeds
mcp({ server: "server-name" })    # list available tools
```
