# Data sourcing round 1: BLIND PACKET (23 Nov 2026)

Three anonymous answers (Sets P, Q, R) to the same prompt (docs/DATA_ROUND_1.md). Wording is unchanged except that tracking tags, browser-chip lines and favicon image lines were removed, and one repo nickname was made neutral. Order and letters were randomised; the key is not in this repo.

Scoring instructions: say which set is yours, then score ONLY the other two on the rubric in docs/DATA_ROUND_1.md (a-e, 0-2 each, total /10, minus 2 for any invented source or price). Check what you can and say what you verified and what you could not. Give a short reason per item. Do not guess authorship of the other two.

## Set P

Step 1: I can search and fetch public pages but my sandbox blocks Yahoo, FRED, Stooq, Shiller and most data sites. Everything below is from memory and is UNVERIFIED: no link has been opened, no price checked.
Candidates, best first (all unverified):
1. Dukascopy historical data feed: free downloads of tick and 1-minute data for index CFDs (US 500, US Tech 100, US 30). I believe coverage starts in the early 2010s. Personal use only; not for redistribution (do not commit to the public repo). Distrust: CFD quotes from one broker, so the same type of data we already hold.
2. Alpaca market data: stock and ETF minute bars (SPY, QQQ, DIA). I believe the free tier gives IEX-only data from about 2016 and delayed consolidated data. Distrust: IEX-only volume is a small share of the market, and limits change.
3. Polygon.io: US stock and ETF minute bars; I believe the free tier covers about 2 years and paid tiers go back much further. Prices unverified. Distrust: terms bar redistribution.
4. Databento: pay-as-you-go CME futures (ES, NQ, YM) back to about 2010. I believe new accounts get free credit. Distrust: cost grows with the amount downloaded; I have not checked prices.
5. FirstRate Data: one-off purchase of historical 1-minute index, ETF and futures packages. Prices unverified. Distrust: small vendor; roll and adjustment conventions must be read before use.
Not found by me: any free source of exchange-grade 1-minute data before 2010. Daily history from the 1990s onward exists from FRED, Shiller and Stooq but I cannot reach them.
Honest summary: I can name where to look; I cannot verify any of it. Whoever verifies links and prices should score higher than this list.

---

## Set Q

## **Step 1 — What I can check**

I can access public websites and documentation live, including vendor product pages, pricing pages and published licence terms. I cannot inspect private account dashboards, test authenticated downloads, verify the contents of a paid data file, or confirm that a vendor will grant a particular licence without contacting them.

I’ll distinguish information visible on public pages now from anything I cannot verify. I will not sign up, accept terms or purchase data.

## **Step 2 — Best sources found**

I found **two credible, relevant vendors**. Neither offers a licence that permits putting the raw purchased data in our public GitHub repository. I did not find a convincing free source of multi-year, pre-2021, exchange-quality one-minute data.

### **1. Kibot — strongest match for long ETF and futures history**

**Links:** [Kibot data catalogue](https://www.kibot.com/buy.html) · [custom order and live quote](https://www.kibot.com/custom-order.html) · [quality and coverage](https://www.kibot.com/quality/update-timing-and-quality-checks.html)

- **Instruments and dates:** US stocks, ETFs and indices have one-minute history from 1998 in the vendor's archive; individual instruments begin at their first available record or listing date. Continuous ES and NQ futures start **27 September 2009**; YM is also in the futures catalogue. The futures catalogue lists individual contracts as well as continuous series.

- **Bid/ask:** One-minute bid/ask is available for a top-50 ETF package from 2009, including SPY, QQQ and DIA. The listed price is **$680 one-time**. Continuous futures also have bid/ask coverage from September 2009.

- **Price:** The custom-order page displayed an example of **SPY + QQQ, full-history, one-minute bars for $125**, and ES + NQ one-minute bars since 2009 for $135. These are example quotes, not a guaranteed quote for a different combination or date range. The prices page also lists the broad continuous-and-individual-futures one-minute package at **$820 one-time**. Prices checked **23 November 2026**.

- **Free access:** Free daily US-stock/ETF data and small intraday samples are available. The one-minute samples are IBM and OIH, not SPY/QQQ; bid/ask samples are IVE and WDC. So the free files do not let you validate the target instruments' full history.

- **Licence:** Personal/internal use only; the licence explicitly prohibits resale, redistribution and transfer. **Do not commit raw files to the public repo.** Derived aggregate statistics and backtest summaries may be shared.

- **Download:** CSV files through the vendor's download service, FTP, desktop agent or API. Timestamps default to US Eastern Time; sessions can include pre-market and after-hours unless filtered.

- **Quality caveat:** Kibot documents gap checks and repairs, but says tick prints are not automatically filtered; real, uncancelled extreme prints remain. Its own documentation disclaims guarantees of accuracy and completeness.

- **Reason to distrust:** It is vendor-aggregated historical data, not a substitute for checking sample bars against an independent exchange-grade source. Continuous futures also require careful inspection of the roll construction and adjustment convention.

**Assessment:** Best apparent value for a longer ETF/futures test, especially if the $125 SPY+QQQ example is representative. The 2009 futures history is useful, but it is not a 20-year futures dataset.

### **2. FirstRate Data — strongest direct-index and ETF coverage**

**Links:** [SPY data page](https://firstratedata.com/i/etf/SPY) · [US index bundle](https://firstratedata.com/b/8/us-index-historic-intraday) · [licence](https://firstratedata.com/about/license) · [free intraday data](https://firstratedata.com/free-intraday-data)

- **Instruments and dates:** SPY one-minute, five-minute and daily bars are listed from **3 January 2000**. The US index bundle lists one-minute and five-minute data from **January 2008**, with 115 major US indices, including DJI; the individual SPX page lists data from **2 January 2008**. The vendor also lists ETF history from 2000 and individual futures history from 2008.

- **Bid/ask:** I found no evidence on the pages checked that the SPY or index minute-bar products include historical bid/ask spreads. Treat these as OHLC bars, not quote data.

- **Price:** Paid product; **the initial purchase price was not visible in the pages I could inspect**, so it is unverified. The index bundle page lists $59.95/month for updates after its included first month; the SPY page lists an annual $99.95 update subscription after its included first month. Those are update charges, not the initial data price.

- **Free access:** The vendor advertises one year of free intraday data for selected popular datasets, including SPY, QQQ, DIA and the SPX/NDX/DJI indices. Individual ticker samples are two weeks.

- **Licence:** Perpetual private-use licence. Research, models, charts and derived results can be published, but raw data cannot be redistributed. **Do not commit raw files to the public repo.**

- **Download:** Zipped CSV files via a customer download page; API access is offered with bundles. Data is timestamped in US Eastern Time. Zero-volume bars are omitted, so gaps can mean no trades rather than missing data.

- **Quality caveat:** The vendor describes exchange sourcing and completeness checks, but its licence disclaims warranties of accuracy and completeness. Its own dataset documentation also identifies omitted zero-volume bars and corporate-action adjustment issues.

- **Reason to distrust:** Its minute bars are trade-aggregated OHLC, not bid/ask quotes. It would extend the history materially, but would not by itself solve spread-aware execution modelling.

**Assessment:** Best alternative if the priority is direct index history plus long ETF history. The SPY page gives an exact 2000 start date; the direct SPX page gives a 2008 start date.

### **Bottom line**

- **Best first sample to inspect:** Kibot SPY/QQQ one-minute files, because the displayed combined full-history example is $125 and the archive reaches back before 2021.
- **Best second source for comparison:** FirstRate SPY and SPX. It offers direct index bars and a free one-year sample route.
- **For spread information:** Kibot's ETF bid/ask package is the clearest match I found, but it starts in 2009 and costs $680.
- **For the public repo:** Neither vendor permits raw data redistribution. Keep any purchased files private; publish only permitted derived results.
- **Free data:** There are useful samples and limited free windows, but I found no good free source for a long, clean, pre-2021 intraday history of these instruments.

I also opened the repository's [DATA_ROUND_1.md rubric](https://raw.githubusercontent.com/joemoney888/index/main/docs/DATA_ROUND_1.md). It confirms the five scoring categories and the prohibition on invented prices or sources. I did not attempt Yahoo, FRED or Stooq in this round; I therefore cannot say that those sites failed. Databento's catalogue appeared in search, but its direct page returned a 502 error when I tried to open it, so I have not included it as a verified recommendation.

---

## Set R

**Step 1 — what I can check (honest inventory)**

Live search works; direct page fetch works partially. Verified NOW (this session): kibot.com (free-samples, buy and FAQ pages, incl. licence text), firstratedata.com catalog pages, databento.com GLBX.MDP3 dataset page, alpaca.markets data page, stooq.com download pages — via search snippets plus two full-page fetches. Failed NOW: Databento /licensing (404), FirstRate /license (404); in earlier rounds NBER/ScienceDirect PDFs failed. From MEMORY (marked "unverified" below): SPY start dates, Stooq intraday depth, Alpaca cutoffs, Yahoo limits, non-Kibot licences.

**Step 2 — five sources, best first**

1. **Kibot** — kibot.com/buy.html. 1-min bars; stocks back to Jan 1998 (verified for IBM; SPY start unverified), ES continuous futures full history; prices SEEN TODAY (22 Nov 2026): **ES 1-min full history $110; SPY+QQQ 1-min full history $125; custom orders from $19, one payment**. 45 days download access (then back up your files). LICENCE VERIFIED from FAQ: personal research and AI-assisted analysis fine, aggregate results shareable, but "**the data itself may not be shared, published or given to anyone else**" → we CANNOT commit it to the public repo. CSV, US Eastern timestamps; futures unadjusted with published roll dates. Distrust trigger: samples are regular-session only and index symbols are index prints, not tradable CFD prices — validate on the 2021+ overlap with our OANDA bars first.

2. **Databento GLBX.MDP3** — databento.com/datasets/GLBX.MDP3. ES/NQ/YM futures, "since March 2017" (verified), MBP-1 schema gives best bid/ask — the only pre-2021 route to spread data (target 2). Pay-as-you-go historical rates; batch API; repo already has databento_pull.py, so plumbing exists. Cost per GB unverified; licence unverified (page 404; assume no redistribution). Distrust: usage-based bill can spike — price a query via their cost endpoint before buying; futures need roll handling.

3. **FirstRate Data** — firstratedata.com. 1-min ETF/index/futures bundles, "25 years data" (their tagline); stock set back to Jan 2000 incl. SPY (verified page text); bundle updates "approx $60-$100 per month" (seen today); single-purchase price unverified; free sample files. US Eastern time. Licence unverified (404). Distrust: small vendor, no independent audit — overlap-check against OANDA 2021+ before use.

4. **Alpaca free tier** — alpaca.markets/data. Free IEX-only 1-min bars for SPY/QQQ/DIA, "7+ years of historical data" (verified), ~200 requests/min, API key required (never commit keys). Reaches only ~2018-19; IEX-only bars have documented gaps (community reports verified). No spreads. Licence unverified; assume no redistribution.

5. **Stooq** — stooq.com/db/h. Free bulk daily/hourly/5-min CSVs, no registration. Best as the daily 20+ year fallback (target 3); daily depth believed decades (exact starts unverified); 5-min history believed short/recent (unverified). Licence unverified — do not commit bulk data to the repo. Distrust: own adjustment conventions; very long index back-series partly reconstructed.

Rejected: massive.com (serves Polygon.io's indices product; minute history only 1-2 years on $79/$199 tiers, seen today — too short); Yahoo (1-min 7 days, 5-min 60 days — memory, unverified); CBOE DataShop and CME DataMine (paid, prices unverified).

**Honest bottom line:** nothing good and free exists for pre-2021 intraday index history. The practical move is ~$110-125 one-time at Kibot (deepest, clean licence terms verified) or Databento usage fees (2017+, futures, with bid/ask). Whatever we buy: cross-validate on the 2021+ overlap with our OANDA bars before trusting it — free, costs no N.

---
