"""Cost-stack rerun + sensitivity tests for the NAS100 BFG rule (FTMO-filtered entries).
Detail simulator = agent/search.py trades() (non-runner path) re-implemented to also return entry/exit prices, exit reason and path, so extra costs can be applied:
  gap : stop exits fill at the bar OPEN when the bar opens beyond the stop (backtest assumes the stop price)
  slip: extra adverse slippage on stop exits, in multiples of the bar's spread
  fin : overnight financing per 22:00 UTC rollover crossed (long 6.5%/yr, short 3%/yr of notional; estimates)
  com : commission in bps of notional per side
"""
import sys, json, numpy as np
sys.path.insert(0, "/home/claude/index/ftmo"); sys.path.insert(0, "/home/claude/index")
import ftmo_filters as F
from agent import search
P = json.load(open("/home/claude/index/search/NAS100/finalists.json"))[0]["p"]

def detail(p, d, f, mask, lo, hi):
    """returns structured rows: t_entry, i, side, e, risk, n(bars held), reason(0 stop,1 target,2 time), R_base, ex_stop_price, open_gap_price"""
    w = np.array(p["w"]); score = f["F"][lo:hi] @ w / np.abs(w).sum() * 2
    hrs = f["hour"][lo:hi]; g = f["gates"][p.get("gate", "none")] & ~mask
    ok = (np.abs(score) >= p["theta"]) & (hrs >= p["h0"]) & (hrs < p["h1"]) & f["valid"][lo:hi]
    if p["trend"]: ok &= np.sign(score) == f["trend"][lo:hi]
    ok &= g[lo:hi]
    idx = np.flatnonzero(ok) + lo; H = p["H"]; idx = idx[idx + H + 2 < hi]
    out, free = [], -1; cand = idx; side_all = np.sign(score[cand - lo]); k = 0
    while k < len(cand):
        i = cand[k]
        if i < free: k = int(np.searchsorted(cand, free)); continue
        side = side_all[k]; e = d["o"][i + 1] + side * d["s"][i] / 2; a = f["atr"][i]; risk = p["ks"] * a
        if risk <= 0: k += 1; continue
        hh, ll = d["h"][i + 1:i + 1 + H], d["l"][i + 1:i + 1 + H]; oo = d["o"][i + 1:i + 1 + H]; half = d["s"][i] / 2; td = p.get("td", 0.0)
        if side > 0:
            stop, tgt = e - risk, e + p["kt"] * a
            if td:
                cm = np.maximum.accumulate(hh); prev = np.concatenate([[-np.inf], cm[:-1]])
                st = np.where(prev - e >= p["ts"] * a, np.maximum(stop, prev - td * a), stop)
            else: st = np.full(len(ll), stop)
            hs = ll - half <= st; ht = hh - half >= tgt
        else:
            stop, tgt = e + risk, e - p["kt"] * a
            if td:
                cm = np.minimum.accumulate(ll); prev = np.concatenate([[np.inf], cm[:-1]])
                st = np.where(e - prev >= p["ts"] * a, np.minimum(stop, prev + td * a), stop)
            else: st = np.full(len(hh), stop)
            hs = hh + half >= st; ht = ll + half <= tgt
        js = int(np.argmax(hs)) if hs.any() else H; jt = int(np.argmax(ht)) if ht.any() else H
        gapfill = np.nan
        if js <= jt and js < H:
            ex, n, reason = st[js], js, 0
            gapfill = min(st[js], oo[js] - half) if side > 0 else max(st[js], oo[js] + half)
        elif jt < js: ex, n, reason = tgt, jt, 1
        else: ex, n, reason = d["c"][i + H] - side * half, H - 1, 2
        out.append((d["t"][i], i, side, e, risk, n, reason, side * (ex - e) / risk, ex, gapfill, half * 2))
        free = i + 1 + n + 1; k = int(np.searchsorted(cand, free))
    return np.array(out) if out else np.empty((0, 11))

def net_R(D, d, gap=False, slip=0.0, fin=False, com_bps=0.0):
    R = D[:, 7].copy(); side, e, risk = D[:, 2], D[:, 3], D[:, 4]; stopm = D[:, 6] == 0
    if gap:
        gp = np.where(stopm, D[:, 9], D[:, 8]); R = np.where(stopm, side * (gp - e) / risk, R)
    if slip: R = R - np.where(stopm, slip * D[:, 10] / risk, 0.0)
    if fin:
        i = D[:, 1].astype(int); n = D[:, 5].astype(int); t0 = d["t"][i + 1]; t1 = d["t"][np.minimum(i + 1 + n, len(d["t"]) - 1)]
        nights = np.array([max(0, int(((b - 22 * 3600) // 86400) - ((a - 22 * 3600) // 86400))) for a, b in zip(t0, t1)])
        rate = np.where(side > 0, 0.065, 0.03)
        R = R - (rate * nights / 365) * e / risk
    if com_bps: R = R - 2 * com_bps * 1e-4 * e / risk
    return R

def summ(tag, t, R):
    r = search.day_t(np.column_stack([t, R])); return f"{tag:44s} n={r['n']:5d} mean {r['mean']:+.3f}R t {r['t']:5.2f}"

if __name__ == "__main__":
    d = search.load_arrays("/home/claude/gbpusd-paper-agent/data/bars5/NAS100.csv.gz"); f = search.build_features(d)
    t = d["t"]; v0, e0 = search.split_points(int(t[-1])); iv, ie = int(np.searchsorted(t, v0)), int(np.searchsorted(t, e0))
    mask = F.block_mask(t, ["nfp", "fomc"], 120, False, True)
    segs = {"val+exam": (iv, len(t)), "exam": (ie, len(t))}
    for nm, (lo, hi) in segs.items():
        D = detail(P, d, f, mask, lo, hi)
        chk = F.run("D", d, f, P, mask, lo, hi); assert len(chk) == len(D) and abs(chk[:, 1].mean() - D[:, 7].mean()) < 1e-9, "detail simulator differs from engine"
        T = D[:, 0]; print(f"\n=== COST STACK | {nm} | detail simulator matches engine (n={len(D)}) ===")
        print(summ("A backtest as is", T, D[:, 7]))
        print(summ("B + stop gaps fill at bar open", T, net_R(D, d, gap=True)))
        print(summ("C + extra stop slippage 1x spread", T, net_R(D, d, gap=True, slip=1)))
        print(summ("D + financing (6.5% long/3% short)", T, net_R(D, d, gap=True, slip=1, fin=True)))
        for bp in (0.25, 0.5, 1.0):
            print(summ(f"E + commission {bp} bp/side", T, net_R(D, d, gap=True, slip=1, fin=True, com_bps=bp)))
        stopm = D[:, 6] == 0; rs = D[:, 4] / D[:, 3] * 1e4
        print(f"stop distance: median {np.median(rs):.0f} bp of price; median spread {np.median(D[:,10]/D[:,3]*1e4):.2f} bp; stop exits gapped through: {np.mean(D[stopm,9]!=D[stopm,8]):.1%} of stop exits")
        print("exit reasons (share, mean R):", {k: (f"{np.mean(D[:,6]==c):.0%}", f"{D[D[:,6]==c,7].mean():+.2f}") for k, c in (("stop", 0), ("target", 1), ("time", 2))})
        print("held overnight (crossed 22:00 UTC):", f"{np.mean(np.array([int((((d['t'][min(int(i)+1+int(n),len(t)-1)])-22*3600)//86400)-((d['t'][int(i)+1]-22*3600)//86400))>0 for i,n in zip(D[:,1],D[:,5])])):.0%}")
    print("\n=== SENSITIVITY (engine, FTMO-filtered entries; train / val / exam) ===")
    def seg_tr(p, gate=None):
        g = dict(f["gates"]); 
        if gate is not None: g["x2"] = gate; p = dict(p, gate="x2")
        f2 = dict(f); f2["gates"] = g; out = []
        for lo, hi in ((0, iv), (iv, ie), (ie, len(t))):
            out.append(search.day_t(F.run("s", d, f2, p, mask, lo, hi)))
        return out
    exp = f["gates"]["atr_expanding"]
    cases = {"baseline": (P, None), "trailing stop OFF": (dict(P, td=0.0), None), "trail 1.5 ATR": (dict(P, td=1.5), None), "trail 2.0 ATR": (dict(P, td=2.0), None),
             "gate OFF (all bars)": (P, np.ones(len(t), bool)), "gate INVERTED (vol not expanding)": (P, ~exp)}
    for nm, (p, gt) in cases.items():
        r = seg_tr(p, gt); print(f"{nm:34s} " + " | ".join(f"{s} n={x['n']:5d} {x['mean']:+.3f}R t={x['t']:5.2f}" for s, x in zip(("train", "val", "exam"), r)))
