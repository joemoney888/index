# Family A: older data (23 Nov 2026). DECIDED by Joe (project manager) at 09:32 UTC: OPTION A. Spec v1.1 stays frozen and unchanged.

## What changed
Joe found a free NAS100 5-minute CFD history (Kaggle, 15 Nov 2016 to 1 Oct 2025, same type of broker data as our OANDA feed). It is held in the PRIVATE repo only (research use; the prices are broker prices). Checks done (data quality only, no strategy returns): no duplicate timestamps; normal weekend/daily gaps; on the 2021-06 to 2025-09 overlap its 5-minute returns correlate 0.997 (median month) with our OANDA bars and prices agree within 0.07%. The raw timestamps are broker server time = Europe/Athens (UTC+2 winter, UTC+3 with EU daylight saving), converted to UTC. One month (2022-05) correlated 0.85 because OUR OANDA bars on 2022-05-04 are mostly missing between 18:35 and 22:00 UTC, with the few bars present frozen at 12,950.0 (a feed freeze around the FOMC announcement; the new file moves about 3% there). A full scan of our bars (docs/HOUSEKEEPING_2026-11-23.md) found only 3 such days in 5.5 years (2022-05-04, 2022-05-12, 2026-02-04) and no long flat runs anywhere.
Search history: all 941,542 trials used OANDA data from 2021-05-19 onward. To Claude's knowledge nothing before that date has been looked at, so 2016-11-15 to 2021-05-18 (about 1,100 trading days) is a clean, untouched window. It is SEALED: coverage and cost checks only until a reviewed pre-registration says otherwise.

## Options for Family A (reviewers to comment; Joe decides)
A. Keep v1.1 as frozen. Run once on 2021-05-20 to 2026-11-17. Only if a spec passes, run that SAME spec once on the sealed window as a replication (pre-registered now: pass = same sign, t at least 2.0, net mean at least +0.5 bp). Costs nothing extra in power for the main test (detectable about 1.9 bp, estimate). A pass would then carry an independent confirmation.
B. Pool both windows (about 2,450 usable days, estimate). Detectable mean at t 2.8 and SD 25 bp (estimate) = 2.8 x 25 / sqrt(2450) = about 1.4 bp. Better power, but no untouched confirmation window is left and the older window needs a frozen cost assumption.
Claude Sonnet 5.5 leaning: A. A replication on untouched data is worth more than 0.5 bp of extra detectability, and it keeps v1.1 unchanged. Reviewers may disagree.

## Things that must be frozen BEFORE any look at either option
1. Spreads before 2021 are unknown (the file has no spread column). Proposed assumption: use the 2021+ median half-spread for each 5-minute slot; also report a x1.5 sensitivity. Reviewers: is that acceptable?
2. Calendar: famA/calendar.json covers 2021-2026 only. A 2016-11 to 2021-05 list of NYSE full holidays and early closes must be written from the official NYSE calendar and verified, not from memory.
3. Timezone rule: Europe/Athens server time to UTC (unit test on known dates in March, late October and early November).
4. Third boundaries for the sealed window if option B is chosen.
5. N accounting: same specs on new data. Proposal: N +0 for new specs, but record the replication as a second look at the same three hypotheses; GLM and ChatGPT 6 to say whether it should count as +3.
6. Added coverage-only pre-run check for BOTH feeds: scan for flat/stale stretches (for example identical closes for 12 or more consecutive bars) by dates and counts only; decide in writing how a stale stretch is treated (skip the day) before looking at returns.

## Not changed
Decision rule (|t| at least 2.8 in the claimed direction, net mean at least +1.0 bp, positive in at least 2 of 3 thirds), the three specs, run once, write-up due 2026-12-19.

## Questions for reviewers (answer briefly, each with a reason)
1. A or B?
2. Is the pre-2021 spread assumption acceptable, or should the older window be restricted to a cost-free gross check?
3. Should the replication count as N +3?
4. Anything in the data-quality evidence above that you would check differently?


## DECISION RECORD (Joe, 23 Nov 2026, 09:32 UTC)
- Option A adopted: run frozen v1.1 once on 2021-05-20 to 2026-11-17. Only if a spec passes its registered rule, replicate that same spec ONCE on the sealed window 2016-11-15 to 2021-05-18. Replication pass rule (pre-registered now): same sign, |t| at least 2.0, net mean at least +0.5 bp. A failed replication means that spec is not confirmed.
- Operating decisions taken by Claude Sonnet 5.5 as defaults inside Joe's decision (Joe may overrule): (1) pre-2021 spreads = the 2021+ median half-spread per 5-minute slot, with a x1.5 sensitivity report; (2) trial count: N is pre-created at +3 for the main run as planned; if the replication is run it is recorded as a second look at the same three hypotheses (+0 new specs, noted separately) and not as +3 new specs; (3) the 2016-2021 calendar of holidays and early closes is written from the official NYSE source before the replication, not from memory.
- Governance: Joe decides as project manager; the reviewers (GLM, ChatGPT 6) and Claude Sonnet 5.5 advise. Reviewer input is requested where Joe asks for it; otherwise Claude Sonnet 5.5 proceeds with the default and records it.
