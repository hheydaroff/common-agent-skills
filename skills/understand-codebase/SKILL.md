---
name: understand-codebase
description: "Analyze a codebase and produce an interactive knowledge graph showing architecture, components, and relationships. Use when user says 'understand this codebase', 'map the architecture', 'knowledge graph', 'how does this project work', 'onboard me', or wants a visual overview of code structure."
---

# Understand Codebase

Turn any codebase into an interactive knowledge graph you can explore in a browser. No build tools, no dependencies — the agent does the analysis and produces a self-contained dashboard.

## Workflow

### 1. Scan the project

```bash
bash <SKILL_DIR>/scripts/scan-project.sh <PROJECT_ROOT>
```

This outputs a JSON manifest of files, languages, and framework hints. Review the output — if >200 files, suggest the user scope to a subdirectory.

### 2. Analyze in batches

Read files in batches of 10-15. For each file, extract:
- **Nodes**: files, functions/methods, classes, configs, services
- **Edges**: imports, calls, contains, depends_on, configures

Follow the schema in [references/schema.md](references/schema.md) exactly.

For each batch, read the files and produce nodes + edges. Append results to a running list. Prioritize:
- Entry points first (main.ts, index.ts, app.py, main.go)
- Then core business logic
- Then utilities, configs, tests last

### 3. Identify architecture layers

After all files are analyzed, group file-level nodes into layers:
- **API/Routes** — HTTP handlers, controllers, endpoints
- **Business Logic** — services, use cases, domain models
- **Data** — repositories, database, ORM models, migrations
- **Infrastructure** — Docker, CI/CD, cloud configs
- **UI** — components, pages, layouts, styles
- **Utilities** — helpers, shared libs, types

Assign each file node to exactly one layer.

### 4. Build a guided tour

Create 5-10 tour steps ordered by dependency (start from entry point, follow the request flow). Each step references 1-3 nodes and explains what they do and why they matter.

### 5. Save the graph

Write the final JSON to `.understand-anything/knowledge-graph.json`:

```bash
mkdir -p <PROJECT_ROOT>/.understand-anything
```

### 6. Launch the dashboard

Copy the dashboard viewer and serve it:

```bash
cp <SKILL_DIR>/dashboard.html <PROJECT_ROOT>/.understand-anything/index.html
cd <PROJECT_ROOT>/.understand-anything && python3 -m http.server 8080 &
open http://localhost:8080  # macOS
# or: xdg-open http://localhost:8080 on Linux
```

The HTML file loads `knowledge-graph.json` via fetch from the same directory. A local server is required (browsers block fetch on file:// URLs). Kill the server after viewing with `kill %1`.

## Reference Files

| File | When to load |
|------|--------------|
| [schema.md](references/schema.md) | Always — defines the JSON structure for nodes, edges, layers, tour |
| [analysis-guide.md](references/analysis-guide.md) | When analyzing files — extraction patterns per language |

## Incremental Updates

If `.understand-anything/knowledge-graph.json` already exists:
1. Check which files changed: `git diff --name-only <last-commit>..HEAD`
2. Re-analyze only changed files
3. Remove old nodes/edges for those files, insert new ones
4. Re-run layer assignment on the full set

## Tips

- Keep summaries under 2 sentences — they appear as tooltips in the dashboard
- Use consistent node ID format: `type:path` or `type:path:name`
- Every node needs at least one edge (no orphans)
- The dashboard is a single HTML file with D3.js loaded from CDN
- Output goes to `.understand-anything/` — add this to `.gitignore` or commit it for team sharing
