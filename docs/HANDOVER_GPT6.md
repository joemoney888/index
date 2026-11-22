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

(Next block: GPT6 first review, once received.)
