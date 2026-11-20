# Harmonics, Elliott, cycles and the index spread trade (train and validation only; exam untouched)

All use the same data (NAS100, SPX500, US30, 5-minute bars, real spreads), costs and exits as the main engine, confirmed swing points only (no hindsight), and count every variant.

| Test | Variants (N) | Luck bar | Best train t (>=500 trades; spread >=300) | Average train t | Passing the bar |
|---|---|---|---|---|---|
| Harmonic (Gartley, Bat, Butterfly, Crab, Cypher), ABCD, three drives, Elliott impulse rules | 112,307 | 5.32 | 3.64 | -0.95 to -1.52 by pattern | 0 |
| Cycle lines (dominant-cycle phase, FFT) | 2,201 | 4.43 | 0.43 | -3.68 | 0 |
| Index spread trade (NAS100/SPX500/US30 pairs, both legs' costs) | 9,566 | 4.78 | 1.17 | -1.11 | 0 |

Notes
- Bat, Butterfly, Crab and three-drives rarely appear often enough to reach 500 trades, so they cannot be judged.
- The closest result was the Cypher pattern following the textbook direction with K=6 (train t about 3.6; validation t 0.6 to 1.8 on about 170 trades; below the +2.0 validation bar and the luck bar). All of its top variants share the same entries, so it is effectively ONE hypothesis. Not a finalist; at most a candidate to watch.
- The spread trade has no edge even before costs (gross average t -0.23 on 120 variants); with both legs' spreads it is clearly negative.
- Elliott was tested only as simple, objective rule checks (wave 2 not beyond the start, wave 3 not the shortest, wave 4 not overlapping wave 1), not as a subjective wave count.

Verdict: nothing found in any of these families.
