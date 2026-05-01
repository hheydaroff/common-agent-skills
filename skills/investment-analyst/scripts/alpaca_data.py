#!/usr/bin/env python3
"""
Alpaca Markets data fetcher — stocks, options, crypto, screener, and news.
Requires API key stored in ~/.pi/.secrets/alpaca_api_key and alpaca_api_secret.

Usage: python3 alpaca_data.py <command> <args>

Commands:
  quote <TICKER>                      Real-time quote (NBBO)
  bars <TICKER> [timeframe] [period]  Historical bars (1Min,5Min,15Min,1Hour,1Day)
  snapshot <TICKER>                   Latest bar + quote + trade + minute bar
  multisnapshot <T1,T2,...>           Multiple snapshots at once
  trades <TICKER> [limit]            Recent trades
  options_chain <TICKER>              Full options chain with Greeks
  options_snapshot <SYMBOL>           Single option contract snapshot
  news <TICKER> [limit]              Recent news articles
  screener <type>                     Most active / top gainers / top losers
  crypto_quote <SYMBOL>               Crypto quote (BTC/USD, ETH/USD, etc.)
  crypto_bars <SYMBOL> [tf] [period]  Crypto historical bars
  account                             Account info (if trading enabled)
"""

import sys
import json
import os
import warnings
from datetime import datetime, timedelta

warnings.filterwarnings("ignore")

try:
    from alpaca.data.historical import StockHistoricalDataClient, OptionHistoricalDataClient, CryptoHistoricalDataClient
    from alpaca.data.live import StockDataStream
    from alpaca.data.requests import (
        StockBarsRequest, StockLatestQuoteRequest, StockSnapshotRequest,
        StockTradesRequest, OptionChainRequest, OptionSnapshotRequest,
        CryptoBarsRequest, CryptoSnapshotRequest,
        StockLatestBarRequest,
    )
    from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
    from alpaca.common.exceptions import APIError
    import pandas as pd
except ImportError as e:
    print(f"Error: Missing dependency — {e}")
    print("Install with: uv run --with alpaca-py --with pandas python3 alpaca_data.py ...")
    sys.exit(1)


def get_keys():
    """Load Alpaca API keys from secrets files."""
    secrets_dir = os.path.expanduser("~/.pi/.secrets")
    key_file = os.path.join(secrets_dir, "alpaca_api_key")
    secret_file = os.path.join(secrets_dir, "alpaca_api_secret")

    api_key = os.environ.get("ALPACA_API_KEY")
    api_secret = os.environ.get("ALPACA_API_SECRET")

    if not api_key:
        if os.path.exists(key_file):
            api_key = open(key_file).read().strip()
        else:
            print(f"Error: No Alpaca API key found.")
            print(f"Store it: echo 'your-key' > {key_file} && chmod 600 {key_file}")
            sys.exit(1)

    if not api_secret:
        if os.path.exists(secret_file):
            api_secret = open(secret_file).read().strip()
        else:
            print(f"Error: No Alpaca API secret found.")
            print(f"Store it: echo 'your-secret' > {secret_file} && chmod 600 {secret_file}")
            sys.exit(1)

    return api_key, api_secret


def get_stock_client():
    api_key, api_secret = get_keys()
    return StockHistoricalDataClient(api_key=api_key, secret_key=api_secret)


def get_option_client():
    api_key, api_secret = get_keys()
    return OptionHistoricalDataClient(api_key=api_key, secret_key=api_secret)


def get_crypto_client():
    api_key, api_secret = get_keys()
    return CryptoHistoricalDataClient(api_key=api_key, secret_key=api_secret)


def parse_timeframe(tf_str):
    """Parse timeframe string like '1Day', '5Min', '1Hour'."""
    tf_map = {
        "1min": TimeFrame(1, TimeFrameUnit.Minute),
        "5min": TimeFrame(5, TimeFrameUnit.Minute),
        "15min": TimeFrame(15, TimeFrameUnit.Minute),
        "30min": TimeFrame(30, TimeFrameUnit.Minute),
        "1hour": TimeFrame(1, TimeFrameUnit.Hour),
        "4hour": TimeFrame(4, TimeFrameUnit.Hour),
        "1day": TimeFrame(1, TimeFrameUnit.Day),
        "1week": TimeFrame(1, TimeFrameUnit.Week),
        "1month": TimeFrame(1, TimeFrameUnit.Month),
    }
    return tf_map.get(tf_str.lower(), TimeFrame(1, TimeFrameUnit.Day))


def period_to_start(period_str):
    """Convert period string to start datetime."""
    now = datetime.now()
    period_map = {
        "1d": timedelta(days=1),
        "5d": timedelta(days=5),
        "1w": timedelta(weeks=1),
        "1mo": timedelta(days=30),
        "3mo": timedelta(days=90),
        "6mo": timedelta(days=180),
        "1y": timedelta(days=365),
        "2y": timedelta(days=730),
        "5y": timedelta(days=1825),
    }
    delta = period_map.get(period_str.lower(), timedelta(days=30))
    return now - delta


def cmd_quote(ticker):
    """Get real-time NBBO quote."""
    client = get_stock_client()
    request = StockLatestQuoteRequest(symbol_or_symbols=ticker.upper())
    quotes = client.get_stock_latest_quote(request)

    for symbol, quote in quotes.items():
        result = {
            "ticker": symbol,
            "bid": quote.bid_price,
            "ask": quote.ask_price,
            "bid_size": quote.bid_size,
            "ask_size": quote.ask_size,
            "spread": round(quote.ask_price - quote.bid_price, 4) if quote.ask_price and quote.bid_price else None,
            "spread_pct": round((quote.ask_price - quote.bid_price) / quote.bid_price * 100, 4) if quote.bid_price else None,
            "timestamp": str(quote.timestamp),
        }
        print(json.dumps(result, indent=2, default=str))


def cmd_bars(ticker, timeframe="1Day", period="3mo"):
    """Get historical bars."""
    client = get_stock_client()
    tf = parse_timeframe(timeframe)
    start = period_to_start(period)

    request = StockBarsRequest(
        symbol_or_symbols=ticker.upper(),
        timeframe=tf,
        start=start,
    )
    bars = client.get_stock_bars(request)

    records = []
    for bar in bars[ticker.upper()]:
        records.append({
            "timestamp": str(bar.timestamp),
            "open": bar.open,
            "high": bar.high,
            "low": bar.low,
            "close": bar.close,
            "volume": bar.volume,
            "vwap": bar.vwap,
            "trade_count": bar.trade_count,
        })

    result = {
        "ticker": ticker.upper(),
        "timeframe": timeframe,
        "period": period,
        "total_bars": len(records),
        "recent_bars": records[-30:],  # Last 30
    }

    if records:
        closes = [r["close"] for r in records]
        result["summary"] = {
            "start_price": closes[0],
            "end_price": closes[-1],
            "return_pct": round((closes[-1] / closes[0] - 1) * 100, 2),
            "high": max(r["high"] for r in records),
            "low": min(r["low"] for r in records),
            "avg_volume": int(sum(r["volume"] for r in records) / len(records)),
        }

    print(json.dumps(result, indent=2, default=str))


def cmd_snapshot(ticker):
    """Get latest snapshot — quote + trade + bar."""
    client = get_stock_client()
    request = StockSnapshotRequest(symbol_or_symbols=ticker.upper())
    snapshots = client.get_stock_snapshot(request)

    for symbol, snap in snapshots.items():
        result = {
            "ticker": symbol,
            "latest_trade": {
                "price": snap.latest_trade.price if snap.latest_trade else None,
                "size": snap.latest_trade.size if snap.latest_trade else None,
                "timestamp": str(snap.latest_trade.timestamp) if snap.latest_trade else None,
            },
            "latest_quote": {
                "bid": snap.latest_quote.bid_price if snap.latest_quote else None,
                "ask": snap.latest_quote.ask_price if snap.latest_quote else None,
                "bid_size": snap.latest_quote.bid_size if snap.latest_quote else None,
                "ask_size": snap.latest_quote.ask_size if snap.latest_quote else None,
            },
            "daily_bar": {
                "open": snap.daily_bar.open if snap.daily_bar else None,
                "high": snap.daily_bar.high if snap.daily_bar else None,
                "low": snap.daily_bar.low if snap.daily_bar else None,
                "close": snap.daily_bar.close if snap.daily_bar else None,
                "volume": snap.daily_bar.volume if snap.daily_bar else None,
                "vwap": snap.daily_bar.vwap if snap.daily_bar else None,
            },
            "minute_bar": {
                "open": snap.minute_bar.open if snap.minute_bar else None,
                "high": snap.minute_bar.high if snap.minute_bar else None,
                "low": snap.minute_bar.low if snap.minute_bar else None,
                "close": snap.minute_bar.close if snap.minute_bar else None,
                "volume": snap.minute_bar.volume if snap.minute_bar else None,
            },
            "prev_daily_bar": {
                "open": snap.previous_daily_bar.open if snap.previous_daily_bar else None,
                "close": snap.previous_daily_bar.close if snap.previous_daily_bar else None,
                "volume": snap.previous_daily_bar.volume if snap.previous_daily_bar else None,
            },
        }
        print(json.dumps(result, indent=2, default=str))


def cmd_multisnapshot(tickers_str):
    """Get snapshots for multiple tickers."""
    tickers = [t.strip().upper() for t in tickers_str.split(",")]
    client = get_stock_client()
    request = StockSnapshotRequest(symbol_or_symbols=tickers)
    snapshots = client.get_stock_snapshot(request)

    results = []
    for symbol, snap in snapshots.items():
        results.append({
            "ticker": symbol,
            "price": snap.latest_trade.price if snap.latest_trade else None,
            "bid": snap.latest_quote.bid_price if snap.latest_quote else None,
            "ask": snap.latest_quote.ask_price if snap.latest_quote else None,
            "daily_open": snap.daily_bar.open if snap.daily_bar else None,
            "daily_high": snap.daily_bar.high if snap.daily_bar else None,
            "daily_low": snap.daily_bar.low if snap.daily_bar else None,
            "daily_close": snap.daily_bar.close if snap.daily_bar else None,
            "daily_volume": snap.daily_bar.volume if snap.daily_bar else None,
            "daily_vwap": snap.daily_bar.vwap if snap.daily_bar else None,
            "prev_close": snap.previous_daily_bar.close if snap.previous_daily_bar else None,
            "change_pct": round((snap.daily_bar.close / snap.previous_daily_bar.close - 1) * 100, 2)
                if (snap.daily_bar and snap.previous_daily_bar and snap.previous_daily_bar.close) else None,
        })

    print(json.dumps({"snapshots": results}, indent=2, default=str))


def cmd_trades(ticker, limit=20):
    """Get recent trades."""
    client = get_stock_client()
    request = StockTradesRequest(
        symbol_or_symbols=ticker.upper(),
        limit=int(limit),
    )
    trades = client.get_stock_trades(request)

    records = []
    for trade in trades[ticker.upper()]:
        records.append({
            "price": trade.price,
            "size": trade.size,
            "timestamp": str(trade.timestamp),
            "exchange": trade.exchange,
        })

    print(json.dumps({"ticker": ticker.upper(), "trades": records}, indent=2, default=str))


def cmd_options_chain(ticker):
    """Get options chain with Greeks."""
    client = get_option_client()

    try:
        request = OptionChainRequest(underlying_symbol=ticker.upper())
        chain = client.get_option_chain(request)

        results = {"ticker": ticker.upper(), "contracts": []}

        for symbol, snapshot in list(chain.items())[:50]:  # Limit to 50 contracts
            contract = {
                "symbol": symbol,
                "latest_quote": None,
                "latest_trade": None,
                "greeks": None,
                "implied_volatility": None,
            }

            if snapshot.latest_quote:
                contract["latest_quote"] = {
                    "bid": snapshot.latest_quote.bid_price,
                    "ask": snapshot.latest_quote.ask_price,
                    "bid_size": snapshot.latest_quote.bid_size,
                    "ask_size": snapshot.latest_quote.ask_size,
                }

            if snapshot.latest_trade:
                contract["latest_trade"] = {
                    "price": snapshot.latest_trade.price,
                    "size": snapshot.latest_trade.size,
                    "timestamp": str(snapshot.latest_trade.timestamp),
                }

            if hasattr(snapshot, 'greeks') and snapshot.greeks:
                contract["greeks"] = {
                    "delta": snapshot.greeks.delta,
                    "gamma": snapshot.greeks.gamma,
                    "theta": snapshot.greeks.theta,
                    "vega": snapshot.greeks.vega,
                    "rho": snapshot.greeks.rho,
                }

            if hasattr(snapshot, 'implied_volatility'):
                contract["implied_volatility"] = snapshot.implied_volatility

            results["contracts"].append(contract)

        print(json.dumps(results, indent=2, default=str))

    except APIError as e:
        print(json.dumps({"error": str(e), "note": "Options data requires Alpaca options subscription"}, indent=2))


def cmd_options_snapshot(symbol):
    """Get single option contract snapshot."""
    client = get_option_client()

    try:
        request = OptionSnapshotRequest(symbol_or_symbols=symbol.upper())
        snapshots = client.get_option_snapshot(request)

        for sym, snapshot in snapshots.items():
            result = {
                "symbol": sym,
                "latest_quote": {
                    "bid": snapshot.latest_quote.bid_price if snapshot.latest_quote else None,
                    "ask": snapshot.latest_quote.ask_price if snapshot.latest_quote else None,
                },
                "latest_trade": {
                    "price": snapshot.latest_trade.price if snapshot.latest_trade else None,
                    "timestamp": str(snapshot.latest_trade.timestamp) if snapshot.latest_trade else None,
                },
            }

            if hasattr(snapshot, 'greeks') and snapshot.greeks:
                result["greeks"] = {
                    "delta": snapshot.greeks.delta,
                    "gamma": snapshot.greeks.gamma,
                    "theta": snapshot.greeks.theta,
                    "vega": snapshot.greeks.vega,
                    "rho": snapshot.greeks.rho,
                }

            if hasattr(snapshot, 'implied_volatility'):
                result["implied_volatility"] = snapshot.implied_volatility

            print(json.dumps(result, indent=2, default=str))

    except APIError as e:
        print(json.dumps({"error": str(e)}, indent=2))


def cmd_news(ticker, limit=10):
    """Get recent news for a ticker."""
    # Alpaca news is via the trading client, use REST directly
    import urllib.request
    api_key, api_secret = get_keys()

    url = f"https://data.alpaca.markets/v1beta1/news?symbols={ticker.upper()}&limit={limit}&sort=desc"
    req = urllib.request.Request(url, headers={
        "APCA-API-KEY-ID": api_key,
        "APCA-API-SECRET-KEY": api_secret,
    })

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())

        articles = []
        for article in data.get("news", []):
            articles.append({
                "headline": article.get("headline"),
                "summary": article.get("summary", "")[:300],
                "source": article.get("source"),
                "url": article.get("url"),
                "created_at": article.get("created_at"),
                "symbols": article.get("symbols", []),
            })

        print(json.dumps({"ticker": ticker.upper(), "articles": articles}, indent=2, default=str))

    except Exception as e:
        print(json.dumps({"error": str(e)}, indent=2))


def cmd_screener(screen_type):
    """Get most active / top gainers / top losers."""
    import urllib.request
    api_key, api_secret = get_keys()

    # Use the screener endpoint
    type_map = {
        "active": "most_actives",
        "most_active": "most_actives",
        "gainers": "top_gainers",
        "top_gainers": "top_gainers",
        "losers": "top_losers",
        "top_losers": "top_losers",
    }

    endpoint = type_map.get(screen_type.lower(), "most_actives")
    url = f"https://data.alpaca.markets/v1beta1/screener/stocks/{endpoint}?top=20"
    req = urllib.request.Request(url, headers={
        "APCA-API-KEY-ID": api_key,
        "APCA-API-SECRET-KEY": api_secret,
    })

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())

        print(json.dumps({"screener": endpoint, "data": data}, indent=2, default=str))

    except Exception as e:
        print(json.dumps({"error": str(e)}, indent=2))


def cmd_crypto_quote(symbol):
    """Get crypto quote."""
    client = get_crypto_client()

    try:
        request = CryptoSnapshotRequest(symbol_or_symbols=symbol.upper())
        snapshots = client.get_crypto_snapshot(request)

        for sym, snap in snapshots.items():
            result = {
                "symbol": sym,
                "latest_trade": {
                    "price": snap.latest_trade.price if snap.latest_trade else None,
                    "size": snap.latest_trade.size if snap.latest_trade else None,
                    "timestamp": str(snap.latest_trade.timestamp) if snap.latest_trade else None,
                },
                "latest_quote": {
                    "bid": snap.latest_quote.bid_price if snap.latest_quote else None,
                    "ask": snap.latest_quote.ask_price if snap.latest_quote else None,
                },
                "daily_bar": {
                    "open": snap.daily_bar.open if snap.daily_bar else None,
                    "high": snap.daily_bar.high if snap.daily_bar else None,
                    "low": snap.daily_bar.low if snap.daily_bar else None,
                    "close": snap.daily_bar.close if snap.daily_bar else None,
                    "volume": snap.daily_bar.volume if snap.daily_bar else None,
                    "vwap": snap.daily_bar.vwap if snap.daily_bar else None,
                },
            }
            print(json.dumps(result, indent=2, default=str))

    except Exception as e:
        print(json.dumps({"error": str(e)}, indent=2))


def cmd_crypto_bars(symbol, timeframe="1Day", period="1mo"):
    """Get crypto historical bars."""
    client = get_crypto_client()
    tf = parse_timeframe(timeframe)
    start = period_to_start(period)

    request = CryptoBarsRequest(
        symbol_or_symbols=symbol.upper(),
        timeframe=tf,
        start=start,
    )
    bars = client.get_crypto_bars(request)

    records = []
    for bar in bars[symbol.upper()]:
        records.append({
            "timestamp": str(bar.timestamp),
            "open": bar.open,
            "high": bar.high,
            "low": bar.low,
            "close": bar.close,
            "volume": bar.volume,
            "vwap": bar.vwap,
        })

    result = {
        "symbol": symbol.upper(),
        "timeframe": timeframe,
        "total_bars": len(records),
        "recent_bars": records[-20:],
    }
    print(json.dumps(result, indent=2, default=str))


def cmd_account():
    """Get account info."""
    try:
        from alpaca.trading.client import TradingClient
        api_key, api_secret = get_keys()
        client = TradingClient(api_key=api_key, secret_key=api_secret)
        account = client.get_account()

        result = {
            "status": account.status,
            "equity": float(account.equity),
            "cash": float(account.cash),
            "buying_power": float(account.buying_power),
            "portfolio_value": float(account.portfolio_value),
            "day_trade_count": account.daytrade_count,
            "pattern_day_trader": account.pattern_day_trader,
        }
        print(json.dumps(result, indent=2, default=str))

    except Exception as e:
        print(json.dumps({"error": str(e)}, indent=2))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1].lower()
    args = sys.argv[2:]

    commands = {
        "quote": lambda: cmd_quote(args[0]) if args else print("Usage: quote <TICKER>"),
        "bars": lambda: cmd_bars(args[0], args[1] if len(args) > 1 else "1Day", args[2] if len(args) > 2 else "3mo") if args else print("Usage: bars <TICKER> [timeframe] [period]"),
        "snapshot": lambda: cmd_snapshot(args[0]) if args else print("Usage: snapshot <TICKER>"),
        "multisnapshot": lambda: cmd_multisnapshot(args[0]) if args else print("Usage: multisnapshot <T1,T2,...>"),
        "trades": lambda: cmd_trades(args[0], args[1] if len(args) > 1 else 20) if args else print("Usage: trades <TICKER> [limit]"),
        "options_chain": lambda: cmd_options_chain(args[0]) if args else print("Usage: options_chain <TICKER>"),
        "options_snapshot": lambda: cmd_options_snapshot(args[0]) if args else print("Usage: options_snapshot <OPTION_SYMBOL>"),
        "news": lambda: cmd_news(args[0], args[1] if len(args) > 1 else 10) if args else print("Usage: news <TICKER> [limit]"),
        "screener": lambda: cmd_screener(args[0]) if args else print("Usage: screener <active|gainers|losers>"),
        "crypto_quote": lambda: cmd_crypto_quote(args[0]) if args else print("Usage: crypto_quote <SYMBOL>"),
        "crypto_bars": lambda: cmd_crypto_bars(args[0], args[1] if len(args) > 1 else "1Day", args[2] if len(args) > 2 else "1mo") if args else print("Usage: crypto_bars <SYMBOL> [timeframe] [period]"),
        "account": lambda: cmd_account(),
    }

    if command in commands:
        try:
            commands[command]()
        except APIError as e:
            print(json.dumps({"error": f"Alpaca API error: {e}", "hint": "Check your API keys in ~/.pi/.secrets/alpaca_api_key and alpaca_api_secret"}, indent=2))
        except Exception as e:
            error_str = str(e)
            if "401" in error_str or "Unauthorized" in error_str:
                print(json.dumps({"error": "Authentication failed", "hint": "Check your API keys in ~/.pi/.secrets/alpaca_api_key and alpaca_api_secret"}, indent=2))
            else:
                print(json.dumps({"error": error_str}, indent=2))
    else:
        print(f"Unknown command: {command}")
        print(f"Available: {', '.join(commands.keys())}")
        sys.exit(1)


if __name__ == "__main__":
    main()
