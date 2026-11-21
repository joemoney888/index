# Long-term test - frozen BEFORE running (21 Nov 2026). Data: Damodaran annual returns 1928-2025 (S&P 500 total return, 3m T-bill, 10y T-bond).
Strategies (decide at end of year t-1 using only year t-1 and earlier, earn year t):
 BH   : 100% stocks.  6040: 60% stocks/40% bonds rebalanced yearly.
 TR   : stocks if prior-year stock return > prior-year T-bill return, else T-bills (crude yearly trend rule, one parameter-free rule).
Cost: 0.10% of portfolio per switch for TR (0.50% as sensitivity). BH/6040 free.
Claim to test: TR beats BH on CAGR. Pass only if TR CAGR - BH CAGR > 0 AND stationary block-bootstrap (block 5, 10,000 draws, seed 1) 95% CI of mean annual difference excludes 0 AND same sign in both halves (1928-1976, 1977-2025).
Otherwise: no evidence TR beats BH. Report also drawdown/Sharpe (descriptive only). N +1 (counts against the +6 cap).

## RESULT (run once, 21 Nov 2026; run.py, data.csv)
TR CAGR 6.8% vs buy-and-hold 9.7% (diff -3.0 pts; -3.1 at 0.5% cost); bootstrap 95% CI of the mean annual difference (-6.3, -1.4) pts, entirely below zero; worse in both halves (-2.8, -3.1). Verdict: FAIL, no evidence the yearly trend rule beats buy-and-hold; it was reliably worse on return. Descriptive: max drawdown TR -36% vs BH -65% vs 60/40 -40%; Sharpe TR 0.31, BH 0.42, 60/40 0.44. 60/40 CAGR 8.2%.
Caveats: yearly data only (97 observations, one rule), one market (US, survivorship of the winning country), valuation tilt NOT tested (table has no valuation data), daily 200-day rule NOT tested.
