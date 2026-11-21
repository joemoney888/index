"""Read-only: list every instrument the second practice account can trade (counts by type, plus index CFDs). Places no orders. Prints no account id or token."""
import collections, os, json
from agent import oanda
c = oanda.OandaPractice(os.environ["OANDA_API_TOKEN_INDEX"], os.environ["OANDA_ACCOUNT_ID_INDEX"])
ins = c._request("GET", f"/v3/accounts/{c.account}/instruments")["instruments"]
by = collections.Counter(i["type"] for i in ins)
print("total instruments:", len(ins), dict(by))
idx = sorted(i["name"] for i in ins if i["name"].endswith(("_USD", "_EUR", "_GBP", "_JPY", "_HKD", "_AUD", "_CHF", "_CAD", "_SGD")) and i["type"] == "CFD" and any(k in i["name"] for k in ("NAS", "SPX", "US30", "UK100", "DE30", "GER", "JP225", "EU50", "FR40", "AU200", "HK33", "US2000", "CN50", "NL25", "SG30", "TWIX", "IN50")))
print("index CFDs:", idx)
cf = collections.Counter(i.get("displayName", "").split()[-1] if i["type"] == "CFD" else "" for i in ins if i["type"] == "CFD")
print("sample CFD names:", [i["name"] for i in ins if i["type"] == "CFD"][:40])
open("instruments_summary.json", "w").write(json.dumps({"total": len(ins), "by_type": by, "index_cfds": idx}, indent=1))
