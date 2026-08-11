# Fast Headless Fetch (Lightpanda)

For read-only page fetching, [Lightpanda](https://github.com/lightpanda-io/browser) is ~10x faster than launching Chrome and needs no browser window. Use it when you only need page content — never for multi-step interaction.

## Prerequisites

```bash
# macOS (arm64): download from https://github.com/lightpanda-io/browser/releases (nightly)
# place binary on PATH as `lightpanda`
```

## One-shot fetch (no server)

```bash
lightpanda fetch --dump markdown https://example.com
lightpanda fetch --dump html --strip-mode js,css,ui https://example.com
lightpanda fetch --dump semantic_tree_text --wait-until networkidle https://example.com
```

Options:
- `--dump markdown|html|semantic_tree|semantic_tree_text` — output format
- `--strip-mode js,css,ui,full` — remove tag groups
- `--wait-until load|domcontentloaded|networkidle|done` — wait strategy

JS-rendered content works (verified: dynamic pages render correctly, ~0.7s).

## Limitations (tested)

- **Stateless**: every connection is a fresh session — cookies/logins do NOT persist between calls. Login → navigate → scrape flows are impossible. Use the Chrome CDP workflow in this skill for anything stateful.
- No screenshots.
- `lightpanda serve` defaults to port 9222 — same as Chrome remote debugging. If Chrome is running on :9222, use `--port 9223`.

## When to use which

| Need | Use |
|------|-----|
| Grab page content fast, no auth | Lightpanda fetch |
| Any interaction, login, cookies, screenshots, multi-step | Chrome CDP (main skill) |
