"""Chart patterns turned into numbers, with NO hindsight: a swing point is only used K bars after it happened (when it is confirmed).
Patterns: dt = double top (M) / double bottom (W); hs = head and shoulders (and inverse); tri = converging triangle breakout. Direction 'follow' trades the textbook direction (M short, W long, breakout with the break), 'fade' the opposite.
Trigger: brk 0 = at the confirmation of the last swing point; brk 1 = when the close first breaks the neckline / triangle line within 3K bars. Entry is the next bar's open. Reads files only."""
import numpy as np
import pandas as pd


def pivots(h, l, K):
    n = len(h)
    hm = pd.Series(h).rolling(2 * K + 1, center=True).max().to_numpy()
    lm = pd.Series(l).rolling(2 * K + 1, center=True).min().to_numpy()
    ph, pl = np.flatnonzero(h == hm), np.flatnonzero(l == lm)
    ev = sorted([(int(i), float(h[i]), 1) for i in ph] + [(int(i), float(l[i]), -1) for i in pl])
    out = []
    for i, p, t in ev:
        if out and out[-1][2] == t:
            if (t == 1 and p > out[-1][1]) or (t == -1 and p < out[-1][1]):
                out[-1] = (i, p, t)
        else:
            out.append((i, p, t))
    return out


def _first_break(c, start, end, level_fn, direction):
    """First bar in [start, end) whose close crosses level (direction -1 = below, +1 = above); level_fn(t) gives the level at bar t."""
    end = min(end, len(c))
    for t in range(start, end):
        lv = level_fn(t)
        if (direction < 0 and c[t] < lv) or (direction > 0 and c[t] > lv):
            return t
    return None


def signals(pattern, P, K, tol, depth, brk, mode, atr, c):
    """Returns sorted array of (trigger_bar, side). Trigger bar = the bar at whose close the pattern is known."""
    out = []
    sgn = 1 if mode == "follow" else -1
    n = len(P)
    if pattern == "dt":
        for i in range(n - 2):
            (i0, p0, t0), (i1, p1, _), (i2, p2, _) = P[i], P[i + 1], P[i + 2]
            conf = i2 + K
            if conf >= len(c) or not np.isfinite(atr[conf]) or atr[conf] <= 0:
                continue
            a = atr[conf]
            if abs(p0 - p2) > tol * a or abs(p0 - p1) < depth * a:
                continue
            top = t0 == 1
            side_text = -1 if top else 1                   # M expects a fall, W a rise
            if brk:
                t = _first_break(c, conf + 1, conf + 1 + 3 * K, lambda _t: p1, side_text)
                if t is None:
                    continue
            else:
                t = conf
            out.append((t, sgn * side_text))
    elif pattern == "hs":
        for i in range(n - 4):
            (i0, p0, t0), (i1, p1, _), (i2, p2, _), (i3, p3, _), (i4, p4, _) = P[i:i + 5]
            conf = i4 + K
            if conf >= len(c) or not np.isfinite(atr[conf]) or atr[conf] <= 0:
                continue
            a = atr[conf]
            top = t0 == 1
            head = (p2 - max(p0, p4)) if top else (min(p0, p4) - p2)
            if head < depth * a or abs(p0 - p4) > tol * a * 2:
                continue
            neck = (p1 + p3) / 2
            side_text = -1 if top else 1
            if brk:
                t = _first_break(c, conf + 1, conf + 1 + 3 * K, lambda _t: neck, side_text)
                if t is None:
                    continue
            else:
                t = conf
            out.append((t, sgn * side_text))
    else:  # tri: two highs and two lows converging
        for i in range(n - 3):
            q = P[i:i + 4]
            hs_ = [x for x in q if x[2] == 1]
            ls_ = [x for x in q if x[2] == -1]
            if len(hs_) != 2 or len(ls_) != 2:
                continue
            conf = q[-1][0] + K
            if conf >= len(c) or not np.isfinite(atr[conf]) or atr[conf] <= 0:
                continue
            a = atr[conf]
            sh = (hs_[1][1] - hs_[0][1]) / max(hs_[1][0] - hs_[0][0], 1)
            sl = (ls_[1][1] - ls_[0][1]) / max(ls_[1][0] - ls_[0][0], 1)
            width = hs_[1][1] - ls_[1][1]
            if not (sh < 0 < sl) or width < depth * a:        # symmetrical: lower highs, higher lows
                continue
            up = lambda t, h0=hs_[0], s=sh: h0[1] + s * (t - h0[0])   # noqa: E731
            lo = lambda t, l0=ls_[0], s=sl: l0[1] + s * (t - l0[0])   # noqa: E731
            end = conf + 1 + 3 * K
            tu = _first_break(c, conf + 1, end, up, 1)
            td = _first_break(c, conf + 1, end, lo, -1)
            cands = [(t, d) for t, d in ((tu, 1), (td, -1)) if t is not None]
            if not cands:
                continue
            t, d = min(cands)
            out.append((t, sgn * d))
    out.sort()
    return out


def simulate(sig, d, f, p, lo, hi):
    """One position at a time, same cost and fill logic as search.trades (stop ks*ATR, target kt*ATR, horizon H, half-spread each way, entry at next open). Returns array of (entry_time, R)."""
    H, ks, kt = p["H"], p["ks"], p["kt"]
    hrs, atr = f["hour"], f["atr"]
    out, free = [], -1
    for t, side in sig:
        if t < lo or t >= hi or t < free or t + H + 2 >= hi:
            continue
        if not (p["h0"] <= hrs[t] < p["h1"]) or not f["valid"][t]:
            continue
        a = atr[t]
        risk = ks * a
        if not (risk > 0):
            continue
        half = d["s"][t] / 2
        e = d["o"][t + 1] + side * half
        hh, ll = d["h"][t + 1:t + 1 + H], d["l"][t + 1:t + 1 + H]
        if side > 0:
            stop, tgt = e - risk, e + kt * a
            hs, ht = ll - half <= stop, hh - half >= tgt
        else:
            stop, tgt = e + risk, e - kt * a
            hs, ht = hh + half >= stop, ll + half <= tgt
        js = int(np.argmax(hs)) if hs.any() else H
        jt = int(np.argmax(ht)) if ht.any() else H
        if js <= jt and js < H:
            ex, n = stop, js
        elif jt < js:
            ex, n = tgt, jt
        else:
            ex, n = d["c"][t + H] - side * half, H - 1
        out.append((d["t"][t], side * (ex - e) / risk))
        free = t + 1 + n + 1
    return np.array(out) if out else np.empty((0, 2))
