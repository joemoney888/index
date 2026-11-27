# Prompt for reviewers (GLM 5.3, ChatGPT 6) and for Claude Sonnet 5.5's own sealed answer: review the open ideas and propose 3 new ones each. Requested by the PM 23 Nov 2026 15:26 UTC. Unscored side round unless the PM says otherwise.
(The text in the code block below is the prompt as sent. Claude's own answer is committed only after the prompt is sent, per amendment (a).)

```
Context: a documented paper-trading experiment (demo accounts only, no real money, no manual trades; nothing justifies real money). Owner: the PM, a UK retail participant with a small account. Goal: find a trading rule with real, honestly tested evidence, or document a clean "not there"; both are valid results. Write-up is due 19 Dec 2026. The public repo is github.com/joemoney888/index (docs/IDEA_BACKLOG.md, docs/FAMILY_A_SPEC.md, docs/FAMILY_B_SPEC.md, docs/F1B_REGISTRATION.md, longterm/spec.md).

What has been tested (index CFD data, realistic spreads, frozen rules, run once, cumulative trial count N = 941,550, luck bar about 5.75):
- Session timing rules (London-to-New-York reversal; first-half-hour and 15:00-15:30 momentum predicting the last half-hour): all three failed.
- Opening-range breakout (NAS100, 2R target): t 2.45, closed (needed 2.8).
- Pre-FOMC drift: passed 2021-2026 (+45 bp, t 2.95), failed replication on 2016-2021 (+18 bp, t 1.27), and was negative on 2010-2016 free data; not established; now a paper-only forward log (40 events needed, about 2031).
- Post-announcement continuation: closed. Yearly trend rule vs buy-and-hold: failed.
- BFG index mean-reversion agent (live paper): no demonstrated edge after realistic fills (about -0.01R per trade).
Data we have: OANDA NAS100/SPX500/US30 5-minute with real spreads 2021-2026; Kaggle NAS100 5-minute 2016-2025 (no spreads); free OANDA 1-minute 2010-2020 (gappy before 2013); Damodaran annual returns 1928-2025; Cboe strategy-index histories are free.

TASK, in plain English, under 600 words:
A. Review the OPEN ideas below. For each, one line: worth a registered test (yes / no / maybe), the main reason, and the realistic power with the data we have.
 Idea 1 variants: opening-range fade and pullback entry (breakout was run and closed).
 Ideas 2, 3, 4: dropped for lack of 1-minute data (opening range + fair-value-gap entry; cross-index divergence NAS100 vs SPX500; liquidity sweep + structure shift); could be reopened with the free 2010-2020 1-minute data.
 Idea 7 (the PM): confidence-scored fractional Kelly position sizing. Idea 8 (the PM): option strategies (covered call, PMCC, vertical spreads, protective put, collar) vs CFDs.
 Idea 9 (the PM, spitballing): pre-market moves in the biggest index constituents (for example AAPL) predicting the index open. Idea 10: daily 200-day trend rule. Idea 11: valuation tilt. Idea 12: volatility-targeted sizing.
 Idea 14: reopen Ideas 2-4 with longer history. Idea 16: cTrader copy-trading provider bot (distant goal only).
B. Propose THREE NEW ideas of your own that are not on this list and are not the tested ones above. For each: the exact rule in two sentences, why it might be real (cite a source you are confident exists; mark anything unverified), what free data would test it, how many independent events or trades the data gives, the smallest effect that could be detected at t >= 2.8, and how many trials (N) it would cost. Prefer ideas where the sample is large enough to be properly powered; say so plainly when it is not.
C. One sentence: which single idea, old or new, you would test first and why.

Rules: do not recommend trading real money, do not suggest or encourage betting or speculation, state uncertainty, do not claim figures you cannot source, and do not give strategy details to third parties. A clean "none of these is worth testing" is a valid answer to part A.
```
