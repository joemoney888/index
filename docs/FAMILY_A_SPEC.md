# Family A - frozen specification v1.1 (21 Nov 2026) - NOT RUN YET
Status: no prior evaluation of these rules exists; the same window has about 941k prior random-search looks (different rules, R-based, costed gates), a mild negative prior for LARGE effects only and no bearing on the 1-3 bp effects those gates could not detect. Runs only after (1) Monday housekeeping (ledger audit, stop_1min fix, first trade_closed reconciliation) and (2) GLM's sign-off or Joe's "run". Any change after this point is logged here with the reason and counts as a new spec.
Family N cost: +3 (specs A5, A6a, A6b). Decision rule is shared and pooled (a deliberate, flagged deviation from the locked-exam discipline: these are fully frozen replications of claimed or published effects, nothing is estimated or tuned, and the window 2021-11 to 2026-11 post-dates the 2018 paper; the report must say so).

## Common design
- Instrument: NAS100 CFD, 5-minute bars (agent data, Nov 2021 to Nov 2026), about 1,300 days.
- Clock: America/New_York via zoneinfo for every session time (daylight saving handled by the library, never by fixed UTC offsets). London times via Europe/London.
- One position per day per spec. Entry = open of the named bar +/- half that bar's spread (adverse side). Exit = close of the named bar -/+ half that bar's spread (adverse side). No stop, no target, no financing (intraday).
- A day is skipped if any bar needed by the spec is missing, or on US early-close days (any day with fewer than 78 five-minute bars between 09:30 and 16:00 New York). Report counts of days used and skipped per spec.
- Metric: net return per trade in basis points (no R: there is no stop). Test: t-statistic with Newey-West standard error (5 lags) on the daily series.
- Decision rule (all three must hold): (a) |t| >= 2.8 in the CLAIMED direction (positive net mean for the traded rule); (b) net mean >= +1.0 bp per trade; (c) positive net mean in at least 2 of 3 calendar thirds (2021-11 to 2023-06, 2023-06 to 2025-02, 2025-02 to 2026-11). Otherwise the spec is closed in writing.
- A significant effect in the OPPOSITE direction is recorded as a separate finding. It is never traded, tuned or re-tested in this family; any follow-up needs its own registration and N.

## Spec A5 - London-to-New-York session reversal (two-sided test, traded in the claimed direction)
- London leg: open of the 08:00 London bar to the close of the 5-minute bar ending 09:15 New York (the last bar before the New York open window).
- Trade: opposite sign of the London return; enter at the open of the 09:30 New York bar; exit at the close of the 15:55-16:00 New York bar.
- No noise filter, no stop.

## Spec A6a - Intraday momentum, first half-hour -> last half-hour
- Predictor: return from the open of the 09:30 New York bar to the close of the 09:55 bar (the 09:30-10:00 half-hour). NOTE: this follows GLM's reading of the cited paper (Gao, Han, Li, Zhou, JFE 2018) and has NOT been verified against the paper text; the paper may include the overnight return. The overnight variant is not registered; any change is a new spec.
- Trade: the SAME sign, entered at the open of the 15:30 New York bar, exited at the close of the 15:55 bar (16:00 New York).

## Spec A6b - Intraday momentum, second-to-last half-hour -> last half-hour
- Predictor: return from the open of the 15:00 New York bar to the close of the 15:25 bar.
- Trade: same sign, same entry (15:30) and exit (16:00 close) as A6a.

## Reporting
Per spec: days used/skipped, mean net bp, t, per-third means, gross mean (before costs), the realised half-spreads used, and the final verdict against the rule. Joint report for the family. Backlog stopping rule: write-up of everything by 2026-12-19; total further N capped at +6 (this family +3, optionally idea 1 +1, optionally a Fed-announcement family +2).

## CHANGELOG v1 -> v1.1 (GLM round G sign-off, applied before any look at either variant; N stays +3)
1. A6a predictor changed to the paper's definition: the return from the PREVIOUS DAY'S CLOSE to the close of the 10:00 New York half-hour. Reason: the abstract of Gao, Han, Li and Zhou (JFE 2018) says the first half-hour return "as measured from the previous day's market close" predicts the last half-hour return (verified by Claude from the WUSTL publication page after GLM's correction; GLM's round-F reading of 09:30-10:00 was wrong and Claude's original draft was right). The 09:30-10:00 variant is considered at sign-off, discarded, and never to be run without a new registration.
2. Previous close = the close of the last 5-minute bar at or before 16:00 New York on the previous trading day (an early-close day anchors at its own last bar; Mondays anchor at Friday).
3. Calendar: full holidays and 13:00 early closes are skipped from the frozen list famA/calendar.json (written from the public NYSE calendar; to be checked against the official page before the run); the 78-bar test stays as the data-gap net.
4. Exact dates. The data runs from 2021-05-19 to 2026-11-18, so the sample is 2021-05-20 to 2026-11-17 (2026-11-18 is incomplete) and the earlier "Nov 2021 start" in v1 was wrong. Thirds: T1 2021-05-20 to 2023-03-31, T2 2023-04-03 to 2025-01-31, T3 2025-02-03 to 2026-11-17.
5. A5 direction table: London return > 0 -> SHORT at the 09:30 New York open; London return < 0 -> LONG.
6. Reporting: add per-third gross means and the correlation of the A6a and A6b daily return series; the CFD 16:00 close stands in for the paper's cash close.
7. Each bar pays its OWN half-spread at entry and at exit (the engine's signal-bar-spread-on-exit convention is NOT used).

## Final spec text for A6a (replaces the v1 text above)
- Predictor: return from the previous trading day's close (last 5-minute bar at or before 16:00 New York) to the close of the bar ending 10:00 New York (09:55-10:00). Trade: the SAME sign, enter at the open of the 15:30 New York bar, exit at the close of the 15:55-16:00 bar. Secondary paper result (overnight return predicting the morning) is NOT registered.

## Pre-run checklist (none looks at outcomes; items 2-6 touch bar existence, spreads and second moments only)
1. Ledger audit reconciled and N pre-created (941,542 -> 941,545) before the run. 2. Coverage report of 09:30-16:00 bars per day and the skip list (counts and dates only). 3. Early-close verification: on 3-4 calendar dates count the 13:00-16:00 bars (coverage only). 4. Spread sanity by half-hour slot including the 15:55 and 16:00 bars. 5. Optional, non-decisional: the SD of gross 15:30-16:00 daily returns, for the power statement only. 6. Timezone unit tests (09:30 NY = 14:30 UTC in January, 13:30 UTC in July; the bar closing at 16:00 NY exists on each sample day). 7. Freeze the runner (deterministic, committed), run ONCE, record per-spec verdicts against the frozen rule. Also check famA/calendar.json against the official NYSE page.
