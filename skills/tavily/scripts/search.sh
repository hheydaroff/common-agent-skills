#!/bin/bash
# Tavily Search — POST https://api.tavily.com/search
# Usage: ./search.sh '<json>'
# Example: ./search.sh '{"query": "AI news", "time_range": "week", "max_results": 10}'

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
    echo "Usage: ./search.sh '<json>'"
    echo ""
    echo "Required:  query (string)"
    echo "Optional:  max_results (1-20, default 10)"
    echo "           search_depth (ultra-fast|fast|basic|advanced, default basic)"
    echo "           time_range (day|week|month|year)"
    echo "           start_date / end_date (YYYY-MM-DD)"
    echo "           include_domains / exclude_domains ([\"domain.com\"])"
    echo "           include_raw_content (true/false)"
    echo ""
    echo "Example:"
    echo "  ./search.sh '{\"query\": \"rust async patterns\", \"search_depth\": \"advanced\"}'"
    exit 1
fi

if ! echo "$1" | jq empty 2>/dev/null; then
    echo "Error: Invalid JSON input"; exit 1
fi

if ! echo "$1" | jq -e '.query' >/dev/null 2>&1; then
    echo "Error: 'query' is required"; exit 1
fi

curl -sf --request POST \
    --url "https://api.tavily.com/search" \
    --header "Authorization: Bearer $TAVILY_API_KEY" \
    --header "Content-Type: application/json" \
    --data "$1" \
    | jq '.'
