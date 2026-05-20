# Catalyst Calendar

Forward-looking event calendar for watchlist. Prioritize attention and position ahead of market-moving events.

## When to Use

- `/invest calendar` — build or update the calendar
- "What's coming up this week/month?"
- During weekly ritual to plan ahead

## File Location

Store in user's vault: `finance/catalyst-calendar.md`

## Event Categories

**Earnings & Financial:** Quarterly earnings, investor days, capital markets days, dividend ex-dates
**Corporate:** Product launches, regulatory decisions, M&A milestones, management transitions, lockup expirations
**Industry:** Conferences, trade shows, regulatory rulings, industry data releases, competitor earnings
**Macro:** FOMC (8/yr), Jobs (1st Fri), CPI (mid-month), GDP (quarterly), ECB decisions

## Building the Calendar

```bash
# Get earnings dates for watchlist tickers
uv run --with yfinance --with pandas --with numpy python3 scripts/market_data.py price <TICKER>
# earningsDate field in output

# Macro dates — use Tavily search
# "FOMC meeting dates 2026", "economic calendar this week"
```

## Output Format

```markdown
# Catalyst Calendar
**Last Updated**: YYYY-MM-DD

## This Week
| Date | Event | Ticker/Sector | Impact | Action |
|------|-------|---------------|--------|--------|
| Mon | ACME Q1 earnings | ACME | HIGH | Hold; catalyst checklist ready |
| Tue | FOMC minutes | Macro | MED | Watch rate path language |
| Fri | OPEX | Options | MED | Roll expiring positions |

## Next 30 Days
| Date | Event | Ticker | Impact | Notes |
|------|-------|--------|--------|-------|
| Jun 5 | Jobs report | Macro | HIGH | Last data before FOMC |
| Jun 14 | ABC earnings | ABC | HIGH | Key thesis test |
| Jun 18 | FOMC decision | Macro | HIGH | Dot plot update |
```

## Impact Scoring

| Level | Criteria | Action |
|-------|----------|--------|
| **HIGH** | Tests a thesis pillar; binary outcome; >5% move likely | Build catalyst checklist; consider hedging |
| **MEDIUM** | Data point but not thesis-killing; 2-5% move | Monitor; adjust if surprise |
| **LOW** | Routine; unlikely to move positions | Note but no action |

## Weekly Preview (generate every Monday)

```markdown
## Weekly Preview — Week of YYYY-MM-DD

### Must-Watch (HIGH)
1. [Day]: [Event] — positioning: [Long/Flat], action: [Hold/Trim/Hedge]
2. [Day]: [Event] — portfolio impact if surprise: [details]

### Secondary (MEDIUM)
- [Day]: [Event] — watching for [signal]

### Position Implications
- **Hedge before**: [positions with binary risk]
- **No change**: [positions with no events]
```

## Maintenance

- Update weekly during ritual
- Update immediately when new position opened or earnings date changes
- Archive past events with actual outcome (builds pattern recognition)
