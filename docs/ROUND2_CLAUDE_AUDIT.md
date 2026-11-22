# Round 2 cross-audit - Claude Sonnet 5.5 (prompts sent about 00:55 UTC 22 Nov 2026; committed after the prompt, same clock as the others)
Scope: GLM Round F, G, ideas round and cross-scoring; ChatGPT 6 first review, ideas reply and cross-scoring; and my own longterm test. Only checked items are listed; "unverified" is marked.

## GLM 5.3 - verified errors (none changes a conclusion)
1. Round G power line: "n ~ 1,200 days (5y x ~252 minus ~45 early closes minus data-gap days)". The frozen calendar lists 11 early closes in total and 54 full holidays; the sample 2021-05-20 to 2026-11-17 has 1,381 weekdays that are not full holidays and 1,371 after the early closes. So n is about 1,370 (the data span 5.5 years, not 5), and the detectable mean at t 2.8 is 1.9 bp, not 2.0 bp (2.8 x 25 / sqrt(1371) = 1.89). The error is conservative.
2. Cross-scoring errata: calls the score "Joe's audit"; the scoreboard was written by Claude Sonnet 5.5.
3. Round F first stated Lucca and Moench as "JF 2011"; the ideas round "corrected" it to "AER 2015"; right answer Journal of Finance 70(1) 2015. GLM has corrected this itself, so not counted again.
4. Unverified: "Kurov et al. 2020" for the weakening of the pre-FOMC drift. Related work exists (Kurov, Sancetta, Strasser and Wolfe, JFQA 54(1) 2019, 449-479, "Price drift before U.S. macroeconomic news"; a paper titled "The Disappearing Pre-FOMC Announcement Drift" is listed on SSRN), so the claim is plausible, but the exact citation and year were not confirmed.
Re-computed and CORRECT: Test 4 z = 3.33; sample SD 0.434 from population SD 0.423; exact 95% bound 13.9%; thirds probabilities (0.945, 0.99, 0.96); family-wise 3 x 0.0026 = 0.0077 and exact z 2.39 for 0.05/3 two-sided; Idea 1 detectable 0.21R and 0.32R; Idea 6 split 3.2 and 4.8 bp; Family B 0.52 percent; overnight 8.5 bp gross and 21 percent a year; session 6.7 bp and 17 percent a year; P1 and P2 power (3 percent, 22 percent, 12 percent). Round G's reading of the abstract (previous close to 10:00) matches the published abstract (Claude fetched it).

## ChatGPT 6 - verified errors (none changes a conclusion)
1. First review cited FAMILY_A_SPEC "line 9" (old thirds) and "line 28" (changelog); the actual lines were 11 and 34. The substance (stale 2021-11 thirds in the main text, contradicting the v1.1 changelog) was right and was fixed.
2. Ideas cross-score of Y2 used SD 80 bp (session scale) for a 24-hour hold, so its 35.4 bp detectable effect inherits Claude's error; a 24-hour hold needs about 55-65 bp (GLM caught this; GPT6 did not).
3. Ideas cross-score arithmetic or scale: "10/11" (rubric top is 10). Scored X1 and X2 9/10 although both have power of 3-22 percent by their own numbers.
4. Unverified: Ai and Bansal "15.44 bp (NFP) and 7.53 bp (PPI), 1997-2014". The NBER abstract does not contain them and Claude could not find them either.
5. "|t| >= 2.8" quibble is a wording nit, not an error: Family A's decision rule also requires a positive net mean in the claimed direction, so GPT6 is right that it is effectively one-sided for A6a and A6b; for A5 the test is two-sided by design (claimed direction traded).
Re-computed and CORRECT: 13.9% upper bound; 941,367 + 175 = 941,542; CAGR 6.8 / 9.7 and the CI in the longterm result; all MDE arithmetic in the ideas reply and the cross-scores except item 2.

## Claude Sonnet 5.5 (own longterm test, longterm/spec.md)
1. The yearly data were transcribed from Damodaran's page through the web-reading tool (a summariser), not from a downloaded file. Spot-checked against values Claude knows (1931 -43.84, 1954 +52.56, 1974 -25.90, 2008 -36.55, 1928 +43.81) and all match; the rest are NOT independently verified, and 2025 was not checkable.
2. One rule, one market, 97 yearly observations; the valuation tilt and the daily 200-day rule were not tested (stated in the file).
3. The "worse in both halves" criterion is correct as run, but the sample has only two independent halves; "reliably worse" overstates; "worse in this sample, 95% bootstrap range wholly below zero" is the right wording.

## Addendum (00:5x UTC, after reading GPT6's audit; sealed text above unchanged)
Claude missed one point GPT6 found: GLM's "the 2-of-3 gate costs about 1-3% power" is loose; with GLM's own numbers the loss is about 1% at 2.0 bp and 3.7% at 1.5 bp (so "1-4%"). Claude also found that the repo copy of docs/REPLIES_FROM_GLM.md was missing GLM's Round G (Claude's record error: it had appended only later sections); Round G has now been inserted in order.
