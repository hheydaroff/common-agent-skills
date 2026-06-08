# Python Data Access for Databricks

Run SQL against a Databricks SQL warehouse from Python. Two official libraries, plus a lightweight wrapper. All authenticate against the same `~/.databrickscfg` profiles used by the CLI.

## Which library?

| Library | Import | Use it when | Result style |
|---------|--------|-------------|--------------|
| **databricks-sdk** (Statement Execution API) | `from databricks.sdk import WorkspaceClient` | Default for agents. Many small/medium queries, programmatic looping, no extra deps, auto-auth from profile. | JSON arrays (rows as lists) |
| **databricks-sql-connector** | `from databricks import sql` | You need **pandas/Arrow**, **large result sets** (CloudFetch), or a familiar DB-API cursor. | DB-API rows / Arrow / pandas |
| **databricks-labs-lsql** | `from databricks.labs.lsql.backends import StatementExecutionBackend` | Minimal `fetch_all`/`execute` over the SDK; serverless/short-lived apps. | Row-like objects |

Rule of thumb: start with **databricks-sdk**; switch to **databricks-sql-connector** the moment you need DataFrames or to pull a lot of rows.

---

## databricks-sdk — Statement Execution API (default)

```bash
pip install databricks-sdk
```

```python
from databricks.sdk import WorkspaceClient

# Auth: reuses your CLI profile from ~/.databrickscfg (no host/token needed).
# Profile precedence: explicit profile=... > DATABRICKS_CONFIG_PROFILE env > DEFAULT.
w = WorkspaceClient(profile="my-workspace")

# Pick a warehouse once per session (avoid repeated cold starts).
warehouse_id = w.warehouses.list()[0].id   # or a known id string

def query(sql: str):
    """Run SQL, return a list of dict rows. Good for small/medium result sets (<= 25 MiB INLINE)."""
    resp = w.statement_execution.execute_statement(
        statement=sql,
        warehouse_id=warehouse_id,
        wait_timeout="30s",          # 5s..50s; blocks up to this long, else returns a statement_id
        # catalog="my_catalog", schema="my_schema",   # optional default namespace
        # row_limit=1000,                              # cap rows server-side
    )
    if resp.result is None or resp.result.data_array is None:
        return []
    cols = [c.name for c in resp.manifest.schema.columns]
    return [dict(zip(cols, row)) for row in resp.result.data_array]

print(query("SELECT vendor_id, count(*) AS trips FROM samples.nyctaxi.trips GROUP BY vendor_id"))
```

### Parameterized queries (avoid SQL injection)

```python
from databricks.sdk.service.sql import StatementParameterListItem

resp = w.statement_execution.execute_statement(
    statement="SELECT * FROM samples.nyctaxi.trips WHERE pickup_zip = :zip LIMIT :n",
    warehouse_id=warehouse_id,
    parameters=[
        StatementParameterListItem(name="zip", value="10103"),
        StatementParameterListItem(name="n", value="5", type="INT"),
    ],
)
```

### Long-running or large queries (polling)

`execute_statement` returns a `statement_id` if it doesn't finish within `wait_timeout`. Poll it, and for big results fetch chunks:

```python
import time

resp = w.statement_execution.execute_statement(statement=big_sql, warehouse_id=warehouse_id, wait_timeout="0s")
sid = resp.statement_id
while resp.status.state.value in ("PENDING", "RUNNING"):
    time.sleep(2)
    resp = w.statement_execution.get_statement(sid)

# INLINE results cap at 25 MiB. For larger sets use disposition EXTERNAL_LINKS and iterate chunks:
#   resp.result.next_chunk_index / w.statement_execution.get_statement_result_chunk_n(sid, i)
# Results are retained ~1 hour after success.
```

Notes:
- INLINE + JSON_ARRAY is simplest and works for result sets up to 25 MiB. Beyond that, request `disposition=EXTERNAL_LINKS` (supports JSON_ARRAY / ARROW_STREAM / CSV, up to 100 GiB) and fetch via the returned URLs.
- Max query text size is 16 MiB.

---

## databricks-sql-connector — pandas / Arrow / large pulls

```bash
pip install "databricks-sql-connector[pyarrow]"
```

Needs `server_hostname` and `http_path` (HTTP Path of the SQL warehouse, e.g. `/sql/1.0/warehouses/abc123`), plus a token. Find the HTTP path in the warehouse's **Connection details** in the UI.

```python
import os
from databricks import sql

with sql.connect(
    server_hostname=os.environ["DATABRICKS_SERVER_HOSTNAME"],   # adb-....azuredatabricks.net (no https://)
    http_path=os.environ["DATABRICKS_HTTP_PATH"],               # /sql/1.0/warehouses/<id>
    access_token=os.environ["DATABRICKS_TOKEN"],
) as connection:
    with connection.cursor() as cursor:
        # Native parameterized query (connector >= 3.0.0) — safe from injection
        cursor.execute("SELECT * FROM samples.nyctaxi.trips WHERE pickup_zip = ? LIMIT ?", ["10103", 5])
        for row in cursor.fetchall():
            print(row)

        # Large results → Arrow → pandas (needs pyarrow; CloudFetch streams efficiently)
        cursor.execute("SELECT * FROM samples.nyctaxi.trips")
        df = cursor.fetchall_arrow().to_pandas()
```

OAuth M2M auth is supported (connector >= 2.5.0) and also needs `databricks-sdk` installed.

---

## Multi-query exploration helper (databricks-sdk)

Reusable pattern for answering one question with several queries and keeping the results together:

```python
from databricks.sdk import WorkspaceClient

class Explorer:
    def __init__(self, profile, warehouse_id=None):
        self.w = WorkspaceClient(profile=profile)
        self.wh = warehouse_id or self.w.warehouses.list()[0].id

    def q(self, sql):
        r = self.w.statement_execution.execute_statement(
            statement=sql, warehouse_id=self.wh, wait_timeout="30s")
        if not r.result or not r.result.data_array:
            return []
        cols = [c.name for c in r.manifest.schema.columns]
        return [dict(zip(cols, row)) for row in r.result.data_array]

ex = Explorer(profile="my-workspace")

# 1. find candidate tables
tables = ex.q("SELECT table_catalog, table_schema, table_name "
              "FROM system.information_schema.tables WHERE table_name LIKE '%order%'")

# 2. inspect + 3. drill down, accumulating answers
n = ex.q("SELECT count(*) AS n FROM main.sales.orders")
by_status = ex.q("SELECT status, count(*) AS c FROM main.sales.orders GROUP BY status ORDER BY c DESC")
```

---

## Troubleshooting (Python)

| Symptom | Fix |
|---------|-----|
| `default auth: cannot configure default credentials` | Pass `WorkspaceClient(profile="...")`, or set `DATABRICKS_CONFIG_PROFILE`. Make sure the profile exists (`databricks auth profiles`). |
| `module 'databricks.sdk.service.sql' has no attribute ...` | Upgrade: `pip install -U databricks-sdk`. |
| Result missing / empty | Statement may still be running — poll `get_statement(statement_id)` until state is `SUCCEEDED`. |
| Large result truncated | INLINE caps at 25 MiB — use `disposition=EXTERNAL_LINKS`, or switch to `databricks-sql-connector` with Arrow/CloudFetch. |
| Connector: which `http_path`? | Warehouse UI → Connection details → HTTP Path (`/sql/1.0/warehouses/<id>`). |

## References

- Databricks SDK for Python — Statement Execution: https://databricks-sdk-py.readthedocs.io/en/stable/workspace/sql/statement_execution.html
- Databricks SQL Connector for Python: https://docs.databricks.com/aws/en/dev-tools/python-sql-connector
- databrickslabs/lsql: https://github.com/databrickslabs/lsql
