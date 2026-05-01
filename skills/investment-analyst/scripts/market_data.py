#!/usr/bin/env python3
"""
Market data fetcher using yfinance. No API keys required.
Usage: python3 market_data.py <command> <args>

Commands:
  price <TICKER>                    Current price + key stats
  history <TICKER> [period]         OHLCV history (default: 6mo)
  financials <TICKER>               Income, balance sheet, cash flow
  options <TICKER> [expiry]         Options chain
  holders <TICKER>                  Institutional holders
  recommendations <TICKER>          Analyst recs & price targets
  dividends <TICKER>                Dividend history
  compare <TICKER,TICKER,...>       Side-by-side comparison
  technicals <TICKER> [period]      Technical indicators
  screener <name>                   Predefined stock screeners
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


def fmt_num(n, prefix="", suffix="", decimals=2):
    """Format numbers for display."""
    if n is None or (isinstance(n, float) and np.isnan(n)):
        return "N/A"
    if abs(n) >= 1e12:
        return f"{prefix}{n/1e12:.{decimals}f}T{suffix}"
    if abs(n) >= 1e9:
        return f"{prefix}{n/1e9:.{decimals}f}B{suffix}"
    if abs(n) >= 1e6:
        return f"{prefix}{n/1e6:.{decimals}f}M{suffix}"
    return f"{prefix}{n:.{decimals}f}{suffix}"


def safe_get(info, key, default=None):
    """Safely get a value from dict."""
    val = info.get(key, default)
    if val is None:
        return default
    return val


def cmd_price(ticker):
    """Get current price and key statistics."""
    t = yf.Ticker(ticker)
    info = t.info

    data = {
        "ticker": ticker.upper(),
        "name": safe_get(info, "longName", ticker),
        "sector": safe_get(info, "sector", "N/A"),
        "industry": safe_get(info, "industry", "N/A"),
        "price": {
            "current": safe_get(info, "currentPrice") or safe_get(info, "regularMarketPrice"),
            "previous_close": safe_get(info, "previousClose"),
            "open": safe_get(info, "open") or safe_get(info, "regularMarketOpen"),
            "day_high": safe_get(info, "dayHigh") or safe_get(info, "regularMarketDayHigh"),
            "day_low": safe_get(info, "dayLow") or safe_get(info, "regularMarketDayLow"),
            "52w_high": safe_get(info, "fiftyTwoWeekHigh"),
            "52w_low": safe_get(info, "fiftyTwoWeekLow"),
            "50d_avg": safe_get(info, "fiftyDayAverage"),
            "200d_avg": safe_get(info, "twoHundredDayAverage"),
        },
        "valuation": {
            "market_cap": safe_get(info, "marketCap"),
            "pe_trailing": safe_get(info, "trailingPE"),
            "pe_forward": safe_get(info, "forwardPE"),
            "peg_ratio": safe_get(info, "pegRatio"),
            "price_to_book": safe_get(info, "priceToBook"),
            "price_to_sales": safe_get(info, "priceToSalesTrailing12Months"),
            "ev_to_ebitda": safe_get(info, "enterpriseToEbitda"),
            "ev_to_revenue": safe_get(info, "enterpriseToRevenue"),
        },
        "fundamentals": {
            "revenue_ttm": safe_get(info, "totalRevenue"),
            "net_income_ttm": safe_get(info, "netIncomeToCommon"),
            "ebitda": safe_get(info, "ebitda"),
            "free_cash_flow": safe_get(info, "freeCashflow"),
            "operating_cash_flow": safe_get(info, "operatingCashflow"),
            "total_debt": safe_get(info, "totalDebt"),
            "total_cash": safe_get(info, "totalCash"),
            "debt_to_equity": safe_get(info, "debtToEquity"),
            "profit_margin": safe_get(info, "profitMargins"),
            "operating_margin": safe_get(info, "operatingMargins"),
            "roe": safe_get(info, "returnOnEquity"),
            "roa": safe_get(info, "returnOnAssets"),
        },
        "dividends": {
            "dividend_yield": safe_get(info, "dividendYield"),
            "dividend_rate": safe_get(info, "dividendRate"),
            "payout_ratio": safe_get(info, "payoutRatio"),
            "ex_date": safe_get(info, "exDividendDate"),
        },
        "growth": {
            "revenue_growth": safe_get(info, "revenueGrowth"),
            "earnings_growth": safe_get(info, "earningsGrowth"),
            "earnings_quarterly_growth": safe_get(info, "earningsQuarterlyGrowth"),
        },
        "analyst": {
            "target_high": safe_get(info, "targetHighPrice"),
            "target_low": safe_get(info, "targetLowPrice"),
            "target_mean": safe_get(info, "targetMeanPrice"),
            "target_median": safe_get(info, "targetMedianPrice"),
            "recommendation": safe_get(info, "recommendationKey"),
            "num_analysts": safe_get(info, "numberOfAnalystOpinions"),
        },
        "trading": {
            "volume": safe_get(info, "volume") or safe_get(info, "regularMarketVolume"),
            "avg_volume": safe_get(info, "averageVolume"),
            "avg_volume_10d": safe_get(info, "averageDailyVolume10Day"),
            "beta": safe_get(info, "beta"),
            "short_ratio": safe_get(info, "shortRatio"),
            "short_pct_float": safe_get(info, "shortPercentOfFloat"),
        },
    }
    print(json.dumps(data, indent=2, default=str))


def cmd_history(ticker, period="6mo"):
    """Get OHLCV price history."""
    t = yf.Ticker(ticker)
    hist = t.history(period=period)

    if hist.empty:
        print(json.dumps({"error": f"No history data for {ticker}"}))
        return

    # Convert to records
    records = []
    for date, row in hist.iterrows():
        records.append({
            "date": date.strftime("%Y-%m-%d"),
            "open": round(row["Open"], 2),
            "high": round(row["High"], 2),
            "low": round(row["Low"], 2),
            "close": round(row["Close"], 2),
            "volume": int(row["Volume"]),
        })

    # Summary stats
    closes = hist["Close"]
    summary = {
        "ticker": ticker.upper(),
        "period": period,
        "data_points": len(records),
        "start_date": records[0]["date"],
        "end_date": records[-1]["date"],
        "start_price": records[0]["close"],
        "end_price": records[-1]["close"],
        "return_pct": round((closes.iloc[-1] / closes.iloc[0] - 1) * 100, 2),
        "high": round(closes.max(), 2),
        "low": round(closes.min(), 2),
        "avg_volume": int(hist["Volume"].mean()),
        "volatility_annualized": round(closes.pct_change().std() * (252 ** 0.5) * 100, 2),
    }

    # Only print last 20 records + summary to keep output manageable
    output = {
        "summary": summary,
        "recent_data": records[-20:],
    }
    print(json.dumps(output, indent=2, default=str))


def cmd_financials(ticker):
    """Get financial statements."""
    t = yf.Ticker(ticker)

    result = {"ticker": ticker.upper(), "statements": {}}

    # Income statement
    inc = t.income_stmt
    if inc is not None and not inc.empty:
        result["statements"]["income_statement"] = {}
        for col in inc.columns[:4]:  # Last 4 periods
            period = col.strftime("%Y-%m-%d") if hasattr(col, "strftime") else str(col)
            result["statements"]["income_statement"][period] = {
                k: float(v) if pd.notna(v) else None
                for k, v in inc[col].items()
            }

    # Balance sheet
    bs = t.balance_sheet
    if bs is not None and not bs.empty:
        result["statements"]["balance_sheet"] = {}
        for col in bs.columns[:4]:
            period = col.strftime("%Y-%m-%d") if hasattr(col, "strftime") else str(col)
            result["statements"]["balance_sheet"][period] = {
                k: float(v) if pd.notna(v) else None
                for k, v in bs[col].items()
            }

    # Cash flow
    cf = t.cashflow
    if cf is not None and not cf.empty:
        result["statements"]["cash_flow"] = {}
        for col in cf.columns[:4]:
            period = col.strftime("%Y-%m-%d") if hasattr(col, "strftime") else str(col)
            result["statements"]["cash_flow"][period] = {
                k: float(v) if pd.notna(v) else None
                for k, v in cf[col].items()
            }

    print(json.dumps(result, indent=2, default=str))


def cmd_options(ticker, expiry=None):
    """Get options chain."""
    t = yf.Ticker(ticker)

    expirations = t.options
    if not expirations:
        print(json.dumps({"error": f"No options data for {ticker}"}))
        return

    if expiry is None:
        # Show nearest 3 expirations
        expiry_list = list(expirations[:3])
    else:
        expiry_list = [expiry]

    result = {
        "ticker": ticker.upper(),
        "all_expirations": list(expirations),
        "chains": {},
    }

    for exp in expiry_list:
        try:
            chain = t.option_chain(exp)
            calls = chain.calls[["strike", "lastPrice", "bid", "ask", "volume", "openInterest", "impliedVolatility", "inTheMoney"]].head(15)
            puts = chain.puts[["strike", "lastPrice", "bid", "ask", "volume", "openInterest", "impliedVolatility", "inTheMoney"]].head(15)

            result["chains"][exp] = {
                "calls": calls.to_dict(orient="records"),
                "puts": puts.to_dict(orient="records"),
            }
        except Exception as e:
            result["chains"][exp] = {"error": str(e)}

    print(json.dumps(result, indent=2, default=str))


def cmd_holders(ticker):
    """Get institutional holders."""
    t = yf.Ticker(ticker)
    result = {"ticker": ticker.upper()}

    try:
        inst = t.institutional_holders
        if inst is not None and not inst.empty:
            result["institutional_holders"] = inst.head(15).to_dict(orient="records")
    except:
        result["institutional_holders"] = []

    try:
        mf = t.mutualfund_holders
        if mf is not None and not mf.empty:
            result["mutual_fund_holders"] = mf.head(10).to_dict(orient="records")
    except:
        result["mutual_fund_holders"] = []

    print(json.dumps(result, indent=2, default=str))


def cmd_recommendations(ticker):
    """Get analyst recommendations and price targets."""
    t = yf.Ticker(ticker)
    info = t.info
    result = {
        "ticker": ticker.upper(),
        "consensus": {
            "recommendation": safe_get(info, "recommendationKey"),
            "target_high": safe_get(info, "targetHighPrice"),
            "target_low": safe_get(info, "targetLowPrice"),
            "target_mean": safe_get(info, "targetMeanPrice"),
            "target_median": safe_get(info, "targetMedianPrice"),
            "num_analysts": safe_get(info, "numberOfAnalystOpinions"),
        },
    }

    try:
        recs = t.recommendations
        if recs is not None and not recs.empty:
            recent = recs.tail(20)
            result["recent_recommendations"] = recent.reset_index().to_dict(orient="records")
    except:
        result["recent_recommendations"] = []

    try:
        upgrades = t.upgrades_downgrades
        if upgrades is not None and not upgrades.empty:
            result["upgrades_downgrades"] = upgrades.head(10).reset_index().to_dict(orient="records")
    except:
        result["upgrades_downgrades"] = []

    print(json.dumps(result, indent=2, default=str))


def cmd_dividends(ticker):
    """Get dividend history."""
    t = yf.Ticker(ticker)
    info = t.info

    result = {
        "ticker": ticker.upper(),
        "current": {
            "dividend_yield": safe_get(info, "dividendYield"),
            "dividend_rate": safe_get(info, "dividendRate"),
            "payout_ratio": safe_get(info, "payoutRatio"),
            "ex_date": safe_get(info, "exDividendDate"),
        },
    }

    divs = t.dividends
    if divs is not None and not divs.empty:
        records = [{"date": d.strftime("%Y-%m-%d"), "amount": round(v, 4)} for d, v in divs.tail(20).items()]
        result["history"] = records
        result["total_annual"] = round(divs.last("1Y").sum(), 4) if len(divs) > 0 else None

    print(json.dumps(result, indent=2, default=str))


def cmd_compare(tickers_str):
    """Compare multiple tickers side by side."""
    tickers = [t.strip().upper() for t in tickers_str.split(",")]
    result = {"tickers": tickers, "comparison": []}

    for ticker in tickers:
        try:
            t = yf.Ticker(ticker)
            info = t.info
            result["comparison"].append({
                "ticker": ticker,
                "name": safe_get(info, "longName", ticker),
                "price": safe_get(info, "currentPrice") or safe_get(info, "regularMarketPrice"),
                "market_cap": safe_get(info, "marketCap"),
                "pe_trailing": safe_get(info, "trailingPE"),
                "pe_forward": safe_get(info, "forwardPE"),
                "peg": safe_get(info, "pegRatio"),
                "ps_ratio": safe_get(info, "priceToSalesTrailing12Months"),
                "pb_ratio": safe_get(info, "priceToBook"),
                "ev_ebitda": safe_get(info, "enterpriseToEbitda"),
                "profit_margin": safe_get(info, "profitMargins"),
                "operating_margin": safe_get(info, "operatingMargins"),
                "roe": safe_get(info, "returnOnEquity"),
                "revenue_growth": safe_get(info, "revenueGrowth"),
                "earnings_growth": safe_get(info, "earningsGrowth"),
                "debt_to_equity": safe_get(info, "debtToEquity"),
                "free_cash_flow": safe_get(info, "freeCashflow"),
                "dividend_yield": safe_get(info, "dividendYield"),
                "beta": safe_get(info, "beta"),
                "52w_change": safe_get(info, "52WeekChange"),
            })
        except Exception as e:
            result["comparison"].append({"ticker": ticker, "error": str(e)})

    print(json.dumps(result, indent=2, default=str))


def cmd_technicals(ticker, period="6mo"):
    """Calculate technical indicators from price data."""
    t = yf.Ticker(ticker)
    hist = t.history(period=period)

    if hist.empty:
        print(json.dumps({"error": f"No data for {ticker}"}))
        return

    close = hist["Close"]
    high = hist["High"]
    low = hist["Low"]
    volume = hist["Volume"]

    # Moving averages
    ma_20 = close.rolling(20).mean()
    ma_50 = close.rolling(50).mean()
    ma_200 = close.rolling(200).mean()

    # RSI (14-period)
    delta = close.diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    # MACD
    ema_12 = close.ewm(span=12).mean()
    ema_26 = close.ewm(span=26).mean()
    macd_line = ema_12 - ema_26
    signal_line = macd_line.ewm(span=9).mean()
    macd_histogram = macd_line - signal_line

    # Bollinger Bands
    bb_mid = ma_20
    bb_std = close.rolling(20).std()
    bb_upper = bb_mid + 2 * bb_std
    bb_lower = bb_mid - 2 * bb_std

    # ATR (14-period)
    tr = pd.DataFrame({
        "hl": high - low,
        "hc": abs(high - close.shift(1)),
        "lc": abs(low - close.shift(1))
    }).max(axis=1)
    atr = tr.rolling(14).mean()

    # Volume analysis
    vol_avg_20 = volume.rolling(20).mean()
    vol_ratio = volume / vol_avg_20

    current_price = close.iloc[-1]

    result = {
        "ticker": ticker.upper(),
        "period": period,
        "current_price": round(current_price, 2),
        "date": hist.index[-1].strftime("%Y-%m-%d"),
        "trend": {
            "above_20ma": bool(current_price > ma_20.iloc[-1]) if pd.notna(ma_20.iloc[-1]) else None,
            "above_50ma": bool(current_price > ma_50.iloc[-1]) if pd.notna(ma_50.iloc[-1]) else None,
            "above_200ma": bool(current_price > ma_200.iloc[-1]) if pd.notna(ma_200.iloc[-1]) else None,
            "ma_20": round(ma_20.iloc[-1], 2) if pd.notna(ma_20.iloc[-1]) else None,
            "ma_50": round(ma_50.iloc[-1], 2) if pd.notna(ma_50.iloc[-1]) else None,
            "ma_200": round(ma_200.iloc[-1], 2) if pd.notna(ma_200.iloc[-1]) else None,
            "golden_cross": bool(ma_50.iloc[-1] > ma_200.iloc[-1]) if (pd.notna(ma_50.iloc[-1]) and pd.notna(ma_200.iloc[-1])) else None,
        },
        "momentum": {
            "rsi_14": round(rsi.iloc[-1], 2) if pd.notna(rsi.iloc[-1]) else None,
            "rsi_signal": "overbought" if (pd.notna(rsi.iloc[-1]) and rsi.iloc[-1] > 70) else ("oversold" if (pd.notna(rsi.iloc[-1]) and rsi.iloc[-1] < 30) else "neutral"),
            "macd_line": round(macd_line.iloc[-1], 4) if pd.notna(macd_line.iloc[-1]) else None,
            "macd_signal": round(signal_line.iloc[-1], 4) if pd.notna(signal_line.iloc[-1]) else None,
            "macd_histogram": round(macd_histogram.iloc[-1], 4) if pd.notna(macd_histogram.iloc[-1]) else None,
            "macd_bullish": bool(macd_line.iloc[-1] > signal_line.iloc[-1]) if (pd.notna(macd_line.iloc[-1]) and pd.notna(signal_line.iloc[-1])) else None,
        },
        "volatility": {
            "bollinger_upper": round(bb_upper.iloc[-1], 2) if pd.notna(bb_upper.iloc[-1]) else None,
            "bollinger_mid": round(bb_mid.iloc[-1], 2) if pd.notna(bb_mid.iloc[-1]) else None,
            "bollinger_lower": round(bb_lower.iloc[-1], 2) if pd.notna(bb_lower.iloc[-1]) else None,
            "price_vs_bb": "above_upper" if current_price > bb_upper.iloc[-1] else ("below_lower" if current_price < bb_lower.iloc[-1] else "within_bands") if pd.notna(bb_upper.iloc[-1]) else None,
            "atr_14": round(atr.iloc[-1], 2) if pd.notna(atr.iloc[-1]) else None,
            "atr_pct": round(atr.iloc[-1] / current_price * 100, 2) if pd.notna(atr.iloc[-1]) else None,
            "annualized_volatility": round(close.pct_change().std() * (252**0.5) * 100, 2),
        },
        "volume": {
            "current": int(volume.iloc[-1]),
            "avg_20d": int(vol_avg_20.iloc[-1]) if pd.notna(vol_avg_20.iloc[-1]) else None,
            "ratio_vs_avg": round(vol_ratio.iloc[-1], 2) if pd.notna(vol_ratio.iloc[-1]) else None,
        },
        "support_resistance": {
            "recent_high": round(high.tail(20).max(), 2),
            "recent_low": round(low.tail(20).min(), 2),
            "period_high": round(high.max(), 2),
            "period_low": round(low.min(), 2),
        },
        "returns": {
            "1d": round(close.pct_change().iloc[-1] * 100, 2) if len(close) > 1 else None,
            "5d": round((close.iloc[-1] / close.iloc[-5] - 1) * 100, 2) if len(close) > 5 else None,
            "20d": round((close.iloc[-1] / close.iloc[-20] - 1) * 100, 2) if len(close) > 20 else None,
            "60d": round((close.iloc[-1] / close.iloc[-60] - 1) * 100, 2) if len(close) > 60 else None,
        },
    }

    print(json.dumps(result, indent=2, default=str))


def cmd_screener(name):
    """Predefined screeners."""
    screeners = {
        "mega_tech": ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA"],
        "sector_etfs": ["XLK", "XLF", "XLE", "XLV", "XLI", "XLP", "XLU", "XLY", "XLC", "XLRE", "XLB"],
        "mag7": ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA"],
        "semiconductors": ["NVDA", "AMD", "INTC", "AVGO", "QCOM", "TSM", "ASML", "MU"],
        "financials": ["JPM", "BAC", "GS", "MS", "WFC", "C", "BLK", "SCHW"],
        "dividend_kings": ["JNJ", "PG", "KO", "PEP", "MMM", "EMR", "CL", "SWK"],
        "growth": ["CRWD", "SNOW", "DDOG", "NET", "PLTR", "PANW", "ZS", "BILL"],
        "value": ["BRK-B", "JPM", "UNH", "XOM", "CVX", "PFE", "VZ", "CSCO"],
        "indices": ["SPY", "QQQ", "DIA", "IWM", "VTI"],
        "commodities": ["GLD", "SLV", "USO", "UNG", "COPX", "WEAT"],
        "bonds": ["TLT", "IEF", "SHY", "HYG", "LQD", "AGG"],
        "crypto_related": ["COIN", "MARA", "RIOT", "MSTR", "BITF"],
    }

    if name not in screeners:
        print(json.dumps({
            "error": f"Unknown screener: {name}",
            "available": list(screeners.keys()),
        }, indent=2))
        return

    tickers = screeners[name]
    cmd_compare(",".join(tickers))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1].lower()
    args = sys.argv[2:]

    commands = {
        "price": lambda: cmd_price(args[0]) if args else print("Usage: price <TICKER>"),
        "history": lambda: cmd_history(args[0], args[1] if len(args) > 1 else "6mo") if args else print("Usage: history <TICKER> [period]"),
        "financials": lambda: cmd_financials(args[0]) if args else print("Usage: financials <TICKER>"),
        "options": lambda: cmd_options(args[0], args[1] if len(args) > 1 else None) if args else print("Usage: options <TICKER> [expiry]"),
        "holders": lambda: cmd_holders(args[0]) if args else print("Usage: holders <TICKER>"),
        "recommendations": lambda: cmd_recommendations(args[0]) if args else print("Usage: recommendations <TICKER>"),
        "dividends": lambda: cmd_dividends(args[0]) if args else print("Usage: dividends <TICKER>"),
        "compare": lambda: cmd_compare(args[0]) if args else print("Usage: compare <TICKER,TICKER,...>"),
        "technicals": lambda: cmd_technicals(args[0], args[1] if len(args) > 1 else "6mo") if args else print("Usage: technicals <TICKER> [period]"),
        "screener": lambda: cmd_screener(args[0]) if args else print("Usage: screener <name>"),
    }

    if command in commands:
        commands[command]()
    else:
        print(f"Unknown command: {command}")
        print(f"Available: {', '.join(commands.keys())}")
        sys.exit(1)


if __name__ == "__main__":
    main()
