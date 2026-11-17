"""SP_CH18 — number checks for Chapter 18 (reads des_results.json for the simulation tables)."""
import sys, json, numpy as np; sys.path.insert(0,__file__.rsplit('/',1)[0])
from sp_ch18_des import *
from scipy.stats import poisson, norm
R=json.load(open(__file__.rsplit('/',1)[0]+'/des_results.json'))
def show(l,v): print(f"{l:<52} {v}")
arr=np.array([0.6,2.0,2.3,5.2,5.7]); serv=np.array([1.8,1.1,0.7,1.2,0.9]); pat=np.array([np.inf,np.inf,0.5,np.inf,np.inf]); st,ab,_=run_queue(arr,serv,pat,[(0,1)])
show("Ex 18.2 starts, abandoned",(np.round(st,1).tolist(),ab.tolist())); show("Ex 18.2 area, Lq, lambda, util",(1.6,round(1.6/7.3,3),round(5/7.3,3),round(5.0/7.3,3)))
st2,ab2,_=run_queue(arr,serv,np.full(5,np.inf),[(0,1)]); show("Quest 18.1 (patient)",(np.round(st2-arr,1).tolist(),round(float((st2-arr).sum()),1)))
show("Ex 18.3 accept probs; calls per period; day",([0.5,1,0.625,0.75],[240,720,300,540],1800))
w=np.array(R['audit']['wq']); show("Ex 18.4 audit",(round(w.mean(),1),round(1.96*w.std(ddof=1)/np.sqrt(20),1),round(np.mean(R['audit']['pw']),3),round(erlang_c(3,2/3,5)['Wq']*60,1)))
for k in "ABCDE": s=R['scen'][k]; show(f"Ex 18.6/18.8 scenario {k}",(round(s['sl'],3),round(s['aband'],3),round(s['wait'],2),round(s['maxwait'],1),s['hours'],[round(p[0],3) for p in s['per']]))
show("Ex 18.7 Erlang C per period (SL)",{k:(None if v is None else round(v['SL'],3)) for k,v in R['erl'].items()})
dC=np.array(R['crn_cd']['dC']); dI=np.array(R['crn_cd']['dI']); show("Ex 18.9 CRN C-D",(round(dC.mean(),4),round(dC.std(ddof=1),4),round(dI.std(ddof=1),4),round((dI.std(ddof=1)/dC.std(ddof=1))**2,1)))
q=R['warm']['q']; show("Ex 18.10 warm-up at 30/60/120/300",[round(q[int(x/5)],2) for x in (30,60,120,300)])
c1=np.array(R['r5']['rtf']); c2=np.array(R['r5']['age']); show("Ex 18.12 R5",(round(c1.mean(),2),round(np.mean(c1>=3),3),round(c2.mean(),2),round(np.mean(c2>=3),3),round(np.mean(c2==0),3),round(R['r5']['planned'],2)))
show("Exercise 18.4",round(1-norm.cdf(30.5/np.sqrt(720)),3)); show("Exercise 18.15 spares",(int(poisson.ppf(0.95,4.508)),int(poisson.ppf(0.95,1.05))))
show("Exercise 18.9 costs A-E",[round(h*25+a*1801*10+1801*(1-a)*w*2) for h,a,w in ((50,0.05,4.731),(60,0.018,0.909),(56,0.013,0.728),(59,0.010,0.570),(59,0.007,0.468))])
