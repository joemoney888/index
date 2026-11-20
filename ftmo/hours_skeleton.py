"""(1) BFG mean R by entry hour. (2) price-only version of the 'pullback to discount + bullish reversal' setup on NAS100 5-min, with BFG's real-spread simulation style (1R=stop)."""
import sys, json, numpy as np
sys.path.insert(0,"ftmo"); sys.path.insert(0,".")
import ftmo_filters as F
from agent import search
p=json.load(open("search/NAS100/finalists.json"))[0]["p"]
d=search.load_arrays("/home/claude/gbpusd-paper-agent/data/bars5/NAS100.csv.gz"); f=search.build_features(d)
t=d["t"]; v0,e0=search.split_points(int(t[-1])); iv=int(np.searchsorted(t,v0)); ie=int(np.searchsorted(t,e0))
m=F.block_mask(t,["nfp","fomc"],120,False,True)
print("== BFG (FTMO filters) mean R by UTC entry hour, val+exam / exam")
for nm,(lo,hi) in {"val+exam":(iv,len(t)),"exam":(ie,len(t))}.items():
    tr=F.run("D",d,f,p,m,lo,hi); h=((tr[:,0]%86400)//3600).astype(int)
    print(nm, " ".join(f"{k}h:{tr[h==k,1].mean():+.3f}(n{(h==k).sum()})" for k in range(13,21) if (h==k).sum()))
# (2) skeleton: first 90 min after the 14:30 UTC (winter) / 13:30 (summer) US cash open -> use bars 13:30-15:30 UTC window broadly; daily trend = close > close 5 days ago (higher-TF up)
import datetime as dt
from zoneinfo import ZoneInfo
NY=ZoneInfo("America/New_York")
o,h_,l,c,s=d["o"],d["h"],d["l"],d["c"],d["s"]; n=len(t)
def run(lo,hi,side_both=True,tgt="swing",RR=None):
    out=[]; free=-1
    atr=f["atr"]
    for i in range(lo+300,hi-80):
        if i<free: continue
        ts=int(t[i]); lt=dt.datetime.fromtimestamp(ts,NY)
        mins=lt.hour*60+lt.minute
        if not (9*60+30<=mins<=11*60): continue
        if np.isnan(atr[i]) or atr[i]<=0: continue
        trend=f["trend"][i]                    # 20-day trend sign
        if trend==0: continue
        k=trend
        # swing over last 78 bars (~6.5h): low->high for up trend
        seg_h,seg_l=h_[i-78:i+1],l[i-78:i+1]
        sh,sl=seg_h.max(),seg_l.min(); rng=sh-sl
        if rng<2*atr[i]: continue
        if k>0:
            z_hi,z_lo=sh-0.705*rng,sh-0.886*rng
            inz=l[i]<=z_hi and l[i]>=z_lo*1.0 - 0   # wick into zone
            conf=(c[i]>o[i]) and (c[i-1]<o[i-1]) and l[i]>=sl           # bullish flip after bearish bar, zone not broken
            if not(inz and conf): continue
            e=o[i+1]+s[i]/2; stop=l[i]-0.1*atr[i]; risk=e-stop; tg=sh
            if risk<=0 or tg<=e: continue
            hh,ll=h_[i+1:i+1+78],l[i+1:i+1+78]
            js=np.argmax(ll-s[i]/2<=stop) if (ll-s[i]/2<=stop).any() else 99999
            jt=np.argmax(hh-s[i]/2>=tg) if (hh-s[i]/2>=tg).any() else 99999
            if js==99999 and jt==99999: ex=c[i+78]-s[i]/2; nb=77
            elif js<=jt: ex,nb=stop,js
            else: ex,nb=tg,jt
            out.append((ts,(ex-e)/risk)); free=i+2+nb
        else:
            z_lo,z_hi=sl+0.705*rng,sl+0.886*rng
            inz=h_[i]>=z_lo and h_[i]<=z_hi
            conf=(c[i]<o[i]) and (c[i-1]>o[i-1]) and h_[i]<=sh
            if not(inz and conf): continue
            e=o[i+1]-s[i]/2; stop=h_[i]+0.1*atr[i]; risk=stop-e; tg=sl
            if risk<=0 or tg>=e: continue
            hh,ll=h_[i+1:i+1+78],l[i+1:i+1+78]
            js=np.argmax(hh+s[i]/2>=stop) if (hh+s[i]/2>=stop).any() else 99999
            jt=np.argmax(ll+s[i]/2<=tg) if (ll+s[i]/2<=tg).any() else 99999
            if js==99999 and jt==99999: ex=c[i+78]+s[i]/2; nb=77
            elif js<=jt: ex,nb=stop,js
            else: ex,nb=tg,jt
            out.append((ts,(e-ex)/risk)); free=i+2+nb
    return np.array(out) if out else np.empty((0,2))
print("\n== price-only skeleton (with 20d trend, 0.705-0.886 zone, flip candle, NY 9:30-11:00, target swing extreme)")
for nm,(lo,hi) in {"train":(0,iv),"val":(iv,ie),"exam":(ie,n)}.items():
    tr=run(lo,hi); r=search.day_t(tr); print(nm,r, f"win%={100*(tr[:,1]>0).mean():.0f}" if len(tr) else "")
