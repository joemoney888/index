# Text to add to the next reviewer prompt (from Joe via Claude Sonnet 5.5, 23 Nov 2026 20:20 UTC)

Add this block after the list of open ideas:

```
Idea 17 (Joe): the live paper agent needs a news feed, at least for pre-market, the open and the close, with those reports scored into how the agent reads moves. Trigger: on 23 Nov 2026 Nvidia reinstated its CEO and the Nasdaq rose about 7 percent; the agent (an intraday mean-reversion fader, no news input, 5-minute prices only) took 33 short trades out of 33 and lost about 1.5R. Joe's point: in the real world it left too much on the table and did not perform; this is a game, but building a loser is not part of the game.
Questions: (1) Is a scored news layer a credible way to stop a fader being run over on catalyst days, and what is the simplest version (stand aside, long-only, wider stops)? (2) We have no timestamped news history, so what free or cheap timestamped sources exist (SEC 8-K times, FOMC statements, economic calendars, GDELT, others) and how reliable are they? (3) How can the score be tested without look-ahead, given that a language model scoring old headlines may already know the outcome? We propose a forward, log-only test first; is that sound, and how many days are needed to detect a direction hit rate above chance at t >= 2.8? (4) Name the main ways this fails (latency, headline noise, overfitting to one day) and give your honest probability it adds value after costs. (5) Do not recommend real money; state uncertainty; mark unverified sources.
```
