# US index forward shadow (the NAS100 rule, unchanged, on NAS100, SPX500 and US30)

Forward period starts 2026-11-19. Paper replay of the exact tested rule; no orders. Backtest expectation per trade: NAS100 +0.03 to +0.07R, SPX500 and US30 about +0.015R.

| Market | Trades | Avg R | Cumulative R | Win rate | t-stat |
|---|---|---|---|---|---|
| NAS100 | 25 | -0.017 | -0.4 | 52% | -0.13 |
| SPX500 | 35 | +0.014 | +0.5 | 40% | 0.14 |
| US30 | 39 | -0.067 | -2.6 | 44% | -0.74 |

Pooled: 99 trades, -0.026R average, t -0.43. Data to 2026-11-26 23:00 UTC.
- Verdict: TOO EARLY until about 300 trades per market (about 2 months); then it counts only if the average stays positive with t >= 2.


_The no-target variant (kt 20) was switched off on 2026-11-21; its earlier rows are kept in forward/*_open_shadow.csv and count for nothing._