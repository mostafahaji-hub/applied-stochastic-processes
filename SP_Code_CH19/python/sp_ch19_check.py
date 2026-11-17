"""SP_CH19 — number checks for Chapter 19 (reads ch19_results.json written by sp_ch19_simulation.py --all)."""
import sys, json, numpy as np; sys.path.insert(0,__file__.rsplit('/',1)[0])
from sp_ch19_output import *
from scipy.stats import gamma as G, t as tdist
R=json.load(open(__file__.rsplit('/',1)[0]+'/ch19_results.json'))
def show(l,v): print(f"{l:<54} {v}")
sl=np.array(R['sl']['E']); m,h=ci(sl); show("Ex 19.1 E service level, SD, days ±0.01/±0.005",(round(m,4),round(h,4),round(sl.std(ddof=1),4),int(np.ceil((1.96*sl.std(ddof=1)/0.01)**2)),int(np.ceil((1.96*sl.std(ddof=1)/0.005)**2)),round(sl.min(),3),round(sl.max(),3)))
ma=np.array(R['welch']['ma15']); show("Ex 19.2 Welch MA at 60/120/180 min",[round(ma[int(x/5)],2) for x in (60,120,180)])
bm=R['bm']; show("Ex 19.3 naive SE, batch SE (b=2000), ESS",(round(bm[0][1],3),round(bm[4][1],2),round(R['ess_w'])))
for k in 'ABCD': show(f"Ex 19.4 E − {k} (Bonferroni)",tuple(round(x,4) for x in R['bonf'][k]))
ex=R['mcmc1']['exact']; s=np.array(R['mcmc1']['sample']); show("Ex 19.5 exact mean, 95%, mean uptime",(round(ex['mean'],4),round(ex['q025'],4),round(ex['q975'],4),round(ex['mean_up'],2)))
show("Ex 19.5 MCMC mean, quantiles, acceptance, ESS",(round(s.mean(),4),np.round(np.quantile(s,[0.025,0.975]),4).tolist(),round(R['mcmc1']['acc'],3),round(R['mcmc1']['ess'])))
show("Ex 19.6 tuning (sd, acc, ESS)",[(t['sd'],round(t['acc'],3),round(t['ess'])) for t in R['tuning']])
W=R['weib']; T=np.array(W['Tstar']); c5=np.array(W['c5']); cs=np.array(W['cs']); rtf=np.array(W['rtf'])
show("Ex 19.7 T* mean, 90%, P([4,6]), regret, saving",(round(T.mean(),2),np.quantile(T,[0.05,0.95]).tolist(),round(np.mean((T>=4)&(T<=6)),3),round((c5-cs).mean(),3),round((rtf-c5).mean(),1)))
show("Ex 19.8 exact ruin, IS mean ± SE, plain hits",(R['is']['exact'],R['is']['is_mean'],R['is']['is_se'],R['is']['plain_hits']))
show("Exercise 19.11 posteriors",((round(G.ppf(0.025,14,scale=1/94),3),round(G.ppf(0.975,14,scale=1/94),3)),(round(G.ppf(0.025,26,scale=1/178),3),round(G.ppf(0.975,26,scale=1/178),3))))
