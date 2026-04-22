#!/bin/bash
# Exa Research — POST https://api.exa.ai/research/v1 (async, polls until complete)
# Usage: ./research.sh '<json>' [output_file]
# Example: ./research.sh '{"query": "LangGraph vs CrewAI for multi-agent systems", "model": "exa-research-pro"}' report.md

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
    echo "Usage: ./research.sh '<json>' [output_file]"
    echo ""
    echo "Required:  query (string)"
    echo "Optional:  model (exa-research|exa-research-pro|exa-research-fast, default exa-research)"
    echo "             exa-research      — balanced speed and quality"
    echo "             exa-research-pro  — comprehensive, higher quality"
    echo "             exa-research-fast — faster, good for simpler topics"
    echo ""
    echo "  output_file  optional — saves the report to a file"
    echo ""
    echo "Examples:"
    echo "  ./research.sh '{\"query\": \"what is retrieval augmented generation\"}'"
    echo "  ./research.sh '{\"query\": \"LangGraph vs CrewAI\", \"model\": \"exa-research-pro\"}' report.md"
    exit 1
fi

if ! echo "$1" | jq empty 2>/dev/null; then
    echo "Error: Invalid JSON input"; exit 1
fi

if ! echo "$1" | jq -e '.query' >/dev/null 2>&1; then
    echo "Error: 'query' is required"; exit 1
fi

OUTPUT_FILE="$2"
QUERY=$(echo "$1" | jq -r '.query')
MODEL=$(echo "$1" | jq -r '.model // "exa-research"')

echo "Starting research: $QUERY (model: $MODEL)" >&2
echo "This may take 30-120 seconds..." >&2

START_RESPONSE=$(curl -sf --request POST \
    --url "https://api.exa.ai/research/v1" \
    --header "x-api-key: $EXA_API_KEY" \
    --header "Content-Type: application/json" \
    --data "$1")

RESEARCH_ID=$(echo "$START_RESPONSE" | jq -r '.researchId // .id // empty')

if [ -z "$RESEARCH_ID" ]; then
    echo "Error: Failed to start research job"
    echo "$START_RESPONSE" | jq '.'
    exit 1
fi

echo "Research job started (id: $RESEARCH_ID), polling for results..." >&2

TIMEOUT=180
ELAPSED=0
INTERVAL=5

while [ $ELAPSED -lt $TIMEOUT ]; do
    sleep $INTERVAL
    ELAPSED=$((ELAPSED + INTERVAL))

    POLL_RESPONSE=$(curl -sf --request GET \
        --url "https://api.exa.ai/research/v1/$RESEARCH_ID" \
        --header "x-api-key: $EXA_API_KEY")

    STATUS=$(echo "$POLL_RESPONSE" | jq -r '.status // empty')

    if [ "$STATUS" = "completed" ]; then
        RESULT=$(echo "$POLL_RESPONSE" | jq -r '.output // .result // .')
        if [ -n "$OUTPUT_FILE" ]; then
            echo "$RESULT" > "$OUTPUT_FILE"
            echo "Report saved to: $OUTPUT_FILE" >&2
        else
            echo "$RESULT"
        fi
        exit 0
    elif [ "$STATUS" = "failed" ] || [ "$STATUS" = "error" ]; then
        echo "Error: Research job failed"
        echo "$POLL_RESPONSE" | jq '.'
        exit 1
    fi

    echo "  Status: $STATUS (${ELAPSED}s elapsed)" >&2
done

echo "Error: Research timed out after ${TIMEOUT}s (id: $RESEARCH_ID)" >&2
exit 1
