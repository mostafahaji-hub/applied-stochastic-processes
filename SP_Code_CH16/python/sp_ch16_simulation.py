"""SP_CH16 v2 — textbook Keshtel algorithm on R6 (random keys).
Usage: --trace (Tables 16.1–16.3, seed 24) | --runs (30 runs, seed 162) | --ablation (seed 16, 2,000 runs each)
       --groups (seed 161, 2,000 runs) | --toy N2 (barrier landscape, seed 1617) | --smax S (3,000 runs, seed 16)"""
import sys, numpy as np; sys.path.insert(0,__file__.rsplit('/',1)[0])
from sp_ch16_ka import *
A=sys.argv
def stat(rng,R,**kw):
    fh=[];s=0
    for _ in range(R):
        o=ka_run(rng,**kw); s+=o['first'] is not None
        if o['first'] is not None: fh.append(o['first'])
    fh=np.array(fh); return s/R,float(np.mean(fh<=100))*s/R,float(fh.mean())
if "--trace" in A:
    P0,o,tr,new,moves,P,fv=hand_trace(24)
    for t in tr: print(t[0],'neighbor',int(o[t[1]])+1,np.round(t[2],3),label(decode(t[2])),int(t[3]),'better' if t[4] else 'not better')
    for oi,k,f in new: print('landing for',int(oi)+1,k,label(decode(k)),f)
    for m in moves: print('move',int(m[0])+1,'toward',int(m[1])+1,int(m[2])+1,'alpha',m[3],label(decode(m[4])),m[5],'->',m[6])
    print('new population',fv,'mean',round(fv.mean(),2))
elif "--runs" in A:
    rng=np.random.default_rng(162); fh=[o['first'] for o in (ka_run(rng,Smax=2) for _ in range(30)) if o['first'] is not None]; print(len(fh),'of 30; mean',round(np.mean(fh),1),'median',np.median(fh))
elif "--ablation" in A:
    rng=np.random.default_rng(16)
    for name,kw in [('full',{}),('N1=0',dict(N1=0,N2=3)),('N2=0',dict(N1=2,N2=0)),('N3=0',dict(N1=2,N2=8)),('N2 only',dict(N1=0,N2=10))]: print(name,np.round(stat(rng,2000,Smax=2,**kw),3))
elif "--groups" in A:
    rng=np.random.default_rng(161); imp=np.zeros(4); fg=np.zeros(4)
    for _ in range(2000):
        o=ka_run(rng,Smax=2)
        for g in o['groups']: imp[g]+=1
        if o['first'] is not None and o['groups']: fg[o['groups'][-1]]+=1
    print('improvements lucky/unlucky/remaining',np.round(imp[1:]/imp[1:].sum(),3),' first discovery',np.round(fg[1:]/fg[1:].sum(),3))
elif "--toy" in A:
    n2=int(A[A.index("--toy")+1]); rng=np.random.default_rng(1617); fs=[ka_toy(rng,N2=n2,Smax=2) for _ in range(2000)]; ok=[f for f in fs if f is not None]
    print(f"N2 = {n2}: success {len(ok)/2000:.4f}"+(f", mean {np.mean(ok):.1f}" if ok else ""))
elif "--smax" in A:
    s=int(A[A.index("--smax")+1]); print('Smax',s,np.round(stat(np.random.default_rng(16),3000,Smax=s),3))
else: print(__doc__)
