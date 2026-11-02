# Writing the AGENTS.md of a Fabric app repo

Pattern observed in djouallah/analytics-as-code (1,150 lines, maintained by AI) and in Fabric Atlas / campus-scheduler
templates. Use it when creating or reviewing the AGENTS.md of an app repo so the next agent can maintain it.

## Structure
1. Quick Reference: stack, exact run commands per target, layout, schemas.
2. Architecture: what exists and which parts are the only persistent state.
3. Per-area sections (client, deploy, auth, model), each ending with how to verify ("to check a deploy, open the Logs tab...").
4. Tables for inventories (models, items, workflows), a Key Patterns list, and a version/pinning policy.
5. Open items split into "waiting on upstream" and "possible improvements"; an honest preface that preview limits describe the version in use, not the product.

## Line-level rules
- Every rule carries its WHY, often as the failure that produced it ("appending the whole log each run would grow the table by its own size 48 times a day until the catalog answers HTTP 500").
- Facts are dated and tied to evidence: run ids, issue numbers (`microsoft/rayfin#89`), dates, a measurement. A later dated entry beats an earlier doc; update or delete the stale one.
- Keep decision history where it prevents regressions ("Until 2026-10-28 the app ran DuckDB 2.0... back to 2.0 once duckdb-wasm 2.0 is on npm").
- State priorities that settle conflicts ("the public page must never break"; "look in the sibling repo first and port fixes rather than diverging").
- List deliberate local differences that must survive a port, and explicit "do not" lines with their reason ("do not use `dbt run --full-refresh`: RENAME has never been probed against this catalog").
- Say what is NOT done and why ("no fallback, on purpose").
- Name the identity and owner of every deployed item, who deploys it, and from where.
- Record the supported browser/engine/CLI versions and the pinning policy (what is pinned exactly, what is not, and why).
- Secrets: names and shapes only; values never.

## Fabric-specific content to include
Item names and their owners; workspace/tenant switches the app depends on; which identity each function and connector runs as; the deploy command per item; the verification step per posture; the known-issue ledger with issue numbers and the date last checked; where the version-matched Rayfin docs are (`node_modules/@microsoft/rayfin-guide/assets/docs`).

## Anti-patterns
Copying API reference into AGENTS.md (it goes stale; link to the docs path), undated "we found that...", rules without a reason, instructions the code or a lint could enforce instead (move them below the prose: a check, a test, a clearer error).
