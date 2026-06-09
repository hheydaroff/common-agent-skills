---
name: research-skill-foundation
description: "Deep research phase before building a new agent skill. Runs parallel Exa + Tavily searches, pulls official GitHub repos (MCP servers, existing skill implementations, API docs), fetches raw SKILL.md and reference files, organizes everything into /tmp/<name>-research/ with numbered markdown docs. Produces a ready-to-use research folder the skill-generation step can read directly. Use when user wants to build a new skill and needs comprehensive prior art, API coverage, and official implementations pulled first. Triggers: 'research for skill', 'gather references for skill', 'pull docs before building skill', 'find prior art for skill'."
---

# Research Skill Foundation

## When to Use

Before building a new agent skill from scratch — especially when:
- The skill wraps an external API or tool (Figma, Notion, Linear, Slack, etc.)
- There are official MCP servers or existing skill implementations to learn from
- You need to understand API tiers, auth models, and rate limits before scripting
- The user says "search the web and pull relevant info before we generate the skill"

## Steps

### 1. Create the research directory (never delete it)
```bash
mkdir -p /tmp/<skill-name>-research
mkdir -p /tmp/<skill-name>-research/official-skills
```

Tell the user explicitly: **this folder will be preserved** — do not rm -rf it at the end.
Save a vault_memory entry pointing to the `/tmp` path so future sessions can find it.

### 2. Fire parallel searches — Exa + Tavily simultaneously

Run **4+ searches at once** using both skills in the same turn:

```bash
# Exa — GitHub-focused, semantic
cd ~/.agents/skills/exa
./scripts/search.sh '{"query": "<topic> API components access programmatic", "category": "github", "numResults": 10, "contents": {"summary": {"query": "<what you need>"}}}'

# Exa — MCP servers
./scripts/search.sh '{"query": "<topic> MCP server Model Context Protocol AI agent", "category": "github", "numResults": 10, "contents": {"summary": {...}}}'

# Exa — npm packages / SDKs
./scripts/search.sh '{"query": "<topic>-api npm package node SDK", "numResults": 8, "contents": {"text": true}}'

# Tavily — tutorials, official docs, design patterns
cd ~/.agents/skills/tavily
./scripts/search.sh '{"query": "<topic> REST API design tokens access tutorial", "search_depth": "advanced", "max_results": 10}'
```

Key Exa categories: `github`, `research paper`, `news`, `company`, `pdf`
Key Tavily options: `search_depth: advanced`, `include_domains: ["github.com", "docs.<tool>.com"]`

### 3. Discover official GitHub repo structure before fetching

Use GitHub API to list directories — don't guess filenames:

```bash
# List top-level skills directory
curl -sL "https://api.github.com/repos/<owner>/<repo>/contents/<path>" \
  | python3 -c "import sys,json; [print(f['name'], f.get('type','')) for f in json.load(sys.stdin) if isinstance(f,dict)]"
```

### 4. Fetch raw files in bulk

```bash
# SKILL.md files
for skill in skill-a skill-b skill-c; do
  mkdir -p "/tmp/<name>-research/official-skills/$skill"
  curl -sL "https://raw.githubusercontent.com/<owner>/<repo>/main/skills/$skill/SKILL.md" \
    -o "/tmp/<name>-research/official-skills/$skill/SKILL.md"
  wc -c "/tmp/<name>-research/official-skills/$skill/SKILL.md"
done

# Reference files
for ref in api-reference.md gotchas.md variable-patterns.md; do
  curl -sL "https://raw.githubusercontent.com/<owner>/<repo>/main/skills/<name>/references/$ref" \
    -o "/tmp/<name>-research/official-skills/<name>/references/$ref"
done
```

**Watch for 404s** — a 14-byte file is `404: Not Found`. Cross-check against the GitHub API listing.
Some repos have moved files — always list the directory first.

**Fallback for missing files:** Check if OpenAI's curated copy has them:
`https://raw.githubusercontent.com/openai/skills/main/skills/.curated/<skill-name>/SKILL.md`

### 5. Write numbered research docs

Organize findings into `/tmp/<name>-research/`:

```
00-SUMMARY.md           ← key findings, recommended architecture, next steps
01-<primary-tool>.md    ← official MCP / API / SDK deep-dive
02-rest-api.md          ← REST endpoints, auth, rate limits
03-third-party.md       ← community tools, alternatives comparison table
04-design-tokens.md     ← domain-specific topic
05-access-patterns.md   ← how to read/write the main resource
06-skill-design.md      ← use cases, architecture decisions, scripts to build
07-scripts-reference.md ← ready-to-use shell scripts
08-official-index.md    ← index of pulled official skills + diff notes
```

Each file should be self-contained and skimmable — headers, tables, code blocks.

### 6. Fetch official Exa answer for a holistic overview

```bash
cd ~/.agents/skills/exa
./scripts/answer.sh '{"query": "What is the <tool> <capability> in 2025-2026, full capabilities for AI agents?", "text": true}'
```

### 7. Save vault_memory

```
vault_memory write "<skill-name>-research"
  - /tmp location and contents
  - Key findings
  - Architecture decision made
  - "Do not delete /tmp/<name>-research"
```

---

## Key Gotchas

- **Always parallelise searches** — fire 4+ in one turn. Exa for GitHub/semantic, Tavily for tutorials/official docs.
- **GitHub raw URLs 404 silently** — a 14-byte result is a 404. Always verify with GitHub API listing first.
- **OpenAI keeps a curated copy** of Figma/Cursor skills at `openai/skills/.curated/` — useful when the original repo reorganizes.
- **Don't clean up /tmp** — the research folder is an intermediate artifact the skill-generation step reads. Tell the user it's preserved.
- **Rate limits** — Exa and Tavily have per-request costs. Cap numResults at 8-10 and use `summary` not full `text` for large batch fetches.
- **Save vault_memory immediately** — if the session ends before skill generation, the next session needs to find `/tmp/<name>-research/` without re-doing the research.

## Output

After this skill runs:
- `/tmp/<name>-research/` contains 8-10 numbered markdown docs (40-600KB total)
- `/tmp/<name>-research/official-skills/` contains raw SKILL.md + references pulled verbatim
- `vault_memory` has an entry pointing to the folder
- User is ready to run the actual skill-generation step

## Related Skills

- `skill-manager` — for deploying the generated skill once built
- `create-pi-extension` — if the result is a pi extension rather than a skill
