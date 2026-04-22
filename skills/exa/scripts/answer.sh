#!/bin/bash
# Exa Answer — POST https://api.exa.ai/answer
# Usage: ./answer.sh '<json>'
# Example: ./answer.sh '{"query": "What is the current state of fusion energy research?"}'

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
    echo "Usage: ./answer.sh '<json>'"
    echo ""
    echo "Required:  query (string)"
    echo "Optional:  text (true/false — include source page text in response)"
    echo ""
    echo "Examples:"
    echo "  ./answer.sh '{\"query\": \"What is the latest valuation of SpaceX?\"}'"
    echo "  ./answer.sh '{\"query\": \"Key differences between LangGraph and CrewAI?\", \"text\": true}'"
    exit 1
fi

if ! echo "$1" | jq empty 2>/dev/null; then
    echo "Error: Invalid JSON input"; exit 1
fi

if ! echo "$1" | jq -e '.query' >/dev/null 2>&1; then
    echo "Error: 'query' is required"; exit 1
fi

curl -sf --request POST \
    --url "https://api.exa.ai/answer" \
    --header "x-api-key: $EXA_API_KEY" \
    --header "Content-Type: application/json" \
    --data "$1" \
    | jq '.'
