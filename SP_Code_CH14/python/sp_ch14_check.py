"""SP_CH14 — number checks for every example and exercise of Chapter 14."""
import sys, numpy as np; sys.path.insert(0,__file__.rsplit('/',1)[0])
from sp_ch14_sa import *
def show(l,v): print(f"{l:<58} {v}")
vals,counts=np.unique(F,return_counts=True)
show("R6: states, min, #opt, mean, levels",(len(STATES),int(F.min()),len(OPT),round(F.mean(),2),len(vals)))
show("Table 14.1 first 12 levels; rest",(list(zip(vals[:12].tolist(),counts[:12].tolist())),int(720-counts[:12].sum())))
show("Ex 14.1 J2-J1-J4-J5-J3-J6; start neighbors",(tardiness((1,0,3,4,2,5)),[int(F[y]) for y in NA[START]]))
show("Ex 14.2 random search 100; mean",(round(1-(718/720)**100,3),360))
Ms=metropolis_adj(0,strict=True); absorb=[x for x in range(720) if Ms[x,x]==1.0]; trans=[x for x in range(720) if x not in absorb]
Q=Ms[np.ix_(trans,trans)]; R=Ms[np.ix_(trans,absorb)]; Nf=np.linalg.inv(np.eye(len(trans))-Q); B=Nf@R; t=Nf@np.ones(len(trans))
Pab=np.zeros((720,len(absorb))); Pab[trans]=B
for k,a in enumerate(absorb): Pab[a,k]=1
tt=np.zeros(720); tt[trans]=t; oc=[k for k,a in enumerate(absorb) if F[a]==11]
show("Ex 14.4 absorbing states",[(label(STATES[a]),int(F[a])) for a in absorb])
show("Ex 14.4 P(success) random/START; split; steps",(round(Pab[:,oc].sum(1).mean(),4),round(Pab[START,oc].sum(),4),Pab[START].round(3),round(tt.mean(),1),round(tt[START],1)))
show("Ex 14.5 greedy with ties: mean hit random/START",(round(hitting_times(metropolis_adj(0),OPT).mean(),1),round(hitting_times(metropolis_adj(0),OPT)[START],1)))
show("Ex 14.6 acceptance T=1,3,10",[[round(np.exp(-d/T),4) for d in (1,3,8)] for T in (1,3,10)])
rng=np.random.default_rng(0); x=START; tr=[]
for k in range(8):
    r1=round(rng.random(),2); r2=round(rng.random(),2); m=min(int(5*r1),4); y=NA[x][m]; d=int(F[y]-F[x]); acc=d<=0 or r2<np.exp(-d/3)
    tr.append((k+1,int(F[x]),r1,m+1,int(F[y]),d,round(min(1,np.exp(-d/3)),3),r2,acc)); x=y if acc else x
show("Ex 14.7 trace (step,f,r1,move,f',Δ,p,r2,acc)",tr); show("Ex 14.7 end",(label(STATES[x]),int(F[x])))
show("Ex 14.8 flows equal",np.isclose(np.exp(-36/3)*0.2,np.exp(-28/3)*0.2*np.exp(-8/3)))
show("Ex 14.9 P(opt) T=1,3,10,inf; E[f]",([round(boltzmann(T)[OPT].sum(),4) for T in (1,3,10,1e9)],[round((boltzmann(T)*F).sum(),2) for T in (1,3,10,1e9)]))
show("Ex 14.10 max|pi - Boltzmann| at T=3",float(np.abs(stationary(metropolis_adj(3))-boltzmann(3)).max()))
show("Ex 14.11 hitting from START T=0,1,3,10,inf",[round(hitting_times(metropolis_adj(T),OPT)[START],1) for T in (0,1,3,10,1e6)])
show("Ex 14.12 toy hitting T=0.5,1,2,4,10,inf",[round(hitting_times(toy_matrix(T),[17])[0],1) for T in (0.5,1,2,4,10,1e6)])
D=np.array([F[NA[x]]-F[x] for x in range(720)]).ravel(); show("Ex 14.14 mean uphill, share up/tie, T0, alpha, T50",(round(D[D>0].mean(),2),round((D>0).mean(),3),round((D==0).mean(),3),round(-3.24/np.log(0.7),2),round((0.06/10)**0.01,3),round(10*0.95**50,3)))
# exercises
show("Exercise 14.1",(tardiness((0,1,3,4,2,5)),tardiness((5,3,1,0,4,2)),tardiness((0,1,3,4,5,2))))
show("Exercise 14.3",(round(1-(718/720)**50,3),round(1-(718/720)**200,3)))
show("Exercise 14.6",[[round(np.exp(-d/T),4) for d in (1,3,8)] for T in (0.5,2,5)])
show("Exercise 14.7",(tardiness((0,1,3,4,2,5)),tardiness((0,1,3,4,5,2)),round(np.exp(-1/3),3)))
show("Exercise 14.9",[float(f"{np.exp(25/T):.3g}") for T in (1,3,10)])
show("Exercise 14.10 truncated vs exact",(round(2/sum(n*np.exp(-(k-11)/2) for k,n in zip(vals[:12],counts[:12])),4),round(boltzmann(2)[OPT].sum(),4)))
for T in (1e-9,1,1e6):
    p=0.5*np.exp(-2/T); m=np.linalg.solve(np.array([[0.5,-0.5],[-p,0.5+p]]),np.ones(2)); show(f"Exercise 14.12 T={T:g} (m_A,m_B)",m.round(3))
show("Exercise 14.13",(round(np.exp(3),1),round(np.exp(2),2)))
show("Exercise 14.14",([round(10*0.95**k,3) for k in (20,50,100)],round(0.01**(1/200),4)))
show("Exercise 14.15",(round(-3.24/np.log(0.8),1),round(-3.24/np.log(0.5),2)))
show("Exercise 14.16",(round(28/30,3),round(1.96*np.sqrt(28/30*2/30/30),3)))
show("Exercise 14.17",round(1-(718/720)**47,3)); show("Exercise 14.18 swap-15 T=0 hit from START",round(hitting_time_to_opt(0,START),1))
