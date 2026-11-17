"""SP_CH06 — number checks for every example and exercise of Chapter 6."""
import numpy as np
from scipy.stats import norm, binom
def show(l,v): print(f"{l:<60} {v}")
def tardiness(order,P=[6,3,8,2,5,4],D=[14,8,20,6,18,12]):
    t=0; tot=0; C=[]
    for j in order: t+=P[j]; C.append(t); tot+=max(0,t-D[j])
    return C,tot
show("Ex 6.2 P(X>6), P(at least one of 30)",(round(1-binom.cdf(6,12,.23),4),round(1-binom.cdf(6,12,.23)**30,3)))
show("Ex 6.4 N30 mean/var, Cov(N10,N30), rho",(6.9,round(30*.23*.77,3),round(10*.23*.77,3),round(np.sqrt(10/30),3)))
show("Ex 6.5 S20 sd, P(>5000)",(round(1000*np.sqrt(20),1),round(1-norm.cdf(5000/(1000*np.sqrt(20))),3)))
show("Ex 6.6 drift: E,SD step; 60 days; P(<0)",(100,round(np.sqrt(990000),1),6000,round(995*np.sqrt(60),1),round(norm.cdf(-6000/(995*np.sqrt(60))),3)))
show("Ex 6.8 B(60,.05), B(6000,.0005) means",(3,3))
show("Ex 6.10 RW rho(m,n)=sqrt(m/n)",round(np.sqrt(20/80),2))
show("Ex 6.13 AR(1): var, sd, rho(k)",(2500,50,[round(0.6**k,3) for k in range(1,4)]))
show("Ex 6.18 R2: W->W, W->S->W",(0.86,0.07))
show("Ex 6.19 R3 S->G->P two months",0.01)
show("Ex 6.20 R4 90 days",(29000,round(995*np.sqrt(90))))
show("Quest 6.3 / Ex 6.18a",tardiness([3,1,5,0,4,2]))
show("Fig 6.11 sequence J1..J6",tardiness([0,1,2,3,4,5]))
# exercises
show("Exercise 6.2 0.963^5",round(0.963**5,3))
show("Exercise 6.3",(2.8,round(20*.14*.86,2),round(5*.14*.86,3),0.5))
show("Exercise 6.4",(3000,round(1-norm.cdf(4/3),3)))
show("Exercise 6.5",(200,960000,20000,round(980*10),round(norm.cdf(-20000/9798),3)))
show("Exercise 6.8",(64,36,0.75))
show("Exercise 6.11",(2500,50,[0.8,round(0.8**3,3),round(0.8**7,2)]))
show("Exercise 6.16",(round(0.2+0.7*0.2+0.1*0.1,3),round(0.49+0.005,3)))
show("Exercise 6.17",round(0.86**2+0.1*0.7+0.04*0.5,3))
show("Exercise 6.18",(tardiness([1,3,5,0,4,2]),tardiness([3,1,5,4,0,2])))
show("Exercise 6.20a",(30,round(np.sqrt(30),2),12,round(np.sqrt(4/10),2)))
show("Exercise 6.20b",(26000,round(995*np.sqrt(60)),round(norm.cdf((-10000-26000)/(995*np.sqrt(60))),6)))
