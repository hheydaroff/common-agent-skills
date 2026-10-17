# Source playbooks

The `why` skill spawns one investigator per available evidence category, each reading a single source-specific playbook below. The playbooks are concrete examples for common MCPs; adapt them for a different MCP in the same category.

## Calling MCPs in pi

These playbooks were written against named MCP servers (Linear, Notion, Slack, Datadog, Sentry, Databricks). In pi, MCP servers are built in and their tools are real tools named `mcp__<server>__<tool>`, called from a `codemode` script:

- `ALL_TOOLS` — every tool; group by the `mcp__<server>__` prefix to list connected servers.
- `await searchTools("<query>", { limit })` — find tools by name/description.
- `await describeNamespace("mcp__<server>")` / `await describeTool("<name>")` — list a server's tools / show a tool's parameters.
- `await tools.mcp__<server>__<tool>({ ... })` — call a tool (args is a plain object).
- Auth-protected servers: `/mcp login <server>` (see the `mcp-tools` skill).

So wherever a playbook says "use the Linear MCP `get_issue`", in pi that is `await tools.mcp__linear__get_issue({ ... })`. Source control (git / `gh`) is the exception — run it with the `bash` tool.

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
