"""Strategy and safety settings. Everything tunable lives here, in one place.

Each instrument is one Config. `strategies()` returns the list the agent runs.
"""
import os
from dataclasses import dataclass, replace
from datetime import time
from typing import List


@dataclass(frozen=True)
class Config:
    name: str = "GBPUSD"           # label used in the log, alerts and skip_days.txt
    instrument: str = "GBP_USD"    # OANDA instrument name
    granularity: str = "M15"
    tz: str = "Europe/London"      # all times below are in this time zone

    # Opening range: the first 30 minutes of the session (two 15-minute candles).
    range_start: time = time(8, 0)
    range_end: time = time(8, 30)
    # Last candle (by start time) that may trigger an entry.
    last_entry_candle_start: time = time(14, 45)
    # Any open trade is closed at this time.
    close_time: time = time(16, 30)
    # The agent ignores runs outside this window.
    window_start: time = time(7, 50)
    window_end: time = time(16, 45)

    reward_risk: float = 1.5
    # How an open trade is managed: "fixed" (stop and target never move), "be" (stop to breakeven at +1R)
    # or "trail" (breakeven, then the stop follows 1R behind; target cap 3R). See agent/exits.py.
    exit_mode: str = "fixed"

    # A virtual GBP account so the experiment is realistic. The OANDA practice
    # account usually holds far more, so sizing ignores its real balance.
    virtual_equity_gbp: float = 500.0
    risk_fraction: float = 0.01   # 1% of virtual equity = 5 pounds per trade
    leverage: int = 30            # UK retail cap: 30:1 on major FX, 20:1 on major indices

    # Skip the trade if the stop is closer or further than this, as a fraction of price.
    min_stop_frac: float = 0.0006   # about 8 pips on GBPUSD
    max_stop_frac: float = 0.0038   # about 50 pips on GBPUSD

    max_trades_per_day: int = 2
    max_losses_per_day: int = 2          # for this instrument
    # Global rules, across every instrument on the account (UK calendar day). Live orders only.
    max_total_trades_per_day: int = 4
    max_consecutive_losses: int = 2      # stop for the day after this many losing trades in a row
    max_signal_age_minutes: int = 20     # ignore a signal that is older than this

    pip: float = 0.0001           # size of one "pip" (one point for indices)
    unit_label: str = "pips"
    price_decimals: int = 5
    units_precision: int = 0      # decimal places allowed in the position size
    min_units: float = 1.0

    quote_ccy: str = "USD"        # currency the price is quoted in: USD, GBP or JPY (turns £ risk into units)
    trend_filter: bool = False    # only take a breakout in the direction of the 20-day average of daily closes
    score: float = 0.0            # ranking when signals arrive together: higher goes first (see strategies())

    dry_run: bool = True          # True means log signals, never place orders
    trading_enabled: bool = True  # False is the kill switch


def strategies() -> List[Config]:
    dry = os.environ.get("DRY_RUN", "true").strip().lower() != "false"
    enabled = os.environ.get("TRADING_ENABLED", "true").strip().lower() != "false"
    mode = os.environ.get("EXIT_MODE", "fixed").strip().lower()
    if mode not in ("fixed", "be", "trail"):
        mode = "fixed"
    gbpusd = Config(dry_run=dry, trading_enabled=enabled, exit_mode=mode, score=-0.083)
    # Nasdaq 100: the US cash open is 09:30 New York time. Using New York time keeps
    # the rule right in the weeks when UK and US clocks change on different dates.
    nas100 = Config(
        name="NAS100",
        instrument="NAS100_USD",
        tz="America/New_York",
        range_start=time(9, 30),
        range_end=time(10, 0),
        last_entry_candle_start=time(11, 45),
        close_time=time(15, 45),
        window_start=time(9, 20),
        window_end=time(16, 5),
        leverage=20,
        min_stop_frac=0.0015,
        max_stop_frac=0.015,
        pip=1.0,
        unit_label="points",
        price_decimals=1,
        units_precision=2,
        min_units=0.01,
        dry_run=dry,
        trading_enabled=enabled,
        exit_mode=mode,
        score=0.025,
    )
    # Nasdaq 100 morning breakout (London session): a research strategy added after the backtest.
    # It shares the NAS100_USD instrument with the afternoon rule above, and the live trade counting
    # is per instrument, so the two would interfere if real paper orders were placed. Until that is
    # solved it is locked to dry run, whatever DRY_RUN says.
    nas100_am = Config(
        name="NAS100_AM",
        instrument="NAS100_USD",
        tz="Europe/London",
        range_start=time(8, 0),
        range_end=time(8, 30),
        last_entry_candle_start=time(11, 45),
        close_time=time(14, 15),
        window_start=time(7, 50),
        window_end=time(14, 25),
        leverage=20,
        min_stop_frac=0.0015,
        max_stop_frac=0.015,
        pip=1.0,
        unit_label="points",
        price_decimals=1,
        units_precision=2,
        min_units=0.01,
        dry_run=True,
        trading_enabled=enabled,
    )
    out = [gbpusd, nas100, nas100_am] + _more_instruments(dry, enabled, mode)
    # Variable DRY_ONLY (comma list of strategy names) keeps those in dry run even when DRY_RUN is false.
    forced = {x.strip().upper() for x in os.environ.get("DRY_ONLY", "").split(",") if x.strip()}
    out = [replace(c, dry_run=True) if c.name.upper() in forced else c for c in out]
    # Variable LIMITS=off removes every daily trade and loss limit (per instrument and global) so the practice account collects as much data as possible.
    # Default is "on": 2 trades and 2 losses per instrument, 4 trades a day and a stop after 2 losses in a row across the account. Use "on" for real money.
    if os.environ.get("LIMITS", "on").strip().lower() == "off":
        out = [replace(c, max_trades_per_day=999, max_losses_per_day=999, max_total_trades_per_day=999, max_consecutive_losses=999) for c in out]
    # Signals that arrive together are handled best-first: the strategies run in score order.
    return sorted(out, key=lambda c: -c.score)


# Scores for ranking = the average of the earlier-two-thirds and last-third average R in reports/discovery_report.md
# (the existing three use their numbers from reports/backtest_report.md). They are noisy: a tie-break, not a forecast.
def _more_instruments(dry: bool, enabled: bool, mode: str) -> List[Config]:
    fx = dict(leverage=30, min_stop_frac=0.0006, max_stop_frac=0.0038, units_precision=0, min_units=1.0)
    cfd = dict(leverage=20, min_stop_frac=0.0010, max_stop_frac=0.015, pip=1.0, unit_label="points")
    ny_early = dict(tz="America/New_York", range_start=time(8, 30), range_end=time(9, 0),
                    last_entry_candle_start=time(11, 45), close_time=time(15, 45),
                    window_start=time(8, 20), window_end=time(16, 5))
    ny_open = dict(tz="America/New_York", range_start=time(9, 30), range_end=time(10, 0),
                   last_entry_candle_start=time(11, 45), close_time=time(15, 45),
                   window_start=time(9, 20), window_end=time(16, 5))
    london = dict(tz="Europe/London", range_start=time(8, 0), range_end=time(8, 30),
                  last_entry_candle_start=time(11, 45), close_time=time(16, 15),
                  window_start=time(7, 50), window_end=time(16, 25))
    common = dict(dry_run=dry, trading_enabled=enabled, exit_mode=mode)
    return [
        Config(name="EURUSD", instrument="EUR_USD", reward_risk=2.0, trend_filter=True, score=-0.029,
               price_decimals=5, **fx, **ny_early, **common),
        # Not the pre-registered Tokyo pick (the agent has no overnight runs): best London variant on the earlier data.
        Config(name="USDJPY", instrument="USD_JPY", reward_risk=2.0, trend_filter=True, score=0.109, quote_ccy="JPY",
               pip=0.01, unit_label="pips", price_decimals=3, **fx, **london, **common),
        Config(name="WTI", instrument="WTICO_USD", reward_risk=2.0, trend_filter=True, score=0.050,
               pip=0.01, unit_label="cents", price_decimals=3, units_precision=0, min_units=1.0,
               leverage=10, min_stop_frac=0.0010, max_stop_frac=0.015, **london, **common),
        Config(name="UK100", instrument="UK100_GBP", reward_risk=2.0, score=-0.038, quote_ccy="GBP",
               price_decimals=1, units_precision=1, min_units=0.1, **cfd, **ny_open, **common),
        Config(name="SPX500", instrument="SPX500_USD", reward_risk=2.0, trend_filter=True, score=0.052,
               price_decimals=1, units_precision=2, min_units=0.01, **cfd, **ny_open, **common),
        Config(name="GOLD", instrument="XAU_USD", reward_risk=2.0, score=-0.095, price_decimals=3,
               units_precision=1, min_units=0.1, **{**cfd, "unit_label": "dollars"}, **ny_early, **common),
        Config(name="SILVER", instrument="XAG_USD", reward_risk=1.5, trend_filter=True, score=-0.071,
               pip=0.01, unit_label="cents", price_decimals=5, units_precision=0, min_units=1.0,
               leverage=10, min_stop_frac=0.0010, max_stop_frac=0.015, **ny_early, **common),
    ]
