"""Does any version of the trailing stop keep the edge when fills are realistic? Entries = the 5-minute engine's (FTMO-filtered) entries; exits re-simulated on 1-MINUTE bars (2023-11 .. 2026-11).
 U=5 : stop level updated only every 5 minutes from the best price known then (what the live agent does: it moves the stop once per poll) ; if price is already beyond the new level the exit is at market (that minute's open).
 U=1 : stop level updated every minute (approximates a broker-native trailing stop). Gap-aware fills in both. Same stop/target/trail multiples."""
import sys, numpy as np
sys.path.insert(0, "/home/claude/index/ftmo"); sys.path.insert(0, "/home/claude/index")
import ftmo_filters as F, cost_stack as C
from agent import search
d5 = search.load_arrays("/home/claude/gbpusd-paper-agent/data/bars5/NAS100.csv.gz"); f = search.build_features(d5)
d1 = search.load_arrays("/home/claude/gbpusd-paper-agent/data/bars1/NAS100.csv.gz"); t1 = d1["t"]; P = C.P
mask = F.block_mask(d5["t"], ["nfp", "fomc"], 120, False, True)
lo = int(np.searchsorted(d5["t"], t1[0] + 86400 * 2)); D = C.detail(P, d5, f, mask, lo, len(d5["t"]))
def sim(row, U, trail=True):
    i = int(row[1]); side, e, risk = row[2], row[3], row[4]; a = risk / P["ks"]; tstart = d5["t"][i + 1]
    j0 = int(np.searchsorted(t1, tstart)); jn = int(np.searchsorted(t1, tstart + P["H"] * 300))
    if j0 >= len(t1) or jn - j0 < 5: return np.nan
    hi, lw, op, cl, sp = d1["h"][j0:jn], d1["l"][j0:jn], d1["o"][j0:jn], d1["c"][j0:jn], d1["s"][j0:jn] / 2
    stop0 = e - side * risk; tgt = e + side * P["kt"] * a; best = e; level = stop0
    for k in range(len(hi)):
        if k % U == 0 and k > 0 and trail:                 # update level from best price known BEFORE this minute
            if side * (best - e) >= P["ts"] * a: level = max(level, best - P["td"] * a) if side > 0 else min(level, best + P["td"] * a)
        if side > 0:
            if lw[k] - sp[k] <= level:  return (min(level, op[k] - sp[k]) - e) / risk
            if hi[k] - sp[k] >= tgt:    return (tgt - e) / risk
            best = max(best, hi[k])
        else:
            if hi[k] + sp[k] >= level:  return (e - max(level, op[k] + sp[k])) / risk
            if lw[k] + sp[k] <= tgt:    return (e - tgt) / risk
            best = min(best, lw[k])
    return side * (cl[-1] - side * sp[-1] - e) / risk
T = D[:, 0]; print(f"{len(D)} trades on 1-minute coverage (from {T[0]:.0f})")
base = D[:, 7]; print(C.summ("5-min engine as is (same trades)", T, base))
for nm, U, tr in (("1-min, update every 5 min (live agent), gap-aware", 5, True), ("1-min, update every 1 min (native trail), gap-aware", 1, True), ("1-min, NO trailing stop, gap-aware", 5, False)):
    R = np.array([sim(r, U, tr) for r in D]); ok = ~np.isnan(R); print(C.summ(nm, T[ok], R[ok]), f"| last 365d: " + C.summ("", T[ok][T[ok] >= T[-1] - 365 * 86400], R[ok][T[ok] >= T[-1] - 365 * 86400]).strip())
