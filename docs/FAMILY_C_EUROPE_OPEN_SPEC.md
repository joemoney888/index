# Europe-open window: frozen spec v1.0 (registered 23 Nov 2026, before any return is computed)

Source: Bondarenko & Muravyev, JFQA 58(3) 2023 (window 23:30-03:30 New York; secondary figure ~3 bp/night gross, not verified by me). Proposed by GPT6, scored #1. Idea #5 (overnight vs intraday) is folded in, not registered separately.

N: 941,550 -> 941,551 (+1). The replication below is Option A and adds no N.

## Rule (frozen)
- Instrument NAS100 CFD, 5-minute bars of the agent data (bars5/NAS100.csv.gz), America/New_York via zoneinfo.
- Every evening D (Sun-Thu, any bar present): long at the OPEN of the 23:30 NY bar on D, exit at the CLOSE of the 03:25 NY bar on the next calendar day.
- Each leg pays its own bar's half-spread (spread/2), adverse side, as in Family A.
- Skip a window if the entry bar or exit bar is missing or fewer than 44 of 48 bars exist. No holiday calendar. Skips are counted and reported.
- Evenings 2021-05-20 to 2026-11-16.
- Financing: none charged; window starts after 17:00 NY rollover. Unverified against OANDA terms; reported as a caveat, not adjusted.

## Decision rule (same as Family A)
Pass only if all hold, claimed direction long: Newey-West (5 lags) t >= 2.8; mean net >= +1.0 bp; net mean > 0 in >= 2 of 3 equal-count thirds. Opposite-direction t <= -2.8 is recorded only, never traded.

## Replication (Option A, once, only if discovery passes)
Sealed window 2016-11-15..2021-05-18 on the Kaggle 5-minute file (no spread column): flat 0.56 bp per leg (the observed median in discovery data). Pass: same sign, t >= 2.0, net >= 0.5 bp.

## Descriptive only (not tested, no N)
Mean gross for the 23:30-03:30 window against the rest of the 24 hours, by third.

Frozen. No parameter is tuned after seeing results. Runs once.
