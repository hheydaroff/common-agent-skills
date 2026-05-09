# Daily Investment Scan Methodology

Automated daily research sweep across tracked themes. Reads configuration from `finance/watchlist.md` in the user's Obsidian vault.

## Overview

The scan mimics what a human analyst would do each morning:
1. Check trade publications for constraint language
2. Check for new government contracts (SAM.gov)
3. Check insider buying activity
4. Check for earnings surprises in tracked sectors
5. Check for hiring surges at tracked companies

## Input

Read `finance/watchlist.md` to get:
- **Themes** with constraint keywords, trade sources, and **region** (US/EU/Global)
- **Companies** being tracked with current status and exchange suffix
- **Scan configuration** (frequency, thresholds, output path)

**Region-aware scanning:**
- US themes: use SAM.gov, openinsider.com, SEC EDGAR, BLS
- EU themes: use TED (ted.europa.eu), Disclosyr.com, Investegate.co.uk, Bundesanzeiger
- Global themes: scan both US and EU sources

## Scan Direction: Upstream + Downstream

Every theme should be analyzed in BOTH directions:

```
UPSTREAM (what does the theme need?)     →     THE THEME     →     DOWNSTREAM (what does the theme enable?)
Supply chain bottlenecks                       [e.g., AI]           New industries unlocked
Who can't be routed around?                                         Who gains traction next?
Physical constraints (years to build)                               Adoption signals (pilots → production)
```

**For upstream:** Look for constraint language, supply shortages, sole-source suppliers
**For downstream:** Look for pilot-to-production transitions, first commercial deployments, customer adoption signals

When a theme lists `upstream_dependencies` in the watchlist, scan those specifically for bottleneck companies.

---

## Scan Steps

### Step 1: Constraint Language Search

For each active theme in watchlist.md:
1. Take the `constraint_keywords` list
2. Search using Tavily: each keyword phrase (time_range: week)
3. Look for these signal phrases in results:
   - "Lead times extended to..."
   - "Fully allocated through..."
   - "Price increases of X%..."
   - "Backlog reached record..."
   - "Delayed due to lack of..."
   - "Capacity expansion announced..."
4. Score: HIGH if signal found in multiple sources, MEDIUM if one source, LOW if nothing new

**For EU themes specifically:**
- Search European trade publications: Energy Monitor, Euractive, Janes Defence
- Include EU-specific constraint language: "delivery delays in Europe", "EU allocation", "European procurement backlog"

### Step 2: Contract Awards

**US — SAM.gov:**
For each theme's `sam_gov_keywords`:
1. Search via Tavily: `site:sam.gov "[keyword]" contract award` (time_range: week)
2. Alternative: Exa search for `"sam.gov" "[keyword]" awarded 2026`
3. Note: contract dollar amount, recipient company, timeline
4. Score: HIGH if >$50M contract to a tracked company, MEDIUM if relevant sector, LOW if nothing

**EU — TED (Tenders Electronic Daily):**
For each theme's `ted_keywords`:
1. Search via Tavily: `site:ted.europa.eu "[keyword]" contract notice` (time_range: week)
2. Alternative: Exa search for `"ted.europa.eu" "[keyword]" awarded 2026`
3. Also check: UK contracts via `contracts-finder.service.gov.uk`
4. Note: contract value (€), recipient, country, timeline
5. Score: HIGH if >€50M contract to a tracked company, MEDIUM if relevant sector

### Step 3: Insider Activity

**US:**
For tracked companies (Tier 1 and Tier 2):
1. Search via Tavily: `site:openinsider.com "[TICKER]"` (time_range: week)
2. Alternative: `"[company name]" insider buying Form 4` (time_range: week)
3. Flag: cluster buys (3+ insiders in same week = strong signal)
4. Score: HIGH if cluster buy at tracked company, MEDIUM if single insider buy, LOW if nothing

**EU:**
For tracked European companies:
1. Search via Tavily: `site:disclosyr.com "[COMPANY]"` (time_range: week)
2. UK: `site:investegate.co.uk "[COMPANY]" director` (time_range: week)
3. Germany: `"[COMPANY]" directors dealings BaFin` (time_range: week)
4. Sweden: `site:fi.se "[COMPANY]" insider` (time_range: week)
5. Flag: cluster buys from European executives carry same signal weight as US Form 4
6. Score: same thresholds as US

### Step 4: Earnings Surprises

Check if any tracked companies or theme-adjacent companies reported:
1. Tavily search: `"[TICKER] earnings beat"` (time_range: week) for each Tier 1/2 company
2. Broader: `"industrials OR utilities OR materials" earnings surprise` (time_range: week)
3. Flag: beat >10% + revenue growing after flat period = inflection signal
4. Score: HIGH if tracked company beats, MEDIUM if theme-adjacent company beats, LOW if nothing

### Step 5: Hiring Signals

For Tier 1 companies only (keep focused):
1. Tavily search: `"[company name]" hiring OR "job openings" engineer` (time_range: month)
2. Flag: hiring surges in specific technical roles (welders, electrical engineers, process engineers)
3. Score: HIGH if 50+ technical roles posted, MEDIUM if notable hiring, LOW if nothing

## Output Format

Write to `daily/invest-scan-YYYY-MM-DD.md`:

```markdown
---
type: daily-component
component: invest-scan
date: "YYYY-MM-DD"
created: "YYYY-MM-DDTHH:MM"
---

# Investment Scan — [Full Date]

## Signals Found

### 🔴 HIGH (requires attention)
- [Signal description with source link]
- Theme: [which theme]
- Company affected: [if applicable]
- Implication: [one sentence — what does this mean for the thesis?]

### 🟡 MEDIUM (worth noting)
- [Signal description]
- Theme: [which theme]

### ⚪ LOW / No Signal
- [Themes checked with no new findings]

## Theme Health Summary

| Theme | Region | Signal Strength | Trend vs Last Week | Notes |
|-------|--------|----------------|-------------------|-------|
| Electrical Equipment | US/EU | 🔴/🟡/⚪ | ↑/→/↓ | [one line] |
| Water Infrastructure | US | 🔴/🟡/⚪ | ↑/→/↓ | [one line] |
| Reshoring | US/EU | 🔴/🟡/⚪ | ↑/→/↓ | [one line] |
| Defense | US/EU | 🔴/🟡/⚪ | ↑/→/↓ | [one line] |
| EU Defense (Zeitenwende) | EU | 🔴/🟡/⚪ | ↑/→/↓ | [one line] |
| EU Grid Infrastructure | EU | 🔴/🟡/⚪ | ↑/→/↓ | [one line] |
| EU Energy Transition | EU | 🔴/🟡/⚪ | ↑/→/↓ | [one line] |
| Silver Tsunami | US/EU | 🔴/🟡/⚪ | ↑/→/↓ | [one line] |
| Copper | Global | 🔴/🟡/⚪ | ↑/→/↓ | [one line] |

## Watchlist Price Check

| Ticker | Price | Δ 1w | Δ 1m | Signal |
|--------|-------|------|------|--------|
[For each Tier 1 company, pull current price via market_data.py]

## New Opportunities Spotted

[Any company or theme that emerged from the scan that ISN'T already on the watchlist]
- Company: [name]
- Why it appeared: [which search surfaced it]
- Theme alignment: [does it fit an existing theme or is it a new one?]
- Action: Add to watchlist? Research further?

---
*Scan completed: [timestamp]*
```

## Integration with Daily Brief

When called as part of `/daily-brief`:
- Run the full scan
- Return a 3-5 line summary for the brief:
  - Number of HIGH/MEDIUM signals
  - Which themes showed activity
  - Any alert-worthy findings
- Full details saved to `daily/invest-scan-YYYY-MM-DD.md`

## Weekly Roll-Up (Friday)

On Fridays, additionally:
1. Read all `daily/invest-scan-*.md` from the current week
2. Synthesize: which themes showed repeated signals?
3. Flag: any company appearing in multiple signal types = convergence
4. Suggest: "Based on this week's signals, [TICKER] warrants deeper research (Level 2)"
