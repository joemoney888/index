"""F1 replication on the sealed 2016-11-15..2021-05-18 window. Run ONCE. Usage: python famB/replicate_f1.py <kaggle utc csv.gz> <agent NAS100 5m csv.gz>"""
import gzip, json, os, sys
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); NY = "America/New_York"
def rd(p):
    a = np.loadtxt(gzip.open(p, "rt"), delimiter=",", skiprows=1); return a
def main():
    out = os.path.join(HERE, "REPLICATION_F1.json")
    if os.path.exists(out): sys.exit("already run once")
    k = rd(sys.argv[1]); ag = rd(sys.argv[2])
    # slot median half-spread in bp from the 2021-2026 agent data
    ta = pd.to_datetime(ag[:, 0].astype("int64"), unit="s", utc=True).tz_convert(NY)
    bp = ag[:, 5] / 2 / ag[:, 4] * 1e4; slot = ta.hour * 60 + ta.minute
    med = {m: float(np.median(bp[slot == m])) for m in (14 * 60, 13 * 60 + 55)}
    t = k[:, 0].astype("int64"); o, c = k[:, 1], k[:, 4]
    tk = pd.to_datetime(t, unit="s", utc=True).tz_convert(NY)
    ix = {(d, m): i for i, (d, m) in enumerate(zip(tk.date, tk.hour * 60 + tk.minute))}
    cal = json.load(open(os.path.join(HERE, "..", "famA", "calendar.json"))); hol = set(cal["full_holidays"])
    sessions = sorted({d for (d, m) in ix if 9 * 60 + 30 <= m <= 15 * 60 + 55 and d.weekday() < 5})
    fm = json.load(open(os.path.join(HERE, "fomc_2016_2021.json")))["decision_days"]
    res = {}
    for mult in (1.0, 1.5):
        v = []; used = []
        for ds in fm:
            D = pd.Timestamp(ds).date(); pr = [d for d in sessions if d < D][-1:]
            if not pr: continue
            e, x = ix.get((pr[0], 14 * 60)), ix.get((D, 13 * 60 + 55))
            if e is None or x is None: continue
            he, hx = med[14 * 60] * mult / 1e4 * o[e], med[13 * 60 + 55] * mult / 1e4 * c[x]
            pe, px = o[e] + he, c[x] - hx; v.append((px - pe) / pe * 1e4); used.append(ds)
        v = np.array(v); tt = float(v.mean() / (v.std(ddof=1) / len(v) ** .5))
        res[str(mult)] = {"n": len(v), "net_mean_bp": float(v.mean()), "t": tt, "skipped": len(fm) - len(v), "PASS": bool(v.mean() > 0 and tt >= 2.0 and v.mean() >= 7.5)}
    json.dump({"half_spread_bp_used": {str(k_): v for k_, v in med.items()}, "results": res}, open(out, "w"), indent=1); print(json.dumps(res, indent=1), med)
if __name__ == "__main__": main()
