# Slow trend-following family (train only so far; validation and exam untouched for the promising; none promising)

Daily bars from the 5-minute data on NAS100, SPX500, US30, GER40, UK100 (equal-weighted), train period 2021-05 to about Nov 2024. Variants: N-day breakout or N-day average, N 20-200, long-only or long+short, trailing stop 0-6 ATR.
Costs: half-spread on each change, financing 6.5%/yr long and 3%/yr short (estimates). Score: weekly TIMING ALPHA versus holding the index at the same average exposure (the benchmark pays the same financing), t-stat over weeks.

- Variants tried: **2,000** (seed 1). Luck bar: sqrt(2 ln N) + 0.5 = **4.40**.
- Best train t: **0.84**. Average train t: **-0.82**. Nothing reached even 1.5, so nothing went to validation.

Reading: on these indices in this period, slow trend rules did not beat simply holding the index once financing and spreads are paid, and mostly did worse. The 30 Mar to 4 May style move is easy to see in hindsight but the rules that tried to catch it also took the whipsaws.
