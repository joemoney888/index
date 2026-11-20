"""Pulls ONE slice of CME NQ (Nasdaq-100 futures) 10-level order book data from Databento, after a hard cost check, and keeps only one-second samples.
Env: DATABENTO_API_KEY (a repository secret, never printed), START and END (UTC, e.g. 2026-11-18T14:30), SYMBOL (default NQ.c.0 = front month), MAX_USD (default 10; the job stops if the quoted cost is higher).
Output: depth/nq/START.csv.gz with t, mid, spread, bidsz1, asksz1, imb1, imb5, imb10. The raw download is deleted. Uses prepaid credit; places NO orders."""
import csv
import gzip
import os
import sys

import numpy as np


def process_frame(df):
    """df: Databento mbp-10 frame (ts_recv index, bid_px_00.. ask_px_00.., bid_sz_00.. ask_sz_00..). Returns one row per second: last book state in that second."""
    import pandas as pd
    epoch = pd.Timestamp("1970-01-01", tz="UTC")
    sec = ((df.index - epoch) // pd.Timedelta("1s")).to_numpy()
    last = df.groupby(sec).tail(1)
    secs = ((last.index - epoch) // pd.Timedelta("1s")).to_numpy()
    bp, ap = last["bid_px_00"].to_numpy(float), last["ask_px_00"].to_numpy(float)
    out = []
    bs = [last[f"bid_sz_{i:02d}"].to_numpy(float) for i in range(10)]
    as_ = [last[f"ask_sz_{i:02d}"].to_numpy(float) for i in range(10)]
    for k in range(len(last)):
        if not (bp[k] > 0 and ap[k] > 0) or ap[k] < bp[k]:
            continue
        row = [int(secs[k]), (bp[k] + ap[k]) / 2, ap[k] - bp[k], bs[0][k], as_[0][k]]
        for n in (1, 5, 10):
            b, a = sum(bs[i][k] for i in range(n)), sum(as_[i][k] for i in range(n))
            row.append(round((b - a) / (b + a), 4) if b + a > 0 else 0.0)
        out.append(row)
    return out


def main():
    import databento as db
    key = os.environ["DATABENTO_API_KEY"]
    start, end = os.environ["START"], os.environ["END"]
    sym, max_usd = os.environ.get("SYMBOL", "NQ.c.0"), float(os.environ.get("MAX_USD", "10"))
    client = db.Historical(key)
    args = dict(dataset="GLBX.MDP3", symbols=[sym], stype_in="continuous", schema="mbp-10", start=start, end=end)
    cost = client.metadata.get_cost(**args)
    size = client.metadata.get_billable_size(**args)
    print(f"QUOTED COST ${cost:.2f} for {size/1e9:.2f} GB ({start} to {end}, {sym}, mbp-10)", flush=True)
    if cost > max_usd:
        sys.exit(f"Quoted cost ${cost:.2f} is above the cap ${max_usd:.2f}: stopping without downloading.")
    import pandas as pd, time
    rows = []
    edges = pd.date_range(pd.Timestamp(start, tz="UTC"), pd.Timestamp(end, tz="UTC"), freq="30min")
    if edges[-1] < pd.Timestamp(end, tz="UTC"):
        edges = edges.append(pd.DatetimeIndex([pd.Timestamp(end, tz="UTC")]))
    for s0, s1 in zip(edges[:-1], edges[1:]):
        a2 = dict(args, start=s0.isoformat(), end=s1.isoformat())
        path = "nq_raw.dbn.zst"
        for attempt in range(4):
            try:
                client.timeseries.get_range(**a2, path=path)
                break
            except Exception as e:
                print("retry", s0, attempt, e, flush=True)
                time.sleep(5)
        else:
            sys.exit("chunk failed after retries: " + str(s0))
        store = db.DBNStore.from_file(path)
        for chunk in store.to_df(count=2_000_000):
            rows += process_frame(chunk)
        os.remove(path)
        print("chunk done", s0, len(rows), flush=True)
    # keep the last row per second across chunk boundaries
    seen = {}
    for r in rows:
        seen[r[0]] = r
    rows = [seen[k] for k in sorted(seen)]
    os.makedirs("depth/nq", exist_ok=True)
    name = start.replace(":", "").replace("T", "_")
    with gzip.open(f"depth/nq/{name}.csv.gz", "wt", newline="") as f:
        w = csv.writer(f)
        w.writerow(["t", "mid", "spread", "bidsz1", "asksz1", "imb1", "imb5", "imb10"])
        w.writerows(rows)
    print("rows", len(rows))


if __name__ == "__main__":
    main()
