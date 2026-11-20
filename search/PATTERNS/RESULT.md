# Chart patterns as numbers (M and W, head and shoulders, triangles) - train and validation only; exam untouched

Swing points are used only K bars after they happen (no hindsight). NAS100, SPX500 and US30 pooled, 5-minute bars, real spreads, same exits and cost logic as the main engine. Rules tried: double top/bottom (M/W), head and shoulders (and inverse), symmetrical-triangle breakout; each either following the textbook direction or fading it; trigger at confirmation or at the neckline/line break; K 6-48 bars, tolerance 0.3-1.5 ATR, depth 1-3 ATR, random exits and session hours.

- Variants tried: **21,684** (2-minute run, seed 10). Luck bar: sqrt(2 ln N) + 0.5 = **4.97**.
- Best TRAIN t among variants with at least 500 trades: **2.97**. The 4.75 maximum came from tiny samples and means nothing.
- Average TRAIN t by pattern (variants with >=500 trades): double top/bottom -1.84, head and shoulders -1.32, triangle -1.90. Below zero = costs eat random-looking entries, as in every other family.
- The three variants above t 2.5 were checked on validation: t -0.07, +0.52, -2.33. None passes (needs >= +2.0).
- Candidates passing the luck bar: **0**. Finalists: **0**. Nothing goes to an exam.

Reading: quantified M/W, head-and-shoulders and triangle rules have no measurable edge on these indices after costs. Harmonic (XABCD, Cypher, ABCD, three drives), Elliott waves and cycle lines are not yet tested here; they would multiply the variant count and, given these results, are low odds.
