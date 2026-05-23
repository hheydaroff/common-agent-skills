# Using the Knowledge Graph

Once `.understand-anything/knowledge-graph.json` exists, use these patterns to query it.

## Ask Questions (Chat)

When the user asks about the codebase ("how does auth work?", "what calls the payment service?"):

1. **Search nodes** — grep the graph for keywords:
   ```bash
   grep -i "auth\|login\|token" .understand-anything/knowledge-graph.json | head -30
   ```

2. **Find connected edges** — for matched node IDs, grep for their connections:
   ```bash
   grep "file:src/auth/login.ts" .understand-anything/knowledge-graph.json
   ```

3. **Follow the chain** — `imports` edges show dependencies, `calls` edges show runtime flow, `contains` edges show structure.

4. **Answer in context** — use node summaries + edge relationships to explain how components interact. Reference specific files.

## Diff Impact Analysis

When the user wants to understand the impact of their current changes:

1. **Get changed files**:
   ```bash
   git diff --name-only              # uncommitted
   git diff main...HEAD --name-only  # branch vs main
   ```

2. **Find graph nodes for changed files** — grep each changed path in the graph

3. **Find 1-hop affected components** — for each changed node, find edges where it appears as source or target. Those connected nodes are "potentially affected."

4. **Report**:
   - **Changed**: what was directly modified (with summaries)
   - **Affected**: what depends on or is called by the changed files
   - **Risk**: based on complexity values and number of cross-layer connections
   - **Suggest**: what to test, review carefully, or update

## Explain a Component

When the user asks to explain a specific file or function:

1. **Find the node** — grep for the file path or function name
2. **Get its edges** — all connections (imports, calls, tested_by, contains)
3. **Identify its layer** — which architectural layer it belongs to
4. **Read the actual file** — get the source code
5. **Explain in context**:
   - Its role in the architecture (which layer, why it exists)
   - What it depends on (outgoing edges)
   - What depends on it (incoming edges)
   - Internal structure (functions/classes it contains)
   - Data flow and key logic patterns

## Generate Onboarding Guide

When the user wants a team onboarding document:

1. **Read project metadata** — name, description, languages, frameworks
2. **Read layers** — the architectural breakdown
3. **Read the tour** — the guided walkthrough steps
4. **Identify complexity hotspots** — nodes with `complexity: "complex"`

5. **Generate markdown** with sections:
   - **Project Overview** — what it does, tech stack
   - **Architecture** — layers table with descriptions and key files
   - **Guided Tour** — step-by-step learning path (from tour data)
   - **File Map** — what each key file does, organized by layer
   - **Complexity Hotspots** — areas to approach carefully
   - **Key Patterns** — recurring patterns from tags analysis

6. **Save** to `docs/ONBOARDING.md`

## Extract Business Domains

When the user wants domain/flow analysis:

1. **Group by tags** — cluster nodes by business-related tags (auth, payment, notification, etc.)
2. **Identify flows** — trace edge chains that represent business processes (e.g., request → validate → process → store → respond)
3. **Name domains** — each cluster is a business domain
4. **Map flows to steps** — each flow has ordered steps with the nodes involved

Output structure (add to graph or report separately):
- **Domains**: high-level business areas (Authentication, Payments, Notifications)
- **Flows**: processes within domains (Login Flow, Payment Processing)
- **Steps**: ordered actions within flows (Validate Input → Check Credentials → Issue Token)

## Tips for Efficient Graph Reading

- **Never load the entire JSON into context** — always grep first
- **Node IDs are predictable**: `file:path`, `function:path:name`, `class:path:name`
- **Edge weights indicate strength**: 1.0 = structural (contains), 0.7 = imports, 0.5 = weak link
- **Tags** are the fastest way to find thematic groups
- **Layers** are the fastest way to understand where something fits architecturally
