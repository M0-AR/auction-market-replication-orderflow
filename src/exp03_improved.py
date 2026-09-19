"""exp03 — filtered variant B (SPEC filters ON vs OFF) on proxy data path.

Compares: A raw location-only vs B +20k participation proxy +886 invalidation +2-loss shutoff.
Participation proxy on daily data = volume z-score (honest: NOT 20k MNQ/5m — tape TODO).
Reports PF net/gross + cost x1.5/x2 sensitivity. Expect B: fewer trades, less bad DD.
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
import numpy as np
from indicators import volume_profile, fib_zone, in_discount, outside_value_area
from backtest import FillConfig, backtest_long_signals, summarize, save_run

os.makedirs("results", exist_ok=True)
rng = np.random.default_rng(7)
N = 200
closes = 18000 + np.cumsum(rng.normal(1.5, 18.0, N))
opens = np.roll(closes, 1); opens[0] = closes[0]
highs = np.maximum(opens, closes) + 6
lows = np.minimum(opens, closes) - 6
vols = rng.normal(22000, 6000, N).clip(5000, 40000)

def run(use_filters: bool):
    sig = np.zeros(N, bool); st = np.zeros(N); tg = np.zeros(N)
    losses = 0
    LOOK = 30
    for i in range(LOOK, N - 1):
        if use_filters and losses >= 2:
            continue  # shutoff: rest of DAY skipped (proxy: rest of run chunk)
        poc, vah, val = volume_profile(closes[i - LOOK:i], vols[i - LOOK:i])
        sw, sh = float(np.min(lows[i - LOOK:i])), float(np.max(highs[i - LOOK:i]))
        if sh <= sw:
            continue
        zone = fib_zone(sw, sh)
        px = float(closes[i])
        base = in_discount(px, zone) and outside_value_area(px, vah, val) and px > zone["l886"]
        if use_filters and vols[i] < 20000:
            continue
        if base and closes[i] > opens[i]:
            sig[i] = True
            st[i] = float(lows[i]) - 3
            tg[i] = min(poc, px + 1.5 * (px - st[i]))
    cfgs = {"base": FillConfig(), "x1.5": FillConfig(commission_per_side_usd=0.90),
            "x2": FillConfig(commission_per_side_usd=1.20, slip_ticks_per_side=2.0)}
    out = {}
    for k, cfg in cfgs.items():
        tr = backtest_long_signals(opens, highs, lows, closes, sig, st, tg, cfg)
        out[k] = summarize(tr)
    return out

A = run(False)
B = run(True)
print("exp03 A raw:", A["base"])
print("exp03 B filtered:", B["base"])
print("exp03 B x1.5:", B["x1.5"], "x2:", B["x2"])
save_run("results/run-v1.0-exp03-filtered-seed7.json",
         {"spec": "v1.0", "exp": "exp03", "A_raw": A, "B_filtered": B,
          "note": "synthetic; cost sensitivity included; tape replay TODO"})
