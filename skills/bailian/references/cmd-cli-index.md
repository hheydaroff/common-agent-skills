# `bailian-cli` command reference

> Auto-generated from `packages/cli/src/commands.ts`. Do not edit by hand.
> Regenerate: `pnpm --filter bailian-cli run generate:reference`.

Command **details** are in sibling `<group>.md` files in this directory.
This index only covers groups owned by this skill. Other `bl` groups live in sibling bailian-* skills.
Use this index for the skill-scoped quick index and global flags.

## Quick index

| Command                         | Authentication | Description                                                                                                        | Detail                         |
| ------------------------------- | -------------- | ------------------------------------------------------------------------------------------------------------------ | ------------------------------ |
| `bl advisor recommend`          | API Key        | Recommend the best models for your use case (intent → routing → recall → score → rank, with agent clarification)   | [advisor.md](cmd-cli-advisor.md)       |
| `bl agents security alerts`     | API Key        | List Agent security alerts                                                                                         | [agents.md](cmd-cli-agents.md)         |
| `bl agents security overview`   | API Key        | Show the Agent security protection overview (last 24 hours)                                                        | [agents.md](cmd-cli-agents.md)         |
| `bl alert create`               | Console        | Create a model alert rule from an alert template                                                                   | [alert.md](cmd-cli-alert.md)           |
| `bl alert delete`               | Console        | Delete model alert rules                                                                                           | [alert.md](cmd-cli-alert.md)           |
| `bl alert disable`              | Console        | Disable a model alert rule (keeps the rule, stops notifications)                                                   | [alert.md](cmd-cli-alert.md)           |
| `bl alert enable`               | Console        | Enable a model alert rule                                                                                          | [alert.md](cmd-cli-alert.md)           |
| `bl alert history`              | Console        | List model alert history (firing and recovered events)                                                             | [alert.md](cmd-cli-alert.md)           |
| `bl alert list`                 | Console        | List model alert rules                                                                                             | [alert.md](cmd-cli-alert.md)           |
| `bl alert metrics`              | Console        | List metrics that alert rules can be created on, with supported aggregations                                       | [alert.md](cmd-cli-alert.md)           |
| `bl alert template create`      | Console        | Create a custom alert template (or copy an official one with --from)                                               | [alert.md](cmd-cli-alert.md)           |
| `bl alert template delete`      | Console        | Delete custom alert templates (official templates cannot be deleted)                                               | [alert.md](cmd-cli-alert.md)           |
| `bl alert template list`        | Console        | List alert templates (official and custom); pass --template-id for details                                         | [alert.md](cmd-cli-alert.md)           |
| `bl alert template update`      | Console        | Update a custom alert template (full replacement of conditions)                                                    | [alert.md](cmd-cli-alert.md)           |
| `bl alert update`               | Console        | Update a model alert rule (full replacement; same fields as create)                                                | [alert.md](cmd-cli-alert.md)           |
| `bl app call`                   | API Key        | Call a Bailian application (agent or workflow)                                                                     | [app.md](cmd-cli-app.md)               |
| `bl app list`                   | Console        | List Bailian applications                                                                                          | [app.md](cmd-cli-app.md)               |
| `bl auth generate-access-token` | No Auth        | Generate a CLI access token using OpenAPI AK/SK                                                                    | [auth.md](cmd-cli-auth.md)             |
| `bl auth login`                 | No Auth        | Authenticate with API key, console browser login, or OpenAPI AK/SK (credentials can coexist)                       | [auth.md](cmd-cli-auth.md)             |
| `bl auth logout`                | No Auth        | Clear stored credentials; full logout also clears the model Base URL                                               | [auth.md](cmd-cli-auth.md)             |
| `bl auth status`                | No Auth        | Show current authentication state                                                                                  | [auth.md](cmd-cli-auth.md)             |
| `bl batch cancel`               | API Key        | Request cancellation of a Batch task                                                                               | [batch.md](cmd-cli-batch.md)           |
| `bl batch convert`              | No Auth        | Build Batch JSONL from CSV locally                                                                                 | [batch.md](cmd-cli-batch.md)           |
| `bl batch create`               | API Key        | Upload or reference input and create an asynchronous Batch task                                                    | [batch.md](cmd-cli-batch.md)           |
| `bl batch download`             | API Key        | Download original Batch results/errors, optionally export CSV                                                      | [batch.md](cmd-cli-batch.md)           |
| `bl batch get`                  | API Key        | Get Batch task details, optionally following progress                                                              | [batch.md](cmd-cli-batch.md)           |
| `bl batch list`                 | API Key        | List one page of Batch tasks                                                                                       | [batch.md](cmd-cli-batch.md)           |
| `bl cmodel base-models`         | Console        | List base models that can be imported as custom models                                                             | [cmodel.md](cmd-cli-cmodel.md)         |
| `bl cmodel delete`              | API Key        | Delete a custom model and its Bailian-side import record                                                           | [cmodel.md](cmd-cli-cmodel.md)         |
| `bl cmodel get`                 | API Key        | Get details of a custom model (import job)                                                                         | [cmodel.md](cmd-cli-cmodel.md)         |
| `bl cmodel import`              | API Key        | Import a custom model from OSS (creates an import job)                                                             | [cmodel.md](cmd-cli-cmodel.md)         |
| `bl cmodel list`                | API Key        | List custom models (import jobs)                                                                                   | [cmodel.md](cmd-cli-cmodel.md)         |
| `bl cmodel watch`               | API Key        | Probe a custom model's import status (default: single non-blocking fetch). Pass --follow to poll until terminal.   | [cmodel.md](cmd-cli-cmodel.md)         |
| `bl config agent`               | No Auth        | Configure a coding agent to use DashScope API                                                                      | [config.md](cmd-cli-config.md)         |
| `bl config list`                | No Auth        | List config profiles and show the active profile                                                                   | [config.md](cmd-cli-config.md)         |
| `bl config set`                 | No Auth        | Set a config value                                                                                                 | [config.md](cmd-cli-config.md)         |
| `bl config show`                | No Auth        | Display current configuration                                                                                      | [config.md](cmd-cli-config.md)         |
| `bl config ui`                  | No Auth        | Open a local web UI to manage config profiles                                                                      | [config.md](cmd-cli-config.md)         |
| `bl config use`                 | No Auth        | Set the active config profile                                                                                      | [config.md](cmd-cli-config.md)         |
| `bl console call`               | Console        | Call a Bailian console API via the CLI gateway                                                                     | [console.md](cmd-cli-console.md)       |
| `bl decision`                   | API Key        | Run the decision model: typed choice / noul / score answers with probabilities                                     | [decision.md](cmd-cli-decision.md)     |
| `bl file upload`                | API Key        | Upload a local file to DashScope temporary storage (48h)                                                           | [file.md](cmd-cli-file.md)             |
| `bl log audit count`            | Console        | Count model audit logs in a time range (useful before exporting)                                                   | [log.md](cmd-cli-log.md)               |
| `bl log audit disable`          | Console        | Disable audit log delivery for all models in the workspace                                                         | [log.md](cmd-cli-log.md)               |
| `bl log audit enable`           | Console        | Enable audit log delivery to SLS (SLR authorization → SLS instance → log switch)                                   | [log.md](cmd-cli-log.md)               |
| `bl log audit get`              | Console        | Show a single audit log entry with its raw origin record                                                           | [log.md](cmd-cli-log.md)               |
| `bl log audit list`             | Console        | Query model audit logs (call metadata; request/response content is not recorded)                                   | [log.md](cmd-cli-log.md)               |
| `bl log inference count`        | Console        | Count model inference logs in a time range (useful before exporting)                                               | [log.md](cmd-cli-log.md)               |
| `bl log inference disable`      | Console        | Disable inference log delivery for all models in the workspace                                                     | [log.md](cmd-cli-log.md)               |
| `bl log inference enable`       | Console        | Enable inference log delivery to SLS (SLR authorization → SLS instance → log switch)                               | [log.md](cmd-cli-log.md)               |
| `bl log inference get`          | Console        | Show a single inference log entry with full request/response content                                               | [log.md](cmd-cli-log.md)               |
| `bl log inference list`         | Console        | Query model inference logs (requires inference log delivery; use `log inference get` for request/response content) | [log.md](cmd-cli-log.md)               |
| `bl log status`                 | Console        | Show model log delivery status (SLS authorization, audit / inference service and switches)                         | [log.md](cmd-cli-log.md)               |
| `bl log trace get`              | Console        | Show a single call trace with its span tree                                                                        | [log.md](cmd-cli-log.md)               |
| `bl log trace list`             | Console        | List call traces for a model or app                                                                                | [log.md](cmd-cli-log.md)               |
| `bl log trace stats`            | Console        | Show per-resource trace statistics (calls, tokens, latency)                                                        | [log.md](cmd-cli-log.md)               |
| `bl mcp call`                   | API Key        | Call a tool on an MCP server (tools/call)                                                                          | [mcp.md](cmd-cli-mcp.md)               |
| `bl mcp connect`                | API Key        | Register a Bailian MCP server in an Agent's native configuration                                                   | [mcp.md](cmd-cli-mcp.md)               |
| `bl mcp disconnect`             | No Auth        | Remove an unchanged MCP registration previously managed by bailian-cli                                             | [mcp.md](cmd-cli-mcp.md)               |
| `bl mcp list`                   | Console        | List MCP servers activated under your Bailian account                                                              | [mcp.md](cmd-cli-mcp.md)               |
| `bl mcp tools`                  | API Key        | List tools exposed by an MCP server (tools/list)                                                                   | [mcp.md](cmd-cli-mcp.md)               |
| `bl model code`                 | No Auth        | Print a ready-to-run SDK sample for calling a model                                                                | [model.md](cmd-cli-model.md)           |
| `bl model list`                 | No Auth        | Browse model families or show detailed model info in the Bailian model marketplace                                 | [model.md](cmd-cli-model.md)           |
| `bl model search`               | No Auth        | Search the model catalog by keyword, ranked by relevance                                                           | [model.md](cmd-cli-model.md)           |
| `bl monitor delivery disable`   | Console        | Disable monitor delivery for all models in the workspace                                                           | [monitor.md](cmd-cli-monitor.md)       |
| `bl monitor delivery enable`    | Console        | Activate monitoring delivery: CMS SLR authorization, CMS service, and the dedicated Prometheus instance            | [monitor.md](cmd-cli-monitor.md)       |
| `bl monitor delivery status`    | Console        | Show monitoring delivery (Prometheus instance) status                                                              | [monitor.md](cmd-cli-monitor.md)       |
| `bl monitor errors`             | Console        | Show failure breakdown by HTTP status code and error code                                                          | [monitor.md](cmd-cli-monitor.md)       |
| `bl monitor metrics`            | Console        | Query time-series monitor metrics (RPM/TPM, latency percentiles, token usage)                                      | [monitor.md](cmd-cli-monitor.md)       |
| `bl monitor models`             | Console        | List per-model / per-API-key call statistics with server-side sort and paging                                      | [monitor.md](cmd-cli-monitor.md)       |
| `bl monitor overview`           | Console        | Show aggregated model call statistics (calls, failures, latency, token usage)                                      | [monitor.md](cmd-cli-monitor.md)       |
| `bl parsex extract result`      | API Key        | Query ParseX extraction status, fields and citations                                                               | [parsex.md](cmd-cli-parsex.md)         |
| `bl parsex extract submit`      | API Key        | Submit ParseX structured field extraction                                                                          | [parsex.md](cmd-cli-parsex.md)         |
| `bl parsex parse result`        | API Key        | Query ParseX parsing status, results or a result slice                                                             | [parsex.md](cmd-cli-parsex.md)         |
| `bl parsex parse submit`        | API Key        | Submit a ParseX document or media parsing task                                                                     | [parsex.md](cmd-cli-parsex.md)         |
| `bl permission grant`           | API Key        | Grant model permissions (inference / finetune / deploy)                                                            | [permission.md](cmd-cli-permission.md) |
| `bl permission list`            | API Key        | List model permissions (inference / fine-tune / deploy) in the workspace                                           | [permission.md](cmd-cli-permission.md) |
| `bl permission revoke`          | API Key        | Revoke model permissions (inference / finetune / deploy)                                                           | [permission.md](cmd-cli-permission.md) |
| `bl pipeline run`               | No Auth        | Run a pipeline workflow definition                                                                                 | [pipeline.md](cmd-cli-pipeline.md)     |
| `bl pipeline validate`          | No Auth        | Validate a pipeline definition without executing                                                                   | [pipeline.md](cmd-cli-pipeline.md)     |
| `bl plugin install`             | No Auth        | Install or upgrade an allowlisted Command Pack                                                                     | [plugin.md](cmd-cli-plugin.md)         |
| `bl plugin link`                | No Auth        | Link an allowlisted local Command Pack for development                                                             | [plugin.md](cmd-cli-plugin.md)         |
| `bl plugin list`                | No Auth        | List installed Command Packs and their load status                                                                 | [plugin.md](cmd-cli-plugin.md)         |
| `bl plugin remove`              | No Auth        | Remove an installed Command Pack                                                                                   | [plugin.md](cmd-cli-plugin.md)         |
| `bl quota check`                | Console        | Check current usage against rate limits                                                                            | [quota.md](cmd-cli-quota.md)           |
| `bl quota delete`               | API Key        | Clear all custom rate limits (QPM/TPM) for a model                                                                 | [quota.md](cmd-cli-quota.md)           |
| `bl quota history`              | Console        | View quota change history                                                                                          | [quota.md](cmd-cli-quota.md)           |
| `bl quota list`                 | API Key        | View model rate limits (QPM/TPM, account and workspace level)                                                      | [quota.md](cmd-cli-quota.md)           |
| `bl quota update`               | API Key        | Update model rate limits (QPM/TPM)                                                                                 | [quota.md](cmd-cli-quota.md)           |
| `bl search web`                 | API Key        | Search the web via a chat model with built-in web search (default) or the DashScope MCP WebSearch service          | [search.md](cmd-cli-search.md)         |
| `bl skill add`                  | No Auth        | Install skills from the Bailian skill registry into local agents                                                   | [skill.md](cmd-cli-skill.md)           |
| `bl skill init`                 | No Auth        | Install all bailian-* skills (one-shot bootstrap for new environments)                                             | [skill.md](cmd-cli-skill.md)           |
| `bl skill list`                 | No Auth        | List registry skills and diff against local installs                                                               | [skill.md](cmd-cli-skill.md)           |
| `bl skill remove`               | No Auth        | Remove locally installed skills (registry is untouched)                                                            | [skill.md](cmd-cli-skill.md)           |
| `bl skill update`               | No Auth        | Update installed skills to the latest registry versions                                                            | [skill.md](cmd-cli-skill.md)           |
| `bl text chat`                  | API Key        | Send a text model request (OpenAI compatible, DashScope)                                                           | [text.md](cmd-cli-text.md)             |
| `bl token-plan add-member`      | AK/SK          | Add a member to a Token Plan organization                                                                          | [token-plan.md](cmd-cli-token-plan.md) |
| `bl token-plan assign-seats`    | AK/SK          | Batch assign Token Plan seats to members                                                                           | [token-plan.md](cmd-cli-token-plan.md) |
| `bl token-plan create-key`      | AK/SK          | Create a Token Plan API key for a seat                                                                             | [token-plan.md](cmd-cli-token-plan.md) |
| `bl token-plan harness-quota`   | Console        | Show Token Plan harness entitlement quota usage                                                                    | [token-plan.md](cmd-cli-token-plan.md) |
| `bl token-plan list-seats`      | AK/SK          | List Token Plan subscription seat details                                                                          | [token-plan.md](cmd-cli-token-plan.md) |
| `bl update`                     | No Auth        | Update the CLI to the latest or a specified version                                                                | [update.md](cmd-cli-update.md)         |
| `bl usage coding-plan`          | Console        | Show Coding Plan quota usage                                                                                       | [usage.md](cmd-cli-usage.md)           |
| `bl usage free`                 | Console        | Query free-tier quota for models (all models if --model is omitted)                                                | [usage.md](cmd-cli-usage.md)           |
| `bl usage freetier`             | Console        | Enable or disable auto-stop for free-tier models. Enables by default; use --off to disable                         | [usage.md](cmd-cli-usage.md)           |
| `bl usage stats`                | Console        | Query model usage statistics                                                                                       | [usage.md](cmd-cli-usage.md)           |
| `bl usage summary`              | Console        | Show a unified usage summary: free-tier quota and recent usage overview                                            | [usage.md](cmd-cli-usage.md)           |
| `bl usage token-plan`           | Console        | Show Token Plan quota usage                                                                                        | [usage.md](cmd-cli-usage.md)           |
| `bl workspace init`             | No Auth        | Initialize Bailian workspace and activate postpaid services                                                        | [workspace.md](cmd-cli-workspace.md)   |
| `bl workspace list`             | Console        | List all workspaces                                                                                                | [workspace.md](cmd-cli-workspace.md)   |

## By group

| Group        | Commands                                                                                                                                                                                                                     | Reference                      |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------ |
| `advisor`    | `recommend`                                                                                                                                                                                                                  | [advisor.md](cmd-cli-advisor.md)       |
| `agents`     | `security alerts`, `security overview`                                                                                                                                                                                       | [agents.md](cmd-cli-agents.md)         |
| `alert`      | `create`, `delete`, `disable`, `enable`, `history`, `list`, `metrics`, `template create`, `template delete`, `template list`, `template update`, `update`                                                                    | [alert.md](cmd-cli-alert.md)           |
| `app`        | `call`, `list`                                                                                                                                                                                                               | [app.md](cmd-cli-app.md)               |
| `auth`       | `generate-access-token`, `login`, `logout`, `status`                                                                                                                                                                         | [auth.md](cmd-cli-auth.md)             |
| `batch`      | `cancel`, `convert`, `create`, `download`, `get`, `list`                                                                                                                                                                     | [batch.md](cmd-cli-batch.md)           |
| `cmodel`     | `base-models`, `delete`, `get`, `import`, `list`, `watch`                                                                                                                                                                    | [cmodel.md](cmd-cli-cmodel.md)         |
| `config`     | `agent`, `list`, `set`, `show`, `ui`, `use`                                                                                                                                                                                  | [config.md](cmd-cli-config.md)         |
| `console`    | `call`                                                                                                                                                                                                                       | [console.md](cmd-cli-console.md)       |
| `decision`   | `(root)`                                                                                                                                                                                                                     | [decision.md](cmd-cli-decision.md)     |
| `file`       | `upload`                                                                                                                                                                                                                     | [file.md](cmd-cli-file.md)             |
| `log`        | `audit count`, `audit disable`, `audit enable`, `audit get`, `audit list`, `inference count`, `inference disable`, `inference enable`, `inference get`, `inference list`, `status`, `trace get`, `trace list`, `trace stats` | [log.md](cmd-cli-log.md)               |
| `mcp`        | `call`, `connect`, `disconnect`, `list`, `tools`                                                                                                                                                                             | [mcp.md](cmd-cli-mcp.md)               |
| `model`      | `code`, `list`, `search`                                                                                                                                                                                                     | [model.md](cmd-cli-model.md)           |
| `monitor`    | `delivery disable`, `delivery enable`, `delivery status`, `errors`, `metrics`, `models`, `overview`                                                                                                                          | [monitor.md](cmd-cli-monitor.md)       |
| `parsex`     | `extract result`, `extract submit`, `parse result`, `parse submit`                                                                                                                                                           | [parsex.md](cmd-cli-parsex.md)         |
| `permission` | `grant`, `list`, `revoke`                                                                                                                                                                                                    | [permission.md](cmd-cli-permission.md) |
| `pipeline`   | `run`, `validate`                                                                                                                                                                                                            | [pipeline.md](cmd-cli-pipeline.md)     |
| `plugin`     | `install`, `link`, `list`, `remove`                                                                                                                                                                                          | [plugin.md](cmd-cli-plugin.md)         |
| `quota`      | `check`, `delete`, `history`, `list`, `update`                                                                                                                                                                               | [quota.md](cmd-cli-quota.md)           |
| `search`     | `web`                                                                                                                                                                                                                        | [search.md](cmd-cli-search.md)         |
| `skill`      | `add`, `init`, `list`, `remove`, `update`                                                                                                                                                                                    | [skill.md](cmd-cli-skill.md)           |
| `text`       | `chat`                                                                                                                                                                                                                       | [text.md](cmd-cli-text.md)             |
| `token-plan` | `add-member`, `assign-seats`, `create-key`, `harness-quota`, `list-seats`                                                                                                                                                    | [token-plan.md](cmd-cli-token-plan.md) |
| `update`     | `(root)`                                                                                                                                                                                                                     | [update.md](cmd-cli-update.md)         |
| `usage`      | `coding-plan`, `free`, `freetier`, `stats`, `summary`, `token-plan`                                                                                                                                                          | [usage.md](cmd-cli-usage.md)           |
| `workspace`  | `init`, `list`                                                                                                                                                                                                               | [workspace.md](cmd-cli-workspace.md)   |

## Global flags

Available on every command (in addition to command-specific flags):

| Flag                  | Type   | Required | Description                                               |
| --------------------- | ------ | -------- | --------------------------------------------------------- |
| `--introspect`        | switch | no       | Print the machine-readable command schema (JSON) and exit |
| `--output <format>`   | string | no       | Output format: text, json                                 |
| `--timeout <seconds>` | number | no       | Request timeout                                           |
| `--quiet`             | switch | no       | Suppress non-essential output                             |
| `--verbose`           | switch | no       | Print HTTP request/response details                       |
| `--dry-run`           | switch | no       | Dry run mode                                              |
| `--config <name>`     | string | no       | Use a config profile for this command                     |
| `--help`              | switch | no       | Show help                                                 |
| `--version`           | switch | no       | Print version                                             |

## Model auth flags

Available on model-domain commands (API-key auth); also listed per command below:

| Flag               | Type   | Required | Description  |
| ------------------ | ------ | -------- | ------------ |
| `--api-key <key>`  | string | no       | API key      |
| `--base-url <url>` | string | no       | API base URL |

## Console auth flags

Available on console-domain commands (console login auth); also listed per command below:

| Flag                           | Type   | Required | Description                                              |
| ------------------------------ | ------ | -------- | -------------------------------------------------------- |
| `--console-region <region>`    | string | no       | Console gateway region (e.g. cn-beijing, ap-southeast-1) |
| `--console-site <site>`        | string | no       | Console site: domestic, international                    |
| `--console-switch-agent <uid>` | number | no       | Switch agent UID for delegated access                    |
| `--workspace-id <id>`          | string | no       | Workspace ID (env: BAILIAN_WORKSPACE_ID)                 |

## OpenAPI auth flags

Available on OpenAPI-domain commands (AK/SK auth); also listed per command below:

| Flag                        | Type   | Required | Description                                                            |
| --------------------------- | ------ | -------- | ---------------------------------------------------------------------- |
| `--access-key-id <key>`     | string | no       | Alibaba Cloud Access Key ID (env: ALIBABA_CLOUD_ACCESS_KEY_ID)         |
| `--access-key-secret <key>` | string | no       | Alibaba Cloud Access Key Secret (env: ALIBABA_CLOUD_ACCESS_KEY_SECRET) |
| `--security-token <token>`  | string | no       | Alibaba Cloud STS Security Token (env: ALIBABA_CLOUD_SECURITY_TOKEN)   |

## Notes

- Console commands (`app list`, `usage free`, `console call`) require `bl auth login --console`.
- Most API commands use `DASHSCOPE_API_KEY` or `bl auth login --api-key`.
- Token Plan commands use OpenAPI AK/SK via `bl auth login --open-api` or `ALIBABA_CLOUD_ACCESS_KEY_ID` / `ALIBABA_CLOUD_ACCESS_KEY_SECRET`.
- Default output: **text** unless explicitly set to `json` with `--output`, `DASHSCOPE_OUTPUT`, or config.
