# Daily-data tests: frozen spec v1.0 (registered 23 Nov 2026, before any return is computed)

Data: SPY daily, 1993-01-29 to 2024-04-15 (Kaggle file, stored outside the repo), adjusted_close used for returns. ETF, no spread column: flat 1 bp per leg charged on every entry and exit. Time order only; no future data in any signal.
N: 941,551 -> 941,553 (+2: D1 and D2). Whole sample, one run each, no sealed split (too few months/regime changes to split; honest low power noted). Thirds are equal-count, chronological.

## D1: turn-of-month long (GLM B1, Claude idea; Lakonishok & Smidt 1988)
- Each calendar month M: long at the close of the second-to-last trading day of M, exit at the close of the 3rd trading day of M+1. One observation per month = sum of the four daily adjusted-close returns, minus 2 bp round trip.
- Pass (all): Newey-West (1 lag) t >= 2.8; mean net >= +4 bp per month-block; net mean > 0 in >= 2 of 3 thirds. Opposite t <= -2.8 recorded only.
- Expected power: ~375 blocks, SD ~240 bp -> detectable ~35 bp per block (~8.7 bp/day). Low; a clean "not there" is the likely honest outcome.

## D2: 200-day trend filter (Idea 10)
- Signal at the close of day t-1: adjusted close above its 200-day simple average. Day-t return is "in" if the signal was above, "out" otherwise (no look-ahead).
- Statistic: mean daily return of "in" days minus "out" days (regression on an in/out dummy, Newey-West 5 lags), after charging 1 bp per leg on each switch, spread over the switch day.
- Pass (all): t >= 2.8 for in-minus-out; difference >= +3 bp/day net; difference > 0 in >= 2 of 3 thirds.
- Descriptive only, no N: CAGR, max drawdown and Sharpe of trend-filtered vs buy-and-hold; the same with 10% volatility-targeted sizing (Idea 12, 20-day realised vol).

Frozen. Nothing tuned after results. Each runs once.
