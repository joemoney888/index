from datetime import datetime, timedelta, timezone

import pytest

from agent import ctrader
from agent.oanda import PermanentError

OLD = datetime(2026, 1, 5, 10, 0, tzinfo=timezone.utc)


class Fake:
    is_demo = True

    def __init__(self):
        self.pos = [{"id": 7, "symbol": "US100", "side": -1, "units": 0.04, "price": 27694.2, "open_ms": int(OLD.timestamp() * 1000), "stop_loss": 27838.8, "take_profit": 27509.1}]
        self.calls = []

    def trendbars(self, symbol, pm, f, t):
        now = datetime.now(timezone.utc).replace(second=0, microsecond=0)
        cur = now - timedelta(minutes=now.minute % 5)                    # the bar that is still open
        old = int((cur - timedelta(minutes=5)).timestamp() * 1000)
        return [{"utc_ms": int(OLD.timestamp() * 1000), "open": 1.0, "high": 2.0, "low": 0.5, "close": 1.5, "volume": 10},
                {"utc_ms": int(OLD.timestamp() * 1000), "open": 1.0, "high": 2.0, "low": 0.5, "close": 1.5, "volume": 10},   # duplicate dropped
                {"utc_ms": int(cur.timestamp() * 1000), "open": 9, "high": 9, "low": 9, "close": 9, "volume": 1}]            # in progress: dropped

    def quote(self, symbol):
        return 100.0, 100.4

    def positions(self):
        return list(self.pos)

    def market_order(self, symbol, side, units, stop, tp):
        self.calls.append(("order", symbol, side, units, stop, tp))
        return {"filled": True, "position_id": "55", "price": 27680.5}

    def amend(self, pid, stop, tp):
        self.calls.append(("amend", pid, stop, tp))

    def close(self, pid, units):
        self.calls.append(("close", pid, units))


def mk():
    return ctrader.CTraderBroker(Fake(), {"NAS100_USD": "US100"})


def test_demo_only():
    f = Fake()
    f.is_demo = False
    with pytest.raises(RuntimeError):
        ctrader.CTraderBroker(f, {"NAS100_USD": "US100"})


def test_candles_complete_unique_utc():
    cs = mk().get_candles_range("NAS100_USD", OLD - timedelta(days=1), datetime.now(timezone.utc) + timedelta(minutes=1), "M5")
    assert len(cs) == 1 and cs[0].start == OLD and cs[0].complete and cs[0].close == 1.5


def test_open_trades_signed_units_and_names():
    t = mk().open_trades()[0]
    assert t.instrument == "NAS100_USD" and t.units == -0.04 and t.stop_loss == 27838.8 and t.open_time == OLD


def test_place_order_side_precision():
    b = mk()
    r = b.place_order("NAS100_USD", -0.04, 27838.84, 27509.07, 1, 2)
    assert r == {"filled": True, "trade_id": "55", "price": 27680.5}
    assert b.transport.calls[-1] == ("order", "US100", -1, 0.04, 27838.8, 27509.1)


def test_move_stop_keeps_target_and_close_full_size():
    b = mk()
    b.move_stop("7", 27618.64, 1)
    assert b.transport.calls[-1] == ("amend", "7", 27618.6, None)
    b.close_trade("7")
    assert b.transport.calls[-1] == ("close", "7", 0.04)
    with pytest.raises(PermanentError):
        b.close_trade("999")


def test_pricing_and_unknown_symbol():
    b = mk()
    assert b.get_pricing("NAS100_USD").spread == pytest.approx(0.4)
    with pytest.raises(PermanentError):
        b.get_pricing("XYZ_USD")
