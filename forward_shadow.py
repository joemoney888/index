"""Forward test of the NAS100 rule that passed the one-time exam (search/NAS100/finalists.json). Replays the exact backtest logic on fresh bars after FORWARD_START and writes
forward/NAS100_shadow.csv (one row per hypothetical trade: entry time, R) and forward/NAS100_SUMMARY.md. Paper only: no orders. Deterministic, so it can be re-run any day."""
import csv
import json
import os
from datetime import datetime, timedelta, timezone

import numpy as np

from agent import oanda, search

FORWARD_START = datetime(2026, 11, 19, tzinfo=timezone.utc)   # fixed on the day the exam was passed; nothing before it counts
WARMUP_DAYS = 45


MARKETS = ["NAS100", "SPX500", "US30"]


def fetch_chunked(client, instrument, start, end, step_days=15):
    """5-minute candles with real spreads, in 15-day chunks, retrying each chunk."""
    import time
    out, seen, cur = [], set(), start
    while cur < end:
        nxt = min(cur + timedelta(days=step_days), end)
        for attempt in range(6):
            try:
                chunk = client.get_candles_range(instrument, cur, nxt, "M5", price="MBA")
                break
            except Exception:  # noqa: BLE001
                if attempt == 5:
                    raise
                time.sleep(10 * (attempt + 1))
        for c in chunk:
            if c.start not in seen:
                seen.add(c.start)
                out.append(c)
        cur = nxt
    return sorted(out, key=lambda c: c.start)


def run_market(name, p, client, tag="shadow"):
    inst = f"{name}_USD"
    end = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
    cs = [c for c in fetch_chunked(client, inst, FORWARD_START - timedelta(days=WARMUP_DAYS), end) if c.complete]
    d = {"t": np.array([int(c.start.timestamp()) for c in cs]), "o": np.array([c.open for c in cs]), "h": np.array([c.high for c in cs]),
         "l": np.array([c.low for c in cs]), "c": np.array([c.close for c in cs]), "s": np.array([c.spread for c in cs])}
    f = search.build_features(d)
    lo = int(np.searchsorted(d["t"], int(FORWARD_START.timestamp())))
    tr = search.trades(p, d, f, lo, len(d["t"]))
    os.makedirs("forward", exist_ok=True)
    with open(f"forward/{name}_{tag}.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["entry_utc", "R"])
        for t, r in tr:
            w.writerow([datetime.fromtimestamp(int(t), timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), round(float(r), 4)])
    s = search.day_t(tr) if len(tr) else {"n": 0, "mean": 0.0, "t": 0.0}
    return tr, s, end


def main():
    p = json.load(open("search/NAS100/finalists.json"))[0]["p"]   # one rule, never refitted; NAS100 passed the exam, SPX500 and US30 are unfitted replications
    client = oanda.OandaPractice(os.environ["OANDA_API_TOKEN_INDEX"], os.environ["OANDA_ACCOUNT_ID_INDEX"])
    L = ["# US index forward shadow (the NAS100 rule, unchanged, on NAS100, SPX500 and US30)", "",
         f"Forward period starts {FORWARD_START:%Y-%m-%d}. Paper replay of the exact tested rule; no orders. Backtest expectation per trade: NAS100 +0.03 to +0.07R, SPX500 and US30 about +0.015R.", "",
         "| Market | Trades | Avg R | Cumulative R | Win rate | t-stat |", "|---|---|---|---|---|---|"]
    alltr, end = [], None
    for name in MARKETS:
        tr, s, end = run_market(name, p, client)
        alltr.append(tr)
        cum = float(tr[:, 1].sum()) if len(tr) else 0.0
        wins = float((tr[:, 1] > 0).mean()) if len(tr) else 0.0
        L.append(f"| {name} | {s['n']} | {s['mean']:+.3f} | {cum:+.1f} | {wins:.0%} | {s['t']:.2f} |")
    pool = np.vstack([t for t in alltr if len(t)]) if any(len(t) for t in alltr) else np.empty((0, 2))
    ps = search.day_t(pool) if len(pool) else {"n": 0, "mean": 0.0, "t": 0.0}
    L += ["", f"Pooled: {ps['n']} trades, {ps['mean']:+.3f}R average, t {ps['t']:.2f}. Data to {end:%Y-%m-%d %H:%M} UTC.",
          "- Verdict: TOO EARLY until about 300 trades per market (about 2 months); then it counts only if the average stays positive with t >= 2.", ""]
    # registered 19 Nov 2026: second forward variant, target effectively removed (kt 20, trailing stop unchanged). Exploratory (train+validation only, 48 exit variants tried); paper only.
    p2 = dict(p, kt=20.0)
    L += ["", "## Variant: no fixed target (let winners run; kt 20, same trailing stop). Exploratory, started 2026-11-19.", "", "| Market | Trades | Avg R | Cumulative R | Win rate | t-stat |", "|---|---|---|---|---|---|"]
    alt = []
    for name in MARKETS:
        tr, s, _ = run_market(name, p2, client, "open_shadow")
        alt.append(tr)
        cum = float(tr[:, 1].sum()) if len(tr) else 0.0
        wins = float((tr[:, 1] > 0).mean()) if len(tr) else 0.0
        L.append(f"| {name} | {s['n']} | {s['mean']:+.3f} | {cum:+.1f} | {wins:.0%} | {s['t']:.2f} |")
    open("forward/NAS100_SUMMARY.md", "w").write("\n".join(L))
    print("\n".join(L))


if __name__ == "__main__":
    main()
