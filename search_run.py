"""One search job: sample random strategies, score them on TRAIN (and VALIDATION for promising ones), record counts. The exam period is cut off before anything is computed.
Env: SEED, SECONDS (time budget, default 3000), MAX_TRIALS. Output search/runs/SEED.json. Needs data/bars5/*.csv.gz (fetchm5 workflow)."""
import glob
import json
import os
import time

import numpy as np

from agent import search


def main():
    seed = int(os.environ.get("SEED_BASE", "1")) * 10 + int(os.environ.get("SEED_K", "0"))
    budget = float(os.environ.get("SECONDS", "3000"))
    max_trials = int(os.environ.get("MAX_TRIALS", "1000000"))
    want = {m.strip().upper() for m in os.environ.get("MARKETS", "").split(",") if m.strip()}
    out = os.environ.get("SEARCH_DIR", "search")
    mk = {}
    scalp = os.environ.get("SCALP") == "1"
    day = 1440 if scalp else 288
    for p in sorted(glob.glob("data/bars1/*.csv.gz" if scalp else "data/bars5/*.csv.gz")):
        if want and os.path.basename(p).split(".")[0] not in want:
            continue
        d = search.load_arrays(p)
        t_last = int(d["t"][-1])
        val0, exam0 = search.split_points(t_last)
        cut = int(np.searchsorted(d["t"], exam0))          # the exam period never enters memory
        d = {k: v[:cut] for k, v in d.items()}
        f = search.build_features(d, day)
        mk[os.path.basename(p).split(".")[0]] = (d, f, int(np.searchsorted(d["t"], val0)), cut)
    print("markets", list(mk), flush=True)
    rng = np.random.default_rng(seed)
    t0, n, ts, top, best500 = time.time(), 0, [], [], -99.0
    while time.time() - t0 < budget and n < max_trials:
        p = search.sample(rng, scalp)
        tr = [search.trades(p, d, f, 300, v0) for d, f, v0, _ in mk.values()]
        train = search.day_t(np.vstack([x for x in tr if len(x)]) if any(len(x) for x in tr) else np.empty((0, 2)))
        n += 1
        ts.append(train["t"])
        if train["n"] >= 500:
            best500 = max(best500, train["t"])
        if train["n"] >= 500 and train["t"] >= 2.5:
            vr = [search.trades(p, d, f, v0, cut) for d, f, v0, cut in mk.values()]
            val = search.day_t(np.vstack([x for x in vr if len(x)]) if any(len(x) for x in vr) else np.empty((0, 2)))
            top.append({"p": p, "train": train, "val": val})
            top = sorted(top, key=lambda r: -r["train"]["t"])[:40]
        if n % 500 == 0:
            print(n, f"{time.time() - t0:.0f}s best train t {max(ts):.2f}", flush=True)
    os.makedirs(f"{out}/runs", exist_ok=True)
    a = np.array(ts)
    json.dump({"seed": seed, "n": n, "seconds": round(time.time() - t0), "t_mean": float(a.mean()), "t_sd": float(a.std()), "t_max": float(a.max()), "t_max_n500": best500, "top": top},
              open(f"{out}/runs/{seed}.json", "w"))
    print("done", n, "trials")


if __name__ == "__main__":
    main()
