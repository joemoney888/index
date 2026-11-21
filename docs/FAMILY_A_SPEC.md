# Family A - frozen specification v1 (21 Nov 2026) - NOT RUN YET
Status: written down BEFORE any data for these hypotheses has been looked at. Runs only after (1) Monday housekeeping (ledger audit, stop_1min fix, first trade_closed reconciliation) and (2) GLM's sign-off or Joe's "run". Any change after this point is logged here with the reason and counts as a new spec.
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
