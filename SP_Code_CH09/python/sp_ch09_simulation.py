"""SP_CH09 — simulate Markov chains (Example 9.19, Exercise 9.19).
Usage: python sp_ch09_simulation.py            (10,000 Silver customers for 24 months)
       python sp_ch09_simulation.py --lifetime (simulate until churn: mean months, fraction ever Platinum)
       python sp_ch09_simulation.py --weather  (10,000 days of the weather chain)"""
import sys, numpy as np; sys.path.insert(0,__file__.rsplit('/',1)[0])
from sp_ch09_markov import *
rng=np.random.default_rng(93)
if "--lifetime" in sys.argv:
    months=[]; plat=0
    for _ in range(10000):
        s=0; n=0; seen=False
        while s!=3: s=int(np.searchsorted(np.cumsum(P3[s]),rng.random())); n+=1; seen|=(s==2)
        months.append(n); plat+=seen
    print(f"mean months {np.mean(months):.2f} (7.5)   fraction ever Platinum {plat/10000:.3f} (0.143)")
elif "--weather" in sys.argv:
    path=simulate(W,0,10000,rng); print(f"fraction rainy days {np.mean(np.array(path)==0):.3f} (0.298)")
else:
    state=np.zeros(10000,int); cum=np.cumsum(P3,axis=1)
    for m in range(24): u=rng.random(10000); state=np.array([np.searchsorted(cum[s],u[i]) for i,s in enumerate(state)])
    print("after 24 months:",(np.bincount(state,minlength=4)/10000).round(3),"theory",nstep(P3,24)[0].round(3))
