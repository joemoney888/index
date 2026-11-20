# FTMO-compliant BFG test (20 Nov 2026)
Entry-only blackouts: 2h before any market close >= 2h (weekends/holidays), FOMC and jobs report windows, CPI proxy (dates 10-15, over-blocks).
| case | blocked | exam (last 365d) |
|---|---|---|
| no filter | 0% | +0.067R, t 4.28, n 1368 |
| close windows only | 2% | +0.066R, t 4.17 |
| + NFP/FOMC +-2h | 3.4% | +0.062R, t 3.89 |
| + NFP/FOMC whole day | 9% | +0.062R, t 3.77 |
| + CPI proxy +-2h | 6.9% | +0.062R, t 3.85 (val t 1.39) |
| + CPI proxy whole day | 27.8% | +0.059R, t 3.24 |
Rough 2-Step simulation (realised equity only, overlapping starts, OPEN-TRADE DRAWDOWN NOT MODELLED, in-sample-ish): 0.75-1% risk/trade passes both phases in roughly 75-94% of start dates, median ~45-65 days phase 1, ~20-30 days phase 2. Treat as an upper bound, not a forecast.
Not modelled: FTMO commissions, earnings-day rule, Best Day/consistency rules, FTMO's price feed vs OANDA, stop slippage on gaps.

## UPDATE 20 Nov 2026 (late): the edge does not survive realistic stop fills
Scripts: `ftmo/cost_stack.py`, `ftmo/stop_1min.py`.
- The 5-minute backtest lets the trailing stop jump to a level computed from the previous bar's best price and fills there, even when price has already moved beyond it. A live agent that moves the stop once per poll (or any bar-boundary logic) can only exit at market in that case. Modelling that (stop exits fill at the bar open when the open is already beyond the stop; 28% of stop exits): 2-year mean R +0.046 -> -0.010 (t -0.88); last 365 days +0.062 -> +0.013 (t 0.79). Extra slippage of 1x spread on stop exits: -0.028 / -0.003. Financing is small (2-3% of trades cross the rollover). Commission placeholders (0.25 to 1 bp/side) make it clearly negative.
- Sensitivity (engine): trailing stop OFF: train -0.006R, val -0.085R, exam +0.015R (edge gone, so the edge was the trailing stop). Wider trail 1.5/2.0 ATR: weaker. Gate OFF: still positive (train +0.036, exam +0.044), so the volatility gate is not the source. Gate inverted: weak. 94% of trades exit via a stop (incl. trailing, mean -0.03R), 6% at target (+1.27R).
- Exits re-simulated on 1-MINUTE bars (Nov 2023 - Nov 2026, 4,434 trades, same entries): stop updated every 5 min like the live agent: -0.007R (t -0.78), last 365 days +0.014R (t 0.89). Stop updated every minute (native trailing stop): -0.002R (t -0.27), last year +0.012R. Not distinguishable from zero.
- Live log check: entries fill close to plan (8 fills, mean adverse slippage -0.009R, i.e. no entry cost problem). The live log does NOT record exit fill prices, so live exits cannot yet be compared with the backtest.
Conclusion: on current evidence the +0.04 to +0.07R headline edge is mostly an artefact of idealised trailing-stop fills on 5-minute bars. Realistic expected edge is about zero (95% interval roughly +/-0.03R). The FTMO simulation was not rerun because with ~0R edge the pass rate is no better than chance and the fee refund only applies after a pass. Do NOT buy an FTMO challenge on this rule.

## RECORD FIXES (20 Nov 2026, late) - three corrections requested in review
**1. Luck bar recomputed against the final ledger N.** The NAS100 finalist (train t 5.31, validation t 2.26) cleared the bar recorded at the time of its search (N = 31,740 variants in the NAS100 ledger, bar 5.05). Recomputed with the cumulative ledger (sum of all `runs/*.json` ledgers in both repos; may double count a little):

| N used | N | bar = sqrt(2 ln N)+0.5 | train t 5.31 clears it? |
|---|---|---|---|
| NAS100 ledger (as recorded) | 31,740 | 5.05 | yes |
| US-index markets (NAS100+SPX500+US30) | 115,348 | 5.33 | no (by 0.02) |
| all main-engine ledgers (12 markets/runs) | 669,283 | 5.68 | no |
| everything incl. scalp and pattern families | 941,367 | 5.75 | no |

Outcome: at any cumulative N the finalist does NOT clear the pre-registered train bar; it passed only under the per-market N. The exam (t 4.28, one year, used once) is a fresh test of one pre-selected rule, so it is not subject to this bar, but it can only support the SIGN of an edge and, since the cost re-test below, even that is now unsupported. Record status: candidate under the original per-market bar; not a finalist under the cumulative bar.
**2. The FTMO-compliant configuration versus the pre-registered validation gate (validation mean >= +0.03R and t >= 2.0).** With the conservative CPI blackout (the one most likely to match FTMO's real "major news" list) validation is +0.021R, t 1.39: **FAILS the gate**, even though the exam stays positive (+0.062R, t 3.85). Other variants: close windows only +0.030 (t 2.03) marginal pass; NFP/FOMC +-2h +0.032 (t 2.11) narrow pass; NFP/FOMC whole day +0.033 (t 2.11) narrow pass; CPI proxy whole day t 1.81 fails. Passing the exam does not repair a failed validation gate. The compliant rule must be treated as a NEW, unvalidated hypothesis, not as the validated BFG rule; its exam has already been seen.
**3. FTMO sizing recommendation cut to <= 0.75% risk per trade, with floating P&L modelled** (`ftmo/ftmo_sim2.py`: equity = closed balance + open trade at its worst price each 5-minute bar, daily loss versus equity at the 00:00 CE(S)T reset, non-overlapping monthly starts, phase 2 conditional, Wilson 95% intervals, 24 starts, validation+exam period). Idealised R: 0.50% risk 88% pass both phases (CI 69-96%); 0.75% 96% (80-99%); 1.00% 67% (47-82%, five phase-1 failures) - so 1% is too aggressive even before costs. Gap-aware R: 0-8% at every size. The earlier "0.75-1%" recommendation is withdrawn: maximum 0.75%, and only if the realistic-fill edge is first shown to be positive.
**Bottom line (unchanged): nothing here justifies real money, including an FTMO fee.**
