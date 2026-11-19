# Real Nasdaq order book (ITCH, 30 Jan 2020): does imbalance predict the next move?

## AAPL: 23,400 seconds, typical spread 1.25 bp
- 10s, top1: corr +0.016 (t +0.8); |imbalance|>0.6 n=657, gross -0.04 bp, spread 1.24 bp, net -1.28 bp
- 10s, top5: corr +0.018 (t +0.9); |imbalance|>0.6 n=91, gross -0.01 bp, spread 1.28 bp, net -1.29 bp
- 10s, top10: corr +0.011 (t +0.5); |imbalance|>0.6 n=61, gross -0.44 bp, spread 1.33 bp, net -1.77 bp
- 30s, top1: corr +0.035 (t +1.0); |imbalance|>0.6 n=214, gross +0.23 bp, spread 1.23 bp, net -1.00 bp
- 30s, top5: corr -0.009 (t -0.2); |imbalance|>0.6 n=29, gross +0.07 bp, spread 1.28 bp, net -1.22 bp
- 30s, top10: corr -0.010 (t -0.3); too few strong-imbalance cases
- 60s, top1: corr -0.044 (t -0.9); |imbalance|>0.6 n=120, gross -0.18 bp, spread 1.17 bp, net -1.35 bp
- 60s, top5: corr -0.046 (t -0.9); too few strong-imbalance cases
- 60s, top10: corr +0.002 (t +0.0); too few strong-imbalance cases
- 300s, top1: corr -0.100 (t -0.9); too few strong-imbalance cases
- 300s, top5: corr -0.219 (t -1.9); too few strong-imbalance cases
- 300s, top10: corr -0.241 (t -2.1); too few strong-imbalance cases

## AMZN: 23,400 seconds, typical spread 3.10 bp
- 10s, top1: corr -0.019 (t -0.9); |imbalance|>0.6 n=1328, gross -0.03 bp, spread 3.30 bp, net -3.32 bp
- 10s, top5: corr +0.046 (t +2.2); |imbalance|>0.6 n=470, gross +0.23 bp, spread 2.98 bp, net -2.75 bp
- 10s, top10: corr +0.055 (t +2.6); |imbalance|>0.6 n=211, gross +0.16 bp, spread 2.77 bp, net -2.60 bp
- 30s, top1: corr -0.041 (t -1.1); |imbalance|>0.6 n=448, gross -0.20 bp, spread 3.30 bp, net -3.50 bp
- 30s, top5: corr +0.008 (t +0.2); |imbalance|>0.6 n=161, gross +0.04 bp, spread 2.90 bp, net -2.86 bp
- 30s, top10: corr +0.015 (t +0.4); |imbalance|>0.6 n=69, gross -0.16 bp, spread 2.65 bp, net -2.81 bp
- 60s, top1: corr -0.046 (t -0.9); |imbalance|>0.6 n=227, gross -0.25 bp, spread 3.36 bp, net -3.60 bp
- 60s, top5: corr -0.050 (t -1.0); |imbalance|>0.6 n=79, gross -0.67 bp, spread 2.95 bp, net -3.61 bp
- 60s, top10: corr -0.030 (t -0.6); |imbalance|>0.6 n=36, gross -0.89 bp, spread 2.83 bp, net -3.73 bp
- 300s, top1: corr -0.195 (t -1.7); |imbalance|>0.6 n=43, gross -3.30 bp, spread 3.19 bp, net -6.49 bp
- 300s, top5: corr -0.012 (t -0.1); too few strong-imbalance cases
- 300s, top10: corr -0.012 (t -0.1); too few strong-imbalance cases

## MSFT: 23,400 seconds, typical spread 1.16 bp
- 10s, top1: corr -0.002 (t -0.1); |imbalance|>0.6 n=692, gross -0.09 bp, spread 0.93 bp, net -1.01 bp
- 10s, top5: corr +0.004 (t +0.2); |imbalance|>0.6 n=77, gross -0.54 bp, spread 1.09 bp, net -1.62 bp
- 10s, top10: corr -0.017 (t -0.8); |imbalance|>0.6 n=38, gross -1.51 bp, spread 1.34 bp, net -2.85 bp
- 30s, top1: corr +0.061 (t +1.7); |imbalance|>0.6 n=215, gross +0.34 bp, spread 0.89 bp, net -0.56 bp
- 30s, top5: corr +0.032 (t +0.9); |imbalance|>0.6 n=28, gross -1.18 bp, spread 1.08 bp, net -2.26 bp
- 30s, top10: corr +0.034 (t +1.0); too few strong-imbalance cases
- 60s, top1: corr +0.113 (t +2.2); |imbalance|>0.6 n=123, gross +0.76 bp, spread 0.89 bp, net -0.14 bp
- 60s, top5: corr +0.053 (t +1.0); too few strong-imbalance cases
- 60s, top10: corr +0.093 (t +1.8); too few strong-imbalance cases
- 300s, top1: corr +0.162 (t +1.4); |imbalance|>0.6 n=30, gross +2.85 bp, spread 0.91 bp, net +1.94 bp
- 300s, top5: corr +0.111 (t +1.0); too few strong-imbalance cases
- 300s, top10: corr +0.240 (t +2.1); too few strong-imbalance cases

## NVDA: 23,400 seconds, typical spread 3.29 bp
- 10s, top1: corr +0.040 (t +1.9); |imbalance|>0.6 n=1157, gross +0.20 bp, spread 3.44 bp, net -3.24 bp
- 10s, top5: corr +0.042 (t +2.0); |imbalance|>0.6 n=243, gross +0.29 bp, spread 3.61 bp, net -3.32 bp
- 10s, top10: corr +0.014 (t +0.7); |imbalance|>0.6 n=89, gross -0.10 bp, spread 4.28 bp, net -4.38 bp
- 30s, top1: corr +0.082 (t +2.3); |imbalance|>0.6 n=397, gross +0.91 bp, spread 3.55 bp, net -2.64 bp
- 30s, top5: corr +0.051 (t +1.4); |imbalance|>0.6 n=83, gross +0.13 bp, spread 3.70 bp, net -3.57 bp
- 30s, top10: corr -0.004 (t -0.1); |imbalance|>0.6 n=30, gross -0.52 bp, spread 5.22 bp, net -5.74 bp
- 60s, top1: corr +0.002 (t +0.0); |imbalance|>0.6 n=198, gross +0.19 bp, spread 3.28 bp, net -3.09 bp
- 60s, top5: corr +0.016 (t +0.3); |imbalance|>0.6 n=45, gross +0.07 bp, spread 3.36 bp, net -3.29 bp
- 60s, top10: corr -0.071 (t -1.4); too few strong-imbalance cases
- 300s, top1: corr -0.032 (t -0.3); |imbalance|>0.6 n=31, gross +0.24 bp, spread 2.85 bp, net -2.61 bp
- 300s, top5: corr -0.229 (t -2.0); too few strong-imbalance cases
- 300s, top10: corr -0.147 (t -1.3); too few strong-imbalance cases

## QQQ: 23,400 seconds, typical spread 0.45 bp
- 10s, top1: corr +0.077 (t +3.7); |imbalance|>0.6 n=879, gross +0.23 bp, spread 0.46 bp, net -0.24 bp
- 10s, top5: corr +0.029 (t +1.4); too few strong-imbalance cases
- 10s, top10: corr +0.012 (t +0.6); too few strong-imbalance cases
- 30s, top1: corr +0.058 (t +1.6); |imbalance|>0.6 n=305, gross +0.25 bp, spread 0.46 bp, net -0.22 bp
- 30s, top5: corr +0.015 (t +0.4); too few strong-imbalance cases
- 30s, top10: corr +0.035 (t +1.0); too few strong-imbalance cases
- 60s, top1: corr +0.039 (t +0.8); |imbalance|>0.6 n=158, gross +0.22 bp, spread 0.46 bp, net -0.24 bp
- 60s, top5: corr +0.035 (t +0.7); too few strong-imbalance cases
- 60s, top10: corr +0.045 (t +0.9); too few strong-imbalance cases
- 300s, top1: corr +0.256 (t +2.2); |imbalance|>0.6 n=28, gross +2.91 bp, spread 0.47 bp, net +2.44 bp
- 300s, top5: corr +0.167 (t +1.4); too few strong-imbalance cases
- 300s, top10: corr +0.226 (t +2.0); too few strong-imbalance cases

## SPY: 23,400 seconds, typical spread 0.31 bp
- 10s, top1: corr +0.082 (t +4.0); |imbalance|>0.6 n=632, gross +0.16 bp, spread 0.36 bp, net -0.20 bp
- 10s, top5: corr +0.036 (t +1.7); too few strong-imbalance cases
- 10s, top10: corr +0.014 (t +0.7); too few strong-imbalance cases
- 30s, top1: corr +0.083 (t +2.3); |imbalance|>0.6 n=218, gross +0.26 bp, spread 0.35 bp, net -0.09 bp
- 30s, top5: corr +0.004 (t +0.1); too few strong-imbalance cases
- 30s, top10: corr +0.003 (t +0.1); too few strong-imbalance cases
- 60s, top1: corr +0.039 (t +0.8); |imbalance|>0.6 n=118, gross +0.43 bp, spread 0.34 bp, net +0.09 bp
- 60s, top5: corr +0.043 (t +0.8); too few strong-imbalance cases
- 60s, top10: corr +0.010 (t +0.2); too few strong-imbalance cases
- 300s, top1: corr +0.113 (t +1.0); |imbalance|>0.6 n=22, gross +1.77 bp, spread 0.32 bp, net +1.45 bp
- 300s, top5: corr -0.039 (t -0.3); too few strong-imbalance cases
- 300s, top10: corr -0.098 (t -0.8); too few strong-imbalance cases

## TSLA: 23,400 seconds, typical spread 5.27 bp
- 10s, top1: corr -0.002 (t -0.1); |imbalance|>0.6 n=1126, gross +0.00 bp, spread 5.65 bp, net -5.65 bp
- 10s, top5: corr +0.015 (t +0.7); |imbalance|>0.6 n=363, gross -0.20 bp, spread 5.89 bp, net -6.09 bp
- 10s, top10: corr +0.017 (t +0.8); |imbalance|>0.6 n=251, gross +0.36 bp, spread 6.13 bp, net -5.77 bp
- 30s, top1: corr -0.030 (t -0.8); |imbalance|>0.6 n=394, gross -0.24 bp, spread 5.78 bp, net -6.02 bp
- 30s, top5: corr -0.018 (t -0.5); |imbalance|>0.6 n=123, gross +0.20 bp, spread 5.73 bp, net -5.53 bp
- 30s, top10: corr +0.020 (t +0.6); |imbalance|>0.6 n=78, gross +1.77 bp, spread 5.94 bp, net -4.16 bp
- 60s, top1: corr -0.019 (t -0.4); |imbalance|>0.6 n=199, gross -0.72 bp, spread 5.90 bp, net -6.61 bp
- 60s, top5: corr -0.097 (t -1.9); |imbalance|>0.6 n=62, gross -2.97 bp, spread 5.56 bp, net -8.54 bp
- 60s, top10: corr -0.026 (t -0.5); |imbalance|>0.6 n=41, gross -1.03 bp, spread 5.99 bp, net -7.02 bp
- 300s, top1: corr -0.137 (t -1.2); |imbalance|>0.6 n=38, gross -6.38 bp, spread 5.54 bp, net -11.92 bp
- 300s, top5: corr +0.102 (t +0.9); too few strong-imbalance cases
- 300s, top10: corr +0.110 (t +1.0); too few strong-imbalance cases

## Summary across stocks (average of per-stock results)
- 10s top1: mean corr +0.028, mean gross +0.06 bp, mean net after spread -2.13 bp (7 stocks)
- 10s top10: mean corr +0.016, mean gross -0.30 bp, mean net after spread -3.47 bp (5 stocks)
- 10s top5: mean corr +0.025, mean gross -0.05 bp, mean net after spread -3.02 bp (5 stocks)
- 30s top1: mean corr +0.035, mean gross +0.22 bp, mean net after spread -2.00 bp (7 stocks)
- 30s top10: mean corr +0.011, mean gross +0.36 bp, mean net after spread -4.24 bp (3 stocks)
- 30s top5: mean corr +0.013, mean gross -0.15 bp, mean net after spread -3.09 bp (5 stocks)
- 60s top1: mean corr +0.012, mean gross +0.07 bp, mean net after spread -2.13 bp (7 stocks)
- 60s top10: mean corr -0.028, mean gross -0.96 bp, mean net after spread -5.37 bp (2 stocks)
- 60s top5: mean corr -0.044, mean gross -1.19 bp, mean net after spread -5.15 bp (3 stocks)
- 300s top1: mean corr +0.028, mean gross -0.32 bp, mean net after spread -2.53 bp (6 stocks)

Reading it: a usable signal needs correlation clearly above zero AND net basis points above zero after the spread, consistently across stocks. One day on Nasdaq's own book (not the consolidated market).
