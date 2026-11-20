"""ONE-TIME exam of the finalists on the locked final 365 days. Refuses to run twice (search/exam.json). Writes search/EXAM.md."""
import glob
import json
import os
import sys

import numpy as np

from agent import search


def main():
    want = {m.strip().upper() for m in os.environ.get("MARKETS", "").split(",") if m.strip()}
    out = os.environ.get("SEARCH_DIR", "search")
    if os.path.exists(f"{out}/exam.json"):
        sys.exit("exam already used; it cannot be run again")
    fin = json.load(open(f"{out}/finalists.json"))
    if not fin:
        sys.exit("no finalists")
    mk = {}
    scalp = os.environ.get("SCALP") == "1"
    for p in sorted(glob.glob("data/bars1/*.csv.gz" if scalp else "data/bars5/*.csv.gz")):
        if want and os.path.basename(p).split(".")[0] not in want:
            continue
        d = search.load_arrays(p)
        _, exam0 = search.split_points(int(d["t"][-1]))
        mk[os.path.basename(p).split(".")[0]] = (d, search.build_features(d, 1440 if scalp else 288), int(np.searchsorted(d["t"], exam0)))
    res, L = [], ["# One-time exam (locked final 365 days)", ""]
    for c in fin:
        tr = [search.trades(c["p"], d, f, e0, len(d["t"])) for d, f, e0 in mk.values()]
        ex = search.day_t(np.vstack([x for x in tr if len(x)]) if any(len(x) for x in tr) else np.empty((0, 2)))
        ok = search.exam_pass(ex)
        tag = "PASS" if ok else ("SHADOW-WORTHY" if search.shadow_worthy(ex) else "FAIL")
        res.append({"p": c["p"], "exam": ex, "pass": ok})
        L.append(f"- {tag}: exam mean {ex['mean']:+.3f}R, t {ex['t']:.2f}, n={ex['n']} | train t {c['train']['t']:.2f}, validation t {c['val']['t']:.2f} | {c['p']}")
    json.dump(res, open(f"{out}/exam.json", "w"))
    open(f"{out}/EXAM.md", "w").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
