# REPRODUCIBILITY — data contracts, seeds, costs, versioning

## Seeds & determinism

- Global seed: 7 (numpy + python random). No unseeded sampling in `src/`.
- yfinance proxy (exp01) caches to `data/cache/` with symbol+range in filename; reruns reuse cache.
- Every run writes `results/run-*.json` with: SPEC version, commit hash (if git), params, n, PF gross/net,
  expectancy/R, maxDD, costs, data window, rows skipped by filters + reasons.

## Data contracts

| Layer | Source | Granularity | Proves? |
|---|---|---|---|
| exp00 synthetic | `src` generator, seed 7 | 5-min OHLCV + synthetic bid/ask | Pipeline only (absorption detector fires, no edge claim) |
| exp01 proxy | yfinance `NQ=F` daily (fallback `QQQ`) | Daily | Structure/fib/location arithmetic only — CANNOT prove footprint/GEX |
| exp02 replay/paper | Tradovate MNQ tape (keys, paper=true) OR `data/sample_mnq_5m.csv` | 5-min bid×ask | Real test — TODO until keys + paid tape |
| GEX live | Tanuki/ZeroGEX/FlashAlpha feed (bring your own key) | Intraday flip/walls | Regime filter — TODO, stubbed as config flag in exp02/03 |

- Point-in-time: developing VA/POC stored at decision bar; never revised with future bars.
- Session: RTH NY 09:30–11:00 ET window for signals; ETH/RTH never mixed in one profile.
- Rows/ticks: profile row = 1 tick (MNQ 0.25); VA% = 70 (config, frozen).

## Costs (frozen)

- `COST_PER_SIDE_USD = commission + spread_cost + slip_ticks * tick_value`.
- Defaults (MNQ): tick $0.50, slip 1 tick/side, commission $0.60/side (configurable, reported).
- Sensitivity gate: rerun with ×1.5 and ×2.0 costs; PF must stay >1.0 net or verdict = FAIL.

## Versioning

- SPEC is append-only: `docs/SPEC.md` = v1.0. Edits → `docs/SPEC-v1.1.md` + new results prefix.
- `results/` filenames: `run-<spec>-<exp>-<YYYYMMDD>-<seed>.json`. Never overwrite.
- Public sharing: push this folder as its own repo; keep `.env`/keys out (see `.gitignore`).
