import sys, os, json
import numpy as np, pandas as pd, importlib.util
_sp = importlib.util.spec_from_file_location("runA", os.path.join(os.path.dirname(__file__), "..", "famA", "run.py")); run = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(run)

def synth(effect, days=400, seed=1):
    rng = np.random.default_rng(seed); T=[];O=[];C=[];S=[]; px=10000.0
    for D in pd.bdate_range("2022-01-03", periods=days):
        # session 09:30-16:00 NY, 5-min bars; London 08:00 bar also needed (03:00 NY ~ 08:00 London except DST gaps: build in UTC via London tz)
        lon = pd.Timestamp(D.year, D.month, D.day, 8, 0, tz="Europe/London")
        ts = [lon + pd.Timedelta(minutes=5*k) for k in range(0, 12)]            # 08:00-08:55 London
        ny0 = pd.Timestamp(D.year, D.month, D.day, 9, 10, tz="America/New_York")
        ts += [ny0 + pd.Timedelta(minutes=5*k) for k in range(0, 82)]            # 09:10 .. 16:00 NY
        ts = sorted(set(ts)); rets = rng.normal(0, 3e-4, len(ts))
        idx = {t.tz_convert("America/New_York").strftime("%H:%M"): i for i, t in enumerate(ts)}
        # planted: sign of 15:00-15:25 move continues into 15:30-15:55
        a = [i for t, i in idx.items() if "15:00" <= t <= "15:25"]; b = [i for t, i in idx.items() if "15:30" <= t <= "15:55"]
        sgn = np.sign(rets[a].sum()); rets[b] += sgn * effect / len(b)
        for t, r in zip(ts, rets):
            o = px; px = px * (1 + r); T.append(int(t.timestamp())); O.append(o); C.append(px); S.append(px * 0.4e-4)
    return np.array(T), np.array(O), np.array(C), np.array(S)

def test_trade_math():
    assert abs(run.trade_bp(1, 100, 0.0, 101, 0.0) - 100.0) < 1e-9       # +1% = 100 bp
    assert run.trade_bp(1, 100, .01, 100, .01) < 0 and run.trade_bp(-1, 100, .01, 100, .01) < 0   # spread always costs
    assert abs(run.gross_bp(-1, 100, 99) - 100.0) < 1e-9                 # short wins when price falls

def test_nw_matches_plain_t_for_iid():
    x = np.random.default_rng(0).normal(1, 5, 5000); t, _ = run.nw_t(x, 5)
    assert abs(t - x.mean() / (x.std() / len(x) ** .5)) < 0.3

def test_detects_planted_and_not_null():
    cal = {"full_holidays": [], "early_close_1300": []}
    for eff, expect in ((6e-4, True), (0.0, False)):
        t, o, c, s = synth(eff); rows, skips, _ = run.run_specs(t, o, c, s, cal, "2022-01-04", "2023-07-31")
        out = run.summarise(rows)
        assert out["A6b"]["n_used"] > 300
        assert out["A6b"]["PASS"] == expect, (eff, out["A6b"]["t"], out["A6b"]["net_mean_bp"])
        assert not out["A5"]["PASS"]                                      # no planted London reversal
