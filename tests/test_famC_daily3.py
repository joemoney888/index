import importlib.util, os, numpy as np, pandas as pd
sp = importlib.util.spec_from_file_location("d3", os.path.join(os.path.dirname(__file__), "..", "famC", "run_daily3.py")); d3 = importlib.util.module_from_spec(sp); sp.loader.exec_module(d3)
def test_d4_planted_spike_found():
    idx = pd.bdate_range("1990-01-02", "2000-12-29"); vix = pd.Series(15.0, index=idx); spx = pd.Series(100.0, index=idx)
    for k in range(40, len(idx) - 10, 50):
        vix.iloc[k] = 30.0; spx.iloc[k + 1:] *= 1.02          # planted +2% in the 5 days after each spike
    ev = d3.d4(spx, vix, last="2000-12-29"); assert len(ev) >= 8 and all(x[1] > 150 for x in ev)
def test_d5_picks_third_friday():
    idx = pd.bdate_range("2020-01-01", "2020-06-30"); spx = pd.Series(np.arange(len(idx), dtype=float) + 100, index=idx)
    wk = d3.d5(spx); assert any(str(x[0].date()) == "2020-02-21" for x in wk)
