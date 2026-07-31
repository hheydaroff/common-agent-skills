---
name: n8n-builder
description: "Build and manage n8n workflows and build custom n8n nodes. Use when the user wants to create, edit, validate, test, debug, or publish n8n workflows (via the Workflow-SDK MCP or @n8n/workflow-sdk), or to build community/custom nodes (declarative REST, programmatic, trigger, AI sub-nodes) with @n8n/node-cli. Covers n8n expressions, Code node, credentials, and validation errors."
---

# n8n Builder

Two jobs in one skill: **(1) build & manage n8n workflows** and **(2) build custom n8n
nodes**. This SKILL.md routes — read the matching overview/reference before writing code.

## Decide which job

```
User wants to AUTOMATE something inside n8n (connect nodes, webhooks, AI agents,
   data sync, schedules, Code-node logic, expressions)        → WORKFLOWS  (pillar 1)
User wants to EXTEND n8n with a new integration node/credential
   to publish as an npm community node                        → CUSTOM NODES (pillar 2)
```

If unsure, ask. The two pillars share nothing but the n8n mental model.

---

## Pillar 1 — Build & manage workflows

**Default path = the connected MCP.** This environment has n8n's official **Workflow-SDK
MCP** (`n8n_mcp_*` tools): you write `@n8n/workflow-sdk` code, validate it, and create the
workflow from that code. Always start with [mcp-workflow-tools.md](references/mcp-workflow-tools.md)
for the exact tool flow, then use the SDK references to write the code. With no MCP, use the
local `@n8n/workflow-sdk` (npm + `tsx`) per [workflow-sdk-overview.md](references/workflow-sdk-overview.md).

**Golden rule: never guess node `type`/`version`.** Look them up — live via
`n8n_mcp_search_nodes` + `n8n_mcp_get_node_types`, or offline in
`references/node-registry-official.json` / `node-registry-community.json`.

### Workflow reference routing

| File | When to load |
|------|--------------|
| [mcp-workflow-tools.md](references/mcp-workflow-tools.md) | **Start here for workflows.** Live `n8n_mcp_*` build/edit/publish/execute/debug flow + tool-name mapping |
| [workflow-sdk-overview.md](references/workflow-sdk-overview.md) | SDK concepts, node lookup rules, full API quick-reference, local (no-MCP) setup |
| [workflow-sdk-building.md](references/workflow-sdk-building.md) | Creating a workflow, settings, JSON import/export |
| [workflow-sdk-nodes-connections.md](references/workflow-sdk-nodes-connections.md) | Node factories, subnodes, connection patterns, credentials, node-registry usage |
| [workflow-sdk-control-flow.md](references/workflow-sdk-control-flow.md) | IF/Switch/Merge/Split-in-Batches, branching, error handling |
| [workflow-sdk-expressions-code.md](references/workflow-sdk-expressions-code.md) | SDK expression system, Code-node helpers, `fromAi` |
| [workflow-sdk-validation-testing.md](references/workflow-sdk-validation-testing.md) | `validateWorkflow`, pin data, test data, error codes |
| [workflow-sdk-code-generation.md](references/workflow-sdk-code-generation.md) | JSON↔code round-tripping (`generate`/`parseWorkflowCode`) |
| [workflow-sdk-plugins.md](references/workflow-sdk-plugins.md) | Plugin system, type generation, Zod schemas |
| [workflow-patterns.md](references/workflow-patterns.md) | Proven architectures: webhook, HTTP API, database, AI agent, scheduled |
| [expression-syntax.md](references/expression-syntax.md) | n8n `{{ }}` expressions, `$json`/`$node`/`$now`, **webhook `$json.body` gotcha** |
| [code-node-javascript.md](references/code-node-javascript.md) | JavaScript in the Code node — data access, `$helpers`, return format, errors |
| [code-node-python.md](references/code-node-python.md) | Python in the Code node — limits (no external libs), stdlib, data access |
| [code-node-tool.md](references/code-node-tool.md) | AI-agent Custom Code **Tool** (`toolCode`) — string return, `query` input |
| [node-configuration.md](references/node-configuration.md) | Property dependencies (e.g. `sendBody`→`contentType`), operation-specific config |
| [validation-gotchas.md](references/validation-gotchas.md) | Validation error catalog + false positives, MCP-neutral |

> The adapted files (expression/code-node/patterns/config/validation) name czlonkowski's
> n8n-mcp tools. Map them to the live tools via the table in `mcp-workflow-tools.md`.

---

## Pillar 2 — Build custom nodes

Build production community nodes with the official **`@n8n/node-cli`** (`n8n-node` CLI).
**Always start with [nodes-overview.md](references/nodes-overview.md)** — it covers the full
workflow (choose style → scaffold → implement → validate → publish), code standards, and UX
verification rules. Then drill into the style-specific reference.

Decision: REST API, no triggers, no multi-call chaining → **declarative**. Model/memory
provider for the AI Agent → **AI sub-node**. Triggers, GraphQL, non-REST, complex chaining,
full versioning → **programmatic**.

### Node reference routing

| File | When to load |
|------|--------------|
| [nodes-overview.md](references/nodes-overview.md) | **Start here for nodes.** Full workflow, CLI scaffold, standards, UX rules, gates |
| [nodes-declarative.md](references/nodes-declarative.md) | Declarative node template: routing, preSend/postReceive, pagination, resourceLocator/Mapper |
| [nodes-programmatic.md](references/nodes-programmatic.md) | Programmatic `execute()`, triggers (webhook/poll/stream), versioning, error handling |
| [nodes-credentials.md](references/nodes-credentials.md) | Credential/auth patterns: API key, Bearer, OAuth2, Basic, custom, `test`/`preAuthentication` |
| [nodes-ai-subnodes.md](references/nodes-ai-subnodes.md) | AI sub-nodes (chat model/memory) via `supplyData()` + `@n8n/ai-node-sdk` |
| [nodes-validation.md](references/nodes-validation.md) | The gate protocol: lint → build → cloud-support → runtime; lint-rule catalog |
| [nodes-publishing.md](references/nodes-publishing.md) | Release flow, GitHub Actions + npm provenance, Creator-Portal verification |
| [nodes-common-mistakes.md](references/nodes-common-mistakes.md) | Numbered error-pattern catalog and fixes |

---

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/refresh-node-registry.sh` | Rebuild the offline node-registry caches (official + community index, plus the optional ~5MB `node-registry-properties.jsonl` which is not shipped) |

## Attribution

Adapted from [geckse/n8n-dev-skills](https://github.com/geckse/n8n-dev-skills) (node builder
+ workflow SDK) and [czlonkowski/n8n-skills](https://github.com/czlonkowski/n8n-skills)
(expressions, Code nodes, patterns, config, validation). Both MIT.
