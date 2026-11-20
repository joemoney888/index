# Runner exit test (train + validation only; exam untouched)

Idea: on the FIRST trade of each UTC day, bank half at +1R (stake back), move the stop on the rest to breakeven (or the trailing stop if higher), no target, hold to the end of the session. All other trades unchanged. One hypothesis tested on the existing NAS100 rule; the same on the unfitted SPX500 and US30 copies.

| Market | Period | Base mean R (t) | Runner mean R (t) | Base sum R | Runner sum R |
|---|---|---|---|---|---|
| NAS100 | train | +0.042 (5.31) | +0.042 (5.37) | 249.2 | 251.7 |
| NAS100 | validation | +0.033 (2.26) | +0.033 (2.25) | 54.2 | 53.8 |
| SPX500 | train | +0.014 (1.86) | +0.015 (1.90) | 84.6 | 86.2 |
| SPX500 | validation | +0.018 (1.16) | +0.017 (1.12) | 28.9 | 27.7 |
| US30 | train | +0.014 (1.85) | +0.015 (1.89) | 85.2 | 86.9 |
| US30 | validation | +0.029 (2.12) | +0.030 (2.14) | 51.5 | 52.0 |

Result: no meaningful difference. Verdict: not worth adding. Code stays as an off-by-default option (`run`) in agent/search.py.
