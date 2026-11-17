"""SP_CH08 — discrete-event simulation of M/M/c (Example 8.23, Exercises 8.18–8.19).
Usage: python sp_ch08_simulation.py                 (M/M/5, λ=3, μ=2/3, 1,000,000 calls, seed 88)
       python sp_ch08_simulation.py --mm1            (M/M/1, λ=0.5, μ=2/3, 100,000 calls)
       python sp_ch08_simulation.py --mm1 --deterministic   (M/D/1, service = 1.5 min)
       python sp_ch08_simulation.py --abandon        (M/M/5 with 10% of callers leaving after 2 min)"""
import sys, numpy as np
rng=np.random.default_rng(88); A=sys.argv
if "--mm1" in A: lam,mu,c,n,warm=0.5,2/3,1,100000,10000
else: lam,mu,c,n,warm=3.0,2/3,5,1000000,100000
arr=np.cumsum(rng.exponential(1/lam,n)); serv=np.full(n,1/mu) if "--deterministic" in A else rng.exponential(1/mu,n)
patience=np.where(rng.random(n)<0.10,2.0,np.inf) if "--abandon" in A else np.full(n,np.inf)
free=np.zeros(c); wq=np.full(n,np.nan); left=np.zeros(n,bool)
for i in range(n):
    k=np.argmin(free); start=max(arr[i],free[k]); w=start-arr[i]
    if w>patience[i]: left[i]=True; continue
    wq[i]=w; free[k]=start+serv[i]
served=~left; w=wq[warm:][served[warm:]]
print(f"served {served.mean():.3f}   abandoned {left.mean():.3f}")
print(f"Wq (served): mean {w.mean():.3f} min = {w.mean()*60:.1f} s    P(wait>0) {(w>0).mean():.3f}")
