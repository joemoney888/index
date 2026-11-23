"""Europe-open runner, docs/FAMILY_C_EUROPE_OPEN_SPEC.md v1.0. Usage: python famC/run_europe.py <bars5 csv.gz t,o,h,l,c,spread> <label: discovery|replication> [fixed_half_spread_bp]
Run ONCE per label; refuses if RESULT_<label>.json exists."""
import gzip, json, os, sys
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); NY = "America/New_York"
WIN = {"discovery": ("2021-05-20", "2026-11-16"), "replication": ("2016-11-15", "2021-05-18")}
def load(path):
    a = np.loadtxt(gzip.open(path, "rt"), delimiter=",", skiprows=1)
    return a[:, 0].astype("int64"), a[:, 1], a[:, 4], (a[:, 5] if a.shape[1] > 5 else None)
def nw_t(x, lags=5):
    x = np.asarray(x, float); n = len(x); m = x.mean(); e = x - m; v = float(e @ e) / n
    for l in range(1, lags + 1): v += 2 * (1 - l / (lags + 1)) * float(e[l:] @ e[:-l]) / n
    se = (v / n) ** .5; return m / se, se
def run(t, o, c, s, start, end, fixed_hs_bp=None):
    idx = {int(x): i for i, x in enumerate(t)}; rows = []; skips = {"missing": 0, "under44": 0}
    for D in pd.date_range(start, end, freq="D"):
        if D.weekday() == 4 or D.weekday() == 5: continue          # Sun-Thu evenings
        e = int(pd.Timestamp(f"{D.date()} 23:30", tz=NY).timestamp()); nd = D + pd.Timedelta(days=1)
        x = int(pd.Timestamp(f"{nd.date()} 03:25", tz=NY).timestamp())
        if e not in idx or x not in idx: skips["missing"] += 1; continue
        if sum(1 for k in range(48) if e + 300 * k in idx) < 44: skips["under44"] += 1; continue
        i, j = idx[e], idx[x]
        he = (fixed_hs_bp * o[i] / 1e4) if fixed_hs_bp is not None else s[i] / 2
        hx = (fixed_hs_bp * c[j] / 1e4) if fixed_hs_bp is not None else s[j] / 2
        pe, px = o[i] + he, c[j] - hx
        rows.append((D.date(), (px - pe) / pe * 1e4, (c[j] / o[i] - 1) * 1e4))
    return rows, skips
def summarise(rows):
    net = np.array([r[1] for r in rows]); gr = np.array([r[2] for r in rows]); t, se = nw_t(net)
    th = [float(net[k].mean()) for k in np.array_split(np.arange(len(net)), 3)]
    a, b, cc = t >= 2.8, net.mean() >= 1.0, sum(v > 0 for v in th) >= 2
    return {"n": len(net), "net_mean_bp": float(net.mean()), "gross_mean_bp": float(gr.mean()), "nw_se_bp": float(se), "t": float(t), "thirds_net_bp": th,
            "rule_a_t_ge_2.8": bool(a), "rule_b_net_ge_1bp": bool(b), "rule_c_2of3": bool(cc), "PASS": bool(a and b and cc), "opposite_t_le_-2.8": bool(t <= -2.8)}
def main():
    path, label = sys.argv[1:3]; fixed = float(sys.argv[3]) if len(sys.argv) > 3 else None
    out = os.path.join(HERE, f"RESULT_europe_{label}.json")
    if os.path.exists(out): sys.exit("run once: result exists")
    t, o, c, s = load(path); rows, sk = run(t, o, c, s, *WIN[label], fixed_hs_bp=fixed); r = summarise(rows)
    if label == "replication": r["PASS"] = bool(r["net_mean_bp"] > 0 and r["t"] >= 2.0 and r["net_mean_bp"] >= 0.5)
    r["skips"] = sk; r["window"] = WIN[label]; json.dump(r, open(out, "w"), indent=1); print(json.dumps(r, indent=1))
if __name__ == "__main__": main()
