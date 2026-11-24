"""D1b and D3, docs/FAMILY_D_DAILY_SPEC.md addendum v1.1. Usage: python famC/run_daily2.py <spx_csv DATE,SPX mm/dd/yyyy> <dates_cpi> <dates_nfp> <dates_retail>. Runs once."""
import importlib.util, json, os, re, sys
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
sp = importlib.util.spec_from_file_location("rd", os.path.join(HERE, "run_daily.py")); rd = importlib.util.module_from_spec(sp); sp.loader.exec_module(rd)
def load_spx(p):
    d = pd.read_csv(p); d["date"] = pd.to_datetime(d["DATE"], format="%m/%d/%Y"); d = d.sort_values("date").reset_index(drop=True)
    d["adjusted_close"] = d["SPX"]; d["r"] = d["adjusted_close"].pct_change(); d.loc[d["date"].diff().dt.days > 7, "r"] = np.nan; return d[["date", "adjusted_close", "r"]]
def read_dates(p): return [pd.Timestamp(l.strip()) for l in open(p) if re.fullmatch(r"\d{4}-\d\d-\d\d", l.strip())]
def d3(d, files):
    raw = [x for f in files for x in read_dates(f)]; ts = set(d["date"]); n_raw = len(raw)
    wk = sum(1 for x in raw if x.weekday() >= 5); cleaned = sorted({x for x in raw if x.weekday() < 5 and x >= pd.Timestamp("1975-01-02") and x in ts})
    notrade = sum(1 for x in set(raw) if x.weekday() < 5 and x >= pd.Timestamp("1975-01-02") and x not in ts)
    ev = d[d["date"].isin(cleaned)].dropna(subset=["r"]); net = ev["r"].to_numpy() * 1e4 - 3.0
    res = rd.judge(net, 1, 3.0); non = d[~d["date"].isin(cleaned)].dropna(subset=["r"])["r"].to_numpy() * 1e4
    res.update({"raw_dates": n_raw, "weekend_dropped": wk, "not_trading_day_dropped": notrade, "event_days_used": len(ev), "gross_event_mean_bp": float(ev["r"].mean() * 1e4),
                "gross_nonevent_mean_bp": float(non.mean()), "event_minus_nonevent_bp": float(ev["r"].mean() * 1e4 - non.mean())}); return res
def main():
    out = os.path.join(HERE, "RESULT_daily2.json")
    if os.path.exists(out): sys.exit("run once: result exists")
    d = rd.load.__globals__["pd"] and load_spx(sys.argv[1]); rows = rd.d1(d)
    res = {"D1b_turn_of_month_official": rd.judge([x[1] for x in rows], 1, 4.0)}
    a = [x[1] for x in rows if x[0] < "1993-01"]; b = [x[1] for x in rows if x[0] >= "1993-01"]
    res["D1b_descriptive"] = {"1975_92": {"n": len(a), "net_mean_bp": float(np.mean(a)), "t": float(rd.nw_t(a, 1)[0])}, "1993_2026": {"n": len(b), "net_mean_bp": float(np.mean(b)), "t": float(rd.nw_t(b, 1)[0])}}
    res["D3_announcement_day"] = d3(d, sys.argv[2:5]); res["window"] = [str(d["date"].min().date()), str(d["date"].max().date())]
    json.dump(res, open(out, "w"), indent=1); print(json.dumps(res, indent=1))
if __name__ == "__main__": main()
