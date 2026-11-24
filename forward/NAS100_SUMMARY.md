# US index forward shadow (the NAS100 rule, unchanged, on NAS100, SPX500 and US30)

Forward period starts 2026-11-19. Paper replay of the exact tested rule; no orders. Backtest expectation per trade: NAS100 +0.03 to +0.07R, SPX500 and US30 about +0.015R.

| Market | Trades | Avg R | Cumulative R | Win rate | t-stat |
|---|---|---|---|---|---|
| NAS100 | 14 | +0.086 | +1.2 | 64% | 0.39 |
| SPX500 | 19 | +0.187 | +3.5 | 58% | 1.30 |
| US30 | 18 | -0.062 | -1.1 | 50% | -0.38 |

Pooled: 51 trades, +0.071R average, t 0.66. Data to 2026-11-24 23:00 UTC.
- Verdict: TOO EARLY until about 300 trades per market (about 2 months); then it counts only if the average stays positive with t >= 2.


_The no-target variant (kt 20) was switched off on 2026-11-21; its earlier rows are kept in forward/*_open_shadow.csv and count for nothing._