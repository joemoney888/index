"""Read-only, descriptive look at the 96 live BFG entries with a different exit: take 30% off at +1R, move the stop to break-even, close the rest at +2R (or at the stop/break-even, or after 192 bars). R = the entry-to-original-stop distance.
Not a registered test: places no orders, writes no files, prints totals only. Same approximations as sim_no_trail.py; if the stop and a target are touched in one bar the adverse side is assumed first; units are not rounded to the 0.01 minimum (a 30% slice of 0.03 units is not placeable)."""
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
    R = abs(stop - entry)
    tp1 = entry - side * R if side < 0 else entry + R
    tp1 = entry + (-R if side < 0 else R)
    tp2 = entry + (-2 * R if side < 0 else 2 * R)
    got1, cur_stop, out, k, last = False, stop, "open", 0, None
    realised = 0.0
    rest = 1.0
    for c in bars[mk]:
        if int(c.start.timestamp()) < start:
            continue
        k += 1
        half = c.spread / 2
        hi, lo = c.high + half, c.low - half
        adverse = (hi >= cur_stop) if side < 0 else (lo <= cur_stop)
        if adverse and not got1:
            realised += rest * (-R); rest = 0; out = "stop"
            break
        if not got1:
            fav = (lo <= tp1) if side < 0 else (hi >= tp1)
            if fav:
                got1 = True; realised += 0.3 * R; rest = 0.7; cur_stop = entry
                adverse = (hi >= cur_stop) if side < 0 else (lo <= cur_stop)
                if adverse:
                    out = "tp1_then_BE"; rest = 0
                    break
        if got1:
            adverse = (hi >= cur_stop) if side < 0 else (lo <= cur_stop)
            if adverse:
                out = "tp1_then_BE"; rest = 0
                break
            fav2 = (lo <= tp2) if side < 0 else (hi >= tp2)
            if fav2:
                realised += rest * 2 * R; rest = 0; out = "tp1_then_2R"
                break
        last = c.close
        if k >= H_BARS:
            mv = (entry - last) if side < 0 else (last - entry)
            realised += rest * mv; rest = 0; out = "time"
            break
    if rest > 0 and last is not None:
        mv = (entry - last) if side < 0 else (last - entry)
        realised += rest * mv
    exit_px = None
    pts = realised
    pl = pts * units / gbpusd
    act = float(closed[tid]["realized_pl"])
    day = ts[:10]
    n[out] += 1
    tot[day] += pl
    tot["_actual_" + day] += act
    actual_total += act
    sim_total += pl
tn = sum(n.values())
print("trades compared", tn, "| outcome with 30% at 1R + break-even + 2R:", {k: f"{v} ({v / tn:.0%})" for k, v in n.items()})
print("actual total GBP %.2f | partial+BE total GBP %.2f" % (actual_total, sim_total))
for day in sorted(k for k in tot if not k.startswith("_")):
    print(day, "actual %.2f | partial+BE %.2f" % (tot["_actual_" + day], tot[day]))
