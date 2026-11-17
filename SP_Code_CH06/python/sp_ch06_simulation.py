"""SP_CH06 — simulate sample paths of the cash random walk (Example 6.21, Exercise 6.19).
Usage: python sp_ch06_simulation.py              (±1000, p=0.5, 20 days, seed 65)
       python sp_ch06_simulation.py --r4          (R4: start 20,000, p=0.55, 60 days; first-passage below 10,000)"""
import sys, numpy as np
rng=np.random.default_rng(65)
if "--r4" in sys.argv:
    steps=np.where(rng.random((10000,60))<0.55,1000,-1000); paths=20000+np.cumsum(steps,axis=1)
    print(f"day 60: mean {paths[:,-1].mean():.0f} (26,000)  sd {paths[:,-1].std():.0f} (7,707)")
    print(f"below 10,000 at day 60: {(paths[:,-1]<10000).mean():.3f}   below 10,000 at some point during the 60 days: {(paths.min(axis=1)<10000).mean():.3f}")
else:
    steps=np.where(rng.random((10000,20))<0.5,1000,-1000); paths=np.cumsum(steps,axis=1)
    print(f"day 20: mean {paths[:,-1].mean():.0f} (0)  sd {paths[:,-1].std():.0f} (4,472)  P(>5000) {(paths[:,-1]>5000).mean():.3f} (0.13)")
