---
name: databricks-data-explore
description: "Explore data in a Databricks workspace using SQL or Python. Authenticate, pick a profile, find tables, discover schemas, and run multiple ad-hoc SQL queries to answer analytical questions — via the Databricks CLI or the Python SDK. Use when the user wants to query Databricks/Unity Catalog data, investigate a question with several SQL queries, inspect or compare table schemas, validate data, pull results into Python/pandas, or set up Databricks CLI auth. Triggers: 'query Databricks', 'explore Databricks tables', 'discover schema', 'Unity Catalog', 'run SQL on the warehouse', 'analyze this in Databricks', 'databricks auth'."
compatibility: Requires databricks CLI 1.0+ (or >= v0.292.0). Python paths need databricks-sdk (and optionally databricks-sql-connector).
metadata:
  version: "0.2.0"
---

# Databricks Data Exploration

Answer analytical questions against a Databricks workspace by running SQL — from the **CLI** for quick ad-hoc queries, or from **Python** when you need to loop many queries and process results programmatically.

## Prerequisites

1. **CLI installed**: Run `databricks --version`. CLI 1.0+ is GA; treat anything `< v0.292.0` as too old.
   - **If missing or outdated: STOP. Do not work around a missing CLI.** Read [CLI Installation](references/databricks-cli-install.md) and guide the user.
   - In sandboxed environments (Cursor, containers), install commands may be blocked — present the command and ask the user to run it themselves.
2. **Authenticated**: `databricks auth profiles` — if not, see [CLI Authentication](references/databricks-cli-auth.md). Both the CLI and the Python SDK read the same `~/.databrickscfg` profiles.

## Profile Selection - CRITICAL

**NEVER auto-select a profile.**
1. List profiles: `databricks auth profiles`
2. Present ALL profiles to the user with workspace URLs
3. Let the user choose (even if only one exists)
4. Offer to create a new profile if needed

## Separate Shell Sessions - IMPORTANT

Each Bash command runs in a **separate shell session**, so env vars don't persist:

```bash
databricks warehouses list --profile my-workspace                          # WORKS: --profile flag
export DATABRICKS_CONFIG_PROFILE=my-workspace && databricks warehouses list # WORKS: chained with &&
# DOES NOT WORK across two commands: a separate `export` then a separate databricks call
```

---

## Mode A — SQL via the CLI (default for quick exploration)

> ⚠️ The data tools live under the **`experimental`** namespace and stay there even in CLI 1.0+ (by design). Use them as written.

```bash
# discover table structure (columns, types, 5 sample rows, null counts, row count)
databricks experimental aitools tools discover-schema catalog.schema.table --profile <PROFILE>

# run ad-hoc SQL (auto-detects a warehouse unless DATABRICKS_WAREHOUSE_ID is set)
databricks experimental aitools tools query "SELECT * FROM catalog.schema.table LIMIT 10" --profile <PROFILE>

# which warehouse will be used?
databricks experimental aitools tools get-default-warehouse --profile <PROFILE>
```

**Don't know which catalog/schema holds the data?** Search `information_schema` — never iterate `catalogs`→`schemas`→`tables` by hand:

```bash
databricks experimental aitools tools query \
  "SELECT table_catalog, table_schema, table_name FROM system.information_schema.tables WHERE table_name LIKE '%keyword%'" \
  --profile <PROFILE>
```

Use `--output json` to get parseable results (pipe to `jq`). See [Data Exploration](references/data-exploration.md) for full flags, examples, and troubleshooting.

---

## Mode B — SQL via Python (for multi-query / programmatic work)

Use Python when answering a question needs **many queries**, result post-processing, or pandas. The **`databricks-sdk`** Statement Execution API is the default — it reuses your CLI profile (no host/token wiring):

```python
# pip install databricks-sdk
from databricks.sdk import WorkspaceClient

w = WorkspaceClient(profile="<PROFILE>")          # same profile as the CLI
wh = w.warehouses.list()[0].id                     # or hardcode a warehouse id

def q(sql: str):
    r = w.statement_execution.execute_statement(statement=sql, warehouse_id=wh, wait_timeout="30s")
    cols = [c.name for c in r.manifest.schema.columns]
    return [dict(zip(cols, row)) for row in (r.result.data_array or [])]

print(q("SELECT count(*) AS n FROM samples.nyctaxi.trips"))
```

Switch to **`databricks-sql-connector`** only when you need **pandas / Arrow / large result sets** (CloudFetch). See [Python Data Access](references/python-data-access.md) for both libraries, large-result handling, and a reusable multi-query helper.

---

## Workflow — answering a question with multiple queries

1. **Locate** the data: `information_schema` keyword search (Mode A) if the table is unknown.
2. **Discover schema** of the candidate table(s) before writing complex SQL (`discover-schema`).
3. **Explore iteratively**, always with `LIMIT` while investigating:
   - shape/size → `SELECT count(*)`, date ranges, distinct counts
   - distributions → `GROUP BY ... ORDER BY count DESC`
   - drill into anomalies found in earlier results
4. **Synthesize**: combine the query results into the answer. In Python, accumulate results across queries; in CLI, use `--output json` and parse.
5. Prefer **one warehouse** for a session and discover it once (`get-default-warehouse`) to avoid cold-starts.

## Quick Reference (catalog/table commands)

```bash
databricks current-user me --profile <PROFILE>
databricks warehouses list --profile <PROFILE>
databricks catalogs list --profile <PROFILE>

# ⚠️ Unity Catalog uses POSITIONAL args, NOT flags:
databricks schemas list <CATALOG> --profile <PROFILE>
databricks tables list <CATALOG> <SCHEMA> --profile <PROFILE>
databricks tables get <CATALOG>.<SCHEMA>.<TABLE> --profile <PROFILE>

# ❌ These DON'T EXIST:
# databricks schemas list --catalog-name <C>   ← FAILS (use positional)
# databricks sql-warehouses list               ← use `warehouses list`
# databricks execute-statement / sql execute   ← use `experimental aitools tools query`
```

## Troubleshooting

| Error | Solution |
|-------|----------|
| `cannot configure default credentials` | Use `--profile` / `WorkspaceClient(profile=...)`, or authenticate first |
| `configuration does not support OAuth tokens` | Re-auth: `databricks auth login --host <URL> --profile <PROFILE>`. See [CLI Authentication](references/databricks-cli-auth.md). |
| `No available SQL warehouse found` | `databricks warehouses list` and start one, or set `DATABRICKS_WAREHOUSE_ID` |
| `PERMISSION_DENIED` | Check Unity Catalog / warehouse grants |
| `RESOURCE_DOES_NOT_EXIST` / `TABLE_OR_VIEW_NOT_FOUND` | Verify `CATALOG.SCHEMA.TABLE` and profile |

## Reference Files

| File | When to load |
|------|--------------|
| [references/databricks-cli-install.md](references/databricks-cli-install.md) | First-time setup; CLI missing or outdated |
| [references/databricks-cli-auth.md](references/databricks-cli-auth.md) | Auth issues, new workspace, profile management (CLI + Python) |
| [references/data-exploration.md](references/data-exploration.md) | CLI exploration: full flags, examples, troubleshooting |
| [references/python-data-access.md](references/python-data-access.md) | Querying from Python: SDK vs sql-connector, multi-query helper, large results |
