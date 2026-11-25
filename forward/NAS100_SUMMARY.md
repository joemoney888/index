# US index forward shadow (the NAS100 rule, unchanged, on NAS100, SPX500 and US30)

Forward period starts 2026-11-19. Paper replay of the exact tested rule; no orders. Backtest expectation per trade: NAS100 +0.03 to +0.07R, SPX500 and US30 about +0.015R.

| Market | Trades | Avg R | Cumulative R | Win rate | t-stat |
|---|---|---|---|---|---|
| NAS100 | 16 | +0.105 | +1.7 | 62% | 0.53 |
| SPX500 | 22 | +0.149 | +3.3 | 50% | 1.18 |
| US30 | 28 | -0.093 | -2.6 | 43% | -0.79 |

Pooled: 66 trades, +0.036R average, t 0.45. Data to 2026-11-25 23:00 UTC.
- Verdict: TOO EARLY until about 300 trades per market (about 2 months); then it counts only if the average stays positive with t >= 2.


_The no-target variant (kt 20) was switched off on 2026-11-21; its earlier rows are kept in forward/*_open_shadow.csv and count for nothing._