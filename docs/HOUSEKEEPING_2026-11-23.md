# Monday housekeeping, 23 Nov 2026 (Claude Sonnet 5.5)

## 1. Both agents running
Both repos' workflows ran every 5 minutes through the weekend and this morning, all green (checked 09:19 UTC). BFG has made no new trades since Friday: the US cash session had not opened yet.

## 2. Bug found and fixed: closed trades were never logged
`log_closed_trades` filtered with a plain substring test on the raw CSV text, but the details column stores JSON with doubled quotes, so the test never matched and no `trade_closed` event was ever written. The unit test used a hand-written unquoted file, so it passed. Fixed in commit 2cdc942 (CSV parsed properly) and the test now uses the real logger (it fails on the old code). First run after the fix (09:21 UTC) logged the 8 closed trades.

## 3. Reconciliation of the first 8 closed trades (all shorts, 19-20 Nov)
- Result: 5 take-profits (+1.26R to +1.33R), 2 stops (-0.99R, -1.01R), 1 trailed stop (+0.23R). Total about +4.6R, +GBP 21.11 (financing 0 for all). That was the day the index fell 5.6%, so this is not evidence of an edge.
- Entries and exits are consistent with the plan: take-profit fills sit at or inside the target, stop fills 0.4 to 1.9 points beyond the stop.
- `realized_pl` is in GBP: for example trade 42 earned USD 7.99 on its price move and OANDA reports GBP 6.04.
- Found: the USD-to-GBP conversion differs for gains and losses (implied rates about 1.324 for gains and 1.298 for losses). If that is a conversion markup it costs roughly 1% of each P&L move, about 0.01R per trade. Small, systematic, and consistent with the realistic-fill drag already measured. Not independently confirmed with OANDA's own statement (I have no account access).
- Compounding sizing (INDEX_COMPOUND) is now safe to switch on from a data standpoint; it is OFF until Joe says so.

## 4. ftmo/stop_1min.py time-exit fix (GLM nit (a))
Done: the 1-minute exit window now ends after the H-th 5-minute bar, as in the engine, not at entry time plus H x 300 seconds. Re-run: the same results as before at the recorded precision (5-minute update -0.007R t -0.78; 1-minute update -0.002R t -0.27; no trailing stop -0.023R t -0.88). Conclusion unchanged. Details in ftmo/RESULT.md (addendum). Nit (b) remains open.

## 5. Ledger audit (independent recount from the run files)
| Source | Variants |
|---|---|
| Private repo ledgers (11 markets, gold, scalp, runs) | 760,493 |
| Public repo run files excluding calibration (PATTERNS 21,684; PATTERNS_CYCLE 2,201; PATTERNS_GEO 112,307; SPREAD 9,566; SPX500 35,116; TREND 2,000; EXITS 175) | 183,049 |
| Sum | 943,542 |
| Documented cumulative N | 941,542 |
| Difference | 2,000 (equal to the TREND run) |
Calibration runs (666,540 variants on shuffled data) are correctly excluded: they are not looks at real returns. The documented N therefore looks low by 2,000 (0.2%) if the TREND run was not included. Effect on the luck bar: sqrt(2 ln N) + 0.5 = 5.7450 for 941,542 and 5.7455 for 943,542, no practical difference. Recommendation: keep 941,542 as the recorded N, add a note that a recount gives 943,542, and use 943,542 if Joe wants the conservative figure; Family A's pre-created N would then be 943,545. I could not re-derive the intermediate groups (115,348; 669,283) without their original definition; only the total was reconciled.

## 6. Data gaps in OANDA bars (counts and dates only, no returns)
- 11 markets: no run of 12 or more consecutive fully flat 5-minute bars anywhere.
- NAS100, SPX500, US30 (5.5 years): apart from the normal daily break, weekends and holidays, only these unusual in-day gaps: 2022-05-04 (bars missing around 18:35, 19:20 and 22:00 UTC and the few bars present flat at 12,950.0 for about 1.5 hours, around the FOMC announcement, while an independent file moves about 3%), 2022-05-12 (2.8 h from 05:15 UTC), 2026-02-04 (2 h from 21:00 UTC); plus 31 Dec 2024 and 2025 (25 h, New Year's Day closure not on the holiday list as a Dec 31 start).
- Effect: about 3 days out of about 1,400. The Family A coverage test (fewer than 78 bars from 09:30 to 16:00 New York) would skip 2022-05-04 automatically; list the three dates as known data-gap days in the pre-run report.
- Correction to an earlier note: the 2022-05-04 problem is mostly missing bars plus frozen prices, not a long run of flat bars.
