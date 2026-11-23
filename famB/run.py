"""Family B + ORB runner implementing docs/FAMILY_B_SPEC.md v1. Deterministic, run ONCE (refuses if RESULT.json exists).
Usage: python famB/run.py <NAS100 5-minute csv.gz t,o,h,l,c,spread> [out_dir]"""
import gzip, hashlib, json, os, sys
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
START, END = "2021-05-20", "2026-11-17"
NY = "America/New_York"

def load(path):
    a = np.loadtxt(gzip.open(path, "rt"), delimiter=",", skiprows=1)
    return a[:, 0].astype("int64"), a[:, 1], a[:, 2], a[:, 3], a[:, 4], a[:, 5]

def tstat(x):
    x = np.asarray(x, float); return float(x.mean() / (x.std(ddof=1) / len(x) ** .5)) if len(x) > 2 else float("nan")

def trade_bp(side, o_ent, h_ent, c_ext, h_ext):
    if side > 0: pe, px = o_ent + h_ent, c_ext - h_ext; return (px - pe) / pe * 1e4
    pe, px = o_ent - h_ent, c_ext + h_ext; return (pe - px) / pe * 1e4

def summarise(dates, vals, floor):
    v = np.array(vals); idx = np.array_split(np.arange(len(v)), 3)
    th = [float(v[i].mean()) for i in idx]; t = tstat(v)
    a, b, c = t >= 2.8, v.mean() >= floor, sum(x > 0 for x in th) >= 2
    return {"n": len(v), "net_mean": float(v.mean()), "t": t, "thirds_net_mean": th, "rule_a": bool(a), "rule_b": bool(b), "rule_c": bool(c), "PASS": bool(a and b and c), "opposite_t_le_-2.8": bool(t <= -2.8)}

def run_all(t, o, h, l, c, s, cal, fomc, start=START, end=END):
    ts = pd.to_datetime(t, unit="s", utc=True).tz_convert(NY)
    ix = {(d, m): i for i, (d, m) in enumerate(zip(ts.date, ts.hour * 60 + ts.minute))}
    hol, early = set(cal["full_holidays"]), set(cal["early_close_1300"])
    M = lambda hh, mm: hh * 60 + mm
    days = [d.date() for d in pd.date_range(start, end, freq="D") if d.weekday() < 5 and d.date().isoformat() not in hol]
    prev = {days[i]: days[i - 1] for i in range(1, len(days))}
    hs = lambda i: s[i] / 2
    out = {"F1": ([], []), "F2": ([], []), "ORB": ([], [])}; skips = {"F1": 0, "F2": 0, "ORB_nosignal": 0, "ORB_skipped_day": 0, "ORB_bad_R": 0}
    for ds in fomc["decision_days"]:
        D = pd.Timestamp(ds).date()
        if not (start <= ds <= end): continue
        P = prev.get(D); g = lambda d, hh, mm: ix.get((d, M(hh, mm)))
        e, x = (g(P, 14, 0) if P else None), g(D, 13, 55)
        if None in (e, x): skips["F1"] += 1
        else: out["F1"][0].append(ds); out["F1"][1].append(trade_bp(1, o[e], hs(e), c[x], hs(x)))
        a, b, en, ex = g(D, 14, 0), g(D, 14, 25), g(D, 14, 30), g(D, 15, 55)
        if None in (a, b, en, ex) or c[b] == o[a]: skips["F2"] += 1
        else:
            side = 1 if c[b] > o[a] else -1
            out["F2"][0].append(ds); out["F2"][1].append(trade_bp(side, o[en], hs(en), c[ex], hs(ex)))
    for D in days:
        iso = D.isoformat()
        if iso in early or sum(1 for m in range(M(9, 30), M(16, 0), 5) if (D, m) in ix) < 78: skips["ORB_skipped_day"] += 1; continue
        rb = [ix.get((D, M(9, 30) + 5 * k)) for k in range(3)]
        if None in rb: skips["ORB_skipped_day"] += 1; continue
        hi, lo = max(h[i] for i in rb), min(l[i] for i in rb)
        sig = None
        for m in range(M(9, 45), M(11, 25) + 1, 5):
            i = ix.get((D, m))
            if i is None: continue
            if c[i] > hi: sig = (1, m); break
            if c[i] < lo: sig = (-1, m); break
        if sig is None: skips["ORB_nosignal"] += 1; continue
        side, m = sig; ie = ix.get((D, m + 5))
        if ie is None: skips["ORB_skipped_day"] += 1; continue
        entry = o[ie] + side * hs(ie); stop = lo if side > 0 else hi
        R = (entry - stop) * side
        if R <= 0: skips["ORB_bad_R"] += 1; continue
        target = entry + side * 2 * R; res = None
        for mm in range(m + 5, M(15, 55) + 1, 5):
            i = ix.get((D, mm))
            if i is None: continue
            if side > 0:
                if o[i] <= stop: px = o[i]; res = "stop"
                elif l[i] <= stop: px = stop; res = "stop"
                elif h[i] >= target: px = target; res = "tgt"
            else:
                if o[i] >= stop: px = o[i]; res = "stop"
                elif h[i] >= stop: px = stop; res = "stop"
                elif l[i] <= target: px = target; res = "tgt"
            if res: px = px - side * hs(i); break
        if res is None:
            i = ix.get((D, M(15, 55)))
            if i is None: skips["ORB_skipped_day"] += 1; continue
            px = c[i] - side * hs(i)
        out["ORB"][0].append(iso); out["ORB"][1].append((px - entry) * side / R)
    return out, skips

def main():
    path = sys.argv[1]; od = sys.argv[2] if len(sys.argv) > 2 else HERE; res = os.path.join(od, "RESULT.json")
    if os.path.exists(res): sys.exit("RESULT.json exists: run ONCE. Refusing.")
    cal = json.load(open(os.path.join(HERE, "..", "famA", "calendar.json"))); fomc = json.load(open(os.path.join(HERE, "fomc.json")))
    t, o, h, l, c, s = load(path)
    out, skips = run_all(t, o, h, l, c, s, cal, fomc)
    floors = {"F1": 15.0, "F2": 10.0, "ORB": 0.05}
    R = {k: summarise(*out[k], floors[k]) for k in out}
    json.dump({"spec": "docs/FAMILY_B_SPEC.md v1", "data_sha256": hashlib.sha256(open(path, "rb").read()).hexdigest(), "skips": skips, "results": R}, open(res, "w"), indent=1)
    L = ["# Family B + ORB result (spec v1), run once", "", "| Spec | n | net mean | t | thirds | a | b | c | PASS |", "|---|---|---|---|---|---|---|---|---|"]
    for k, v in R.items():
        u = "R" if k == "ORB" else "bp"
        L.append(f"| {k} | {v['n']} | {v['net_mean']:+.3f} {u} | {v['t']:+.2f} | " + " / ".join(f"{x:+.2f}" for x in v["thirds_net_mean"]) + f" | {v['rule_a']} | {v['rule_b']} | {v['rule_c']} | {v['PASS']} |")
    L += ["", f"Skips: {skips}"]
    open(os.path.join(od, "RESULT.md"), "w").write("\n".join(L) + "\n"); print("\n".join(L))

if __name__ == "__main__": main()
