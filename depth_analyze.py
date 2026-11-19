"""Does order book imbalance predict the next price move, after costs? Reads depth/data/*.csv.gz (Kraken BTC/USD, ETH/USD, 1-second samples). Prints and writes depth/REPORT.md.
Signal: imbalance over the top N levels (N = 1, 5, 25). Forward return of the mid over 10 s, 30 s, 60 s, 300 s, in basis points (1 bp = 0.01%). Cost: crossing the spread (entry at the far side, exit at the far side)."""
import glob
import gzip
import csv
import numpy as np


def load():
    out = {}
    for p in sorted(glob.glob("depth/data/*.csv.gz")):
        with gzip.open(p, "rt") as f:
            for r in csv.DictReader(f):
                out.setdefault(r["symbol"], []).append((int(r["t"]), float(r["mid"]), float(r["spread"]), float(r["imb1"]), float(r["imb5"]), float(r["imb25"])))
    return {k: np.array(sorted(v)) for k, v in out.items()}


def main():
    D = load()
    L = ["# Order book imbalance: does it predict the next move? (crypto concept test)", ""]
    for sym, a in D.items():
        t, mid, spr = a[:, 0], a[:, 1], a[:, 2]
        # require contiguous seconds
        L.append(f"## {sym}: {len(a):,} one-second samples, {(t[-1]-t[0])/3600:.1f} hours span, typical spread {np.median(spr/mid)*1e4:.2f} bp")
        for hname, h in (("10s", 10), ("30s", 30), ("60s", 60), ("300s", 300)):
            idx = np.arange(len(a) - h)
            ok = (t[idx + h] - t[idx]) == h
            idx = idx[ok]
            if len(idx) < 500:
                continue
            fr = (mid[idx + h] / mid[idx] - 1) * 1e4
            for col, nm in ((3, "top1"), (4, "top5"), (5, "top25")):
                x = a[idx, col]
                r = np.corrcoef(x, fr)[0, 1]
                # non-overlapping t-stat: every h-th sample
                sel = idx[::max(h, 1)] - idx[0]
                xs, ys = x[::max(h, 1)], fr[::max(h, 1)]
                n = len(xs)
                tstat = np.corrcoef(xs, ys)[0, 1] * np.sqrt(max(n - 2, 1)) if n > 10 else 0.0
                # simple rule: strong imbalance (|x|>0.6) -> trade with it, pay the whole spread
                m = np.abs(xs) > 0.6
                if m.sum() >= 30:
                    side = np.sign(xs[m])
                    cost = spr[idx][::max(h, 1)][m] / mid[idx][::max(h, 1)][m] * 1e4   # round trip crossing the spread once each way approx = spread
                    net = side * ys[m] - cost
                    L.append(f"- {hname} ahead, {nm}: corr {r:+.3f} (non-overlapping t {tstat:+.1f}); trade only when |imbalance|>0.6: n={m.sum()}, gross {np.mean(side*ys[m]):+.2f} bp, cost {np.mean(cost):.2f} bp, net {np.mean(net):+.2f} bp")
                else:
                    L.append(f"- {hname} ahead, {nm}: corr {r:+.3f} (non-overlapping t {tstat:+.1f}); too few strong-imbalance cases")
        L.append("")
    L.append("Reading it: a real signal needs a clearly non-zero correlation AND net basis points above zero after the spread, stable across days. Crypto is only a test bed for the idea; indices differ.")
    open("depth/REPORT.md", "w").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
