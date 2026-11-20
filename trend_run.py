"""Random search over the slow trend family on train, then validation for the promising. Exam never loaded. Env: SEED, TRIALS, MARKETS (default NAS100,SPX500,US30,GER40,UK100), DATA (dir with NAME.csv.gz), OUT."""
import json
import math
import os

import numpy as np
import pandas as pd

from agent import search, trend


def main():
    seed, trials = int(os.environ.get("SEED", "1")), int(os.environ.get("TRIALS", "3000"))
    names = os.environ.get("MARKETS", "NAS100,SPX500,US30,GER40,UK100").split(",")
    data = os.environ.get("DATA", "data/bars5")
    mk = {n: trend.daily(f"{data}/{n}.csv.gz") for n in names}
    t_last = max(int(x.index[-1].timestamp()) for x in mk.values())
    val0, exam0 = search.split_points(t_last)
    tz = lambda t: pd.Timestamp(t, unit="s", tz="UTC")  # noqa: E731
    t_first = min(x.index[0] for x in mk.values())
    rng = np.random.default_rng(seed)
    res, ts = [], []
    for _ in range(trials):
        p = trend.sample(rng)
        w, det = trend.alpha_series(p, mk, t_first, tz(val0))
        tt = trend.tstat(w)
        ts.append(tt)
        if tt >= 1.5:
            wv, dv = trend.alpha_series(p, mk, tz(val0), tz(exam0))
            res.append({"p": p, "train_t": round(tt, 2), "train_mean_w": float(w.mean()), "val_t": round(trend.tstat(wv), 2), "val_mean_w": float(wv.mean()) if len(wv) else 0.0,
                        "train": det, "val": dv})
    res.sort(key=lambda r: -r["train_t"])
    ts = np.array(ts)
    out = os.environ.get("OUT", "search/TREND")
    os.makedirs(out, exist_ok=True)
    json.dump({"seed": seed, "n": trials, "luck_bar": search.luck_bar(trials), "t_mean": float(ts.mean()), "t_max": float(ts.max()), "top": res[:15]}, open(f"{out}/run_{seed}.json", "w"), indent=1)
    print("trials", trials, "luck bar", round(search.luck_bar(trials), 2), "best train t", round(ts.max(), 2), "avg train t", round(ts.mean(), 2))
    for r in res[:8]:
        print(r["train_t"], r["val_t"], r["p"])


if __name__ == "__main__":
    main()
