> **Local addition** (from the user's `bedrock-prompt-caching` skill).
> Authoritative mechanics, model token thresholds, TTL matrix, debug workflow and break-even
> math live in [references/prompt-caching.md](references/bedrock/references/prompt-caching.md).
> This file is the TypeScript/`ConverseStreamCommand` implementation recipe — read both.
> Paths are relative to the `aws` skill root.

# Bedrock Prompt Caching

## When to Use
- Project calls AWS Bedrock with large static system prompts (>1024 tokens)
- Multi-turn agentic flows where system prompt + tools are re-sent every turn
- Want to reduce input token costs by up to 90% and latency by up to 85%
- Using Claude Sonnet 4+ or Claude Opus 4+ models on Bedrock

## Prerequisites
- `@aws-sdk/client-bedrock-runtime` ≥ 3.750 (cachePoint support)
- Model must support prompt caching (see limits below)

## Model Limits

| Model | Min tokens/checkpoint | Max checkpoints | TTL |
|-------|----------------------|-----------------|-----|
| Claude Sonnet 4.6 | 1,024 | 4 | 5min |
| Claude Opus 4.5/4.6, Haiku 4.5, Sonnet 4.5 | 4,096 | 4 | 5min or 1h |
| Claude 3.7 Sonnet | 1,024 | 4 | 5min |

## Steps

### 1. Identify Static Content

Categorize your prompt into:
- **Static** (same every request): system prompt, tool definitions, few-shot examples, documents
- **Dynamic** (changes per request): user messages, conversation history, tool results

### 2. Add cachePoint to System Prompt

```typescript
const command = new ConverseStreamCommand({
  modelId: MODEL_ID,
  system: [
    { text: SYSTEM_PROMPT },
    { cachePoint: { type: "default" } },  // ← Cache checkpoint
  ] as unknown[],  // TypeScript needs this cast for discriminated unions
  messages: converseMessages,
  toolConfig,
} as ConverseStreamCommandInput);
```

### 3. Add cachePoint to Tools

```typescript
const toolConfig = {
  tools: [
    ...TOOL_DEFINITIONS.map((t) => ({
      toolSpec: { name: t.name, description: t.desc, inputSchema: { json: t.schema } },
    })),
    { cachePoint: { type: "default" } },  // ← After all tool specs
  ] as unknown[],
};
```

### 4. Cache Conversation History (Multi-Turn Agent Loops)

In agentic flows where the same messages array grows each turn (tool calls → results → more tool calls), the conversation PREFIX is immutable between turns. Cache it:

```typescript
// Inject cachePoint into second-to-last message's content.
// Everything before it was identical in the previous request → cache hit.
const converseMessages = toBedrockMessages(messages);

if (converseMessages.length >= 3) {
  const secondToLast = converseMessages[converseMessages.length - 2];
  if (Array.isArray(secondToLast.content)) {
    (secondToLast.content as unknown[]).push({ cachePoint: { type: "default" } });
  }
}
```

**Why second-to-last?** On turn N, messages[0..N-2] were already sent in turn N-1. The cachePoint marks that boundary. Only the LAST message (fresh tool result) is uncached.

**Budget accounting**: With system (1) + tools (1) + messages (1) = 3 of 4 allowed checkpoints used.

**Minimum token threshold**: The conversation prefix must exceed 1024 tokens (Sonnet 4.6) for caching to engage. Early turns (1-2) won't cache; turn 3+ will. In practice, tool results are verbose enough that this threshold is hit quickly.

### 5. Cache Static File Attachments (Images/PDFs)

When users attach images or PDFs in their first message, those become part of the cached prefix on turn 2+:

```typescript
// Image and document content blocks go in the first user message.
// Since our message caching marks the second-to-last message,
// ALL prior messages (including attachments) get cached automatically.
messages: [
  { role: "user", content: [
    { image: { format: "png", source: { bytes: base64Data } } },
    { text: "Convert this chart into a slide" },
  ]},
  // ... subsequent tool turns are appended after this
]
```

Images can be 1000-5000+ tokens. Caching them means they're only processed once, not re-analyzed on every agent loop iteration.

### 6. Log Cache Metrics

In the stream event handler, capture the metadata event:

```typescript
for await (const event of response.stream) {
  // ... handle contentBlockStart, contentBlockDelta, contentBlockStop ...
  if (event.metadata?.usage) {
    const { inputTokens, outputTokens, cacheReadInputTokens, cacheWriteInputTokens } = event.metadata.usage;
    console.log(
      `Tokens — input: ${inputTokens}, output: ${outputTokens}` +
      (cacheReadInputTokens ? `, cache_read: ${cacheReadInputTokens}` : "") +
      (cacheWriteInputTokens ? `, cache_write: ${cacheWriteInputTokens}` : "")
    );
  }
}
```

### 7. Verify with Test Script

Create a test that makes 2+ requests and confirms `cacheReadInputTokens > 0` on the second:

```typescript
// Request 1 → expect cache_write (or cache_read if recently cached)
// Request 2 → expect cache_read
// Both should have the same number of cached tokens
```

## Key Gotchas

1. **TypeScript types** — The AWS SDK uses discriminated unions (`SystemContentBlock`, `Tool`, `ContentBlock`). The `cachePoint` variant exists but TS inference breaks with spread operators. Use `as unknown[]` on the arrays and `as ConverseStreamCommandInput` on the full input.

2. **Prefix must be IDENTICAL** — Any change to cached content (even whitespace) invalidates the cache. Ensure system prompts and tools are truly static (built once at startup, not per-request).

3. **Ordering matters** — Static content must come BEFORE dynamic content. The cache matches from the beginning of each section (system, tools, messages).

4. **Cache TTL** — Default is 5 minutes, resets on each hit. For infrequent requests, use `{ cachePoint: { type: "default", ttl: "1h" } }` (only on models that support it).

5. **Cross-Region Inference** — Using cross-region model IDs (`eu.anthropic.claude-*`) works fine with caching, but high-demand routing may cause occasional cache misses.

6. **Cost model** — Cache writes cost ~1.25x normal input rate. Cache reads cost ~0.1x. Break-even is at 2 requests using the same cache within TTL.

## Verification Checklist

- [ ] First request logs show `cache_write` OR `cache_read` (if cache already warm)
- [ ] Second request logs show `cache_read` with same token count
- [ ] `inputTokens` is small (only the dynamic/user message portion)
- [ ] Latency improvement visible on subsequent requests (~30-85% TTFT reduction)
