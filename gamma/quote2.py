import os, databento as db
c = db.Historical(os.environ["DATABENTO_API_KEY"])
for a, b in (("2026-11-17T00:00", "2026-11-17T06:00"), ("2026-11-17T06:00", "2026-11-17T12:00"), ("2026-11-17T14:30", "2026-11-17T15:30"), ("2026-11-17T15:30", "2026-11-17T21:00"), ("2026-11-17T21:00", "2026-11-18T00:00")):
    k = dict(dataset="OPRA.PILLAR", symbols="QQQ.OPT", stype_in="parent", schema="statistics", start=a, end=b)
    try: print(a, b, "cost $", round(c.metadata.get_cost(**k), 3), "bytes", c.metadata.get_billable_size(**k), flush=True)
    except Exception as e: print(a, "ERROR", str(e)[:200], flush=True)
