"""Family A runner, implementing docs/FAMILY_A_SPEC.md v1.1 exactly. Deterministic: no randomness, nothing tuned. Run ONCE.
Usage: python famA/run.py <NAS100 5-minute csv.gz: t,o,h,l,c,spread> [out_dir]
Bar names follow the spec: a bar is named by its OPENING time (the "15:55 bar" closes at 16:00). Prices are the bar o/c in the data file; each bar pays its OWN half-spread (spread/2) at entry and exit, adverse side.
Writes RESULT.json and RESULT.md and refuses to run if RESULT.json already exists (run once)."""
import gzip, hashlib, json, os, sys
from collections import Counter
import numpy as np
import pandas as pd

START, END = "2021-05-20", "2026-11-17"
THIRDS = (("T1", "2021-05-20", "2023-03-31"), ("T2", "2023-04-03", "2025-01-31"), ("T3", "2025-02-03", "2026-11-17"))
NY, LON = "America/New_York", "Europe/London"


def load(path):
    a = np.loadtxt(gzip.open(path, "rt"), delimiter=",", skiprows=1)
    return a[:, 0].astype("int64"), a[:, 1], a[:, 4], a[:, 5]        # t, o, c, spread


def nw_t(x, lags=5):
    """t-statistic of the mean with a Newey-West (Bartlett) standard error."""
    x = np.asarray(x, float); n = len(x); m = x.mean(); e = x - m
    g0 = float(e @ e) / n; v = g0
    for l in range(1, lags + 1):
        v += 2 * (1 - l / (lags + 1)) * float(e[l:] @ e[:-l]) / n
    se = (v / n) ** 0.5
    return m / se, se


def trade_bp(side, o_ent, half_ent, c_ext, half_ext):
    """Net return in basis points: long pays the ask side at entry and sells the bid side at exit; short the reverse."""
    if side > 0:
        pe, px = o_ent + half_ent, c_ext - half_ext
        return (px - pe) / pe * 1e4
    pe, px = o_ent - half_ent, c_ext + half_ext
    return (pe - px) / pe * 1e4


def gross_bp(side, o_ent, c_ext):
    return side * (c_ext / o_ent - 1) * 1e4


def build_index(t):
    ts = pd.to_datetime(t, unit="s", utc=True)
    ny = ts.tz_convert(NY); lo = ts.tz_convert(LON)
    nyi = {(d, m): i for i, (d, m) in enumerate(zip(ny.date, ny.hour * 60 + ny.minute))}
    loi = {(d, m): i for i, (d, m) in enumerate(zip(lo.date, lo.hour * 60 + lo.minute))}
    return nyi, loi


def run_specs(t, o, c, s, cal, start=START, end=END):
    nyi, loi = build_index(t)
    hol = set(cal["full_holidays"]); early = set(cal["early_close_1300"])
    mins = lambda h, m: h * 60 + m
    days = [d.date() for d in pd.date_range(start, end, freq="D") if d.weekday() < 5]
    # session dates (any bar 09:30-15:55 on a non-holiday weekday) for the previous-trading-day anchor
    sess = sorted({d for (d, m) in nyi if mins(9, 30) <= m <= mins(15, 55) and d.isoformat() not in hol and d.weekday() < 5})
    sess_set = set(sess)
    rows = {"A5": [], "A6a": [], "A6b": []}; skips = {k: Counter() for k in rows}
    for D in days:
        iso = D.isoformat()
        if iso in hol or iso in early:
            for k in rows: skips[k]["calendar"] += 1
            continue
        nbars = sum(1 for m in range(mins(9, 30), mins(16, 0), 5) if (D, m) in nyi)
        if nbars < 78:
            for k in rows: skips[k]["under78"] += 1
            continue
        g = lambda h, m: nyi.get((D, mins(h, m)))
        ent15, ex = g(15, 30), g(15, 55)
        # ---- A5: London leg (open of the 08:00 London bar -> close of the 09:10 NY bar), trade the OPPOSITE sign from the 09:30 open to the 15:55 close
        li, c0910, ent930 = loi.get((D, mins(8, 0))), g(9, 10), g(9, 30)
        if None in (li, c0910, ent930, ex):
            skips["A5"]["missing"] += 1
        else:
            r = c[c0910] / o[li] - 1
            if r == 0: skips["A5"]["zero signal"] += 1
            else:
                side = -1 if r > 0 else 1
                rows["A5"].append((D, side, trade_bp(side, o[ent930], s[ent930] / 2, c[ex], s[ex] / 2), gross_bp(side, o[ent930], c[ex]), s[ent930] / 2 / o[ent930] * 1e4, s[ex] / 2 / c[ex] * 1e4))
        # ---- A6a: previous trading day's close (last bar starting at or before 15:55) -> close of the 09:55 bar; same sign 15:30 open -> 15:55 close
        prev = [d for d in sess if d < D][-1:] if sess else []
        anc = None
        if prev:
            P = prev[0]; ms = [m for m in range(mins(9, 30), mins(16, 0), 5) if (P, m) in nyi]
            anc = nyi[(P, ms[-1])] if ms else None
        c0955 = g(9, 55)
        if None in (anc, c0955, ent15, ex):
            skips["A6a"]["missing"] += 1
        else:
            r = c[c0955] / c[anc] - 1
            if r == 0: skips["A6a"]["zero signal"] += 1
            else:
                side = 1 if r > 0 else -1
                rows["A6a"].append((D, side, trade_bp(side, o[ent15], s[ent15] / 2, c[ex], s[ex] / 2), gross_bp(side, o[ent15], c[ex]), s[ent15] / 2 / o[ent15] * 1e4, s[ex] / 2 / c[ex] * 1e4))
        # ---- A6b: open of the 15:00 bar -> close of the 15:25 bar; same sign 15:30 open -> 15:55 close
        o1500, c1525 = g(15, 0), g(15, 25)
        if None in (o1500, c1525, ent15, ex):
            skips["A6b"]["missing"] += 1
        else:
            r = c[c1525] / o[o1500] - 1
            if r == 0: skips["A6b"]["zero signal"] += 1
            else:
                side = 1 if r > 0 else -1
                rows["A6b"].append((D, side, trade_bp(side, o[ent15], s[ent15] / 2, c[ex], s[ex] / 2), gross_bp(side, o[ent15], c[ex]), s[ent15] / 2 / o[ent15] * 1e4, s[ex] / 2 / c[ex] * 1e4))
    return rows, skips, len(days)


def summarise(rows):
    out = {}
    for k, r in rows.items():
        d = [x[0] for x in r]; net = np.array([x[2] for x in r]); gr = np.array([x[3] for x in r])
        t, se = nw_t(net)
        thirds = {}
        for nm, a, b in THIRDS:
            sel = [(a <= x[0].isoformat() <= b) for x in r]; v = net[sel]; w = gr[sel]
            thirds[nm] = {"n": int(len(v)), "net_mean_bp": float(v.mean()), "gross_mean_bp": float(w.mean())}
        a_ok = bool(t >= 2.8); b_ok = bool(net.mean() >= 1.0); c_ok = sum(1 for v in thirds.values() if v["net_mean_bp"] > 0) >= 2
        out[k] = {"n_used": int(len(r)), "net_mean_bp": float(net.mean()), "nw_se_bp": float(se), "t": float(t), "gross_mean_bp": float(gr.mean()),
                  "mean_half_spread_entry_bp": float(np.mean([x[4] for x in r])), "mean_half_spread_exit_bp": float(np.mean([x[5] for x in r])),
                  "thirds": thirds, "rule_a_t_ge_2.8": a_ok, "rule_b_net_ge_1bp": b_ok, "rule_c_two_of_three_thirds_positive": bool(c_ok),
                  "PASS": bool(a_ok and b_ok and c_ok), "opposite_direction_significant_t_le_-2.8": bool(t <= -2.8)}
    return out


def main():
    path = sys.argv[1]; od = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(os.path.abspath(__file__))
    res = os.path.join(od, "RESULT.json")
    if os.path.exists(res):
        sys.exit("RESULT.json exists: Family A is run ONCE. Refusing.")
    cal = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "calendar.json")))
    t, o, c, s = load(path)
    rows, skips, ndays = run_specs(t, o, c, s, cal)
    out = {"spec": "docs/FAMILY_A_SPEC.md v1.1", "data_sha256": hashlib.sha256(open(path, "rb").read()).hexdigest(), "window": [START, END], "weekdays_in_window": ndays,
           "skips": {k: dict(v) for k, v in skips.items()}, "specs": summarise(rows)}
    a, b = {x[0]: x[2] for x in rows["A6a"]}, {x[0]: x[2] for x in rows["A6b"]}
    both = sorted(set(a) & set(b))
    out["corr_A6a_A6b_daily_net_bp"] = float(np.corrcoef([a[d] for d in both], [b[d] for d in both])[0, 1]) if len(both) > 2 else None
    json.dump(out, open(res, "w"), indent=1)
    L = ["# Family A result (spec v1.1), run once", "", f"Window {START} to {END}, {ndays} weekdays. Data sha256 {out['data_sha256'][:16]}...", "",
         "| Spec | n used | skips | net mean bp | t (NW5) | gross mean bp | T1 / T2 / T3 net bp | rule a | rule b | rule c | PASS |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for k, v in out["specs"].items():
        th = " / ".join(f"{v['thirds'][x]['net_mean_bp']:+.2f}" for x in ("T1", "T2", "T3"))
        L.append(f"| {k} | {v['n_used']} | {dict(skips[k])} | {v['net_mean_bp']:+.2f} | {v['t']:+.2f} | {v['gross_mean_bp']:+.2f} | {th} | {v['rule_a_t_ge_2.8']} | {v['rule_b_net_ge_1bp']} | {v['rule_c_two_of_three_thirds_positive']} | {v['PASS']} |")
    L += ["", f"Correlation of the A6a and A6b daily net series: {out['corr_A6a_A6b_daily_net_bp']:.3f}.", "Opposite-direction significant (t <= -2.8): " + ", ".join(f"{k}: {v['opposite_direction_significant_t_le_-2.8']}" for k, v in out["specs"].items())]
    open(os.path.join(od, "RESULT.md"), "w").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
