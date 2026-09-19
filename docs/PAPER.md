# PAPER outline — from replication to decision (fill as gates clear)

1. Question: does the transcript-frozen 4-step (GEX regime → VA+fib discount → footprint absorb+flip → 1.5–2R)
   survive point-in-time, contract-correct costs, WFA, and paper — or fail like most retail systems?
2. Related: Steidlmayer AMT (1985/86), Pardo WFA (1992), Bailey–López de Prado PBO/DSR, prop trailing-DD math,
   0DTE/settled-vs-flow GEX literature (2024–26 vendor docs in SOURCES).
3. Method: SPEC v1.0 frozen; exp00 pipeline proof → exp01 proxy arithmetic → exp02 tape replay → exp03 filtered;
   next_open + stop-first + 1-tick slip; WFA 70/30 stepped; CSCV-PBO + DSR + Kupiec/Christoffersen; cost ×1.5/×2.
4. Results: report PF net/gross, expectancy/R, maxDD, n, PBO, DSR, adherence, divergence — per regime
   (value-up/down/sideways × pos/neg gamma). Preserve negatives.
5. Decision: GO (advance under limits) / HOLD (missing evidence) / REJECT (≤0 net, costs eat edge, fills unavailable).
6. Threats: single-month championship regime, small-n, discretionary gaps (news/psych levels), stale GEX,
   MNQ-vs-NQ tape mismatch, yfinance proxy ≠ futures tape.
7. Artifacts: SPEC, code, seeds, caches, run JSONs, dashboard — all in-repo for independent rerun.
