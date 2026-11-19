"""Blue Falcon Green: draw the day's trades on 5-minute charts (PNG per market) and write a TradingView Pine Script that marks the same trades.
Env: DAY (YYYY-MM-DD UTC, default today), OANDA_API_TOKEN_INDEX, OANDA_ACCOUNT_ID_INDEX. Reads only; places NO orders. Output: charts/DAY/*.png and charts/DAY/blue_falcon_green.pine"""
import csv
import json
import os
from datetime import datetime, timedelta, timezone

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from agent import oanda  # noqa: E402

MARKETS = ["NAS100", "SPX500", "US30"]


def ts(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def load_events(day):
    trades, moves = {}, {}
    with open("logs/index_events.csv") as f:
        for r in csv.DictReader(f):
            if not r["timestamp_utc"].startswith(day):
                continue
            d = json.loads(r["details"])
            if r["event"] == "order_placed":
                trades[d["trade_id"]] = {"market": r["market"], "t": ts(r["timestamp_utc"]), **d}
            elif r["event"] == "move_stop":
                moves.setdefault(d["trade"], []).append((ts(r["timestamp_utc"]), d["to"]))
    return trades, moves


def draw(market, candles, trades, moves, closed, path, day):
    fig, ax = plt.subplots(figsize=(13, 6.5))
    for c in candles:
        x = c.start
        col = "#2a9d8f" if c.close >= c.open else "#e76f51"
        ax.plot([x, x], [c.low, c.high], color=col, lw=0.8)
        ax.plot([x, x], [c.open, c.close], color=col, lw=3)
    for tid, t in trades.items():
        if t["market"] != market:
            continue
        side = "SHORT" if t["side"] < 0 else "LONG"
        end = closed[tid].close_time if tid in closed and closed[tid].close_time else candles[-1].start
        ax.plot(t["t"], t["price"], marker="v" if t["side"] < 0 else "^", color="black", ms=11, zorder=5)
        ax.hlines(t["target"], t["t"], end, colors="#2a9d8f", linestyles="--", lw=1.2)
        xs, ys = [t["t"]], [t["stop"]]
        for mt, to in moves.get(tid, []):
            xs += [mt, mt]
            ys += [ys[-1], to]
        xs.append(end)
        ys.append(ys[-1])
        ax.plot(xs, ys, color="#e63946", lw=1.4, ls="--", drawstyle="default")
        ax.annotate(f"{side} entry {t['price']:.1f}", (t["t"], t["price"]), textcoords="offset points", xytext=(6, 14), fontsize=9, fontweight="bold")
        if tid in closed and closed[tid].close_time:
            ct = closed[tid].close_time
            near = min(candles, key=lambda c: abs((c.start - ct).total_seconds()))
            pl = closed[tid].realized_pl
            ax.plot(ct, near.close, marker="o", color="#1d3557", ms=9, zorder=5)
            ax.annotate(f"closed {pl:+.2f} GBP", (ct, near.close), textcoords="offset points", xytext=(6, -16), fontsize=9, color="#1d3557", fontweight="bold")
    mine = [t for t in trades.values() if t["market"] == market]
    if mine:
        t_lo = min(t["t"] for t in mine) - timedelta(minutes=40)
        t_hi = max((closed[k].close_time for k, t in trades.items() if t["market"] == market and k in closed and closed[k].close_time), default=candles[-1].start) + timedelta(minutes=50)
        vis = [c for c in candles if t_lo <= c.start <= t_hi]
        if vis:
            ax.set_xlim(t_lo, t_hi)
            lo, hi = min(c.low for c in vis), max(c.high for c in vis)
            lv = [v for t in mine for v in (t["stop"], t["target"])]
            lo, hi = min([lo] + lv), max([hi] + lv)
            pad = (hi - lo) * 0.06
            ax.set_ylim(lo - pad, hi + pad)
    ax.set_title(f"Blue Falcon Green - {market} - {day} (UTC)", fontsize=12)
    fig.text(0.01, 0.01, "Black triangle = entry | red dashed = stop (steps when moved) | green dashed = target | blue dot = close", fontsize=9)
    ax.grid(alpha=0.25)
    fig.autofmt_xdate()
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(path, dpi=130)
    plt.close(fig)


def pine(trades, moves, closed, day):
    L = ['//@version=5', f'indicator("Blue Falcon Green trades {day}", overlay=true, max_labels_count=200, max_lines_count=200)',
         '// Paste into the Pine Editor on a NAS100 / SPX500 / US30 chart (any OANDA-style symbol), press Add to chart. Times are UTC.',
         'f(ms) => ms', 'if barstate.islast']
    for tid, t in trades.items():
        mk = t["market"]
        t0 = int(t["t"].timestamp() * 1000)
        end = int((closed[tid].close_time if tid in closed and closed[tid].close_time else t["t"] + timedelta(hours=1)).timestamp() * 1000)
        lab = f'"{"SHORT" if t["side"] < 0 else "LONG"} {t["price"]}"'
        L += [f'    if str.contains(syminfo.ticker, "{mk}")',
              f'        label.new({t0}, {t["price"]}, {lab}, xloc=xloc.bar_time, style={"label.style_label_down" if t["side"] < 0 else "label.style_label_up"}, color=color.black, textcolor=color.white)',
              f'        line.new({t0}, {t["target"]}, {end}, {t["target"]}, xloc=xloc.bar_time, color=color.green, style=line.style_dashed)']
        stop, tm = t["stop"], t0
        for mt, to in moves.get(tid, []):
            m = int(mt.timestamp() * 1000)
            L.append(f'        line.new({tm}, {stop}, {m}, {stop}, xloc=xloc.bar_time, color=color.red, style=line.style_dashed)')
            stop, tm = to, m
        L.append(f'        line.new({tm}, {stop}, {end}, {stop}, xloc=xloc.bar_time, color=color.red, style=line.style_dashed)')
        if tid in closed and closed[tid].close_time:
            L.append(f'        label.new({end}, {t["price"]}, "closed {closed[tid].realized_pl:+.2f} GBP", xloc=xloc.bar_time, style=label.style_label_left, color=color.blue, textcolor=color.white)')
    return "\n".join(L) + "\n"


def main():
    day = os.environ.get("DAY") or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    trades, moves = load_events(day)
    client = oanda.OandaPractice(os.environ["OANDA_API_TOKEN_INDEX"], os.environ["OANDA_ACCOUNT_ID_INDEX"])
    closed = {t.id: t for t in client.closed_trades(200)}
    d0 = datetime.strptime(day, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    out = f"charts/{day}"
    os.makedirs(out, exist_ok=True)
    for m in MARKETS:
        if not any(t["market"] == m for t in trades.values()):
            continue
        cs = client.get_candles_range(f"{m}_USD", d0 + timedelta(hours=12), d0 + timedelta(hours=22), "M5")
        draw(m, cs, trades, moves, closed, f"{out}/{m}.png", day)
    open(f"{out}/blue_falcon_green.pine", "w").write(pine(trades, moves, closed, day))
    print("trades", len(trades), "charts in", out)


if __name__ == "__main__":
    main()
