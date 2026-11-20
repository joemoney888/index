import sys, numpy as np, json
sys.path.insert(0,"ftmo"); sys.path.insert(0,".")
import ftmo_filters as F
from agent import search
p=json.load(open("search/NAS100/finalists.json"))[0]["p"]
d=search.load_arrays("/home/claude/gbpusd-paper-agent/data/bars5/NAS100.csv.gz"); f=search.build_features(d)
v0,e0=search.split_points(int(d["t"][-1])); iv=int(np.searchsorted(d["t"],v0)); ie=int(np.searchsorted(d["t"],e0))
m=F.block_mask(d["t"],["nfp","fomc"],120,False,True)
for seg,(lo,hi) in {"val+exam":(iv,len(d["t"])),"exam":(ie,len(d["t"]))}.items():
    tr=F.run("D",d,f,p,m,lo,hi); R=tr[:,1]
    run=best=0; w=0; ws=0
    for r in R:
        run=run+1 if r<0 else 0; best=max(best,run)
    cs=np.cumsum(R); dd=(np.maximum.accumulate(cs)-cs).max()
    day=(tr[:,0]//86400).astype(int); u,inv=np.unique(day,return_inverse=True); ds=np.bincount(inv,weights=R)
    print(f"{seg}: n={len(R)} win%={100*(R>0).mean():.0f} longest losing run={best} worst day={ds.min():.2f}R worst 5 days={np.sort(ds)[:5].round(2)} max drawdown={dd:.1f}R days/yr traded={len(u)}")
    for lim in (None,1.5,2,3):
        keep=[];cur=None;s=0
        for t,r in tr:
            dk=int(t//86400)
            if dk!=cur: cur=dk;s=0
            if lim is not None and s<=-lim: continue
            keep.append(r); s+=r
        k=np.array(keep); print(f"   daily stop {lim}R: n={len(k)} mean {k.mean():+.3f}R total {k.sum():.0f}R")
