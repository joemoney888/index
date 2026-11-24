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

---
# Addendum v1.1 (24 Nov 2026, registered before running): D1b and D3 on the official S&P 500 series
Data: Cboe/official S&P 500 daily close, 1975-01-02 to 2026-11-20 (file stored outside the repo), price index (no dividends; about 0.7 bp/day understated, same for all days). Release dates: ALFRED lists for CPI (release 10), Employment Situation (50), Advance Retail Sales (9), supplied by Joe. N: 941,553 -> 941,555 (+2: D1b, D3). One run each.
ALFRED caveat (from GPT6, confirmed in the files): some dates are weekends or provider dates. Frozen cleaning: drop duplicate and weekend dates and any date that is not an S&P 500 trading day; count them; a day with several releases counts once; only dates 1975-01-02 or later.

## D1b: turn-of-month, same rule as D1 on the official series
Identical to D1 (last trading day of the month plus the first 3 of the next, four daily returns summed, 2 bp round trip, NW 1 lag, pass t >= 2.8, mean >= +4 bp per block, >= 2 of 3 equal-count thirds positive). Window 1975-01-02..2026-11-20. Overlaps D1 on 1993-2024; the 1975-92 and 2024-26 days are unseen. Descriptive only: the same rule on 1975-92 alone and on 1993-2026.

## D3: announcement-day premium (GLM B2; Savor and Wilson, JFQA 2013)
Event days: any day with a CPI, jobs-report or retail-sales release (cleaned list above). Trade: long the S&P 500 from the previous trading day's close to the announcement day's close, 3 bp round-trip cost. Statistic: mean net return over event days, NW 1 lag. Pass (all): t >= 2.8; mean net >= +3 bp per event day; net mean > 0 in >= 2 of 3 equal-count thirds. Opposite t <= -2.8 recorded only. FOMC days are excluded because I have no verified dates before 2005. Descriptive only: mean gross return on non-event days; event minus non-event gap.
Frozen. Nothing tuned after results.
