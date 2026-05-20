# Reddit Sentiment (`/invest reddit` or `/invest reddit <TICKER>`)

Gauge retail investor sentiment from Reddit — used as a contrarian signal (extreme consensus often marks inflection points) and for early detection of emerging narratives. No dedicated script; uses Tavily/Exa with `include_domains: ["reddit.com"]`.

## Full Scan (during daily scan or `/invest reddit`)

1. Tavily search: `"stock market what are you buying this week"` with `include_domains: ["reddit.com"]`, `time_range: "week"`
2. Exa search: `"investing opportunity <theme keywords>"` with `includeDomains: ["reddit.com"]`, `startPublishedDate: <7d ago>`
3. Review returned titles + content snippets for narrative direction

## Ticker-Specific (`/invest reddit <TICKER>`)

1. Tavily search: `"<TICKER> stock analysis bullish bearish"` with `include_domains: ["reddit.com"]`, `time_range: "week"`
2. If few results: broaden to `time_range: "month"` or use company name instead of ticker
3. Exa search (semantic): `"<company name> investment thesis"` with `includeDomains: ["reddit.com"]`
4. Assess: is Reddit ahead of Wall Street, or chasing a move?

## How to Interpret Reddit Signals

| Signal | Meaning | Action |
|--------|---------|--------|
| Sudden spike in mentions + bullish sentiment | Retail FOMO, possible late-stage momentum | If already long: consider trimming. If not: probably too late. |
| High engagement + mixed sentiment (heated debate) | Controversial thesis, high uncertainty | Worth researching — one side will be wrong |
| Consistent mentions + bearish "it's dead" sentiment | Possible contrarian buy signal | Check fundamentals — if thesis intact, could be capitulation |
| Ticker in r/SecurityAnalysis or r/ValueInvesting | Higher-quality discussion, longer time horizon | Prioritize reading these threads |
| Ticker ONLY in r/wallstreetbets | Momentum/meme play, short time horizon | Not suitable for thesis-based investing unless fundamentals support it |

## Integration with Other Workflows

- Use before `/invest deep <TICKER>` to understand retail positioning
- Use in `/invest bear <TICKER>` to check if crowd is ignoring risks
- Use in `/invest scan` daily to detect narrative shifts early
