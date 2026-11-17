"""SP_CH19 — output analysis, MCMC and importance sampling.
Usage: python sp_ch19_simulation.py --all        (re-creates ch19_results.json: scenario days, Welch, long run, MCMC, Weibull posterior, importance sampling)
       python sp_ch19_simulation.py --mcmc SD    (failure-rate posterior with proposal SD)
       python sp_ch19_simulation.py --is PPRIME N (importance sampling of the cash-ruin probability)"""
import sys, json, numpy as np; sys.path.insert(0,__file__.rsplit('/',1)[0])
from sp_ch19_output import *; from sp_ch18_des import *
from scipy.stats import gamma as G, weibull_min
from scipy.special import gammaln
A=sys.argv
if "--mcmc" in A:
    sd=float(A[A.index("--mcmc")+1]); c,acc=metropolis_1d(log_post_rate,0.15,sd,21000,np.random.default_rng(1906)); s=c[1000:]
    print(f"proposal SD {sd}: acceptance {acc:.3f}, ESS {ess(s):.0f}, mean {s.mean():.4f}, 95% [{np.quantile(s,0.025):.4f}, {np.quantile(s,0.975):.4f}] (exact 0.1489 [0.0814, 0.2365])")
elif "--is" in A:
    i=A.index("--is"); pp=float(A[i+1]); n=int(A[i+2]); w=ruin_mc(n,np.random.default_rng(1910),p_sim=pp)
    print(f"p' = {pp}, n = {n}: estimate {w.mean():.3e} ± {w.std(ddof=1)/np.sqrt(n):.2e} (exact {exact_ruin():.3e})")
elif "--all" in A:
    R={}; SCEN={'A':[(0,5)],'B':[(0,6)],'C':[(0,5),(120,7),(300,5)],'D':[(0,5),(120,8),(300,5)],'E':[(0,5),(120,7),(300,5),(420,6)]}
    rng=np.random.default_rng(186); day={k:[] for k in SCEN}
    for r in range(100):
        arr,serv,pat=r1_stream(rng)
        for k,cs in SCEN.items(): st,ab,_=run_queue(arr,serv,pat,cs); day[k].append(day_stats(arr,st,ab)['sl'])
    R['sl']=day; R['bonf']={k:list(ci(np.array(day['E'])-np.array(day[k]),1-0.05/4)) for k in 'ABCD'}
    grid=np.arange(0,601,5.0); rng=np.random.default_rng(1902); Q=[]
    for r in range(200):
        arr,serv,pat=r1_stream(rng,profile=((0,600,3.0),),T=600,lam_max=3.0,p_imp=0.0); st,ab,rec=run_queue(arr,serv,pat,[(0,5)],grid); Q.append(rec)
    Qm=np.mean(np.array(Q),axis=0); R['welch']=dict(grid=grid.tolist(),q=Qm.tolist(),ma5=moving_average(Qm,5).tolist(),ma15=moving_average(Qm,15).tolist())
    rng=np.random.default_rng(1903); arr,serv,pat=r1_stream(rng,profile=((0,70000,3.0),),T=70000,lam_max=3.0,p_imp=0.0); st,ab,_=run_queue(arr,serv,pat,[(0,5)]); w=((st-arr)[arr>500])*60
    R['bm']=[(b,)+tuple(map(float,batch_means_se(w,b))) for b in (1,10,100,1000,2000,5000,10000,20000)]; R['acf']=dict(lags=list(range(0,3001,25)),r=[1.0]+acf(w,list(range(25,3001,25)))); R['ess_w']=float(ess(w,20000)); R['w_len']=len(w)
    a,b=PRIOR_A+FAILS,PRIOR_B+SHIFTS; ch,acc=metropolis_1d(log_post_rate,0.5,0.04,21000,np.random.default_rng(1905)); s=ch[1000:]
    R['mcmc1']=dict(chain=ch[:3000].tolist(),sample=s[::4].tolist(),acc=acc,ess=float(ess(s)),exact=dict(mean=a/b,q025=G.ppf(0.025,a,scale=1/b),q975=G.ppf(0.975,a,scale=1/b),mean_up=b/(a-1)))
    R['tuning']=[]
    for sd in (0.005,0.04,0.4):
        c,ac=metropolis_1d(log_post_rate,0.15,sd,21000,np.random.default_rng(1906)); ss=c[1000:]; R['tuning'].append(dict(sd=sd,acc=ac,ess=float(ess(ss)),mean=float(ss.mean()),trace=c[:1500].tolist()))
    x=weibull_min.rvs(2.5,scale=12,size=20,random_state=np.random.default_rng(1919)); Wm,accw=metropolis_weibull(x,30000,np.random.default_rng(1907)); Wm=Wm[2000:]; k,eta=Wm[:,0],Wm[:,1]; ml=eta*np.exp(gammaln(1+1/k))
    Ts=np.arange(2,14.01,0.25); idx=np.random.default_rng(1908).choice(len(k),400,replace=False); Tst=[];cs=[];c5=[];rt=[]
    for i in idx:
        cc=age_cost_curve(k[i],eta[i],Ts); j=int(np.argmin(cc)); Tst.append(float(Ts[j])); cs.append(float(cc[j])); c5.append(float(cc[np.argmin(np.abs(Ts-5))])); rt.append(float(600/ml[i]))
    R['weib']=dict(x=x.tolist(),k=k[::10].tolist(),eta=eta[::10].tolist(),Tstar=Tst,c5=c5,cs=cs,rtf=rt,acc=accw)
    plain=ruin_mc(200000,np.random.default_rng(1909)); isw=ruin_mc(20000,np.random.default_rng(1910),p_sim=0.35)
    R['is']=dict(exact=exact_ruin(),plain_cum=(np.cumsum(plain)/np.arange(1,len(plain)+1))[::200].tolist(),is_cum=(np.cumsum(isw)/np.arange(1,len(isw)+1))[::20].tolist(),plain_se=float(plain.std(ddof=1)/np.sqrt(len(plain))),is_se=float(isw.std(ddof=1)/np.sqrt(len(isw))),plain_hits=int((plain>0).sum()),is_mean=float(isw.mean()),plain_mean=float(plain.mean()))
    json.dump(R,open(__file__.rsplit('/',1)[0]+'/ch19_results.json','w')); print("written ch19_results.json")
else: print(__doc__)
