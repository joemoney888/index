"""Random search for the index spread trade on train, then validation for the promising. Exam never loaded. Env: SEED, SECONDS, DATA, OUT (default search/SPREAD)."""
import itertools
import json
import os
import time

import numpy as np

from agent import search, spread


def main():
    seed = int(os.environ.get("SEED_BASE", "1")) * 10 + int(os.environ.get("SEED_K", "0"))
    budget = float(os.environ.get("SECONDS", "600"))
    data, out = os.environ.get("DATA", "data/bars5"), os.environ.get("OUT", "search/SPREAD")
    raw = {n: search.load_arrays(f"{data}/{n}.csv.gz") for n in ("NAS100", "SPX500", "US30")}
    pairs, mk = list(itertools.combinations(raw, 2)), {}
    for a, b in pairs:
        m = spread.align(raw[a], raw[b])
        val0, exam0 = search.split_points(int(m["t"][-1]))
        cut = int(np.searchsorted(m["t"], exam0))
        mk[(a, b)] = ({k: v[:cut] for k, v in m.items()}, int(np.searchsorted(m["t"], val0)), cut)
    prc = {}
    rng = np.random.default_rng(seed)

    def score(p, which):
        tr = []
        for pr, (m, v0, cut) in mk.items():
            key = (pr, p["L"])
            if key not in prc:
                prc[key] = spread.prep(m, p["L"])
            lo, hi = (3000, v0) if which == "train" else (v0, cut)
            tr.append(spread.simulate(m, prc[key], p, lo, hi))
        tr = [x for x in tr if len(x)]
        return search.day_t(np.vstack(tr) if tr else np.empty((0, 2)))

    t0, n, ts, top, best = time.time(), 0, [], [], -99.0
    while time.time() - t0 < budget:
        h0 = int(rng.choice([0, 13, 14]))
        p = {"L": int(rng.choice([288, 864, 1440, 2880])), "z0": float(rng.choice([1.5, 2.0, 2.5, 3.0])), "ez": float(rng.choice([0.0, 0.5])),
             "ks": float(rng.choice([2, 3, 4])), "H": int(rng.choice([48, 96, 192, 576])), "h0": h0, "h1": 24 if h0 == 0 else int(min(24, h0 + rng.choice([4, 6, 8])))}
        tr = score(p, "train")
        n += 1
        ts.append(tr["t"])
        if tr["n"] >= 300:
            best = max(best, tr["t"])
        if tr["n"] >= 300 and tr["t"] >= 2.5:
            top.append({"p": p, "train": tr, "val": score(p, "val")})
            top = sorted(top, key=lambda r: -r["train"]["t"])[:40]
        if n % 50 == 0:
            print(n, f"{time.time() - t0:.0f}s best train t (n>=300) {best:.2f}", flush=True)
    os.makedirs(f"{out}/runs", exist_ok=True)
    a = np.array(ts)
    json.dump({"seed": seed, "n": n, "seconds": round(time.time() - t0), "t_mean": float(a.mean()), "t_max_n300": best, "top": top}, open(f"{out}/runs/{seed}.json", "w"))
    print("done", n, "variants; best train t (n>=300):", round(best, 2), "avg t", round(float(a.mean()), 2))
    for r in top[:5]:
        print(round(r["train"]["t"], 2), r["train"]["n"], "val", round(r["val"]["t"], 2), r["val"]["n"], r["p"])


if __name__ == "__main__":
    main()
