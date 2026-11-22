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
- Blind cross-scoring prompt sent to both GLM and GPT6 at 00:36 UTC on 22 Nov 2026 (per Joe). Replies pending; elapsed to be logged on receipt.
- GPT6 blind cross-scoring reply received 00:37 UTC (about 1 minute after the 00:36 send). Claude's check of GPT6 as a scorer: all five citation venues it supplied are correct (JFQA, J. Finance x2, J. Asset Management, RFS); all arithmetic correct, including correcting Claude's loose "about 30 bp" for pre-FOMC to 35.4 bp; it rightly noted that Y2 (pre-FOMC drift) repeats the excluded Fed family (Claude's own breach of its own exclusion; accepted). Weaker points: it scored X1/X2 9/10 although by their own numbers neither is testable (power 3-22%), and X1 is in the same class as the Fed family; "10/11" is not on the rubric's scale (best proposal 9 + 1 = 10); stray citation markers. Net: accurate and checked, somewhat lenient on feasibility, harsh in the right places on Y.

## IDEAS ROUND 1 - FINAL SCORECARD (22 Nov 2026; all three views)
Response times: GLM blind cross-score pasted 00:45 UTC (about 9 minutes after the 00:36 send); GPT6 00:37 (about 1 minute).
| Set | Claude | GPT6 | GLM |
|---|---|---|---|
| X (GLM) | 8 | 10 | (own set; self-assessed 8 in errata, "no appeal") |
| Y (Claude) | 8 (self, strict: -1 for C1 wrong venue and C2 repeating the banned Fed family) | 7 | 9 |
| Z (GPT6, no proposal) | 8 as a screened candidate (provisional); formula-strict 1/10 | (own set) | 1/10 (formula; "not comparable") |
Claude's own scoring of set Y (same rubric): C1 5/10 (a 0 under the strict letter: venue was wrong; b 1: "needs net +1 bp" conflates the kill floor with the t-gate, passing t>=2.8 needs about 4.5 bp net; c 2; d 1; e 1), C2 6/10 (a 2; b 1: SD 80 bp is session-scale, a 24-hour hold is about 120-150 bp so detectable is about 55-65 bp not 30; c 2; d 0: banned repeat; e 1), C3 8/10 (a 2; b 2; c 2; d 1; e 1). Best 8 + 1 calibrated - 1 breach = 8/10.
Reconciling Z: Claude's 8/10 scored GPT6's screened-and-withdrawn candidate as if it were a proposal; the rubric's formula scores an empty set 0 + 1 = 1. GLM is right that the two are not comparable; the better statement is "empty and honest, ranks above an invented set, produced no usable idea".
Check of GLM as scorer/auditor: verified errata (four journal venues, all correct incl. RFS 1(4) 403-425, JF 70(1) 329-371); real errors found in Claude's set that GPT6 missed or repeated (Y2 SD scale and detectable effect, the net-vs-t-gate conflation); owned its errors without appeal. Weaker: calls it "Joe's audit" (it was Claude's scoreboard); cites "Kurov et al. 2020" for weakening of the pre-FOMC drift, which Claude could not verify (the paper Claude knows is Kurov, Sancetta, Strasser and Wolfe, JFQA 2019 - year/venue to be checked); its criticism that GPT6 could have bounded costs from spreads is only half fair (reviewers have no access to the private bar files).
Cross-view conclusion: the three sets converge: no idea in this round is testable above about 35 bp per event, so none justifies an N from the remaining +3. GLM's route stands: Family A first; if the programme continues, fold the announcement-day idea into the Fed family (shared Bonferroni). Differences are in style: GPT6 most cautious, GLM most thorough and most numerically exact but the sloppiest on first-pass citations, Claude fastest to put a set down but made a rule breach and a venue slip.

## ROUND 2 (cross-audit) - SCORECARD (22 Nov 2026)
Prompts sent about 00:55 UTC. Replies: Claude Sonnet 5.5 committed 00:56 (about 1 minute, after the prompt); ChatGPT 6 pasted 00:58 (about 3 minutes); GLM 5.3 pasted 01:02 (about 7 minutes). All within 10 minutes: no speed deductions. Scoring: +1 per VERIFIED new error found, -1 per false or invalid claim; errors already recorded are not counted again. Full texts are in the REPLIES files; Claude's audit is docs/ROUND2_CLAUDE_AUDIT.md.
- **GLM 5.3: +4, no false claims.** Found no error in GPT6's own claims (it says so), but verified four errors in the surrounding record and Claude's longterm files: (1) HANDOVER_GPT6.md named the wrong paper for the weakening pre-FOMC drift (the "disappearing drift" paper is Kurov, Wolfe and Gilbert, Finance Research Letters 40 (2021) 101781 - Claude confirmed on RePEc; Claude had written the JFQA 2019 Kurov-Sancetta-Strasser-Wolfe paper, a different one); (3) the record of GPT6's reply was inconsistent (Set Z carried "1958-2009", which GPT6's original did not state, and the repo held only Claude's summary, not the sealed original) - Claude's record error; (4) longterm/spec.md half labels should read 1929-1976 and 1977-2025; (5) latent seed in run.py (no effect on results). Re-ran run.py exactly. One self-erratum (Kurov year/paper).
- **ChatGPT 6: +2 net (3 valid, 1 invalid).** Valid: (F1) GLM compared a 0.52% detectable mean with the paper's 49 bp, which is for the 24-hour window, not the proposed 10:00-13:55 window; (F3) the 2-of-3 cost is 3.7% at 1.5 bp, not within 1-3%; (source note) the repo copy of REPLIES_FROM_GLM.md was missing Round G - Claude's record error, now fixed. Invalid: the "line 9 still has old thirds" finding - already fixed at 00:12 UTC (it read a stale copy) and not a GLM error. Missed: the 1,200-versus-1,370 trading-day error in GLM's power line.
- **Claude Sonnet 5.5: +1 net.** Found GLM's n error (1,371 days not about 1,200; detectable 1.9 bp not 2.0), and own longterm caveats; recorded errors found by others that Claude introduced: the wrong Kurov paper (-1), the missing Round G, summaries saved as verbatim, and the Set Z embellishment (record errors, counted as one -1 for false claims in the audit round). Found GPT6's errors only where already recorded.
Round 2 ranking: GLM 1st (5 points), ChatGPT 6 and Claude Sonnet 5.5 - ChatGPT 6 2nd on net score (3 points), Claude Sonnet 5.5 3rd (1 point).
