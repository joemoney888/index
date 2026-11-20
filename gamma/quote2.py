import os, databento as db
c = db.Historical(os.environ["DATABENTO_API_KEY"])
for a, b in (("2026-11-17T12:00", "2026-11-17T14:30"), ("2026-11-17T13:00", "2026-11-17T14:30"), ("2026-07-15T12:00", "2026-07-15T13:30")):
    k = dict(dataset="OPRA.PILLAR", symbols="QQQ.OPT", stype_in="parent", schema="statistics", start=a, end=b)
    try: print(a, b, "cost $", round(c.metadata.get_cost(**k), 3), "bytes", c.metadata.get_billable_size(**k), flush=True)
    except Exception as e: print(a, "ERROR", str(e)[:200], flush=True)
