"""Read-only diagnostic for the US-index agent. Places no orders and writes no files. Uses the same data call and the same features as index_run.py, and prints,
for today's bars only, how many pass each entry condition (so a quiet day can be told apart from a data or logic problem). Prints counts and scores only."""
import json
import os
from datetime import datetime, timedelta, timezone

import numpy as np

from agent import oanda, search
from agent.index_live import MARKETS

client = oanda.OandaPractice(os.environ["OANDA_API_TOKEN_INDEX"], os.environ["OANDA_ACCOUNT_ID_INDEX"])
p = json.load(open("search/NAS100/finalists.json"))[0]["p"]
w = np.array(p["w"])
now = datetime.now(timezone.utc)
day0 = int(now.replace(hour=0, minute=0, second=0, microsecond=0).timestamp())
print("now", now.strftime("%Y-%m-%dT%H:%M:%SZ"), "theta", p["theta"], "window", p["h0"], p["h1"], "trend", p["trend"], "gate", p.get("gate"))
for name, inst in MARKETS.items():
    cs = client.get_candles_range(inst, now - timedelta(days=34), now + timedelta(minutes=1), "M5", price="MBA")
    d = {"t": np.array([int(c.start.timestamp()) for c in cs]), "o": np.array([c.open for c in cs]), "h": np.array([c.high for c in cs]),
         "l": np.array([c.low for c in cs]), "c": np.array([c.close for c in cs]), "s": np.array([c.spread for c in cs])}
    f = search.build_features(d)
    score = (f["F"] @ w / np.abs(w).sum() * 2)
    sel = d["t"] >= day0
    idx = np.where(sel)[0]
    last = len(cs) - 1
    print(f"== {name}: total bars {len(cs)}, today bars {len(idx)}, last bar start {cs[last].start:%Y-%m-%dT%H:%M}Z, last close {d['c'][last]}")
    if not len(idx):
        continue
    hr = f["hour"][idx]
    c_win = (hr >= p["h0"]) & (hr < p["h1"])
    c_val = f["valid"][idx]
    c_gate = f["gates"][p.get("gate", "none")][idx]
    c_thr = np.abs(score[idx]) >= p["theta"]
    side = np.where(score[idx] > 0, 1, -1)
    c_trend = side == f["trend"][idx].astype(int)
    print(f"   in window {int(c_win.sum())} | valid {int(c_val.sum())} | gate {int(c_gate.sum())} | |score|>=theta {int(c_thr.sum())} | with-trend {int(c_trend.sum())}")
    print(f"   window&valid&gate {int((c_win & c_val & c_gate).sum())} | + threshold {int((c_win & c_val & c_gate & c_thr).sum())} | + trend (= signals) {int((c_win & c_val & c_gate & c_thr & c_trend).sum())}")
    print(f"   score today: min {score[idx].min():.2f} max {score[idx].max():.2f} | 20d trend sign now {int(f['trend'][last])}")
    for k in idx[-3:]:
        print(f"   bar {cs[k].start:%H:%M} score {score[k]:.2f} gate {bool(f['gates'][p.get('gate', 'none')][k])} trend {int(f['trend'][k])} hr {int(f['hour'][k])}")
