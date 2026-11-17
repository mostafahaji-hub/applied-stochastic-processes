"""
SP_CH01 — Level 1: Why Randomness Matters
Monte Carlo illustration of probability as a long-run frequency (Example 1.24, Exercise 1.17).
Usage:  python sp_ch01_simulation.py [p] [n] [seed]
Reproduces the numbers in the book: p=0.30, n=1000, seed=7  ->  0.200 (n=10), 0.310 (n=100), 0.307 (n=1000)
"""
import sys, numpy as np
def running_frequency(p=0.30, n=1000, seed=7):
    rng = np.random.default_rng(seed)
    late = (rng.random(n) < p).astype(int)          # 1 = late day, 0 = on time
    return np.cumsum(late) / np.arange(1, n + 1)     # fraction of late days after each day
if __name__ == "__main__":
    p = float(sys.argv[1]) if len(sys.argv) > 1 else 0.30
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 7
    r = running_frequency(p, n, seed)
    for k in [10, 100, 1000, 2000]:
        if k <= n: print(f"after {k:5d} days: fraction late = {r[k-1]:.4f}")
