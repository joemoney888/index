"""Rough FTMO 2-Step simulation on filtered NAS100 BFG trades. Realised-trade equity only (open-trade drawdown NOT modelled -> optimistic)."""
import sys, numpy as np
sys.path.insert(0, "/home/claude/index/ftmo"); sys.path.insert(0, "/home/claude/index")
import json, ftmo_filters as F
from agent import search
from zoneinfo import ZoneInfo
import datetime as dt
p = json.load(open("/home/claude/index/search/NAS100/finalists.json"))[0]["p"]
d = search.load_arrays("/home/claude/gbpusd-paper-agent/data/bars5/NAS100.csv.gz"); f = search.build_features(d)
val0, ex0 = search.split_points(int(d["t"][-1])); ie = int(np.searchsorted(d["t"], ex0)); iv = int(np.searchsorted(d["t"], val0))
mask = F.block_mask(d["t"], ["nfp", "fomc"], 120, False, True)
mask_cpi = F.block_mask(d["t"], ["nfp", "fomc", "cpi"], 120, False, True)
CET = ZoneInfo("Europe/Prague")
def day_key(ts): return dt.datetime.fromtimestamp(int(ts), CET).date().toordinal()
def phase(tr, i0, risk, target, maxdays=400):
    """tr: array(entry_time,R) sorted. Start at trade index i0. Returns (status, next_index, days). status 'pass'/'fail'/'open'."""
    eq = 0.0; start_day = day_key(tr[i0, 0]); cur = start_day; day_open = 0.0; days = set()
    for j in range(i0, len(tr)):
        dk = day_key(tr[j, 0])
        if dk != cur: cur = dk; day_open = eq
        if dk - start_day > maxdays: return "open", j, dk - start_day
        eq += tr[j, 1] * risk; days.add(dk)
        if eq - day_open <= -0.05 or eq <= -0.10: return "fail", j + 1, dk - start_day
        if eq >= target and len(days) >= 4: return "pass", j + 1, dk - start_day
    return "open", len(tr), 0
def sim(tr, risk, step=5):
    r = {"p1": 0, "both": 0, "n": 0, "d1": [], "d2": []}
    for i0 in range(0, len(tr) - 30, step):
        s1, j, d1 = phase(tr, i0, risk, 0.10); r["n"] += 1
        if s1 == "pass":
            r["p1"] += 1; r["d1"].append(d1)
            s2, _, d2 = phase(tr, j, risk, 0.05)
            if s2 == "pass": r["both"] += 1; r["d2"].append(d2)
    return r
for nm, m in [("filters D (NFP/FOMC +-2h, closes)", mask), ("filters F (+CPI proxy)", mask_cpi)]:
    for seg, (lo, hi) in {"val+exam (2 yrs)": (iv, len(d["t"])), "exam (last 365d)": (ie, len(d["t"]))}.items():
        tr = F.run(nm, d, f, p, m, lo, hi)
        print(f"\n{nm} | {seg} | {len(tr)} trades, mean {tr[:,1].mean():+.3f}R, sd {tr[:,1].std():.2f}R")
        for risk in (0.005, 0.0075, 0.01):
            r = sim(tr, risk)
            print(f"  risk {risk*100:.2f}%/trade: phase1 pass {r['p1']/r['n']*100:3.0f}%, both phases {r['both']/r['n']*100:3.0f}% (starts {r['n']}), median days p1 {np.median(r['d1']) if r['d1'] else 0:.0f}, p2 {np.median(r['d2']) if r['d2'] else 0:.0f}")
