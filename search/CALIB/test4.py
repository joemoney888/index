"""Test 4 (pre-registered 21 Nov 2026, agreed by Claude and GLM 5.3): is the random-search pipeline calibrated? Does it produce false finalists on data with NO intraday structure?
Null: per UTC day, keep the first bar fixed and randomly permute the other bars' (gap-from-previous-close, body, upper wick, lower wick) quadruples, re-chained from the day's real open. Preserves each day's open->close move, bar-return multiset, wick shapes, ATR/volatility levels, overnight gaps, the 20-day trend filter, and spread-by-clock-slot. Destroys within-day ordering (what an intraday entry rule exploits). Does NOT test daily-scale families.
Engine: the FIXED engine (search.GAP_AWARE = True): stop exits whose bar opens beyond the stop fill at that open. Same sampler, same train/validation split, exam cut off, same gates.
Per run: n = 31,740 trials (the original NAS100 family's own n), luck bar 5.05 (= sqrt(2 ln 31740) + 0.5). Candidate: train n>=500, mean>=0.03, t>=bar. Finalist: candidate AND validation n>=150, mean>=0.03, t>=2.0.
Plan: 1 reference run on the REAL data (gap-aware engine) + 10 shuffles first. Reading: 0 finalists in 10 -> run 10 more; 1 -> extend to 20 then reassess; >=2 in 10 -> pipeline miscalibrated: asterisk every family null and require a recalibrated bar for any future candidate. Also compare the max train t across shuffles with the reference. 0/20 bounds the false-finalist rate at about 14% (rule of three): this detects gross miscalibration only. N +0.
Usage: python search/CALIB/test4.py <id> [<id> ...]   id 0 = real-data reference, 1.. = shuffle seeds."""
import sys, os, json, time, numpy as np
sys.path.insert(0, "/home/claude/index")
from agent import search
search.GAP_AWARE = True
NTRIALS = 31740
BAR = search.luck_bar(NTRIALS)
DATA = "/home/claude/gbpusd-paper-agent/data/bars5/NAS100.csv.gz"

def shuffled(d, seed):
    rng = np.random.default_rng(seed); n = len(d["t"]); day = d["t"] // 86400
    o, h, l, c = d["o"], d["h"], d["l"], d["c"]
    prev_c = np.concatenate([[c[0]], c[:-1]]); gap = o - prev_c; body = c - o; up = h - np.maximum(o, c); dn = np.minimum(o, c) - l
    no, nh, nl, nc = o.copy(), h.copy(), l.copy(), c.copy()
    bounds = np.flatnonzero(np.diff(day)) + 1; starts = np.concatenate([[0], bounds]); ends = np.concatenate([bounds, [n]])
    for a, b in zip(starts, ends):
        if b - a < 3: continue
        perm = a + 1 + rng.permutation(b - a - 1)           # bars a+1..b-1 shuffled; bar a (the day's first) fixed
        order = np.concatenate([[a], perm])
        px = o[a]
        for k, j in enumerate(order):
            if k == 0:
                no[a], nc[a] = o[a], c[a]; nh[a], nl[a] = h[a], l[a]; px = c[a]; continue
            op = px + gap[j]; cl = op + body[j]; i = a + k
            no[i], nc[i] = op, cl; nh[i] = max(op, cl) + up[j]; nl[i] = min(op, cl) - dn[j]; px = cl
    return {**d, "o": no, "h": nh, "l": nl, "c": nc}

def run(rid):
    d = search.load_arrays(DATA); val0, exam0 = search.split_points(int(d["t"][-1])); cut = int(np.searchsorted(d["t"], exam0))
    d = {k: v[:cut] for k, v in d.items()}
    if rid > 0: d = shuffled(d, 1000 + rid)
    f = search.build_features(d); v0 = int(np.searchsorted(d["t"], val0))
    rng = np.random.default_rng(777000 + rid); t0 = time.time(); ts = []; best500 = -99.0; cands = []; fins = []
    for n in range(NTRIALS):
        p = search.sample(rng); tr = search.trades(p, d, f, 300, v0); train = search.day_t(tr); ts.append(train["t"])
        if train["n"] >= 500: best500 = max(best500, train["t"])
        if train["n"] >= 500 and train["t"] >= 2.5:
            val = search.day_t(search.trades(p, d, f, v0, cut))
            if search.is_candidate(train, NTRIALS):
                cands.append({"p": p, "train": train, "val": val})
                if search.is_finalist(val): fins.append({"p": p, "train": train, "val": val})
        if (n + 1) % 2000 == 0: print(rid, n + 1, f"{time.time()-t0:.0f}s best500 {best500:.2f} cands {len(cands)} fins {len(fins)}", flush=True)
    a = np.array(ts); out = {"id": rid, "real_data": rid == 0, "n": NTRIALS, "bar": BAR, "seconds": round(time.time() - t0), "t_mean": float(a.mean()), "t_sd": float(a.std()), "t_max": float(a.max()), "t_max_n500": best500, "candidates": len(cands), "finalists": len(fins), "top": (cands + fins)[:5]}
    json.dump(out, open(f"/home/claude/index/search/CALIB/test4_{rid}.json", "w")); print("DONE", {k: v for k, v in out.items() if k != "top"}, flush=True)

if __name__ == "__main__":
    for r in sys.argv[1:]: run(int(r))
