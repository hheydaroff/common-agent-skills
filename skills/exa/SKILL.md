---
name: exa
description: Neural and keyword web search, content retrieval from specific URLs, find-similar pages, AI-powered answers with citations, and async deep research via the Exa API. Better than traditional search for semantic or conceptual queries, research papers, and finding related pages. Use search.sh to find pages, contents.sh to fetch full text from known URLs, find-similar.sh to discover related pages, answer.sh for direct AI answers grounded in live web data, research.sh for comprehensive multi-source reports. Requires exa_api_key in ~/.pi/.secrets/.
---

# Exa

Exa is an AI-native search engine with neural embeddings purpose-built for LLMs. Results are ranked by semantic relevance, not just keyword matches.

## Setup

Store your API key (get one at https://dashboard.exa.ai):
```bash
mkdir -p ~/.pi/.secrets
echo "your-exa-key-here" > ~/.pi/.secrets/exa_api_key && chmod 600 ~/.pi/.secrets/exa_api_key
```

## Search

Find pages by semantic or keyword query, optionally fetching content in the same call:
```bash
./scripts/search.sh '{"query": "transformer architecture explained"}'
./scripts/search.sh '{"query": "AI safety research", "category": "research paper", "numResults": 10}'
./scripts/search.sh '{"query": "latest openai news", "category": "news", "startPublishedDate": "2025-01-01"}'
./scripts/search.sh '{"query": "rust async patterns", "type": "neural", "contents": {"text": true}}'
./scripts/search.sh '{"query": "LLM architectures", "contents": {"summary": {"query": "key findings"}}}'
```

Key options: `query` (required), `type` (auto/neural/fast/deep, default auto), `numResults` (default 10), `category` (news/research paper/tweet/company/pdf/github/personal site/financial report/people), `includeDomains`/`excludeDomains`, `startPublishedDate`/`endPublishedDate` (ISO 8601), `contents` (inline content retrieval: `{"text": true}`, `{"summary": {"query": "..."}}`, `{"highlights": {"numSentences": 3}}`).

## Contents

Fetch full text from specific URLs you already have:
```bash
./scripts/contents.sh '{"urls": ["https://arxiv.org/abs/2307.06435"]}'
./scripts/contents.sh '{"urls": ["https://example.com/article"], "text": {"maxCharacters": 2000}}'
./scripts/contents.sh '{"urls": ["https://example.com/page"], "summary": {"query": "main findings"}, "highlights": {"numSentences": 3}}'
```

Key options: `urls` (required), `text` (true or `{"maxCharacters": N}`), `summary` (true or `{"query": "..."}`), `highlights` (`{"numSentences": N, "query": "..."}`).

## Find Similar

Discover pages semantically similar to a URL:
```bash
./scripts/find-similar.sh '{"url": "https://arxiv.org/abs/2307.06435"}'
./scripts/find-similar.sh '{"url": "https://example.com/paper", "numResults": 10, "excludeSourceDomain": true, "contents": {"text": true}}'
```

Key options: `url` (required), `numResults`, `excludeSourceDomain` (true/false), `contents`.

## Answer

Direct AI-generated answer grounded in live web search, with citations:
```bash
./scripts/answer.sh '{"query": "What is the current state of fusion energy research?"}'
./scripts/answer.sh '{"query": "What are the key differences between LangGraph and CrewAI?", "text": true}'
```

Key options: `query` (required), `text` (true/false — include source page text in response).

## Research

Comprehensive multi-source research report — async, takes 30-120 seconds:
```bash
./scripts/research.sh '{"query": "compare LangGraph vs CrewAI for multi-agent systems"}'
./scripts/research.sh '{"query": "fintech startup landscape 2025", "model": "exa-research-pro"}' report.md
```

Key options: `query` (required), `model` (exa-research/exa-research-pro/exa-research-fast, default exa-research). Optional second argument saves the report to a file.
