import csv,random,math,sys
R=list(csv.DictReader(open('data.csv')))
y=[int(r['year']) for r in R]; s=[float(r['spx'])/100 for r in R]; b=[float(r['bill'])/100 for r in R]; bo=[float(r['bond'])/100 for r in R]
def tr(cost):
    out=[];prev=(s[0]>b[0]);
    for i in range(len(y)):
        if i==0: out.append(None);continue
        inn=s[i-1]>b[i-1]
        r=s[i] if inn else b[i]
        if inn!=prev: r-=cost
        prev=inn;out.append(r)
    return out
n=len(y)
BH=s[1:];SB=[.6*s[i]+.4*bo[i] for i in range(1,n)]
def cagr(r):return math.exp(sum(math.log(1+x) for x in r)/len(r))-1
def mdd(r):
    v=1;pk=1;m=0
    for x in r:
        v*=1+x;pk=max(pk,v);m=min(m,v/pk-1)
    return m
def sh(r,rf):
    e=[a-c for a,c in zip(r,rf)];m=sum(e)/len(e);sd=(sum((x-m)**2 for x in e)/(len(e)-1))**.5;return m/sd
rf=b[1:]
def boot(d,B=10000,bl=5,seed=1):
    random.seed(seed);m=len(d);res=[]
    for _ in range(B):
        t=[];
        while len(t)<m:
            st=random.randrange(m);L=1
            while random.random()>1/bl:L+=1
            t+= [d[(st+k)%m] for k in range(L)]
        t=t[:m];res.append(sum(t)/m)
    res.sort();return res[int(.025*B)],res[int(.975*B)]
for cost in (.001,.005):
    T=tr(cost)[1:]
    d=[a-c for a,c in zip(T,BH)]
    h=len(d)//2
    print(f"cost {cost}: CAGR TR {cagr(T):.4f} BH {cagr(BH):.4f} diff {cagr(T)-cagr(BH):+.4f} meandiff {sum(d)/len(d):+.4f} CI {boot(d)} halves CAGRdiff {cagr(T[:h])-cagr(BH[:h]):+.4f} {cagr(T[h:])-cagr(BH[h:]):+.4f}")
    print(f"  maxDD TR {mdd(T):.3f} BH {mdd(BH):.3f} 6040 {mdd(SB):.3f}; Sharpe TR {sh(T,rf):.2f} BH {sh(BH,rf):.2f} 6040 {sh(SB,rf):.2f}; switches {sum(1 for i in range(1,len(T)) if (s[i]>b[i])!=(s[i-1]>b[i-1]))}; in-market {sum(1 for i in range(n-1) if s[i]>b[i])/(n-1):.2f}")
print(f"CAGR BH {cagr(BH):.4f} 6040 {cagr(SB):.4f}; vol BH {(sum((x-sum(BH)/len(BH))**2 for x in BH)/(len(BH)-1))**.5:.3f}")
