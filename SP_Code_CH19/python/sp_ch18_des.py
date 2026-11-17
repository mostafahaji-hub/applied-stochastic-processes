"""SP_CH18 — discrete-event simulation (importable): an event-list engine for R1 (multi-server queue with
time-varying arrivals by thinning, impatient callers and shift changes), the R2 line with general repair times,
and the R5 tire fleet. Times in minutes from 08:00 for R1, in shifts for R2, in months for R5."""
import heapq, numpy as np
from collections import deque
from math import factorial
R1_PROFILE=((0,120,2.0),(120,300,4.0),(300,420,2.5),(420,600,3.0))     # 8–10, 10–13, 13–15, 15–18 (calls/min)
def rate(t,profile=R1_PROFILE):
    for a,b,l in profile:
        if a<=t<b: return l
    return 0.0
def r1_stream(rng,profile=R1_PROFILE,T=600,lam_max=4.0,p_imp=0.10,patience=2.0,mean_service=1.5):
    """arrivals by thinning a Poisson(lam_max) stream; service Exp(mean 1.5); 10% of callers leave after 2 min of waiting."""
    t=0.0; arr=[]
    while True:
        t+=rng.exponential(1/lam_max)
        if t>=T: break
        if rng.random()<rate(t,profile)/lam_max: arr.append(t)
    n=len(arr); serv=rng.exponential(mean_service,n); pat=np.where(rng.random(n)<p_imp,patience,np.inf)
    return np.array(arr),serv,pat
def run_queue(arr,serv,pat,cap_schedule,grid=None):
    """event-list simulation; cap_schedule = [(0, c0), (t1, c1), ...]. Returns per-customer starts, abandonment flags and the queue on a grid."""
    n=len(arr); ev=[]; seq=0
    def push(t,typ,x):
        nonlocal seq; heapq.heappush(ev,(t,seq,typ,x)); seq+=1
    for i in range(n): push(arr[i],'A',i)
    for tc,cc in cap_schedule[1:]: push(tc,'C',cc)
    cap=cap_schedule[0][1]; busy=0; q=deque(); waiting=set(); start=np.full(n,np.nan); ab=np.zeros(n,bool)
    rec=[] if grid is not None else None; g=0
    def serve_waiting(t):
        nonlocal busy
        while busy<cap and q:
            j=q.popleft()
            if j in waiting:
                waiting.discard(j); busy+=1; start[j]=t; push(t+serv[j],'D',j)
    while ev:
        t,_,typ,x=heapq.heappop(ev)
        if grid is not None:
            while g<len(grid) and grid[g]<=t: rec.append(len(waiting)); g+=1
        if typ=='A':
            if busy<cap and not waiting: busy+=1; start[x]=t; push(t+serv[x],'D',x)
            else:
                q.append(x); waiting.add(x)
                if np.isfinite(pat[x]): push(t+pat[x],'R',x)
        elif typ=='D': busy-=1; serve_waiting(t)
        elif typ=='R':
            if x in waiting: waiting.discard(x); ab[x]=True
        elif typ=='C': cap=x; serve_waiting(t)
    if grid is not None:
        while g<len(grid): rec.append(0); g+=1
    return start,ab,(np.array(rec) if grid is not None else None)
def day_stats(arr,start,ab):
    served=~np.isnan(start); w=start[served]-arr[served]
    return dict(calls=len(arr),aband=ab.mean(),wait=w.mean(),sl=np.mean(served&((start-arr)<=0.5)),maxwait=w.max() if len(w) else 0.0)
def erlang_c(lam,mu,c):
    a=lam/mu; r=a/c
    if r>=1: return None
    s=sum(a**k/factorial(k) for k in range(c)); p0=1/(s+a**c/factorial(c)/(1-r)); C=a**c/factorial(c)*p0/(1-r)
    return dict(C=C,Wq=C/(c*mu-lam),SL=1-C*np.exp(-(c*mu-lam)*0.5))
# ---- R2 line: three machines at failure rate 0.05/shift, machine 3 at 1/7, one repair crew (machine 3 first) ----
def line_sim(repair_draw,rng,T=50000.0):
    rates=np.array([0.05,0.05,1/7,0.05]); fail_at=rng.exponential(1/rates); failed=np.zeros(4,bool); rep=None; rep_done=np.inf
    t=0.0; up=0.0; downs=[]; down_start=None
    def start_rep(now):
        nonlocal rep,rep_done
        if rep is None and failed.any(): rep=2 if failed[2] else int(np.flatnonzero(failed)[0]); rep_done=now+repair_draw(rng)
    while t<T:
        nf=np.where(failed,np.inf,fail_at); i=int(np.argmin(nf)); tn=min(nf[i],rep_done,T)
        if not failed.any(): up+=tn-t
        t=tn
        if t>=T: break
        was_up=not failed.any()
        if rep_done<=nf[i]:
            failed[rep]=False; fail_at[rep]=t+rng.exponential(1/rates[rep]); rep=None; rep_done=np.inf; start_rep(t)
        else: failed[i]=True; start_rep(t)
        now_up=not failed.any()
        if was_up and not now_up: down_start=t
        if (not was_up) and now_up and down_start is not None: downs.append(t-down_start)
    return up/T,np.array(downs)
# ---- R5 fleet: 48 tires, Weibull(2.5, 12) lives, run-to-failure or age replacement at T months ----
def fleet_bursts(rng,months=1200,n_tires=48,T=None):
    counts=np.zeros(months,int); planned=np.zeros(months,int)
    for k in range(n_tires):
        t=0.0
        while t<months:
            L=12*(-np.log(1-rng.random()))**0.4
            if T is not None and L>=T:
                t+=T
                if t<months: planned[int(t)]+=1
            else:
                t+=L
                if t<months: counts[int(t)]+=1
    return counts,planned
