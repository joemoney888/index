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

## RESULT (run once, 23 Nov 2026; SPY 1993-01-29 to 2024-04-15)
**D1 turn-of-month: FAIL (near miss, closed).** 374 monthly blocks, net +29.2 bp per block, NW t 2.70 (needs 2.8). Floor (+4 bp) passed; thirds +42.6 / +27.6 / +17.3 bp all positive but shrinking each period. Fails rule A by 0.10 in t. The frozen rule is not relaxed after the result. Opposite direction: no.
**D2 200-day trend: FAIL, no edge in returns (closed).** In-minus-out +0.09 bp/day, t 0.02; thirds +4.6 / -2.4 / -3.5 bp. Descriptive only (not tested): trend filter CAGR 8.4% vs buy-and-hold 10.2%, max drawdown -24% vs -55%, Sharpe 0.72 vs 0.61. 10% vol-target (always in, capped at 1x): CAGR 7.2%, max drawdown -34%, Sharpe 0.73. A drawdown/risk control, not a return edge.
Caveats: SPY ETF with assumed flat 1 bp per leg, no CFD financing; data ends Apr 2024.

## DATA-QUALITY NOTE (24 Nov 2026, added after the results; the results above are NOT changed)
Joe supplied the official S&P 500 daily closes (1975-01-02 to 2026-11-20) and FRED Nasdaq-100 (1986-2026). Comparing them with the SPY file used for D1/D2: daily returns disagree by more than 0.5% on 333 of 7,856 common days (for example 2000-01-07: SPX +2.7%, SPY file +5.8%; 2008-10-13: +11.6% vs +14.5%), correlation 0.98 instead of about 0.99+. The SPY file has bad closes on some days, so the D1 near miss (t 2.70) and the D2 null are on flawed data. The frozen D1/D2 results stand as recorded. Any re-run on the official series is a new registration (N +1 each) and must be declared as overlapping; it would also add 1975-92 (unseen) and 2024-26 (unseen) data.
