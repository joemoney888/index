"""Test 2 (pre-registered): where did the old edge go? Split BFG stop exits into GAPPED (the exit bar opened beyond the stop level, so the gap-aware fill is worse than the level) vs CLEAN (touched inside the bar).
Decision rule: if gapped exits are <25% of stop exits but carry >60% of the degradation -> old edge was gap-risk rent concentrated by the vol gate -> close the exit line. If degradation is spread over clean exits -> trail timing dominated.
Also split by entry ATR-ratio tercile if the ratio feature is available. N +0."""
import sys, numpy as np
sys.path.insert(0, "/home/claude/index/ftmo"); sys.path.insert(0, "/home/claude/index")
import ftmo_filters as F, cost_stack as C
from agent import search
d = search.load_arrays("/home/claude/gbpusd-paper-agent/data/bars5/NAS100.csv.gz"); f = search.build_features(d)
mask = F.block_mask(d["t"], ["nfp", "fomc"], 120, False, True); D = C.detail(C.P, d, f, mask, 0, len(d["t"]))
base = D[:, 7]; gap = C.net_R(D, d, gap=True); stopm = D[:, 6] == 0; diff = base - gap
gapped = stopm & (diff > 1e-12); clean = stopm & ~gapped
print(f"trades {len(D)}  base mean {base.mean():+.4f}R  gap-aware mean {gap.mean():+.4f}R  total degradation/trade {diff.mean():.4f}R")
print(f"stop exits {stopm.sum()} ({stopm.mean():.1%}); gapped {gapped.sum()} ({gapped.sum()/stopm.sum():.1%} of stop exits, {gapped.mean():.2%} of trades)")
tot = diff.sum(); print(f"degradation share: gapped {diff[gapped].sum()/tot:.1%}  clean {diff[clean].sum()/tot:.1%}  (clean is 0 by construction in the 5-min sim; the 1-min sim adds the trail-timing part)")
print("mean R gapped exits: base %+.3f -> gap %+.3f" % (base[gapped].mean(), gap[gapped].mean()))
print("keys with ratio?", [k for k in f if "atr" in k.lower() or "ratio" in k.lower()])
