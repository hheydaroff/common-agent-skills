# n8n Workflow MCP — Official Workflow-SDK MCP Server

This environment connects to n8n's **official MCP Server** (v1.1.0), exposed as `n8n-mcp`
with tools prefixed `n8n_mcp_*`. It is a **Workflow SDK (code) builder** — you build
workflows by writing `@n8n/workflow-sdk` TypeScript, validating it, then creating the
workflow from that code. It is **not** a raw-JSON CRUD API and it is **not** czlonkowski's
n8n-mcp. Use this file as the source of truth for which tool to call.

## Required build flow (do not skip steps)

```
1. n8n_mcp_get_sdk_reference          # MANDATORY before writing any SDK code
2. n8n_mcp_get_suggested_nodes        # planning step; pass { categories: [...] }
3. n8n_mcp_search_nodes               # find exact node type/version
   n8n_mcp_get_node_types             # get TS param definitions for a node
4. <write @n8n/workflow-sdk code>     # see references/workflow-sdk-*.md
5. n8n_mcp_validate_node_config       # validate each node's config as you write it
6. n8n_mcp_validate_workflow          # validate the full SDK code → expect { valid: true }
7. n8n_mcp_create_workflow_from_code  # creates the workflow (INACTIVE) → returns workflowId + URL
8. n8n_mcp_publish_workflow           # activate it (required before execute)
9. n8n_mcp_execute_workflow           # run it; returns execution id (async, status "started")
10. n8n_mcp_get_execution             # poll with { includeData: true } for node I/O + errors
```

### Planning gotcha
`n8n_mcp_get_suggested_nodes` rejects some category names. `"api_integration"` returns
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

`n8n_mcp_update_workflow` applies an **atomic batch** of operations (discriminated union):

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
| Reference | `n8n_mcp_get_sdk_reference`, `n8n_mcp_get_workflow_sdk_reference` |
| Discovery | `n8n_mcp_search_nodes`, `n8n_mcp_get_node_types`, `n8n_mcp_get_suggested_nodes` |
| Validation | `n8n_mcp_validate_node_config`, `n8n_mcp_validate_workflow` |
| Create | `n8n_mcp_create_workflow_from_code`, `n8n_mcp_get_workflow_preview` |
| Edit | `n8n_mcp_update_workflow`, `n8n_mcp_archive_workflow` |
| Lifecycle | `n8n_mcp_publish_workflow`, `n8n_mcp_unpublish_workflow` |
| Run/debug | `n8n_mcp_execute_workflow`, `n8n_mcp_get_execution`, `n8n_mcp_search_executions`, `n8n_mcp_prepare_test_pin_data`, `n8n_mcp_test_workflow` |
| Discover wf | `n8n_mcp_search_workflows`, `n8n_mcp_get_workflow_details`, `n8n_mcp_search_projects`, `n8n_mcp_search_folders` |
| Credentials | `n8n_mcp_list_credentials` |
| Data tables | `n8n_mcp_search_data_tables`, `n8n_mcp_create_data_table`, `n8n_mcp_rename_data_table`, `n8n_mcp_add_data_table_column`, `n8n_mcp_delete_data_table_column`, `n8n_mcp_rename_data_table_column`, `n8n_mcp_add_data_table_rows` |

## Tool-name mapping (czlonkowski docs → this server)

The adapted references (`expression-syntax.md`, `code-node-*.md`, `workflow-patterns.md`,
`node-configuration.md`, `validation-gotchas.md`) use czlonkowski's tool names. Map them:

| czlonkowski n8n-mcp | Official Workflow-SDK MCP (here) |
|---------------------|----------------------------------|
| `search_nodes` | `n8n_mcp_search_nodes` |
| `get_node` (info/properties) | `n8n_mcp_get_node_types` |
| `validate_node` / `validate_node_operation` | `n8n_mcp_validate_node_config` |
| `validate_workflow` (JSON) | `n8n_mcp_validate_workflow` (SDK code) |
| `n8n_create_workflow` (JSON) | `n8n_mcp_create_workflow_from_code` (SDK code) |
| `n8n_update_partial_workflow` | `n8n_mcp_update_workflow` |
| `n8n_get_workflow` / `n8n_list_workflows` | `n8n_mcp_get_workflow_details` / `n8n_mcp_search_workflows` |
| `n8n_trigger_webhook_workflow` / test | `n8n_mcp_execute_workflow` / `n8n_mcp_test_workflow` |
| `n8n_list_executions` / `n8n_get_execution` | `n8n_mcp_search_executions` / `n8n_mcp_get_execution` |
| `n8n_autofix_workflow` | *(no equivalent)* — fix in SDK code, re-validate |
| `search_templates` / `get_template` | *(no equivalent)* — use `n8n_mcp_search_workflows` |

> Key difference: czlonkowski edits **JSON**; this server builds and edits via **SDK code**.
> When an adapted doc says "create/update the workflow JSON", instead write/modify the
> `@n8n/workflow-sdk` code and call the SDK-code tools above.

## When there is NO connected MCP

Fall back to the local `@n8n/workflow-sdk` (public npm, run with `tsx`) — build, validate,
and `.toJSON()` locally, then import the JSON into n8n manually. See
[workflow-sdk-overview.md](workflow-sdk-overview.md).
