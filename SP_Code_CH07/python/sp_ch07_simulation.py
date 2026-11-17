"""SP_CH07 — simulate a Poisson process from exponential gaps (Example 7.24, Exercise 7.19).
Usage: python sp_ch07_simulation.py           (rate 3/min, count N(5), 10,000 runs, seed 77)
       python sp_ch07_simulation.py --nhpp    (rate 2 for 5 min then 4 for 5 min; fraction of arrivals in the first half)"""
import sys, numpy as np
rng=np.random.default_rng(77); lam=3.0
if "--nhpp" in sys.argv:
    # thinning method: simulate at max rate 4, keep each arrival with prob lambda(t)/4
    tot=[]; first=[]
    for _ in range(5000):
        s=np.cumsum(rng.exponential(1/4,120)); s=s[s<=10]; keep=rng.random(len(s))<np.where(s<5,0.5,1.0); a=s[keep]
        tot.append(len(a)); first.append((a<5).sum())
    tot=np.array(tot); first=np.array(first); print(f"N(10): mean {tot.mean():.2f} (30)   fraction in first half {first.sum()/tot.sum():.3f} (1/3, not 1/2)")
else:
    counts=np.array([(np.cumsum(rng.exponential(1/lam,60))<=5).sum() for _ in range(10000)])
    print(f"N(5): mean {counts.mean():.2f} (15)  var {counts.var():.2f} (15)  P(N=12) {(counts==12).mean():.3f} (0.083)")
