#!/bin/bash
# Tavily Research — POST https://api.tavily.com/research (async, polls until complete)
# Usage: ./research.sh '<json>' [output_file]
# Example: ./research.sh '{"input": "LangGraph vs CrewAI", "model": "pro"}' report.md

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
    echo "Usage: ./research.sh '<json>' [output_file]"
    echo ""
    echo "Required:  input (string — research topic or question)"
    echo "Optional:  model (mini|pro|auto, default mini)"
    echo "             mini — targeted, ~30s, good for single-topic questions"
    echo "             pro  — comprehensive, ~60-120s, good for comparisons and reports"
    echo ""
    echo "  output_file  optional — saves the report to a file"
    echo ""
    echo "Examples:"
    echo "  ./research.sh '{\"input\": \"what is retrieval augmented generation\"}'"
    echo "  ./research.sh '{\"input\": \"LangGraph vs CrewAI for multi-agent systems\", \"model\": \"pro\"}' report.md"
    exit 1
fi

if ! echo "$1" | jq empty 2>/dev/null; then
    echo "Error: Invalid JSON input"; exit 1
fi

if ! echo "$1" | jq -e '.input' >/dev/null 2>&1; then
    echo "Error: 'input' is required"; exit 1
fi

INPUT=$(echo "$1" | jq -r '.input')
MODEL=$(echo "$1" | jq -r '.model // "mini"')
OUTPUT_FILE="$2"

echo "Starting research: $INPUT (model: $MODEL)" >&2
echo "This may take 30-120 seconds..." >&2

# Start async research job
START_RESPONSE=$(curl -sf --request POST \
    --url "https://api.tavily.com/research" \
    --header "Authorization: Bearer $TAVILY_API_KEY" \
    --header "Content-Type: application/json" \
    --data "$1")

REQUEST_ID=$(echo "$START_RESPONSE" | jq -r '.request_id // empty')

if [ -z "$REQUEST_ID" ]; then
    echo "Error: Failed to start research job"
    echo "$START_RESPONSE" | jq '.'
    exit 1
fi

echo "Research job started (id: $REQUEST_ID), polling for results..." >&2

# Poll until complete
TIMEOUT=180
ELAPSED=0
INTERVAL=5

while [ $ELAPSED -lt $TIMEOUT ]; do
    sleep $INTERVAL
    ELAPSED=$((ELAPSED + INTERVAL))

    POLL_RESPONSE=$(curl -sf --request GET \
        --url "https://api.tavily.com/research/$REQUEST_ID" \
        --header "Authorization: Bearer $TAVILY_API_KEY")

    STATUS=$(echo "$POLL_RESPONSE" | jq -r '.status // empty')

    if [ "$STATUS" = "completed" ]; then
        RESULT=$(echo "$POLL_RESPONSE" | jq -r '.content // .')
        if [ -n "$OUTPUT_FILE" ]; then
            echo "$RESULT" > "$OUTPUT_FILE"
            echo "Report saved to: $OUTPUT_FILE" >&2
        else
            echo "$RESULT"
        fi
        exit 0
    elif [ "$STATUS" = "failed" ]; then
        echo "Error: Research job failed"
        echo "$POLL_RESPONSE" | jq '.'
        exit 1
    fi

    echo "  Status: $STATUS (${ELAPSED}s elapsed)" >&2
done

echo "Error: Research timed out after ${TIMEOUT}s (request_id: $REQUEST_ID)" >&2
exit 1
