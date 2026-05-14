---
name: ddg-search
description: Search the web using DuckDuckGo. No API key required. Use when user asks to "search for", "look up", "find articles about", or needs current information from the web and no paid search API is available.
---

# DuckDuckGo Web Search

Free web search via DuckDuckGo's HTML interface. No API key needed — works immediately as a fallback when Tavily/Exa are unavailable.

## When to Use

- User asks to search / look up / find articles about something
- No Tavily or Exa API key is configured
- Need a quick, free web search without setup

## Search

```bash
./scripts/search.py "your query"
./scripts/search.py "your query" --num 10
./scripts/search.py "your query" --num 3 --fetch-content
./scripts/search.py "your query" --json
```

Options:
- `--num N` — number of results (default: 5)
- `--fetch-content` — also fetch and extract readable text from each result page (first 3000 chars)
- `--json` — output raw JSON instead of formatted text

## Output

Each result returns:
- **Title** — page title
- **URL** — full URL
- **Snippet** — short description from DDG

With `--fetch-content`: also returns first 3000 chars of extracted page text.

## Limitations

- No JavaScript-rendered pages (SPAs may return empty content)
- May be rate-limited if queries are too frequent — add 1-2s delay between calls
- Results may be less fresh than Tavily/Exa
- No advanced features (no categories, no date filtering, no content summaries)

## When to Upgrade

If `~/.pi/.secrets/tavily_api_key` or `~/.pi/.secrets/exa_api_key` exists, prefer the `tavily` or `exa` skills instead — they offer richer results, date filtering, domain scoping, and content extraction.
