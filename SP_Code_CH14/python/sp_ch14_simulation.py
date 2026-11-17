"""SP_CH14 — simulated annealing on R6 (and on the barrier landscape).
Usage: python sp_ch14_simulation.py --trace          (Table 14.2: eight hand-traceable steps at T = 3, seed 0)
       python sp_ch14_simulation.py --runs           (30 runs from the start sequence, T0 = 10, alpha = 0.95, 100 iterations, seed 149)
       python sp_ch14_simulation.py --toy ALPHA      (success rate on the barrier landscape, 10,000 runs, T0 = 10, 300 iterations)
       python sp_ch14_simulation.py --stationary T   (exact stationary law of the 720-state chain vs Boltzmann)"""
import sys, numpy as np; sys.path.insert(0,__file__.rsplit('/',1)[0])
from sp_ch14_sa import *
A=sys.argv
if "--trace" in A:
    rng=np.random.default_rng(0); x=START
    for k in range(8):
        r1=round(rng.random(),2); r2=round(rng.random(),2); m=min(int(5*r1),4); y=NA[x][m]; d=int(F[y]-F[x]); p=min(1.0,np.exp(-d/3)); acc=d<=0 or r2<p
        print(f"{k+1}: {label(STATES[x])} ({F[x]})  r1={r1:.2f} -> swap {m+1}-{m+2}: {label(STATES[y])} ({F[y]})  delta={d:+d}  p={p:.3f}  r2={r2:.2f}  {'accept' if acc else 'reject'}")
        if acc: x=y
    print("end:",label(STATES[x]),F[x])
elif "--runs" in A:
    rng=np.random.default_rng(149); res=[run_sa_adj(START,10,0.95,100,rng) for _ in range(30)]
    fh=[r[4] for r in res]; print("successes:",sum(F[r[3]]==11 for r in res),"of 30;  first hit: mean",np.mean(fh).round(1),"median",np.median(fh),"min",min(fh),"max",max(fh))
elif "--toy" in A:
    a=float(A[A.index("--toy")+1]); rng=np.random.default_rng(1416); ok=np.mean([run_sa_toy(10,a,300,rng)[1]==11 for _ in range(10000)])
    print(f"alpha = {a}: success rate {ok:.3f} (T after 300 iterations = {10*a**300:.4f})")
elif "--stationary" in A:
    T=float(A[A.index("--stationary")+1]); pi=stationary(metropolis_adj(T)); b=boltzmann(T)
    print(f"T = {T}: max |pi - Boltzmann| = {np.abs(pi-b).max():.2e};  P(optimum) = {b[OPT].sum():.4f};  E[f] = {(b*F).sum():.2f}")
else: print(__doc__)
