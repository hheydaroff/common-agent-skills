# Bear Case Research Methodology

The most important step before any investment. Systematically identify what kills the thesis, research how probable each scenario is, then define measurable exit triggers.

**Core principle:** Your job is to DISPROVE the thesis. If you can't after genuine effort, it might be real.

## The 4 Bear Case Categories

Every stock has exactly 4 ways it can fail:

| Category | Core Question |
|----------|--------------|
| **Demand risk** | "What if the demand I'm betting on never materializes?" |
| **Competition risk** | "What if someone else captures this demand instead?" |
| **Execution risk** | "What if the company itself fails to deliver?" |
| **Valuation risk** | "What if the thesis is right but I overpay?" |

## Research Process

### Demand Risk

**What you're verifying:** Is the demand driver real, growing, and irreversible?

| Source | What to look for | How to access |
|--------|-----------------|---------------|
| Industry trade publications | Are customers ordering? | Google: `"[product] orders 2026"` or `"[product] backlog"` |
| Company earnings calls | "Fully booked" vs "softening demand" | seekingalpha.com (free for recent transcripts) |
| Customer company earnings | Are BUYERS confirming spend? | Listen to the customer's earnings call |
| Government data | Is regulation/funding flowing? | DOE, EPA, FERC announcements |

**Search queries:**
- Tavily: `"[product/sector] demand outlook 2026 2027"` (time_range: month)
- Tavily: `"[product/sector] slowdown OR decline OR canceled"` (time_range: 3months)

### Competition Risk

**What you're verifying:** Can someone else serve this demand instead?

| Source | What to look for | How to access |
|--------|-----------------|---------------|
| Import/export data | Foreign competitors shipping product? | US International Trade Commission (usitc.gov) |
| Competitor earnings | Are competitors entering this space? | Their earnings calls |
| Patent filings | Alternative technology developing? | Google Patents |
| Tariff/trade policy | Protection or exposure? | Trade.gov, executive orders |

**Search queries:**
- Exa: `"[company] competitors market share"` (category: financial report)
- Tavily: `"[product] imports OR alternative OR substitute 2026"`

**Quick test:** How many companies can serve this demand?
- 1-2 = oligopoly = safe (high pricing power)
- 3-5 = competitive but manageable
- 10+ = commoditized = high risk

### Execution Risk

**What you're verifying:** Can THIS company deliver without going bankrupt?

| Check | Tool/Source | Red flag threshold |
|-------|-------------|-------------------|
| Debt/Equity ratio | `market_data.py financials <TICKER>` | > 100% = high risk |
| Operating cash flow | Same | Negative 2+ quarters = dangerous |
| Short interest | `market_data.py price <TICKER>` (short_pct_float) | > 15% = bears active |
| Insider activity | openinsider.com | Heavy selling = warning |
| Credit rating | Google: `"[company] credit rating"` | Downgrade = serious |
| Risk factors | SEC 10-K filing, "Risk Factors" section | Company must legally disclose |

**Search queries:**
- Tavily: `"[company] credit rating OR downgrade OR debt"` (time_range: 6months)

### Valuation Risk

**What you're verifying:** Even if right, am I paying too much?

| Check | What it tells you |
|-------|------------------|
| PEG ratio | < 1 = potentially cheap, > 2 = expensive for growth |
| 52-week position | Near highs after big run = less upside remaining |
| Analyst targets vs price | target_mean < current = analysts think it's overvalued |
| Historical P/E | Current vs 5-year average (macrotrends.net) |
| Stock move from lows | Up > 200% = likely late |

## Probability Estimation

You don't need precision. Use this guide:

| Evidence Pattern | Probability |
|-----------------|-------------|
| 3+ independent sources confirm the risk is LOW | < 20% this goes wrong |
| Mixed signals, some positive some negative | ~40% |
| Only the company itself denies the risk | ~50% |
| Independent sources suggest the risk is REAL | > 60% |

**Specific heuristics:**
- Competition: 0-1 competitors + physical barriers to entry → threat < 20%
- Competition: 3+ competitors OR easy switching → threat > 60%
- Execution: Debt/Equity > 100% AND negative cash flow → risk > 50%
- Execution: Net cash + positive FCF → risk < 20%
- Valuation: Stock up > 200% AND P/E > 40x → overvaluation risk > 50%

## Synthesis: The Decision Table

```
| Category | Bear Case | Probability | Impact if True | Evidence Source |
|----------|-----------|-------------|---------------|----------------|
| Demand | [specific scenario] | __% | Stock → $__ | [what you read] |
| Competition | [specific scenario] | __% | Stock → $__ | [what you read] |
| Execution | [specific scenario] | __% | Stock → $__ | [what you read] |
| Valuation | [specific scenario] | __% | Flat / -__% | [what you read] |
```

**Decision rule:**
- Total risk > 60% → PASS (too many ways to lose)
- Total risk 30-60% → SMALL position (2% max) with tight exit triggers
- Total risk < 30% → Standard position (3-5%) with quarterly monitoring

## Exit Triggers

For each bear case, define ONE specific, measurable signal:

```
I SELL if:
1. [Demand] — Revenue declines 2 consecutive quarters after "inflection"
2. [Competition] — [Specific competitor] gains >X% market share (check quarterly)
3. [Execution] — Credit downgrade, or cash flow negative 3+ consecutive quarters
4. [Valuation] — P/E exceeds [X] without corresponding earnings acceleration
```

## Weekly Monitoring (5 min per position)

- **Quarterly:** Re-read earnings call transcript, check for bear case keywords
- **Monthly:** One industry source check for demand/competition signals
- **Immediately if triggered:** Execute the exit. The trigger was defined rationally before entry — don't override it emotionally.
