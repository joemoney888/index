"""Strategy search engine (variants 183+). Random search over adaptive, multi-timeframe strategies on 5-minute bars with real spreads.
HONESTY RULES (fixed before any run, 18 Nov 2026):
  * Data is split by time. EXAM = the last 365 days: never loaded by the search (the arrays are cut before it), used once at the very end.
    VALIDATION = the 365 days before that. TRAIN = everything older (about 3.5 years).
  * Every sampled variant is counted. N = total variants tried across all runs (ledger in search/runs/*.json).
  * A variant is a CANDIDATE only if TRAIN trades >= 500, TRAIN mean R >= +0.03 and its day-clustered TRAIN t-stat >= sqrt(2 ln N) + 0.5 (what pure luck is expected to produce at N tries, plus a margin).
  * A candidate is a FINALIST only if VALIDATION mean R >= +0.03 and VALIDATION t >= 2.0 with >= 150 trades. Best 3 by validation t go to the exam.
  * EXAM, run once per finalist set: PASS if mean R >= +0.05 and t >= 2.5 (about Bonferroni for 3). A pass still only earns forward paper-trading as a shadow strategy.
Strategy family (engine v2, 19 Nov: the first six features were joined by RSI(14) on 5-minute and 1-hour scales, MACD histogram on both, Bollinger position on both and a 14-bar stochastic and a day-VWAP-like distance; plus compression GATES: squeeze fired (Bollinger inside Keltner then out), Bollinger width in the bottom 20% of 24h, ATR(12 bars)/ATR(24h) above 1 or below 0.7, and an optional 4-hour-momentum agreement; N keeps counting across versions, which is conservative): a score = weighted sum of 1 to 4 causal features (1h, 4h, 1d momentum in volatility units; position in the 24h range; distance from the 24h mean; wick balance; the indicators above),
trade when |score| >= threshold inside a UTC session window (optionally only with the 20-day trend); entry at the next bar's open +/- half the real spread; stop and target are multiples of
the 24h average true range (dynamic: they widen when the market is fast); time exit after H bars; one position at a time."""
import math
from typing import Dict, List, Optional

import numpy as np

BAR = 300
DAY = 288
FEATURES = ["m1h", "m4h", "m1d", "pos24", "dev24", "wick", "rsi5", "rsi1h", "macd5", "macd1h", "boll5", "boll1h", "stoch5", "vwapd", "don1h", "don4h"]  # engine v2 adds the last seven (RSI, MACD, Bollinger, stochastic)
EXAM_DAYS = 365
VAL_DAYS = 365


def load_arrays(path: str) -> Dict[str, np.ndarray]:
    import csv
    import gzip
    with gzip.open(path, "rt") as f:
        rows = list(csv.reader(f))[1:]
    a = np.array(rows, dtype=float)
    return {"t": a[:, 0].astype(np.int64), "o": a[:, 1], "h": a[:, 2], "l": a[:, 3], "c": a[:, 4], "s": a[:, 5]}


def rolling_mean(x: np.ndarray, n: int) -> np.ndarray:
    cs = np.cumsum(np.insert(x, 0, 0.0))
    out = np.full(len(x), np.nan)
    out[n - 1:] = (cs[n:] - cs[:-n]) / n
    return out


def rolling_ext(x: np.ndarray, n: int, fn) -> np.ndarray:
    import pandas as pd
    s = pd.Series(x)
    return (s.rolling(n).max() if fn == "max" else s.rolling(n).min()).to_numpy()


def build_features(d: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
    """All features use only bars up to and including bar i (known at its close)."""
    o, h, l, c = d["o"], d["h"], d["l"], d["c"]
    pc = np.concatenate([[c[0]], c[:-1]])
    tr = np.maximum(h - l, np.maximum(abs(h - pc), abs(l - pc)))
    atr = rolling_mean(tr, DAY)
    lc = np.log(c)

    def mom(n):
        m = np.full(len(c), np.nan)
        m[n:] = (lc[n:] - lc[:-n]) / np.maximum(atr[n:] / c[n:] * math.sqrt(n), 1e-12)
        return m
    hi, lo = rolling_ext(h, DAY, "max"), rolling_ext(l, DAY, "min")
    rngw = np.maximum(hi - lo, 1e-12)
    pos = (c - lo) / rngw * 2 - 1
    dev = (c - rolling_mean(c, DAY)) / np.maximum(atr * math.sqrt(12), 1e-12)
    rng = np.maximum(h - l, 1e-12)
    wick_raw = ((h - np.maximum(o, c)) - (np.minimum(o, c) - l)) / rng   # + = long upper wick (rejection of highs)
    wick = -np.nan_to_num(rolling_mean(wick_raw, 3))                      # + = bullish rejection of lows
    trend = np.sign(c - rolling_mean(c, DAY * 20))
    hour = ((d["t"] % 86400) // 3600).astype(np.int64)
    import pandas as pd
    cs = pd.Series(c)

    def rsi(n):
        dlt = cs.diff()
        up = dlt.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean()
        dn = (-dlt.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean()
        return ((100 - 100 / (1 + up / dn.replace(0, np.nan))).fillna(50).to_numpy() - 50) / 15

    def macd(k):  # MACD(12,26,9) with every period multiplied by k (k=12: the 1-hour chart's MACD built from 5-minute bars), histogram in volatility units
        line = cs.ewm(span=12 * k, adjust=False).mean() - cs.ewm(span=26 * k, adjust=False).mean()
        hist = line - line.ewm(span=9 * k, adjust=False).mean()
        return hist.to_numpy() / np.maximum(atr * math.sqrt(k), 1e-12)

    def boll(n):
        m, sd = cs.rolling(n).mean(), cs.rolling(n).std()
        return ((cs - m) / (2 * sd.replace(0, np.nan))).to_numpy()
    lo14, hi14 = rolling_ext(l, 14, "min"), rolling_ext(h, 14, "max")
    stoch = (c - lo14) / np.maximum(hi14 - lo14, 1e-12) * 2 - 1
    day_id = pd.Series(d["t"] // 86400)
    tp = (cs + pd.Series(h) + pd.Series(l)) / 3
    vwapd = ((tp - tp.groupby(day_id).transform(lambda x: x.expanding().mean())) / np.maximum(atr * math.sqrt(12), 1e-12)).to_numpy()   # equal-weight "VWAP" (no true volume on CFDs)
    def donchian(n):   # +1 / -1 when the close breaks the previous n bars' high / low (a breakout), else 0
        ph = pd.Series(h).shift(1).rolling(n).max().to_numpy()
        pl = pd.Series(l).shift(1).rolling(n).min().to_numpy()
        return np.where(c > ph, 1.0, np.where(c < pl, -1.0, 0.0))
    F = np.vstack([mom(12), mom(48), mom(DAY), pos, dev, wick, rsi(14), rsi(14 * 12), macd(1), macd(12), boll(20), boll(240), stoch, vwapd, donchian(12), donchian(48)]).T
    # compression gates (they say WHEN to trade; the weighted score says WHICH way)
    m20, sd20 = cs.rolling(20).mean(), cs.rolling(20).std()
    tr20 = pd.Series(tr).rolling(20).mean()
    kc = 1.5 * tr20
    sq_on = ((m20 + 2 * sd20) < (m20 + kc)) & ((m20 - 2 * sd20) > (m20 - kc))
    sq_recent = sq_on.shift(1).rolling(6).max().fillna(0).astype(bool)
    fired = (sq_recent & ~sq_on).to_numpy()
    bbw = (4 * sd20 / m20)
    bbw_pct = bbw.rolling(DAY).rank(pct=True).to_numpy()
    ratio = (pd.Series(tr).rolling(12).mean() / pd.Series(tr).rolling(DAY).mean()).to_numpy()
    gates = {"none": np.ones(len(c), bool), "squeeze_fired": np.nan_to_num(fired).astype(bool), "bbw_low": np.nan_to_num(bbw_pct, nan=1.0) <= 0.2,
             "atr_expanding": np.nan_to_num(ratio, nan=0.0) > 1.0, "atr_contracted": np.nan_to_num(ratio, nan=9.0) < 0.7}
    F = np.clip(np.nan_to_num(F, nan=0.0), -4, 4)
    valid = ~np.isnan(atr) & ~np.isnan(trend)
    return {"F": F, "atr": atr, "trend": np.nan_to_num(trend), "hour": hour, "valid": valid, "gates": gates, "htf": np.sign(np.nan_to_num(F[:, 1]))}


def sample(rng: np.random.Generator) -> dict:
    w = np.zeros(len(FEATURES))
    k = int(rng.integers(1, 5))                       # 1 to 4 active features: sparse, so combinations are interpretable
    for j in rng.choice(len(FEATURES), size=k, replace=False):
        w[j] = rng.choice([-1.0, -0.5, 0.5, 1.0])
    h0 = int(rng.choice([0, 6, 7, 8, 12, 13, 14]))
    return {"w": [float(x) for x in w], "theta": round(float(rng.uniform(0.4, 2.5)), 2), "ks": round(float(rng.uniform(0.5, 3.0)), 2),
            "kt": round(float(rng.uniform(0.5, 4.0)), 2), "H": int(rng.choice([12, 24, 48, 96, 192, 576])), "h0": h0, "h1": int(min(24, h0 + rng.choice([4, 6, 8, 12]))),
            "trend": int(rng.integers(0, 2)), "gate": str(rng.choice(["none", "none", "squeeze_fired", "bbw_low", "atr_expanding", "atr_contracted"])), "htf": int(rng.integers(0, 2)),
            "td": float(rng.choice([0, 0, 1.0, 1.5, 2.0, 3.0])), "ts": float(rng.choice([0.5, 1.0, 1.5]))}


def trades(p: dict, d: Dict[str, np.ndarray], f: Dict[str, np.ndarray], lo: int, hi: int) -> np.ndarray:
    """Simulate over bars [lo, hi). Returns array of (entry_time, R)."""
    w = np.array(p["w"])
    score = f["F"][lo:hi] @ w / np.abs(w).sum() * 2
    hrs = f["hour"][lo:hi]
    ok = (np.abs(score) >= p["theta"]) & (hrs >= p["h0"]) & (hrs < p["h1"]) & f["valid"][lo:hi]
    if p["trend"]:
        ok &= np.sign(score) == f["trend"][lo:hi]
    ok &= f["gates"][p.get("gate", "none")][lo:hi]
    if p.get("htf"):
        ok &= np.sign(score) == f["htf"][lo:hi]      # the 4-hour momentum must agree (higher-timeframe bias)
    idx = np.flatnonzero(ok) + lo
    idx = idx[idx + p["H"] + 2 < hi]
    if len(idx) == 0:
        return np.empty((0, 2))
    H = p["H"]
    out, free = [], -1
    cand = idx
    # one position at a time: resolve sequentially but only over candidate entries
    side_all = np.sign(score[cand - lo])
    k = 0
    while k < len(cand):
        i = cand[k]
        if i < free:
            k = int(np.searchsorted(cand, free))
            continue
        side = side_all[k]
        e = d["o"][i + 1] + side * d["s"][i] / 2
        a = f["atr"][i]
        risk = p["ks"] * a
        if risk <= 0:
            k += 1
            continue
        hh, ll = d["h"][i + 1:i + 1 + H], d["l"][i + 1:i + 1 + H]
        half = d["s"][i] / 2
        td = p.get("td", 0.0)
        if side > 0:
            stop, tgt = e - risk, e + p["kt"] * a
            if td:   # trailing stop: once the best price is ts*ATR in profit, the stop follows td*ATR behind the best price (known from the previous bar only)
                cm = np.maximum.accumulate(hh)
                prev = np.concatenate([[-np.inf], cm[:-1]])
                st = np.where(prev - e >= p["ts"] * a, np.maximum(stop, prev - td * a), stop)
                hs = ll - half <= st
            else:
                st = np.full(len(ll), stop)
                hs = ll - half <= stop
            ht = hh - half >= tgt
        else:
            stop, tgt = e + risk, e - p["kt"] * a
            if td:
                cm = np.minimum.accumulate(ll)
                prev = np.concatenate([[np.inf], cm[:-1]])
                st = np.where(e - prev >= p["ts"] * a, np.minimum(stop, prev + td * a), stop)
                hs = hh + half >= st
            else:
                st = np.full(len(hh), stop)
                hs = hh + half >= stop
            ht = ll + half <= tgt
        js = int(np.argmax(hs)) if hs.any() else H
        jt = int(np.argmax(ht)) if ht.any() else H
        if js <= jt and js < H:
            ex, n = st[js], js
        elif jt < js:
            ex, n = tgt, jt
        else:
            ex, n = d["c"][i + H] - side * half, H - 1
        out.append((d["t"][i], side * (ex - e) / risk))
        free = i + 1 + n + 1
        k = int(np.searchsorted(cand, free))
    return np.array(out)


def day_t(tr: np.ndarray) -> Dict[str, float]:
    """Mean R and a day-clustered t-statistic (each calendar day's trades count as one observation, pooled over markets)."""
    if len(tr) == 0:
        return {"n": 0, "mean": 0.0, "t": 0.0}
    days = (tr[:, 0] // 86400).astype(np.int64)
    u, inv = np.unique(days, return_inverse=True)
    s = np.bincount(inv, weights=tr[:, 1])
    cnt = np.bincount(inv)
    mean = tr[:, 1].sum() / len(tr)
    resid = s - mean * cnt           # cluster-robust: sum of (R - mean) within each day
    sd = float(tr[:, 1].std())
    if sd < 1e-6 or len(u) < 2:       # all trades identical (e.g. every one stopped out): no usable variance
        return {"n": int(len(tr)), "mean": float(mean), "t": 0.0}
    se = max(math.sqrt((resid ** 2).sum()) / len(tr), sd / math.sqrt(len(tr)))   # never smaller than the plain standard error
    return {"n": int(len(tr)), "mean": float(mean), "t": float(mean / se)}


def split_points(t_last: int):
    exam0 = t_last - EXAM_DAYS * 86400
    return exam0 - VAL_DAYS * 86400, exam0


def luck_bar(n_total: int) -> float:
    """t-stat that pure luck is expected to reach as the best of n_total tries, plus the pre-registered margin."""
    return math.sqrt(2 * math.log(max(n_total, 2))) + 0.5


def is_candidate(train: dict, n_total: int) -> bool:
    return train["n"] >= 500 and train["mean"] >= 0.03 and train["t"] >= luck_bar(n_total)


def is_finalist(val: dict) -> bool:
    return val["n"] >= 150 and val["mean"] >= 0.03 and val["t"] >= 2.0


def exam_pass(ex: dict) -> bool:
    """Registered 19 Nov 2026 BEFORE the first exam (NAS100's single finalist): twelve market families were searched, so the exam t bar is raised from 2.5 to 3.0 (about 0.05/12);
    the mean bar stays +0.05R. A weaker result (t >= 2.0 and mean > +0.02R) is only 'shadow-worthy': forward paper-trading as a second strategy, no live status."""
    return ex["mean"] >= 0.05 and ex["t"] >= 3.0


def shadow_worthy(ex: dict) -> bool:
    return ex["mean"] > 0.02 and ex["t"] >= 2.0
