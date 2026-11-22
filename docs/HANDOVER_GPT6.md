# Welcome, ChatGPT 6 - reviewer onboarding for Blue Falcon Green (BFG)
Written 22 Nov 2026 (UTC) by Claude (writes and tests all code; grades reviewer replies). Owner: Joe. **Everything is paper/demo money. You cannot push code, and nobody trades on your say-so.** Nothing here is financial advice.

## Your role
Independent reviewer, same job as GLM (another reviewer, replies in `docs/REPLIES_FROM_GLM.md`). Claude writes and tests ALL code; reviewers only read, check and write. Joe pastes your reply back; Claude commits it to `docs/REPLIES_FROM_GPT6.md` and scores it at the end of this file.

## Read in this order
1. `docs/HANDOVER.md` (project, discipline, what failed; top banner: the old backtest edge was an artefact of idealised trailing-stop fills; section 10 is the correction).
2. Since then (all in the public repo): `search/CALIB/RESULT.md` (Test 4: shuffle calibration, 0/20 false finalists, no gross miscalibration detected - NOT "calibrated"), `ftmo/RESULT.md` (entry drift, gap decomposition), `docs/FAMILY_A_SPEC.md` (v1.1, frozen, NOT RUN), `docs/IDEA_BACKLOG.md`, `longterm/spec.md` (yearly trend rule vs buy-and-hold, FAIL), `docs/NOTES_FOR_GLM.md` and `docs/REPLIES_FROM_GLM.md` (what was already asked and answered - do not repeat it).
3. Current state in one paragraph: BFG has no demonstrated edge (realistic fills about -0.01R/trade over 2 years, +0.013R last year; 175-variant realistic-exit search found nothing). The only live next test is Family A (A5 London->NY reversal, A6a first-half-hour momentum, A6b last-half-hour), frozen before any look, N +3. Cumulative trial count N is 941,542 (luck bar sqrt(2 ln N)+0.5 = 5.75). Cap: at most +6 further N, write-up by 2026-12-19. Also tested and shelved: XND options (costs and contract size make the product unsuitable at this account size), longer-horizon option structures (no edge to express).

## Rules
- Concise. Show arithmetic. Separate (1) errors verifiable in the repo, (2) judgement calls, (3) ideas. No praise, no padding, no repeating the question. Say when you cannot verify something. Do not invent results.
- You MAY propose new rules, but only as written proposals for sign-off, never as results. Max 3, your best: the exact rule; the mechanism or published source (NO ideas mined from our own data); expected edge and power at our sample size; what result would kill it; and its cost in N. Nothing is run until a second reviewer and Joe sign off. Claude then runs it ONCE.
- No keys, tokens, account ids or private-repo contents are ever needed or shared.

## First review (about 600 words max)
1. Errors in `docs/FAMILY_A_SPEC.md` v1.1: definitions, timezone and daylight-saving handling, the NYSE holiday/early-close list (`famA/calendar.json`), decision rule, power.
2. Does Test 4 support "no gross miscalibration detected", and what does it NOT show?
3. Is `longterm/spec.md` valid, and is "no evidence the yearly trend rule beats buy-and-hold" the right conclusion (97 yearly observations, one rule, one market)?
4. The single biggest weakness in how N is counted.
5. Optional: up to 3 proposals under the rules above.

## Scoring rubric (applied by Claude to every reviewer, same for GLM and you)
Each criterion 0-2, total /10: (a) **Verified errors found** - real, checkable in the repo; (b) **No false claims** - wrong statements subtract; (c) **Arithmetic/power correct** (Claude re-computes); (d) **Calibration** - separates fact from judgement, admits what it cannot verify; (e) **Concision and usefulness** - no padding; ideas have mechanism, power and a kill rule. A correct self-correction scores in (d), not against. Claude is a participant as well as the grader, so Joe can ask a reviewer to check a score.

## SCOREBOARD (append one block per session; newest at the bottom)
### Baseline (Claude's retroactive reading of GLM's earlier rounds; indicative, not scored line by line)
- GLM round F: found real issues (Test 2 tautological rule, B.1 overclaim, "calibrated" overclaim, UTC London boundary across DST) - but its A6a predictor reading (09:30-10:00) was wrong.
- GLM round G: self-corrected the predictor; added power arithmetic; four blocking items on the spec that were all valid (predictor, previous-close definition, holiday list, exact dates).
- DeepSeek (no longer used): found useful points but made errors Claude caught (favourable-fill tie-break advice, trades vs variants 941k, wrong N counting for control tests).

### GPT6 - session 1 (first review, 22 Nov 2026) - Claude score 8/10
(a) Verified errors found: 1/2 - one genuine new defect (the main text of FAMILY_A_SPEC still carried the old 2021-11 dates and thirds, contradicting the v1.1 changelog; Claude confirmed and fixed it, editorial only). The calendar-verification and N-audit points were already on Claude's own pre-run checklist, so not new.
(b) No false claims: 2/2 - nothing wrong found on checking; Test 4's exact bound 1-0.05^(1/20)=13.9% re-computed and correct; N arithmetic (941,367 + 175 = 941,542) correct. Minor: cited lines 9 and 28 (actually 11 and 34).
(c) Arithmetic/power: 2/2 - correct, and it was right that the spec itself carries no full power calculation (that sits in the backlog/GLM round G).
(d) Calibration: 2/2 - said it cannot certify the holiday list, labelled "no gross miscalibration" correctly, and declined to invent proposals to use up the N allowance (a good sign).
(e) Concision/usefulness: 1/2 - concise and structured; but little that was new, a vague "|t|" wording quibble, the long-term point was fair (it correctly says the result is stronger than "no evidence"), and stray citation markers clutter the text.
Overall: careful, honest, no errors, one real catch. Needs to show it can find things GLM did not. Next session: ask for adversarial checks of famA/calendar.json against its own knowledge of the NYSE calendar and a power calculation using the measured SD.


### GPT6 - session 2 (ideas round 1, 22 Nov 2026) - Claude score 8/10 (provisional until blind cross-scoring)
Submitted no proposal; screened one candidate (non-FOMC macro-announcement premium) and withdrew it on power grounds.
(a) Source real and correctly described: 1/2 - Savor and Wilson (2013, JFQA 48(2), 343-375) verified by Claude: abstract says announcement-day excess return 11.4 bp versus 1.1 bp, 1958-2009 (GPT6 omitted the period and the announcements cover inflation, unemployment and interest rates, not only NFP/PPI - applying it to NFP+PPI is an extrapolation). Ai and Bansal (NBER WP 22527; Econometrica 2018) is real, but its quoted 15.44 bp (NFP) and 7.53 bp (PPI) could NOT be verified by Claude (the abstract has no such numbers; may be in a table).
(b) Power/effect size honest: 2/2 - arithmetic re-computed and correct (2.8 x 75/sqrt(132) = 18.3 bp; 100 bp SD -> 24.4; 150 -> 36.6; expected t = 1.32).
(c) Pre-registerable: 2/2 - exact rule, times, numeric kill rule.
(d) Novel: 1/2 - not on the list, but closely related to the already-listed Fed-announcement family.
(e) Feasible: 1/2 - by its own arithmetic it is not testable at our sample size; net cost left blank (it said it could not give a number without spreads - honest).
Calibrated: +1 (honest prior below 2%, preserved N, refused to invent).
Overall: very calibrated and honest, but it generated no usable idea. The value so far is in what it refuses to claim, not in what it proposes.

### GLM - session (ideas round 1, 22 Nov 2026) - Claude score 8/10 (provisional until blind cross-scoring)
Two proposals (P1 NFP+CPI announcement-day long; P2 pre-holiday long), third slot deliberately empty with arithmetic; priors 4-5%; recommends registering neither unless Joe wants the science value, and folding P1 into the Fed family.
(a) Source real and correctly described: 1/2 each - papers, authors, titles and years right, but journal venues wrong in four places: Savor and Wilson is JFQA 48(2) 2013 (GLM: "Journal of Finance 2013 or 2014 (unsure)"); Ariel 1990 is the Journal of Finance 45(5), 1611-1626 (GLM: JFQA); Lakonishok and Smidt 1988 is the Review of Financial Studies (GLM: JFE); and Lucca and Moench is Journal of Finance 70(1) 2015, which GLM asserted WITHOUT hedging as "AER 2015" while "correcting" an earlier near-miss. Three were hedged "verify"; the Lucca-Moench one was not (-1). Lou, Polk and Skouras (JFE 2019) and Acharya-Johnson (JFE 2007, single-name CDS) are right. Effect sizes quoted (roughly 10-15 bp announcement days) are consistent with the verified 11.4 bp vs 1.1 bp.
(b) Power/effect size: 2/2 - all arithmetic re-computed and right (140/sqrt(128)=12.4 bp; detectable 34.7; power at 12 bp about 3%, at 25 bp 22%; P2 85/sqrt(48)=12.3, detectable 34.4, power at 20 bp 12%; overnight 80/sqrt(1390)=2.1, detectable 6.0).
(c) Pre-registerable: 2/2 - exact rules, times, frozen calendars, numeric kill rule, drift benchmark.
(d) Novel: P1 1/2 (same class as the Fed family; GLM says so), P2 2/2.
(e) Feasible: 1/2 each - by its own arithmetic neither is testable above about 35 bp.
Best proposal 8/10 (P2), +1 calibrated, -1 for the unhedged wrong venue = 8/10.
Overall: more concrete and more complete than GPT6's reply, but with the sloppiest sourcing; it caught nothing wrong in itself while stating a wrong venue with confidence. Independently converged with GPT6 on the macro-announcement premium and with Claude on rejecting overnight and turn-of-month.

### Response-time log (added 22 Nov 2026)
Times are when Joe pasted the reply to Claude (UTC = London in November), so they are upper bounds on the reviewer's own time. From now on each block records: prompt sent, reply received, elapsed.
- Ideas round 1 prompt sent to both: about 00:16-00:17. GPT6: first reply (could not open the file) 00:17; full ideas reply received 00:21 after the text was re-sent at about 00:20 (about 1-5 minutes). GLM: reply received 00:33 (about 17 minutes). Claude: committed its own set at 00:15 (before the prompt went out).
- Earlier sessions: GPT6 first review sent 00:11 about 7 minutes after the prompt at 00:04-00:10 (approximate); GLM rounds F and G not timed.
