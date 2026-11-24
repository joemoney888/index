# Round 3 prompt for GPT6 and GLM (24 Nov 2026). Send the text in the code block.

```
Round 3. Paper-trading research project, demo accounts only. Nothing here justifies real money; a clean "not there" is a valid result. Please do not suggest or encourage betting of any kind. Never send or ask for API keys or tokens.

WHAT HAS BEEN TESTED SINCE YOUR LAST ROUND (N is the running count of tests: now 941,553)
- Europe-open window (long NAS100 23:30-03:30 New York, 2021-26, own spreads): gross +0.9 bp, net -0.25 bp, t -0.31. FAIL.
- Turn-of-month long (SPY daily 1993-2024, 374 monthly blocks): net +29 bp per block, t 2.70 against a frozen 2.8. FAIL, near miss; effect shrinks by third (+43, +28, +17 bp). Followed forward only.
- 200-day trend filter (same data): in-minus-out +0.09 bp per day, t 0.02. FAIL as an edge. Descriptively it cut the worst drawdown from -55% to -24%.
- Earlier closed: Family A, opening-range breakout, F2, harmonic and Elliott families (112,307 variants, none passed), pre-FOMC drift (passed discovery, failed replication; forward log running).

WHAT IS MISSING (please help if you can browse; say which items you verified and which are from memory)
1. A dated list of US release days since 1993: CPI, Employment Situation (jobs report), Advance Retail Sales, as CSV (date, release, source URL). Mark any date you are not sure of. I cannot reach FRED/ALFRED pages from my workspace.
2. The exact free download page for Cboe BXM and PUT index history (and any free daily CLL/PPUT series), or another free source with daily values since 1990 or earlier.
3. Any other free source for: daily S&P 500 / Nasdaq-100 since 1990 to the present (my files stop in April 2024), and any timestamped, free news or filing feed (SEC EDGAR 8-K times, FOMC statement times, economic-calendar history) that could be used for a log-only news flag.

TWO NEW IDEAS FROM THE PROJECT MANAGER (comment on each: prior, data needed, how you would test it honestly, N cost)
- Idea 17: a scored news feed (pre-market, open, close) to steer a mean-reversion fade agent that lost on 23 Nov when Nvidia news drove the Nasdaq up about 7%. We have no timestamped news history, so the plan is a forward, log-only record of big-gap or big-first-hour days. Is that the right design? What would you change?
- Idea 18: harmonic patterns (Gartley, Bat, Butterfly, Crab, Cypher, ABCD) in combination with another indicator. Standalone was tested (112,307 variants, 0 passed; best t 3.64 vs luck bar 5.32; Cypher K=6 a watch item only). Is there any published evidence that a combination does better than its parts, and what single pre-specified combination (if any) would you register?

THREE NEW IDEAS EACH
Give three new, testable ideas not on the tested or closed lists above, each with: the rule in one line; a published source (mark verified vs memory); the data it needs and whether it is free; the number of tests or events and the smallest effect detectable at t 2.8; N cost; and your honest prior of passing. Say which you would test first and why. Prefer ideas that can be tested on data we can get free, and that would still matter after real costs.

Format: numbered answers matching the sections above; keep it short; mark estimates "(est.)".
```
