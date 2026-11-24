# Idea 8 (Joe): options vs plain index, zero-N descriptive look at the Cboe BuyWrite index (24 Nov 2026)
Data: Cboe BXM daily close 2002-03-22 to 2026-11-23 (supplied by Joe, stored outside the repo) vs official S&P 500 price index, common days to 2026-11-20 (6,205). Descriptive only, NOT a test, N unchanged (941,555). BXM is a hypothetical covered-call index (long the index, sell one-month at-the-money calls); it ignores real option spreads, margin and taxes. Whether BXM counts dividends is unverified by me; the S&P comparison is the price index.

| Period | BXM CAGR | S&P CAGR | BXM vol | S&P vol | BXM max drawdown | S&P max drawdown |
|---|---|---|---|---|---|---|
| 2002-2026 | 5.8% | 7.6% | 13.7% | 19.0% | -40% | -57% |
| 2002-2012 | 4.1% | 2.0% | 15.4% | 21.4% | -40% | -57% |
| 2013-2026 | 7.0% | 11.8% | 12.3% | 16.9% | -30% | -34% |
| 2020-2026 | 6.5% | 11.5% | 14.6% | 20.2% | -30% | -34% |

Return per unit of risk (mean/SD, annualised, no risk-free): 0.48 vs 0.48 over the whole period; 2013-26 0.62 vs 0.75. On S&P down days BXM averages -47 bp vs -81 bp; on up days +44 bp vs +76 bp (correlation 0.91). Worst day: BXM -12.2%, S&P -12.0% (both in March 2020): the covered call did not protect against the worst day.
Reading: the covered call is the same market exposure with about 70% of the swings and about 70% of the gains; it did better only in the flat/falling 2002-2012 stretch, and worse in the long rally since. It reduces risk, it did not add return per unit of risk, and in the recent period it lagged. This does not create a trading edge for a CFD strategy, as noted in Idea 8's first look. A real small-account version would also pay option spreads this index ignores.
