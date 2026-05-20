# Peer Quartile Benchmarking

Systematic peer comparison using quartile analysis to position a stock relative to its competitive set.

## When to Use

- During `/invest deep <TICKER>` — add a peer positioning table
- When user asks "is this expensive/cheap vs peers?"
- For sector comparisons in `/invest sector`

## Core Concept

Use **quartile distribution** to show where a stock sits vs peers:
- **Above 75th percentile**: Premium — needs justification (faster growth, better margins, moat)
- **50th-75th**: Above average — reasonably valued if fundamentals support it
- **25th-50th**: Below average — potential opportunity if quality is there
- **Below 25th percentile**: Discount — either deep value or there's a reason

## Peer Selection Rules

1. **Same business model** — don't mix SaaS with on-premise
2. **Similar scale** (within 0.3x-3x revenue)
3. **Same geography exposure**
4. **5-8 peers ideal** — fewer than 5 is unreliable, more than 10 is noise
5. **Exclude restructuring outliers** — note and remove

## Data Collection

```bash
uv run --with yfinance --with pandas --with numpy python3 scripts/market_data.py compare <TICKER>,<PEER1>,<PEER2>,<PEER3>,...
uv run --with yfinance --with pandas --with numpy python3 scripts/market_data.py price <TICKER>
uv run --with yfinance --with pandas --with numpy python3 scripts/market_data.py financials <TICKER>
```

## Metrics to Benchmark

**Operating (always):** Revenue Growth YoY, Gross Margin, EBITDA Margin, FCF Margin
**Valuation (always):** Forward P/E, EV/EBITDA, EV/Revenue, PEG Ratio

**Sector-specific additions:**
- Tech/SaaS: Net retention, Rule of 40, R&D/Revenue
- Financials: ROE, NIM, Efficiency Ratio
- Industrials: Asset Turnover, Backlog/Revenue, CapEx Intensity
- Consumer: Same-store sales, Inventory Turnover

## Output Format

```markdown
## Peer Positioning: <TICKER> vs Comparable Set
**Peers**: [PEER1], [PEER2], [PEER3], [PEER4], [PEER5]

### Operating Metrics
| Metric | <TICKER> | 25th | Median | 75th | Percentile | Signal |
|--------|----------|------|--------|------|-----------|--------|
| Rev Growth | 18% | 10% | 14% | 20% | 65th | Above avg |
| Gross Margin | 72% | 58% | 65% | 71% | 78th | Premium |
| EBITDA Margin | 25% | 15% | 22% | 28% | 60th | Avg |

### Valuation Metrics
| Metric | <TICKER> | 25th | Median | 75th | Percentile | Signal |
|--------|----------|------|--------|------|-----------|--------|
| Fwd P/E | 28x | 20x | 25x | 32x | 55th | Fair |
| EV/EBITDA | 18x | 12x | 16x | 20x | 60th | Slight prem |
| PEG | 1.4x | 1.1x | 1.5x | 2.0x | 45th | Attractive |

### Quality-Valuation Verdict
- **Quality**: [Top / Above Avg / Average / Below Avg] quartile
- **Valuation**: [Premium / Fair / Discount] vs peers
- **Verdict**: [Justified premium / Overvalued / Undervalued / Fair]
```

## The Quality-Valuation Matrix

| | Cheap (<25th val) | Fair (25-75th) | Expensive (>75th val) |
|---|---|---|---|
| **High Quality (>75th ops)** | 🟢 Strong Buy | 🟢 Buy | 🟡 Hold (justified) |
| **Average Quality (25-75th)** | 🟢 Buy (value) | 🟡 Neutral | 🔴 Expensive |
| **Low Quality (<25th ops)** | 🟡 Value trap? | 🔴 Avoid | 🔴 Strong Avoid |

## Statistical Notes

- Use **median** not mean — avoids outlier distortion
- Exclude negative-earnings companies from P/E and PEG quartiles
- Note dispersion (75th - 25th): tight = sector trades uniformly; wide = differentiation matters
