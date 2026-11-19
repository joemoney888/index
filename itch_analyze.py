"""Does the REAL Nasdaq order book imbalance predict the next price move, after the spread? Reads depth/itch/*.csv.gz (one-second samples of QQQ, SPY, AAPL, MSFT, NVDA, AMZN, TSLA for 30 Jan 2020). Writes depth/ITCH_REPORT.md.
Forward return of the mid over 10 s / 30 s / 60 s / 300 s in basis points; non-overlapping samples for the t-stat; a simple rule trades only strong imbalance and pays the quoted spread. ONE day: it shows whether there is a signal worth chasing, it cannot prove an edge."""
import csv
import glob
import gzip
import os

import numpy as np


def main():
    L = ["# Real Nasdaq order book (ITCH, 30 Jan 2020): does imbalance predict the next move?", ""]
    pooled = {}
    for p in sorted(glob.glob("depth/itch/*.csv.gz")):
        sym = os.path.basename(p).split(".")[0]
        with gzip.open(p, "rt") as f:
            a = np.array([[float(x) for x in r] for r in list(csv.reader(f))[1:]])
        if len(a) < 2000:
            continue
        t, mid, spr = a[:, 0], a[:, 1], a[:, 2]
        L.append(f"## {sym}: {len(a):,} seconds, typical spread {np.median(spr/mid)*1e4:.2f} bp")
        for h in (10, 30, 60, 300):
            idx = np.arange(len(a) - h)
            idx = idx[(t[idx + h] - t[idx]) == h]
            fr = (mid[idx + h] / mid[idx] - 1) * 1e4
            for col, nm in ((5, "top1"), (6, "top5"), (7, "top10")):
                x = a[idx, col]
                step = h
                xs, ys, cs = x[::step], fr[::step], (spr[idx] / mid[idx] * 1e4)[::step]
                r = np.corrcoef(xs, ys)[0, 1] if np.std(xs) > 0 and np.std(ys) > 0 else 0.0
                tstat = r * np.sqrt(max(len(xs) - 2, 1))
                m = np.abs(xs) > 0.6
                if m.sum() >= 20:
                    gross = np.sign(xs[m]) * ys[m]
                    net = gross - cs[m]
                    L.append(f"- {h}s, {nm}: corr {r:+.3f} (t {tstat:+.1f}); |imbalance|>0.6 n={m.sum()}, gross {gross.mean():+.2f} bp, spread {cs[m].mean():.2f} bp, net {net.mean():+.2f} bp")
                    pooled.setdefault((h, nm), []).append((sym, r, tstat, gross.mean(), net.mean()))
                else:
                    L.append(f"- {h}s, {nm}: corr {r:+.3f} (t {tstat:+.1f}); too few strong-imbalance cases")
        L.append("")
    L.append("## Summary across stocks (average of per-stock results)")
    for (h, nm), v in sorted(pooled.items()):
        L.append(f"- {h}s {nm}: mean corr {np.mean([x[1] for x in v]):+.3f}, mean gross {np.mean([x[3] for x in v]):+.2f} bp, mean net after spread {np.mean([x[4] for x in v]):+.2f} bp ({len(v)} stocks)")
    L.append("")
    L.append("Reading it: a usable signal needs correlation clearly above zero AND net basis points above zero after the spread, consistently across stocks. One day on Nasdaq's own book (not the consolidated market).")
    open("depth/ITCH_REPORT.md", "w").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
