#!/bin/bash
# Tavily Crawl — POST https://api.tavily.com/crawl
# Usage: ./crawl.sh '<json>' [output_dir]
# Example: ./crawl.sh '{"url": "https://docs.example.com", "max_depth": 2}' ./docs

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
    echo "Usage: ./crawl.sh '<json>' [output_dir]"
    echo ""
    echo "Required:  url (string)"
    echo "Optional:  max_depth (1-5, default 1 — start here)"
    echo "           limit (total pages cap, default 50)"
    echo "           instructions (semantic focus, use with chunks_per_source for LLM context)"
    echo "           chunks_per_source (1-5, requires instructions)"
    echo "           select_paths / exclude_paths ([\"regex\"])"
    echo "           extract_depth (basic|advanced)"
    echo "           format (markdown|text)"
    echo ""
    echo "  output_dir  optional — saves each page as a .md file"
    echo ""
    echo "Examples:"
    echo "  ./crawl.sh '{\"url\": \"https://docs.example.com\"}'"
    echo "  ./crawl.sh '{\"url\": \"https://docs.example.com\", \"max_depth\": 2, \"instructions\": \"Find API docs\", \"chunks_per_source\": 3}'"
    echo "  ./crawl.sh '{\"url\": \"https://docs.example.com\", \"max_depth\": 2}' ./output"
    exit 1
fi

if ! echo "$1" | jq empty 2>/dev/null; then
    echo "Error: Invalid JSON input"; exit 1
fi

if ! echo "$1" | jq -e '.url' >/dev/null 2>&1; then
    echo "Error: 'url' is required"; exit 1
fi

OUTPUT_DIR="$2"

RESPONSE=$(curl -sf --request POST \
    --url "https://api.tavily.com/crawl" \
    --header "Authorization: Bearer $TAVILY_API_KEY" \
    --header "Content-Type: application/json" \
    --data "$1")

if [ -n "$OUTPUT_DIR" ]; then
    mkdir -p "$OUTPUT_DIR"
    PAGE_COUNT=$(echo "$RESPONSE" | jq '.results | length')
    echo "Saving $PAGE_COUNT pages to $OUTPUT_DIR..."
    echo "$RESPONSE" | jq -r '.results[] | @base64' | while read -r encoded; do
        result=$(echo "$encoded" | base64 -d)
        url=$(echo "$result" | jq -r '.url')
        content=$(echo "$result" | jq -r '.raw_content // ""')
        # Derive filename from URL path
        filename=$(echo "$url" | sed 's|https\?://||' | sed 's|[/:]|_|g' | sed 's|_$||').md
        echo "$content" > "$OUTPUT_DIR/$filename"
        echo "  Saved: $filename"
    done
    echo "Done. $PAGE_COUNT pages saved to $OUTPUT_DIR"
else
    echo "$RESPONSE" | jq '.'
fi
