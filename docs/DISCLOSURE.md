# DISCLOSURE — Hypothetical Performance, No Advice

> Required reading before any figure in this repo. Mirrors `trader-math-verify` disclosure posture.

1. **Not financial advice.** Educational replication of a public interview. No recommendation to trade,
   buy/sell any security, futures contract, option, or prop challenge.
2. **Hypothetical performance (CFTC 4.41 / SEC 206(4)-1 / FINRA 2210).** All backtests, synthetic
   experiments, and paper runs are hypothetical: prepared with hindsight, no financial risk, no slippage/
   liquidity/technology failures modeled beyond stated costs. Actual results will differ, often materially.
3. **Prop-firm conflict.** Prop challenges are marketed products with ~6% pass rates (2023 dataset via
   TradingView/FundedFast). Trailing drawdowns + daily loss limits punish variance. Past championship month
   ≠ future months. Fees are a cost whether you pass or not.
4. **Data limits (honest).** Free tiers (yfinance proxy, sample CSVs) CANNOT prove footprint absorption or
   dealer GEX — those need CME bid/ask tape (Tradovate/CQG/Kinetick) + paid options chain (CBOE/Tanuki/
   ZeroGEX/FlashAlpha). This repo marks every proxy as proxy.
5. **No cherry-picking.** All frozen-spec runs are reported win or lose. Abandoned variants stay in
   `results/` with REJECTED prefix. Cost sensitivity (+50–100%) is mandatory.
6. **Trademarks.** NQ/MNQ (CME), QQQ (Nasdaq), SPX/ES (S&P/CBOE), ATAS, NinjaTrader, Sierra Chart,
   TradingView, Tradovate, Tanuki Trade belong to their owners. No affiliation.
7. **Risk.** Futures are leveraged and can lose more than deposited. Do not trade money you cannot lose.
   If you forward-test, use demo/micro with predefined kill-switch (see SPEC §7).
