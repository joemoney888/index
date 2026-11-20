"""Index spread trade (statistical arbitrage): trade the gap between two related indices, e.g. long NAS100 / short beta x SPX500, when the log-price gap is stretched against its own recent average, exit when it reverts, hits a stop or times out.
Costs: both legs' spreads in and out. All inputs at bar t use data up to t; entry is the next bar's open. Risk unit = ks x the spread's rolling standard deviation. Reads files only; places NO orders."""
import numpy as np
import pandas as pd


def align(a, b):
    """a, b: dicts of arrays (t,o,h,l,c,s). Returns merged dict on common timestamps."""
    A = pd.DataFrame({"t": a["t"], "oa": a["o"], "ca": a["c"], "sa": a["s"]}).drop_duplicates("t")
    B = pd.DataFrame({"t": b["t"], "ob": b["o"], "cb": b["c"], "sb": b["s"]}).drop_duplicates("t")
    m = A.merge(B, on="t").sort_values("t")
    return {k: m[k].to_numpy() for k in m.columns}


def prep(m, L):
    la, lb = np.log(m["ca"]), np.log(m["cb"])
    sa, sb = pd.Series(la), pd.Series(lb)
    beta = (sa.rolling(L).cov(sb) / sb.rolling(L).var()).shift(0).to_numpy()
    spr = la - beta * lb
    s = pd.Series(spr)
    mu, sd = s.rolling(L).mean().to_numpy(), s.rolling(L).std().to_numpy()
    return {"beta": beta, "mu": mu, "sd": sd, "z": (spr - mu) / sd}


def simulate(m, pp, p, lo, hi):
    """Returns array of (entry_time, R)."""
    z, beta, mu, sd = pp["z"], pp["beta"], pp["mu"], pp["sd"]
    hour = (m["t"] // 3600) % 24
    ok = (np.abs(z) >= p["z0"]) & (hour >= p["h0"]) & (hour < p["h1"]) & np.isfinite(z) & (sd > 0)
    cand = np.flatnonzero(ok)
    cand = cand[(cand >= lo) & (cand + p["H"] + 3 < hi)]
    la, lb = np.log(m["ca"]), np.log(m["cb"])
    H, ks = p["H"], p["ks"]
    out, free, k = [], -1, 0
    while k < len(cand):
        t = cand[k]
        if t < free:
            k = int(np.searchsorted(cand, free))
            continue
        side = -1 if z[t] > 0 else 1                      # stretched up -> short the spread
        b = beta[t]
        risk = ks * sd[t]
        e = np.log(m["oa"][t + 1]) - b * np.log(m["ob"][t + 1])
        cost = (m["sa"][t] / m["oa"][t + 1] + abs(b) * m["sb"][t] / m["ob"][t + 1])        # both legs, in and out (half-spread each way x2)
        sf = la[t + 1:t + 1 + H] - b * lb[t + 1:t + 1 + H]
        pnl = side * (sf - e)
        tgt = side * (mu[t] + (-side) * p["ez"] * sd[t] - e)          # revert to mean (ez sd short of it)
        hs = pnl <= -risk
        ht = pnl >= max(tgt, 0.0) if tgt > 0 else np.zeros(len(pnl), bool)
        js = int(np.argmax(hs)) if hs.any() else H
        jt = int(np.argmax(ht)) if ht.any() else H
        if js <= jt and js < H:
            r, n = -risk, js
        elif jt < js:
            r, n = pnl[jt], jt
        else:
            r, n = pnl[H - 1], H - 1
        out.append((m["t"][t], (r - cost) / risk))
        free = t + 1 + n + 1
        k = int(np.searchsorted(cand, free))
    return np.array(out) if out else np.empty((0, 2))
