"""Minimal OANDA v20 client. PRACTICE ACCOUNTS ONLY: the live server is not wired in."""
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Optional

import time

import requests

from .strategy import Candle

PRACTICE_BASE = "https://api-fxpractice.oanda.com"
TIMEOUT = 15


@dataclass(frozen=True)
class Trade:
    id: str
    instrument: str
    open_time: datetime
    close_time: Optional[datetime]
    units: float
    price: float
    realized_pl: float
    stop_loss: Optional[float] = None   # current stop-loss price on an open trade


@dataclass(frozen=True)
class Quote:
    bid: float
    ask: float

    @property
    def spread(self) -> float:
        return self.ask - self.bid

    @property
    def mid(self) -> float:
        return (self.bid + self.ask) / 2


def parse_time(s: str) -> datetime:
    """OANDA sends nanoseconds, e.g. 2026-11-16T08:15:00.000000000Z."""
    s = s.rstrip("Z")
    if "." in s:
        base, frac = s.split(".")
        s = f"{base}.{frac[:6]}"
    return datetime.fromisoformat(s).replace(tzinfo=timezone.utc)


class PermanentError(RuntimeError):
    """A client error (4xx) that retrying cannot fix."""


RETRY_PAUSE = 2.0


class OandaPractice:
    def __init__(self, token: str, account_id: str):
        token = (token or "").strip()
        account_id = (account_id or "").strip()
        if not token or not account_id:
            raise RuntimeError("OANDA_API_TOKEN and OANDA_ACCOUNT_ID must be set")
        # Practice account ids start with 101-. Live ones start with 001-. Refuse live.
        if not account_id.startswith("101-"):
            raise RuntimeError(
                f"This is not a practice account id (it starts with {account_id[:4]!r}, "
                "practice ids start with '101-'). Refusing to run."
            )
        self.account = account_id
        self.http = requests.Session()
        self.http.headers.update(
            {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        )

    def _request(self, method: str, path: str, **kw):
        """Reads (GET) are retried up to 5 times with a growing pause on timeouts and 5xx errors, so a brief OANDA fault (504) does not fail the run.
        Anything that changes state (orders, stops) keeps the original two attempts with no pause: a 504 on an order can mean it WAS placed."""
        url = f"{PRACTICE_BASE}{path}"
        reads = method.upper() == "GET"
        attempts = 5 if reads else 2
        last = None
        for i in range(attempts):
            try:
                r = self.http.request(method, url, timeout=TIMEOUT, **kw)
                if r.status_code >= 400:
                    if reads and 400 <= r.status_code < 500 and r.status_code != 429:
                        raise PermanentError(f"OANDA {r.status_code}: {r.text[:300]}")     # a bad request will not improve by waiting
                    raise RuntimeError(f"OANDA {r.status_code}: {r.text[:300]}")
                return r.json()
            except PermanentError:
                raise
            except (requests.RequestException, RuntimeError) as e:
                last = e
                if reads and i < attempts - 1:
                    time.sleep(RETRY_PAUSE * (2 ** i))
        raise last

    def get_candles(self, instrument: str, count: int = 80, granularity: str = "M15") -> List[Candle]:
        data = self._request(
            "GET",
            f"/v3/instruments/{instrument}/candles",
            params={"granularity": granularity, "count": count, "price": "M"},
        )
        out = []
        for c in data["candles"]:
            m = c["mid"]
            out.append(
                Candle(
                    start=parse_time(c["time"]),
                    open=float(m["o"]),
                    high=float(m["h"]),
                    low=float(m["l"]),
                    close=float(m["c"]),
                    complete=bool(c["complete"]),
                    volume=int(c.get("volume", 0)),
                )
            )
        return out

    def get_candles_range(self, instrument: str, start: datetime, end: datetime,
                          granularity: str = "M15", page: int = 5000, price: str = "M") -> List[Candle]:
        """Completed candles from `start` up to `end`, fetched page by page (history for backtests).
        price="MBA" also returns bid and ask, which fills Candle.spread with the real closing spread."""
        out, seen = [], set()
        cursor = start
        for _ in range(200):  # hard stop: a runaway loop must never hammer the API
            data = self._request(
                "GET",
                f"/v3/instruments/{instrument}/candles",
                params={"granularity": granularity, "count": page, "price": price,
                        "from": cursor.strftime("%Y-%m-%dT%H:%M:%S.000000000Z")},
            )
            new = 0
            for c in data["candles"]:
                t = parse_time(c["time"])
                if t >= end or not c["complete"] or t in seen:
                    continue
                seen.add(t)
                m = c["mid"]
                sp = float(c["ask"]["c"]) - float(c["bid"]["c"]) if "ask" in c and "bid" in c else 0.0
                out.append(Candle(start=t, open=float(m["o"]), high=float(m["h"]), low=float(m["l"]),
                                  close=float(m["c"]), complete=True, volume=int(c.get("volume", 0)), spread=sp))
                new += 1
            last = parse_time(data["candles"][-1]["time"]) if data["candles"] else None
            if not data["candles"] or new == 0 or last is None or last >= end or last <= cursor:
                break
            cursor = last
        return sorted(out, key=lambda c: c.start)

    def get_book(self, instrument: str, kind: str = "positionBook", time: str = None) -> dict:
        """Read-only: OANDA's order book or position book snapshot (kind 'orderBook' or 'positionBook'); time = ISO for history."""
        params = {"time": time} if time else None
        return self._request("GET", f"/instruments/{instrument}/{kind}", params=params)

    def list_instruments(self) -> list:
        """Every instrument this practice account can trade, with sizing details."""
        data = self._request("GET", f"/v3/accounts/{self.account}/instruments")
        return data["instruments"]

    def get_pricing(self, instrument: str) -> Quote:
        data = self._request(
            "GET", f"/v3/accounts/{self.account}/pricing", params={"instruments": instrument}
        )
        p = data["prices"][0]
        return Quote(bid=float(p["bids"][0]["price"]), ask=float(p["asks"][0]["price"]))

    @staticmethod
    def _trade(t) -> Trade:
        return Trade(
            id=str(t["id"]),
            instrument=t["instrument"],
            open_time=parse_time(t["openTime"]),
            close_time=parse_time(t["closeTime"]) if t.get("closeTime") else None,
            units=float(t["initialUnits"]),
            price=float(t["price"]),
            realized_pl=float(t.get("realizedPL", 0.0)),
            stop_loss=float(t["stopLossOrder"]["price"]) if t.get("stopLossOrder") else None,
        )

    def open_trades(self) -> List[Trade]:
        """Open trades on every instrument."""
        data = self._request("GET", f"/v3/accounts/{self.account}/openTrades")
        return [self._trade(t) for t in data["trades"]]

    def closed_trades(self, count: int = 100) -> List[Trade]:
        """Recently closed trades on every instrument."""
        data = self._request(
            "GET",
            f"/v3/accounts/{self.account}/trades",
            params={"state": "CLOSED", "count": count},
        )
        return [self._trade(t) for t in data["trades"]]

    def closed_trades_raw(self, count: int = 50) -> list:
        """Recently closed trades as OANDA returns them (adds averageClosePrice, closingTransactionIDs, financing). Read only."""
        data = self._request("GET", f"/v3/accounts/{self.account}/trades", params={"state": "CLOSED", "count": count})
        return data["trades"]

    def transaction(self, transaction_id: str) -> dict:
        """One transaction (e.g. the order fill that closed a trade: reason, price, bid/ask at the fill). Read only."""
        return self._request("GET", f"/v3/accounts/{self.account}/transactions/{transaction_id}").get("transaction", {})

    def place_order(self, instrument: str, units: float, stop: float, target: float,
                    decimals: int, units_precision: int) -> dict:
        body = {
            "order": {
                "type": "MARKET",
                "instrument": instrument,
                "units": f"{units:.{units_precision}f}",
                "timeInForce": "FOK",
                "positionFill": "DEFAULT",
                "stopLossOnFill": {"price": f"{stop:.{decimals}f}"},
                "takeProfitOnFill": {"price": f"{target:.{decimals}f}"},
            }
        }
        data = self._request("POST", f"/v3/accounts/{self.account}/orders", json=body)
        if "orderFillTransaction" in data:
            fill = data["orderFillTransaction"]
            opened = fill.get("tradeOpened", {})
            return {"filled": True, "trade_id": str(opened.get("tradeID", "")), "price": float(fill["price"])}
        reason = data.get("orderCancelTransaction", {}).get("reason", "unknown")
        return {"filled": False, "reason": reason}

    def close_trade(self, trade_id: str) -> None:
        self._request(
            "PUT",
            f"/v3/accounts/{self.account}/trades/{trade_id}/close",
            json={"units": "ALL"},
        )

    def move_stop(self, trade_id: str, price: float, decimals: int) -> None:
        """Replace the stop-loss on an open trade. The take-profit is left as it is."""
        self._request(
            "PUT",
            f"/v3/accounts/{self.account}/trades/{trade_id}/orders",
            json={"stopLoss": {"price": f"{price:.{decimals}f}", "timeInForce": "GTC"}},
        )
