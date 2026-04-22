---
name: tavily
description: Web search, URL content extraction, site crawling, and deep research via the Tavily API. Use search.sh to find current web information on any topic. Use extract.sh to get clean content from specific URLs you already know. Use crawl.sh to download an entire site or documentation as markdown. Use research.sh for comprehensive multi-source research reports with citations. Requires tavily_api_key in ~/.pi/.secrets/.
---

# Tavily

Tavily is a search API built for LLMs — results are pre-processed and optimised for AI consumption.

## Setup

Store your API key (get one at https://app.tavily.com):
```bash
mkdir -p ~/.pi/.secrets
echo "tvly-your-key-here" > ~/.pi/.secrets/tavily_api_key && chmod 600 ~/.pi/.secrets/tavily_api_key
```

## Search

Find web pages on any topic:
```bash
./scripts/search.sh '{"query": "latest rust async patterns"}'
./scripts/search.sh '{"query": "AI news", "time_range": "week", "max_results": 10}'
./scripts/search.sh '{"query": "site reliability engineering", "search_depth": "advanced", "include_domains": ["sre.google", "github.com"]}'
```

Key options: `query` (required), `max_results` (1-20, default 10), `search_depth` (ultra-fast/fast/basic/advanced), `time_range` (day/week/month/year), `include_domains`, `exclude_domains`.

## Extract

Get clean content from specific URLs you already have:
```bash
./scripts/extract.sh '{"urls": ["https://docs.example.com/api"]}'
./scripts/extract.sh '{"urls": ["https://example.com/page1", "https://example.com/page2"], "query": "authentication"}'
./scripts/extract.sh '{"urls": ["https://spa.example.com"], "extract_depth": "advanced"}'
```

Key options: `urls` (required, max 20), `query` (reranks chunks by relevance), `extract_depth` (basic/advanced — use advanced for JS-rendered pages).

## Crawl

Download multiple pages from a site:
```bash
./scripts/crawl.sh '{"url": "https://docs.example.com"}'
./scripts/crawl.sh '{"url": "https://docs.example.com", "max_depth": 2, "limit": 50}' ./output-dir
./scripts/crawl.sh '{"url": "https://example.com", "instructions": "Find API reference pages", "chunks_per_source": 3}'
```

Key options: `url` (required), `max_depth` (1-5, start with 1), `limit` (total pages cap), `instructions` (semantic focus — use with `chunks_per_source` when feeding into LLM context), `select_paths`/`exclude_paths` (regex). Optional second argument saves each page as a markdown file in the given directory.

## Research

Comprehensive research report with citations — takes 30-120 seconds:
```bash
./scripts/research.sh '{"input": "compare LangGraph vs CrewAI for multi-agent systems", "model": "pro"}'
./scripts/research.sh '{"input": "fintech startup landscape 2025", "model": "pro"}' report.md
```

Key options: `input` (required), `model` (mini=fast/focused, pro=comprehensive/multi-angle). Optional second argument saves the report to a file.
