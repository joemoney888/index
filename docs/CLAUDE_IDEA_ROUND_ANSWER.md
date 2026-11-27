# Claude Sonnet 5.5's own answer to the idea review round and the options question (23 Nov 2026, committed after the PM confirmed the prompts were sent at 20:10 UTC, per amendment (a)). Unscored side round. Nothing here was run; all figures are rough estimates and marked.

## Options versus CFDs (Idea 8), short answer
1. Wrapping a signal in options does not make the signal real; it changes payoff shape and cost. None of the failed or unconfirmed signals would pass.
2. Real world for a small UK account, my view (not tax advice; general knowledge, unverified for current broker terms): options on US indexes (XND/SPX style) have large contract sizes for a small account, wider spreads in percentage terms, assignment risk on American-style stock options, and a defined maximum loss for spreads and puts. CFDs are granular, cheap to size, and carry financing and gap risk. Covered calls and collars need the underlying (shares or an ETF); PMCC and verticals need option-chain quotes with real spreads. The honest edge available from options is the premium for selling insurance, which historically shows lower volatility and drawdown but not reliably higher risk-adjusted return, and the Cboe indexes are hypothetical.
3. Free testable route: Cboe strategy-index histories (BXM, PUT, CLL, PPUT, CLLZ) versus the S&P 500, N +5, risk-adjusted metric. PMCC and verticals need paid option history.
4. Verdict: worth one cheap registered test of the Cboe indexes only if the PM wants the "options do not rescue it" fact in the write-up; otherwise not worth it. Probability it overturns the project's null: low.

## Part A: the open ideas (one line each)
- Idea 1 fade: maybe. The breakout came out +0.077R, t 2.45; a fade is the mirror image so it would be negative, and would cost N +1 to confirm a known-bad direction. No.
- Idea 1 pullback entry: maybe, low prior (about 3 percent); needs about 1,000 trades, detectable about 0.09R.
- Ideas 2, 3, 4 / 14 (needs 1-minute data): maybe for 3 (cross-index divergence has a real mechanism); no for 2 and 4 (many free parameters, ICT-style, trade counts too low). The 2013-2020 free 1-minute data gives about 1,800 days.
- Idea 7 (Kelly sizing): no until a signal survives; sizing multiplies an edge.
- Idea 8: see above, maybe.
- Idea 9 (constituent pre-market): no; no free pre-market history for constituents and the information is mostly in index futures already.
- Idea 10 (daily 200-day trend): yes, cheapest and well powered on 20+ years; but expect a null on risk-adjusted terms.
- Idea 11 (valuation tilt): maybe; needs CAPE history (free) and has few independent observations (valuation moves over decades).
- Idea 12 (vol targeting): yes as a test of risk-adjusted return on buy-and-hold, published support (verify), about 20 years daily.
- Idea 16: not a test.

## Part B: three new ideas (my own). Each has a low prior; none is a rescue.
1. **Turn-of-the-month effect.** Rule: hold the index from the close of the last trading day of the month to the close of the 3rd trading day of the next month, otherwise cash. Why it might be real: documented in US and international data (Ariel 1987; Lakonishok and Smidt 1988; McConnell and Xu 2008; all unverified from memory), plausibly from pension and payday flows. Data: daily index history (OANDA 2005 to 2026 plus Kaggle), about 250 months. Detectable at t 2.8 with a window SD near 3 percent: about 0.5 percent per month (rough). N +1. Prior about 5 percent that it is tradable after costs.
2. **Overnight versus intraday split.** Rule: hold long only close-to-open (overnight), never intraday, versus the reverse. Why: published work finds a large share of equity returns accrue overnight (Cooper, Cliff and Gulen 2008; Lou, Polk and Skouras 2019; unverified). Data: our 5-minute bars 2016-2026 give about 2,600 days; detectable about 4 bp per day (rough). Catch: CFD overnight financing is about 1 bp or more per day and spreads at the close, so the cost may exceed the effect. N +1. Prior low.
3. **Third-Friday option-expiration week.** Rule: compare index returns in expiration week versus other weeks, long only the expiration week or only the days after expiration. Why: pinning and hedging flows (Stoll and Whaley 1987; Ni, Pearson and Poteshman 2005; weak in recent data, unverified). Data: about 250 expiration weeks in 20 years; detectable about 1 percent per week (rough). N +1. Prior very low.

## Part C
Test first: Idea 10 or Idea 12 (daily, 20+ years, well powered, cheap), because they answer whether a simple, published rule beats buy-and-hold on risk-adjusted terms with enough data; expected result is "no" or "same return, smaller drawdown", which is itself a useful documented outcome.
