# Source playbooks

The `why` skill spawns one investigator per available evidence category, each reading a single source-specific playbook below. The playbooks are concrete examples for common MCPs; adapt them for a different MCP in the same category.

## Calling MCPs in pi

These playbooks were written against named MCP servers (Linear, Notion, Slack, Datadog, Sentry, Databricks). In pi you do **not** call those servers directly — every MCP server is reached through the **`mcp` gateway tool**:

- `mcp({})` — list connected servers and tool counts.
- `mcp({ server: "<name>" })` — list a server's tools.
- `mcp({ search: "<query>" })` — search tools across all servers by name/description.
- `mcp({ describe: "<tool>" })` — show a tool's parameters.
- `mcp({ tool: "<tool>", args: '{"k":"v"}' })` — call a tool (args is a JSON string).
- Auth-protected servers use pi's `/mcp-auth` flow.

So wherever a playbook says "use the Linear MCP `get_issue`", in pi that is `mcp({ tool: "get_issue", args: '{...}' })` (optionally with `server:` to disambiguate). Source control (git / `gh`) is the exception — run it with the `bash` tool, not the gateway.

| Category | Playbook | Example MCP it documents |
|---|---|---|
| Source control history | [`sources/code-archaeology.md`](./sources/code-archaeology.md) | git, `gh` (via `bash`) |
| Issue / ticket tracker | [`sources/linear.md`](./sources/linear.md) | Linear (adapt for Jira, GitHub Issues, Plane, Shortcut) |
| Long-form documents | [`sources/notion.md`](./sources/notion.md) | Notion (adapt for Confluence, Google Docs, Coda) |
| Real-time team chat | [`sources/slack.md`](./sources/slack.md) | Slack (adapt for Discord, Microsoft Teams, Mattermost) |
| Infrastructure observability | [`sources/datadog.md`](./sources/datadog.md) | Datadog (adapt for New Relic, Honeycomb, Grafana, Splunk) |
| Error / exception tracking | [`sources/sentry.md`](./sources/sentry.md) | Sentry (adapt for Rollbar, Bugsnag, Airbrake) |
| Product analytics warehouse | [`sources/databricks.md`](./sources/databricks.md) | Databricks SQL (adapt for Snowflake, BigQuery, ClickHouse, dbt) |

Cross-cutting:

- [`sources/incident-postmortem.md`](./sources/incident-postmortem.md). Add this if the target code looks defensive (null checks, retry, timeout, rate limit, feature flag, egress guard, OOM handler).
