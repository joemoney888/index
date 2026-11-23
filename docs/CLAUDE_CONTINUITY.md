# Claude continuity file (backup in case the chat is lost)
Updated 22 Nov 2026 01:05 UTC (session closed). To resume: start a new Claude session, attach/point it at this file and `docs/HANDOVER.md`, and say "continue from CLAUDE_CONTINUITY". No keys or tokens are stored here and none should ever be.

## The project and the owner
Joe (UK, Europe/London). Documented paper-trading/AI experiment. Two agents: **Blue Falcon** (old ORB agent, private repo `joemoney888/gbpusd-paper-agent`, first OANDA practice account, runs to about 24 Nov) and **Blue Falcon Green, BFG** (US-index mean reversion, public repo `joemoney888/index`, second OANDA practice account, cron-job.org -> workflow_dispatch every 5 min, `index.yml`). Reviewers: GLM 5.3 (active), ChatGPT 6 (invited, onboarding in `docs/HANDOVER_GPT6.md`), DeepSeek and K3.1 retired. Joe pastes reviewer replies; Claude commits them and grades them neutrally.
Joe's style: plain English, short, action over talk; "chuck it at the wall and see what sticks"; dislikes wasted compute; decides spending himself.

## Standing rules (never break)
Demo/paper only; no manual trades on practice accounts; keep the Blue Falcon repo private; never put keys in chat; Claude must not contact third parties, sign up, subscribe or accept terms for Joe; no strategy details in outreach; LIMITS=on before any real money; nothing justifies real money; bars only rise (N counter, luck bar sqrt(2 ln N)+0.5) - never lowered; no overclaims ("no gross miscalibration detected", never "calibrated"; never "no drift at any horizon").

## State of the science
BFG has no demonstrated edge: backtest edge was an artefact of idealised trailing-stop fills; realistic about -0.01R/trade over 2 years (+0.013R last year). Entry line closed (B.1/C.2). Test 4 shuffle calibration: 0/20 false finalists. Long-term yearly trend rule vs buy-and-hold: FAIL (`longterm/`). XND options and longer-dated option structures: unsuitable at this size (costs and contract granularity). Family A (A5, A6a, A6b) spec v1.1 is frozen, NOT RUN: `docs/FAMILY_A_SPEC.md`, calendar `famA/calendar.json` (written from memory of the public NYSE calendar - must be checked against the official page before the run). N is 941,542 now, pre-create 941,545 before the Family A run. Cap: at most +6 further N, write-up by 2026-12-19. New rule ideas: reviewers may propose; run only after a second reviewer and Joe sign off.

## Monday (23 Nov) checklist - DONE items 1-4 (details in docs/HOUSEKEEPING_2026-11-23.md)
1. DONE: OANDA runs green. 2. DONE: found and fixed the trade_closed logging bug (CSV quoting); first 8 closed trades reconciled; realized_pl is GBP. 3. DONE: stop_1min.py bar-count time exit, results unchanged. 4. DONE: ledger recount 943,542 vs 941,542 (TREND run 2,000), bar unchanged; data-gap scan found 3 unusual days (2022-05-04, 2022-05-12, 2026-02-04).
5. OPEN: Family A pre-run checklist (no outcome looks): decide the amendment proposal first (docs/FAMILY_A_AMENDMENT_PROPOSAL.md, option A or B; external NAS100 data held in the PRIVATE repo, sealed 2016-11-15 to 2021-05-18), ledger/N pre-create, bar coverage, early-close verification (calendar from the NYSE page), spread sanity, timezone unit tests, freeze the runner, run ONCE, record verdicts.
6. OPEN, needs Joe: switch on optional compounding sizing: repo variables `INDEX_COMPOUND=true` and `INDEX_COMPOUND_START=<ISO timestamp>` (default off; log it in `docs/NOTES_FOR_GLM.md`).
7. DONE earlier: GPT6's first review graded. Session 2 league: data round done (ChatGPT 6 5, GLM 3, Claude Sonnet 5.5 1).

## Things built recently (22 Nov)
Weekly R-only report: workflow `weekly_report.yml` in the private repo (Fridays 21:30 UTC), script `report/eod_report.py`, output `reports/weekly/<date>/` (weekly and daily total R for both agents; no pound figures). Chart labels in R (`index_chart.py`, `agent/review.py` in the private repo). `list_instruments.py` read-only lister (the BFG account trades 123 instruments: 34 CFDs, 21 metals, 68 currencies; 15 index CFDs).

## Scheduled tasks (Claude scheduling tool)
Daily error review (08:41 Europe/London, read-only report); reminder 1 Dec 2026 09:00 UTC review of the AI shadow test; reminder 9 Feb 2027 to renew the cron-job.org GitHub token (expires 16 Feb 2027).

## Where things are
Public repo `joemoney888/index`: `agent/` engine, `search/` ledgers and calibration, `ftmo/`, `forward/`, `famA/`, `longterm/`, `report/`, `docs/` (HANDOVER, NOTES_FOR_GLM, REPLIES_FROM_GLM, FAMILY_A_SPEC, IDEA_BACKLOG, HANDOVER_GPT6). Private repo: old agent, 5-minute data for 11 markets (NAS100 etc., 2021-05-19 to 2026-11-18), macro data (VIX, yields), weekly reports. Tests: `python -m pytest -q tests` (13 pass). Use the GitHub REST API (`gh api`), not GraphQL, from Claude sessions.

## Open decisions with Joe
Test 5 (flip logging) skipped unless asked; optional idea 1 (N+1) and a Fed-announcement family (N+2) only after Family A; optional email/notification of the weekly report; whether to check XND spreads on an IBKR paper account (Joe would need to open it).


## Session close, 22 Nov 2026 (01:05 UTC): what happened after the first version of this file
- Reviewers: GLM 5.3 and ChatGPT 6 (onboarding `docs/HANDOVER_GPT6.md`; replies verbatim in `docs/REPLIES_FROM_GLM.md` and `docs/REPLIES_FROM_GPT6.md`). Monthly league table `docs/LEAGUE_TABLE.md`: 1st 5 points, 2nd 3, 3rd 1. After rounds 1 (ideas) and 2 (cross-audit): GLM 10, Claude Sonnet 5.5 4, ChatGPT 6 4. Speed rule from round 2: reply within 10 minutes none, over 10 up to 20 minutes -1, over 20 -2; Claude commits its own work only after the prompt is sent; errata within 30 minutes carry no penalty; blind packets carry wording unchanged. Next round: Joe decides (not started).
- Ideas round 1 result: no idea is testable above about 35 bp per event; none justifies spending the remaining +3 N. Family A first; fold any announcement-day idea into the Fed family later. Files: `docs/IDEAS_ROUND_1.md`, `docs/IDEAS_ROUND_CLAUDE.md`, `docs/IDEAS_ROUND_1_BLIND.md`, `docs/ROUND2_CLAUDE_AUDIT.md`.
- Built: optional compounding position size (OFF; repo variables INDEX_COMPOUND and INDEX_COMPOUND_START); R-only weekly report (private repo workflow `weekly_report.yml`, Fridays 21:30 UTC); chart labels in R; `list_instruments.py` (BFG account trades 123 instruments, 15 index CFDs, no stock CFDs).
- Research done: XND options unsuitable at this account size (forecast annual R strongly negative for long, short and spread; contract granularity; CFD better for this agent); long-term yearly trend rule vs buy-and-hold FAIL (`longterm/`, labels fixed, results identical); legal and tax questions answered in general terms only (not legal or tax advice).
- Record fixes: GLM Round G was missing from the repo copy and is now inserted; GPT6 replies saved verbatim; the pre-FOMC weakening paper is Kurov, Wolfe and Gilbert, Finance Research Letters 40 (2021) 101781 (not the JFQA 2019 paper).
- Still open for Monday: the checklist above (OANDA runs resumed, reconcile `trade_closed`, clock-based time exit fix, ledger audit, Family A pre-run checks and the single run, switch-on of compounding after reconciliation).
