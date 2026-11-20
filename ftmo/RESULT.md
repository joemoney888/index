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
