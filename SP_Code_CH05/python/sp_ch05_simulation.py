"""SP_CH05 — simulations: mixture variance (Example 5.12), CLT (Exercise 5.19a), binomial tail (Exercise 5.19b).
Usage: python sp_ch05_simulation.py [--mixture | --clt | --binom]"""
import sys, numpy as np
rng=np.random.default_rng(5)
if "--clt" in sys.argv:
    for n in (2,10,50):
        m=rng.exponential(1,(20000,n)).mean(axis=1); print(f"n={n:2d}: mean {m.mean():.3f}, sd {m.std():.3f} (theory {1/np.sqrt(n):.3f}), skewness {((m-m.mean())**3).mean()/m.std()**3:.2f}")
elif "--binom" in sys.argv:
    x=rng.binomial(600,0.23,20000); print(f"P(X>=150) simulated {(x>=150).mean():.3f}")
else:
    rain=rng.random(20000)<0.3; p=np.where(rain,0.40,0.157); x=rng.binomial(12,p)
    print(f"mixture: mean {x.mean():.3f} (2.76), variance {x.var():.3f} (law of total variance: 3.76)")
