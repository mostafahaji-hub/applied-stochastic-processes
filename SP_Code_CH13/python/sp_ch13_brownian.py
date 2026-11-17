"""SP_CH13 — Brownian motion, Gaussian processes and SDE tools (importable).
Units for Nava's cash (R4): thousand euros and days. Fair model: steps ±1 per day (sigma = 1).
R4 model: steps +1 w.p. 0.55, -1 w.p. 0.45  =>  mu = 0.1 per day, sigma^2 = 0.99 per day."""
import numpy as np
from scipy.stats import norm
MU_R4, SIG_R4 = 0.1, np.sqrt(0.99)
def bm_paths(n_paths,T,dt,rng,mu=0.0,sigma=1.0,x0=0.0):
    n=int(round(T/dt)); inc=mu*dt+sigma*np.sqrt(dt)*rng.standard_normal((n_paths,n))
    return np.linspace(0,T,n+1), np.hstack([np.full((n_paths,1),x0),x0+np.cumsum(inc,axis=1)])
def p_end_below(a,mu,sigma,T):
    """P(X(T) <= x0 - a) for X = x0 + mu t + sigma W."""
    return norm.cdf((-a-mu*T)/(sigma*np.sqrt(T)))
def p_hit_below(a,mu,sigma,T):
    """P(min_{s<=T} X(s) <= x0 - a): first passage to a lower barrier at distance a (a > 0)."""
    s=sigma*np.sqrt(T)
    return norm.cdf((-a-mu*T)/s)+np.exp(-2*mu*a/sigma**2)*norm.cdf((-a+mu*T)/s)
def p_ever_below(a,mu,sigma):
    return 1.0 if mu<=0 else np.exp(-2*mu*a/sigma**2)
def p_up_before_down(a,b,mu,sigma):
    """start 0; P(hit +b before -a)."""
    if abs(mu)<1e-15: return a/(a+b)
    k=2*mu/sigma**2; return (1-np.exp(k*a))/(np.exp(-k*b)-np.exp(k*a))
def first_passage_cdf_up(t,a,mu,sigma):
    """P(T_a <= t) for hitting +a (a > 0) with drift mu (inverse Gaussian when mu > 0)."""
    s=sigma*np.sqrt(t); return norm.cdf((mu*t-a)/s)+np.exp(2*mu*a/sigma**2)*norm.cdf((-mu*t-a)/s)
def gbm_stats(S0,mu,sigma,t):
    m=(mu-sigma**2/2)*t; s=sigma*np.sqrt(t)
    return dict(mean=S0*np.exp(mu*t),median=S0*np.exp(m),q05=S0*np.exp(m-1.645*s),q95=S0*np.exp(m+1.645*s))
def gbm_prob_above(S0,mu,sigma,t,K): return 1-norm.cdf((np.log(K/S0)-(mu-sigma**2/2)*t)/(sigma*np.sqrt(t)))
def ou_forecast(x,m,theta,stat_sd,h):
    """mean and SD of an OU process h time units ahead, given today's value x."""
    return m+(x-m)*np.exp(-theta*h), stat_sd*np.sqrt(1-np.exp(-2*theta*h))
def euler_maruyama(a,b,x0,T,dt,n_paths,rng):
    n=int(round(T/dt)); X=np.full(n_paths,float(x0))
    for _ in range(n): X=X+a(X)*dt+b(X)*np.sqrt(dt)*rng.standard_normal(n_paths)
    return X
def hit_freq(x0,barrier,mu,sigma,T,dt,n_paths,rng,chunk=2000):
    """fraction of simulated paths whose minimum on the grid dt falls to the barrier."""
    hits=0; n=int(round(T/dt))
    for k in range(0,n_paths,chunk):
        m=min(chunk,n_paths-k); inc=mu*dt+sigma*np.sqrt(dt)*rng.standard_normal((m,n))
        hits+=int((x0+np.minimum.accumulate(np.cumsum(inc,axis=1),axis=1)[:,-1]<=barrier).sum())
    return hits/n_paths
