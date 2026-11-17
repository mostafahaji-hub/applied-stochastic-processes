"""SP_CH02 — number checks for every example and exercise of Level 2."""
from math import comb
def show(l,v): print(f"{l:<58} {v}")
def bayes(prior, sens, fp): 
    """P(cause | positive) for a two-state cause."""
    return prior*sens/(prior*sens+(1-prior)*fp)
def total(ws, ps): return sum(w*p for w,p in zip(ws,ps))
def series(rs):
    out=1.0
    for r in rs: out*=r
    return out
def parallel(rs):
    out=1.0
    for r in rs: out*=(1-r)
    return 1-out
show("Ex 2.1/2.2 churn by tier; tier given churn", ([110/550,30/300,6/150],[round(110/146,3),round(30/146,3),round(6/146,3)]))
show("Ex 2.3 long wait total; Ex 2.4", (total([.4,.35,.25],[.1,.2,.3]), 0.075/0.185))
show("Ex 2.5 GGG, GDG, comb check", (round(8/12*7/11*6/10,4), round(8/12*4/11*7/10,4), round(comb(8,3)/comb(12,3),4)))
show("Ex 2.6 hiring; Ex 2.7 backup", (0.6*0.5*0.8, 0.8+0.2*0.7))
show("Ex 2.8 P(D); Ex 2.13 posteriors", (round(total([.5,.3,.2],[.02,.04,.08]),4), [round(x/0.038,3) for x in (0.010,0.012,0.016)]))
show("Ex 2.9 FCR, improved", (round(total([.3,.5,.2],[.85,.7,.5]),4), round(total([.3,.5,.2],[.85,.7,.65]),4)))
show("Ex 2.11 window", round(total([.2,.3,.5],[.6,.8,.9]),4))
show("Ex 2.12 scanner posterior; P(good|no flag)", (round(bayes(.03,.95,.08),4), round(8924/8939,4)))
show("Ex 2.14 fraud", round(bayes(.005,.9,.02),4))
o=0.03/0.97*(0.95/0.08); show("Ex 2.15 odds one/two flags", (round(o/(1+o),4), round(o*11.875/(1+o*11.875),4)))
show("Ex 2.16 pass/fail", (round(240/415,4), round(60/585,4)))
show("Ex 2.19 two vans", (0.23**2, 0.77**2, round(1-0.77**2,4), round(2*0.23*0.77,4)))
show("Ex 2.21 20 sensors, 4 sensors, p max", (round(1-0.95**20,4), round(1-0.95**4,4), round(1-0.9**(1/20),5)))
show("Ex 2.22 calls needed", next(n for n in range(1,20) if 0.6**n<=0.1))
show("Ex 2.23 series 4,5; r needed", (round(0.95**4,4), round(0.95**5,4), round(0.95**0.25,4)))
show("Ex 2.24 parallel 3,2,1", (parallel([.9]*3), parallel([.9]*2), .9))
show("Ex 2.25 mixed", round(series([parallel([series([.9,.9]),.85]),.98]),4))
show("Ex 2.26 generators", next(n for n in range(1,10) if 0.2**n<=0.01))
show("Ex 2.27 Simpson", (72/80,10/20,82/100,19/20,48/80,67/100))
show("Ex 2.28 correlated second scan", round(300*.95*.95/(300*.95*.95+9700*.08),3))
# exercises
show("Exercise 2.4", (round(10/15*9/14*8/13,4), round(comb(10,3)/comb(15,3),4), round(5/15*10/14*9/13,4)))
show("Exercise 2.6", (total([.4,.35,.25],[.9,.8,.7]), total([.4,.35,.25],[.9,.8,.85])))
show("Exercise 2.7", (0.1*0.3+0.9*0.02, 0.03/0.048))
show("Exercise 2.8/2.10/2.11", (round(bayes(.05,.9,.1),4), round((0.05/0.95*81)/(1+0.05/0.95*81),3), round(8550/8600,4)))
show("Exercise 2.9", (0.7*0.01+0.3*0.05, round(0.015/0.022,4)))
show("Exercise 2.14", (round(1-0.97**12,4), next(n for n in range(1,50) if 0.97**n<=0.5)))
show("Exercise 2.15/2.16/2.17", (round(0.98**5,4), 1-0.02**2, round(parallel([.9,.9])*.95,4), next(n for n in range(1,10) if 0.3**n<=0.05)))
show("Exercise 2.19", (405/500, round(405/1355,3)))
show("Exercise 2.20", (total([.5,.3,.2],[.05,.1,.2]), round(0.04/0.095,3), 320/1280, round(0.97**3*parallel([.9,.9]),4)))
