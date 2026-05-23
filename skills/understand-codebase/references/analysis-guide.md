# Analysis Guide

## General Extraction Process

For each file:
1. **Read the file** (first 200 lines is usually sufficient for structure)
2. **Create a file node** with summary and tags
3. **Extract functions/classes** as child nodes with `contains` edges
4. **Identify imports** — create `imports` edges to other file nodes
5. **Detect patterns** — routes, tests, configs get appropriate edge types

## Language-Specific Patterns

### TypeScript / JavaScript

- **Imports**: `import { X } from './path'` → `imports` edge to resolved file
- **Exports**: Named/default exports → the file's public API
- **Classes**: `class X extends Y` → `inherits` edge
- **React components**: functional components are functions; `<Component />` usage → `calls`
- **Express/Fastify routes**: `app.get('/path', handler)` → `endpoint` node + `routes` edge

### Python

- **Imports**: `from module import X` → resolve to file path
- **Classes**: `class X(Base):` → `inherits` edge to Base
- **Decorators**: `@app.route` → `endpoint` node; `@pytest.fixture` → skip
- **Django/FastAPI**: views, serializers, models map to layers naturally

### Go

- **Imports**: `import "pkg/path"` → resolve within module
- **Interfaces**: `type X interface` → other types `implements`
- **Handlers**: `func(w http.ResponseWriter, r *http.Request)` → endpoint

### Rust

- **Modules**: `mod name;` → contains edge to the module file
- **Traits**: `impl Trait for Type` → `implements` edge
- **Use statements**: `use crate::path` → imports edge

### Java / Kotlin

- **Imports**: `import com.pkg.Class` → resolve to file
- **Extends/implements**: `class X extends Y implements Z`
- **Annotations**: `@RestController`, `@Service` → hints for layer assignment

## What to Skip

- **Test files** (*.test.*, *.spec.*): create a file node but mark with `test` tag. Create `tested_by` edge from the production file to the test file.
- **Generated files** (*.generated.*, *.min.*): skip entirely
- **Lock files** (package-lock.json, yarn.lock): skip
- **Binary files** (images, fonts): skip
- **node_modules/, vendor/, .git/**: skip

## Tagging Strategy

Apply 2-4 tags per node from this vocabulary:

| Tag | When to apply |
|-----|--------------|
| `entry-point` | Main file, index, app bootstrap |
| `api` | HTTP handlers, routes, controllers |
| `auth` | Authentication/authorization logic |
| `database` | DB access, queries, migrations |
| `model` | Data models, entities, schemas |
| `service` | Business logic services |
| `util` | Helper functions, shared utilities |
| `config` | Configuration files |
| `test` | Test files |
| `ui` | Frontend components, pages |
| `middleware` | Request/response middleware |
| `infra` | Docker, CI/CD, cloud resources |
| `types` | Type definitions, interfaces |
| `error-handling` | Error classes, handlers |
| `validation` | Input validation, schemas |

## Summary Writing Style

- Max 2 sentences
- Start with what it does, not what it is
- Use active voice: "Handles authentication" not "This file is used for authentication"
- Mention key dependencies if non-obvious
- Example: "Validates user input against Zod schemas before passing to the auth service. Rejects malformed requests with structured error responses."

## Batch Strategy

Process files in this order:
1. **Entry points** — main.ts, index.ts, app.py (understand the boot sequence)
2. **Route/API layer** — understand what the app exposes
3. **Services/business logic** — understand what it does
4. **Data layer** — models, repositories, database
5. **Infrastructure** — Docker, CI/CD, configs
6. **Tests** — last, creates tested_by edges back

This order means earlier batches inform later analysis (you know the architecture by the time you hit utilities).
