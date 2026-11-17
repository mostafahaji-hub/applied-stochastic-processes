"""SP_CH18 — discrete-event simulation of Nava's processes.
Usage: python sp_ch18_simulation.py --trace        (Table 18.1: one operator, five callers, one impatient)
       python sp_ch18_simulation.py --audit        (M/M/5 vs Erlang C, 20 replications, seed 184)
       python sp_ch18_simulation.py --day X        (scenario X in A–E over 100 days, seed 186)
       python sp_ch18_simulation.py --crn          (C vs D service level: common vs independent random numbers)
       python sp_ch18_simulation.py --r2 | --r5 | --warm
       python sp_ch18_simulation.py --all          (re-creates des_results.json used by sp_ch18_figures.py)"""
import sys, json, numpy as np; sys.path.insert(0,__file__.rsplit('/',1)[0])
from sp_ch18_des import *
A=sys.argv
SCEN={'A':[(0,5)],'B':[(0,6)],'C':[(0,5),(120,7),(300,5)],'D':[(0,5),(120,8),(300,5)],'E':[(0,5),(120,7),(300,5),(420,6)]}
HOURS={'A':50,'B':60,'C':56,'D':59,'E':59}
def audit(seed=184):
    rng=np.random.default_rng(seed); wq=[];pw=[]
    for r in range(20):
        arr,serv,pat=r1_stream(rng,profile=((0,7500,3.0),),T=7500,lam_max=3.0,p_imp=0.0); st,ab,_=run_queue(arr,serv,pat,[(0,5)]); keep=arr>500; w=(st-arr)[keep]; wq.append(w.mean()*60); pw.append((w>1e-12).mean())
    return wq,pw
def per_period(arr,st,ab,bounds=(0,120,300,420,600)):
    out=[]
    for a,b in zip(bounds[:-1],bounds[1:]):
        m=(arr>=a)&(arr<b); served=~np.isnan(st[m]); w=st[m]-arr[m]; out.append((np.mean(served&(w<=0.5)),ab[m].mean(),np.nanmean(np.where(served,w,np.nan))))
    return out
if "--trace" in A:
    arr=np.array([0.6,2.0,2.3,5.2,5.7]); serv=np.array([1.8,1.1,0.7,1.2,0.9]); pat=np.array([np.inf,np.inf,0.5,np.inf,np.inf])
    st,ab,_=run_queue(arr,serv,pat,[(0,1)])
    for i in range(5): print(f"caller {i+1}: arrives {arr[i]}, " + ("abandons after 0.5" if ab[i] else f"starts {st[i]:.1f}, waits {st[i]-arr[i]:.1f}, leaves {st[i]+serv[i]:.1f}"))
    waits=np.where(ab,pat,st-arr); print("sum of waits (area under the queue curve):",round(waits.sum(),2))
elif "--audit" in A:
    wq,pw=audit(); print(f"Wq = {np.mean(wq):.1f} ± {1.96*np.std(wq,ddof=1)/np.sqrt(20):.1f} s (Erlang C 137.2);  P(wait) = {np.mean(pw):.3f} (0.762)")
elif "--day" in A:
    k=A[A.index("--day")+1]; rng=np.random.default_rng(186); res=[]
    for r in range(100):
        arr,serv,pat=r1_stream(rng); st,ab,_=run_queue(arr,serv,pat,SCEN[k]); res.append(day_stats(arr,st,ab))
    print(k,{x:round(float(np.mean([d[x] for d in res])),3) for x in ('calls','sl','aband','wait','maxwait')},"operator-hours",HOURS[k])
elif "--crn" in A:
    rng=np.random.default_rng(186); dC=[]
    for r in range(100):
        arr,serv,pat=r1_stream(rng); s1,a1,_=run_queue(arr,serv,pat,SCEN['C']); s2,a2,_=run_queue(arr,serv,pat,SCEN['D']); dC.append(day_stats(arr,s1,a1)['sl']-day_stats(arr,s2,a2)['sl'])
    rng=np.random.default_rng(188); dI=[]
    for r in range(100):
        a1_,s1_,p1_=r1_stream(rng); a2_,s2_,p2_=r1_stream(rng); x1,y1,_=run_queue(a1_,s1_,p1_,SCEN['C']); x2,y2,_=run_queue(a2_,s2_,p2_,SCEN['D'])
        dI.append(day_stats(a1_,x1,y1)['sl']-day_stats(a2_,x2,y2)['sl'])
    print(f"C − D service level: common {np.mean(dC):.4f} (SD {np.std(dC,ddof=1):.4f});  independent {np.mean(dI):.4f} (SD {np.std(dI,ddof=1):.4f})")
elif "--r2" in A:
    rng=np.random.default_rng(1812); s=np.sqrt(np.log(1+1.5**2)); m=-s**2/2
    for k,f in [('exponential',lambda g: g.exponential(1.0)),('constant',lambda g: 1.0),('lognormal',lambda g: g.lognormal(m,s))]:
        Av,d=line_sim(f,rng); print(f"{k:12s} availability {Av:.3f}  mean stop {d.mean():.2f}  P(stop > 2) {np.mean(d>2):.3f}  95th pct {np.quantile(d,0.95):.2f}")
elif "--r5" in A:
    rng=np.random.default_rng(1813); c1,_=fleet_bursts(rng); c2,pl=fleet_bursts(rng,T=5.0)
    print(f"run to failure: {c1.mean():.2f} bursts/month, P(>=3) {np.mean(c1>=3):.3f};  age 5: {c2.mean():.2f}, P(>=3) {np.mean(c2>=3):.3f}, P(0) {np.mean(c2==0):.3f}, planned {pl.mean():.2f}/month")
elif "--warm" in A:
    grid=np.arange(0,301,5.0); rng=np.random.default_rng(1810); Q=[]
    for r in range(300):
        arr,serv,pat=r1_stream(rng,profile=((0,300,3.0),),T=300,lam_max=3.0,p_imp=0.0); st,ab,rec=run_queue(arr,serv,pat,[(0,5)],grid); Q.append(rec)
    Qm=np.mean(np.array(Q),axis=0); print("mean queue at 30, 60, 120, 300 min:",[round(Qm[int(x/5)],2) for x in (30,60,120,300)],"(steady 6.86)")
elif "--all" in A:
    R={}; wq,pw=audit(); R['audit']=dict(wq=wq,pw=pw)
    grid=np.arange(0,721,5.0); rng=np.random.default_rng(186); res={k:[] for k in SCEN}; Q={k:[] for k in SCEN}; per={k:[] for k in SCEN}
    for r in range(100):
        arr,serv,pat=r1_stream(rng)
        for k,cs in SCEN.items():
            st,ab,rec=run_queue(arr,serv,pat,cs,grid); res[k].append(day_stats(arr,st,ab)); Q[k].append(rec); per[k].append(per_period(arr,st,ab))
    R['scen']={k:dict(calls=float(np.mean([x['calls'] for x in res[k]])),aband=float(np.mean([x['aband'] for x in res[k]])),wait=float(np.mean([x['wait'] for x in res[k]])),sl=float(np.mean([x['sl'] for x in res[k]])),maxwait=float(np.mean([x['maxwait'] for x in res[k]])),hours=HOURS[k],per=np.mean(np.array(per[k]),axis=0).tolist(),qmean=np.mean(np.array(Q[k]),axis=0).tolist(),q90=np.percentile(np.array(Q[k]),90,axis=0).tolist(),q10=np.percentile(np.array(Q[k]),10,axis=0).tolist()) for k in SCEN}
    R['grid']=grid.tolist(); R['erl']={f'{l}_{c}':erlang_c(l,2/3,c) for l,c in ((2,5),(2.5,5),(3,5),(4,7),(4,8))}
    dC=[res['C'][i]['sl']-res['D'][i]['sl'] for i in range(100)]; rng=np.random.default_rng(188); dI=[]
    for r in range(100):
        a1_,s1_,p1_=r1_stream(rng); a2_,s2_,p2_=r1_stream(rng); x1,y1,_=run_queue(a1_,s1_,p1_,SCEN['C']); x2,y2,_=run_queue(a2_,s2_,p2_,SCEN['D']); dI.append(day_stats(a1_,x1,y1)['sl']-day_stats(a2_,x2,y2)['sl'])
    R['crn_cd']=dict(dC=dC,dI=dI)
    gw=np.arange(0,301,5.0); rng=np.random.default_rng(1810); Qw=[]
    for r in range(300):
        arr,serv,pat=r1_stream(rng,profile=((0,300,3.0),),T=300,lam_max=3.0,p_imp=0.0); st,ab,rec=run_queue(arr,serv,pat,[(0,5)],gw); Qw.append(rec)
    R['warm']=dict(grid=gw.tolist(),q=np.mean(np.array(Qw),axis=0).tolist())
    rng=np.random.default_rng(1813); c1,_=fleet_bursts(rng); c2,pl=fleet_bursts(rng,T=5.0); R['r5']=dict(rtf=c1.tolist(),age=c2.tolist(),planned=float(pl.mean()))
    json.dump(R,open(__file__.rsplit('/',1)[0]+'/des_results.json','w')); print("written des_results.json")
else: print(__doc__)
