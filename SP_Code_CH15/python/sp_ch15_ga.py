"""SP_CH15 — Genetic algorithm on R6 as a stochastic process (importable).
Encoding: a permutation of the six jobs (0-based internally; J1..J6 for display).
Operators: binary tournament selection (two random members, the better wins), order crossover (OX: two random
positions a <= b, copy parent 1 on a..b, fill the other positions left to right in parent 2's order),
adjacent-swap mutation (the move of Chapter 14), elitism (keep the best)."""
import numpy as np, sys
sys.path.insert(0,__file__.rsplit('/',1)[0])
from sp_ch14_sa import P_TIMES, DUE, NAMES, tardiness, STATES, INDEX, F, OPT, label
from scipy.stats import binom
from math import comb
SPT=(3,1,5,4,0,2)          # J4-J2-J6-J5-J1-J3, shortest processing time first: tardiness 14
EDD=(3,1,5,0,4,2)          # J4-J2-J6-J1-J5-J3, earliest due date first: tardiness 11 (an optimum)
def ox(p1,p2,a,b):
    """order crossover: child[a..b] = p1[a..b]; other positions filled left to right with p2's order."""
    seg=list(p1[a:b+1]); rest=[j for j in p2 if j not in seg]; child=[None]*6; child[a:b+1]=seg; it=iter(rest)
    for i in range(6):
        if child[i] is None: child[i]=next(it)
    return tuple(child)
def one_point(p1,p2,c): return tuple(list(p1[:c])+list(p2[c:]))
def mutate_adjacent(s,k): s=list(s); s[k],s[k+1]=s[k+1],s[k]; return tuple(s)
def tournament(fit,rng):
    i,j=rng.integers(len(fit),size=2); return i if fit[i]<=fit[j] else j
def ga_run(N,G,pc,pm,rng,elitism=True,init=None,record=False):
    pop=[STATES[k] for k in rng.integers(720,size=N)] if init is None else list(init)
    fit=np.array([F[INDEX[s]] for s in pop]); evals=N; first=evals if fit.min()==11 else None
    best_hist=[fit.min()]; mean_hist=[fit.mean()]; pops=[list(pop)] if record else None; div=[len(set(pop))]
    for g in range(G):
        new=[]
        if elitism: new.append(pop[int(np.argmin(fit))])
        while len(new)<N:
            p1=pop[tournament(fit,rng)]; p2=pop[tournament(fit,rng)]
            if rng.random()<pc:
                a,b=sorted(rng.integers(6,size=2)); child=ox(p1,p2,a,b)          # two random positions, possibly equal
            else: child=p1
            if rng.random()<pm: child=mutate_adjacent(child,rng.integers(5))
            new.append(child)
        newfit=np.array([F[INDEX[s]] for s in new])
        evals+=N-(1 if elitism else 0)
        if first is None and newfit.min()==11: first=evals
        pop,fit=new,newfit; best_hist.append(fit.min()); mean_hist.append(fit.mean()); div.append(len(set(pop)))
        if record: pops.append(list(pop))
    return dict(best=np.array(best_hist),mean=np.array(mean_hist),div=np.array(div),pops=pops,first=first,evals=evals,final_best=int(fit.min()))
def position_matrix(pop):
    M=np.zeros((6,6))
    for s in pop:
        for pos,j in enumerate(s): M[j,pos]+=1
    return M/len(pop)
# ---- Wright–Fisher model of a population with two types: EDD (f = 11) and SPT (f = 14) ----
def select_prob(x,rule,gO=46,gM=43):
    if rule=="tournament": return 1-(1-x)**2
    if rule=="roulette": return gO*x/(gO*x+gM*(1-x)) if x>0 else 0.0
    return x   # neutral
def wf_matrix(N,rule="tournament",mu=0.0,elite=False):
    M=np.zeros((N+1,N+1))
    for k in range(N+1):
        p=select_prob(k/N,rule); p=p*(1-mu)+(1-p)*mu
        if elite and k>=1:   # one elite copy of the better type is kept; the other N-1 are drawn
            M[k,1:]=binom.pmf(np.arange(N),N-1,p)
        else:
            M[k]=binom.pmf(np.arange(N+1),N,p)
    return M
def absorption(M):
    n=M.shape[0]; trans=list(range(1,n-1)); Q=M[np.ix_(trans,trans)]; R=M[np.ix_(trans,[0,n-1])]
    Nf=np.linalg.inv(np.eye(len(trans))-Q); B=Nf@R; t=Nf@np.ones(len(trans)); return B,t
def stationary(M):
    n=M.shape[0]; A=np.vstack([M.T-np.eye(n),np.ones(n)]); b=np.r_[np.zeros(n),1]; return np.linalg.lstsq(A,b,rcond=None)[0]

def hand_trace(pop,rng,pc=0.9,pm=0.2):
    """one generation with random numbers rounded to two decimals (for Table 15.2)."""
    fit=[tardiness(s) for s in pop]; N=len(pop); u=lambda: round(float(rng.random()),2)
    rows=[]; new=[pop[int(np.argmin(fit))]]
    while len(new)<N:
        draws={}
        def tour():
            ri,rj=u(),u(); i,j=min(int(N*ri),N-1),min(int(N*rj),N-1); w=i if fit[i]<=fit[j] else j; return (ri,rj,i+1,j+1,w+1),pop[w]
        t1,p1=tour(); t2,p2=tour(); rc=u()
        if rc<pc:
            ra,rb=u(),u(); a,b=sorted((min(int(6*ra),5),min(int(6*rb),5))); child=ox(p1,p2,a,b); cx=(ra,rb,a+1,b+1)
        else: child=p1; cx=None
        rm=u(); mk=None
        if rm<pm: rk=u(); k=min(int(5*rk),4); child=mutate_adjacent(child,k); mk=(rk,k+1)
        rows.append(dict(t1=t1,t2=t2,rc=rc,cx=cx,before=None,rm=rm,mk=mk,child=child,f=tardiness(child))); new.append(child)
    return rows,new
