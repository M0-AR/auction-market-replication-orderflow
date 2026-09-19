"""exp01 — historical proxy arithmetic (yfinance NQ=F daily, fallback QQQ, else synthetic).

HONEST LIMITS (printed + saved): daily bars CANNOT prove 5-min footprint absorption or
intraday GEX. This checks location arithmetic (VA + fib discount + 886) and R math only.
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
import numpy as np
from indicators import volume_profile, fib_zone, in_discount, outside_value_area
from backtest import FillConfig, backtest_long_signals, summarize, save_run

os.makedirs("data/cache", exist_ok=True)
os.makedirs("results", exist_ok=True)

closes = opens = highs = lows = vols = None
proxy = "synthetic-fallback"
try:
    import yfinance as yf
    for sym in ("NQ=F", "QQQ"):
        try:
            df = yf.download(sym, period="6mo", interval="1d", progress=False, auto_adjust=True)
            if df is not None and len(df) >= 60:
                proxy = sym
                closes = df["Close"].to_numpy().ravel().astype(float)
                opens = df["Open"].to_numpy().ravel().astype(float)
                highs = df["High"].to_numpy().ravel().astype(float)
                lows = df["Low"].to_numpy().ravel().astype(float)
                vols = df["Volume"].to_numpy().ravel().astype(float)
                vols[vols <= 0] = 1e6
                break
        except Exception as e:
            print(f"yfinance {sym} failed: {e}")
except Exception as e:
    print(f"yfinance unavailable: {e}")

if closes is None:
    rng = np.random.default_rng(7)
    N = 130
    closes = 18000 + np.cumsum(rng.normal(2.0, 25.0, N))
    opens = np.roll(closes, 1); opens[0] = closes[0]
    highs = np.maximum(opens, closes) + 8
    lows = np.minimum(opens, closes) - 8
    vols = np.full(N, 1e6)

N = len(closes)
signals = np.zeros(N, bool); stops = np.zeros(N); targets = np.zeros(N)
LOOK = 30
hits = 0
for i in range(LOOK, N - 1):
    c = closes[i - LOOK:i]
    v = vols[i - LOOK:i]
    poc, vah, val = volume_profile(c, v)
    sw, sh = float(np.min(lows[i - LOOK:i])), float(np.max(highs[i - LOOK:i]))
    if sh <= sw:
        continue
    zone = fib_zone(sw, sh, "long")
    px = float(closes[i])
    if in_discount(px, zone) and outside_value_area(px, vah, val) and px > zone["l886"]:
        # proxy confirmation: bullish close + next-bar higher low (footprint needs tape — logged as proxy)
        if closes[i] > opens[i] and lows[i + 1] >= lows[i] - (sh - sw) * 0.02:
            signals[i] = True
            stops[i] = float(lows[i]) - (sh - sw) * 0.02
            targets[i] = min(poc, px + 1.5 * (px - stops[i]))  # ~1.5R toward POC
            hits += 1

cfg = FillConfig()
trades = backtest_long_signals(opens, highs, lows, closes, signals, stops, targets, cfg)
stats = summarize(trades)
out = {"spec": "v1.0", "exp": "exp01", "proxy": proxy, "location_hits": hits,
       "LIMITS": "daily proxy cannot prove footprint/GEX; tape test TODO in exp02", **stats}
print("exp01 proxy:", json.dumps(out, indent=2))
save_run("results/run-v1.0-exp01-proxy-seed7.json", out)
