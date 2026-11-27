# Ideas round 1 - Claude's own proposals (committed BEFORE reading any reviewer's proposals; 22 Nov 2026)
Same rules and rubric as the other participants (see docs/IDEAS_ROUND_1.md). Sources are cited from memory and MUST be verified by the scorer before credit is given. N cap context: Family A uses +3 of the +6 further N, so at most +3 remain unless the PM raises the cap. Nothing here is run until signed off.

## C1. Overnight versus intraday drift on NAS100 (Kelly and Clark 2011, "Returns in trading versus non-trading hours: the difference is day and night", Journal of Investing / related literature)
Rule: long NAS100 CFD from the 16:00 New York close bar to the 09:30 New York open bar, one trade per night, skip weekends' rollovers handled as one trade Friday-Monday, no stop. Net of half-spread on both bars and the logged overnight financing.
Mechanism: published claim that most of the equity premium accrues outside the cash session (inventory and risk-premium effects around the close). Power: about 1,400 nights, overnight SD about 60 bp, SE about 1.6 bp, detectable at t 2.8 about 4.5 bp; costs about 2-3 bp, so the bar is net +1 bp. Prior of passing about 5%. Kill rule: net mean below +1.0 bp or t below 2.8 or positive in fewer than 2 of 3 thirds. N cost +1.

## C2. Pre-FOMC announcement drift (Lucca and Moench 2015, "The Pre-FOMC Announcement Drift", Journal of Finance)
Rule: long NAS100 from 24 hours before the scheduled FOMC statement time to 5 minutes before it; exit before the announcement. Scheduled meetings only. Science-only (FTMO forbids entries within 2 hours of Fed decisions).
Mechanism: published abnormal return in the 24 hours before scheduled FOMC announcements (an average of about 49 bp in 1994-2011; later literature reports it weakened). Power: about 40 meetings in our window, event SD about 80 bp, SE about 12 bp, so only an effect of about 30 bp or more is detectable. Prior about 10% that anything survives. Kill rule: t below 2.8 or net mean below +10 bp. N cost +1 (counted in the backlog already as part of the Fed family).

## C3. Turn-of-the-month (Lakonishok and Smidt 1988, "Are seasonal anomalies real?", Review of Financial Studies)
Rule: long NAS100 from the 15:55 bar of the last trading day before month-end to the close of the third trading day of the new month; one trade per month. Net of costs.
Mechanism: published concentration of returns around month turn (flows, payroll investment). Power: about 66 months, event SD about 250 bp, SE about 31 bp; detectable only at about 85 bp or more. Underpowered by design; a pass would need an effect far above what the literature reports. Prior 3%. Kill rule: t below 2.8 or net mean below +20 bp. N cost +1. Recommendation: probably NOT worth an N; submitted because it is the cheapest to state, and to show the cost of weak power.

## ERRATA (22 Nov, after checking sources; sealed text above left as committed)
C1's source: Kelly and Clark (2011) was published in the Journal of Asset Management 12(2), not "Journal of Investing" as written above (venue misdescribed by Claude; the paper, authors, title and year are right). Lou, Polk and Skouras, "A Tug of War: Overnight versus Intraday Expected Returns", JFE 2019, is the stronger source for the overnight idea (raised by GLM).
