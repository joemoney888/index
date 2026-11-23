"""F1b runner on OANDA NAS100 1-minute files. Usage: python famB/run_f1b.py <events.json> <data_dir NAS100_USD> <label> [statement_times.json]
Each event: long from the open of the 5-minute window starting at (statement time) on the previous weekday to the close of the last 1-minute bar before (statement time) on the decision day. Default statement time 14:00 NY. Run ONCE per label."""
import json, os, sys, glob
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); NY = "America/New_York"
def load(dd, years):
    fs = [f for y in years for f in glob.glob(f"{dd}/{y}/oanda-NAS100_USD-{y}-*.csv")]
    d = pd.concat([pd.read_csv(f, parse_dates=["time"]) for f in fs]).sort_values("time")
    d["time"] = d["time"].dt.tz_localize("UTC"); return d.reset_index(drop=True)
def main():
    ev_path, dd, label = sys.argv[1:4]; st = json.load(open(sys.argv[4])) if len(sys.argv) > 4 else {}
    out = os.path.join(HERE, f"RESULT_{label}.json")
    if os.path.exists(out): sys.exit("already run once")
    ev = json.load(open(ev_path))["decision_days"]; years = sorted({int(e[:4]) for e in ev} | {int(e[:4]) - 1 for e in ev if e[5:7] == "01"})
    d = load(dd, years); t = d["time"].astype("int64").to_numpy() // 10**9; o, c = d["open"].to_numpy(), d["close"].to_numpy()
    def first_open(ts0):                       # first bar in [ts0, ts0+300)
        i = np.searchsorted(t, ts0); return o[i] if i < len(t) and t[i] < ts0 + 300 else None
    def last_close(ts1):                       # last bar in [ts1-300, ts1)
        j = np.searchsorted(t, ts1) - 1; return c[j] if j >= 0 and t[j] >= ts1 - 300 else None
    def ts(date, hm): h, m = (int(x) for x in hm.split(":")); return int(pd.Timestamp(f"{date} {h:02d}:{m:02d}", tz=NY).timestamp())
    res = {}
    for hs in (1.0, 2.5, 5.0):
        v = []; used = []; skipped = []
        for e in ev:
            hm = st.get(e, "14:00"); D = pd.Timestamp(e); P = D - pd.Timedelta(days=1 if D.weekday() > 0 else 3)
            a = first_open(ts(P.date(), hm)); b = last_close(ts(e, hm))
            if a is None or b is None: skipped.append(e); continue
            pe, px = a * (1 + hs / 1e4), b * (1 - hs / 1e4); v.append((px - pe) / pe * 1e4); used.append(e)
        v = np.array(v); idx = np.array_split(np.arange(len(v)), 3); th = [float(v[i].mean()) for i in idx]
        t_ = float(v.mean() / (v.std(ddof=1) / len(v) ** .5))
        res[str(hs)] = {"n": len(v), "skipped": skipped, "net_mean_bp": float(v.mean()), "t": t_, "thirds": th, "PASS": bool(v.mean() >= 15 and t_ >= 2.0 and sum(x > 0 for x in th) >= 2)}
    json.dump(res, open(out, "w"), indent=1); print(label, json.dumps(res, indent=1))
if __name__ == "__main__": main()
