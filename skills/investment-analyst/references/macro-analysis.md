# Sector & Macro Analysis (`/invest macro` or `/invest sector <SECTOR>`)

## US Macro

1. `macro_data.py summary` — US macro dashboard
2. `alpaca_data.py screener active` — most active US stocks today
3. `alpaca_data.py multisnapshot XLK,XLF,XLE,XLV,XLI,XLP,XLU,XLY,XLC,XLRE,XLB` — US sector ETF prices
4. `market_data.py compare` — sector ETFs valuation
5. Tavily search: `"sector rotation market cycle 2025"` (time_range: week)

## European Macro (`/invest eu macro` or `/invest eu sector`)

1. `macro_data.py eu_summary` — European macro dashboard
2. `market_data.py screener eu_sector_etfs` — STOXX 600 sector ETFs
3. `market_data.py screener eu_mega` — top European stocks
4. `macro_data.py eu_conditions` — full European conditions incl. FX
5. Tavily search: `"ECB policy European sector rotation 2025"` (time_range: week)

## Output

Market cycle phase, sector rankings, rotation signals, risk regime. For European analysis, include ECB policy impact and EUR/USD dynamics.
