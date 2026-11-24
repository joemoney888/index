import os, sys, types, importlib, csv, datetime as dt
from zoneinfo import ZoneInfo
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
fc = importlib.import_module("forward_context")
NY = ZoneInfo("America/New_York")
class C:
    def __init__(s, t, o, c): s.start, s.open, s.close, s.spread = t, o, c, 0.5
class Fake:
    def __init__(s, gap, hr): s.gap, s.hr = gap, hr
    def get_candles_range(s, ins, a, b, g, price="MBA"):
        d = a.astimezone(NY).date(); u = lambda h, m: dt.datetime(d.year, d.month, d.day, h, m, tzinfo=NY).astimezone(dt.timezone.utc)
        return [C(u(9, 30), 100 * (1 + s.gap / 100), 100), C(u(10, 25), 100, 100 * (1 + s.gap / 100) * (1 + s.hr / 100)), C(u(15, 55), 100, 101)]
def test_flags():
    D = dt.date(2026, 11, 24)
    r = fc.row_for(Fake(1.5, 0.0), "X", D, 100.0); assert r["big_day_flag"] == 1 and abs(r["gap_pct"] - 1.5) < 1e-6
    r = fc.row_for(Fake(0.1, 0.1), "X", D, 100.0); assert r["big_day_flag"] == 0
def test_missing_bars_skipped():
    class Empty:
        def get_candles_range(s, *a, **k): return []
    assert fc.row_for(Empty(), "X", dt.date(2026, 11, 24), 100.0) is None
