# Review of BFG's trading on Mon 23 Nov 2026 (Claude Sonnet 5.5, written 20:30 UTC at Joe's request). From logs/index_events.csv; nothing re-run.

Joe's observation: the agent was poor today; NAS100 and SPX500 had big up days (Nvidia rebound and the CEO being reinstated, confirmed below), the agent was slow to see the direction and was caught short in both markets when it should have been long.

## What the log shows
- Orders placed today: 33 (11 each in NAS100, SPX500, US30). ALL 33 were short (side -1). No long was taken in any market all day.
- Result of the trades that opened and closed today (R = P&L / the 1R risk of about GBP 5.0 to 5.2 per trade, compounding sizing on): NAS100 11 trades, -0.98R (-GBP 5.34), 5 wins 6 losses; SPX500 11 trades, -0.69R (-GBP 3.99), 5 wins 6 losses; US30 11 trades, +0.19R (+GBP 0.55), 6 wins 5 losses. Total about -1.5R (about -GBP 8.8, roughly 1.7 percent of a GBP 500 account). Not a disaster in size: stops are about 1R and size is small.
- NAS100 path from the agent's own entries: 26,558 at 14:01 UTC, 26,426 low at 14:41, 26,984 at 15:21 (about +1.7 percent from the early level), 26,770 at 17:56. SPX500 7,185 to 7,281 (+1.3 percent). A broad up move with pullbacks.
- Speed was not the issue. Example: the 14:01 shorts in NAS100 and SPX500 were stopped out at 14:02 to 14:04, within about 1 to 3 minutes of entry. The agent reacts within one 5-minute cycle by design.

## Why it was short all day
BFG is a mean-reversion (fade) agent. It sells after an up-extension and buys after a down-extension. On a day that trends up it keeps selling the dips of a rising market, hits stops, and re-enters short. It has no news feed and no trend-day filter, so it cannot know a rally is driven by a catalyst; "should have been long all day" is true in hindsight only.

## What it means for the project
1. One day is not evidence. The earlier day (-5.6 percent index day) gave +4.6R from 8 trades; today gave about -1.5R. Both fit "no demonstrated edge" (realistic backtest about -0.01R per trade). A fade agent profits on chop and loses on trend days; the test is whether it wins more than it loses over a long run, not on any one day.
2. News or trend-day awareness is a NEW rule, not a tweak. Fixes people suggest after a bad day (follow the first-hour move, switch to long on a catalyst, stand aside on trend days) have to be registered and tested on history before use, each costing N. Family A already tested the closest published version (first-half-hour momentum predicting the last half-hour): it failed.
3. A news feed cannot be tested on our history (we have no timestamped news data), so a news-driven switch cannot be honestly back-tested. That is a real limit, not a to-do.
4. Cheap, honest next step if Joe wants one: log, but do not trade, a "trend-day flag" (for example the morning move beyond a set number of ATRs) alongside each day's R, and look at it after 60 or more days; any rule built from it would still need a registration.

## Cause of the move: CONFIRMED (correction at 20:25 UTC; my first two searches returned stale 9-18 Nov pages and I wrongly treated their silence as "no reinstatement")
Nvidia's 8-K of 23 Nov 2026 and same-day coverage (Reuters, CNN, Yahoo Finance) confirm: the board voted unanimously to reinstate Jensen Huang as President, CEO and director effective immediately, 11 days after his resignation. Nvidia shares rose about 30 percent (premarket about 28 percent); Reuters at 12:31 ET had the Nasdaq up nearly 7 percent and CNN said all three indexes were on track for their best day since April 2025. So Joe was right: this was a huge, news-driven trend day. The agent's own shorts (33 of 33) were against it; the small loss (-1.5R) came from stops, not from the agent being right.
How the news reached the agent: it did not. BFG reads 5-minute prices only. My own news access is web search of public pages (no Bloomberg, no terminal), which lags and can miss today's articles unless the query is aimed at the event.
