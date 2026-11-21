"""End-of-day report for both paper agents, in R only (no pound figures).
R = profit or loss as a multiple of the risk taken on that trade (1R = the initial stop distance).
Usage: python report/eod_report.py <old_agent_events.csv> <bfg_events.csv> [out_dir]
Writes eod_report.png (weekly total R, both agents, in one chart; daily R for the last 10 days) and eod_report.md. Read-only."""
import csv, json, sys, os, collections
from datetime import datetime, date, timedelta
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def old_agent(path):
    risk, out = {}, []
    rows = list(csv.DictReader(open(path)))
    for r in rows:
        if r["event"] == "order_placed":
            d = json.loads(r["details"]); risk[d["trade_id"]] = d.get("risk_gbp")
    for r in rows:
        if r["event"] == "trade_closed":
            d = json.loads(r["details"]); k = risk.get(d.get("trade_id"))
            if k:
                out.append((r["timestamp_utc"][:10], float(d["realized_pl"]) / float(k)))
    return out

def bfg(path):
    plan, out = {}, []
    rows = list(csv.DictReader(open(path)))
    for r in rows:
        if r["event"] == "order_placed":
            d = json.loads(r["details"]); plan[str(d["trade_id"])] = (float(d.get("price", d["entry"])), float(d["stop"]))
    for r in rows:
        if r["event"] == "trade_closed":   # written from the first run after 2026-11-23 reconciliation
            d = json.loads(r["details"]); p = plan.get(str(d.get("trade")))
            if p and d.get("close_price") and d.get("units"):
                side = 1 if float(d["units"]) > 0 else -1
                out.append((r["timestamp_utc"][:10], side * (float(d["close_price"]) - p[0]) / abs(p[0] - p[1])))
    return out

def week(d):
    x = date.fromisoformat(d); return (x - timedelta(days=x.weekday())).isoformat()

def main():
    a, b = old_agent(sys.argv[1]), bfg(sys.argv[2]); od = sys.argv[3] if len(sys.argv) > 3 else "."
    weeks = sorted({week(d) for d, _ in a + b})
    tot = {n: collections.defaultdict(float) for n in ("Blue Falcon", "BFG")}
    cnt = {n: collections.defaultdict(int) for n in tot}
    for n, rows in (("Blue Falcon", a), ("BFG", b)):
        for d, r in rows: tot[n][week(d)] += r; cnt[n][week(d)] += 1
    days = sorted({d for d, _ in a + b})[-10:]
    daily = {n: collections.defaultdict(float) for n in tot}
    for n, rows in (("Blue Falcon", a), ("BFG", b)):
        for d, r in rows: daily[n][d] += r
    fig, ax = plt.subplots(2, 1, figsize=(9, 7))
    w = 0.38; xs = range(len(weeks))
    for j, n in enumerate(tot):
        ax[0].bar([x + (j - .5) * w for x in xs], [tot[n][k] for k in weeks], w, label=n)
    ax[0].axhline(0, color="k", lw=.8); ax[0].set_xticks(list(xs)); ax[0].set_xticklabels(["w/c " + k[5:] for k in weeks])
    ax[0].set_title("Weekly total R (positive = profit, negative = loss)"); ax[0].set_ylabel("R"); ax[0].legend()
    xs2 = range(len(days))
    for j, n in enumerate(daily):
        ax[1].bar([x + (j - .5) * w for x in xs2], [daily[n][d] for d in days], w, label=n)
    ax[1].axhline(0, color="k", lw=.8); ax[1].set_xticks(list(xs2)); ax[1].set_xticklabels([d[5:] for d in days], rotation=45)
    ax[1].set_title("Daily total R, last 10 trading days"); ax[1].set_ylabel("R")
    fig.tight_layout(); fig.savefig(os.path.join(od, "eod_report.png"), dpi=130)
    L = ["# End-of-day report (R only)", "", "| Week commencing | Blue Falcon trades | Blue Falcon R | BFG trades | BFG R |", "|---|---|---|---|---|"]
    for k in weeks: L.append(f"| {k} | {cnt['Blue Falcon'][k]} | {tot['Blue Falcon'][k]:+.2f} | {cnt['BFG'][k]} | {tot['BFG'][k]:+.2f} |")
    L.append(f"| **Total** | {len(a)} | {sum(r for _, r in a):+.2f} | {len(b)} | {sum(r for _, r in b):+.2f} |")
    open(os.path.join(od, "eod_report.md"), "w").write("\n".join(L) + "\n"); print("\n".join(L))

if __name__ == "__main__": main()
