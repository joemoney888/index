import importlib.util, os, math
sp = importlib.util.spec_from_file_location("ff", os.path.join(os.path.dirname(__file__), "..", "forward_fomc.py")); ff = importlib.util.module_from_spec(sp); sp.loader.exec_module(ff)
from datetime import date
def test_prev_weekday():
    assert ff.prev_weekday(date(2026, 12, 9)) == date(2026, 12, 8) and ff.prev_weekday(date(2027, 3, 15)) == date(2027, 3, 12)
def test_net_bp_cost_and_sign():
    assert abs(ff.net_bp(100.0, 0, 101.0, 0) - 100.0) < 1e-9 and ff.net_bp(100.0, 0.01, 100.0, 0.01) < 0
def test_stats():
    n, m, t = ff.stats([10.0, 20.0, 30.0]); assert n == 3 and abs(m - 20) < 1e-9 and abs(t - 20 / (10 / math.sqrt(3))) < 1e-9
