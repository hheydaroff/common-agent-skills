# Attribution

`fabric-app` is an original synthesis. No source text is copied verbatim; rules, patterns and traps were
distilled and re-expressed from the following (all MIT-licensed unless noted).

- **djouallah/analytics-as-code** (c) 2026 Mimoune Djouallah, MIT. Primary worked example: Fabric app architecture
  (host adapter, OneLake SAS function, browser store, build stamping), CI/deploy design, test ladder, and the
  AGENTS.md method. https://github.com/djouallah/analytics-as-code
- **microsoft/rayfin** (c) Microsoft Corporation, MIT. Official agent skills (`rayfin`, `rayfin-functions`,
  `rayfin-connectors`, `rayfin-storage`, `rayfin-getting-started`), the `data-app` and `universal-app` sample skills,
  and the `@microsoft/rayfin-guide` / `rayfin-docs` package docs (version 1.36.2). https://github.com/microsoft/rayfin
- **microsoft/awesome-rayfin** (c) Microsoft Corporation, MIT. Template gallery: Fabric Atlas, pbi-fixer,
  semantic-directory, finance-analytics, helsinki-public-transport, campus-scheduler, field-technician, universal-app.
- **microsoft/skills-for-fabric** (c) 2026 Microsoft Corporation, MIT. Read only to map neighbouring skills
  (`ecosystem.md`); it contains no Rayfin coverage.
- Field notes read and summarised (not copied): Microsoft Learn `fabric/apps/*`, rayfin.ai docs, microsoft/rayfin
  issues #61 and #89 and #93, Beyond The Analytics, Metis BI, Jihwan Kim (powerbimvp.com), Tabular Editor,
  DataTako. Their prices, regions and licensing statements are flagged volatile in the skill.

Local additions: `scripts/rayfin-lint.mjs` (original), the decision tables, the symptom index in
`references/troubleshooting.md`, and the cross-source conflict resolutions (newer dated source wins; disagreements
recorded where they matter).

Snapshot: sources read 2026-10-29 against Rayfin CLI 1.36.2. Preview-era details drift; every `[VOLATILE]` item must be re-checked.
