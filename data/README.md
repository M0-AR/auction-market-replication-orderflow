# data

- `sample_mnq_5m.csv` (optional, YOU provide): columns `ts,open,high,low,close,volume,bid,ask` — 5-min MNQ RTH.
  Keep ≤5k rows for git; larger tape stays local (`data/cache/`, git-ignored).
- `cache/` holds yfinance proxy downloads (symbol+range in filename, rerunnable offline).
- Never commit `.env`, keys, or full paid-tape dumps. See `docs/REPRODUCIBILITY.md`.
