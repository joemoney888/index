"""Forward CONTEXT log (paper only, no orders, no test, no N). Writes forward/daily_context.csv and forward/daily_context_SUMMARY.md.
One row per instrument per New York trading day from START: prior close, 09:30 open, 10:30 price, 15:55 close, gap %, first-hour %, day %, (turn-of-month blocks for the D1 near miss are derived later from these dates and day returns) and a log-only 'big-day' flag (|gap| >= 1.0% or |first hour| >= 0.75%). Thresholds fixed now and NOT tuned; the flag is a description for later review against BFG results (Idea 17), never a trading input.
Idempotent: a day already in the CSV is never rewritten. Missing bars are recorded as SKIPPED."""
import csv, os
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
NY = ZoneInfo("America/New_York"); CSV = "forward/daily_context.csv"; SUM = "forward/daily_context_SUMMARY.md"
START = "2026-11-23"; INSTR = ("SPX500_USD", "NAS100_USD", "US30_USD")
FIELDS = ["date", "instrument", "prev_close", "open_0930", "px_1030", "close_1555", "gap_pct", "first_hour_pct", "day_pct", "big_day_flag", "status"]
GAP, HOUR = 1.0, 0.75

def at(cs, t):
    for c in cs:
        if c.start == t: return c
    return None

def row_for(client, ins, D, prev_close):
    s = datetime(D.year, D.month, D.day, 9, 25, tzinfo=NY).astimezone(timezone.utc); e = datetime(D.year, D.month, D.day, 16, 5, tzinfo=NY).astimezone(timezone.utc)
    cs = client.get_candles_range(ins, s, e, "M5", price="MBA")
    ut = lambda h, m: datetime(D.year, D.month, D.day, h, m, tzinfo=NY).astimezone(timezone.utc)
    a, b, c = at(cs, ut(9, 30)), at(cs, ut(10, 25)), at(cs, ut(15, 55))
    if a is None or b is None or c is None or prev_close is None: return None
    gap = (a.open / prev_close - 1) * 100; hr = (b.close / a.open - 1) * 100; day = (c.close / a.open - 1) * 100
    return {"open_0930": a.open, "px_1030": b.close, "close_1555": c.close, "gap_pct": round(gap, 3), "first_hour_pct": round(hr, 3), "day_pct": round(day, 3),
            "big_day_flag": int(abs(gap) >= GAP or abs(hr) >= HOUR)}

def main():
    from agent import oanda
    rows = list(csv.DictReader(open(CSV))) if os.path.exists(CSV) else []
    done = {(r["date"], r["instrument"]) for r in rows}
    now = datetime.now(timezone.utc); client = oanda.OandaPractice(os.environ["OANDA_API_TOKEN_INDEX"], os.environ["OANDA_ACCOUNT_ID_INDEX"])
    D = datetime.fromisoformat(START).date()
    while D <= now.astimezone(NY).date():
        if D.weekday() < 5 and now >= datetime(D.year, D.month, D.day, 16, 30, tzinfo=NY).astimezone(timezone.utc):
            for ins in INSTR:
                if (D.isoformat(), ins) in done: continue
                prev = [r for r in rows if r["instrument"] == ins and r["status"] == "OK"]
                prev_close = float(prev[-1]["close_1555"]) if prev else None
                if prev_close is None:   # first day: anchor on the previous weekday's 15:55 close
                    P = D - timedelta(days=3 if D.weekday() == 0 else 1)
                    ps = datetime(P.year, P.month, P.day, 15, 55, tzinfo=NY).astimezone(timezone.utc)
                    pc = at(client.get_candles_range(ins, ps, ps + timedelta(minutes=5), "M5", price="MBA"), ps); prev_close = pc.close if pc else None
                r = row_for(client, ins, D, prev_close)
                base = {"date": D.isoformat(), "instrument": ins, "prev_close": prev_close if prev_close is not None else ""}
                if r is None: rows.append({k: "" for k in FIELDS} | base | {"status": "SKIPPED"})
                else: rows.append({k: "" for k in FIELDS} | base | r | {"status": "OK"})
        D += timedelta(days=1)
    os.makedirs("forward", exist_ok=True)
    with open(CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS); w.writeheader(); w.writerows(rows)
    ok = [r for r in rows if r["status"] == "OK"]
    big = sum(int(r["big_day_flag"]) for r in ok)
    open(SUM, "w").write(f"# Forward context log (paper, no orders, no test)\nRows OK: {len(ok)}, skipped: {len(rows) - len(ok)}, big-day flags: {big}. Log only; review against BFG results (Idea 17) once there are at least 100 flagged days. Not evidence before that.\n")

if __name__ == "__main__": main()
