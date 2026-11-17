"""SP_CH03 — Chapter 3 figures and number checks (discrete random variables)."""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from scipy.stats import binom, geom, nbinom, hypergeom, poisson
from math import comb
NAVY, GOLD, EMER, BURG, BLUE, CORAL, IVORY, SLATE = "#0B2545","#C9A227","#1B7F5C","#7A1E2B","#2E86AB","#E07A5F","#FBF8F1","#5B6B7C"
plt.rcParams.update({"font.size":14,"axes.titlesize":15,"axes.labelsize":14,"font.family":"DejaVu Sans","axes.edgecolor":SLATE,"axes.spines.top":False,"axes.spines.right":False,"axes.titlepad":10})
OUT="/home/claude/ch03/fig/"
def save(fig,name): fig.savefig(OUT+name,dpi=300,bbox_inches="tight",facecolor="white",pad_inches=0.15); plt.close(fig)
def rbox(ax,x,y,w,h,fc,ec,lw=2.5): ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0,rounding_size=0.12",fc=fc,ec=ec,lw=lw,zorder=2))
p=0.23
# ---- Fig 3.1 outcomes -> numbers (3 vans) ----
fig,ax=plt.subplots(figsize=(11,5.6)); ax.axis("off"); ax.set_xlim(0,11); ax.set_ylim(0,6.2)
outs=["OOO","OOL","OLO","LOO","OLL","LOL","LLO","LLL"]; xs=[0,1,1,1,2,2,2,3]
for i,(o,x) in enumerate(zip(outs,xs)):
    y=5.6-i*0.72; rbox(ax,0.6,y-0.28,1.6,0.56,IVORY,NAVY,1.8); ax.text(1.4,y,o,ha="center",va="center",fontsize=13,color=NAVY,fontweight="bold",zorder=3)
    ax.add_patch(FancyArrowPatch((2.3,y),(5.6,0.95+x*1.35),arrowstyle="-|>",color=[SLATE,BLUE,EMER,BURG][x],lw=1.6,mutation_scale=14,zorder=1))
for x in range(4):
    y=0.95+x*1.35; rbox(ax,5.7,y-0.4,1.0,0.8,[SLATE,BLUE,EMER,BURG][x],[SLATE,BLUE,EMER,BURG][x]); ax.text(6.2,y,f"X = {x}",ha="center",va="center",fontsize=14,color="white",fontweight="bold",zorder=3)
    pr=comb(3,x)*p**x*(1-p)**(3-x); ax.text(7.0,y,f"{comb(3,x)} outcome{'s' if comb(3,x)>1 else ''}   →   P(X = {x}) = {pr:.3f}",va="center",fontsize=12.5,color=NAVY)
ax.text(1.4,6.05,"outcome (vans A, B, C)",ha="center",fontsize=12,color=SLATE); ax.text(6.2,6.05,"number of late vans",ha="center",fontsize=12,color=SLATE)
save(fig,"SP_Fig_CH03_01.png")
# ---- Fig 3.2 pmf + cdf of X (3 vans) ----
k=np.arange(4); pm=binom.pmf(k,3,p); cd=binom.cdf(k,3,p)
fig,axs=plt.subplots(1,2,figsize=(13,4.8),gridspec_kw={"wspace":0.3})
ax=axs[0]; b=ax.bar(k,pm,color=NAVY,width=0.5)
for bi,v in zip(b,pm): ax.text(bi.get_x()+bi.get_width()/2,v+0.012,f"{v:.3f}",ha="center",color=NAVY,fontsize=12,fontweight="bold")
ax.set_xticks(k); ax.set_xlabel("x (number of late vans)"); ax.set_ylabel("P(X = x)"); ax.set_ylim(0,0.55); ax.set_title("(a) Probability mass function",color=NAVY)
ax=axs[1]; ax.step(np.r_[-1,k,4],np.r_[0,cd,1],where="post",color=GOLD,lw=2.5); ax.scatter(k,cd,color=GOLD,s=60,zorder=3)
for ki,v in zip(k,cd): ax.text(ki+0.08,v+0.03,f"{v:.3f}",fontsize=11.5,color=NAVY)
ax.set_xlim(-0.8,3.8); ax.set_ylim(0,1.08); ax.set_xticks(k); ax.set_xlabel("x"); ax.set_ylabel("F(x) = P(X ≤ x)"); ax.set_title("(b) Cumulative distribution function",color=NAVY)
fig.add_artist(plt.Line2D([0.5,0.5],[0.05,0.95],color=SLATE,lw=1.2,ls=":"))
save(fig,"SP_Fig_CH03_02.png")
# ---- Fig 3.3 expectation as balance point ----
vals=np.array([0,20,50,100]); probs=np.array([0.5,0.3,0.15,0.05]); mu=(vals*probs).sum()
fig,ax=plt.subplots(figsize=(10,4.2))
ax.bar(vals,probs,width=6,color=NAVY); ax.plot([-5,105],[-0.02,-0.02],color=SLATE,lw=3)
ax.annotate("",xy=(mu,-0.02),xytext=(mu,-0.14),arrowprops=dict(arrowstyle="-|>",color=GOLD,lw=3,mutation_scale=18))
ax.text(mu,-0.18,f"balance point = E[X] = {mu:.1f}",ha="center",color=GOLD,fontsize=13,fontweight="bold")
for v,pr in zip(vals,probs): ax.text(v,pr+0.012,f"{pr:.2f}",ha="center",color=NAVY,fontsize=12)
ax.set_ylim(-0.22,0.6); ax.set_xlabel("return value x (€ of refund per order)"); ax.set_ylabel("P(X = x)"); ax.spines["bottom"].set_visible(False); ax.set_yticks([0,0.2,0.4,0.6])
save(fig,"SP_Fig_CH03_03.png")
# ---- Fig 3.4 same mean, different spread ----
fig,axs=plt.subplots(1,2,figsize=(13,4.5),gridspec_kw={"wspace":0.3})
A=([8,9,10,11,12],[0.1,0.2,0.4,0.2,0.1]); Bv=([4,7,10,13,16],[0.1,0.2,0.4,0.2,0.1])
for ax,(v,pr),t,c in zip(axs,[A,Bv],["(a) Supplier P: lead time, SD = 1.1 days","(b) Supplier Q: lead time, SD = 3.3 days"],[NAVY,BURG]):
    ax.bar(v,pr,width=0.7,color=c); ax.axvline(10,color=GOLD,ls="--",lw=2.5); ax.text(10.2,0.42,"mean = 10",color=GOLD,fontsize=12,fontweight="bold")
    ax.set_xlim(2,18); ax.set_ylim(0,0.5); ax.set_xlabel("delivery lead time (days)"); ax.set_ylabel("probability"); ax.set_title(t,color=NAVY)
fig.add_artist(plt.Line2D([0.5,0.5],[0.05,0.95],color=SLATE,lw=1.2,ls=":"))
save(fig,"SP_Fig_CH03_04.png")
# ---- Fig 3.5 binomial n=12 ----
fig,axs=plt.subplots(1,2,figsize=(13,4.6),gridspec_kw={"wspace":0.3}); k=np.arange(13)
for ax,pp,c,t in zip(axs,[0.23,0.5],[NAVY,EMER],["(a) n = 12, p = 0.23  (Nava’s vans)","(b) n = 12, p = 0.50  (a fair coin, for comparison)"]):
    pm=binom.pmf(k,12,pp); ax.bar(k,pm,color=c,width=0.6)
    for ki,v in zip(k,pm):
        if v>0.004: ax.text(ki,v+(0.006 if ki%2==0 else 0.018),f"{v:.3f}",ha="center",fontsize=9.5,color=NAVY)
    ax.axvline(12*pp,color=GOLD,ls="--",lw=2); ax.text(12*pp+0.3,0.31,f"mean = {12*pp:.2f}",color=GOLD,fontsize=11,fontweight="bold")
    ax.set_xticks(k); ax.set_xlabel("x (late vans out of 12)"); ax.set_ylabel("P(X = x)"); ax.set_ylim(0,0.34); ax.set_title(t,color=NAVY)
fig.add_artist(plt.Line2D([0.5,0.5],[0.05,0.95],color=SLATE,lw=1.2,ls=":"))
save(fig,"SP_Fig_CH03_05.png")
# ---- Fig 3.6 geometric p=0.4 ----
k=np.arange(1,11); pm=geom.pmf(k,0.4)
fig,ax=plt.subplots(figsize=(10,4.5)); ax.bar(k,pm,color=NAVY,width=0.6)
for ki,v in zip(k,pm): ax.text(ki,v+0.008,f"{v:.3f}",ha="center",fontsize=11,color=NAVY)
ax.axvline(2.5,color=GOLD,ls="--",lw=2); ax.text(2.65,0.36,"mean = 1/p = 2.5",color=GOLD,fontsize=12,fontweight="bold")
ax.set_xticks(k); ax.set_xlabel("x (attempt on which the customer first answers)"); ax.set_ylabel("P(X = x)"); ax.set_ylim(0,0.45)
save(fig,"SP_Fig_CH03_06.png")
# ---- Fig 3.7 hypergeometric vs binomial ----
fig,axs=plt.subplots(1,2,figsize=(13,4.6),gridspec_kw={"wspace":0.3}); k=np.arange(0,5)
for ax,(N,D),t in zip(axs,[(20,3),(2000,300)],["(a) Pallet of N = 20 with 3 damaged, inspect 4","(b) Shipment of N = 2,000 with 300 damaged, inspect 4"]):
    h=hypergeom.pmf(k,N,D,4); b=binom.pmf(k,4,D/N)
    ax.bar(k-0.18,h,width=0.36,color=NAVY,label="hypergeometric (without replacement)"); ax.bar(k+0.18,b,width=0.36,color=GOLD,label="binomial (with replacement)")
    for ki,hv,bv in zip(k,h,b): ax.text(ki-0.18,hv+0.01,f"{hv:.3f}",ha="center",fontsize=9.5,color=NAVY); ax.text(ki+0.18,bv+0.01,f"{bv:.3f}",ha="center",fontsize=9.5,color=NAVY)
    ax.set_xticks(k); ax.set_xlabel("x (damaged parcels found)"); ax.set_ylabel("probability"); ax.set_ylim(0,0.62); ax.set_title(t,color=NAVY); ax.legend(frameon=False,fontsize=10)
fig.add_artist(plt.Line2D([0.5,0.5],[0.05,0.95],color=SLATE,lw=1.2,ls=":"))
save(fig,"SP_Fig_CH03_07.png")
# ---- Fig 3.8 Poisson ----
fig,ax=plt.subplots(figsize=(11,4.8)); k=np.arange(0,19)
for lam,c,m in [(1,EMER,"o"),(3,NAVY,"s"),(8,BURG,"^")]:
    ax.plot(k,poisson.pmf(k,lam),"-"+m,color=c,lw=2,ms=7,label=f"λ = {lam}")
ax.set_xticks(k); ax.set_xlabel("x (number of calls in one minute)"); ax.set_ylabel("P(X = x)"); ax.legend(frameon=False)
save(fig,"SP_Fig_CH03_08.png")
# ---- Fig 3.9 binomial -> Poisson ----
fig,ax=plt.subplots(figsize=(10,4.6)); k=np.arange(0,10)
ax.bar(k-0.18,binom.pmf(k,500,0.005),width=0.36,color=NAVY,label="binomial n = 500, p = 0.005")
ax.bar(k+0.18,poisson.pmf(k,2.5),width=0.36,color=GOLD,label="Poisson λ = 2.5")
ax.set_xticks(k); ax.set_xlabel("x (fraudulent orders among 500)"); ax.set_ylabel("probability"); ax.legend(frameon=False)
save(fig,"SP_Fig_CH03_09.png")
# ---- Fig 3.10 decision tree ----
fig,ax=plt.subplots(figsize=(17,8)); ax.axis("off"); ax.set_xlim(0,17); ax.set_ylim(0,8.2)
def q(x,y,t,w=3.6,h=1.0): rbox(ax,x-w/2,y-h/2,w,h,IVORY,NAVY); ax.text(x,y,t,ha="center",va="center",fontsize=12,color=NAVY,fontweight="bold",zorder=3,linespacing=1.3)
def d(x,y,t,c,w=3.2,h=1.0): rbox(ax,x-w/2,y-h/2,w,h,c,c); ax.text(x,y,t,ha="center",va="center",fontsize=12,color="white",fontweight="bold",zorder=3,linespacing=1.3)
def a(p1,p2): ax.add_patch(FancyArrowPatch(p1,p2,arrowstyle="-|>",color=SLATE,lw=1.8,mutation_scale=14,zorder=1))
q(8.5,7.5,"What are you counting?")
q(3.2,5.9,"Successes in a FIXED\nnumber of trials n",w=4.2); q(9.5,5.9,"Trials UNTIL\na success happens",w=4.0); q(14.6,5.9,"Events in a time\nwindow or area",w=3.8)
a((6.9,7.1),(3.2,6.4)); a((8.7,7.0),(9.5,6.4)); a((10.1,7.1),(14.6,6.4))
q(1.6,4.2,"Independent trials\n(or with replacement)",w=3.0); q(4.9,4.2,"Without replacement\nfrom a small lot",w=3.0)
a((2.4,5.4),(1.6,4.7)); a((4.0,5.4),(4.9,4.7))
d(1.6,2.5,"Binomial\nB(n, p)",NAVY,w=2.6); d(4.9,2.5,"Hypergeometric\n(N, D, n)",BLUE,w=2.8)
a((1.6,3.7),(1.6,3.0)); a((4.9,3.7),(4.9,3.0))
q(8.1,4.2,"the first success",w=2.6); q(11.1,4.2,"the r-th success",w=2.6)
a((8.9,5.4),(8.1,4.7)); a((10.1,5.4),(11.1,4.7))
d(8.1,2.5,"Geometric\nGeo(p)",EMER,w=2.5); d(11.1,2.5,"Negative binomial\nNB(r, p)",EMER,w=2.9)
a((8.1,3.7),(8.1,3.0)); a((11.1,3.7),(11.1,3.0))
d(14.6,4.2,"Poisson\nPois(λ)",BURG,w=2.8); a((14.6,5.4),(14.6,4.7))
d(1.6,0.8,"n = 1  →  Bernoulli",SLATE,w=3.0); a((1.6,2.0),(1.6,1.3))
d(14.6,2.5,"n large, p small:\nBinomial ≈ Poisson",GOLD,w=3.6); a((14.6,3.7),(14.6,3.0))
d(9.6,0.8,"All outcomes equally likely  →  Discrete uniform",SLATE,w=6.2)
save(fig,"SP_Fig_CH03_10.png")

# ---- Fig 3.11 simulation ----
rng=np.random.default_rng(12); days=10000; late=rng.binomial(12,0.23,size=days)
k=np.arange(13); emp=np.bincount(late,minlength=13)/days; th=binom.pmf(k,12,0.23)
fig,ax=plt.subplots(figsize=(11,4.8))
ax.bar(k-0.18,emp,width=0.36,color=NAVY,label="simulated frequency (10,000 days, seed 12)"); ax.bar(k+0.18,th,width=0.36,color=GOLD,label="binomial pmf B(12, 0.23)")
ax.set_xticks(k); ax.set_xlabel("x (late vans in a day)"); ax.set_ylabel("probability / frequency"); ax.legend(frameon=False)
save(fig,"SP_Fig_CH03_11.png")
print("sim: mean",late.mean(),"var",late.var(ddof=0),"P(X>=4) emp",(late>=4).mean(),"P(0)",emp[0])
# ---- Fig 3.12 concept map ----
fig,ax=plt.subplots(figsize=(12,7)); ax.axis("off"); ax.set_xlim(0,12); ax.set_ylim(0,7.3); ax.set_aspect("equal")
def cbox(x,y,t,c=NAVY,fc=IVORY,w=2.9,h=1.0,tc=None): rbox(ax,x-w/2,y-h/2,w,h,fc,c,2.2); ax.text(x,y,t,ha="center",va="center",fontsize=11.5,color=tc or NAVY,fontweight="bold",zorder=3,linespacing=1.3)
def link(p1,p2): ax.add_patch(FancyArrowPatch(p1,p2,arrowstyle="-|>",color=SLATE,lw=1.8,mutation_scale=15,zorder=1))
cbox(6,6.5,"Random variable X\n(a number for each outcome)",NAVY,NAVY,tc="white",w=4.6)
cbox(2.5,4.8,"pmf  p(x) = P(X = x)\ncdf  F(x) = P(X ≤ x)"); cbox(6,4.8,"Expectation E[X]\n(balance point)"); cbox(9.5,4.8,"Variance, SD\n(spread)")
cbox(2.5,3.0,"Bernoulli → Binomial\n(independence + counting)",BLUE,w=3.3); cbox(6,3.0,"Geometric,\nNegative binomial",EMER); cbox(9.5,3.0,"Hypergeometric\n(without replacement)",BLUE,w=3.2)
cbox(2.5,1.1,"Poisson\n(rare events, Ch 7)",BURG); cbox(6,1.1,"Choosing a distribution\n(decision tree)",GOLD,w=3.3); cbox(9.5,1.1,"Simulation check\n(Ch 17)",GOLD)
for b in [(2.5,5.3),(6,5.3),(9.5,5.3)]: link((6,6.0),b)
for xx in (2.5,6,9.5): link((xx,4.3),(xx,3.5)); link((xx,2.5),(xx,1.6))
link((4.0,4.8),(4.5,4.8)); link((7.5,4.8),(8.05,4.8))
save(fig,"SP_Fig_CH03_12.png")

# ---------- number checks ----------
def show(l,v): print(f"{l:<60} {v}")
show("3 vans pmf (p=0.23)",[round(binom.pmf(x,3,0.23),4) for x in range(4)])
show("3 vans cdf",[round(binom.cdf(x,3,0.23),4) for x in range(4)])
show("3 vans E, Var",(round(3*0.23,3),round(3*0.23*0.77,4)))
show("refund pmf E, E[X^2], Var, SD",(mu,(vals**2*probs).sum(),(vals**2*probs).sum()-mu**2,np.sqrt((vals**2*probs).sum()-mu**2)))
vA=np.array(A[0]);pA=np.array(A[1]);vB=np.array(Bv[0]);pB=np.array(Bv[1])
show("lead time P: mean,var,sd",((vA*pA).sum(),(vA**2*pA).sum()-(vA*pA).sum()**2,np.sqrt((vA**2*pA).sum()-(vA*pA).sum()**2)))
show("lead time Q: mean,var,sd",((vB*pB).sum(),(vB**2*pB).sum()-(vB*pB).sum()**2,np.sqrt((vB**2*pB).sum()-(vB*pB).sum()**2)))
show("12 vans P(0),P(<=2),P(>=4),E,Var,SD",(round(binom.pmf(0,12,.23),4),round(binom.cdf(2,12,.23),4),round(1-binom.cdf(3,12,.23),4),2.76,round(12*.23*.77,4),round(np.sqrt(12*.23*.77),3)))
show("12 vans P(=3),P(=2)",(round(binom.pmf(3,12,.23),4),round(binom.pmf(2,12,.23),4)))
show("QC 10 with replacement p=0.03: P(0),P(>=1),P(>=2)",(round(binom.pmf(0,10,.03),4),round(1-binom.pmf(0,10,.03),4),round(1-binom.cdf(1,10,.03),4)))
show("5 attempts p=0.4: P(X>=1) binomial",round(1-0.6**5,4))
show("geom p=0.4: P(1),P(2),P(3),P(X<=3),P(X>5),E",(0.4,0.24,0.144,round(1-0.6**3,4),round(0.6**5,5),2.5))
show("geom p=0.14 days until stop: E, P(X>10)",(round(1/0.14,2),round(0.86**10,4)))
show("negbin r=3,p=0.4: P(X=5), E",(round(comb(4,2)*0.4**3*0.6**2,4),7.5))
show("hypergeom N=20 D=3 n=4: P(0),P(1),P(>=1), E",(round(hypergeom.pmf(0,20,3,4),4),round(hypergeom.pmf(1,20,3,4),4),round(1-hypergeom.pmf(0,20,3,4),4),4*3/20))
show("hypergeom N=50 D=8 n=6: P(0), P(<=1)",(round(hypergeom.pmf(0,50,8,6),4),round(hypergeom.cdf(1,50,8,6),4)))
show("poisson 3/min: P(0),P(1),P(2),P(3),P(>=5), P(>=1)",[round(poisson.pmf(x,3),4) for x in range(4)]+[round(1-poisson.cdf(4,3),4),round(1-poisson.pmf(0,3),4)])
show("poisson 3/min -> 5 min lambda 15: P(<=10)",round(poisson.cdf(10,15),4))
show("complaints 1.2/day: P(0), P(>=3)",(round(poisson.pmf(0,1.2),4),round(1-poisson.cdf(2,1.2),4)))
show("fraud 500 x 0.005: binom P(0),P(>=5) vs poisson",(round(binom.pmf(0,500,.005),4),round(1-binom.cdf(4,500,.005),4),round(poisson.pmf(0,2.5),4),round(1-poisson.cdf(4,2.5),4)))
show("uniform 1..8: E, Var",(4.5,(8**2-1)/12))
# exercises
show("Ex pmf 2 machines fail 0.1,0.2: P(X=0,1,2)",(0.72,0.26,0.02))
show("Ex E[aX+b]: tips 3X+5 with E[X]=2.76",(3*2.76+5,9*12*.23*.77))
show("Ex binom n=8 p=0.15: P(0),P(1),P(>=2),E",(round(binom.pmf(0,8,.15),4),round(binom.pmf(1,8,.15),4),round(1-binom.cdf(1,8,.15),4),1.2))
show("Ex binom n=20 p=0.05 sensors: P(0),P(>=2)",(round(binom.pmf(0,20,.05),4),round(1-binom.cdf(1,20,.05),4)))
show("Ex geom p=0.25: P(X=4), P(X>4), E",(round(0.75**3*0.25,4),round(0.75**4,4),4))
show("Ex negbin r=2 p=0.3: P(X=4)",round(comb(3,1)*0.3**2*0.7**2,4))
show("Ex hyper N=30 D=5 n=5: P(0),P(>=1)",(round(hypergeom.pmf(0,30,5,5),4),round(1-hypergeom.pmf(0,30,5,5),4)))
show("Ex poisson 2/hr: P(0),P(>=3); 4 hrs lambda 8 P(<=5)",(round(poisson.pmf(0,2),4),round(1-poisson.cdf(2,2),4),round(poisson.cdf(5,8),4)))
show("Ex poisson approx 1000 x 0.002: P(>=1) exact, poisson",(round(1-binom.pmf(0,1000,.002),4),round(1-poisson.pmf(0,2),4)))
show("Boss: 12 vans P(<=1); 10 parcels 2 damaged inspect 3 P(0); calls 4/min P(>=7); contract E",(round(binom.cdf(1,12,.23),4),round(hypergeom.pmf(0,10,2,3),4),round(1-poisson.cdf(6,4),4),0.6*0+0.3*50+0.1*200))
