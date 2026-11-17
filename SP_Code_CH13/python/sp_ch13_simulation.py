"""SP_CH13 — simulations for Chapter 13.
Usage: python sp_ch13_simulation.py [--start X]   (R4 cash: P(touch -10 within 90 days) with several monitoring frequencies)
       python sp_ch13_simulation.py --qv            (quadratic variation of one path for n = 10, 100, 10,000)
       python sp_ch13_simulation.py --gbm           (Euler–Maruyama for the fuel price, Example 13.19)
       python sp_ch13_simulation.py --ou            (Euler–Maruyama for OU demand: stationary mean and SD)"""
import sys, numpy as np; sys.path.insert(0,__file__.rsplit('/',1)[0])
from sp_ch13_brownian import *
A=sys.argv; mu,s=MU_R4,SIG_R4
if "--qv" in A:
    rng=np.random.default_rng(1306); N=10000; dW=rng.standard_normal(N)*np.sqrt(1/N)
    for n in (10,100,10000): inc=dW.reshape(n,-1).sum(axis=1); print(f"n = {n:6d}:  sum of squared increments = {(inc**2).sum():.4f}   (theory 1 ± {np.sqrt(2/n):.3f})")
elif "--gbm" in A:
    rng=np.random.default_rng(1319); S=euler_maruyama(lambda x:0.04*x,lambda x:0.25*x,1.6,1.0,1/250,10000,rng); g=gbm_stats(1.6,0.04,0.25,1)
    print(f"Euler–Maruyama: mean {S.mean():.3f} (theory {g['mean']:.3f})  P(S>2) {(S>2).mean():.3f} (theory {gbm_prob_above(1.6,0.04,0.25,1,2):.3f})  q95 {np.quantile(S,0.95):.2f} (theory {g['q95']:.2f})")
elif "--ou" in A:
    th=-np.log(0.6); rng=np.random.default_rng(1320); X=euler_maruyama(lambda x:-th*(x-500),lambda x:50*np.sqrt(2*th)+0*x,500,50,0.01,20000,rng)
    print(f"OU after 50 days: mean {X.mean():.1f} (500)  SD {X.std():.1f} (50)")
else:
    x0=float(A[A.index("--start")+1]) if "--start" in A else 5.0; a=x0+10; rng=np.random.default_rng(1311)
    for dt,N,lab in ((1.0,400000,"daily"),(0.25,200000,"every 6 h"),(0.05,100000,"every 1.2 h"),(0.02,50000,"every 29 min")):
        print(f"{lab:13s}: {hit_freq(x0,-10,mu,s,90,dt,N,rng,chunk=5000):.4f}   (barrier-shift approximation {p_hit_below(a+0.5826*s*np.sqrt(dt),mu,s,90):.4f})")
    print(f"continuous formula: {p_hit_below(a,mu,s,90):.4f}")
