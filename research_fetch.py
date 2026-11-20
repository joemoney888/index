"""Downloads the FIXED research window of 5-minute OANDA candles (mid OHLC + spread) for one market into data/bars5/NAME.csv.gz (not committed; the public repo never republishes the data).
The window is pinned (2021-05-19 16:00 to 2026-11-18 16:00 UTC, identical to the original private-repo data) so the train / validation / locked-exam boundaries never slide. Env: MARKET, OANDA_API_TOKEN_INDEX, OANDA_ACCOUNT_ID_INDEX. Reads only."""
import csv
import gzip
import os
from datetime import datetime, timezone

from agent import oanda
from forward_shadow import fetch_chunked

START = datetime(2021, 5, 19, 16, 0, tzinfo=timezone.utc)
END = datetime(2026, 11, 18, 16, 0, tzinfo=timezone.utc)
INSTR = {"NAS100": "NAS100_USD", "SPX500": "SPX500_USD", "US30": "US30_USD"}


def main():
    name = os.environ["MARKET"].upper()
    client = oanda.OandaPractice(os.environ["OANDA_API_TOKEN_INDEX"], os.environ["OANDA_ACCOUNT_ID_INDEX"])
    cs = [c for c in fetch_chunked(client, INSTR.get(name, name + "_USD"), START, END) if c.complete]
    os.makedirs("data/bars5", exist_ok=True)
    with gzip.open(f"data/bars5/{name}.csv.gz", "wt", newline="") as f:
        w = csv.writer(f)
        w.writerow(["t", "o", "h", "l", "c", "spread"])
        for c in cs:
            w.writerow([int(c.start.timestamp()), c.open, c.high, c.low, c.close, round(c.spread, 6)])
    print(name, len(cs), "bars", cs[0].start if cs else None, cs[-1].start if cs else None)


if __name__ == "__main__":
    main()
