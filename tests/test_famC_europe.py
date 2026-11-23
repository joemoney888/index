import importlib.util, os, numpy as np, pandas as pd
sp = importlib.util.spec_from_file_location("eu", os.path.join(os.path.dirname(__file__), "..", "famC", "run_europe.py")); eu = importlib.util.module_from_spec(sp); sp.loader.exec_module(eu)
def synth(drift_bp):
    ts = []; o = []; c = []; p = 10000.0
    for D in pd.date_range("2022-01-03", "2022-03-31", freq="D"):
        s0 = int(pd.Timestamp(f"{D.date()} 16:00", tz="America/New_York").timestamp())
        for k in range(12 * 24):                       # 16:00 -> next 16:00
            ts.append(s0 + 300 * k); hour = (16 + k * 5 / 60) % 24; step = drift_bp / 48 if (hour >= 23.5 or hour < 3.5) else 0.0
            o.append(p); p *= 1 + step / 1e4; c.append(p)
    return np.array(ts), np.array(o), np.array(c), np.full(len(ts), 0.0)
def test_planted_drift_detected():
    t, o, c, s = synth(5.0); rows, sk = eu.run(t, o, c, s, "2022-01-10", "2022-03-20"); r = eu.summarise(rows)
    assert abs(r["gross_mean_bp"] - 5.0) < 0.3 and r["n"] > 40
def test_zero_drift_none():
    t, o, c, s = synth(0.0); rows, _ = eu.run(t, o, c, s, "2022-01-10", "2022-03-20"); assert abs(np.mean([x[2] for x in rows])) < 1e-6
