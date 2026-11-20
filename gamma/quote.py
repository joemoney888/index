"""QUOTE ONLY (no download, no spend): what would QQQ option open-interest history and QQQ daily prices cost on Databento?"""
import os, databento as db
c = db.Historical(os.environ["DATABENTO_API_KEY"])
def q(label, **k):
    try:
        print(label, "cost $", round(c.metadata.get_cost(**k), 3), "| bytes", c.metadata.get_billable_size(**k), flush=True)
    except Exception as e:
        print(label, "ERROR", str(e)[:300], flush=True)
for ds in ("OPRA.PILLAR", "EQUS.MINI", "XNAS.BASIC", "DBEQ.BASIC"):
    try: print(ds, "range", c.metadata.get_dataset_range(ds), flush=True)
    except Exception as e: print(ds, "range ERROR", str(e)[:200], flush=True)
for a, b in (("2026-11-17", "2026-11-18"), ("2026-10-19", "2026-11-19"), ("2025-11-19", "2026-11-19")):
    q(f"OPRA statistics QQQ.OPT {a}..{b}", dataset="OPRA.PILLAR", symbols="QQQ.OPT", stype_in="parent", schema="statistics", start=a, end=b)
for ds in ("EQUS.MINI", "XNAS.BASIC", "DBEQ.BASIC"):
    q(f"{ds} ohlcv-1m QQQ 1y", dataset=ds, symbols="QQQ", schema="ohlcv-1m", start="2025-11-19", end="2026-11-19")
