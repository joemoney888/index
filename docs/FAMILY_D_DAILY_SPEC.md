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

## RESULTS of addendum v1.1 (run once, 24 Nov 2026; official S&P 500 1975-01-02 to 2026-11-20; N 941,555)
**D1b turn-of-month: PASSES the frozen rule, but is NOT established.** 622 blocks, net +35.6 bp per block, NW t 4.35; thirds +57.6 / +26.7 / +22.4 bp (all positive, shrinking). Descriptive split: 1975-92 (unseen by D1) n 215, +54.7 bp, t 4.05; 1993-2026 n 407, +25.5 bp, t 2.50 (below 2.8 on its own, consistent with D1's near miss).
Why not established (descriptive checks, not tests): (1) the rule tests against zero, and the market drifts up anyway: TOM days average +9.4 bp/day vs +2.9 bp on other days, excess +6.5 bp/day, Welch t 2.75. (2) The excess has decayed: 1975-89 +12.1 bp/day (t 3.09); 1990s +6.6 (t 1.43); 2000s +4.8 (t 0.69); 2010s +1.1 (t 0.23); 2020-26 +4.8 (t 0.66). (3) t 4.35 is below the project's luck bar at N 941,555 (about 5.75). (4) On a CFD, about three nights of financing (est. 5-6 bp per block) would be charged on top. Status: passes its frozen rule on a long history, the effect is mostly in 1975-89 and has largely faded; forward shadow only, no trading.
**D3 announcement-day premium: FAIL, closed.** 1,841 event days (2,577 raw dates; 13 weekend and 18 non-trading dates dropped). Gross +5.3 bp on event days vs +3.9 bp on other days (gap +1.3 bp; published 11.4 bp); net of 3 bp +2.3 bp, t 0.89; thirds +1.5 / +3.8 / +1.5 bp.

---
# Addendum v1.2 (24 Nov 2026 07:4x UTC, registered before any run, on Joe's "go"): D4 VIX panic-spike long and D5 option-expiration-week long
N: 941,555 -> 941,557 (+2). One run each, official S&P 500 daily close (1975-01-02 to 2026-11-20, closes only, so all returns are close-to-close) and Cboe VIX daily close (1990-01-02 to 2026-11-20). 3 bp round-trip cost charged per trade. Pass rule as D1: t >= 2.8, floor, >= 2 of 3 equal-count chronological thirds positive; opposite t <= -2.8 recorded, never traded.

## D4 (GLM N1; Kudryavtsev 2017 existence only)
Signal on day t (VIX and S&P both have a row): VIX close(t) >= 1.4 x median of the previous 10 VIX closes (t-10..t-1) AND VIX close(t) >= 20. Take the first signal; the next eligible signal is on or after the 10th session later. Long the S&P at close(t), exit at close(t+5 sessions). Signal dates 1990-01-02 .. 2026-11-13 only (later signals have unknown outcomes: the 20 Nov 2026 signal is forward, log only). NW 1 lag; floor net mean >= +30 bp per trade. Descriptive only: the unconditional mean 5-day return over all days (excess), and event counts and mean for sensitivities 1.35x/18 and 1.5x/25 (not decisive, not tested).
Expected: ~45 events, SD ~3%, detectable ~1.25% per event.

## D5 (GLM N3; Stivers and Sun, J. Banking and Finance 2013, existence only)
Each month 1975-01 .. 2026-11: exit day = third Friday (if not a trading day, the previous trading day); entry day = the second Friday (the Friday 7 days earlier; previous trading day if a holiday). Long the S&P at close(entry), exit at close(exit); about 5 sessions. NW 1 lag; floor net mean >= +25 bp per week. Descriptive only: mean of all rolling 5-session returns over the same period (excess).
Expected: ~623 weeks, SD ~2.2%, detectable ~25 bp per week.

## Not registered (decided before running): BFG gap-day diagnostic
On the data that can support a realistic-fill replay (NAS100 1-minute 2023-11-19 to 2026-11-19) only 21 days have |gap| >= 2% (59 at 1.5%; 131 at 1%). Detectable difference at t 2.8 with ~2R per-day SD is about 1.2R/day at 21 days, 0.7R/day at 59: it cannot answer the question, and N would be spent for a "can't tell". Counts only, no returns looked at. The gap flag stays a forward log (forward/daily_context.csv).
Frozen. Nothing tuned after results.
