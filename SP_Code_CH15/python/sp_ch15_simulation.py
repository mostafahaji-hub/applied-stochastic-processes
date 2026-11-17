"""SP_CH15 — genetic algorithm on R6 and the Wright–Fisher model.
Usage: python sp_ch15_simulation.py --trace                       (Tables 15.2–15.3, seed 2)
       python sp_ch15_simulation.py --runs                        (30 runs of the basic GA, seed 158)
       python sp_ch15_simulation.py --ga N G PC PM [--noelite]    (success rate over 2,000 runs)
       python sp_ch15_simulation.py --wf RULE N MU [--elite]       (RULE = neutral | roulette | tournament)
       python sp_ch15_simulation.py --heat                        (heat map of generation 10, 1,000 runs)"""
import sys, numpy as np; sys.path.insert(0,__file__.rsplit('/',1)[0])
from sp_ch15_ga import *
A=sys.argv
POP0=[(0,1,2,3,4,5),(5,4,3,2,1,0),(1,0,3,4,2,5),(0,1,5,3,4,2),(4,2,0,5,1,3),(3,0,1,2,5,4)]
if "--trace" in A:
    rows,new=hand_trace(POP0,np.random.default_rng(2))
    print("elite:",label(new[0]),tardiness(new[0]))
    for i,r in enumerate(rows,1): print(f"child {i}: T1 {r['t1']}  T2 {r['t2']}  r_c {r['rc']}  OX {r['cx']}  r_m {r['rm']}  mut {r['mk']}  ->  {label(r['child'])} ({r['f']})")
    f=[tardiness(s) for s in new]; print("new population:",f,"best",min(f),"mean",round(np.mean(f),2))
elif "--runs" in A:
    rng=np.random.default_rng(158); runs=[ga_run(10,21,0.9,0.2,rng) for _ in range(30)]
    fh=[o["first"] for o in runs if o["first"] is not None]; print("successes",len(fh),"of 30; first hit mean",round(np.mean(fh),1),"median",np.median(fh))
elif "--ga" in A:
    i=A.index("--ga"); N,G=int(A[i+1]),int(A[i+2]); pc,pm=float(A[i+3]),float(A[i+4]); el="--noelite" not in A
    rng=np.random.default_rng(1519); res=[ga_run(N,G,pc,pm,rng,elitism=el) for _ in range(2000)]
    print(f"N={N} G={G} pc={pc} pm={pm} elitism={el}: success {np.mean([o['first'] is not None for o in res]):.3f}, evaluations {res[0]['evals']}")
elif "--wf" in A:
    i=A.index("--wf"); rule=A[i+1]; N=int(A[i+2]); mu=float(A[i+3]); el="--elite" in A; M=wf_matrix(N,rule,mu,elite=el)
    if mu==0 and not el: B,t=absorption(M); print(f"{rule}, N={N}: fixation from one copy {B[0,1]:.4f}, mean generations to absorption {t[0]:.2f}")
    else: pi=stationary(M); print(f"{rule}, N={N}, mu={mu}, elite={el}: stationary P(no EDD) {pi[0]:.3g}, mean share {(np.arange(N+1)*pi).sum()/N:.3f}")
elif "--heat" in A:
    rng=np.random.default_rng(1561); H=np.zeros((6,6))
    for _ in range(1000): H+=position_matrix(ga_run(10,10,0.9,0.2,rng,record=True)["pops"][10])
    H/=1000; print("rows J1..J6, columns positions 1..6"); print(np.round(H,2))
else: print(__doc__)
