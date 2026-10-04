# n8n Workflow MCP — Official Workflow-SDK MCP Server

This environment connects to n8n's **official MCP Server** (v1.1.0), exposed as `n8n-mcp`
with tools prefixed `mcp__n8n_mcp__*`. It is a **Workflow SDK (code) builder** — you build
workflows by writing `@n8n/workflow-sdk` TypeScript, validating it, then creating the
workflow from that code. It is **not** a raw-JSON CRUD API and it is **not** czlonkowski's
n8n-mcp. Use this file as the source of truth for which tool to call.

These are pi built-in MCP tools (exposure `codemode` by default, so they are not declared to the model): call them from a codemode script as `await tools.mcp__n8n_mcp__<name>({...})`; discover with `searchTools("n8n")` / `describeTool(name)`.

## Required build flow (do not skip steps)

```
1. mcp__n8n_mcp__get_sdk_reference          # MANDATORY before writing any SDK code
2. mcp__n8n_mcp__get_suggested_nodes        # planning step; pass { categories: [...] }
3. mcp__n8n_mcp__search_nodes               # find exact node type/version
   mcp__n8n_mcp__get_node_types             # get TS param definitions for a node
4. <write @n8n/workflow-sdk code>     # see references/workflow-sdk-*.md
5. mcp__n8n_mcp__validate_node_config       # validate each node's config as you write it
6. mcp__n8n_mcp__validate_workflow          # validate the full SDK code → expect { valid: true }
7. mcp__n8n_mcp__create_workflow_from_code  # creates the workflow (INACTIVE) → returns workflowId + URL
8. mcp__n8n_mcp__publish_workflow           # activate it (required before execute)
9. mcp__n8n_mcp__execute_workflow           # run it; returns execution id (async, status "started")
10. mcp__n8n_mcp__get_execution             # poll with { includeData: true } for node I/O + errors
```

### Planning gotcha
`mcp__n8n_mcp__get_suggested_nodes` rejects some category names. `"api_integration"` returns
"not found"; use known-good categories like `"scheduling"`, `"data_transformation"`.

### SDK-code gotchas (verified)
- Every node needs a sample `output: [...]` so pin data / preview works.
- Keep all variables inside **one** `{{ }}` block. Two `{{ }}` blocks in one string →
  "Nested expressions are not supported".
- Build expression strings with **single-quoted** literals inside the expression, e.g.
  `={{ '"' + $json.q + '" — ' + $json.a }}`. Escaped double quotes (`\"`) collapse to `"""`
  and break the stored expression.
- HTTP Request v4.x with default options auto-parses a JSON array into fields directly on
  `$json` (`$json.q`), NOT under `$json.body` — `body` wrapping only happens with certain
  response/full-response options. (Webhook nodes DO wrap under `$json.body`.)

## Editing existing workflows

`mcp__n8n_mcp__update_workflow` applies an **atomic batch** of operations (discriminated union):

```
updateNodeParameters | setNodeParameter | addNode | removeNode | renameNode |
addConnection | removeConnection | setNodeCredential | setNodePosition |
setNodeDisabled | setWorkflowMetadata
```

Example (replace all params of one node):
`{ type: "updateNodeParameters", nodeName: "Format Message", parameters: { ...full params... } }`

After `update_workflow`, **re-publish** to make the new version active before executing.

## Full tool inventory (this server)

| Area | Tools |
|------|-------|
| Reference | `mcp__n8n_mcp__get_sdk_reference`, `mcp__n8n_mcp__get_workflow_sdk_reference` |
| Discovery | `mcp__n8n_mcp__search_nodes`, `mcp__n8n_mcp__get_node_types`, `mcp__n8n_mcp__get_suggested_nodes` |
| Validation | `mcp__n8n_mcp__validate_node_config`, `mcp__n8n_mcp__validate_workflow` |
| Create | `mcp__n8n_mcp__create_workflow_from_code`, `mcp__n8n_mcp__get_workflow_preview` |
| Edit | `mcp__n8n_mcp__update_workflow`, `mcp__n8n_mcp__archive_workflow` |
| Lifecycle | `mcp__n8n_mcp__publish_workflow`, `mcp__n8n_mcp__unpublish_workflow` |
| Run/debug | `mcp__n8n_mcp__execute_workflow`, `mcp__n8n_mcp__get_execution`, `mcp__n8n_mcp__search_executions`, `mcp__n8n_mcp__prepare_test_pin_data`, `mcp__n8n_mcp__test_workflow` |
| Discover wf | `mcp__n8n_mcp__search_workflows`, `mcp__n8n_mcp__get_workflow_details`, `mcp__n8n_mcp__search_projects`, `mcp__n8n_mcp__search_folders` |
| Credentials | `mcp__n8n_mcp__list_credentials` |
| Data tables | `mcp__n8n_mcp__search_data_tables`, `mcp__n8n_mcp__create_data_table`, `mcp__n8n_mcp__rename_data_table`, `mcp__n8n_mcp__add_data_table_column`, `mcp__n8n_mcp__delete_data_table_column`, `mcp__n8n_mcp__rename_data_table_column`, `mcp__n8n_mcp__add_data_table_rows` |

## Tool-name mapping (czlonkowski docs → this server)

The adapted references (`expression-syntax.md`, `code-node-*.md`, `workflow-patterns.md`,
`node-configuration.md`, `validation-gotchas.md`) use czlonkowski's tool names. Map them:

| czlonkowski n8n-mcp | Official Workflow-SDK MCP (here) |
|---------------------|----------------------------------|
| `search_nodes` | `mcp__n8n_mcp__search_nodes` |
| `get_node` (info/properties) | `mcp__n8n_mcp__get_node_types` |
| `validate_node` / `validate_node_operation` | `mcp__n8n_mcp__validate_node_config` |
| `validate_workflow` (JSON) | `mcp__n8n_mcp__validate_workflow` (SDK code) |
| `n8n_create_workflow` (JSON) | `mcp__n8n_mcp__create_workflow_from_code` (SDK code) |
| `n8n_update_partial_workflow` | `mcp__n8n_mcp__update_workflow` |
| `n8n_get_workflow` / `n8n_list_workflows` | `mcp__n8n_mcp__get_workflow_details` / `mcp__n8n_mcp__search_workflows` |
| `n8n_trigger_webhook_workflow` / test | `mcp__n8n_mcp__execute_workflow` / `mcp__n8n_mcp__test_workflow` |
| `n8n_list_executions` / `n8n_get_execution` | `mcp__n8n_mcp__search_executions` / `mcp__n8n_mcp__get_execution` |
| `n8n_autofix_workflow` | *(no equivalent)* — fix in SDK code, re-validate |
| `search_templates` / `get_template` | *(no equivalent)* — use `mcp__n8n_mcp__search_workflows` |

> Key difference: czlonkowski edits **JSON**; this server builds and edits via **SDK code**.
> When an adapted doc says "create/update the workflow JSON", instead write/modify the
> `@n8n/workflow-sdk` code and call the SDK-code tools above.

## When there is NO connected MCP

Fall back to the local `@n8n/workflow-sdk` (public npm, run with `tsx`) — build, validate,
and `.toJSON()` locally, then import the JSON into n8n manually. See
[workflow-sdk-overview.md](workflow-sdk-overview.md).
