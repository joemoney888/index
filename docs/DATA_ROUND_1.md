# Data sourcing round 1 (23 Nov 2026) - SCORED, all three players

Task: find the best source of longer, cleaner intraday US index history for a small private researcher. No trial count (N) is spent.
Players: GLM 5.3, ChatGPT 6, Claude Sonnet 5.5. Scorer: the PM, with Claude Sonnet 5.5 committing the replies and checking links and prices. Blind cross-scoring as in earlier rounds, wording unchanged.

## Prompt (exactly as sent to GLM and ChatGPT 6)
See the prompt text the PM sent: Step 1 (what you can and cannot check), Step 2 (up to 5 sources, each with link, instruments, bar size, first and last date, price with date seen, licence and redistribution, download method, data-quality problems, one reason to distrust it). Rules: every claim needs a checkable link or "unverified"; an invented source or price scores -2; no sign-ups, accounts, terms or payments on anyone's behalf; no API keys; an honest short answer beats a padded one; no strategy ideas.

## Rubric (0-2 each, total /10, minus 2 for any invented source or price)
a. Sources are real and the link is correct and checkable.
b. Details are accurate (dates covered, bar size, price with date seen, free-tier limits).
c. Licence and redistribution are stated correctly (our repo is public).
d. Honest about what was and was not checked ("unverified" where not checked; no padding).
e. Fit to our need: 1- or 5-minute US index/ETF/futures history before 2021 with usable data-quality notes.
Speed rule from the league applies: response time counted from the moment the PM sends the prompt (10 minutes or less none, over 10 to 20 minus 1, over 20 minus 2).

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

## Response-time log (23 Nov 2026, UTC)
- ChatGPT 6: prompt sent about 00:40, reply about 00:45 (about 5-6 minutes, no penalty; send time not logged exactly).
- GLM 5.3: first session restarted by the PM; clock counted from the resend to the fresh session, sent 00:46 UTC (the PM's word "now" at 00:46). Reply time to be logged on arrival.
- GLM reply received about 00:49 UTC (about 3 minutes from the 00:46 resend). Both replies are recorded verbatim with Claude checks in docs/REPLIES_FROM_GLM.md and docs/REPLIES_FROM_GPT6.md. Provisional: GPT6 9/10, GLM 8/10, Claude sealed entry not self-scored (to be scored blind). Final scoring pending.

## RESULT (23 Nov 2026, about 01:10 UTC)
Key (held in the private repo until all blind scores were in): Set P = Claude Sonnet 5.5, Set Q = ChatGPT 6, Set R = GLM 5.3.

| Player (set) | Scored by | Scores | Average |
|---|---|---|---|
| ChatGPT 6 (Q) | GLM 5.3 (blind), Claude Sonnet 5.5 (provisional, not blind) | 9, 9 | **9.0** |
| GLM 5.3 (R) | ChatGPT 6 (blind), Claude Sonnet 5.5 (provisional, not blind) | 5, 8 | **6.5** |
| Claude Sonnet 5.5 (P) | ChatGPT 6 (blind), GLM 5.3 (blind) | 5, 6 | **5.5** |
Claude Sonnet 5.5 did not score its own set.
Rank: 1st ChatGPT 6 (5 points), 2nd GLM 5.3 (3), 3rd Claude Sonnet 5.5 (1). Speed: nobody over 10 minutes, no deductions.
Contested item: ChatGPT 6 applied a -2 "price penalty" to GLM's set because the Kibot ES figure of $110 was not on the page it checked. Claude's reading of the rubric is that -2 is for an INVENTED price; an unconfirmed price is a lower accuracy score, not necessarily an invention. GLM's blind scoring and errata did not substantiate $110 either (it verified $125 and $135 examples only). Without the penalty GLM would average 7.5 instead of 6.5. The ranking is the same either way.
Errors found and acknowledged by the players:
- GLM errata: Databento start is 2010-06-06 (not March 2017); Kibot download access is one year from the last purchase (not 45 days); FirstRate updates are $79.95 per month for the complete bundle and $99.95 per YEAR for single tickers; FirstRate licence page was findable.
- GPT6 errata: Kibot example prices are dated 9 Oct 2026 on the page; GLM also found that the "one year of free intraday data" claim is not on the free-data page (two-week samples for 686 tickers) and that the $59.95/month index-bundle update price was not confirmed.
- Claude Sonnet 5.5 errata (reviewers' findings; Claude has not independently verified the two Polygon/Alpaca points): Alpaca's free plan is IEX with 7+ years of history (so "from about 2016" and "delayed consolidated data" were wrong); Polygon's free tier is end-of-day per its own site (so "about 2 years of free minute data" was wrong); the sealed list gave no links, which the prompt required. Right on: Databento back to about 2010, Dukascopy free index data exists.
Process note (Claude Sonnet 5.5): the approved amendment (a) says Claude commits its own work only AFTER the prompt is sent, on the same clock. In this round Claude committed its sealed entry BEFORE the prompt was sent (00:38 UTC; prompt about 00:40). That breaks amendment (a). It did not change any score or time deduction (Claude's entry took about 2 minutes of work either way), but it is recorded as a Claude process error.
Practical takeaway for the PM: nothing has been bought or downloaded. Databento reaches back to 2010 with bid/ask, Kibot and FirstRate are the cheap long-history routes, and neither Kibot nor FirstRate allows raw data in the public repo. Open the Kibot pages yourself to confirm prices before spending anything.
