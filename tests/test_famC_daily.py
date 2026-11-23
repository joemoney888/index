import importlib.util, os, numpy as np, pandas as pd
sp = importlib.util.spec_from_file_location("dd", os.path.join(os.path.dirname(__file__), "..", "famC", "run_daily.py")); dd = importlib.util.module_from_spec(sp); sp.loader.exec_module(dd)
def synth(tom_bp, seed=0):
    rng = np.random.default_rng(seed); dates = pd.bdate_range("1995-01-02", "2015-12-31"); r = rng.normal(0, 0.01, len(dates)); df = pd.DataFrame({"date": dates, "r0": r})
    df["ym"] = df["date"].dt.to_period("M"); pos = df.groupby("ym").cumcount(); rev = df.groupby("ym").cumcount(ascending=False)
    df.loc[(pos < 3) | (rev < 1), "r0"] += tom_bp / 1e4; df["adjusted_close"] = 100 * np.cumprod(1 + df["r0"]); return df[["date", "adjusted_close"]].assign(close=lambda x: x["adjusted_close"])
def test_planted_tom_found():
    d = dd.load_df(synth(40)) if hasattr(dd, "load_df") else None
    df = synth(40).sort_values("date").reset_index(drop=True); df["r"] = df["adjusted_close"].pct_change(); rows = dd.d1(df); assert dd.judge([x[1] for x in rows], 1, 4.0)["PASS"]
def test_null_not_found():
    df = synth(0, seed=3).sort_values("date").reset_index(drop=True); df["r"] = df["adjusted_close"].pct_change(); rows = dd.d1(df); assert not dd.judge([x[1] for x in rows], 1, 4.0)["PASS"]
