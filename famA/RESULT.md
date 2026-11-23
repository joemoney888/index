# Family A result (spec v1.1), run once

Window 2021-05-20 to 2026-11-17, 1434 weekdays. Data sha256 1ff22b6fa4c2d9f3...

| Spec | n used | skips | net mean bp | t (NW5) | gross mean bp | T1 / T2 / T3 net bp | rule a | rule b | rule c | PASS |
|---|---|---|---|---|---|---|---|---|---|---|
| A5 | 1366 | {'calendar': 63, 'under78': 3, 'missing': 1, 'zero signal': 1} | -3.34 | -1.07 | -2.93 | -5.50 / -1.90 / -2.55 | False | False | False | False |
| A6a | 1368 | {'calendar': 63, 'under78': 3} | -1.70 | -2.09 | -1.31 | -3.19 / -1.22 / -0.63 | False | False | False | False |
| A6b | 1363 | {'calendar': 63, 'zero signal': 5, 'under78': 3} | +0.22 | +0.27 | +0.60 | +2.91 / -1.61 / -0.74 | False | False | False | False |

Correlation of the A6a and A6b daily net series: -0.032.
Opposite-direction significant (t <= -2.8): A5: False, A6a: False, A6b: False
