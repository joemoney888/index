# Order book imbalance: does it predict the next move? (CME NQ futures (Databento))

## 2026-11-18_1430: 23,400 seconds, typical spread 0.28 bp
- 10s, top1: corr -0.039 (t -1.9); too few strong-imbalance cases
- 10s, top5: corr +0.024 (t +1.1); too few strong-imbalance cases
- 10s, top10: corr +0.017 (t +0.8); too few strong-imbalance cases
- 30s, top1: corr -0.044 (t -1.2); too few strong-imbalance cases
- 30s, top5: corr +0.033 (t +0.9); too few strong-imbalance cases
- 30s, top10: corr +0.020 (t +0.5); too few strong-imbalance cases
- 60s, top1: corr -0.101 (t -2.0); too few strong-imbalance cases
- 60s, top5: corr -0.042 (t -0.8); too few strong-imbalance cases
- 60s, top10: corr -0.027 (t -0.5); too few strong-imbalance cases
- 300s, top1: corr -0.053 (t -0.5); too few strong-imbalance cases
- 300s, top5: corr -0.049 (t -0.4); too few strong-imbalance cases
- 300s, top10: corr -0.137 (t -1.2); too few strong-imbalance cases

## Summary across stocks (average of per-stock results)

Reading it: a usable signal needs correlation clearly above zero AND net basis points above zero after the spread, consistently across stocks. One day on Nasdaq's own book (not the consolidated market).
