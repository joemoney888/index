import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import index_run


class Fake:
    def closed_trades_raw(self, count=50):
        return [{"id": "6", "instrument": "NAS100_USD", "price": "27694.2", "averageClosePrice": "27618.6", "initialUnits": "-0.04", "openTime": "a", "closeTime": "b",
                 "realizedPL": "1.01", "financing": "0.0", "closingTransactionIDs": ["99"]},
                {"id": "77", "instrument": "NAS100_USD", "price": "1", "closingTransactionIDs": []}]       # 77 is not ours: never logged

    def transaction(self, tid):
        return {"reason": "STOP_LOSS_ORDER", "price": "27618.6", "fullPrice": {"bids": [{"price": "27618.0"}], "asks": [{"price": "27619.0"}]}}


def test_logs_only_our_closed_trades_once(tmp_path, monkeypatch):
    log = tmp_path / "events.csv"
    monkeypatch.setattr(index_run, "LOG", str(log))
    index_run.log("NAS100", "order_placed", {"key": "k", "trade_id": "6"})      # written by the real logger, so the CSV quoting is the real one
    index_run.log_closed_trades(Fake()); index_run.log_closed_trades(Fake())
    rows = [l for l in log.read_text().splitlines() if "trade_closed" in l]
    assert len(rows) == 1 and "STOP_LOSS_ORDER" in rows[0] and "27618.6" in rows[0] and '"77"' not in rows[0]


def test_never_raises(tmp_path, monkeypatch):
    class Bad:
        def closed_trades_raw(self, count=50): raise RuntimeError("boom")
    monkeypatch.setattr(index_run, "LOG", str(tmp_path / "e.csv"))
    index_run.log_closed_trades(Bad())
