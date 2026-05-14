#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "requests",
#   "beautifulsoup4",
# ]
# ///
"""
DuckDuckGo search tool for CORTEX vault.
Usage: uv run ddg_search.py "your query" [--num 5] [--fetch-content]
"""

import sys
import argparse
import requests
from bs4 import BeautifulSoup
import json
import time

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'https://duckduckgo.com/',
}

def search(query, num_results=5):
    """Search DuckDuckGo and return structured results."""
    try:
        session = requests.Session()
        session.get('https://duckduckgo.com/', headers=HEADERS, timeout=10)
        r = session.get('https://html.duckduckgo.com/html/', params={'q': query}, headers=HEADERS, timeout=10)
        r.raise_for_status()
    except requests.RequestException as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

    soup = BeautifulSoup(r.text, 'html.parser')
    results = []

    all_items = [i for i in soup.select('.result__body') if not i.find_parent(class_='result--ad')]
    for item in all_items[:num_results]:
        title_el = item.select_one('.result__title')
        snippet_el = item.select_one('.result__snippet')
        url_el = item.select_one('.result__url')
        link_el = item.select_one('a.result__a')

        title = title_el.get_text(strip=True) if title_el else ''
        snippet = snippet_el.get_text(strip=True) if snippet_el else ''
        display_url = url_el.get_text(strip=True) if url_el else ''
        href = link_el['href'] if link_el and link_el.get('href') else ''

        # DDG wraps URLs in a redirect — extract actual URL
        if 'uddg=' in href:
            from urllib.parse import urlparse, parse_qs, unquote
            parsed = parse_qs(urlparse(href).query)
            href = unquote(parsed.get('uddg', [href])[0])

        if title:
            results.append({
                'title': title,
                'url': href or f'https://{display_url}',
                'display_url': display_url,
                'snippet': snippet,
            })

    return results

def fetch_page_text(url, max_chars=3000):
    """Fetch a URL and extract readable text."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        # Remove scripts, styles, nav
        for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
            tag.decompose()
        text = soup.get_text(separator='\n', strip=True)
        # Collapse excessive blank lines
        lines = [l for l in text.splitlines() if l.strip()]
        return '\n'.join(lines)[:max_chars]
    except Exception as e:
        return f"[Could not fetch page: {e}]"

def format_results(results, fetch_content=False):
    """Pretty-print results for Claude to consume."""
    if not results:
        print("No results found.")
        return

    for i, r in enumerate(results, 1):
        print(f"\n{'='*60}")
        print(f"[{i}] {r['title']}")
        print(f"URL: {r['url']}")
        print(f"Snippet: {r['snippet']}")
        if fetch_content:
            print(f"\n--- Page Content ---")
            print(fetch_page_text(r['url']))
            time.sleep(0.5)  # polite delay
    print(f"\n{'='*60}")

def main():
    parser = argparse.ArgumentParser(description='DuckDuckGo search')
    parser.add_argument('query', help='Search query')
    parser.add_argument('--num', type=int, default=5, help='Number of results (default: 5)')
    parser.add_argument('--fetch-content', action='store_true', help='Fetch full page text for each result')
    parser.add_argument('--json', action='store_true', help='Output raw JSON')
    args = parser.parse_args()

    results = search(args.query, args.num)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        format_results(results, fetch_content=args.fetch_content)

if __name__ == '__main__':
    main()
