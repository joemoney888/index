"""Forward shadow test of F1 (pre-FOMC drift). PAPER ONLY, NO ORDERS: reads prices, writes forward/F1_fomc_shadow.csv and forward/F1_fomc_SUMMARY.md.
Rule (frozen, docs/F1B_REGISTRATION.md and docs/FORWARD_F1.md): LONG NAS100 at the open of the 14:00 New York 5-minute bar on the previous weekday, exit at the close of the 13:55 bar on the decision day; each leg pays half of that bar's spread (adverse side). Events: famB/fomc_forward.json from 2026-12-09. Idempotent: an event already in the CSV is never rewritten."""
import csv, json, math, os
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
NY = ZoneInfo("America/New_York"); CSV = "forward/F1_fomc_shadow.csv"; SUM = "forward/F1_fomc_SUMMARY.md"
FIELDS = ["decision_day", "entry_utc", "entry_open", "entry_halfspread", "exit_utc", "exit_close", "exit_halfspread", "net_bp"]

def prev_weekday(d):
    return d - timedelta(days=3 if d.weekday() == 0 else 1)

def net_bp(entry_open, entry_hs, exit_close, exit_hs):
    pe, px = entry_open + entry_hs, exit_close - exit_hs
    return (px - pe) / pe * 1e4

def stats(v):
    n = len(v)
    if n < 2: return n, (v[0] if v else float("nan")), float("nan")
    m = sum(v) / n; sd = math.sqrt(sum((x - m) ** 2 for x in v) / (n - 1))
    return n, m, (m / (sd / math.sqrt(n)) if sd > 0 else float("nan"))

def candle_at(cs, when_utc):
    for c in cs:
        if c.start == when_utc: return c
    return None

def main():
    from agent import oanda
    days = json.load(open("famB/fomc_forward.json"))["decision_days"]
    rows = list(csv.DictReader(open(CSV))) if os.path.exists(CSV) else []
    done = {r["decision_day"] for r in rows}
    now = datetime.now(timezone.utc); client = None
    for ds in days:
        D = datetime.fromisoformat(ds).date()
        close_t = datetime(D.year, D.month, D.day, 14, 0, tzinfo=NY).astimezone(timezone.utc)
        if ds in done or now < close_t + timedelta(hours=1): continue
        P = prev_weekday(D)
        t_in = datetime(P.year, P.month, P.day, 14, 0, tzinfo=NY).astimezone(timezone.utc); t_out = close_t - timedelta(minutes=5)
        client = client or oanda.OandaPractice(os.environ["OANDA_API_TOKEN_INDEX"], os.environ["OANDA_ACCOUNT_ID_INDEX"])
        a = candle_at(client.get_candles_range("NAS100_USD", t_in, t_in + timedelta(minutes=5), "M5", price="MBA"), t_in)
        b = candle_at(client.get_candles_range("NAS100_USD", t_out, t_out + timedelta(minutes=5), "M5", price="MBA"), t_out)
        if a is None or b is None:
            print("missing bar for", ds, "- recorded as skipped"); rows.append({k: "" for k in FIELDS} | {"decision_day": ds, "net_bp": "SKIPPED"}); continue
        rows.append({"decision_day": ds, "entry_utc": t_in.isoformat(), "entry_open": a.open, "entry_halfspread": a.spread / 2, "exit_utc": t_out.isoformat(),
                     "exit_close": b.close, "exit_halfspread": b.spread / 2, "net_bp": round(net_bp(a.open, a.spread / 2, b.close, b.spread / 2), 3)})
    os.makedirs("forward", exist_ok=True)
    with open(CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS); w.writeheader(); w.writerows(rows)
    v = [float(r["net_bp"]) for r in rows if r["net_bp"] not in ("", "SKIPPED")]
    n, m, t = stats(v)
    open(SUM, "w").write(f"# F1 forward shadow (paper, no orders)\nEvents recorded: {n} (skipped: {sum(r['net_bp']=='SKIPPED' for r in rows)}). Net mean {m:+.1f} bp, t {t:+.2f}.\n"
                          f"NOT TESTED until at least 40 events exist (about Dec 2031 at 8 a year). Before that these numbers are a log, not evidence. Rule: docs/FORWARD_F1.md.\n")

if __name__ == "__main__": main()
