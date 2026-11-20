"""FTMO 2-Step simulation v2: floating P&L modelled (equity = closed balance + open trade at its worst price each 5-min bar), daily loss 5% vs equity at the 00:00 CE(S)T reset, static 10% max loss, 4 trading days,
phase 2 conditional on phase 1 passing, NON-overlapping monthly start dates, Wilson 95% intervals. Compared for idealised R and gap-aware R. Sizing = fixed fraction of the initial $ per R."""
import sys, math, datetime as dt, numpy as np
from zoneinfo import ZoneInfo
sys.path.insert(0, "/home/claude/index/ftmo"); sys.path.insert(0, "/home/claude/index")
import ftmo_filters as F, cost_stack as C
from agent import search
CET = ZoneInfo("Europe/Prague"); _c = {}
def dkey(ts):
    h = int(ts // 3600)
    if h not in _c: _c[h] = dt.datetime.fromtimestamp(h * 3600, CET).date().toordinal()
    return _c[h]
d = search.load_arrays("/home/claude/gbpusd-paper-agent/data/bars5/NAS100.csv.gz"); f = search.build_features(d); t = d["t"]
v0, e0 = search.split_points(int(t[-1])); iv = int(np.searchsorted(t, v0))
mask = F.block_mask(t, ["nfp", "fomc"], 120, False, True)
D = C.detail(C.P, d, f, mask, iv, len(t)); Rid = D[:, 7]; Rgap = C.net_R(D, d, gap=True)
paths = []
for r in D:
    i, n, side, e, risk = int(r[1]), int(r[5]), r[2], r[3], r[4]; ks = np.arange(i + 1, i + 2 + n); half = d["s"][ks] / 2
    worst = (d["l"][ks] - half - e) / risk if side > 0 else (e - (d["h"][ks] + half)) / risk
    close = side * (d["c"][ks] - e) / risk
    paths.append((t[ks], worst, close))
def phase(start, Rs, risk, target):
    bal, days, cur, dstart, lastfl = 0.0, set(), None, 0.0, 0.0
    for j in range(start, len(D)):
        pt, worst, close = paths[j]; days.add(dkey(pt[0]))
        for k in range(len(pt)):
            dk = dkey(pt[k])
            if dk != cur: cur = dk; dstart = bal + risk * lastfl
            eq = bal + risk * min(worst[k], Rs[j] if k == len(pt) - 1 else worst[k])
            if eq - dstart <= -0.05 or eq <= -0.10: return "fail", j + 1
            lastfl = close[k]
        bal += risk * Rs[j]; lastfl = 0.0
        if bal >= target and len(days) >= 4: return "pass", j + 1
    return "open", len(D)
def wilson(k, n):
    if n == 0: return (0, 0)
    p = k / n; z = 1.96; c = (p + z * z / (2 * n)) / (1 + z * z / n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n); return (max(0, c - h), min(1, c + h))
mon = {}; 
for j, r in enumerate(D): mon.setdefault(dt.datetime.fromtimestamp(r[0], dt.UTC).strftime("%Y-%m"), j)
starts = [j for j in mon.values() if j < len(D) - 100]
print(f"{len(D)} trades (val+exam, FTMO-filtered entries); {len(starts)} non-overlapping monthly starts")
for nm, Rs in (("IDEALISED R (original backtest)", Rid), ("GAP-AWARE R (realistic stop fills)", Rgap)):
    print(f"\n{nm}: mean {Rs.mean():+.3f}R")
    for risk in (0.005, 0.0075, 0.01):
        p1 = both = fail1 = fail2 = opn = 0
        for s in starts:
            a, j = phase(s, Rs, risk, 0.10)
            if a == "pass":
                p1 += 1; b, _ = phase(j, Rs, risk, 0.05)
                if b == "pass": both += 1
                elif b == "fail": fail2 += 1
            elif a == "fail": fail1 += 1
            else: opn += 1
        lo, hi = wilson(both, len(starts)); print(f"  risk {risk*100:.2f}%: phase1 pass {p1}/{len(starts)}, both {both}/{len(starts)} = {both/len(starts):.0%} (95% CI {lo:.0%}-{hi:.0%}); failed in P1 {fail1}, failed in P2 {fail2}, unfinished {opn}")
