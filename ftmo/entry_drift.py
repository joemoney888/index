"""B.1 + C.2 (pre-registered before running): does the BFG ENTRY SIGNAL predict returns with NO exits at all?
Signals: every bar passing the fitted rule's entry conditions (score>=theta, hours, trend agreement, gate, valid), whole 5-min history, no one-position limit.
Forward return: from next bar open +/- half spread (entry) to the open h bars later -/+ half spread (exit), sign-adjusted to the signal side, in R units of the rule's stop (ks*ATR).
Horizons h (bars): 6,12,24,48,96,192 (30m,1h,2h,4h,8h,16h)  -> 6 looks, Bonferroni t>=2.64.
De-duplication: per horizon, greedy non-overlapping signals (next signal must start after the previous one's exit).
Permutation (C.2): per horizon keep the same days and the same side per day, move each signal to a random valid bar inside the same day's hours window; 2000 draws; p = share of draws with mean >= actual.
Kill rule: no horizon with day-clustered t>=2.64 AND permutation p<0.05 -> entry line closed. Counted in N: +0 (analysis of an already-selected rule, no new candidates)."""
import sys, json, numpy as np
sys.path.insert(0, "/home/claude/index")
from agent import search
P = json.load(open("/home/claude/index/search/NAS100/finalists.json"))[0]["p"]
d = search.load_arrays("/home/claude/gbpusd-paper-agent/data/bars5/NAS100.csv.gz"); f = search.build_features(d); n = len(d["t"])
w = np.array(P["w"]); score = f["F"] @ w / np.abs(w).sum() * 2
ok = (np.abs(score) >= P["theta"]) & (f["hour"] >= P["h0"]) & (f["hour"] < P["h1"]) & f["valid"]
if P["trend"]: ok &= np.sign(score) == f["trend"]
ok &= f["gates"][P.get("gate", "none")]
ok_hours = (f["hour"] >= P["h0"]) & (f["hour"] < P["h1"]) & f["valid"]   # random-placement pool (no score/gate: a within-day relocation)
side_all = np.sign(score); risk_all = P["ks"] * f["atr"]; day = (d["t"] // 86400).astype(np.int64)
v0, e0 = search.split_points(int(d["t"][-1])); iv, ie = int(np.searchsorted(d["t"], v0)), int(np.searchsorted(d["t"], e0))
def fwd(i, h):
    s = side_all[i]; e = d["o"][i + 1] + s * d["s"][i] / 2; x = d["o"][i + 1 + h] - s * d["s"][i + 1 + h] / 2
    return s * (x - e) / risk_all[i]
def dedup(idx, h):
    out, free = [], -1
    for i in idx:
        if i >= free and i + h + 2 < n and risk_all[i] > 0: out.append(i); free = i + h + 1
    return np.array(out, dtype=int)
sig = np.flatnonzero(ok); rng = np.random.default_rng(7)
print(f"signals {len(sig)}  bars {n}  days {len(np.unique(day))}  train<{iv} val<{ie} exam>={ie}")
pool_by_day = {}
for i in np.flatnonzero(ok_hours): pool_by_day.setdefault(day[i], []).append(i)
for h in (6, 12, 24, 48, 96, 192):
    I = dedup(sig, h); R = np.array([fwd(i, h) for i in I]); r = search.day_t(np.column_stack([d["t"][I], R]))
    segs = {nm: R[(I >= a) & (I < b)] for nm, (a, b) in (("train", (0, iv)), ("val", (iv, ie)), ("exam", (ie, n)))}
    sp = "  ".join(f"{nm} {x.mean():+.3f}R(n{len(x)})" for nm, x in segs.items())
    # permutation (vectorised): same days & sides, random valid bar in that day
    nn = n - h - 2; ii = np.arange(nn); ee_l = d["o"][ii + 1] + d["s"][ii] / 2; xx_l = d["o"][ii + 1 + h] - d["s"][ii + 1 + h] / 2
    ee_s = d["o"][ii + 1] - d["s"][ii] / 2; xx_s = d["o"][ii + 1 + h] + d["s"][ii + 1 + h] / 2
    RL = np.full(n, np.nan); RS = np.full(n, np.nan); RL[:nn] = (xx_l - ee_l) / risk_all[:nn]; RS[:nn] = -(xx_s - ee_s) / risk_all[:nn]
    days_ = day[I]; sides = side_all[I]
    starts, lens, flat = [], [], []
    for x in days_:
        c = np.array(pool_by_day[x]); c = c[(c + h + 2 < n) & (risk_all[c] > 0)]; starts.append(len(flat)); lens.append(len(c)); flat.extend(c.tolist())
    starts = np.array(starts); lens = np.array(lens); flat = np.array(flat, dtype=int); k = lens > 0; B = 2000; cnt = 0
    for _ in range(B):
        pick = flat[starts[k] + (rng.random(k.sum()) * lens[k]).astype(int)]
        m = np.where(sides[k] > 0, RL[pick], RS[pick]); cnt += np.nanmean(m) >= R.mean()
    print(f"h={h:3d} ({h*5:4d}min) n={len(I):5d} mean {r['mean']:+.4f}R  day-t {r['t']:5.2f} | {sp} | perm p {(cnt+1)/(B+1):.3f}", flush=True)
