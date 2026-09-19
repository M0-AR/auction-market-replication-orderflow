"""exp04 — PUBLIC 5-minute NQ intraday verification (yfinance 60d, Stooq fallback).

Sources (docs/SOURCES.md §J): Yahoo intraday depth (1m 7d / 5m 60d / 1h 730d) via
MarketData-Hub 2026 guide; Stooq free CSV (daily + delayed 5m/60m, no key) via stooq.com/db/h
+ DeepCharts 2025 yfinance-break tutorial; paid Level1 (Portara/CQG, Databento, FirstRate,
Barchart) noted as the ONLY true footprint tape — this exp is location+R math on PUBLIC bars,
NOT absorption proof. RTH 09:30–11:00 ET enforced when tz convertible.
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
import numpy as np
from indicators import volume_profile, fib_zone, in_discount, outside_value_area
from backtest import FillConfig, backtest_long_signals, summarize, save_run

os.makedirs("data/cache", exist_ok=True)
os.makedirs("results", exist_ok=True)

opens = highs = lows = closes = vols = idx = None
provenance = "synthetic-fallback(empty-public)"
try:
    import yfinance as yf
    df = yf.download("NQ=F", period="60d", interval="5m", progress=False, auto_adjust=True)
    if df is not None and len(df) >= 200:
        # flatten multiindex columns if present
        if hasattr(df.columns, "levels"):
            try:
                df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
            except Exception:
                pass
        idx = df.index
        # RTH filter if tz-aware
        try:
            ny = idx.tz_convert("America/New_York")
            mask = (ny.time >= __import__("datetime").time(9, 30)) & (ny.time <= __import__("datetime").time(11, 0))
            df = df.loc[mask]
            idx = df.index
            rth_note = "RTH 09:30-11:00 ET enforced"
        except Exception as e:
            rth_note = f"tz-naive, no RTH filter ({e})"
        closes = df["Close"].to_numpy().ravel().astype(float)
        opens = df["Open"].to_numpy().ravel().astype(float)
        highs = df["High"].to_numpy().ravel().astype(float)
        lows = df["Low"].to_numpy().ravel().astype(float)
        v = df["Volume"].to_numpy().ravel().astype(float) if "Volume" in df.columns else np.full(len(df), 20000.0)
        v[v <= 0] = 20000.0
        vols = v
        provenance = f"yfinance NQ=F 5m 60d, n={len(df)}, {rth_note}"
        with open("data/cache/nq_f_5m_60d.csv", "w") as f:
            df.to_csv(f)
        print(provenance)
except Exception as e:
    print(f"yfinance 5m failed: {e}")

if closes is None:
    try:
        import pandas as pd
        import datetime
        end = datetime.date.today()
        start = end - datetime.timedelta(days=180)
        url = f"https://stooq.com/q/d/l/?s=nq.f&d1={start:%Y%m%d}&d2={end:%Y%m%d}&i=d"
        sdf = pd.read_csv(url, parse_dates=["Date"])
        if len(sdf) >= 60:
            closes = sdf["Close"].to_numpy().astype(float)
            opens = sdf["Open"].to_numpy().astype(float)
            highs = sdf["High"].to_numpy().astype(float)
            lows = sdf["Low"].to_numpy().astype(float)
            vols = sdf["Volume"].to_numpy().astype(float)
            vols[vols <= 0] = 1e6
            provenance = f"Stooq nq.f daily fallback, n={len(sdf)} (5m unavailable, location-only)"
            sdf.to_csv("data/cache/stooq_nq_f_daily.csv", index=False)
            print(provenance)
    except Exception as e:
        print(f"Stooq fallback failed: {e}")

if closes is None:
    rng = np.random.default_rng(7)
    N = 500
    closes = 29000 + np.cumsum(rng.normal(0.5, 8.0, N))
    opens = np.roll(closes, 1); opens[0] = closes[0]
    highs = np.maximum(opens, closes) + 3
    lows = np.minimum(opens, closes) - 3
    vols = np.full(N, 22000.0)
    print("PUBLIC sources unreachable — synthetic fallback (marked, not proof)")

N = len(closes)
LOOK = 30
sig = np.zeros(N, bool); st = np.zeros(N); tg = np.zeros(N)
hits = 0
part_blocked = 0
for i in range(LOOK, N - 1):
    c = closes[i - LOOK:i]; v = vols[i - LOOK:i]
    poc, vah, val = volume_profile(c, v)
    sw, sh = float(np.min(lows[i - LOOK:i])), float(np.max(highs[i - LOOK:i]))
    if sh <= sw:
        continue
    zone = fib_zone(sw, sh, "long")
    px = float(closes[i])
    if not (in_discount(px, zone) and outside_value_area(px, vah, val) and px > zone["l886"]):
        continue
    hits += 1
    # participation proxy: 5m volume above rolling median (honest: NOT 20k MNQ tape)
    if vols[i] < np.median(v):
        part_blocked += 1
        continue
    if closes[i] > opens[i] and lows[i] >= float(np.min(lows[i - 3:i])) - (sh - sw) * 0.01:
        sig[i] = True
        st[i] = float(lows[i]) - (sh - sw) * 0.01
        tg[i] = min(poc, px + 1.5 * max(px - st[i], 1e-6))

cfgs = {"base": FillConfig(), "x1.5": FillConfig(commission_per_side_usd=0.90),
        "x2": FillConfig(commission_per_side_usd=1.20, slip_ticks_per_side=2.0)}
out = {"spec": "v1.0", "exp": "exp04", "provenance": provenance,
       "location_hits": hits, "participation_blocked": part_blocked,
       "LIMITS": "public bars: NO bid/ask tape, NO GEX feed; absorption unproven; tape TODO"}
for k, cfg in cfgs.items():
    out[k] = summarize(backtest_long_signals(opens, highs, lows, closes, sig, st, tg, cfg))
print(json.dumps({k: out[k] for k in ("base", "x1.5", "x2")}, indent=2))
print("hits:", hits, "blocked:", part_blocked, "prov:", provenance)
save_run("results/run-v1.0-exp04-public5m-seed7.json", out)
