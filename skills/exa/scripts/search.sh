#!/bin/bash
# Exa Search — POST https://api.exa.ai/search
# Usage: ./search.sh '<json>'
# Example: ./search.sh '{"query": "AI safety research", "category": "research paper", "numResults": 5}'

set -e

SECRETS_FILE="$HOME/.pi/.secrets/exa_api_key"

if [ -z "$EXA_API_KEY" ]; then
    if [ ! -f "$SECRETS_FILE" ]; then
        echo "Error: No Exa API key found."
        echo "Get one at https://dashboard.exa.ai and store it:"
        echo "  echo 'your-key' > $SECRETS_FILE && chmod 600 $SECRETS_FILE"
        exit 1
    fi
    EXA_API_KEY=$(cat "$SECRETS_FILE")
fi

if [ -z "$1" ]; then
    echo "Usage: ./search.sh '<json>'"
    echo ""
    echo "Required:  query (string)"
    echo "Optional:  type (auto|neural|fast|deep, default auto)"
    echo "           numResults (default 10)"
    echo "           category (news|research paper|tweet|company|pdf|github|personal site|financial report|people)"
    echo "           includeDomains / excludeDomains ([\"domain.com\"])"
    echo "           startPublishedDate / endPublishedDate (ISO 8601, e.g. 2025-01-01)"
    echo "           contents (inline retrieval: {\"text\": true} or {\"summary\": {\"query\": \"...\"}})"
    echo ""
    echo "Examples:"
    echo "  ./search.sh '{\"query\": \"rust async patterns\"}'"
    echo "  ./search.sh '{\"query\": \"AI papers\", \"category\": \"research paper\", \"contents\": {\"text\": true}}'"
    exit 1
fi

if ! echo "$1" | jq empty 2>/dev/null; then
    echo "Error: Invalid JSON input"; exit 1
fi

if ! echo "$1" | jq -e '.query' >/dev/null 2>&1; then
    echo "Error: 'query' is required"; exit 1
fi

curl -sf --request POST \
    --url "https://api.exa.ai/search" \
    --header "x-api-key: $EXA_API_KEY" \
    --header "Content-Type: application/json" \
    --data "$1" \
    | jq '.'
