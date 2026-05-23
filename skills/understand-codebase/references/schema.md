# Knowledge Graph Schema

## Top-level Structure

```json
{
  "version": "1.0.0",
  "project": {
    "name": "project-name",
    "description": "What this project does",
    "languages": ["TypeScript", "Python"],
    "frameworks": ["Next.js", "FastAPI"],
    "analyzedAt": "2026-05-23T12:00:00Z",
    "gitCommitHash": "abc123"
  },
  "nodes": [],
  "edges": [],
  "layers": [],
  "tour": []
}
```

## Node Schema

```json
{
  "id": "file:src/auth/login.ts",
  "type": "file",
  "name": "login.ts",
  "filePath": "src/auth/login.ts",
  "summary": "Handles user authentication via email/password and OAuth providers.",
  "tags": ["auth", "api"],
  "complexity": "moderate"
}
```

### Node Types

| Type | ID Convention | Example |
|------|--------------|---------|
| `file` | `file:<relative-path>` | `file:src/index.ts` |
| `function` | `function:<path>:<name>` | `function:src/utils.ts:formatDate` |
| `class` | `class:<path>:<name>` | `class:src/models/User.ts:User` |
| `module` | `module:<name>` | `module:auth` |
| `config` | `config:<path>` | `config:tsconfig.json` |
| `document` | `document:<path>` | `document:README.md` |
| `service` | `service:<path>` | `service:Dockerfile` |
| `endpoint` | `endpoint:<path>:<name>` | `endpoint:src/routes.ts:POST /login` |
| `pipeline` | `pipeline:<path>` | `pipeline:.github/workflows/ci.yml` |

### Complexity Values

- `simple` — straightforward, few branches
- `moderate` — some logic, manageable
- `complex` — heavy branching, many dependencies

## Edge Schema

```json
{
  "source": "file:src/routes/auth.ts",
  "target": "file:src/services/auth.ts",
  "type": "imports",
  "weight": 0.7
}
```

### Edge Types

| Type | Meaning | Weight |
|------|---------|--------|
| `imports` | File imports/requires another | 0.7 |
| `contains` | File contains function/class | 1.0 |
| `calls` | Function calls another function | 0.8 |
| `inherits` | Class extends another | 0.9 |
| `implements` | Class implements interface | 0.9 |
| `depends_on` | General dependency | 0.6 |
| `configures` | Config file configures a service | 0.6 |
| `tested_by` | Production code tested by test file | 0.5 |
| `documents` | Doc file documents code | 0.5 |
| `deploys` | Infra deploys a service | 0.5 |
| `routes` | Router maps to handler | 0.7 |

## Layer Schema

```json
{
  "id": "layer:api",
  "name": "API Layer",
  "description": "HTTP handlers, controllers, route definitions",
  "nodeIds": ["file:src/routes/auth.ts", "file:src/routes/users.ts"]
}
```

Every file-level node must appear in exactly one layer.

## Tour Schema

```json
{
  "order": 1,
  "title": "Entry Point",
  "description": "The app boots from main.ts which sets up Express and mounts routes.",
  "nodeIds": ["file:src/main.ts"]
}
```

Tour steps are ordered 1..N. Each step has 1-3 nodeIds. Total 5-10 steps covering the critical path through the codebase.

## Validation Rules

1. Every `edge.source` and `edge.target` must reference an existing node ID
2. Every file-level node must be in exactly one layer
3. Every tour step must reference existing nodes
4. No duplicate node IDs
5. No orphan nodes (every node has at least one edge)
6. Node IDs use the format `type:path` or `type:path:name`
