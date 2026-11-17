"""SP_CH09 — Markov chain toolkit (importable): n-step, distributions, first-step analysis."""
import numpy as np
P2=np.array([[.86,.10,.04],[.70,.20,.10],[.50,0,.50]])                     # R2 machine 3 (W,S,M)
P3=np.array([[.70,.10,0,.20],[.05,.75,.10,.10],[0,.06,.90,.04],[0,0,0,1]]) # R3 club (S,G,P,C)
W=np.array([[.6,.4],[.17,.83]])                                            # weather (rain, dry)
def nstep(P,n): return np.linalg.matrix_power(P,n)
def dist(alpha,P,n): return np.asarray(alpha)@nstep(P,n)
def hitting_time(P,target):
    """expected steps to first reach any state in `target` (indices), from every state."""
    S=P.shape[0]; T=[i for i in range(S) if i not in target]; Q=P[np.ix_(T,T)]
    m=np.linalg.solve(np.eye(len(T))-Q,np.ones(len(T))); out=np.zeros(S); out[T]=m; return out
def hitting_prob(P,A,B):
    """probability of reaching A before B, from every state."""
    S=P.shape[0]; T=[i for i in range(S) if i not in A and i not in B]; Q=P[np.ix_(T,T)]; R=P[np.ix_(T,A)].sum(axis=1)
    h=np.linalg.solve(np.eye(len(T))-Q,R); out=np.zeros(S); out[A]=1; out[T]=h; return out
def value(P,transient,reward):
    Q=P[np.ix_(transient,transient)]; return np.linalg.solve(np.eye(len(transient))-Q,np.asarray(reward))
def runway(p,N,i): r=(1-p)/p; return i/N if abs(p-0.5)<1e-12 else (1-r**i)/(1-r**N)
def simulate(P,start,n,rng): 
    s=start; path=[s]; cum=np.cumsum(P,axis=1)
    for _ in range(n): s=int(np.searchsorted(cum[s],rng.random())); path.append(s)
    return path
