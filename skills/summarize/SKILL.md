---
name: summarize
description: "Fetch URL or convert local file (PDF/DOCX/HTML/etc.) to Markdown via markitdown, with optional summarization. YouTube URLs get metadata + full transcript via yt-dlp."
---

Turn "things" (URLs, PDFs, Word docs, PowerPoints, HTML pages, text files, etc.) into **Markdown** so they can be inspected/quoted/processed like normal text.

`markitdown` can fetch URLs by itself; this skill mainly wraps it to make saving + summarizing convenient.
For PDF inputs, use the `markitdown[pdf]` extra (or the wrapper below, which now does this automatically).
For **YouTube** URLs, the wrapper extracts title/description + the full spoken **transcript** via `yt-dlp` subtitles (markitdown only returns page metadata for videos).

## When to use

Use this skill when you need to:
- pull down a web page as a document-like Markdown representation
- convert binary docs (PDF/DOCX/PPTX) into Markdown for analysis
- extract a **YouTube video's transcript** to analyze what was actually said
- quickly produce a short summary of a long document before deeper work

## Quick usage

### Convert a URL or file to Markdown

Run from **this skill folder** (the agent should `cd` here first):

```bash
uvx --from 'markitdown[pdf]' markitdown <url-or-path>
```

To write Markdown to a temp file (prints the path) use the wrapper:

```bash
node to-markdown.mjs <url-or-path> --tmp
```

Tip: when summarizing, the script will **always** write the full converted Markdown to a temp `.md` file and will **always** print a final "Hint" line with the path (so you can open/inspect the full content).

Write Markdown to a specific file:

```bash
uvx --from 'markitdown[pdf]' markitdown <url-or-path> > /tmp/doc.md
```

### YouTube videos

Just pass the URL to the wrapper — no separate step needed:

```bash
node to-markdown.mjs https://www.youtube.com/watch?v=<id> --tmp
node to-markdown.mjs https://youtu.be/<id> --summary --prompt "Focus on X."
```

The wrapper detects YouTube URLs and produces Markdown with title, channel, upload date, runtime, description, and the full transcript (prefers manual subtitles, falls back to auto-generated; prefers the video's own language, then English).

**Gotcha:** the locally installed `yt-dlp` goes stale and fails with "The page needs to be reloaded" / SABR streaming errors — the wrapper runs `uvx yt-dlp` (fresh version) for this reason. If YouTube extraction breaks again, update nothing locally; the wrapper is already pinned to the latest via uvx.

### Convert + summarize with haiku-4-5 (pass context!)

Summaries are only useful when you provide **what you want extracted** and the **audience/purpose**.

```bash
node to-markdown.mjs <url-or-path> --summary --prompt "Summarize focusing on X, for audience Y. Extract Z."
```

Or:

```bash
node to-markdown.mjs <url-or-path> --summary --prompt "Focus on security implications and action items."
```

This will:
1) convert to Markdown via `uvx --from 'markitdown[pdf]' markitdown`
2) write the full Markdown to a temp `.md` file and print its path as a "Hint" line
3) run `pi --model claude-haiku-4-5` (no-tools, no-session) to summarize using your extra prompt
