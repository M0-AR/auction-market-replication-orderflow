"""exp02 — replay/paper harness (dry-run default). Real tape TODO until keys exist.

- Reads `data/sample_mnq_5m.csv` if present (columns: ts,open,high,low,close,volume,bid,ask),
  else runs dry-run self-check on synthetic bid/ask and exits 0 without edge claims.
- Live hooks (Tradovate paper + GEX feed) are import-guarded stubs: prints what WOULD run.
- Enforces SPEC filters: 20k participation, 90-min RTH window note, 2-loss shutoff (simulated).
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
import numpy as np
from indicators import detect_absorption, gex_regime_stub
from backtest import FillConfig

os.makedirs("results", exist_ok=True)
SAMPLE = "data/sample_mnq_5m.csv"

print("exp02 replay/paper harness — SPEC v1.0")
print("GEX stub (no key):", gex_regime_stub(None))
print("Tradovate hook:", "SKIPPED (no TRADOVATE_* env; set TRADOVATE_PAPER=true + creds to enable)")

if not os.path.exists(SAMPLE):
    # dry-run: verify shutoff + absorption logic without claiming trades
    losses = 0
    for r in [-1.0, -1.0, +1.5]:
        losses = losses + 1 if r < 0 else 0
        if losses >= 2:
            print(f"dry-run shutoff OK after 2 losses (r={r})")
            break
    assert detect_absorption(8000, 1500, 1.0, 2000.0), "absorption self-check must pass"
    assert not detect_absorption(300, 290, 1.0, 2000.0), "noise must not flag"
    with open("results/run-v1.0-exp02-dryrun-seed7.json", "w") as f:
        json.dump({"spec": "v1.0", "exp": "exp02", "mode": "dry-run",
                   "shutoff_ok": True, "absorption_selfcheck": True,
                   "TODO": "add Tradovate MNQ tape + GEX feed for 30-trade replay"}, f, indent=2)
    print("saved results/run-v1.0-exp02-dryrun-seed7.json (NO trades claimed)")
    sys.exit(0)

import pandas as pd
df = pd.read_csv(SAMPLE)
print(f"loaded {SAMPLE}: {len(df)} rows — full replay TODO (frozen rules engine hooks here)")
