"""Pure strategy logic: no network, no clock. Easy to test."""
import math
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Optional
from zoneinfo import ZoneInfo

from .config import Config

CANDLE_MINUTES = 15


@dataclass(frozen=True)
class Candle:
    start: datetime  # timezone-aware, UTC
    open: float
    high: float
    low: float
    close: float
    complete: bool
    volume: int = 0  # tick volume (OANDA does not give real volume for CFDs)
    spread: float = 0.0  # closing ask minus bid, when the candle was fetched with bid/ask (0 = unknown)

    @property
    def end(self) -> datetime:
        return self.start + timedelta(minutes=CANDLE_MINUTES)


@dataclass(frozen=True)
class OpeningRange:
    high: float
    low: float
    pips: float  # width of the range, in pips (FX) or points (indices)


@dataclass(frozen=True)
class Signal:
    side: str  # "long" or "short"
    candle_start: datetime
    candle_end: datetime
    close: float


@dataclass(frozen=True)
class OrderPlan:
    side: str
    units: float  # signed: positive = buy, negative = sell
    entry: float
    stop: float
    target: float
    stop_pips: float
    risk_gbp: float


def _minutes(t) -> int:
    return t.hour * 60 + t.minute


def opening_range(candles, day: date, cfg: Config) -> Optional[OpeningRange]:
    """High and low of the opening range on `day`, or None if it is not complete yet."""
    tz = ZoneInfo(cfg.tz)
    expected = (_minutes(cfg.range_end) - _minutes(cfg.range_start)) // CANDLE_MINUTES
    picked = []
    for c in candles:
        local = c.start.astimezone(tz)
        if (
            c.complete
            and local.date() == day
            and cfg.range_start <= local.time() < cfg.range_end
        ):
            picked.append(c)
    if len(picked) != expected:
        return None
    high = max(c.high for c in picked)
    low = min(c.low for c in picked)
    return OpeningRange(high=high, low=low, pips=(high - low) / cfg.pip)


def find_signal(
    candles, rng: OpeningRange, day: date, cfg: Config, after: Optional[datetime] = None
) -> Optional[Signal]:
    """First completed 15-minute candle after the range that closes outside it.

    `after`: ignore candles that finished at or before this time (used so a trade
    that has already been taken is not triggered again by the same candle).
    """
    tz = ZoneInfo(cfg.tz)
    for c in sorted(candles, key=lambda x: x.start):
        local = c.start.astimezone(tz)
        if not c.complete or local.date() != day:
            continue
        if local.time() < cfg.range_end or local.time() > cfg.last_entry_candle_start:
            continue
        if after is not None and c.end <= after:
            continue
        if c.close > rng.high:
            return Signal("long", c.start, c.end, c.close)
        if c.close < rng.low:
            return Signal("short", c.start, c.end, c.close)
    return None


def _floor(x: float, places: int) -> float:
    f = 10 ** places
    return math.floor(x * f + 1e-9) / f


def build_order(side: str, rng: OpeningRange, entry: float, cfg: Config, gbpusd: float):
    """Return (plan, reason). plan is None when the trade should be skipped.

    `gbpusd` is the current GBP/USD rate, used to turn the pound risk into dollars
    (both GBPUSD and the Nasdaq 100 are priced in dollars).
    """
    stop = rng.low if side == "long" else rng.high
    risk_dist = (entry - stop) if side == "long" else (stop - entry)
    if risk_dist <= 0:
        return None, "price is already beyond the stop level"
    stop_pips = risk_dist / cfg.pip
    stop_frac = risk_dist / entry
    if stop_frac < cfg.min_stop_frac:
        return None, f"stop too tight ({stop_pips:.1f} {cfg.unit_label})"
    if stop_frac > cfg.max_stop_frac:
        return None, f"stop too wide ({stop_pips:.1f} {cfg.unit_label})"

    target = entry + cfg.reward_risk * risk_dist if side == "long" else entry - cfg.reward_risk * risk_dist
    risk_gbp = cfg.virtual_equity_gbp * cfg.risk_fraction
    risk_usd = risk_gbp * gbpusd
    raw_units = risk_usd / risk_dist
    # Margin cap: the position's dollar value may not exceed virtual equity x leverage.
    cap_units = cfg.virtual_equity_gbp * cfg.leverage * gbpusd / entry
    units = _floor(min(raw_units, cap_units), cfg.units_precision)
    if units < cfg.min_units:
        return None, "position size is below the minimum"
    if cfg.units_precision == 0:
        units = int(units)
    signed = units if side == "long" else -units
    d = cfg.price_decimals
    return (
        OrderPlan(
            side=side,
            units=signed,
            entry=round(entry, d),
            stop=round(stop, d),
            target=round(target, d),
            stop_pips=round(stop_pips, 1),
            risk_gbp=round(risk_gbp, 2),
        ),
        "",
    )
