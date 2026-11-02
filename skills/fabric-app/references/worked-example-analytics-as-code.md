# Worked example: djouallah/analytics-as-code, decomposed

Source: github.com/djouallah/analytics-as-code (MIT, "every line written by AI"; AEMO electricity data; Oct 2026,
Rayfin 1.36.1). Its value to us is not the energy data; it is a repo where an AI maintains a full stack and every
hard-won rule is written down. Use this file to (a) see how the pieces fit, (b) decide what to copy, (c) apply the
same extraction method to the next exemplar repo.

## The stack in one line
source CSVs -> dbt-duckdb on CI (ephemeral, in-memory) -> Iceberg tables in a OneLake lakehouse (the only state)
-> ONE semantic model (YAML, measures in DAX; `model.bim` written at deploy) -> ONE page -> three hosts
(GitHub Pages / Fabric app on DuckDB-WASM / Fabric app on the semantic model).

## Map: where each transferable idea lives
| Layer | Repo location | Idea to copy | Our reference |
|---|---|---|---|
| One page, many hosts | `front_end/page/`, `front_end/<host>/storage/data.js` | page written once; a host adds only its data adapter; absence of a member = capability flag | static-engine-patterns |
| Fabric app: SAS app | `front_end/fabric_app/iceberg/` (`rayfin.yml`, `functions/src/function_app.ts`, `site/storage/*.js`) | one function mints a read-only SAS; browser engine plans and caches itself | static-engine-patterns, functions-and-secrets |
| Fabric app: semantic model | `front_end/fabric_app/vertipaq/` | connector `fabric-semanticmodel`, connector written at deploy | data-apps-semantic-model, deploy-and-ci |
| Shared build + sign-in | `front_end/fabric_app/common/{build.mjs,site/storage/auth.js}`, `scripts/{stamp_build,stage_pages}.mjs` | no bundler; stamp; modulepreload; auth gate | static-engine-patterns, auth-and-security |
| One CLI for two apps | `front_end/fabric_app/package.json` | devDependency + `npx rayfin` per app folder | rayfin-project |
| Whole-stack deploy | `.github/workflows/deploy_fabric.yml`, `scripts/deploy_fabric.py` | parts as argv/inputs, idempotent, test workspace by default | deploy-and-ci |
| Model deploy + check | `scripts/{deploy_model,check_model,ossie_to_bim}.py/.mjs` | placeholders filled at deploy; per-measure contract check by XMLA | deploy-and-ci, data-apps-semantic-model |
| Test ladder | `scripts/parity/*`, `build.yml`, `deploy_model.yml` | lint, fixtures, engine parity, A/B, deployed-model reference | deploy-and-ci |
| Pages publish | `scripts/deploy_pages.sh`, `squash_deploy_repo.yml` | retry, `git add -f`, weekly squash | deploy-and-ci |
| Method | `AGENTS.md` (1,150 lines), `doc/ARCHITECTURE.md` | rule + why + date + evidence; priority statements | agents-md-method |
| Data pipeline | `dbt/`, `scripts/maintain/` | insert-only merges, file-based incremental, manifests for date bounds | not covered here |

## Ideas that transfer beyond this domain
1. **Put every rule in the model, keep the client dumb.** Figures are measures; the page "works out no figure of its own". A lint enforces it (`page_lint.mjs`: no arithmetic in the page). The same measure answers a day and a year because it picks the table.
2. **A thin host adapter is the portability seam.** Three hosts share `index.html` byte for byte; engine-specific risk (auth, SAS, caches) lives in one file each.
3. **Priority statement settles conflicts.** "The GitHub page is public and must never break. The Fabric apps are internal... where the clients pull apart the public page wins." An agent now has a tie-break.
4. **Own item, own identity.** The deploy ownership rule produced a layout (laptop item vs CI item, two workspaces) rather than a workaround.
5. **Test the contract, not the build.** After every model deploy a script asks each measure for the newest week and exits 1 on any failure; engine parity runs on dispatch because it spends capacity, and only for queries whose content key changed.
6. **Self-describing debug record.** The Logs tab (build stamp, function call, per-query wait/run/engine, worker HTTP, store state) turns "it is slow" into a paste-able artifact.
7. **Fail loudly on what you cannot handle, on purpose.** Equality deletes, a codec the Avro reader lacks, no OPFS writer: error with a reason, no silent fallback.
8. **Honest scope in the docs.** README: "Much of the stack is pre-release... A limit below that comes from one of them describes the version in use, not the product." Open items split into "waiting on upstream" and "possible improvements".
9. **Idempotent, part-wise deploy tooling** with defaults that protect money (schedule off in test) and correctness (parts default on).

## Do not copy
- The AEMO/dbt/Iceberg-maintenance specifics unless you build the same pipeline.
- The hand-rolled DuckDB-WASM block store unless your use case needs ad hoc SQL over multi-GB files; for most Fabric apps a semantic-model connector is simpler, secure by default, and supported.
- `assetAccess: public` as a default (it fits there because all data sits behind the SAS function).
- Dated numbers (timings, file sizes, version pins) as facts; the repo's own docs disagree in places (`doc/ARCHITECTURE.md` is older than `AGENTS.md`: trust the later dated entries).

## Extraction method for the next exemplar repo
1. Read the top-level README, then `AGENTS.md`/architecture docs for rules with a stated WHY and a date. Those are the high-value lines.
2. Locate the platform boundary files (`rayfin.yml`, functions, deploy workflow/script, auth code) and read them whole; skim the domain code.
3. List constraints the author hit (grep for "because", "on purpose", "never", issue numbers, dates). Each becomes a decision rule or a trap with the exact error string.
4. Separate durable from volatile (preview bugs, version pins, issue numbers). Tag the volatile ones.
5. Cross-check against official docs; where they disagree, the newer dated source wins and the disagreement is recorded.
6. Decompose by reader intent (design, build, deploy, debug), not by repo layout.
7. Fan out one analyst per slice (runtime, delivery, official docs, field notes) with a shared brief and report format; merge reports into reference files and keep traps keyed by symptom.
