"""Free proxy for the gamma regime test: negative gamma ~ high/rising volatility, positive gamma ~ calm. Split BFG (FTMO filters) trades by prior-day range vs its 20-day average and by 5-day vs 60-day realised vol. Also the power calculation."""
import sys, json, numpy as np
sys.path.insert(0,"ftmo"); sys.path.insert(0,".")
import ftmo_filters as F
from agent import search
p=json.load(open("search/NAS100/finalists.json"))[0]["p"]
d=search.load_arrays("/home/claude/gbpusd-paper-agent/data/bars5/NAS100.csv.gz"); f=search.build_features(d)
t=d["t"]; v0,e0=search.split_points(int(t[-1])); iv=int(np.searchsorted(t,v0)); ie=int(np.searchsorted(t,e0))
m=F.block_mask(t,["nfp","fomc"],120,False,True)
day=t//86400; u,idx=np.unique(day,return_index=True)
hi=np.maximum.reduceat(d["h"],idx); lo=np.minimum.reduceat(d["l"],idx); cl=d["c"][np.r_[idx[1:]-1,len(t)-1]]
rng=(hi-lo)/cl
avg20=np.array([rng[max(0,i-20):i].mean() if i>=20 else np.nan for i in range(len(rng))])
prev=np.r_[np.nan,rng[:-1]]; ratio=prev/np.r_[np.nan,avg20[:-1]]
r1=dict(zip(u,ratio))
for nm,(lo_i,hi_i) in {"val+exam (2y)":(iv,len(t)),"exam (1y)":(ie,len(t))}.items():
    tr=F.run("D",d,f,p,m,lo_i,hi_i); rr=np.array([r1.get(int(x//86400),np.nan) for x in tr[:,0]]); ok=~np.isnan(rr)
    med=np.nanmedian(rr); hi_m=ok&(rr>=med); lo_m=ok&(rr<med)
    a,b=search.day_t(tr[hi_m]),search.day_t(tr[lo_m])
    se=np.hypot(abs(a['mean']/a['t']) if a['t'] else 0, abs(b['mean']/b['t']) if b['t'] else 0)
    print(f"{nm}: after HIGH-vol day n={a['n']} {a['mean']:+.3f}R (t {a['t']:.2f}) | after CALM day n={b['n']} {b['mean']:+.3f}R (t {b['t']:.2f}) | diff {a['mean']-b['mean']:+.3f}R, se {se:.3f}, z {(a['mean']-b['mean'])/se:.2f}")
sd=0.58; 
for n in (650,1300):
    se_=sd/np.sqrt(n/2)*np.sqrt(2)*1.3   # x1.3 for day clustering
    print(f"power: {n} trades/yr split 50/50 -> se of difference ~{se_:.3f}R; need ~{2.8*se_:.3f}R difference for 80% power")
