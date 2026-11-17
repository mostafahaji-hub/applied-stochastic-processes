"""SP_CH17 — Monte Carlo basics.
Usage: python sp_ch17_simulation.py --lcg A C M SEED   (sequence and period of an LCG)
       python sp_ch17_simulation.py --plate N          (estimate P(van 7 late) from N simulated days, seed 172)
       python sp_ch17_simulation.py --audit            (Table 17.1, seed 172)
       python sp_ch17_simulation.py --vr               (plain vs antithetic vs control variate, seed 178)
       python sp_ch17_simulation.py --crn              (tire policies 5 vs 6 months, independent vs common random numbers, seed 179)"""
import sys, numpy as np; sys.path.insert(0,__file__.rsplit('/',1)[0])
from sp_ch17_mc import *
from sp_ch14_sa import F
A=sys.argv
def late(rng,n):
    rain=rng.random(n)<0.3; return np.where(rain,rng.random(n)<0.40,rng.random(n)<0.157)
if "--lcg" in A:
    i=A.index("--lcg"); a,c,m,x0=map(int,A[i+1:i+5]); print("sequence:",lcg(a,c,m,x0,min(m,40)),"\nperiod:",period(a,c,m,x0),"  Hull-Dobell full period:",hull_dobell(a,c,m))
elif "--plate" in A:
    n=int(A[A.index("--plate")+1]); m,se,ci=mc_mean(late(np.random.default_rng(172),n)); print(f"n = {n}: estimate {m:.4f}, SE {se:.4f}, 95% interval [{ci[0]:.3f}, {ci[1]:.3f}]  (exact 0.2299)")
elif "--audit" in A:
    rng=np.random.default_rng(172)
    print("P(late), n=1000:",mc_mean(late(rng,1000)))
    print("refund, n=1000:",mc_mean(discrete_inv(rng.random(1000),[0,20,50,100],[0.5,0.3,0.15,0.05])))
    print("mean tardiness, n=100:",mc_mean(F[rng.integers(720,size=100)]))
    hits=0
    for _ in range(10000):
        x=2
        while 0<x<10: x+=1 if rng.random()<0.55 else -1
        hits+=x==10
    print("runway h(2), n=10000:",hits/10000,"SE",np.sqrt(hits/10000*(1-hits/10000)/10000))
    print("tire mean life, n=1000:",mc_mean(weib_inv(rng.random(1000),2.5,12)))
elif "--vr" in A:
    rng=np.random.default_rng(178); U=rng.random(200000); L=weib_inv(U,2.5,12); Y=-np.log(1-U); b=np.cov(L,Y)[0,1]/Y.var(); ep=[];ea=[];ec=[]
    for r in range(2000):
        u=rng.random(100); l=weib_inv(u,2.5,12); ep.append(l.mean()); u2=rng.random(50); ea.append(0.5*(weib_inv(u2,2.5,12)+weib_inv(1-u2,2.5,12)).mean()); ec.append(l.mean()-b*((-np.log(1-u)).mean()-1))
    print(f"b = {b:.3f};  SD plain {np.std(ep):.3f}, antithetic {np.std(ea):.3f}, control {np.std(ec):.3f}  (exact mean {TIRE_MEAN:.3f})")
elif "--crn" in A:
    rng=np.random.default_rng(179); dI=[];dC=[]
    for r in range(1000):
        La=weib_inv(rng.random(1000),2.5,12); Lb=weib_inv(rng.random(1000),2.5,12)
        dI.append(tire_cost_rate(Lb,6)-tire_cost_rate(La,5)); dC.append(tire_cost_rate(La,6)-tire_cost_rate(La,5))
    dI,dC=np.array(dI),np.array(dC); print(f"independent: mean {dI.mean():.3f}, SD {dI.std():.3f}, wrong sign {np.mean(dI<0):.3f};  common: mean {dC.mean():.3f}, SD {dC.std():.3f}, wrong sign {np.mean(dC<0):.3f}  (exact 0.867)")
else: print(__doc__)
