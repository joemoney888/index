# Data sourcing round 1 (23 Nov 2026) - SCORED, all three players

Task: find the best source of longer, cleaner intraday US index history for a small private researcher. No trial count (N) is spent.
Players: GLM 5.3, ChatGPT 6, Claude Sonnet 5.5. Scorer: Joe, with Claude Sonnet 5.5 committing the replies and checking links and prices. Blind cross-scoring as in earlier rounds, wording unchanged.

## Prompt (exactly as sent to GLM and ChatGPT 6)
See the prompt text Joe sent: Step 1 (what you can and cannot check), Step 2 (up to 5 sources, each with link, instruments, bar size, first and last date, price with date seen, licence and redistribution, download method, data-quality problems, one reason to distrust it). Rules: every claim needs a checkable link or "unverified"; an invented source or price scores -2; no sign-ups, accounts, terms or payments on anyone's behalf; no API keys; an honest short answer beats a padded one; no strategy ideas.

## Rubric (0-2 each, total /10, minus 2 for any invented source or price)
a. Sources are real and the link is correct and checkable.
b. Details are accurate (dates covered, bar size, price with date seen, free-tier limits).
c. Licence and redistribution are stated correctly (our repo is public).
d. Honest about what was and was not checked ("unverified" where not checked; no padding).
e. Fit to our need: 1- or 5-minute US index/ETF/futures history before 2021 with usable data-quality notes.
Speed rule from the league applies: response time counted from the moment Joe sends the prompt (10 minutes or less none, over 10 to 20 minus 1, over 20 minus 2).

## Claude Sonnet 5.5 sealed answer (committed BEFORE the prompt was sent)
Step 1: I can search and fetch public pages but my sandbox blocks Yahoo, FRED, Stooq, Shiller and most data sites. Everything below is from memory and is UNVERIFIED: no link has been opened, no price checked.
Candidates, best first (all unverified):
1. Dukascopy historical data feed: free downloads of tick and 1-minute data for index CFDs (US 500, US Tech 100, US 30). I believe coverage starts in the early 2010s. Personal use only; not for redistribution (do not commit to the public repo). Distrust: CFD quotes from one broker, so the same type of data we already hold.
2. Alpaca market data: stock and ETF minute bars (SPY, QQQ, DIA). I believe the free tier gives IEX-only data from about 2016 and delayed consolidated data. Distrust: IEX-only volume is a small share of the market, and limits change.
3. Polygon.io: US stock and ETF minute bars; I believe the free tier covers about 2 years and paid tiers go back much further. Prices unverified. Distrust: terms bar redistribution.
4. Databento: pay-as-you-go CME futures (ES, NQ, YM) back to about 2010. I believe new accounts get free credit. Distrust: cost grows with the amount downloaded; I have not checked prices.
5. FirstRate Data: one-off purchase of historical 1-minute index, ETF and futures packages. Prices unverified. Distrust: small vendor; roll and adjustment conventions must be read before use.
Not found by me: any free source of exchange-grade 1-minute data before 2010. Daily history from the 1990s onward exists from FRED, Shiller and Stooq but I cannot reach them.
Honest summary: I can name where to look; I cannot verify any of it. Whoever verifies links and prices should score higher than this list.
