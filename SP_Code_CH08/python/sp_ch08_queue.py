"""SP_CH08 — queueing formulas used throughout Chapter 8 (importable)."""
import numpy as np
from math import factorial
def mm1(lam,mu):
    r=lam/mu; L=r/(1-r); Lq=r*r/(1-r); W=1/(mu-lam); Wq=r/(mu-lam); return dict(rho=r,L=L,Lq=Lq,W=W,Wq=Wq,Pwait=r)
def mm1k(lam,mu,K):
    r=lam/mu; p=np.array([r**n for n in range(K+1)]); p=p/p.sum(); L=(np.arange(K+1)*p).sum(); lam_eff=lam*(1-p[K]); Lq=L-lam_eff/mu; W=L/lam_eff; Wq=Lq/lam_eff
    return dict(rho=r,p=p,pK=p[K],lam_eff=lam_eff,L=L,Lq=Lq,W=W,Wq=Wq)
def mmc(lam,mu,c):
    a=lam/mu; r=a/c
    if r>=1: return None
    s=sum(a**n/factorial(n) for n in range(c)); p0=1/(s+a**c/factorial(c)/(1-r)); C=(a**c/factorial(c))*p0/(1-r)  # Erlang C = P(wait)
    Lq=C*r/(1-r); Wq=Lq/lam; W=Wq+1/mu; L=lam*W
    return dict(a=a,rho=r,p0=p0,Pwait=C,Lq=Lq,Wq=Wq,W=W,L=L)
def pwait_gt(lam,mu,c,t):
    q=mmc(lam,mu,c); return q["Pwait"]*np.exp(-(c*mu-lam)*t)
def erlangB(a,c):
    num=a**c/factorial(c); den=sum(a**n/factorial(n) for n in range(c+1)); return num/den
def mg1(lam,mu,sigma):
    r=lam/mu; Lq=(lam**2*sigma**2+r**2)/(2*(1-r)); Wq=Lq/lam; return dict(rho=r,Lq=Lq,Wq=Wq,W=Wq+1/mu,L=Lq+r)
def finite_source(N,lam_each,mu):
    # single repairman, N machines, each fails at rate lam_each when working
    p=[1.0]
    for n in range(1,N+1): p.append(p[-1]*(N-n+1)*lam_each/mu)
    p=np.array(p); p=p/p.sum(); L=(np.arange(N+1)*p).sum(); lam_eff=lam_each*(N-L); W=L/lam_eff; Lq=L-(1-p[0]); Wq=Lq/lam_eff
    return dict(p=p,L=L,lam_eff=lam_eff,W=W,Lq=Lq,Wq=Wq,util=1-p[0])
