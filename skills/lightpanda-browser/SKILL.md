---
name: lightpanda-browser
description: Headless browser automation via Lightpanda and Chrome DevTools Protocol. Use when you need to fetch web pages, extract content, evaluate JavaScript, or automate headless browsing without requiring a full Chrome installation. Lightweight alternative to browser-tools that works on any Linux system.
---

# Lightpanda Browser

Headless browser tools powered by [Lightpanda](https://github.com/lightpanda-io/browser) — a fast, lightweight browser with CDP support. No Chrome installation required.

## Prerequisites

Lightpanda binary must be installed and on PATH:

```bash
# Download for Linux x86_64
wget -q "https://github.com/lightpanda-io/browser/releases/download/nightly/lightpanda-x86_64-linux" -O ~/.local/bin/lightpanda
chmod +x ~/.local/bin/lightpanda
```

Install npm dependencies:

```bash
cd {baseDir}/lightpanda-browser
npm install
```

## Quick Fetch (No Server Needed)

For simple page fetching, use Lightpanda directly — no CDP server required:

```bash
lightpanda fetch --dump markdown https://example.com
lightpanda fetch --dump html https://example.com
lightpanda fetch --dump markdown --strip-mode full https://example.com
```

Options:
- `--dump markdown|html|semantic_tree|semantic_tree_text` — output format
- `--strip-mode js,css,ui,full` — remove tag groups from output
- `--wait-until load|domcontentloaded|networkidle|done` — wait strategy
- `--wait-ms 5000` — wait time in milliseconds
- `--with-frames` — include iframe contents

This is the **preferred approach** for most use cases. Use CDP mode only when you need JavaScript evaluation.

## CDP Server Mode

For JavaScript evaluation, content extraction with Readability, or cookie inspection.

**Important**: Lightpanda creates a fresh session per WebSocket connection, so each tool call is self-contained — it connects, navigates, performs its action, and disconnects. There is no persistent page state between calls.

### Start Server

```bash
node {baseDir}/lightpanda-browser/lp-start.js
```

Starts Lightpanda CDP server on `:9222` (or `LP_PORT` env var). Checks if already running first.

### Stop Server

```bash
node {baseDir}/lightpanda-browser/lp-stop.js
```

### Navigate (Test Connectivity)

```bash
node {baseDir}/lightpanda-browser/lp-nav.js https://example.com
```

Navigates to URL and prints the page title. Useful for testing the server is working.

### Evaluate JavaScript

```bash
node {baseDir}/lightpanda-browser/lp-eval.js https://example.com 'document.title'
node {baseDir}/lightpanda-browser/lp-eval.js https://example.com 'document.querySelectorAll("a").length'
node {baseDir}/lightpanda-browser/lp-eval.js https://example.com '(function(){ return Array.from(document.querySelectorAll("a")).map(a => ({text: a.textContent.trim(), href: a.href})); })()'
```

Navigates to URL then executes JavaScript and returns the result.

### Extract Content as Markdown

```bash
node {baseDir}/lightpanda-browser/lp-content.js https://example.com
```

Navigates to URL and extracts readable content as markdown using Mozilla Readability + Turndown.

### Get Cookies

```bash
node {baseDir}/lightpanda-browser/lp-cookies.js https://example.com
```

Navigates to URL and displays cookies set by the page.

## Environment Variables

- `LP_HOST` — CDP server host (default: `127.0.0.1`)
- `LP_PORT` — CDP server port (default: `9222`)

## When to Use

- **Simple page fetch**: Use `lightpanda fetch --dump markdown <url>` directly
- **JavaScript evaluation**: Use CDP mode (`lp-start.js` + `lp-eval.js`)
- **Rich content extraction**: Use `lp-content.js` for Readability-parsed markdown
- **No Chrome available**: Works on any Linux system with just the Lightpanda binary
- **Server/CI environments**: Fully headless, no GUI needed

## Efficiency Guide

### Prefer Direct Fetch

For read-only page content, skip CDP entirely:

```bash
lightpanda fetch --dump markdown https://example.com
```

### Complex Scripts in Single Calls

Since each eval is a fresh page, do everything in one call:

```javascript
(function() {
  const links = Array.from(document.querySelectorAll('a[href]')).map(a => ({
    text: a.textContent.trim(), href: a.href
  }));
  const title = document.title;
  return JSON.stringify({ title, linkCount: links.length, links: links.slice(0, 20) });
})()
```

### Limitations

- No visual rendering / screenshots (headless only)
- No interactive element picker (no GUI)
- No persistent state between CDP tool calls (each is a fresh session)
- Some JavaScript-heavy SPAs may not fully render
