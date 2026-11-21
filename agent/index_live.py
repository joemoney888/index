"""Live paper runner for the US-index rule that passed the exam (search/NAS100/finalists.json) on the SECOND practice account.
Pure decision functions (tested against agent/search.py so live and backtest cannot drift apart) plus the runner in index_run.py.
Per 5-minute run, per market: manage open trades (trailing stop, time exit), then look at the LAST COMPLETED bar and open a trade if the rule fires."""
import numpy as np

from . import search

MARKETS = {"NAS100": "NAS100_USD", "SPX500": "SPX500_USD", "US30": "US30_USD"}
RISK_GBP = 5.0
MAX_OPEN_TOTAL = 3


def signal_at(p: dict, f: dict, i: int):
    """+1 / -1 / 0 for the bar i that has just closed. Same conditions as search.trades (the entry is then the NEXT bar's open, i.e. now)."""
    w = np.array(p["w"])
    score = float(f["F"][i] @ w / np.abs(w).sum() * 2)
    hr = int(f["hour"][i])
    ok = abs(score) >= p["theta"] and p["h0"] <= hr < p["h1"] and bool(f["valid"][i]) and bool(f["gates"][p.get("gate", "none")][i])
    side = 1 if score > 0 else -1
    if ok and p["trend"] and side != int(np.sign(f["trend"][i])):
        ok = False
    if ok and p.get("htf") and side != int(np.sign(f["htf"][i])):
        ok = False
    return side if ok else 0


def plan(p: dict, side: int, entry: float, atr: float):
    """Stop and target prices (ATR = mean 5-minute true range over 24h at the signal bar)."""
    risk = p["ks"] * atr
    return {"risk": risk, "stop": entry - side * risk, "target": entry + side * p["kt"] * atr}


def trail_stop(p: dict, side: int, entry: float, stop0: float, current_stop: float, atr: float, best: float) -> float:
    """New stop after the bars completed so far. `best` = highest high (long) / lowest low (short) since entry. Never moves backwards."""
    if side > 0:
        new = max(stop0, best - p["td"] * atr) if (p.get("td") and best - entry >= p["ts"] * atr) else stop0
        return max(current_stop, new)
    new = min(stop0, best + p["td"] * atr) if (p.get("td") and entry - best >= p["ts"] * atr) else stop0
    return min(current_stop, new)


BASE_EQUITY_GBP = 500.0
RISK_FRACTION = 0.01


def compound_risk_gbp(closed_pl, base=BASE_EQUITY_GBP, frac=RISK_FRACTION, floor=0.0):
    """Risk per trade when sizing at 1% of VIRTUAL equity = base + the closed P&L (realized + financing, GBP) of this agent's own trades since the switch-on date.
    Off by default (INDEX_COMPOUND != 'true' -> the old fixed RISK_GBP). Equity is floored at `floor`; the result never goes below 0."""
    return round(max(base + sum(closed_pl), floor) * frac, 4)


def units_for(risk_distance_usd: float, gbpusd: float, risk_gbp: float = None) -> float:
    """Units so that the stop distance risks risk_gbp (default RISK_GBP), rounded DOWN to 0.01 (the minimum size)."""
    raw = (RISK_GBP if risk_gbp is None else risk_gbp) * gbpusd / risk_distance_usd
    return max(int(raw * 100) / 100.0, 0.0)
