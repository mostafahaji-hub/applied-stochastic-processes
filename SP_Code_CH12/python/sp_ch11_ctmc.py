"""SP_CH11 — continuous-time Markov chains and renewal tools (importable)."""
import numpy as np
from scipy.linalg import expm
from scipy.integrate import quad
Q3=np.array([[-0.17,0.12,0.05],[3.0,-3.5,0.5],[1.0,0,-1.0]])   # machine 3 (W,S,M), rates per shift
def stationary_Q(Q):
    n=Q.shape[0]; A=np.vstack([Q.T,np.ones(n)]); b=np.r_[np.zeros(n),1]; return np.linalg.lstsq(A,b,rcond=None)[0]
def transition(Q,t): return expm(Q*t)
def jump_chain(Q):
    J=Q.copy().astype(float); np.fill_diagonal(J,0); return J/(-np.diag(Q))[:,None]
def two_state(lam,mu,t):
    """P(up at t | up at 0) with failure rate lam and repair rate mu."""
    return mu/(lam+mu)+lam/(lam+mu)*np.exp(-(lam+mu)*t)
def age_replacement_rate(T,F,cp,cf):
    """long-run cost rate of replacing at age T or at failure; F(x)=cdf of lifetime."""
    EL=quad(lambda x: 1-F(x),0,T)[0]; return (cp*(1-F(T))+cf*F(T))/EL
def simulate_ctmc(Q,start,T,rng):
    s=start; t=0.0; times=[0.0]; states=[s]
    while t<T:
        rate=-Q[s,s]; t+=rng.exponential(1/rate); p=Q[s].copy(); p[s]=0; p/=rate; s=int(rng.choice(len(p),p=p)); times.append(t); states.append(s)
    return np.array(times),np.array(states)
