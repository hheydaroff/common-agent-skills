#!/usr/bin/env python3
"""
Fetch top posts from investment/stock subreddits via Reddit's public JSON API.
No API key or authentication required.

Usage:
    python3 reddit_sentiment.py top [--period week] [--min-score 50]
    python3 reddit_sentiment.py hot [--min-score 30]
    python3 reddit_sentiment.py ticker <TICKER> [--period week]
    python3 reddit_sentiment.py summary [--period week]

Commands:
    top         Top posts from all tracked subreddits (default: past week)
    hot         Currently hot posts across investment subreddits
    ticker      Posts mentioning a specific ticker symbol
    summary     Condensed summary: top themes, most-discussed tickers, sentiment

Options:
    --period    Time period for 'top' sort: day, week, month, year (default: week)
    --min-score Minimum upvote score to include (default: 50 for top, 30 for hot)
    --limit     Max posts per subreddit (default: 25)
    --subs      Comma-separated subreddit override (e.g. "stocks,investing")
"""

import json
import re
import ssl
import sys
import time
import argparse
from datetime import datetime, timedelta, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from collections import Counter

_SSL_CTX = ssl.create_default_context()

# ── Configuration ────────────────────────────────────────────────────
TIMEOUT = 20
MAX_WORKERS = 3
RETRY_COUNT = 1
RETRY_DELAY = 5
USER_AGENT = "InvestmentScanner/1.0 (research; stock-sentiment)"

# Investment-focused subreddits
DEFAULT_SUBREDDITS = [
    # Core investment/trading subs
    {"sub": "wallstreetbets",   "min_score_top": 200, "min_score_hot": 100},
    {"sub": "stocks",           "min_score_top": 50,  "min_score_hot": 30},
    {"sub": "investing",        "min_score_top": 50,  "min_score_hot": 30},
    {"sub": "options",          "min_score_top": 30,  "min_score_hot": 20},
    {"sub": "stockmarket",      "min_score_top": 30,  "min_score_hot": 20},
    {"sub": "ValueInvesting",   "min_score_top": 30,  "min_score_hot": 20},
    {"sub": "dividends",        "min_score_top": 30,  "min_score_hot": 20},
    {"sub": "SecurityAnalysis", "min_score_top": 15,  "min_score_hot": 10},

    # Sector/theme specific
    {"sub": "semiconductors",   "min_score_top": 15,  "min_score_hot": 10},
    {"sub": "EnergyStorage",    "min_score_top": 15,  "min_score_hot": 10},
    {"sub": "nuclearpower",     "min_score_top": 15,  "min_score_hot": 10},
    {"sub": "weedstocks",       "min_score_top": 20,  "min_score_hot": 15},
    {"sub": "Biotechplays",     "min_score_top": 15,  "min_score_hot": 10},

    # Macro/economy
    {"sub": "economics",        "min_score_top": 50,  "min_score_hot": 30},
    {"sub": "finance",          "min_score_top": 30,  "min_score_hot": 20},

    # European / international
    {"sub": "EuropeanStocks",   "min_score_top": 10,  "min_score_hot": 5},
    {"sub": "eupersonalfinance","min_score_top": 20,  "min_score_hot": 15},
]

# Known ticker pattern — $AAPL or standalone 1-5 letter uppercase
TICKER_PATTERN = re.compile(r'(?<!\w)\$([A-Z]{1,5})(?!\w)')
BARE_TICKER = re.compile(r'(?<!\w)([A-Z]{2,5})(?!\w)')

# Common words that look like tickers but aren't
FALSE_TICKERS = {
    'A', 'I', 'AM', 'PM', 'CEO', 'CFO', 'CTO', 'IPO', 'ETF', 'ATH', 'ATL',
    'DD', 'TA', 'FA', 'IMO', 'IMHO', 'FYI', 'PSA', 'TIL', 'ELI', 'CMV',
    'USA', 'GDP', 'CPI', 'FED', 'SEC', 'FDA', 'DOJ', 'IRS', 'NYSE', 'NASDAQ',
    'EU', 'UK', 'US', 'PE', 'PB', 'PS', 'EPS', 'ROE', 'ROI', 'ROA',
    'YOY', 'QOQ', 'MOM', 'YTD', 'QTD', 'EOD', 'AH', 'PM',
    'ALL', 'NEW', 'THE', 'FOR', 'ARE', 'NOT', 'BUT', 'YOU', 'HAS', 'HAD',
    'ITS', 'HIS', 'HER', 'OUR', 'WHO', 'HOW', 'WHY', 'NOW', 'OLD',
    'BIG', 'TOP', 'LOW', 'HIGH', 'LONG', 'SHORT', 'BULL', 'BEAR',
    'BUY', 'SELL', 'HOLD', 'CALL', 'PUT', 'YOLO', 'FOMO', 'HODL',
    'EDIT', 'UPDATE', 'TLDR', 'MOAT', 'DEBT', 'CASH', 'RISK',
    'API', 'AI', 'ML', 'EV', 'RE', 'OTC', 'ITM', 'OTM', 'ATM',
    'DCA', 'DRIP', 'RSI', 'MACD', 'SMA', 'EMA', 'VWAP',
    'OP', 'RIP', 'LOL', 'WTF', 'SMH', 'LMAO',
    # Location / media / common words that look like tickers
    'NYC', 'LA', 'SF', 'DC', 'TV', 'PC', 'GPU', 'CPU', 'RAM', 'SSD',
    'IRA', 'LLC', 'INC', 'LTD', 'CEO', 'WSJ', 'CNN', 'BBC', 'NPR',
    'LLM', 'AGI', 'NPC', 'DRAM', 'HARD', 'SOFT', 'CHIP', 'TECH',
    'WAR', 'WIN', 'LOSS', 'GAIN', 'PUMP', 'DUMP', 'PEAK', 'RATE',
    'BOND', 'FUND', 'LOAN', 'RENT', 'HOME', 'WAGE', 'JOBS',
}

# Noise filter — skip low-signal posts
NOISE_PATTERNS = re.compile(
    r'^(Help|Rant|Am I|ELI5|Newbie|Beginner|First time|Just started|'
    r'Is it too late|Should I sell everything|Scared|Panic|'
    r'Rate my portfolio|Roast my|What do you think of my)',
    re.IGNORECASE
)


def extract_tickers(title, selftext=""):
    """Extract potential ticker symbols from post title and body."""
    text = f"{title} {selftext}"
    tickers = set()

    # $TICKER format (high confidence)
    for match in TICKER_PATTERN.finditer(text):
        t = match.group(1)
        if t not in FALSE_TICKERS:
            tickers.add(t)

    # Bare uppercase in title only (medium confidence, title more reliable)
    for match in BARE_TICKER.finditer(title):
        t = match.group(1)
        if t not in FALSE_TICKERS and len(t) >= 2:
            tickers.add(t)

    return sorted(tickers)


def is_noise(title):
    """Return True if post is likely low-signal noise."""
    if NOISE_PATTERNS.match(title.strip()):
        return True
    if len(title.strip()) < 15:
        return True
    return False


def fetch_subreddit(subreddit, sort="top", period="week", limit=25, min_score=50):
    """Fetch posts from a single subreddit."""
    if sort == "top":
        url = f"https://www.reddit.com/r/{subreddit}/top.json?t={period}&limit={limit}&raw_json=1"
    else:
        url = f"https://www.reddit.com/r/{subreddit}/{sort}.json?limit={limit}&raw_json=1"

    for attempt in range(RETRY_COUNT + 1):
        try:
            req = Request(url, headers={
                'User-Agent': USER_AGENT,
                'Accept': 'text/html,application/json',
            })
            with urlopen(req, timeout=TIMEOUT, context=_SSL_CTX) as resp:
                data = json.loads(resp.read().decode('utf-8'))

            posts = []
            for child in data.get('data', {}).get('children', []):
                post = child.get('data', {})
                if not post:
                    continue

                # Skip stickied/pinned
                if post.get('stickied', False):
                    continue

                score = post.get('score', 0)
                if score < min_score:
                    continue

                title = post.get('title', '').strip()
                if not title:
                    continue

                if is_noise(title):
                    continue

                selftext = post.get('selftext', '')[:500]  # First 500 chars for ticker extraction
                tickers = extract_tickers(title, selftext)

                created_utc = post.get('created_utc', 0)
                post_time = datetime.fromtimestamp(created_utc, tz=timezone.utc)

                permalink = f"https://www.reddit.com{post.get('permalink', '')}"
                flair = post.get('link_flair_text', '') or ''
                num_comments = post.get('num_comments', 0)
                upvote_ratio = post.get('upvote_ratio', 0)

                posts.append({
                    'title': title.replace('|', ' —'),
                    'url': permalink,
                    'source': f"r/{subreddit}",
                    'score': score,
                    'comments': num_comments,
                    'upvote_ratio': upvote_ratio,
                    'tickers': tickers,
                    'flair': flair,
                    'created': post_time.strftime('%Y-%m-%d %H:%M UTC'),
                    'created_utc': created_utc,
                })

            return posts

        except HTTPError as e:
            if e.code == 429 and attempt < RETRY_COUNT:
                time.sleep(10)
                continue
            elif e.code == 403:
                print(f"  ⚠ r/{subreddit}: private/quarantined", file=sys.stderr)
                return []
            print(f"  ⚠ r/{subreddit}: HTTP {e.code}", file=sys.stderr)
        except (URLError, OSError) as e:
            print(f"  ⚠ r/{subreddit}: network error — {e}", file=sys.stderr)
        except Exception as e:
            print(f"  ⚠ r/{subreddit}: {e}", file=sys.stderr)

        if attempt < RETRY_COUNT:
            time.sleep(RETRY_DELAY)

    return []


def deduplicate(posts):
    """Remove duplicate posts (same URL)."""
    seen = set()
    unique = []
    for post in posts:
        if post['url'] not in seen:
            seen.add(post['url'])
            unique.append(post)
    return unique


def cmd_top_or_hot(args, sort):
    """Fetch top or hot posts from all subreddits."""
    subreddits = DEFAULT_SUBREDDITS
    if args.subs:
        subreddits = [{"sub": s.strip(), "min_score_top": args.min_score or 20, "min_score_hot": args.min_score or 10}
                      for s in args.subs.split(',')]

    all_posts = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {}
        for cfg in subreddits:
            sub = cfg["sub"]
            if args.min_score:
                min_score = args.min_score
            else:
                min_score = cfg.get(f"min_score_{sort}", 30)

            future = pool.submit(
                fetch_subreddit, sub, sort,
                period=args.period, limit=args.limit, min_score=min_score
            )
            futures[future] = sub

        for future in as_completed(futures):
            posts = future.result()
            all_posts.extend(posts)
            # Rate limit between subreddit fetches
            time.sleep(0.5)

    all_posts = deduplicate(all_posts)
    all_posts.sort(key=lambda x: -x['score'])

    # Output
    print(f"# Reddit {sort.capitalize()} Posts — Investment/Stock Subreddits")
    print(f"Period: {args.period} | Min score: {args.min_score or 'per-sub default'}")
    print(f"Posts found: {len(all_posts)}")
    print()

    for i, post in enumerate(all_posts, 1):
        tickers_str = ', '.join(post['tickers']) if post['tickers'] else '—'
        print(f"## {i}. {post['title']}")
        print(f"- **Source:** {post['source']} | **Score:** {post['score']} | **Comments:** {post['comments']} | **Ratio:** {post['upvote_ratio']:.0%}")
        print(f"- **Tickers:** {tickers_str}")
        if post['flair']:
            print(f"- **Flair:** {post['flair']}")
        print(f"- **Posted:** {post['created']}")
        print(f"- **URL:** {post['url']}")
        print()

    print(f"\n---\nTotal: {len(all_posts)} posts from {len(subreddits)} subreddits", file=sys.stderr)


def cmd_ticker(args):
    """Find posts mentioning a specific ticker."""
    ticker = args.ticker.upper().replace('$', '')
    subreddits = DEFAULT_SUBREDDITS
    if args.subs:
        subreddits = [{"sub": s.strip(), "min_score_top": 5, "min_score_hot": 5}
                      for s in args.subs.split(',')]

    all_posts = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {}
        for cfg in subreddits:
            sub = cfg["sub"]
            # Use lower threshold for ticker search — we filter by mention
            future = pool.submit(
                fetch_subreddit, sub, "top",
                period=args.period, limit=50, min_score=5
            )
            futures[future] = sub

        for future in as_completed(futures):
            posts = future.result()
            all_posts.extend(posts)
            time.sleep(0.5)

    # Filter to posts mentioning the ticker
    ticker_posts = []
    ticker_re = re.compile(r'(?<!\w)(\$?' + re.escape(ticker) + r')(?!\w)', re.IGNORECASE)
    for post in all_posts:
        if ticker in post['tickers'] or ticker_re.search(post['title']):
            ticker_posts.append(post)

    ticker_posts = deduplicate(ticker_posts)
    ticker_posts.sort(key=lambda x: -x['score'])

    print(f"# Reddit Mentions: ${ticker}")
    print(f"Period: {args.period} | Posts found: {len(ticker_posts)}")
    print()

    if not ticker_posts:
        print(f"No posts mentioning ${ticker} found in the past {args.period}.")
        print("Try a longer period (--period month) or check if the ticker is correct.")
        return

    # Sentiment signals
    bullish_words = re.compile(r'(buy|long|calls?|bull|moon|undervalued|upside|breakout|accumulate)', re.I)
    bearish_words = re.compile(r'(sell|short|puts?|bear|overvalued|crash|dump|avoid|downside)', re.I)

    bull_count = sum(1 for p in ticker_posts if bullish_words.search(p['title']))
    bear_count = sum(1 for p in ticker_posts if bearish_words.search(p['title']))

    print(f"**Sentiment signal:** {bull_count} bullish / {bear_count} bearish / {len(ticker_posts) - bull_count - bear_count} neutral")
    print()

    for i, post in enumerate(ticker_posts[:20], 1):
        print(f"## {i}. {post['title']}")
        print(f"- **Source:** {post['source']} | **Score:** {post['score']} | **Comments:** {post['comments']}")
        print(f"- **Posted:** {post['created']}")
        print(f"- **URL:** {post['url']}")
        print()


def cmd_summary(args):
    """Condensed summary: top themes, most-discussed tickers, high-engagement posts."""
    subreddits = DEFAULT_SUBREDDITS
    if args.subs:
        subreddits = [{"sub": s.strip(), "min_score_top": 20, "min_score_hot": 10}
                      for s in args.subs.split(',')]

    all_posts = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {}
        for cfg in subreddits:
            sub = cfg["sub"]
            min_score = cfg.get("min_score_top", 20)
            future = pool.submit(
                fetch_subreddit, sub, "top",
                period=args.period, limit=args.limit, min_score=min_score
            )
            futures[future] = sub

        for future in as_completed(futures):
            posts = future.result()
            all_posts.extend(posts)
            time.sleep(0.5)

    all_posts = deduplicate(all_posts)

    if not all_posts:
        print("No posts found. Reddit may be rate-limiting or subreddits are empty.")
        return

    # Count ticker mentions
    ticker_counter = Counter()
    for post in all_posts:
        for t in post['tickers']:
            ticker_counter[t] += 1

    # Count by engagement (score-weighted)
    ticker_engagement = Counter()
    for post in all_posts:
        for t in post['tickers']:
            ticker_engagement[t] += post['score']

    # Top posts by engagement (score × comments)
    all_posts.sort(key=lambda x: -(x['score'] * max(x['comments'], 1)))

    print(f"# Reddit Investment Sentiment Summary")
    print(f"Period: {args.period} | Total posts analyzed: {len(all_posts)}")
    print(f"Date: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print()

    # Most discussed tickers
    print("## Most Discussed Tickers (by mention count)")
    print("| Ticker | Mentions | Total Engagement (score) |")
    print("|--------|----------|--------------------------|")
    for ticker, count in ticker_counter.most_common(20):
        eng = ticker_engagement.get(ticker, 0)
        print(f"| ${ticker} | {count} | {eng:,} |")
    print()

    # Highest engagement posts
    print("## Highest Engagement Posts")
    for i, post in enumerate(all_posts[:15], 1):
        tickers_str = ', '.join(f'${t}' for t in post['tickers']) if post['tickers'] else '—'
        print(f"{i}. **[{post['source']}]** {post['title']}")
        print(f"   Score: {post['score']} | Comments: {post['comments']} | Tickers: {tickers_str}")
        print()

    # Subreddit activity
    sub_counts = Counter(p['source'] for p in all_posts)
    print("## Subreddit Activity")
    print("| Subreddit | Posts | Avg Score |")
    print("|-----------|-------|-----------|")
    for sub, count in sub_counts.most_common():
        sub_posts = [p for p in all_posts if p['source'] == sub]
        avg_score = sum(p['score'] for p in sub_posts) / len(sub_posts)
        print(f"| {sub} | {count} | {avg_score:.0f} |")
    print()

    # Simple sentiment from flairs
    flair_counter = Counter(p['flair'] for p in all_posts if p['flair'])
    if flair_counter:
        print("## Post Flairs (sentiment proxy)")
        for flair, count in flair_counter.most_common(10):
            print(f"- {flair}: {count}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Fetch investment/stock posts from Reddit (no API key required)"
    )
    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Top command
    top_parser = subparsers.add_parser('top', help='Top posts from investment subreddits')
    top_parser.add_argument('--period', default='week', choices=['day', 'week', 'month', 'year'])
    top_parser.add_argument('--min-score', type=int, default=0)
    top_parser.add_argument('--limit', type=int, default=25)
    top_parser.add_argument('--subs', type=str, default='', help='Comma-separated subreddit override')

    # Hot command
    hot_parser = subparsers.add_parser('hot', help='Currently hot posts')
    hot_parser.add_argument('--period', default='week')  # unused for hot, but keeps interface consistent
    hot_parser.add_argument('--min-score', type=int, default=0)
    hot_parser.add_argument('--limit', type=int, default=25)
    hot_parser.add_argument('--subs', type=str, default='', help='Comma-separated subreddit override')

    # Ticker command
    ticker_parser = subparsers.add_parser('ticker', help='Posts mentioning a specific ticker')
    ticker_parser.add_argument('ticker', type=str, help='Ticker symbol (e.g. NVDA or $NVDA)')
    ticker_parser.add_argument('--period', default='week', choices=['day', 'week', 'month', 'year'])
    ticker_parser.add_argument('--min-score', type=int, default=0)
    ticker_parser.add_argument('--limit', type=int, default=50)
    ticker_parser.add_argument('--subs', type=str, default='', help='Comma-separated subreddit override')

    # Summary command
    summary_parser = subparsers.add_parser('summary', help='Condensed sentiment summary')
    summary_parser.add_argument('--period', default='week', choices=['day', 'week', 'month', 'year'])
    summary_parser.add_argument('--min-score', type=int, default=0)
    summary_parser.add_argument('--limit', type=int, default=25)
    summary_parser.add_argument('--subs', type=str, default='', help='Comma-separated subreddit override')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == 'top':
        cmd_top_or_hot(args, 'top')
    elif args.command == 'hot':
        cmd_top_or_hot(args, 'hot')
    elif args.command == 'ticker':
        cmd_ticker(args)
    elif args.command == 'summary':
        cmd_summary(args)


if __name__ == "__main__":
    main()
