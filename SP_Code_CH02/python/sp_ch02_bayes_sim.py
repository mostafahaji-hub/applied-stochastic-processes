"""SP_CH02 — Example 2.17: Monte Carlo check of Bayes' rule for the parcel scanner.
Usage: python sp_ch02_bayes_sim.py [base_rate] [sensitivity] [false_alarm] [N] [seed]
Book numbers: 0.03 0.95 0.08 100000 22  ->  posterior ≈ 0.268 (Bayes: 0.269)"""
import sys, numpy as np
a=[float(x) for x in sys.argv[1:4]] or [0.03,0.95,0.08]
base,sens,fp=(a+[0.03,0.95,0.08])[:3]
N=int(sys.argv[4]) if len(sys.argv)>4 else 100000; seed=int(sys.argv[5]) if len(sys.argv)>5 else 22
rng=np.random.default_rng(seed)
defective=rng.random(N)<base                                   # true state of each parcel
flagged=np.where(defective, rng.random(N)<sens, rng.random(N)<fp)   # scanner result given state
print(f"flagged parcels: {flagged.sum()}   defective among flagged: {defective[flagged].mean():.4f}")
print(f"Bayes' rule:     {base*sens/(base*sens+(1-base)*fp):.4f}")
