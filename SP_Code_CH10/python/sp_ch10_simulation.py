"""SP_CH10 — long-run simulation (Example 10.21, Exercise 10.19).
Usage: python sp_ch10_simulation.py            (10,000 shifts of machine 3)
       python sp_ch10_simulation.py --periodic (period-2 chain: time fraction vs probability at step 10,000)"""
import sys, numpy as np; sys.path.insert(0,__file__.rsplit('/',1)[0])
from sp_ch10_longrun import *
from sp_ch09_markov import simulate
rng=np.random.default_rng(10)
if "--periodic" in sys.argv:
    Pp=np.array([[0,1],[1,0]]); path=np.array(simulate(Pp,0,10000,rng)); print(f"time fraction in state 1: {np.mean(path==0):.3f};  P(state 1 at step 10000 | start 1) = {nstep(Pp,10000)[0,0]:.0f}")
else:
    path=np.array(simulate(P2,0,10000,rng)); print("fractions (W,S,M):",[round(np.mean(path==s),3) for s in range(3)],"pi:",stationary(P2).round(3))
