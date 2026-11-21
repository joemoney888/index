# Ideas and checks for an independent reviewer to validate (20 Nov 2026)
Context: see `docs/HANDOVER.md` (sections 10-12). BFG's edge disappeared under realistic exit fills; exits that keep the old fitted stop/target/horizon show no edge under realistic fills; whether the entry carries any drift with NO exits was open until test B.1 (see ftmo/RESULT.md, 21 Nov). Everything below is falsifiable and cheap. Each idea counts toward the global variant total (941,542 so far). Pre-register thresholds BEFORE looking at results; keep a locked final-365-day exam.

## A. Validate our own correction (highest value)
1. Independently re-implement the exit simulation on 1-minute NAS100 bars (`ftmo/stop_1min.py`, `search/exits_realistic.py`): bid/ask-aware fills, stop filled at the minute's open when it opens beyond the stop, stop wins ties. Do you get mean R about -0.01 to 0 for BFG? Is any fill rule too pessimistic (e.g. should a resting stop fill at the stop price inside a gapless minute)?
2. Audit the cumulative variant count (941,542): which ledgers double count? Which choice of N is the defensible one for a luck bar?
3. Confirm or refute the FTMO clause reading in the handover (esp. 13.2.4, 16.3, the "software/AI" clause, gap/news rules).

## B. New falsifiable ideas (none tested yet)
1. **Signal quality with no exits at all.** Mean forward return (net of spread) at +5, +15, +30, +60, +120 minutes after each BFG signal (sign-adjusted), on 1-minute data, day-clustered t. If there is no drift at any horizon the entry is noise. Prior: no edge.
2. **Overnight vs intraday drift on NAS100/SPX500.** Long close-to-open vs open-to-close, net of CFD financing (about 6.5% a year long) and spread. A well-known anomaly; test whether any survives CFD costs. Prior: costs eat it.
3. **Post-event drift.** Mean return in the 1-4 hours after FOMC and jobs-report releases (dates already in `ftmo/ftmo_filters.py`) versus matched ordinary days. FTMO forbids opening trades inside the blackout; this asks whether a compliant version could trade just after it.
4. **Opening-range breakout versus fade (US cash open 14:30/13:30 UTC)** with realistic fills, 1-minute data, one hypothesis with 3 parameters at most. The old Blue Falcon agent was an ORB; its record is in the private repo.
5. **Stock-level idea tied to the owner's own history:** position sizing after earnings gaps using daily bars (Databento, small cost). Question: does adding to a falling large-cap after earnings ever beat holding, after costs? Prior: no.
6. **Seasonality (turn of month, pre-holiday) on daily NAS100** with a power calculation first; with about 5.5 years of data, only large effects are detectable.

## C. Method improvements worth reviewing
- Block-bootstrap or Newey-West standard errors on day-clustered trade series instead of the heuristic cluster formula.
- A cheap permutation test of the entry signal: shuffle signal timestamps within the same days and compare the realised forward-return statistic.
- Walk-forward evaluation of the exit family (fit on year 1, test year 2, ...), with realistic fills.
- Kill criteria for the live test: stop if the average live R is below -0.05R after 75 trades; otherwise judge on logged exit-fill slippage (now being logged as `trade_closed` events), not on the t-stat (about 850 trades would be needed to resolve +0.05R).
