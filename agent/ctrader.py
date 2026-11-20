"""cTrader broker adapter with the same methods as OandaPractice, so the NAS100 runner can later use an FTMO (or any cTrader) DEMO account.
The network layer is a small Transport interface (one object that speaks the cTrader Open API); this file holds everything else and is fully tested with a fake transport.
NOT YET CONNECTED to any real account. Things to confirm on the real demo account are marked TODO(confirm).
DEMO ONLY: the adapter refuses any transport that is not flagged as a demo connection."""
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Protocol

from .oanda import PermanentError, Quote, Trade
from .strategy import Candle

PERIOD_MINUTES = {"M1": 1, "M5": 5, "M15": 15, "H1": 60}


class Transport(Protocol):
    is_demo: bool

    def trendbars(self, symbol: str, period_minutes: int, from_ms: int, to_ms: int) -> List[dict]:
        """Bars as dicts: utc_ms (bar open time), open, high, low, close, volume. Prices already decoded to floats. (cTrader trendbars are BID prices.)"""

    def quote(self, symbol: str) -> tuple:
        """(bid, ask) now."""

    def positions(self) -> List[dict]:
        """Open positions: id, symbol, side (+1 buy, -1 sell), units, price, open_ms, stop_loss (or None), take_profit (or None)."""

    def market_order(self, symbol: str, side: int, units: float, stop: float, take_profit: float) -> dict:
        """Returns {filled: bool, position_id: str, price: float, reason: str}."""

    def amend(self, position_id: str, stop: Optional[float], take_profit: Optional[float]) -> None:
        """Replace stop/target on an open position (values not given are left as they are)."""

    def close(self, position_id: str, units: float) -> None:
        ...


@dataclass
class CTraderBroker:
    transport: Transport
    symbols: Dict[str, str]              # our name or OANDA name -> broker symbol, e.g. {"NAS100_USD": "US100"}  TODO(confirm FTMO symbol name)

    def __post_init__(self):
        if not getattr(self.transport, "is_demo", False):
            raise RuntimeError("Refusing to run: the cTrader connection is not marked as a DEMO account.")

    def _sym(self, instrument: str) -> str:
        if instrument not in self.symbols:
            raise PermanentError(f"No broker symbol mapped for {instrument}")
        return self.symbols[instrument]

    # ---- data ----
    def get_candles_range(self, instrument: str, start: datetime, end: datetime, granularity: str = "M5", page: int = 5000, price: str = "M") -> List[Candle]:
        """Completed bars from start up to end. A bar still in progress is dropped. Spread is unknown for historical bars (0.0); cTrader bars are bid-based (TODO(confirm) effect on the rule: features are relative, so small)."""
        pm = PERIOD_MINUTES[granularity]
        raw = self.transport.trendbars(self._sym(instrument), pm, int(start.timestamp() * 1000), int(end.timestamp() * 1000))
        now = datetime.now(timezone.utc)
        out, seen = [], set()
        for b in raw:
            t = datetime.fromtimestamp(b["utc_ms"] / 1000, timezone.utc)
            if t >= end or t in seen or t + timedelta(minutes=pm) > now:
                continue
            seen.add(t)
            out.append(Candle(start=t, open=float(b["open"]), high=float(b["high"]), low=float(b["low"]), close=float(b["close"]),
                              complete=True, volume=int(b.get("volume", 0)), spread=0.0))
        return sorted(out, key=lambda c: c.start)

    def get_pricing(self, instrument: str) -> Quote:
        bid, ask = self.transport.quote(self._sym(instrument))
        return Quote(bid=float(bid), ask=float(ask))

    # ---- account ----
    def open_trades(self) -> List[Trade]:
        rev = {v: k for k, v in self.symbols.items()}
        out = []
        for p in self.transport.positions():
            if p["symbol"] not in rev:
                continue
            out.append(Trade(id=str(p["id"]), instrument=rev[p["symbol"]], open_time=datetime.fromtimestamp(p["open_ms"] / 1000, timezone.utc), close_time=None,
                             units=float(p["side"]) * float(p["units"]), price=float(p["price"]), realized_pl=0.0,
                             stop_loss=float(p["stop_loss"]) if p.get("stop_loss") else None))
        return out

    def place_order(self, instrument: str, units: float, stop: float, target: float, decimals: int, units_precision: int) -> dict:
        side = 1 if units > 0 else -1
        res = self.transport.market_order(self._sym(instrument), side, round(abs(units), units_precision), round(stop, decimals), round(target, decimals))
        if res.get("filled"):
            return {"filled": True, "trade_id": str(res["position_id"]), "price": float(res["price"])}
        return {"filled": False, "reason": res.get("reason", "unknown")}

    def close_trade(self, trade_id: str) -> None:
        for p in self.transport.positions():
            if str(p["id"]) == str(trade_id):
                self.transport.close(str(trade_id), float(p["units"]))
                return
        raise PermanentError(f"Position {trade_id} not found")

    def move_stop(self, trade_id: str, price: float, decimals: int) -> None:
        self.transport.amend(str(trade_id), round(price, decimals), None)       # target left as it is
