"""SP_CH19 — output analysis, MCMC and importance sampling (importable)."""
import numpy as np, sys
sys.path.insert(0,__file__.rsplit('/',1)[0])
from scipy.stats import gamma as G, weibull_min, norm, t as tdist
def ci(x,level=0.95):
    x=np.asarray(x,float); n=len(x); m=x.mean(); h=tdist.ppf(0.5+level/2,n-1)*x.std(ddof=1)/np.sqrt(n); return m,h
def moving_average(y,w):
    y=np.asarray(y,float); out=np.empty_like(y)
    for i in range(len(y)):
        k=min(i,w,len(y)-1-i); out[i]=y[i-k:i+k+1].mean()
    return out
def acf(x,lags):
    x=np.asarray(x,float)-np.mean(x); v=np.dot(x,x)/len(x); return [np.dot(x[:-k],x[k:])/len(x)/v for k in lags]
def batch_means_se(x,b):
    x=np.asarray(x,float); k=len(x)//b; m=x[:k*b].reshape(k,b).mean(axis=1); return m.std(ddof=1)/np.sqrt(k),k
def ess(x,max_lag=2000):
    """effective sample size by summing autocorrelations until they turn negative (initial positive sequence)."""
    x=np.asarray(x,float); n=len(x); x=x-x.mean(); f=np.fft.rfft(x,2*n); ac=np.fft.irfft(f*np.conj(f))[:n]; ac/=ac[0]
    s=0.0
    for k in range(1,min(max_lag,n)):
        if ac[k]<0: break
        s+=ac[k]
    return n/(1+2*s)
# ---- MCMC 1: machine-3 failure rate, gamma prior, Poisson data (conjugate: exact answer known) ----
PRIOR_A,PRIOR_B,FAILS,SHIFTS=2.0,10.0,12,84
def log_post_rate(l): return -np.inf if l<=0 else (PRIOR_A+FAILS-1)*np.log(l)-(PRIOR_B+SHIFTS)*l
def metropolis_1d(logp,x0,sd,n,rng):
    x=x0; lp=logp(x); out=np.empty(n); acc=0
    for i in range(n):
        y=x+sd*rng.standard_normal(); ly=logp(y)
        if np.log(rng.random())<ly-lp: x,lp=y,ly; acc+=1
        out[i]=x
    return out,acc/n
# ---- MCMC 2: Weibull tire lives (k, eta) with flat priors on log k and log eta ----
def weibull_loglik(k,eta,x):
    return np.sum(np.log(k)-np.log(eta)+(k-1)*(np.log(x)-np.log(eta))-(x/eta)**k)
def metropolis_weibull(x,n,rng,sd=(0.15,0.07),start=(np.log(2.0),np.log(10.0))):
    th=np.array(start,float); lp=weibull_loglik(np.exp(th[0]),np.exp(th[1]),x); out=np.empty((n,2)); acc=0
    for i in range(n):
        pr=th+np.array(sd)*rng.standard_normal(2); lq=weibull_loglik(np.exp(pr[0]),np.exp(pr[1]),x)
        if np.log(rng.random())<lq-lp: th,lp=pr,lq; acc+=1
        out[i]=np.exp(th)
    return out,acc/n
def age_cost_curve(k,eta,Ts,cp=80,cf=600):
    """cost rate of age replacement at each T in Ts (fine grid integration of the survival function)."""
    grid=np.linspace(0,Ts.max(),1201); S=np.exp(-(grid/eta)**k); cum=np.concatenate([[0],np.cumsum((S[1:]+S[:-1])/2*np.diff(grid))])
    EL=np.interp(Ts,grid,cum); F=1-np.exp(-(Ts/eta)**k); return (cp*(1-F)+cf*F)/EL
# ---- importance sampling: R4 cash walk (+1 w.p. 0.55, -1 w.p. 0.45), start 20, ruin at -10 within 90 days ----
def exact_ruin(p=0.55,start=20,barrier=-10,days=90):
    lo=barrier; hi=start+days+1; pos=np.zeros(hi-lo+1); pos[start-lo]=1.0; ruined=0.0
    for d in range(days):
        new=np.zeros_like(pos); new[1:]+=p*pos[:-1]; new[:-1]+=(1-p)*pos[1:]
        ruined+=new[0]; new[0]=0.0; pos=new
    return ruined
def ruin_mc(n,rng,p=0.55,p_sim=0.55,start=20,barrier=-10,days=90,chunk=20000):
    """plain MC (p_sim = p) or importance sampling with tilted up-probability p_sim; returns per-path weighted indicators."""
    out=[]
    for k in range(0,n,chunk):
        m=min(chunk,n-k); up=rng.random((m,days))<p_sim; steps=np.where(up,1,-1); path=start+np.cumsum(steps,axis=1)
        hit=(path<=barrier); ever=hit.any(axis=1); tau=np.where(ever,hit.argmax(axis=1)+1,days)
        ups=np.array([up[i,:tau[i]].sum() for i in range(m)]); downs=tau-ups
        lr=np.exp(ups*np.log(p/p_sim)+downs*np.log((1-p)/(1-p_sim)))
        out.append(np.where(ever,lr,0.0))
    return np.concatenate(out)
