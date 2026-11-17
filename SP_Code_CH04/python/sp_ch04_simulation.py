"""SP_CH04 — simulations for Example 4.24 and Exercise 4.19.
Usage: python sp_ch04_simulation.py            (demand N(500,80), 20,000 days, seed 44)
       python sp_ch04_simulation.py --exp       (20,000 exponential waits with mean 2 min; fraction > 4.6 min)
       python sp_ch04_simulation.py --clt       (20,000 sums of 12 uniforms: mean, sd — a bell shape)"""
import sys, numpy as np
rng=np.random.default_rng(44)
if "--exp" in sys.argv:
    t=rng.exponential(2.0,20000); print(f"fraction of waits > 4.6 min: {(t>4.6).mean():.3f}   (theory e^-2.3 = {np.exp(-2.3):.3f})")
elif "--clt" in sys.argv:
    s=rng.random((20000,12)).sum(axis=1); print(f"sum of 12 uniforms: mean {s.mean():.3f} (6), sd {s.std():.3f} (1.000); fraction within ±1 sd: {((s>5)&(s<7)).mean():.3f} (normal: 0.683)")
else:
    D=rng.normal(500,80,20000); print(f"simulated daily demand: mean {D.mean():.1f}  sd {D.std():.1f}  P(D>600) {(D>600).mean():.3f}   (theory 0.106)")
