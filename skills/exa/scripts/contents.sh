#!/bin/bash
# Exa Contents — POST https://api.exa.ai/contents
# Usage: ./contents.sh '<json>'
# Example: ./contents.sh '{"urls": ["https://arxiv.org/abs/2307.06435"], "text": true}'

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
    echo "Usage: ./contents.sh '<json>'"
    echo ""
    echo "Required:  urls ([\"https://...\"])"
    echo "Optional:  text (true or {\"maxCharacters\": N})"
    echo "           summary (true or {\"query\": \"...\"})"
    echo "           highlights ({\"numSentences\": N, \"query\": \"...\"})"
    echo ""
    echo "Examples:"
    echo "  ./contents.sh '{\"urls\": [\"https://example.com/article\"], \"text\": true}'"
    echo "  ./contents.sh '{\"urls\": [\"https://example.com\"], \"summary\": {\"query\": \"main findings\"}}'"
    exit 1
fi

if ! echo "$1" | jq empty 2>/dev/null; then
    echo "Error: Invalid JSON input"; exit 1
fi

if ! echo "$1" | jq -e '.urls' >/dev/null 2>&1; then
    echo "Error: 'urls' is required"; exit 1
fi

curl -sf --request POST \
    --url "https://api.exa.ai/contents" \
    --header "x-api-key: $EXA_API_KEY" \
    --header "Content-Type: application/json" \
    --data "$1" \
    | jq '.'
