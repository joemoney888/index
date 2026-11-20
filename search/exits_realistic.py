"""PRE-REGISTERED (20 Nov 2026, before any result): do any simple exits keep a positive edge under REALISTIC fills?
Entries: the BFG signal exactly as fitted (search/NAS100/finalists.json weights, theta 0.47, hours 13-21, 20-day trend, ATR-expanding gate), NOT re-searched, no FTMO filters. Entry at the next 5-min open +/- half the 5-min spread (as before).
Exits re-simulated on 1-MINUTE bars with realistic fills: stop fills at the minute's open when it opens beyond the stop (bid/ask aware); target fills at the limit; stop wins if both touch in one minute; time exit at that minute's close -/+ half spread. NO trailing stop (the trailing stop was the idealisation).
Family (175 variants): stop ks in {1.0,1.5,2.0,2.5,3.0} x ATR; target kt in {1,1.5,2,3,4,6,none} x ATR; time exit H in {12,24,48,96,192} 5-min bars. ATR = mean 5-min true range over 24 h, as in the engine. One position at a time.
Splits (1-minute data 2023-11-19..2026-11-19): TRAIN = first ~365 d, VALIDATION = next 365 d, EXAM = last 365 d: LOCKED, not loaded here.
Candidate: TRAIN n>=300, mean R >= +0.03 and day-clustered t >= sqrt(2 ln 175)+0.5 = 3.71 (own family). Also reported against the cumulative bar (N = 941,367 + 175). Finalist: VALIDATION mean >= +0.03R and t >= 2.0 with >=150 trades. Only finalists may go to a single exam. These 175 variants are added to the global N."""
import sys, json, math, numpy as np
sys.path.insert(0, "/home/claude/index")
from agent import search
d5 = search.load_arrays("/home/claude/gbpusd-paper-agent/data/bars5/NAS100.csv.gz"); f = search.build_features(d5)
d1 = search.load_arrays("/home/claude/gbpusd-paper-agent/data/bars1/NAS100.csv.gz"); t1, t5 = d1["t"], d5["t"]
P = json.load(open("/home/claude/index/search/NAS100/finalists.json"))[0]["p"]
KS, KT, HS = [1.0, 1.5, 2.0, 2.5, 3.0], [1.0, 1.5, 2.0, 3.0, 4.0, 6.0, None], [12, 24, 48, 96, 192]
tl = int(t1[-1]); exam0 = tl - 365 * 86400; val0 = exam0 - 365 * 86400
w = np.array(P["w"]); score = f["F"] @ w / np.abs(w).sum() * 2
ok = (np.abs(score) >= P["theta"]) & (f["hour"] >= P["h0"]) & (f["hour"] < P["h1"]) & f["valid"] & (np.sign(score) == f["trend"]) & f["gates"][P["gate"]]
cand = np.flatnonzero(ok); cand = cand[(t5[cand + 1] >= t1[0] + 86400) & (t5[cand + 1] < exam0 - 192 * 300)]   # exam never touched
print(f"{len(cand)} candidate signal bars before the exam window", flush=True)
MAXM = max(HS) * 5; rows = []
for i in cand:
    side = float(np.sign(score[i])); a = f["atr"][i]
    if not a > 0: continue
    e = d5["o"][i + 1] + side * d5["s"][i] / 2; j0 = int(np.searchsorted(t1, t5[i + 1]))
    if j0 + MAXM >= len(t1): continue
    hi, lo, op, cl, hs = d1["h"][j0:j0 + MAXM], d1["l"][j0:j0 + MAXM], d1["o"][j0:j0 + MAXM], d1["c"][j0:j0 + MAXM], d1["s"][j0:j0 + MAXM] / 2
    stop_idx, stop_fill, tgt_idx = {}, {}, {}
    for ks in KS:
        lv = e - side * ks * a
        hit = (lo - hs <= lv) if side > 0 else (hi + hs >= lv)
        k = int(np.argmax(hit)) if hit.any() else MAXM
        stop_idx[ks] = k
        if k < MAXM: stop_fill[ks] = min(lv, op[k] - hs[k]) if side > 0 else max(lv, op[k] + hs[k])
    for kt in KT:
        if kt is None: tgt_idx[kt] = MAXM; continue
        lv = e + side * kt * a
        hit = (hi - hs >= lv) if side > 0 else (lo + hs <= lv)
        tgt_idx[kt] = int(np.argmax(hit)) if hit.any() else MAXM
    tm = {H: (cl[H * 5 - 1] - side * hs[H * 5 - 1]) for H in HS}
    rows.append((int(t5[i + 1]), int(i), side, e, a, stop_idx, stop_fill, tgt_idx, tm))
print(f"{len(rows)} candidates with 1-minute paths", flush=True)
def day_t(tr):
    r = search.day_t(np.array(tr)) if len(tr) else {"n": 0, "mean": 0.0, "t": 0.0}; return r
res = []
for ks in KS:
    for kt in KT:
        for H in HS:
            free = -1; trs = []
            for (te, i, side, e, a, sidx, sfill, tidx, tm) in rows:
                if te < free: continue
                risk = ks * a; k_s, k_t = sidx[ks], tidx[kt]; lim = H * 5 - 1
                if k_s <= lim and k_s <= k_t: ex, n = sfill[ks], k_s
                elif k_t <= lim: ex, n = e + side * kt * a, k_t
                else: ex, n = tm[H], lim
                trs.append((te, side * (ex - e) / risk)); free = te + (n + 1) * 60
            tr = np.array(trs); a_ = tr[tr[:, 0] < val0]; b_ = tr[tr[:, 0] >= val0]
            res.append({"ks": ks, "kt": kt, "H": H, "train": day_t(a_), "val": day_t(b_)})
N = len(res); bar = math.sqrt(2 * math.log(N)) + 0.5; barc = math.sqrt(2 * math.log(941367 + N)) + 0.5
best = sorted(res, key=lambda r: -r["train"]["t"])
cands = [r for r in res if r["train"]["n"] >= 300 and r["train"]["mean"] >= 0.03 and r["train"]["t"] >= bar]
fin = [r for r in cands if r["val"]["n"] >= 150 and r["val"]["mean"] >= 0.03 and r["val"]["t"] >= 2.0]
avg = np.mean([r["train"]["t"] for r in res])
L = ["# Realistic-fill exit search (pre-registered 20 Nov 2026; train and validation only; exam LOCKED)", "",
     f"Variants N = {N} (added to the global ledger: cumulative N = {941367 + N:,}). Own-family luck bar = {bar:.2f}; cumulative-N bar = {barc:.2f}. Average TRAIN t over all variants: {avg:.2f}.",
     f"Candidates passing the own-family bar: **{len(cands)}**. Finalists (validation gate): **{len(fin)}**. Candidates under the cumulative bar: **{len([r for r in res if r['train']['n']>=300 and r['train']['t']>=barc])}**.", "",
     "Top 10 by TRAIN t (n>=300 shown first):", ""]
for r in [x for x in best if x["train"]["n"] >= 300][:10]:
    L.append(f"- ks {r['ks']} kt {r['kt']} H {r['H']}: train n={r['train']['n']} mean {r['train']['mean']:+.3f}R t {r['train']['t']:.2f} | validation n={r['val']['n']} mean {r['val']['mean']:+.3f}R t {r['val']['t']:.2f}")
open("/home/claude/index/search/EXITS/RESULT.md", "w").write("\n".join(L) + "\n"); json.dump(res, open("/home/claude/index/search/EXITS/runs_1.json", "w"))
print("\n".join(L))
