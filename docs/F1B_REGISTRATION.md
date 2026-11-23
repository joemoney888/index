# F1b: a properly powered look at the pre-FOMC drift (registered 23 Nov 2026, Claude Sonnet 5.5; NOT RUN: waits for data)
Cap lifted by Joe (project manager) at 09:51 UTC, 23 Nov 2026 ("lift the cap and register a new, properly powered look at it"). N: 941,548 + 1 = **941,549** pre-created here. Further N is not capped by this decision but each new test still needs its own registration.

## Why a new look needs NEW data
F1 passed on 2021-2026 (+45 bp, t 2.95) and failed its replication on 2016-2021 (+18 bp, t 1.27). Both windows have now been seen, so pooling them is not a new test. Genuinely unseen data is: (1) 2010 to 2016-11 (about 44 scheduled FOMC decisions), and (2) every decision from 9 Dec 2026 onward (8 a year).

## Power, stated before any further look (SD of one F1 event = 100 bp, from the 43 events; effect sizes are what we could be chasing)
| True effect | events for 80% power at t >= 2.0 | years of FOMC meetings |
|---|---|---|
| 45 bp (the 2021-2026 estimate) | 40 | 5 |
| 30 bp | 90 | 11 |
| 18 bp (the 2016-2021 estimate) | 249 | 31 |
| 10 bp | 808 | 101 |
Honest consequence: 2010-2016 alone (about 44 events) can only confirm an effect near 45 bp; it cannot rule out 18 bp. A "properly powered" test of a modest effect would need about 250 events (31 years), which no 5-minute data we can get covers. A daily-close version of the same idea (previous close or 14:00 to the decision) could use decades of free daily data, but is a different trade (the timestamp 14:00 to 14:00 is lost) and would be a separate registration.

## Rule (frozen now, applied once)
Trade identical to F1: long NAS100 (or the nearest index future or ETF in the vendor data if NAS100 is unavailable, ONE instrument stated before the run) at the open of the 14:00 New York bar on the previous trading day, exit at the close of the 13:55 bar on the decision day. Events: scheduled FOMC decision days only; unscheduled meetings excluded; March 2020 not in this window. Costs: the vendor's quoted bid/ask if present, otherwise the F1 median half-spread of 0.19 bp per leg x1.5 (index futures spreads are about 0.25 index points). Pass on the NEW pool: net mean >= +15 bp AND t >= 2.0 AND positive in at least 2 of 3 equal-count thirds. Pooling with 2016-2021 or 2021-2026 is NOT part of the rule. Result recorded either way.
Meaning of outcomes: pass = F1 survives three windows (two consistent, one weaker): worth a cautious forward paper test; fail = closed as "not detectable at this scale". The forward events (from 9 Dec 2026) are logged as they come but are not tested until at least 40 exist (about 5 years); they are not a project deliverable by 19 Dec.

## What is needed from Joe (decision, not purchase by Claude)
Pre-2016 intraday data needs a source. Options: Databento (NQ or ES futures, 1-minute or 5-minute, 2010 onward; paid, he decides and buys, I never take keys); FirstRate or Kibot (already identified; raw data must stay out of the public repo). Until data exists, F1b stays NOT RUN and the family stands at "promising, unconfirmed".
