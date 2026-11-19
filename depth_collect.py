"""Concept test for level 2 data (order book imbalance), on a free public crypto order book (Kraken BTC/USD and ETH/USD). Reads only; places NO orders.
Streams the top-25 book for MINUTES minutes, samples once a second: mid, spread, imbalance over the top 1, 5 and 25 levels. Writes depth/data/DAY_HHMM.csv.gz.
Env: MINUTES (default 10)."""
import asyncio
import csv
import gzip
import json
import os
import time
from datetime import datetime, timezone

import websockets

SYMBOLS = ["BTC/USD", "ETH/USD"]


def imb(bids, asks, n):
    b = sum(q for _, q in sorted(bids.items(), reverse=True)[:n])
    a = sum(q for _, q in sorted(asks.items())[:n])
    return (b - a) / (b + a) if b + a > 0 else 0.0


async def run(minutes):
    books = {s: ({}, {}) for s in SYMBOLS}
    rows = []
    end = time.time() + minutes * 60
    async with websockets.connect("wss://ws.kraken.com/v2", ping_interval=20) as ws:
        await ws.send(json.dumps({"method": "subscribe", "params": {"channel": "book", "symbol": SYMBOLS, "depth": 25}}))
        nxt = time.time()
        while time.time() < end:
            try:
                msg = json.loads(await asyncio.wait_for(ws.recv(), timeout=5))
            except asyncio.TimeoutError:
                continue
            if msg.get("channel") == "book":
                for d in msg.get("data", []):
                    bids, asks = books[d["symbol"]]
                    if msg["type"] == "snapshot":
                        bids.clear()
                        asks.clear()
                    for x in d.get("bids", []):
                        bids.pop(x["price"], None) if x["qty"] == 0 else bids.__setitem__(x["price"], x["qty"])
                    for x in d.get("asks", []):
                        asks.pop(x["price"], None) if x["qty"] == 0 else asks.__setitem__(x["price"], x["qty"])
                    # keep only the best 25 per side
                    for side, rev in ((bids, True), (asks, False)):
                        if len(side) > 25:
                            for p in sorted(side, reverse=rev)[25:]:
                                side.pop(p)
            now = time.time()
            if now >= nxt:
                nxt = now + 1
                for s in SYMBOLS:
                    bids, asks = books[s]
                    if bids and asks:
                        bb, ba = max(bids), min(asks)
                        rows.append((int(now), s, round((bb + ba) / 2, 4), round(ba - bb, 4), round(imb(bids, asks, 1), 4), round(imb(bids, asks, 5), 4), round(imb(bids, asks, 25), 4)))
    return rows


def main():
    minutes = float(os.environ.get("MINUTES", "10"))
    rows = asyncio.run(run(minutes))
    os.makedirs("depth/data", exist_ok=True)
    name = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M")
    with gzip.open(f"depth/data/{name}.csv.gz", "wt", newline="") as f:
        w = csv.writer(f)
        w.writerow(["t", "symbol", "mid", "spread", "imb1", "imb5", "imb25"])
        w.writerows(rows)
    print("rows", len(rows), "->", name)


if __name__ == "__main__":
    main()
