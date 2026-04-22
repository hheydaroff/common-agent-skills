#!/bin/bash
# Exa Find Similar — POST https://api.exa.ai/findSimilar
# Usage: ./find-similar.sh '<json>'
# Example: ./find-similar.sh '{"url": "https://arxiv.org/abs/2307.06435", "numResults": 5}'

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
    echo "Usage: ./find-similar.sh '<json>'"
    echo ""
    echo "Required:  url (string)"
    echo "Optional:  numResults (default 10)"
    echo "           excludeSourceDomain (true/false)"
    echo "           contents ({\"text\": true} or {\"summary\": {\"query\": \"...\"}})"
    echo ""
    echo "Examples:"
    echo "  ./find-similar.sh '{\"url\": \"https://arxiv.org/abs/2307.06435\"}'"
    echo "  ./find-similar.sh '{\"url\": \"https://example.com/paper\", \"excludeSourceDomain\": true, \"numResults\": 10}'"
    exit 1
fi

if ! echo "$1" | jq empty 2>/dev/null; then
    echo "Error: Invalid JSON input"; exit 1
fi

if ! echo "$1" | jq -e '.url' >/dev/null 2>&1; then
    echo "Error: 'url' is required"; exit 1
fi

curl -sf --request POST \
    --url "https://api.exa.ai/findSimilar" \
    --header "x-api-key: $EXA_API_KEY" \
    --header "Content-Type: application/json" \
    --data "$1" \
    | jq '.'
