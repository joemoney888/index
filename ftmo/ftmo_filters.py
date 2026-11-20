"""FTMO-compliant entry filters for the NAS100 BFG rule + backtest + rough 2-Step simulation.
Filters ONLY block opening trades (the rule bans OPENING near news / before long closes; holding through is not mentioned).
Calendar: FOMC dates from federalreserve.gov (2021-2026). Jobs report = first Friday of month 08:30 New York.
CPI exact past dates were NOT available -> proxy: every weekday dated 10th-15th at 08:30 New York (over-blocks on purpose).
Close rule: no entries in the 2 hours before any market gap of >= 2 hours (weekend, holiday closes), read from the data itself."""
import datetime as dt, json, sys
from zoneinfo import ZoneInfo
import numpy as np
sys.path.insert(0, "/home/claude/index")
from agent import search

NY = ZoneInfo("America/New_York"); UTC = ZoneInfo("UTC")
FOMC = """2021-01-27 2021-03-17 2021-04-28 2021-06-16 2021-07-28 2021-09-22 2021-11-03 2021-12-15 2022-01-26 2022-03-16 2022-05-04 2022-06-15 2022-07-27 2022-09-21 2022-11-02 2022-12-14
2023-02-01 2023-03-22 2023-05-03 2023-06-14 2023-07-26 2023-09-20 2023-11-01 2023-12-13 2024-01-31 2024-03-20 2024-05-01 2024-06-12 2024-07-31 2024-09-18 2024-11-07 2024-12-18
2025-01-29 2025-03-19 2025-05-07 2025-06-18 2025-07-30 2025-09-17 2025-10-29 2025-12-10 2026-01-28 2026-03-18 2026-04-29 2026-06-17 2026-07-29 2026-09-16 2026-10-28""".split()

def ny_epoch(day, h, m):
    return int(dt.datetime(day.year, day.month, day.day, h, m, tzinfo=NY).astimezone(UTC).timestamp())

def events(kind):
    out = []
    d = dt.date(2021, 5, 1)
    while d <= dt.date(2026, 11, 30):
        if kind == "nfp" and d.weekday() == 4 and d.day <= 7:
            out.append(ny_epoch(d, 8, 30))
        if kind == "cpi" and d.weekday() < 5 and 10 <= d.day <= 15:
            out.append(ny_epoch(d, 8, 30))
        d += dt.timedelta(days=1)
    if kind == "fomc":
        out = [ny_epoch(dt.date.fromisoformat(x), 14, 0) for x in FOMC]
    return out

def block_mask(t, kinds, win_min=None, whole_day=False, close=True):
    entry = t + 300                      # a signal on bar i enters at the next bar's open
    m = np.zeros(len(t), bool)
    if close:
        for k in np.flatnonzero(np.diff(t) >= 7200 + 300):
            c = t[k] + 300
            m |= (entry >= c - 7200) & (entry < c)
    for kd in kinds:
        for e in events(kd):
            if whole_day:
                d0 = (e // 86400) * 86400
                m |= (entry >= d0) & (entry < d0 + 86400)
            else:
                m |= (entry >= e - win_min * 60) & (entry <= e + win_min * 60)
    return m

def run(name, d, f, p, mask, lo, hi):
    f2 = dict(f); g = dict(f["gates"]); g["x"] = g[p["gate"]] & ~mask; f2["gates"] = g
    return search.trades(dict(p, gate="x"), d, f2, lo, hi)

if __name__ == "__main__":
    p = json.load(open("/home/claude/index/search/NAS100/finalists.json"))[0]["p"]
    d = search.load_arrays("/home/claude/gbpusd-paper-agent/data/bars5/NAS100.csv.gz")
    f = search.build_features(d)
    val0, ex0 = search.split_points(int(d["t"][-1]))
    iv, ie = int(np.searchsorted(d["t"], val0)), int(np.searchsorted(d["t"], ex0))
    segs = {"train": (0, iv), "val": (iv, ie), "exam": (ie, len(d["t"]))}
    cases = {"A baseline (no filter)": None,
             "B close-window only": ([], 0, False, True),
             "C +NFP/FOMC +-15min": (["nfp", "fomc"], 15, False, True),
             "D +NFP/FOMC +-2h": (["nfp", "fomc"], 120, False, True),
             "E +NFP/FOMC whole day": (["nfp", "fomc"], 0, True, True),
             "F +NFP/FOMC/CPI(proxy) +-2h": (["nfp", "fomc", "cpi"], 120, False, True),
             "G +NFP/FOMC/CPI(proxy) whole day": (["nfp", "fomc", "cpi"], 0, True, True)}
    res = {}
    for nm, c in cases.items():
        mask = np.zeros(len(d["t"]), bool) if c is None else block_mask(d["t"], c[0], c[1], c[2], c[3])
        row = {}
        for s, (lo, hi) in segs.items():
            tr = run(nm, d, f, p, mask, lo, hi); row[s] = search.day_t(tr)
            if s == "exam": res[nm + "|tr"] = tr
        res[nm] = row
        print(f"{nm:36s} blocked {mask.mean()*100:4.1f}% | " + " | ".join(f"{s} n={r['n']:5d} {r['mean']:+.3f}R t={r['t']:.2f}" for s, r in row.items()))
    np.save("/home/claude/index/ftmo/_tr_all.npy", np.array([0]))
