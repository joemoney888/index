# Test 4: pipeline false-positive calibration - first batch (21 Nov 2026)
Pre-registered in `search/CALIB/test4.py`. Gap-aware (fixed) engine, within-day bar-permutation null, n = 31,740 trials per run (the NAS100 family's own n), luck bar 5.05. Reference run on REAL data plus 10 shuffles. N +0.

| run | best train t (n>=500) | candidates | finalists |
|---|---|---|---|
| real data | 4.05 | 0 | 0 |
| shuffles 1-10 | 2.82, 3.20, 2.55, 2.72, 2.16, 2.23, 2.16, 3.55, 2.51, 2.68 (mean about 2.66, max 3.55) | 0 in each | 0 in each |

Pre-registered reading: 0 finalists in 10 shuffles -> run a second 10 (started). 0/10 bounds the false-finalist rate at about 26% (exact 95% upper bound 1 - 0.05^(1/10)); 0/20 would bound it at about 14%. Detects gross miscalibration only.
What the first batch says: (1) the search is NOT manufacturing finalists from structure-free data; (2) the nominal luck bar (5.05) is far above what the shuffled data reaches (max about 3.5), so the bar looks conservative for this family: real edges with train t of roughly 3.5-5 would be rejected. That is a statement about power, not a licence to lower the bar: any change must be registered in advance and counted; (3) the REAL-data best t (4.05) is above all 10 shuffles (rank 1 of 11, one-sided p about 0.09 by rank alone): weak, not significant, and it did not become a candidate; it may reflect real intraday structure that the realistic-fill search cannot turn into a validated finalist. No action is taken on it.
Caveats: the null preserves daily candles, so it does not test daily-scale families; only 10 shuffles; the bar-quadruple permutation is one choice of null.
