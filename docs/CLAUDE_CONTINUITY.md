# Claude continuity file (backup in case the chat is lost)
Updated 22 Nov 2026 (UTC). To resume: start a new Claude session, attach/point it at this file and `docs/HANDOVER.md`, and say "continue from CLAUDE_CONTINUITY". No keys or tokens are stored here and none should ever be.

## The project and the owner
Joe (UK, Europe/London). Documented paper-trading/AI experiment. Two agents: **Blue Falcon** (old ORB agent, private repo `joemoney888/gbpusd-paper-agent`, first OANDA practice account, runs to about 24 Nov) and **Blue Falcon Green, BFG** (US-index mean reversion, public repo `joemoney888/index`, second OANDA practice account, cron-job.org -> workflow_dispatch every 5 min, `index.yml`). Reviewers: GLM 5.3 (active), ChatGPT 6 (invited, onboarding in `docs/HANDOVER_GPT6.md`), DeepSeek and K3.1 retired. Joe pastes reviewer replies; Claude commits them and grades them neutrally.
Joe's style: plain English, short, action over talk; "chuck it at the wall and see what sticks"; dislikes wasted compute; decides spending himself.

## Standing rules (never break)
Demo/paper only; no manual trades on practice accounts; keep the Blue Falcon repo private; never put keys in chat; Claude must not contact third parties, sign up, subscribe or accept terms for Joe; no strategy details in outreach; LIMITS=on before any real money; nothing justifies real money; bars only rise (N counter, luck bar sqrt(2 ln N)+0.5) - never lowered; no overclaims ("no gross miscalibration detected", never "calibrated"; never "no drift at any horizon").

## State of the science
BFG has no demonstrated edge: backtest edge was an artefact of idealised trailing-stop fills; realistic about -0.01R/trade over 2 years (+0.013R last year). Entry line closed (B.1/C.2). Test 4 shuffle calibration: 0/20 false finalists. Long-term yearly trend rule vs buy-and-hold: FAIL (`longterm/`). XND options and longer-dated option structures: unsuitable at this size (costs and contract granularity). Family A (A5, A6a, A6b) spec v1.1 is frozen, NOT RUN: `docs/FAMILY_A_SPEC.md`, calendar `famA/calendar.json` (written from memory of the public NYSE calendar - must be checked against the official page before the run). N is 941,542 now, pre-create 941,545 before the Family A run. Cap: at most +6 further N, write-up by 2026-12-19. New rule ideas: reviewers may propose; run only after a second reviewer and Joe sign off.

## Monday (23 Nov) checklist
1. Confirm OANDA runs resumed (the account page had an outage 21 Nov).
2. Reconcile the first `trade_closed` events against OANDA fills (assumption: realized_pl is in GBP).
3. Fix the clock-based time exit in `ftmo/stop_1min.py` and re-run its three rows.
4. 941,367 ledger audit.
5. Family A pre-run checklist (no outcome looks): ledger/N pre-create, bar coverage, early-close verification, spread sanity, timezone unit tests, check calendar against the NYSE page, freeze the runner, run ONCE, record verdicts.
6. When ready, switch on optional compounding sizing: repo variables `INDEX_COMPOUND=true` and `INDEX_COMPOUND_START=<ISO timestamp>` (default off; code in `index_run.py` and `agent/index_live.py`; log it in `docs/NOTES_FOR_GLM.md`).
7. Grade GPT6's first review in `docs/HANDOVER_GPT6.md` (scoreboard).

## Things built recently (22 Nov)
Weekly R-only report: workflow `weekly_report.yml` in the private repo (Fridays 21:30 UTC), script `report/eod_report.py`, output `reports/weekly/<date>/` (weekly and daily total R for both agents; no pound figures). Chart labels in R (`index_chart.py`, `agent/review.py` in the private repo). `list_instruments.py` read-only lister (the BFG account trades 123 instruments: 34 CFDs, 21 metals, 68 currencies; 15 index CFDs).

## Scheduled tasks (Claude scheduling tool)
Daily error review (08:41 Europe/London, read-only report); reminder 1 Dec 2026 09:00 UTC review of the AI shadow test; reminder 9 Feb 2027 to renew the cron-job.org GitHub token (expires 16 Feb 2027).

## Where things are
Public repo `joemoney888/index`: `agent/` engine, `search/` ledgers and calibration, `ftmo/`, `forward/`, `famA/`, `longterm/`, `report/`, `docs/` (HANDOVER, NOTES_FOR_GLM, REPLIES_FROM_GLM, FAMILY_A_SPEC, IDEA_BACKLOG, HANDOVER_GPT6). Private repo: old agent, 5-minute data for 11 markets (NAS100 etc., 2021-05-19 to 2026-11-18), macro data (VIX, yields), weekly reports. Tests: `python -m pytest -q tests` (13 pass). Use the GitHub REST API (`gh api`), not GraphQL, from Claude sessions.

## Open decisions with Joe
Test 5 (flip logging) skipped unless asked; optional idea 1 (N+1) and a Fed-announcement family (N+2) only after Family A; optional email/notification of the weekly report; whether to check XND spreads on an IBKR paper account (Joe would need to open it).
