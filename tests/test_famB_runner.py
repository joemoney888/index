import sys, os
import numpy as np, pandas as pd, importlib.util
_sp = importlib.util.spec_from_file_location("runB", os.path.join(os.path.dirname(__file__), "..", "famB", "run.py")); run = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(run)

def bars(days, drift_after_break=0.0, seed=0):
    rng = np.random.default_rng(seed); T=[];O=[];H=[];L=[];C=[];S=[]; px=10000.0
    for D in pd.bdate_range("2022-01-03", periods=days):
        t0 = pd.Timestamp(D.year, D.month, D.day, 9, 30, tz="America/New_York")
        pre = pd.Timestamp(D.year, D.month, D.day, 8, 0, tz="America/New_York")
        for k in range(-18, 78):
            ts = t0 + pd.Timedelta(minutes=5 * k); r = rng.normal(0, 2e-4)
            if k >= 3 and k < 30: r += drift_after_break      # sustained drift after the opening range
            o = px; px *= 1 + r; hh = max(o, px) * (1 + 1e-4); ll = min(o, px) * (1 - 1e-4)
            T.append(int(ts.timestamp())); O.append(o); H.append(hh); L.append(ll); C.append(px); S.append(px * 0.4e-4)
    return [np.array(x) for x in (T, O, H, L, C, S)]

CAL = {"full_holidays": [], "early_close_1300": []}
FO = {"decision_days": ["2022-02-02"]}

def test_orb_trades_with_drift_and_losses_costs_on_noise():
    for drift, sign in ((6e-4, 1), (0.0, 0)):
        t, o, h, l, c, s = bars(300, drift)
        out, sk = run.run_all(t, o, h, l, c, s, CAL, FO, "2022-01-04", "2022-12-30")
        v = out["ORB"][1]; assert len(v) > 100
        if sign: assert np.mean(v) > 0.3          # clear continuation after break is captured
        else: assert np.mean(v) < 0.1             # no edge -> no profit (costs make it <= ~0)

def test_orb_stop_and_target_bounds():
    t, o, h, l, c, s = bars(300, 0.0, seed=3)
    out, _ = run.run_all(t, o, h, l, c, s, CAL, FO, "2022-01-04", "2022-12-30")
    v = np.array(out["ORB"][1]); assert v.max() <= 2.05 and v.min() >= -1.5   # +2R cap (minus costs), stop about -1R (gap/cost slack)

def test_fomc_events_found_and_cost_sign():
    t, o, h, l, c, s = bars(60)
    out, sk = run.run_all(t, o, h, l, c, s, CAL, FO, "2022-01-04", "2022-03-31")
    assert len(out["F1"][1]) == 1 and len(out["F2"][1]) == 1 and sk["F1"] == 0 and sk["F2"] == 0
