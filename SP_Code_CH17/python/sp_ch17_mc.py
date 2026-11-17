"""SP_CH17 — Monte Carlo basics (importable): generators, inverse transform, acceptance–rejection,
estimation with standard errors, sample size, variance reduction (antithetic, control variates, CRN)."""
import numpy as np
from scipy.stats import norm, weibull_min
from scipy.special import gamma
def lcg(a,c,m,x0,n):
    out=[x0]; x=x0
    for _ in range(n): x=(a*x+c)%m; out.append(x)
    return out
def period(a,c,m,x0):
    seen={}; x=x0; k=0
    while x not in seen: seen[x]=k; x=(a*x+c)%m; k+=1
    return k-seen[x]
def hull_dobell(a,c,m):
    from math import gcd
    def pf(n):
        f=set(); d=2
        while d*d<=n:
            while n%d==0: f.add(d); n//=d
            d+=1
        if n>1: f.add(n)
        return f
    return gcd(c,m)==1 and all((a-1)%p==0 for p in pf(m)) and ((a-1)%4==0 if m%4==0 else True)
exp_inv=lambda u,mean: -mean*np.log(1-u)
weib_inv=lambda u,k,eta: eta*(-np.log(1-u))**(1/k)
def discrete_inv(u,values,probs):
    cdf=np.cumsum(probs); return np.asarray(values)[np.searchsorted(cdf,u,side="right")]
def accept_reject_beta22(rng,n):
    out=[]; tries=0
    while len(out)<n:
        u1,u2=rng.random(),rng.random(); tries+=1
        if u2<=4*u1*(1-u1): out.append(u1)
    return np.array(out),tries
def mc_mean(x,z=1.96):
    x=np.asarray(x,float); m=x.mean(); se=x.std(ddof=1)/np.sqrt(len(x)); return m,se,(m-z*se,m+z*se)
def n_needed(sigma,half_width,z=1.96): return int(np.ceil((z*sigma/half_width)**2))
TIRE_K,TIRE_ETA=2.5,12.0
TIRE_MEAN=TIRE_ETA*gamma(1+1/TIRE_K); TIRE_SD=TIRE_ETA*np.sqrt(gamma(1+2/TIRE_K)-gamma(1+1/TIRE_K)**2)
def tire_cost_rate(L,T,cp=80,cf=600):
    """renewal-reward estimate of the age-replacement cost rate from lifetimes L (one cycle per lifetime)."""
    L=np.asarray(L); cyc=np.minimum(L,T); cost=np.where(L<T,cf,cp); return cost.sum()/cyc.sum()
