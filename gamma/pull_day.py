"""Verification slice: QQQ option open interest for ONE day from Databento (06:00-12:00 UTC statistics), previous-close QQQ spot, naive dealer GEX (calls +, puts -, flat IV).
Env: DATABENTO_API_KEY, DATE (YYYY-MM-DD), MAX_USD (default 1). Cost-capped. Places no orders."""
import os, re, sys, math, datetime as dt
import numpy as np, pandas as pd, databento as db
from scipy.stats import norm
key, date, cap = os.environ["DATABENTO_API_KEY"], os.environ["DATE"], float(os.environ.get("MAX_USD", "1"))
IV = float(os.environ.get("IV", "0.22")); c = db.Historical(key)
k = dict(dataset="OPRA.PILLAR", symbols="QQQ.OPT", stype_in="parent", schema="statistics", start=f"{date}T06:00", end=f"{date}T12:00")
cost = c.metadata.get_cost(**k); print("quote $", cost, flush=True)
if cost > cap: sys.exit(f"over cap {cap}")
st = c.timeseries.get_range(**k).to_df()
oi = st[st["stat_type"] == db.StatType.OPEN_INTEREST].drop_duplicates("symbol", keep="last")[["symbol", "quantity"]].rename(columns={"quantity": "oi"})
print("contracts with OI:", len(oi), "total OI:", int(oi.oi.sum()), flush=True)
px = c.timeseries.get_range(dataset="EQUS.MINI", symbols="QQQ", schema="ohlcv-1d", start=(dt.date.fromisoformat(date) - dt.timedelta(days=7)).isoformat(), end=date).to_df()
spot = float(px["close"].iloc[-1]); print("QQQ previous close", spot, px.index[-1], flush=True)
rows = []
for sym, n in zip(oi.symbol, oi.oi):
    m = re.match(r"^QQQ\s*(\d{6})([CP])(\d{8})$", sym.strip())
    if not m: continue
    exp = dt.datetime.strptime(m.group(1), "%y%m%d"); K = int(m.group(3)) / 1000
    T = max((exp - dt.datetime.strptime(date, "%Y-%m-%d")).days + 0.5, 0.25) / 365
    rows.append((exp, m.group(2), K, T, float(n)))
d = pd.DataFrame(rows, columns=["exp", "cp", "K", "T", "oi"])
def gamma(S, K, T, v=IV):
    d1 = (np.log(S / K) + 0.5 * v * v * T) / (v * math.sqrt(1) * np.sqrt(T)); return norm.pdf(d1) / (S * v * np.sqrt(T))
def net_gex(S):
    g = gamma(S, d.K.values, d["T"].values); sign = np.where(d.cp == "C", 1, -1)
    return float((g * d.oi.values * 100 * S * S * 0.01 * sign).sum())
d["gex"] = gamma(spot, d.K.values, d["T"].values) * d.oi.values * 100 * spot * spot * 0.01 * np.where(d.cp == "C", 1, -1)
by = d.groupby("K").gex.sum()
grid = np.linspace(spot * 0.9, spot * 1.1, 201); curve = np.array([net_gex(s) for s in grid])
flip = next((float(grid[i]) for i in range(1, len(grid)) if curve[i - 1] * curve[i] < 0), None)
call_wall = float(d[d.cp == "C"].groupby("K").oi.sum().idxmax()); put_wall = float(d[d.cp == "P"].groupby("K").oi.sum().idxmax())
print(f"DATE {date} spot {spot:.2f} IV {IV} net GEX ${net_gex(spot)/1e9:.2f}bn per 1% | flip {flip} | call wall {call_wall} | put wall {put_wall}")
print("top strikes by |GEX|:"); print((by.abs().sort_values(ascending=False).head(8).index.map(lambda x: (x, round(float(by[x]) / 1e6, 1)))).tolist())
os.makedirs("gamma/out", exist_ok=True); by.to_csv(f"gamma/out/qqq_gex_{date}.csv")
