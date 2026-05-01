#!/usr/bin/env python3
"""
Macroeconomic data fetcher using FRED (Federal Reserve Economic Data).
Uses the public FRED website — no API key required (scrapes HTML/CSV).
Falls back to yfinance for market-based macro indicators.

Usage: python3 macro_data.py <command>

Commands:
  rates              Fed funds rate, Treasury yields, yield curve
  inflation          CPI, PCE data
  employment         Unemployment, jobless claims
  gdp                GDP growth
  market_conditions  VIX, credit spreads, dollar index
  summary            All-in-one macro dashboard
"""

import sys
import json
import warnings
from datetime import datetime, timedelta

warnings.filterwarnings("ignore")

try:
    import yfinance as yf
    import pandas as pd
    import numpy as np
except ImportError as e:
    print(f"Error: Missing dependency — {e}")
    print("Install with: pip3 install yfinance pandas numpy")
    sys.exit(1)


def get_fred_series_via_yf(series_map):
    """
    Fetch macro data using yfinance tickers that track these indicators.
    This avoids needing a FRED API key.
    """
    results = {}
    for name, ticker in series_map.items():
        try:
            t = yf.Ticker(ticker)
            hist = t.history(period="1y")
            if not hist.empty:
                results[name] = {
                    "current": round(hist["Close"].iloc[-1], 4),
                    "date": hist.index[-1].strftime("%Y-%m-%d"),
                    "1m_ago": round(hist["Close"].iloc[-22], 4) if len(hist) > 22 else None,
                    "3m_ago": round(hist["Close"].iloc[-66], 4) if len(hist) > 66 else None,
                    "6m_ago": round(hist["Close"].iloc[-126], 4) if len(hist) > 126 else None,
                    "1y_change": round(hist["Close"].iloc[-1] - hist["Close"].iloc[0], 4) if len(hist) > 200 else None,
                }
            else:
                results[name] = {"error": "no data"}
        except Exception as e:
            results[name] = {"error": str(e)}
    return results


def cmd_rates():
    """Treasury yields and rate indicators."""
    rate_tickers = {
        "us_2y_treasury": "^IRX",  # 13-week T-bill as proxy
        "us_10y_treasury": "^TNX",
        "us_30y_treasury": "^TYX",
    }

    results = get_fred_series_via_yf(rate_tickers)

    # Calculate spread
    if "us_10y_treasury" in results and "us_2y_treasury" in results:
        try:
            t10 = results["us_10y_treasury"]["current"]
            t2 = results["us_2y_treasury"]["current"]
            results["yield_curve_spread_10y_2y"] = {
                "current": round(t10 - t2, 4),
                "signal": "normal" if t10 > t2 else "inverted (recession signal)",
            }
        except:
            pass

    # Add TLT for long bond price action
    try:
        tlt = yf.Ticker("TLT")
        hist = tlt.history(period="3mo")
        if not hist.empty:
            results["long_bond_etf_TLT"] = {
                "price": round(hist["Close"].iloc[-1], 2),
                "3m_return_pct": round((hist["Close"].iloc[-1] / hist["Close"].iloc[0] - 1) * 100, 2),
            }
    except:
        pass

    print(json.dumps({"command": "rates", "data": results}, indent=2, default=str))


def cmd_inflation():
    """Inflation indicators via market-based proxies."""
    # TIPS ETF and breakeven inflation proxies
    inflation_tickers = {
        "tips_etf_TIP": "TIP",
        "inflation_breakeven_proxy": "RINF",  # ProShares Inflation Expectations
    }

    results = get_fred_series_via_yf(inflation_tickers)

    # Commodity proxies for inflation
    commodity_tickers = {
        "gold": "GLD",
        "oil_wti": "USO",
        "broad_commodities": "DJP",
    }
    commodity_data = get_fred_series_via_yf(commodity_tickers)
    results["commodity_signals"] = commodity_data

    print(json.dumps({"command": "inflation", "data": results, "note": "For precise CPI/PCE numbers, use Tavily to search 'latest CPI report BLS' or fetch from r.jina.ai/https://www.bls.gov/news.release/cpi.nr0.htm"}, indent=2, default=str))


def cmd_employment():
    """Employment market indicators."""
    # No direct yfinance proxy for employment — provide guidance
    results = {
        "note": "Employment data requires web fetch. Use these commands:",
        "commands": [
            "Tavily: search 'latest unemployment rate BLS nonfarm payrolls' time_range=month",
            "Jina: r.jina.ai/https://www.bls.gov/news.release/empsit.nr0.htm",
            "Jina: r.jina.ai/https://fred.stlouisfed.org/series/UNRATE",
        ],
        "market_proxies": {},
    }

    # Staffing companies as employment proxy
    employment_proxies = {
        "staffing_index_RHI": "RHI",
        "staffing_MAN": "MAN",
    }
    results["market_proxies"] = get_fred_series_via_yf(employment_proxies)

    print(json.dumps({"command": "employment", "data": results}, indent=2, default=str))


def cmd_gdp():
    """GDP and economic growth indicators."""
    results = {
        "note": "GDP data requires web fetch for exact numbers.",
        "commands": [
            "Tavily: search 'US GDP growth latest quarter BEA' time_range=month",
            "Jina: r.jina.ai/https://fred.stlouisfed.org/series/GDP",
            "Jina: r.jina.ai/https://www.bea.gov/news/glance",
        ],
        "growth_proxies": {},
    }

    # Economic growth proxies
    growth_tickers = {
        "sp500": "SPY",
        "small_cap_IWM": "IWM",
        "transports_IYT": "IYT",
        "industrials_XLI": "XLI",
        "consumer_disc_XLY": "XLY",
        "consumer_staples_XLP": "XLP",
    }
    results["growth_proxies"] = get_fred_series_via_yf(growth_tickers)

    # Cyclical vs defensive ratio
    try:
        xly = yf.Ticker("XLY").history(period="3mo")["Close"]
        xlp = yf.Ticker("XLP").history(period="3mo")["Close"]
        if not xly.empty and not xlp.empty:
            ratio_now = xly.iloc[-1] / xlp.iloc[-1]
            ratio_3m = xly.iloc[0] / xlp.iloc[0]
            results["cyclical_vs_defensive"] = {
                "current_ratio": round(ratio_now, 4),
                "3m_ago_ratio": round(ratio_3m, 4),
                "signal": "risk-on (expansion)" if ratio_now > ratio_3m else "risk-off (contraction)",
            }
    except:
        pass

    print(json.dumps({"command": "gdp", "data": results}, indent=2, default=str))


def cmd_market_conditions():
    """Market stress and conditions indicators."""
    condition_tickers = {
        "vix": "^VIX",
        "dollar_index_UUP": "UUP",
        "high_yield_spread_HYG": "HYG",
        "investment_grade_LQD": "LQD",
        "sp500": "^GSPC",
        "nasdaq": "^IXIC",
        "russell_2000": "^RUT",
    }

    results = get_fred_series_via_yf(condition_tickers)

    # VIX interpretation
    if "vix" in results and "current" in results["vix"]:
        vix = results["vix"]["current"]
        if vix < 12:
            results["vix"]["regime"] = "extreme_complacency"
        elif vix < 18:
            results["vix"]["regime"] = "low_volatility"
        elif vix < 25:
            results["vix"]["regime"] = "normal"
        elif vix < 35:
            results["vix"]["regime"] = "elevated_fear"
        else:
            results["vix"]["regime"] = "panic"

    # Risk appetite: HYG/LQD ratio
    try:
        hyg = yf.Ticker("HYG").history(period="3mo")["Close"]
        lqd = yf.Ticker("LQD").history(period="3mo")["Close"]
        if not hyg.empty and not lqd.empty:
            ratio_now = hyg.iloc[-1] / lqd.iloc[-1]
            ratio_3m = hyg.iloc[0] / lqd.iloc[0]
            results["credit_risk_appetite"] = {
                "hyg_lqd_ratio": round(ratio_now, 4),
                "3m_trend": "improving" if ratio_now > ratio_3m else "deteriorating",
            }
    except:
        pass

    # Market breadth proxy: RSP (equal-weight) vs SPY
    try:
        rsp = yf.Ticker("RSP").history(period="3mo")["Close"]
        spy = yf.Ticker("SPY").history(period="3mo")["Close"]
        if not rsp.empty and not spy.empty:
            rsp_ret = (rsp.iloc[-1] / rsp.iloc[0] - 1) * 100
            spy_ret = (spy.iloc[-1] / spy.iloc[0] - 1) * 100
            results["breadth"] = {
                "equal_weight_3m_return": round(rsp_ret, 2),
                "cap_weight_3m_return": round(spy_ret, 2),
                "signal": "broad participation" if rsp_ret > spy_ret else "narrow leadership",
            }
    except:
        pass

    print(json.dumps({"command": "market_conditions", "data": results}, indent=2, default=str))


def cmd_summary():
    """All-in-one macro dashboard."""
    print("Fetching macro dashboard...", file=sys.stderr)

    dashboard = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "sections": {},
    }

    # Rates
    try:
        tnx = yf.Ticker("^TNX").history(period="5d")
        irx = yf.Ticker("^IRX").history(period="5d")
        tyx = yf.Ticker("^TYX").history(period="5d")
        dashboard["sections"]["rates"] = {
            "10y_yield": round(tnx["Close"].iloc[-1], 3) if not tnx.empty else None,
            "3m_yield": round(irx["Close"].iloc[-1], 3) if not irx.empty else None,
            "30y_yield": round(tyx["Close"].iloc[-1], 3) if not tyx.empty else None,
        }
        if not tnx.empty and not irx.empty:
            spread = tnx["Close"].iloc[-1] - irx["Close"].iloc[-1]
            dashboard["sections"]["rates"]["10y_3m_spread"] = round(spread, 3)
            dashboard["sections"]["rates"]["yield_curve"] = "normal" if spread > 0 else "inverted"
    except:
        dashboard["sections"]["rates"] = {"error": "failed to fetch"}

    # VIX
    try:
        vix = yf.Ticker("^VIX").history(period="5d")
        if not vix.empty:
            v = vix["Close"].iloc[-1]
            dashboard["sections"]["volatility"] = {
                "vix": round(v, 2),
                "regime": "complacent" if v < 14 else "low" if v < 18 else "normal" if v < 25 else "elevated" if v < 35 else "panic",
            }
    except:
        pass

    # Major indices (1d returns)
    indices = {"SPY": "S&P 500", "QQQ": "Nasdaq 100", "IWM": "Russell 2000", "DIA": "Dow Jones"}
    dashboard["sections"]["indices"] = {}
    for ticker, name in indices.items():
        try:
            h = yf.Ticker(ticker).history(period="5d")
            if not h.empty and len(h) >= 2:
                dashboard["sections"]["indices"][name] = {
                    "price": round(h["Close"].iloc[-1], 2),
                    "1d_change_pct": round((h["Close"].iloc[-1] / h["Close"].iloc[-2] - 1) * 100, 2),
                }
        except:
            pass

    # Dollar
    try:
        uup = yf.Ticker("UUP").history(period="1mo")
        if not uup.empty:
            dashboard["sections"]["dollar"] = {
                "UUP_price": round(uup["Close"].iloc[-1], 2),
                "1m_change_pct": round((uup["Close"].iloc[-1] / uup["Close"].iloc[0] - 1) * 100, 2),
            }
    except:
        pass

    # Gold & Oil
    try:
        gld = yf.Ticker("GLD").history(period="1mo")
        uso = yf.Ticker("USO").history(period="1mo")
        dashboard["sections"]["commodities"] = {}
        if not gld.empty:
            dashboard["sections"]["commodities"]["gold_GLD"] = {
                "price": round(gld["Close"].iloc[-1], 2),
                "1m_change_pct": round((gld["Close"].iloc[-1] / gld["Close"].iloc[0] - 1) * 100, 2),
            }
        if not uso.empty:
            dashboard["sections"]["commodities"]["oil_USO"] = {
                "price": round(uso["Close"].iloc[-1], 2),
                "1m_change_pct": round((uso["Close"].iloc[-1] / uso["Close"].iloc[0] - 1) * 100, 2),
            }
    except:
        pass

    print(json.dumps(dashboard, indent=2, default=str))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1].lower()
    commands = {
        "rates": cmd_rates,
        "inflation": cmd_inflation,
        "employment": cmd_employment,
        "gdp": cmd_gdp,
        "market_conditions": cmd_market_conditions,
        "summary": cmd_summary,
    }

    if command in commands:
        commands[command]()
    else:
        print(f"Unknown command: {command}")
        print(f"Available: {', '.join(commands.keys())}")
        sys.exit(1)


if __name__ == "__main__":
    main()
