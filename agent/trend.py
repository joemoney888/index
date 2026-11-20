"""Slow trend-following family (daily bars made from the 5-minute data). Separate from the mean-reversion engine in search.py.
A variant: signal type ('brk' = N-day high breakout, 'ma' = close above N-day average), N, long-only or long+short, and a trailing stop of k*ATR(20) under the best close since entry (0 = signal exit only).
Decisions are made at the daily close and held to the next close. Costs: half-spread on every position change; overnight financing 6.5%/yr on longs and 3%/yr on shorts (estimates, not OANDA's current rate card).
Score = TIMING ALPHA vs buy-and-hold: weekly net strategy return minus (average exposure x index return), t-stat over weeks, equal-weighted across markets. Reads files only; places NO orders."""
import math

import numpy as np
import pandas as pd

LONG_FIN, SHORT_FIN = 0.065, 0.03


def daily(path):
    d = pd.read_csv(path)
    d["day"] = pd.to_datetime(d["t"], unit="s", utc=True).dt.floor("D")
    g = d.groupby("day")
    x = pd.DataFrame({"o": g["o"].first(), "h": g["h"].max(), "l": g["l"].min(), "c": g["c"].last(), "s": g["spread"].mean(), "n": g.size()})
    return x[x["n"] >= 100]


def sample(rng):
    return {"type": str(rng.choice(["brk", "ma"])), "N": int(rng.choice([20, 40, 60, 100, 150, 200])), "short": int(rng.choice([0, 1])), "k": float(rng.choice([0, 2, 3, 4, 6]))}


def positions(p, x):
    c, h, l = x["c"].to_numpy(), x["h"].to_numpy(), x["l"].to_numpy()
    n = len(c)
    N = p["N"]
    tr = np.maximum(h[1:] - l[1:], np.maximum(abs(h[1:] - c[:-1]), abs(l[1:] - c[:-1])))
    atr = np.concatenate([[np.nan], pd.Series(tr).rolling(20).mean().to_numpy()])
    sma = pd.Series(c).rolling(N).mean().to_numpy()
    hi = pd.Series(c).rolling(N).max().shift(1).to_numpy()
    lo = pd.Series(c).rolling(N).min().shift(1).to_numpy()
    pos = np.zeros(n)
    cur, best = 0, 0.0
    for t in range(N + 1, n - 1):
        if p["type"] == "brk":
            up, dn = c[t] > hi[t], c[t] < lo[t]
        else:
            up, dn = c[t] > sma[t], c[t] < sma[t]
        if cur == 1:
            best = max(best, c[t])
            if (p["k"] and c[t] < best - p["k"] * atr[t]) or dn:
                cur = -1 if (p["short"] and dn) else 0
                best = c[t]
        elif cur == -1:
            best = min(best, c[t])
            if (p["k"] and c[t] > best + p["k"] * atr[t]) or up:
                cur = 1 if up else 0
                best = c[t]
        else:
            if up:
                cur, best = 1, c[t]
            elif dn and p["short"]:
                cur, best = -1, c[t]
        pos[t + 1] = cur            # decided at close t, held through day t+1
    return pos


def net_returns(p, x):
    """Per-day net strategy return and buy-and-hold return (close to close)."""
    c = x["c"].to_numpy()
    ret = np.concatenate([[0.0], c[1:] / c[:-1] - 1])
    pos = positions(p, x)
    gap = np.concatenate([[1.0], np.diff(x.index.tz_localize(None).to_numpy().astype("datetime64[D]").astype(int)).astype(float)])
    fin = np.where(pos > 0, LONG_FIN, np.where(pos < 0, SHORT_FIN, 0.0)) * gap / 365
    chg = np.abs(np.diff(np.concatenate([[0.0], pos])))
    cost = chg * (x["s"].to_numpy() / 2) / c
    return pos * ret - fin - cost, ret - LONG_FIN * gap / 365, pos   # benchmark = holding the index, paying the same long financing


def alpha_series(p, mk, a, b):
    """Weekly equal-weighted timing alpha over day-index window given as timestamps [a, b). Returns (weekly array, details)."""
    ws, det = [], []
    for name, x in mk.items():
        s, r, pos = net_returns(p, x)
        m = (x.index >= a) & (x.index < b)
        if m.sum() < 50:
            continue
        pbar = pos[m].mean()
        a_d = pd.Series((s - pbar * r)[m], index=x.index[m])
        ws.append(a_d.resample("W").sum())
        det.append((name, float(s[m].sum()), float(r[m].sum()), float(pbar)))
    if not ws:
        return np.array([]), det
    w = pd.concat(ws, axis=1).fillna(0).mean(axis=1).to_numpy()
    return w, det


def tstat(w):
    return float(w.mean() / (w.std(ddof=1) / math.sqrt(len(w)))) if len(w) > 20 and w.std() > 0 else 0.0
