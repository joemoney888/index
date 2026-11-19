# US index forward shadow (the NAS100 rule, unchanged, on NAS100, SPX500 and US30)

Forward period starts 2026-11-19. Paper replay of the exact tested rule; no orders. Backtest expectation per trade: NAS100 +0.03 to +0.07R, SPX500 and US30 about +0.015R.

| Market | Trades | Avg R | Cumulative R | Win rate | t-stat |
|---|---|---|---|---|---|
| NAS100 | 0 | +0.000 | +0.0 | 0% | 0.00 |
| SPX500 | 0 | +0.000 | +0.0 | 0% | 0.00 |
| US30 | 0 | +0.000 | +0.0 | 0% | 0.00 |

Pooled: 0 trades, +0.000R average, t 0.00. Data to 2026-11-19 23:00 UTC.
- Verdict: TOO EARLY until about 300 trades per market (about 2 months); then it counts only if the average stays positive with t >= 2.


## Variant: no fixed target (let winners run; kt 20, same trailing stop). Exploratory, started 2026-11-19.

| Market | Trades | Avg R | Cumulative R | Win rate | t-stat |
|---|---|---|---|---|---|
| NAS100 | 0 | +0.000 | +0.0 | 0% | 0.00 |
| SPX500 | 0 | +0.000 | +0.0 | 0% | 0.00 |
| US30 | 0 | +0.000 | +0.0 | 0% | 0.00 |