"""SP_CH10 — long-run toolkit (importable): stationary distribution, classes, period, long-run cost, PageRank."""
import numpy as np, sys; sys.path.insert(0,__file__.rsplit('/',1)[0])
from sp_ch09_markov import P2,P3,W,nstep,hitting_time
def stationary(P):
    n=P.shape[0]; A=np.vstack([P.T-np.eye(n),np.ones(n)]); b=np.r_[np.zeros(n),1]; return np.linalg.lstsq(A,b,rcond=None)[0]
def reachable(P):
    n=P.shape[0]; R=(P>0)|np.eye(n,dtype=bool)
    for _ in range(n): R=R|(R@R)
    return R
def classes(P):
    R=reachable(P); n=P.shape[0]; seen=set(); out=[]
    for i in range(n):
        if i in seen: continue
        cl=[j for j in range(n) if R[i,j] and R[j,i]]; seen|=set(cl); closed=all(not R[j,k] or k in cl for j in cl for k in range(n)); out.append((cl,"recurrent" if closed else "transient"))
    return out
def period(P,i):
    from math import gcd; g=0
    for n in range(1,4*P.shape[0]+1):
        if nstep(P,n)[i,i]>1e-12: g=gcd(g,n)
    return g
def longrun_cost(P,c): return stationary(P)@np.asarray(c)
def pagerank(links,n,d=0.85):
    M=np.zeros((n,n))
    for i,ls in links.items():
        for j in ls: M[i,j]=1/len(ls)
    return stationary(d*M+(1-d)/n)
