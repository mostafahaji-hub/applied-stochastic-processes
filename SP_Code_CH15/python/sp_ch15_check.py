"""SP_CH15 — number checks for every example and exercise of Chapter 15."""
import sys, numpy as np; sys.path.insert(0,__file__.rsplit('/',1)[0])
from sp_ch15_ga import *
from math import comb
def show(l,v): print(f"{l:<60} {v}")
POP0=[(0,1,2,3,4,5),(5,4,3,2,1,0),(1,0,3,4,2,5),(0,1,5,3,4,2),(4,2,0,5,1,3),(3,0,1,2,5,4)]
f=np.array([tardiness(s) for s in POP0]); g=57-f; rank=np.argsort(np.argsort(f))+1; pt=(2*(6-rank)+1)/36
show("Ex 15.1 P0 f, best, mean",(f.tolist(),int(f.min()),round(f.mean(),2)))
show("Ex 15.2 roulette, tournament",((g/g.sum()).round(3).tolist(),pt.round(3).tolist()))
show("Ex 15.2 expected parent counts of #4 (10 draws); P(never)",(round(10*g[3]/g.sum(),2),round(10*pt[3],2),round((1-g[3]/g.sum())**10,3),round((1-pt[3])**10,3)))
show("Ex 15.3 ratio #4/#5: 1/f, 57-f, tournament",(round(56/21,2),36,11))
show("Ex 15.4 N=10 rank probs; P(best never in 18 tournaments)",([(2*(10-r)+1)/100 for r in range(1,11)],round(0.9**36,4)))
show("Ex 15.5 one-point",label_or:=one_point((0,1,2,3,4,5),EDD,3))
show("Ex 15.6 OX(#4,#3; 3,4)",(label(ox(POP0[3],POP0[2],2,3)),tardiness(ox(POP0[3],POP0[2],2,3))))
show("Quest 15.1",(label(ox((0,1,2,3,4,5),EDD,1,3)),tardiness(ox((0,1,2,3,4,5),EDD,1,3))))
rows,new=hand_trace(POP0,np.random.default_rng(2))
for i,r in enumerate(rows,1): show(f"Ex 15.7 child {i}",(r['t1'],r['t2'],r['rc'],r['cx'],r['rm'],r['mk'],label(r['child']),int(r['f'])))
nf=[tardiness(s) for s in new]; show("Ex 15.7 new population f, best, mean, distinct",(nf,min(nf),round(np.mean(nf),2),len(set(new))))
show("Ex 15.7 child 1 before mutation",(label(ox(POP0[1],POP0[0],1,4)),tardiness(ox(POP0[1],POP0[0],1,4))))
show("Ex 15.8 #populations N=2,3,10",(comb(721,2),comb(722,3),f"{comb(729,10):.3e}"))
for rule in ("neutral","roulette","tournament"):
    B,t=absorption(wf_matrix(10,rule)); show(f"Ex 15.8-9 {rule}: fixation from 1, mean gens",(round(B[0,1],4),round(t[0],2)))
for N in (20,50): show(f"Ex 15.9 N={N} roulette/tournament",(round(absorption(wf_matrix(N,'roulette'))[0][0,1],4),round(absorption(wf_matrix(N,'tournament'))[0][0,1],4)))
show("Ex 15.9 P(lost in gen 1)",(round((1-46/433)**10,3),round(0.81**10,3)))
for rule in ("tournament","roulette"):
    M=wf_matrix(10,rule,0,elite=True); tr=list(range(1,10)); t=np.linalg.solve(np.eye(9)-M[np.ix_(tr,tr)],np.ones(9)); show(f"Ex 15.10 elite {rule}: mean gens to fixation",round(t[0],2))
for mu in (0.01,0.05):
    for rule in ("roulette","tournament"):
        pi=stationary(wf_matrix(10,rule,mu)); show(f"Ex 15.11 mu={mu} {rule}: P(no EDD), mean share",(float(f"{pi[0]:.3g}"),round((np.arange(11)*pi).sum()/10,3)))
H=np.load(__file__.rsplit('/',1)[0]+"/heat_gen10.npy") if __import__('os').path.exists(__file__.rsplit('/',1)[0]+"/heat_gen10.npy") else None
if H is not None: show("Ex 15.12 heat gen 10 (J3@6, J5@5, J1@4, J6@3, J2@2, J4@1)",(round(H[2,5],2),round(H[4,4],2),round(H[0,3],2),round(H[5,2],2),round(H[1,1],2),round(H[3,0],2)))
show("Ex 15.14 30 runs mean/median first hit",(round(np.mean([64,37,37,55,64,82,82,55,163,46,19,37,64,73,163,199,100,55,19,55,118,136,136,64,73,64,55]),1),64.0,round(1.96*np.sqrt(0.09/30),3)))
# exercises
show("Exercise 15.1/15.2",([tardiness(s) for s in [(0,1,2,3,4,5),(1,0,3,4,2,5),(0,1,5,3,4,2),SPT]],(np.array([21,32,36,43])/132).round(3).tolist()))
show("Exercise 15.4",((label(ox(SPT,(0,1,2,3,4,5),0,2)),tardiness(ox(SPT,(0,1,2,3,4,5),0,2))),(label(ox((0,1,2,3,4,5),SPT,3,5)),tardiness(ox((0,1,2,3,4,5),SPT,3,5)))))
show("Exercise 15.5",one_point((0,1,2,3,4,5),SPT,2))
show("Exercise 15.6",[(label(mutate_adjacent(EDD,k)),tardiness(mutate_adjacent(EDD,k))) for k in range(5)])
show("Exercise 15.8",(round(0.9**36,3),round(0.85**18,3)))
show("Exercise 15.16 runs needed",round(1.96**2*0.09/0.02**2))
