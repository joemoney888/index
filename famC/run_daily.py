"""Daily tests D1/D2, docs/FAMILY_D_DAILY_SPEC.md v1.0. Usage: python famC/run_daily.py <spy_daily.csv>. Runs once; refuses if RESULT_daily.json exists."""
import json, os, sys
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
def nw_t(x, lags):
    x = np.asarray(x, float); n = len(x); m = x.mean(); e = x - m; v = float(e @ e) / n
    for l in range(1, lags + 1): v += 2 * (1 - l / (lags + 1)) * float(e[l:] @ e[:-l]) / n
    se = (v / n) ** .5; return m / se, se
def load(p):
    d = pd.read_csv(p, parse_dates=["date"]).sort_values("date").reset_index(drop=True)
    d["r"] = d["adjusted_close"].pct_change(); return d
def d1(d):
    d = d.copy(); d["ym"] = d["date"].dt.to_period("M"); rows = []
    months = sorted(d["ym"].unique())
    for k in range(len(months) - 1):
        a = d[d["ym"] == months[k]]; b = d[d["ym"] == months[k + 1]]
        if len(a) < 2 or len(b) < 3: continue
        idx = list(a.index[-1:]) + list(b.index[:3])          # last day of M + first 3 days of M+1 (returns of days after the 2nd-to-last close)
        r = d.loc[idx, "r"].to_numpy(); rows.append((str(months[k + 1]), float(r.sum() * 1e4 - 2.0)))
    return rows
def judge(net, lags, floor):
    net = np.asarray(net); t, se = nw_t(net, lags); th = [float(net[k].mean()) for k in np.array_split(np.arange(len(net)), 3)]
    return {"n": len(net), "net_mean_bp": float(net.mean()), "t": float(t), "se_bp": float(se), "thirds_net_bp": th,
            "PASS": bool(t >= 2.8 and net.mean() >= floor and sum(v > 0 for v in th) >= 2), "opposite_t_le_-2.8": bool(t <= -2.8)}
def d2(d):
    d = d.copy(); d["sma"] = d["adjusted_close"].rolling(200).mean(); d["sig"] = (d["adjusted_close"] > d["sma"]).shift(1)
    d = d.dropna(subset=["sma", "r", "sig"]).copy(); d["sig"] = d["sig"].astype(bool)
    sw = (d["sig"] != d["sig"].shift(1)).fillna(False).to_numpy(); r = d["r"].to_numpy() * 1e4 - np.where(sw, 1.0, 0.0)   # 1 bp on the switch day, once per leg
    x = d["sig"].to_numpy().astype(float); X = np.column_stack([np.ones(len(x)), x]); b = np.linalg.lstsq(X, r, rcond=None)[0]; e = r - X @ b
    n = len(r); S = np.zeros((2, 2))
    for l in range(0, 6):
        w = 1 - l / 6; G = (X[l:] * e[l:, None]).T @ (X[:n - l] * e[:n - l, None]) / n; S += (G if l == 0 else w * (G + G.T))
    A = np.linalg.inv(X.T @ X / n); V = A @ S @ A / n; diff = float(b[1]); t = diff / float(V[1, 1] ** .5)
    th = [];
    for k in np.array_split(np.arange(n), 3): th.append(float(r[k][x[k] == 1].mean() - r[k][x[k] == 0].mean()))
    ret = d["r"].to_numpy() * x; sd = lambda z: float(z.std() * 252 ** .5)
    def stats(z): eq = np.cumprod(1 + z); dd = float((eq / np.maximum.accumulate(eq) - 1).min()); return {"cagr": float(eq[-1] ** (252 / len(z)) - 1), "maxdd": dd, "sharpe": float(z.mean() / z.std() * 252 ** .5)}
    vol = pd.Series(d["r"].to_numpy()).rolling(20).std().shift(1).to_numpy() * 252 ** .5; sz = np.clip(0.10 / vol, 0, 1.0); vt = np.where(np.isnan(sz), 0, sz) * d["r"].to_numpy()
    return {"n": n, "in_days": int(x.sum()), "diff_in_minus_out_bp": diff, "t": float(t), "thirds_diff_bp": th,
            "PASS": bool(t >= 2.8 and diff >= 3.0 and sum(v > 0 for v in th) >= 2), "opposite_t_le_-2.8": bool(t <= -2.8),
            "descriptive": {"buy_hold": stats(d["r"].to_numpy()), "trend_in_market": stats(ret), "vol_target_10pct_always_in": stats(vt)}}
def main():
    out = os.path.join(HERE, "RESULT_daily.json")
    if os.path.exists(out): sys.exit("run once: result exists")
    d = load(sys.argv[1]); rows = d1(d); res = {"D1_turn_of_month": judge([x[1] for x in rows], 1, 4.0), "D2_trend_200d": d2(d), "window": [str(d["date"].min().date()), str(d["date"].max().date())]}
    json.dump(res, open(out, "w"), indent=1); print(json.dumps(res, indent=1))
if __name__ == "__main__": main()
