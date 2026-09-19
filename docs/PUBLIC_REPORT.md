# PUBLIC REPORT — template (fill only from frozen-spec runs, never edit SPEC to fit results)

> Status 2026-09-19: FULL PUBLIC RUN — 7 exps, seed 7. Public 5m NQ (n=950 RTH) + purged WFA + MC + DSR/RC/SPA/PBO.
> Verdict: REJECT as edge (deflated + bootstrap CI fail); WFA procedure 3/4 pass (stable but insignificant).

## Verdict: REJECT (public-bar edge) / HOLD (program)

| Market / session | n | PF net | Expect/R | MaxDD_R | PBO | DSR | Gate |
|---|---|---|---|---|---|---|---|
| Synthetic auction (exp00) | 1 | 0.0 | −0.61 | 0.0 | 0.61* | 0.0* | PIPELINE ONLY |
| NQ=F daily proxy (exp01) | 3 | 2.03 | +0.50 | 1.0 | 0.61* | 0.0* | SMALL-n MIRAGE |
| Replay/paper harness (exp02 dry-run) | 0 | — | — | — | — | — | TODO 30 trades / 30d tape |
| Synthetic raw A vs filtered B (exp03) | 17→11 | 0.38→0.72 | −0.46→−0.16 | 9.1→3.5 | 0.61* | 0.0* | FAIL, filters cut DD −62% |
| **Public 5m NQ RTH (exp04)** | **22 (78 hits, 40 blocked)** | **2.39 base / 2.35 ×2** | **+0.47** | **4.0** | — | — | **ISOLATED profit, needs deflation → see exp05** |
| **Benchmark field (exp05, same 950 bars)** | — | — | — | — | **0.33 lite** | **0.62 (<0.95 FAIL)** | **RC 0.87 / SPA 0.79 FAIL vs buy-hold (buy-hold Sharpe 4.64 > creamer 3.06)** |
| **Purged WFA (exp07, 4 folds, purge2/embargo2)** | **22 (7/5/5/5)** | **1.43/inf/0.44/7.63** | **+0.07/+1.48/−0.50/+0.99** | **4/0/3/1** | — | — | **3/4 PASS, 0 VETO → WFA_PASS True (fold2 FAILs; fold1 5/5 luck)** |
| **Stitched OOS + bootstrap (exp07)** | 22 | 2.41 | +0.47 | 4.0 | — | — | **per-trade Sharpe 0.39, t 1.81, 95% CI [−0.08, 1.08] includes 0 → insignificant** |
| **MC shuffle (exp07)** | — | — | — | — | — | — | **P=1.0 DEGENERATE (shuffle-invariant totals, DaruFinance #1) — not evidence** |

\* PBO/DSR stubs fail closed on small-n (see `src/overfit.py`) — real CSCV/DSR TODO with trial matrix.

## What was tested (frozen v1.0)

- Environment: HTF value-up/down/sideways + GEX regime stub (positive=choppy filter, negative=allow).
- Location: outside VA + discount + fib 705/788/886 + swing/sweep + 886 invalidation.
- Confirmation: absorption (2× per-level size + cross-ratio + wick) + bullish close + 2nd fail higher + flip + ask imbalance.
- Execution: stop beyond 2nd fail, targets swing/POC/VAH, trail on buyer progression, BE on VA-reclaim fail.
- Filters: 20k MNQ/5m, 90-min window, max 2 losses shutoff, news skip.

## Costs (contract-correct intent, proxy·honest)

- Next-open fills, stop-first, 1-tick slip minimum + commission + spread. Report gross AND net.
- Full tick + Tradovate MNQ tape + Tanuki/chain GEX still TODO (paid). Current numbers are pipeline checks, not edge proof.

## Negative results preserved

- `results/REJECTED-*` (none yet — add, never delete).

## How to reproduce

See `docs/REPRODUCIBILITY.md`. Seed 7 everywhere. `pip install -r requirements.txt` then
`python3 src/exp00_synthetic.py && python3 src/exp01_historical.py`.

## Next gates (in order)

1. 1m NQ 2022–26 + 2026 holdout, tick-aware fills, 25k Monte Carlo, WFA.
2. 30d/30-trade replay with frozen-spec adherence ≥85%.
3. 90d/60–100 micro paper within ±0.1R, DD within 1.25×.
4. Only then consider staged sizing. No shortcuts.
