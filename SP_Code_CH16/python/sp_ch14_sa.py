"""SP_CH14 — Simulated annealing on R6 as a Markov chain (importable).
R6: six jobs on the bottleneck station, processing times p and due dates d (Table 6.7); objective = total tardiness."""
import numpy as np
from itertools import permutations, combinations
P_TIMES=np.array([6,3,8,2,5,4]); DUE=np.array([14,8,20,6,18,12]); NAMES=["J1","J2","J3","J4","J5","J6"]
def tardiness(seq):
    t=0; tot=0
    for j in seq: t+=P_TIMES[j]; tot+=max(0,t-DUE[j])
    return tot
STATES=list(permutations(range(6)))                       # 720 sequences
INDEX={s:i for i,s in enumerate(STATES)}
F=np.array([tardiness(s) for s in STATES])
PAIRS=list(combinations(range(6),2))                       # 15 swap moves (positions)
def swap(seq,i,j): s=list(seq); s[i],s[j]=s[j],s[i]; return tuple(s)
NEIGH=np.array([[INDEX[swap(s,i,j)] for (i,j) in PAIRS] for s in STATES])   # 720 x 15
OPT=np.flatnonzero(F==F.min())
def label(seq): return "-".join(NAMES[j] for j in seq)
def metropolis_matrix(T):
    """720x720 transition matrix of SA at fixed temperature T (T=0: accept only improvements or ties? -> strictly no worse)."""
    n=len(STATES); M=np.zeros((n,n))
    for x in range(n):
        for y in NEIGH[x]:
            d=F[y]-F[x]
            a=1.0 if d<=0 else (0.0 if T==0 else np.exp(-d/T))
            M[x,y]+=a/15
        M[x,x]+=1-M[x].sum()
    return M
def boltzmann(T):
    w=np.exp(-(F-F.min())/T); return w/w.sum()
def hitting_time_to_opt(T,start):
    M=metropolis_matrix(T); trans=np.setdiff1d(np.arange(len(STATES)),OPT); Q=M[np.ix_(trans,trans)]
    m=np.linalg.solve(np.eye(len(trans))-Q,np.ones(len(trans))); out=np.zeros(len(STATES)); out[trans]=m; return out[start]
def run_sa(start,T0,alpha,n_iter,rng):
    x=start; best=x; hist=[F[x]]; best_hist=[F[x]]; acc=0
    for k in range(n_iter):
        T=T0*alpha**k; y=NEIGH[x][rng.integers(15)]; d=F[y]-F[x]
        if d<=0 or rng.random()<np.exp(-d/T): x=y; acc+=1
        if F[x]<F[best]: best=x
        hist.append(F[x]); best_hist.append(F[best])
    return np.array(hist),np.array(best_hist),acc/n_iter,best
# ---- adjacent-swap neighborhood (the chapter's main move: swap two consecutive jobs) ----
ADJ=[(i,i+1) for i in range(5)]
NA=np.array([[INDEX[swap(s,i,j)] for (i,j) in ADJ] for s in STATES])     # 720 x 5
START=INDEX[(0,1,2,3,4,5)]                                                   # J1-J2-J3-J4-J5-J6, tardiness 36
TRAP=INDEX[(5,3,1,0,4,2)]                                                    # J6-J4-J2-J1-J5-J3, tardiness 12
def metropolis_adj(T,strict=False):
    n=len(STATES); M=np.zeros((n,n))
    for x in range(n):
        for y in NA[x]:
            d=F[y]-F[x]
            if strict: a=1.0 if d<0 else 0.0
            else: a=1.0 if d<=0 else (0.0 if T==0 else np.exp(-d/T))
            M[x,y]+=a/5
        M[x,x]+=1-M[x].sum()
    return M
def stationary(M):
    n=M.shape[0]; A=np.vstack([M.T-np.eye(n),np.ones(n)]); b=np.r_[np.zeros(n),1]; return np.linalg.lstsq(A,b,rcond=None)[0]
def hitting_times(M,target):
    n=M.shape[0]; trans=np.setdiff1d(np.arange(n),target); Q=M[np.ix_(trans,trans)]
    m=np.linalg.solve(np.eye(len(trans))-Q,np.ones(len(trans))); out=np.zeros(n); out[trans]=m; return out
def run_sa_adj(start,T0,alpha,n_iter,rng):
    x=start; best=x; hist=[F[x]]; best_hist=[F[x]]; acc=0; first_hit=None if F[x]>F.min() else 0
    for k in range(n_iter):
        T=T0*alpha**k; y=NA[x][rng.integers(5)]; d=F[y]-F[x]
        if d<=0 or rng.random()<np.exp(-d/T): x=y; acc+=1
        if F[x]<F[best]: best=x
        if first_hit is None and F[x]==F.min(): first_hit=k+1
        hist.append(F[x]); best_hist.append(F[best])
    return np.array(hist),np.array(best_hist),acc/n_iter,best,first_hit
# ---- a one-dimensional landscape with a barrier (the "miniature" of a rugged problem) ----
TOY=np.array([40,37,34,31,28,25,28,31,29,27,25,23,21,19,17,15,13,11])   # 18 states in a row; local valley at 5 (25), barrier peak at 7 (31), global minimum at 17 (11)
def toy_matrix(T):
    n=len(TOY); M=np.zeros((n,n))
    for x in range(n):
        for y in (x-1,x+1):
            if 0<=y<n:
                d=TOY[y]-TOY[x]; a=1.0 if d<=0 else (0.0 if T==0 else np.exp(-d/T)); M[x,y]+=a/2
        M[x,x]+=1-M[x].sum()
    return M

def run_sa_toy(T0,alpha,n_iter,rng,start=0):
    x=start; hist=[TOY[x]]; best=TOY[x]
    for k in range(n_iter):
        T=T0*alpha**k; y=x+(1 if rng.random()<0.5 else -1)
        if 0<=y<len(TOY):
            d=TOY[y]-TOY[x]
            if d<=0 or rng.random()<np.exp(-d/T): x=y
        best=min(best,TOY[x]); hist.append(TOY[x])
    return np.array(hist),best
