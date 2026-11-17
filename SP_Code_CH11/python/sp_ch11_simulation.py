"""SP_CH11 — simulate the continuous-time machine process and a renewal process (Example 11.20, Exercise 11.19).
Usage: python sp_ch11_simulation.py             (fraction of time in W,S,M over 20,000 shifts)
       python sp_ch11_simulation.py --jumps     (fraction of jumps into each state = jump-chain stationary law)
       python sp_ch11_simulation.py --renewal   (10,000 Weibull tire lives: replacements per year)"""
import sys, numpy as np; sys.path.insert(0,__file__.rsplit('/',1)[0])
from sp_ch11_ctmc import *
from scipy.stats import weibull_min
rng=np.random.default_rng(121)
if "--renewal" in sys.argv:
    L=weibull_min.rvs(2.5,scale=12,size=10000,random_state=rng); print(f"mean life {L.mean():.2f} months; replacements per year per tire {12/L.mean():.3f} (1.127)")
else:
    t,s=simulate_ctmc(Q3,0,20000,rng)
    if "--jumps" in sys.argv: print("fraction of jumps into W,S,M:",(np.bincount(s[1:],minlength=3)/len(s[1:])).round(3))
    else:
        dur=np.diff(t); print("fraction of time in W,S,M:",np.round([dur[s[:-1]==k].sum()/t[-1] for k in range(3)],3),"pi:",stationary_Q(Q3).round(3))
