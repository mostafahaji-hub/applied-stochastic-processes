"""SP_CH03 — Example 3.28 / Exercise 3.19: simulate 12 vans for many days and compare with B(12, p).
Usage: python sp_ch03_simulation.py [n_vans] [p] [days] [seed] [--rain]
Book numbers: 12 0.23 10000 12  ->  mean 2.777, var 2.141, P(X=0) 0.043, P(X>3) 0.298
--rain: 30% rainy days with p=0.40, dry days p=0.157 (Table 1.3) -> same mean, larger variance."""
import sys, numpy as np
from scipy.stats import binom
args=[a for a in sys.argv[1:] if not a.startswith("--")]; rain="--rain" in sys.argv
n=int(args[0]) if len(args)>0 else 12; p=float(args[1]) if len(args)>1 else 0.23
days=int(args[2]) if len(args)>2 else 10000; seed=int(args[3]) if len(args)>3 else 12
rng=np.random.default_rng(seed)
if rain:
    is_rain=rng.random(days)<0.30; pday=np.where(is_rain,0.40,0.157)
else:
    pday=np.full(days,p)
late=rng.binomial(n,pday)                       # number of late vans each day
print(f"simulated mean {late.mean():.3f}   variance {late.var():.3f}   P(X=0) {(late==0).mean():.3f}   P(X>3) {(late>3).mean():.3f}")
print(f"binomial B({n},{p}):  mean {n*p:.3f}   variance {n*p*(1-p):.3f}   P(X=0) {binom.pmf(0,n,p):.3f}   P(X>3) {1-binom.cdf(3,n,p):.3f}")
