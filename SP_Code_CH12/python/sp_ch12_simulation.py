"""SP_CH12 — event-driven simulation of the 4-machine line with one repair crew (Example 12.20, Exercise 12.19).
Keeps scheduled event times (residual lives), so it is valid for non-exponential repair too.
Usage: python sp_ch12_simulation.py [--fixed-repair] [--seed N]"""
import sys, numpy as np; sys.path.insert(0,__file__.rsplit('/',1)[0])
from sp_ch12_reliability import line_availability
A=sys.argv; seed=int(A[A.index("--seed")+1]) if "--seed" in A else 12; fixed="--fixed-repair" in A
rng=np.random.default_rng(seed); T=20000.0; rates=np.array([0.05,0.05,1/7,0.05])
fail_at=rng.exponential(1/rates)                 # next failure time of each (working) machine
failed=np.zeros(4,bool); repairing=None; repair_done=np.inf; t=0.0; up=0.0
def start_repair(now):
    global repairing,repair_done
    if repairing is None and failed.any():
        repairing=2 if failed[2] else int(np.flatnonzero(failed)[0]); repair_done=now+(1.0 if fixed else rng.exponential(1.0))
while t<T:
    nf=np.where(failed,np.inf,fail_at); i=int(np.argmin(nf)); t_next=min(nf[i],repair_done,T)
    if not failed.any(): up+=t_next-t
    t=t_next
    if t>=T: break
    if repair_done<=nf[i]:
        failed[repairing]=False; fail_at[repairing]=t+rng.exponential(1/rates[repairing]); repairing=None; repair_done=np.inf; start_repair(t)
    else:
        failed[i]=True; start_repair(t)
print(f"simulated availability {up/T:.3f}   CTMC {line_availability(1)[0]:.3f}   independent bound {(20/21)**3*7/8:.3f}   ({'fixed' if fixed else 'exponential'} repair)")
