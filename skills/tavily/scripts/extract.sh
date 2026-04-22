#!/bin/bash
# Tavily Extract — POST https://api.tavily.com/extract
# Usage: ./extract.sh '<json>'
# Example: ./extract.sh '{"urls": ["https://docs.example.com/api"], "query": "authentication"}'

set -e

SECRETS_FILE="$HOME/.pi/.secrets/tavily_api_key"

if [ -z "$TAVILY_API_KEY" ]; then
    if [ ! -f "$SECRETS_FILE" ]; then
        echo "Error: No Tavily API key found."
        echo "Create one at https://app.tavily.com and store it:"
        echo "  echo 'tvly-...' > $SECRETS_FILE && chmod 600 $SECRETS_FILE"
        exit 1
    fi
    TAVILY_API_KEY=$(cat "$SECRETS_FILE")
fi

if [ -z "$1" ]; then
    echo "Usage: ./extract.sh '<json>'"
    echo ""
    echo "Required:  urls ([\"https://...\"], max 20)"
    echo "Optional:  query (reranks chunks by relevance)"
    echo "           chunks_per_source (1-5, requires query)"
    echo "           extract_depth (basic|advanced — use advanced for JS pages)"
    echo "           format (markdown|text, default markdown)"
    echo ""
    echo "Examples:"
    echo "  ./extract.sh '{\"urls\": [\"https://example.com/docs\"]}'"
    echo "  ./extract.sh '{\"urls\": [\"https://spa.example.com\"], \"extract_depth\": \"advanced\"}'"
    exit 1
fi

if ! echo "$1" | jq empty 2>/dev/null; then
    echo "Error: Invalid JSON input"; exit 1
fi

if ! echo "$1" | jq -e '.urls' >/dev/null 2>&1; then
    echo "Error: 'urls' is required"; exit 1
fi

curl -sf --request POST \
    --url "https://api.tavily.com/extract" \
    --header "Authorization: Bearer $TAVILY_API_KEY" \
    --header "Content-Type: application/json" \
    --data "$1" \
    | jq '.'
