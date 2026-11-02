# Operational apps: entities, GraphQL, writes

Use when the app owns the data (managed SQL DB behind a GraphQL API, MSSQL dialect only on Fabric). Read
`known-limitations.md` BEFORE designing entities (rayfin-project.md routing table); it is the only place the
platform says what it will not do. Do not write decorators or client calls from memory.

## Design rules
1. Explicit permission decorator on every entity (auth-and-security.md). Per-user data = server `@role`/`@authenticated` policy keyed on `claims.sub`, with a `user_id` column; never a client filter.
2. Every string field gets `max`: `@text({ max: 200 })`. A bare `@text()` becomes NVARCHAR(MAX); the deploy "succeeds" and GraphQL then answers "Internal server error". Fix, then `npx rayfin up db apply --force` after reviewing the destructive change.
3. `services.data.dialect: mssql` is mandatory when data is enabled ("Dialect is required when Data module is enabled").
4. Register every entity in `rayfin/data/schema.ts`; an unregistered entity does not exist for the client. In universal-app workspaces register in BOTH `packages/data/src/index.ts` `schema` and `packages/shared` `UniversalAppSchema`; type-check with `tsc -b`/`npm run typecheck` (bare `tsc --noEmit` gives TS6305).
5. Never name an entity after a built-in scalar or GraphQL root type (`Date`, `Query`, anything starting `__`); rename the class or pass an explicit name to `@entity('...')`. The authoritative list is "Reserved entity names" in `rayfin-core/assets/docs/decorators.md`. Matching is case-sensitive and exact (`TaskDate` is fine).
6. Many-to-many = an explicit join entity with two `@one()`. Selects nest at most 2 levels. Relationship decorators accept only `{optional?, unique?}`. Declare FK fields only if code needs them, named `{property}_id`; write relations as `create({..., parent: { id }})`. Parents before children in seed scripts.
7. Schema is code-owned. Editing the SQL DB in the Fabric portal is read-only by design and overwritten on the next deploy; change `rayfin/data/*.ts` and run `rayfin up`. A table limit of 100 in the child Fabric SQL DB was reported once; use a connector to an external DB for very large models. [VOLATILE]
8. `rayfin up` is the canonical "apply my schema change" (it deploys and migrates). Older docs say run `up db apply` after every entity change; the newer CLI skill and deploy.md say `up` does both. `up db apply` is for an explicit schema-only request. Destructive changes (drop column/table, alter type) are refused without `--force`.
9. Use the typed client (`client.data.<Entity>`), never raw `fetch` or hand-built GraphQL. (`client.data.gql.<Entity>` is the older spelling still in some docs.)

## Reading
- `.execute()` returns ONE page (default 100, DAB max 100,000) with no truncation signal. Lists that can grow: `.first(n)` + `.executePaginated()` + `.after(endCursor)` looping on `hasNextPage`, same select/where/orderBy on every page. Guard a repeated or missing `endCursor` (throw "pagination did not advance").
- No `count()`, `totalCount` is never populated, no `before` paging, date `gt/lt` filters fail on PostgreSQL (irrelevant on Fabric). Select ids and use `results.length`.
- `.where/.orderBy/.first` do not inherit a default selection: add `.select([...])` or you get `SELECTION_REQUIRED`.
- Nullable text, `Date` objects, arrays and objects are invalid React children: render defensively. Date-only strings (`YYYY-MM-DD`) shift a day west of UTC unless formatted with `timeZone: 'UTC'`. Default filters must include a just-created row.

## Writing
- Optimistic create/update/delete with rollback (a failed delete restores the original position). Wrapper promises resolve even on a handled failure: never clear the form on `await create()` alone; clear from an explicit success state. Trust the returned row; no field-by-field readback that fails a save. Match input `maxLength` to `@text({max})`. Confirm destructive actions naming the item. Seed only on a user click, idempotently.
- Bulk or retried writes (Atlas): give each write a client-generated UUID BEFORE the first mutation and verify it before any retry (a timed-out mutation may have completed); cap concurrent mutations at 2 (8 saturated the Data API); allow a 120 s request timeout (default 30 s).
- No multi-row transaction exists. For bulk publish use a snapshot: write child rows, read them back through the production pagination path, verify counts against a manifest, write the manifest LAST; readers hydrate only from a valid manifest; a failed run leaves the previous snapshot; prune old snapshots after publish.
- Long values: do not truncate silently. Chunk (`v1:<part 4d>:<total 4d>:<payload>` in <= 1,960-char pieces), reject sets with missing/duplicate parts; mark truncation explicitly where a value must be cut.
- State that must survive container scale-to-zero belongs in the Rayfin DB, not in a module-level dict (a solver container's confirmed drafts "evaporated silently, indistinguishably from never having done it").
- Model "unknown" as a state: N/A, never a fabricated 0; keep a status vocabulary (collected / partial / unsupported / denied) and say "Fabric denied the app permission", not "the principal was denied".

## Validation helper and forms
`data/validation.md` documents Standard Schema form validation from the entity definition; use it rather than hand-written mirrors of `max` and `optional`.

## Suitability
Wrong target: multi-step transactions, stored procedures, custom auth providers. Not for large analytic scans: put those in a semantic model (data-apps-semantic-model.md) or OneLake files (static-engine-patterns.md).

## Storage (experimental)
`services.storage` / `@blob` only if the user names Rayfin Storage or the project already enables it; never for a generic upload request. Folders need at least one authenticated `@role`; anonymous Storage permissions are unsupported; prefixes organise paths, they do not grant access. Read `rayfin-storage` docs and the `rayfin-storage` skill.
