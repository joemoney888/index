# US index forward shadow (the NAS100 rule, unchanged, on NAS100, SPX500 and US30)

Forward period starts 2026-11-19. Paper replay of the exact tested rule; no orders. Backtest expectation per trade: NAS100 +0.03 to +0.07R, SPX500 and US30 about +0.015R.

| Market | Trades | Avg R | Cumulative R | Win rate | t-stat |
|---|---|---|---|---|---|
| NAS100 | 3 | +0.913 | +2.7 | 100% | 3.11 |
| SPX500 | 3 | +0.714 | +2.1 | 100% | 2.33 |
| US30 | 3 | +0.086 | +0.3 | 33% | 0.00 |

Pooled: 9 trades, +0.571R average, t 2.23. Data to 2026-11-23 23:00 UTC.
- Verdict: TOO EARLY until about 300 trades per market (about 2 months); then it counts only if the average stays positive with t >= 2.


_The no-target variant (kt 20) was switched off on 2026-11-21; its earlier rows are kept in forward/*_open_shadow.csv and count for nothing._