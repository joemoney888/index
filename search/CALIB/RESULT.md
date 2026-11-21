# Test 4: pipeline false-positive calibration - first batch (21 Nov 2026)
Pre-registered in `search/CALIB/test4.py`. Gap-aware (fixed) engine, within-day bar-permutation null, n = 31,740 trials per run (the NAS100 family's own n), luck bar 5.05. Reference run on REAL data plus 10 shuffles. N +0.

| run | best train t (n>=500) | candidates | finalists |
|---|---|---|---|
| real data | 4.05 | 0 | 0 |
| shuffles 1-10 | 2.82, 3.20, 2.55, 2.72, 2.16, 2.23, 2.16, 3.55, 2.51, 2.68 (mean about 2.66, max 3.55) | 0 in each | 0 in each |

Pre-registered reading: 0 finalists in 10 shuffles -> run a second 10 (started). 0/10 bounds the false-finalist rate at about 26% (exact 95% upper bound 1 - 0.05^(1/10)); 0/20 would bound it at about 14%. Detects gross miscalibration only.
What the first batch says: (1) the search is NOT manufacturing finalists from structure-free data; (2) the nominal luck bar (5.05) is far above what the shuffled data reaches (max about 3.5), so the bar looks conservative for this family: real edges with train t of roughly 3.5-5 would be rejected. That is a statement about power, not a licence to lower the bar: any change must be registered in advance and counted; (3) the REAL-data best t (4.05) is above all 10 shuffles (rank 1 of 11, one-sided p about 0.09 by rank alone): weak, not significant, and it did not become a candidate; it may reflect real intraday structure that the realistic-fill search cannot turn into a validated finalist. No action is taken on it.
Caveats: the null preserves daily candles, so it does not test daily-scale families; only 10 shuffles; the bar-quadruple permutation is one choice of null.

**Second batch (shuffles 11-20): not completed.** The background runs only progress while the session is active; both pauses (night, morning) stopped them after about 6,000 of 31,740 trials on shuffles 11-12, and no result was produced. The reading therefore stays at 0 false finalists in 10 shuffles (95% upper bound about 26% on the false-finalist rate) plus the real-data reference. Finishing the second batch would only tighten that bound to about 14%; it would take about 80 minutes of active session time. Decision pending with Joe.

## FINAL (21 Nov 2026, 14:37 UTC): second batch completed - 20 shuffles
Supersedes the "not completed" note above. 20 shuffles + 1 real-data reference, all on the gap-aware engine, n = 31,740 trials each, bar 5.05.
- False finalists: **0 in 20 shuffles**, 0 candidates (95% upper bound on the false-finalist rate about 14%, by the rule of three; exact 1 - 0.05^(1/20) = 13.9%).
- Best train t (n >= 500) over the 20 shuffles: mean 2.61, SD 0.42, range 2.16 to 3.55. The luck bar (5.05) sits about 5.8 SD above the shuffled mean: the bar is very conservative for this family.
- REAL data: best t 4.05, higher than all 20 shuffles (rank 1 of 21; one-sided p about 0.05 by rank; about 3.4 SD above the shuffled mean on a rough normal approximation). It did not become a candidate (4.05 < 5.05) and no validation result was recorded for it.
Reading (pre-registered): 0/20 -> pipeline calibrated within detection power: it does not manufacture finalists from structure-free intraday data. Every earlier family null stands. The real-data excess (4.05 vs max shuffle 3.55) is weak evidence that the real series contains some intraday structure the realistic-fill search could not convert into a validated rule; no action taken, no N counted, and any follow-up (for example a registered lower bar for this family) must be pre-registered and counted before it is looked at.
Limits: within-day bar-permutation null only; it does not test daily-scale families; 20 shuffles detect only gross miscalibration.
