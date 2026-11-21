import numpy as np

from agent import index_live as il, search


def _data(n=9000, seed=0):
    r = np.random.default_rng(seed)
    c = 100 + np.cumsum(r.normal(0, 0.05, n))
    o = np.concatenate([[c[0]], c[:-1]])
    return {"t": 1_700_000_000 + 300 * np.arange(n), "o": o, "h": np.maximum(o, c) + 0.02, "l": np.minimum(o, c) - 0.02, "c": c, "s": np.full(n, 0.01)}


def test_signal_matches_backtest_entries():
    d = _data(9000, seed=2)
    d["t"] = d["t"] - d["t"][0] + 1_700_006_400          # start at 00:00 UTC so the session hours occur
    f = search.build_features(d)
    p = {"w": [0, 0, 0, -0.5, 0, 0, -1.0, -1.0, 0, 0, 0, 0, -0.5, 0, 0, 0], "theta": 0.47, "ks": 2.98, "kt": 3.79, "H": 192, "h0": 0, "h1": 24, "trend": 1, "gate": "none", "htf": 0, "td": 1.0, "ts": 0.5}
    tr = search.trades(p, d, f, 300, len(d["t"]))
    assert len(tr) > 5
    tix = {int(t): i for i, t in enumerate(d["t"])}
    for t, _ in tr:
        assert il.signal_at(p, f, tix[int(t)]) != 0          # every backtest entry is a live signal


def test_trailing_and_sizing():
    p = {"td": 1.0, "ts": 0.5}
    assert il.trail_stop(p, 1, 100, 90, 90, 10, 103) == 90                 # not yet 0.5 ATR in profit... 3 < 5
    assert il.trail_stop(p, 1, 100, 90, 90, 10, 108) == 98                 # best 108 - 1 ATR
    assert il.trail_stop(p, 1, 100, 90, 98, 10, 105) == 98                 # never backwards
    assert il.trail_stop(p, -1, 100, 110, 110, 10, 92) == 102
    assert il.units_for(75.0, 1.31) == 0.08 and il.units_for(1000.0, 1.31) == 0.0


def test_plan():
    pl = il.plan({"ks": 3.0, "kt": 4.0}, -1, 100.0, 2.0)
    assert pl["stop"] == 106.0 and pl["target"] == 92.0


def test_compound_risk():
    assert il.compound_risk_gbp([]) == 5.0
    assert il.compound_risk_gbp([100.0, -50.0]) == 5.5
    assert il.compound_risk_gbp([-600.0]) == 0.0
    assert il.units_for(75.0, 1.31, 10.0) == 0.17 and il.units_for(75.0, 1.31) == 0.08
