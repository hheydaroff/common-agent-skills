---
name: mcp-tools
description: Call Docker MCP tools (web search, browser, Atlassian, fetch) from any agent via mcporter CLI. Use when you need to search the web, fetch URLs, automate a browser, or query Jira/Confluence but have no native MCP support (e.g. Pi coding agent).
---

# MCP Tools via mcporter

Bridges Docker MCP Gateway tools into bash-callable commands. Requires `mcporter` and Docker Desktop with MCP enabled.

## Prerequisites (one-time setup)

```bash
# 1. Install mcporter
npm install -g mcporter

# 2. Configure mcporter to use Docker MCP Gateway
mkdir -p ~/.mcporter
python3 -c "
import json
config = {'mcpServers': {'MCP_DOCKER': {'command': 'docker', 'args': ['mcp', 'gateway', 'run']}}}
open('/Users/' + __import__('os').getenv('USER') + '/.mcporter/mcporter.json', 'w').write(json.dumps(config, indent=2))
"

# 3. Verify discovery (mcporter auto-discovers from Claude Code config too)
mcporter list MCP_DOCKER
```

## Calling Tools

### General syntax
```bash
mcporter call MCP_DOCKER.<tool_name> --param1 "value" --param2 "value"
```

### Web Search (Tavily)
```bash
mcporter call MCP_DOCKER.tavily_search --query "your search query"
mcporter call MCP_DOCKER.tavily_research --input "deep research question"
mcporter call MCP_DOCKER.tavily_extract --urls '["https://example.com"]'
```

### Fetch URL
```bash
mcporter call MCP_DOCKER.fetch --url "https://example.com"
mcporter call MCP_DOCKER.fetch --url "https://example.com" --max_length 3000
```

### Browser Automation
```bash
# Navigate and capture content
mcporter call MCP_DOCKER.browser_navigate --url "https://example.com"
mcporter call MCP_DOCKER.browser_snapshot   # accessibility snapshot (preferred over screenshot)
mcporter call MCP_DOCKER.browser_take_screenshot --type png

# Interact
mcporter call MCP_DOCKER.browser_click --ref "<element-ref-from-snapshot>"
mcporter call MCP_DOCKER.browser_type --ref "<ref>" --text "hello"
```

### Atlassian (Jira / Confluence)
```bash
# Get your cloud ID first
mcporter call MCP_DOCKER.getAccessibleAtlassianResources

# Search across Jira + Confluence
mcporter call MCP_DOCKER.search --query "your query"

# Jira
mcporter call MCP_DOCKER.getJiraIssue --cloudId "<id>" --issueIdOrKey "PROJ-123"
mcporter call MCP_DOCKER.searchJiraIssuesUsingJql \
  --cloudId "<id>" \
  --jql "project = DATA AND status != Done ORDER BY updated DESC" \
  --maxResults 10

# Confluence
mcporter call MCP_DOCKER.getConfluencePage --cloudId "<id>" --pageId "12345"
```

## Parsing Output

All tools return JSON. Pipe through python for readability:

```bash
mcporter call MCP_DOCKER.tavily_search --query "AI news" | python3 -m json.tool

# Extract a field
mcporter call MCP_DOCKER.getJiraIssue --cloudId "<id>" --issueIdOrKey "PROJ-1" \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['fields']['summary'])"
```

## Performance Tip

Start the mcporter daemon to keep the Docker gateway warm between calls:

```bash
mcporter daemon start   # run once per session
# ... make multiple mcporter call commands ...
mcporter daemon stop
```

Without the daemon, each call cold-starts the Docker container (~2–3s overhead).

## Discovering Available Tools

```bash
mcporter list MCP_DOCKER                           # all tools
mcporter list MCP_DOCKER.browser_snapshot          # inspect params for one tool
```
