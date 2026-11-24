"""D4 VIX panic-spike long and D5 option-expiration-week long, docs/FAMILY_D_DAILY_SPEC.md addendum v1.2. Usage: python famC/run_daily3.py <spx csv> <vix csv>. Runs once."""
import importlib.util, json, os, sys
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
def _load(n, f):
    sp = importlib.util.spec_from_file_location(n, os.path.join(HERE, f)); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
rd = _load("rd", "run_daily.py"); r2 = _load("r2", "run_daily2.py")
COST = 3.0
def load_vix(p):
    v = pd.read_csv(p); v["date"] = pd.to_datetime(v["DATE"], format="%m/%d/%Y"); return v.sort_values("date").set_index("date")["CLOSE"]
def d4(spx, vix, mult=1.4, floor_lvl=20.0, last="2026-11-13", first="1990-01-02"):
    j = pd.concat([spx.rename("spx"), vix.rename("vix")], axis=1, join="inner").dropna(); j = j[j.index >= "1989-12-01"]
    v = j["vix"].to_numpy(); s = j["spx"].to_numpy(); idx = j.index; ev = []; t = 10
    while t < len(j) - 5:
        med = np.median(v[t - 10:t])
        if idx[t] >= pd.Timestamp(first) and idx[t] <= pd.Timestamp(last) and v[t] >= mult * med and v[t] >= floor_lvl:
            ev.append((idx[t], (s[t + 5] / s[t] - 1) * 1e4 - COST)); t += 10
        else: t += 1
    return ev
def d5(spx):
    ts = spx.index; rows = []
    for ym in pd.period_range("1975-01", "2026-11", freq="M"):
        fr = [d for d in pd.date_range(ym.start_time, ym.end_time, freq="D") if d.weekday() == 4]
        x = fr[2]; e = x - pd.Timedelta(days=7)
        def on_or_before(d):
            k = ts.searchsorted(d, side="right") - 1
            return ts[k] if k >= 0 else None
        xd, ed = on_or_before(x), on_or_before(e)
        if xd is None or ed is None or xd > ts[-1] or x > ts[-1] or ed >= xd: continue
        rows.append((xd, (spx[xd] / spx[ed] - 1) * 1e4 - COST))
    return rows
def main():
    out = os.path.join(HERE, "RESULT_daily3.json")
    if os.path.exists(out): sys.exit("run once: result exists")
    spx = r2.load_spx(sys.argv[1]).set_index("date")["adjusted_close"]; vix = load_vix(sys.argv[2])
    ev = d4(spx, vix); res = {"D4_vix_spike": rd.judge([x[1] for x in ev], 1, 30.0)}
    s5 = (spx.shift(-5) / spx - 1).dropna() * 1e4; res["D4_vix_spike"]["unconditional_5d_mean_bp_gross"] = float(s5["1990-01-01":].mean())
    res["D4_vix_spike"]["event_mean_gross_bp"] = float(np.mean([x[1] for x in ev]) + COST); res["D4_vix_spike"]["first_last_event"] = [str(ev[0][0].date()), str(ev[-1][0].date())]
    res["D4_vix_spike"]["sensitivities_descriptive"] = {k: {"n": len(e), "mean_net_bp": float(np.mean([x[1] for x in e]))} for k, e in (("1.35x_18", d4(spx, vix, 1.35, 18.0)), ("1.5x_25", d4(spx, vix, 1.5, 25.0)))}
    wk = d5(spx); res["D5_opex_week"] = rd.judge([x[1] for x in wk], 1, 25.0)
    s5a = (spx.shift(-5) / spx - 1).dropna() * 1e4; res["D5_opex_week"]["unconditional_5d_mean_bp_gross"] = float(s5a.mean()); res["D5_opex_week"]["event_mean_gross_bp"] = float(np.mean([x[1] for x in wk]) + COST)
    res["window"] = [str(spx.index.min().date()), str(spx.index.max().date())]
    json.dump(res, open(out, "w"), indent=1); print(json.dumps(res, indent=1))
if __name__ == "__main__": main()
