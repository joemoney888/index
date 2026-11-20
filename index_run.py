"""5-minute runner for the US-index rule on the SECOND practice account. Env: OANDA_API_TOKEN_INDEX, OANDA_ACCOUNT_ID_INDEX, INDEX_TRADING ('true' to place orders; anything else = log only).
Only this second account is ever touched. Appends to logs/index_events.csv."""
import csv
import json
import os
from datetime import datetime, timedelta, timezone

import numpy as np

from agent import oanda, search
from agent.index_live import MARKETS, MAX_OPEN_TOTAL, plan, signal_at, trail_stop, units_for

LOG = "logs/index_events.csv"
DEC = 1
BAR = timedelta(minutes=5)


def log(market, event, details):
    new = not os.path.exists(LOG)
    os.makedirs("logs", exist_ok=True)
    with open(LOG, "a", newline="") as fh:
        w = csv.writer(fh)
        if new:
            w.writerow(["timestamp_utc", "market", "event", "details"])
        w.writerow([datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), market, event, json.dumps(details, default=str)])
    print(market, event, details, flush=True)


def seen(key):
    if not os.path.exists(LOG):
        return False
    return key in open(LOG).read()


def log_closed_trades(client, count=50):
    """Record the REAL exit of every trade this agent opened (fill price, reason, bid/ask at the fill, P&L, financing) once, as a 'trade_closed' event, so live exits can be compared with the backtest.
    Read only; it never raises (a failure here must not stop trading)."""
    try:
        text = open(LOG).read() if os.path.exists(LOG) else ""
        for t in client.closed_trades_raw(count):
            tid = str(t.get("id"))
            if f'"trade_id": "{tid}"' not in text or f"closed|{tid}" in text:
                continue
            reason = fill = None
            ids = t.get("closingTransactionIDs") or []
            if ids:
                tx = client.transaction(str(ids[-1]))
                fill = {"reason": tx.get("reason"), "fill_price": tx.get("price")}
                fp = tx.get("fullPrice") or {}
                if fp.get("bids") and fp.get("asks"):
                    fill["bid"], fill["ask"] = fp["bids"][0].get("price"), fp["asks"][0].get("price")
            log(t.get("instrument", "?"), "trade_closed", {"key": f"closed|{tid}", "trade": tid, "open_price": t.get("price"), "close_price": t.get("averageClosePrice"),
                "units": t.get("initialUnits"), "open_time": t.get("openTime"), "close_time": t.get("closeTime"), "realized_pl": t.get("realizedPL"), "financing": t.get("financing"), **(fill or {})})
    except Exception as e:      # logging only
        print("log_closed_trades failed:", repr(e)[:200], flush=True)


def main():
    live = os.environ.get("INDEX_TRADING", "").lower() == "true"
    client = oanda.OandaPractice(os.environ["OANDA_API_TOKEN_INDEX"], os.environ["OANDA_ACCOUNT_ID_INDEX"])
    p = json.load(open("search/NAS100/finalists.json"))[0]["p"]
    now = datetime.now(timezone.utc)
    open_trades = client.open_trades()
    log_closed_trades(client)
    gbpusd = None
    for name, inst in MARKETS.items():
        cs = client.get_candles_range(inst, now - timedelta(days=34), now + timedelta(minutes=1), "M5", price="MBA")
        if len(cs) < 6200:
            log(name, "skip", {"reason": "not enough bars", "n": len(cs)})
            continue
        d = {"t": np.array([int(c.start.timestamp()) for c in cs]), "o": np.array([c.open for c in cs]), "h": np.array([c.high for c in cs]),
             "l": np.array([c.low for c in cs]), "c": np.array([c.close for c in cs]), "s": np.array([c.spread for c in cs])}
        f = search.build_features(d)
        i = len(cs) - 1
        bar_end = cs[i].start + BAR
        mine = [t for t in open_trades if t.instrument == inst]
        # 1. manage the open trade: time exit, trailing stop
        for t in mine:
            side = 1 if t.units > 0 else -1
            age_bars = int((now - t.open_time).total_seconds() // 300)
            if age_bars >= p["H"]:
                log(name, "time_exit", {"trade": t.id, "age_bars": age_bars})
                if live:
                    client.close_trade(t.id)
                continue
            since = [c for c in cs if c.start >= t.open_time.replace(second=0, microsecond=0) + BAR]
            sig_i = max(0, int(np.searchsorted(d["t"], int(t.open_time.timestamp()))) - 1)
            atr = float(f["atr"][sig_i])
            if since and t.stop_loss is not None and atr > 0:
                stop0 = t.price - side * p["ks"] * atr
                best = max(c.high for c in since) if side > 0 else min(c.low for c in since)
                new = trail_stop(p, side, t.price, stop0, t.stop_loss, atr, best)
                if abs(new - t.stop_loss) >= 10 ** -DEC:
                    log(name, "move_stop", {"trade": t.id, "from": t.stop_loss, "to": round(new, DEC)})
                    if live:
                        client.move_stop(t.id, new, DEC)
        # 2. look for a new entry on the bar that just closed
        if mine:
            continue
        if now - bar_end > timedelta(minutes=7) or bar_end > now + timedelta(seconds=30):
            continue          # stale bar (market closed or a late run): never trade on old information
        side = signal_at(p, f, i)
        if not side:
            continue
        key = f"{name}|{cs[i].start:%Y-%m-%dT%H:%M}"
        if seen(key):
            continue
        if len(open_trades) >= MAX_OPEN_TOTAL:
            log(name, "skip", {"key": key, "reason": "3 trades already open"})
            continue
        q = client.get_pricing(inst)
        entry = q.ask if side > 0 else q.bid
        pl = plan(p, side, entry, float(f["atr"][i]))
        if gbpusd is None:
            gbpusd = client.get_pricing("GBP_USD").mid
        units = units_for(pl["risk"], gbpusd)
        if units < 0.01:
            log(name, "skip", {"key": key, "reason": "size below 0.01", "risk": pl["risk"]})
            continue
        info = {"key": key, "side": side, "entry": entry, "stop": round(pl["stop"], DEC), "target": round(pl["target"], DEC), "units": units * side, "atr": float(f["atr"][i])}
        if live:
            res = client.place_order(inst, units * side, pl["stop"], pl["target"], DEC, 2)
            log(name, "order_placed" if res.get("filled") else "order_rejected", {**info, **res})
            if res.get("filled"):
                open_trades = open_trades + [oanda.Trade(res["trade_id"], inst, now, None, units * side, res["price"], 0.0, round(pl["stop"], DEC))]
        else:
            log(name, "would_place", info)


if __name__ == "__main__":
    main()
