# Earnings Play (`/invest earnings <TICKER>`)

## Script Sequence

1. `market_data.py price <TICKER>` — current IV and price
2. `market_data.py options <TICKER>` — nearest expiry chain
3. Exa search: `"<TICKER> earnings estimate Q[X] 2025"` (category: financial report)
4. Tavily search: `"<TICKER> earnings whisper expectations"` (time_range: week)

## Output

Expected move (from options), historical beat rate, IV percentile, recommended earnings trade (if any), or stay-away signal.
