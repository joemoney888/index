"""Random search over chart-pattern rules on train, then validation for the promising. Exam never loaded. Env: SEED, SECONDS, MARKETS, DATA (dir of NAME.csv.gz), OUT (default search/PATTERNS)."""
import glob
import json
import os
import time

import numpy as np

from agent import patterns, search


FAMILY = os.environ.get("FAMILY", "classic")   # classic | geo | cycle


def sample(rng):
    h0 = int(rng.choice([13, 14, 15]))
    ex = {"ks": round(float(rng.uniform(1.0, 4.0)), 2), "kt": round(float(rng.uniform(0.5, 4.0)), 2), "H": int(rng.choice([12, 24, 48, 96, 192])), "h0": h0, "h1": int(min(24, h0 + rng.choice([4, 6, 8])))}
    if FAMILY == "geo":
        return dict(ex, pattern=str(rng.choice(["gartley", "bat", "butterfly", "crab", "cypher", "abcd", "drives", "elliott"])), K=int(rng.choice([6, 12, 24, 48])),
                    rt=float(rng.choice([0.05, 0.1, 0.15])), mode=str(rng.choice(["follow", "fade"])), ew=str(rng.choice(["w5", "corr"])))
    if FAMILY == "cycle":
        return dict(ex, pattern="cycle", W=int(rng.choice([288, 576, 864])), thr=float(rng.choice([0.05, 0.1, 0.2])), tol=float(rng.choice([0.3, 0.6])), mode=str(rng.choice(["follow", "fade"])))
    return {"pattern": str(rng.choice(["dt", "hs", "tri"])), "K": int(rng.choice([6, 12, 24, 48])), "tol": float(rng.choice([0.3, 0.5, 1.0, 1.5])),
            "depth": float(rng.choice([1.0, 2.0, 3.0])), "brk": int(rng.choice([0, 1])), "mode": str(rng.choice(["follow", "fade"])),
            "ks": round(float(rng.uniform(1.0, 4.0)), 2), "kt": round(float(rng.uniform(0.5, 4.0)), 2), "H": int(rng.choice([12, 24, 48, 96, 192])),
            "h0": h0, "h1": int(min(24, h0 + rng.choice([4, 6, 8])))}


def main():
    seed = int(os.environ.get("SEED_BASE", "1")) * 10 + int(os.environ.get("SEED_K", "0"))
    budget = float(os.environ.get("SECONDS", "600"))
    want = {m.strip().upper() for m in os.environ.get("MARKETS", "NAS100,SPX500,US30").split(",") if m.strip()}
    out = os.environ.get("OUT", "search/PATTERNS")
    data = os.environ.get("DATA", "data/bars5")
    mk = {}
    for pth in sorted(glob.glob(f"{data}/*.csv.gz")):
        name = os.path.basename(pth).split(".")[0]
        if name not in want:
            continue
        d = search.load_arrays(pth)
        val0, exam0 = search.split_points(int(d["t"][-1]))
        cut = int(np.searchsorted(d["t"], exam0))                  # the exam period never enters memory
        d = {k: v[:cut] for k, v in d.items()}
        mk[name] = (d, search.build_features(d), int(np.searchsorted(d["t"], val0)), cut)
    print("markets", list(mk), flush=True)
    piv, sigc = {}, {}

    def get_sig(name, p):
        d, f, _, _ = mk[name]
        if FAMILY == "cycle":
            key = (name, "cycle", p["W"], p["thr"], p["tol"], p["mode"])
            if key not in sigc:
                if (name, p["W"]) not in piv:
                    piv[(name, p["W"])] = patterns.cycle_raw(d["c"], p["W"])
                sigc[key] = patterns.cycle_signals(piv[(name, p["W"])], p["thr"], p["tol"], p["mode"])
            return sigc[key]
        pk = (name, p["K"])
        if pk not in piv:
            piv[pk] = patterns.pivots(d["h"], d["l"], p["K"])
        if FAMILY == "geo":
            key = (name, p["pattern"], p["K"], p["rt"], p["mode"], p["ew"] if p["pattern"] == "elliott" else "")
            if key not in sigc:
                sigc[key] = patterns.signals_geo(p["pattern"], piv[pk], p["K"], p["rt"], p["mode"], f["atr"], d["c"], p["ew"])
            return sigc[key]
        key = (name, p["pattern"], p["K"], p["tol"], p["depth"], p["brk"], p["mode"])
        if key not in sigc:
            sigc[key] = patterns.signals(p["pattern"], piv[pk], p["K"], p["tol"], p["depth"], p["brk"], p["mode"], f["atr"], d["c"])
        return sigc[key]

    def score(p, which):
        tr = []
        for name, (d, f, v0, cut) in mk.items():
            lo, hi = (300, v0) if which == "train" else (v0, cut)
            tr.append(patterns.simulate(get_sig(name, p), d, f, p, lo, hi))
        tr = [x for x in tr if len(x)]
        return search.day_t(np.vstack(tr) if tr else np.empty((0, 2)))

    rng = np.random.default_rng(seed)
    t0, n, ts, top, best500, by = time.time(), 0, [], [], -99.0, {}
    while time.time() - t0 < budget:
        p = sample(rng)
        tr = score(p, "train")
        n += 1
        ts.append(tr["t"])
        if tr["n"] >= 500:
            best500 = max(best500, tr["t"])
            by.setdefault(p["pattern"], []).append(tr["t"])
        if tr["n"] >= 500 and tr["t"] >= 2.5:
            top.append({"p": p, "train": tr, "val": score(p, "val")})
            top = sorted(top, key=lambda r: -r["train"]["t"])[:40]
        if n % 100 == 0:
            print(n, f"{time.time() - t0:.0f}s best train t (n>=500) {best500:.2f}", flush=True)
    os.makedirs(f"{out}/runs", exist_ok=True)
    a = np.array(ts)
    json.dump({"seed": seed, "n": n, "seconds": round(time.time() - t0), "t_mean": float(a.mean()), "t_max": float(a.max()), "t_max_n500": best500,
               "by_pattern_mean_t": {k: float(np.mean(v)) for k, v in by.items()}, "by_pattern_count": {k: len(v) for k, v in by.items()}, "top": top},
              open(f"{out}/runs/{seed}.json", "w"))
    print("done", n, "variants; best train t (n>=500):", round(best500, 2), "| by pattern mean t:", {k: round(float(np.mean(v)), 2) for k, v in by.items()})


if __name__ == "__main__":
    main()
