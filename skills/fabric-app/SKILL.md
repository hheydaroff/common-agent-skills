---
name: fabric-app
description: "Build, run, deploy and debug Microsoft Fabric apps made with Rayfin (npx rayfin up): operational apps (entities, GraphQL, permissions), data apps over a semantic model (fabric-semanticmodel connector, DAX), static analytics apps with a signing function (DuckDB-WASM over OneLake), functions, secrets, connectors, Fabric SSO, CI deploy. Use when the user says Fabric app, Fabric Apps, Rayfin, rayfin.yml, rayfin up, AppBackend, data app, Power BI custom app, openCatalog, udf.func, fabric-semanticmodel, 'Only AppBackend artifact owner', or wants a custom web app on Fabric data or a Power BI semantic model (also: Vega/fabric-visuals charts, KPI cards empty in the Fabric host, 'Cannot convert a BigInt', validate:visual, ConnectorsRayfinClient). Distilled from djouallah/analytics-as-code, Microsoft's Rayfin docs and skills, awesome-rayfin templates and field notes. Not for authoring Power BI reports or semantic models themselves."
---

# Fabric apps (Rayfin)

Fabric apps are code-defined web apps hosted by Fabric: static hosting, Fabric SSO, optional managed SQL DB (GraphQL),
server functions, connectors to Fabric items. Preview product, CLI `@microsoft/rayfin-cli` (`npx rayfin`).

**Division of labour.** Rayfin ships version-matched docs inside `node_modules/@microsoft/*/assets/docs` and a
generated in-project skill (`.agents/skills/rayfin/SKILL.md`). They own API shapes, decorator options, CLI flags.
This skill owns judgment: which shape, which identity, what breaks, in what order, how to verify. Never answer a
Rayfin API question from memory; read the docs (`rayfin-project.md`). If the project's own skill is more specific, it wins.

**Power BI-only profile.** If the only data source is a Power BI semantic model (no lakehouse, SQL, OneLake, functions), load `references/powerbi-only-profile.md` first: it narrows this skill to the data-app shape and lists what to skip.

## 1. Decide the shape (before any code)
| Need | Shape | Read |
|---|---|---|
| App owns data: write-back, workflow, per-user records | operational app (entities) | `operational-apps.md` |
| Custom UX over an existing semantic model, per-user RLS | data app (connector + DAX) | `data-apps-semantic-model.md` |
| Data already in a Fabric SQL item / warehouse | Category A connector | `connectors.md` |
| Ad hoc SQL or very heavy reads in the browser, no per-query capacity | static analytics app + signing function | `static-engine-patterns.md` |
| Secret, external API, Fabric REST, OneLake files | function | `functions-and-secrets.md` |
| Standard report, external users, plain write-back in a report | NOT a Fabric app | `platform-and-prereqs.md` |

## 2. Operating loop
1. **Orient.** `rayfin/rayfin.yml` present? Continue in place; never scaffold a nested project. Otherwise scaffold non-interactively (`rayfin-project.md`). Then read the project's `AGENTS.md` and in-project skill.
2. **Prereqs** (admin switch, F-SKU capacity in a supported region, item-create rights, Execute Queries for data apps). You cannot enable tenant settings: tell the user (`platform-and-prereqs.md`).
3. **Settle identity and ownership up front:** who owns the item, who deploys, what each function/connector runs as (`auth-and-security.md`, `deploy-and-ci.md`). This decides laptop vs CI and whether functions work at all.
4. **Build against real data.** Probe every connector/DAX/catalog call through the CLI before writing UI. No mock data unless asked and labelled. Unknown is a state (N/A), never 0.
5. **Lint:** `node scripts/rayfin-lint.mjs <project-dir>` (path relative to this skill's directory; permission decorators, `@text` max, dialect, functions auth, `host.json`, lockfile registry, deprecated ctx calls). Fix ERRORs.
6. **Deploy:** `rayfin up -n`, then `rayfin up --output json`; parse `steps.*.status`, never trust exit 0 (`deploy-and-ci.md`).
7. **Verify the running system** in a clean browser on the deployed URL, with a second non-owner user; per hosting posture (`frontend-design-and-validation.md`). Only then say "deployed".
8. **On failure** go to `troubleshooting.md` and match the exact error string. No shell? Give the plan and label every command as not executed.

## 3. Hard rules (each cost someone an afternoon)
1. Docs from `node_modules` first (`rayfinDocs.dir`, `npx rayfin docs search '<topic>'`). Remembered Rayfin APIs are routinely wrong.
2. Every entity has an explicit permission decorator; every `@text` has `max`; `services.data` needs `dialect: mssql`; never enable `experimentalDecorators`.
3. The browser holds no token and nothing that can write. Anything in the bundle is public; `assetAccess: public` does not make data anonymous, but put nothing sensitive in it.
4. `rayfin up` is OWNER-only. One deployer identity per item; laptop and CI do not share an item. A service-principal-owned item breaks functions (#89) and Category A connectors (#93). [volatile]
5. New-item order: `up` -> `secret set` -> `up functions deploy`. Functions return `{ error: "<step>: ..." }`, not throw. Never hand-edit generated `types.ts`/`secrets.generated.ts`.
6. `rayfin up` exit 0 is not success. Connector apps: one `generate[]` entry per connector. Frontend and backend deploy separately: verify the running app.
7. A CLI probe is necessary, not sufficient: the deployed app re-authorises as the signed-in user and receives Arrow-typed values (bigint) that JSON probes hide. Test in the host with a non-owner; not done until one real load shows real values.
8. DAX: never turn BLANK into 0; `CONVERT` fixed-decimal measures to DOUBLE; bound result size (no default cap); check both error channels (`error` and `data.status`).
9. Never enable cross-origin isolation or threaded WASM in a Fabric app (breaks the sign-in popup).
10. Stamp builds (`?v=<build>`) and `modulepreload` modules, or browsers run new HTML with cached old JS.
11. Preview-era facts (issue numbers, regions, licensing, version pins) go stale: re-verify the `[VOLATILE]` ones before asserting them; do not promise production-readiness, external-user access or licensing outcomes.
12. Keep the page dumb: figures are model measures; a lint or test enforces that no UI code computes business numbers.
13. Never read or print secret/env files; ask the user for values. Secret values enter only through `rayfin secret set` in a masked prompt or `--stdin`, never chat, args or committed files.

## Reference files
| File | Load when |
|---|---|
| [powerbi-only-profile.md](references/powerbi-only-profile.md) | only a Power BI semantic model as data source, no other Fabric item; what to skip and what is unverified |
| [platform-and-prereqs.md](references/platform-and-prereqs.md) | choosing a shape, "can we", admin switches, regions, licensing, preview limits, volatile issue ledger |
| [rayfin-project.md](references/rayfin-project.md) | scaffolding, docs routing table, project layout, rayfin.yml keys, env files, dev loop, demo mode, templates |
| [auth-and-security.md](references/auth-and-security.md) | sign-in flows, identities, hosting posture, entity permissions, function hardening, secrets |
| [operational-apps.md](references/operational-apps.md) | entities, GraphQL paging, writes, idempotency, snapshots, Storage |
| [data-apps-semantic-model.md](references/data-apps-semantic-model.md) | connector setup, schema discovery, DAX and query design rules, runtime errors, model contract |
| [connectors.md](references/connectors.md) | picking a connector type, Category A vs B, auth default, add/inspect/invoke traps |
| [functions-and-secrets.md](references/functions-and-secrets.md) | writing functions, audiences, secrets order, local dev, SAS-minting pattern, doc routing |
| [static-engine-patterns.md](references/static-engine-patterns.md) | browser engine over OneLake files: host adapter, SAS function, OPFS store, build stamp, Logs tab |
| [deploy-and-ci.md](references/deploy-and-ci.md) | `rayfin up` loop, ownership, GitHub Actions recipe, whole-stack order, model contract check, test ladder |
| [frontend-design-and-validation.md](references/frontend-design-and-validation.md) | visuals, layout, tokens, a11y, tests, browser validation checklist, Playwright in the portal |
| [troubleshooting.md](references/troubleshooting.md) | any error string or symptom |
| [worked-example-analytics-as-code.md](references/worked-example-analytics-as-code.md) | learning from the exemplar repo; extracting rules from another repo |
| [agents-md-method.md](references/agents-md-method.md) | writing or reviewing a repo's AGENTS.md |
| [ecosystem.md](references/ecosystem.md) | Microsoft plugin/skills, skills-for-fabric neighbours, template gallery, other reading |

## Scripts
`scripts/rayfin-lint.mjs [dir] [--json]`: static checks for the mechanical traps above; exit 1 on ERROR, 2 if no project found. No dependencies.

## Non-goals
Authoring semantic models, TMDL or PBIR reports (see `ecosystem.md` for skills-for-fabric), dbt/Iceberg pipeline engineering (only the app-facing contract is covered), and copying Rayfin API reference (read it from the install).

Sources and licences: `ATTRIBUTION.md`.
