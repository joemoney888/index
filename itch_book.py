"""Rebuilds the real Nasdaq order book for a few stocks from a Nasdaq ITCH 5.0 day file streamed on stdin, and samples it once a second during regular hours.
Usage: curl -sL <url> | gzip -dc | python itch_book.py  (nothing is saved except the small per-second CSVs). Reads only; places NO orders.
Output per symbol: depth/itch/SYMBOL.csv.gz with columns t (seconds after midnight, US Eastern as in the file), mid, spread, bidsz1, asksz1, imb1, imb5, imb10.
Imbalance = (bid size - ask size) / (bid size + ask size) summed over the best N price levels. Note: this is Nasdaq's own book, not the consolidated market."""
import csv
import gzip
import heapq
import os
import struct
import sys

SYMS = [s.encode().ljust(8) for s in os.environ.get("SYMS", "QQQ,AAPL,MSFT,NVDA,AMZN,TSLA,SPY").split(",")]
OPEN, CLOSE = 34200, 57600   # 09:30 and 16:00 in seconds after midnight


class Book:
    __slots__ = ("bids", "asks")

    def __init__(self):
        self.bids, self.asks = {}, {}

    def add(self, side, price, shares):
        d = self.bids if side == 66 else self.asks     # 66 = 'B'
        d[price] = d.get(price, 0) + shares

    def sub(self, side, price, shares):
        d = self.bids if side == 66 else self.asks
        left = d.get(price, 0) - shares
        if left <= 0:
            d.pop(price, None)
        else:
            d[price] = left

    def sample(self):
        if not self.bids or not self.asks:
            return None
        nb, na = heapq.nlargest(10, self.bids), heapq.nsmallest(10, self.asks)
        bb, ba = nb[0], na[0]
        row = [(bb + ba) / 2 / 1e4, (ba - bb) / 1e4, self.bids[bb], self.asks[ba]]
        for n in (1, 5, 10):
            b = sum(self.bids[p] for p in nb[:n])
            a = sum(self.asks[p] for p in na[:n])
            row.append(round((b - a) / (b + a), 4))
        return row


def process(stream, syms=SYMS, quiet=False):
    locate, books, orders, out = {}, {}, {}, {s: [] for s in syms}
    buf, last_sec, n = b"", -1, 0
    unpack = struct.unpack_from
    while True:
        chunk = stream.read(1 << 22)
        if not chunk:
            break
        buf += chunk
        pos, end = 0, len(buf)
        while pos + 2 <= end:
            L = (buf[pos] << 8) | buf[pos + 1]
            if pos + 2 + L > end:
                break
            p = pos + 2
            t = buf[p]
            if t in (65, 70, 69, 67, 88, 68, 85):      # sample the book as it stood at the end of the previous second, BEFORE applying this message
                ts = int.from_bytes(buf[p + 5:p + 11], "big") // 1_000_000_000
                if ts != last_sec:
                    if OPEN <= last_sec < CLOSE and last_sec >= 0:
                        for loc, b in books.items():
                            r = b.sample()
                            if r:
                                out[locate[loc]].append([last_sec] + r)
                    last_sec = ts
            if t == 82:                                   # 'R' stock directory
                stock = bytes(buf[p + 11:p + 19])
                if stock in syms:
                    loc = unpack(">H", buf, p + 1)[0]
                    locate[loc] = stock
                    books[loc] = Book()
            elif t == 65 or t == 70:                      # 'A' / 'F' add order
                loc = unpack(">H", buf, p + 1)[0]
                if loc in books:
                    ref, side, shares = unpack(">QcI", buf, p + 11)[0], buf[p + 19], unpack(">I", buf, p + 20)[0]
                    price = unpack(">I", buf, p + 32)[0]
                    orders[ref] = (loc, side, price, shares)
                    books[loc].add(side, price, shares)
            elif t == 69 or t == 67 or t == 88:           # 'E' executed, 'C' executed with price, 'X' cancel (partial)
                ref = unpack(">Q", buf, p + 11)[0]
                o = orders.get(ref)
                if o:
                    shares = unpack(">I", buf, p + 19)[0]
                    loc, side, price, sh = o
                    books[loc].sub(side, price, shares)
                    if shares >= sh:
                        del orders[ref]
                    else:
                        orders[ref] = (loc, side, price, sh - shares)
            elif t == 68:                                 # 'D' delete
                ref = unpack(">Q", buf, p + 11)[0]
                o = orders.pop(ref, None)
                if o:
                    books[o[0]].sub(o[1], o[2], o[3])
            elif t == 85:                                 # 'U' replace
                ref = unpack(">Q", buf, p + 11)[0]
                o = orders.pop(ref, None)
                if o:
                    loc, side, price, sh = o
                    books[loc].sub(side, price, sh)
                    new, shares, nprice = unpack(">Q", buf, p + 19)[0], unpack(">I", buf, p + 27)[0], unpack(">I", buf, p + 31)[0]
                    orders[new] = (loc, side, nprice, shares)
                    books[loc].add(side, nprice, shares)
            n += 1
            pos += 2 + L
        buf = buf[pos:]
        if not quiet and n % 5_000_000 < 200000:
            print("messages", n, "second", last_sec, flush=True)
    return out


def main():
    out = process(sys.stdin.buffer)
    os.makedirs("depth/itch", exist_ok=True)
    for s, rows in out.items():
        name = s.decode().strip()
        with gzip.open(f"depth/itch/{name}.csv.gz", "wt", newline="") as f:
            w = csv.writer(f)
            w.writerow(["t", "mid", "spread", "bidsz1", "asksz1", "imb1", "imb5", "imb10"])
            w.writerows(rows)
        print(name, len(rows), "rows")


if __name__ == "__main__":
    main()
