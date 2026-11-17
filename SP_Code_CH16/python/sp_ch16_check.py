"""SP_CH16 v2 — number checks (textbook Keshtel algorithm with random keys)."""
import sys, json, numpy as np; sys.path.insert(0,__file__.rsplit('/',1)[0])
from sp_ch16_ka import *
D=__file__.rsplit('/',1)[0]+'/'
def show(l,v): print(f"{l:<52} {v}")
show("Ex 16.1 groups; 1+4Smax; max evals/iteration",((2,3,5),1+4*2,2*20+3+5))
P0,o,tr,new,moves,P,fv=hand_trace(24)
show("Table 16.1 keys decode",[(label(decode(p)),tardiness(decode(p))) for p in P0])
show("Table 16.2 swirl values",[(t[0],int(t[3]),bool(t[4])) for t in tr])
show("Table 16.3 landings",[(label(decode(k)),f) for _,k,f in new]); show("Table 16.3 moves",[(m[5],m[6]) for m in moves])
show("new population mean, best",(round(float(fv.mean()),2),int(fv.min())))
show("Quest 16.1",(label(decode(np.array([0.40,0.15,0.95,0.05,0.70,0.30]))),tardiness(decode(np.array([0.40,0.15,0.95,0.05,0.70,0.30])))))
L4=P0[3]; show("Exercise 16.4 distances from keshtel 4",[round(float(np.abs(L4-P0[k]).sum()),2) for k in (0,1,2,4,5)])
show("Exercise 16.3 tie decode",(label(decode(np.array([1,0,1,1,1,0.]))),tardiness(decode(np.array([1,0,1,1,1,0.])))))
q3=1-(718/720)**3; q5=1-(718/720)**5; show("Ex 16.3 / Exercise 16.7 q3, q5, bound",(round(q3,4),round(q5,4),round((718/720)**19,3)))
R=json.load(open(D+'ka2_results.json')); show("Ex 16.5 groups",(np.round(R['groups']['imp'],3).tolist(),np.round(R['groups']['first'],3).tolist()))
show("Ex 16.6 ablation (success, P by 100, mean)",{k:tuple(round(x,3) for x in v) for k,v in R['ablation'].items()})
show("Ex 16.7 toy",(R['toy3'],R['toy0'])); show("Ex 16.8 thirty runs",(R['runs30']['n'],round(R['runs30']['mean'],1),R['runs30']['median']))
T=json.load(open(D+'ka2_ttt.json'))
for k in ('greedy','SA','GA','KA','random'):
    a=np.array([o[0] or 10**9 for o in T[k]]); d=np.array([o[1] or 10**9 for o in T[k]])
    show(f"Ex 16.11 {k}: all by50/100, distinct by50/100",(round(float((a<=50).mean()),3),round(float((a<=100).mean()),3),round(float((d<=50).mean()),3),round(float((d<=100).mean()),3)))
