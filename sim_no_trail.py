"""Read-only, descriptive counterfactual: the same live entries, original stop and target, trailing stop OFF. Places no orders, writes no files, prints totals only.
Approximation: bar highs/lows are mid prices widened by half that bar's closing spread; if the stop and the target are both touched inside one bar the STOP is assumed first (conservative)."""
import csv
import json
import os
from collections import defaultdict
from datetime import datetime, timedelta, timezone

from agent import oanda
from agent.index_live import MARKETS

H_BARS = 192
client = oanda.OandaPractice(os.environ["OANDA_API_TOKEN_INDEX"], os.environ["OANDA_ACCOUNT_ID_INDEX"])
orders, closed = [], {}
for r in csv.DictReader(open("logs/index_events.csv")):
    d = json.loads(r["details"])
    if r["event"] == "order_placed":
        orders.append((r["timestamp_utc"], r["market"], d))
    elif r["event"] == "trade_closed":
        closed[str(d["trade"])] = d
now = datetime.now(timezone.utc)
t0 = datetime.strptime(orders[0][0], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc) - timedelta(hours=1)
gbpusd = client.get_pricing("GBP_USD").mid
bars = {}
for name, inst in MARKETS.items():
    bars[name] = client.get_candles_range(inst, t0, now + timedelta(minutes=1), "M5", price="MBA")
tot = defaultdict(float)
n = defaultdict(int)
actual_total = sim_total = 0.0
rows = []
for ts, mk, d in orders:
    tid = str(d.get("trade_id"))
    if tid not in closed:
        continue
    t = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    start = int(t.timestamp()) // 300 * 300 + 300
    side, entry, stop, target, units = d["side"], d["entry"], d["stop"], d["target"], abs(d["units"])
    out, exit_px, k = "open", None, 0
    for c in bars[mk]:
        if int(c.start.timestamp()) < start:
            continue
        k += 1
        half = c.spread / 2
        hi, lo = c.high + half, c.low - half      # worst case for the trade on the stop side, best on the target side
        stop_hit = (hi >= stop) if side < 0 else (c.low - half <= stop)
        tgt_hit = (lo <= target) if side < 0 else (c.high + half >= target)
        if stop_hit:
            out, exit_px = "stop", stop
            break
        if tgt_hit:
            out, exit_px = "target", target
            break
        if k >= H_BARS:
            out, exit_px = "time", c.close
            break
        last = c.close
    if exit_px is None:
        exit_px = last
    pts = (entry - exit_px) if side < 0 else (exit_px - entry)
    pl = pts * units / gbpusd
    act = float(closed[tid]["realized_pl"])
    day = ts[:10]
    n[out] += 1
    tot[day] += pl
    tot["_actual_" + day] += act
    actual_total += act
    sim_total += pl
tn = sum(n.values())
print("trades compared", tn, "| outcome without trailing stop:", {k: f"{v} ({v / tn:.0%})" for k, v in n.items()})
print("actual total GBP %.2f | no-trailing total GBP %.2f" % (actual_total, sim_total))
for day in sorted(k for k in tot if not k.startswith("_")):
    print(day, "actual %.2f | no-trailing %.2f" % (tot["_actual_" + day], tot[day]))
