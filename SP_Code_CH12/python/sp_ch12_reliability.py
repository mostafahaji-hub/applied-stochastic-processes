"""SP_CH12 — reliability & maintenance tools (importable)."""
import numpy as np, sys; sys.path.insert(0,__file__.rsplit('/',1)[0])
from sp_ch11_ctmc import stationary_Q, age_replacement_rate
from scipy.stats import weibull_min, poisson
def weibull_hazard(t,k,eta): return (k/eta)*(np.asarray(t)/eta)**(k-1)
def R_series(Rs): return np.prod(Rs,axis=0)
def R_parallel(Rs): return 1-np.prod(1-np.asarray(Rs),axis=0)
def R_k_of_n(k,n,R):
    from math import comb; return sum(comb(n,j)*R**j*(1-R)**(n-j) for j in range(k,n+1))
def line_availability(r,lo=0.05,l3=1/7,mu=1.0):
    """4-machine series line: three machines fail at rate lo, machine 3 at l3; r repairers (machine 3 first)."""
    idx={(n,m):n+4*m for n in range(4) for m in range(2)}; Q=np.zeros((8,8))
    for (n,m),i in idx.items():
        if n<3: Q[i,idx[(n+1,m)]]+=(3-n)*lo
        if m==0: Q[i,idx[(n,1)]]+=l3
        crews=r
        if m==1 and crews>0: Q[i,idx[(n,0)]]+=mu; crews-=1
        if n>0 and crews>0: Q[i,idx[(n-1,m)]]+=min(n,crews)*mu
        Q[i,i]=-Q[i].sum()
    pi=stationary_Q(Q); return pi[idx[(0,0)]],pi
def renewal_function(T,k,eta,n=400):
    dt=T/n; t=np.arange(1,n+1)*dt; Fv=weibull_min.cdf(t,k,scale=eta); f=np.diff(np.r_[0,Fv]); m=np.zeros(n)
    for i in range(n): m[i]=Fv[i]+np.dot(m[i-1::-1][:i],f[:i]) if i>0 else Fv[i]
    return m[-1]
def block_replacement_rate(T,k,eta,cp,cf): return (cp+cf*renewal_function(T,k,eta))/T
def inspection_rate(T,lam,ci,cd): return (ci+cd*(T-(1-np.exp(-lam*T))/lam))/T
def spares_needed(mean_failures,level):
    s=0
    while poisson.cdf(s,mean_failures)<level: s+=1
    return s
