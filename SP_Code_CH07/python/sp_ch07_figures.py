"""SP_CH07 — Chapter 7 figures (Poisson process on R1) and number checks."""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from scipy.stats import poisson, gamma, binom, norm, expon
NAVY, GOLD, EMER, BURG, BLUE, CORAL, IVORY, SLATE = "#0B2545","#C9A227","#1B7F5C","#7A1E2B","#2E86AB","#E07A5F","#FBF8F1","#5B6B7C"
plt.rcParams.update({"font.size":14,"axes.titlesize":15,"axes.labelsize":14,"font.family":"DejaVu Sans","axes.edgecolor":SLATE,"axes.spines.top":False,"axes.spines.right":False,"axes.titlepad":10})
OUT="/home/claude/ch07/fig/"
def save(fig,name): fig.savefig(OUT+name,dpi=300,bbox_inches="tight",facecolor="white",pad_inches=0.15); plt.close(fig)
def rbox(ax,x,y,w,h,fc,ec,lw=2.5): ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0,rounding_size=0.12",fc=fc,ec=ec,lw=lw,zorder=2))
sep=lambda fig,xs: [fig.add_artist(plt.Line2D([x,x],[0.05,0.95],color=SLATE,lw=1.2,ls=":")) for x in xs]
lam=3
# 7.1 sample paths
rng=np.random.default_rng(71); fig,ax=plt.subplots(figsize=(11,4.8))
for k,c in enumerate([NAVY,GOLD,EMER]):
    arr=np.cumsum(rng.exponential(1/lam,40)); arr=arr[arr<=10]; ax.step(np.r_[0,arr],np.arange(0,len(arr)+1),where="post",color=c,lw=2,alpha=0.85,label=f"sample path {k+1}")
t=np.linspace(0,10,100); ax.plot(t,lam*t,color=BURG,ls="--",lw=2.5,label="mean function λt (λ = 3/min)")
ax.set_xlabel("t (minutes)"); ax.set_ylabel("N(t) = calls arrived by t"); ax.legend(frameon=False)
save(fig,"SP_Fig_CH07_01.png")
# 7.2 three definitions
fig,ax=plt.subplots(figsize=(13,5)); ax.axis("off"); ax.set_xlim(0,13); ax.set_ylim(0,5)
defs=[(2.2,"Definition 1\nCOUNTS","N(t+s) − N(s) ~ Pois(λt)\nindependent increments",NAVY),(6.5,"Definition 2\nTINY SLICES","P(one event in h) = λh + o(h)\nP(two or more) = o(h)",GOLD),(10.8,"Definition 3\nGAPS","gaps X₁, X₂, … i.i.d. Exp(λ)\nS_k = X₁+⋯+X_k ~ Erlang(k, λ)",EMER)]
for x,t,ex,c in defs:
    rbox(ax,x-1.9,1.5,3.8,2.6,IVORY,c); ax.text(x,3.55,t,ha="center",va="center",fontsize=13,color=c,fontweight="bold",zorder=3); ax.text(x,2.3,ex,ha="center",va="center",fontsize=11,color=NAVY,zorder=3,linespacing=1.5)
for a,b in [((4.2,2.8),(4.5,2.8)),((8.5,2.8),(8.8,2.8))]: ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle="<->",color=SLATE,lw=2.5))
ax.text(6.5,0.6,"All three describe the same process. Use whichever makes the question easy.",ha="center",fontsize=12.5,color=BURG,fontweight="bold")
ax.text(6.5,4.7,"THE POISSON PROCESS WITH RATE λ",ha="center",fontsize=14,color=NAVY,fontweight="bold")
save(fig,"SP_Fig_CH07_02.png")
# 7.3 tiny slices
fig,ax=plt.subplots(figsize=(11,3.4)); ax.axis("off"); ax.set_xlim(0,11); ax.set_ylim(0,3.4)
for i in range(20):
    x=0.5+i*0.5; ax.add_patch(Rectangle((x,1.2),0.46,0.8,fc=(BURG if i in (3,11,17) else IVORY),ec=NAVY,lw=1.2))
    if i in (3,11,17): ax.text(x+0.23,1.6,"1",ha="center",va="center",color="white",fontsize=11,fontweight="bold")
ax.annotate("",xy=(0.5,0.9),xytext=(0.96,0.9),arrowprops=dict(arrowstyle="<->",color=SLATE,lw=1.5)); ax.text(0.73,0.55,"h",ha="center",fontsize=12,color=SLATE)
ax.text(5.5,2.7,"Each slice of length h: a call with probability ≈ λh, no call with probability ≈ 1 − λh, two calls almost never",ha="center",fontsize=12,color=NAVY)
ax.text(5.5,0.3,"n = t/h slices  ⇒  N(t) ≈ Binomial(t/h, λh)  →  Poisson(λt)  as h → 0",ha="center",fontsize=12.5,color=BURG,fontweight="bold")
save(fig,"SP_Fig_CH07_03.png")
# 7.4 gaps and arrival times
gaps=np.array([0.45,0.20,0.62,0.15,0.38,0.52]); S=np.cumsum(gaps)
fig,ax=plt.subplots(figsize=(11,3.6)); ax.set_ylim(-1.2,1.6); ax.set_xlim(0,S[-1]+0.3); ax.set_yticks([]); ax.spines["left"].set_visible(False)
ax.hlines(0,0,S[-1]+0.3,color=NAVY,lw=3); ax.scatter(S,np.zeros(6),s=180,color=BURG,zorder=3)
prev=0
for i,(s,g) in enumerate(zip(S,gaps)):
    ax.annotate("",xy=(s,0.6),xytext=(prev,0.6),arrowprops=dict(arrowstyle="<->",color=GOLD,lw=2)); ax.text((prev+s)/2,0.75,f"X{i+1}",ha="center",fontsize=12,color=GOLD,fontweight="bold"); ax.text(s,-0.45,f"S{i+1}",ha="center",fontsize=12,color=BURG,fontweight="bold"); prev=s
ax.set_xlabel("time (minutes)"); ax.text(S[-1]/2,1.35,"gaps X_k ~ Exp(λ) i.i.d.      arrival times S_k = X₁ + ⋯ + X_k ~ Erlang(k, λ)",ha="center",fontsize=12.5,color=NAVY)
save(fig,"SP_Fig_CH07_04.png")
# 7.5 N(t)>=k <=> S_k<=t
fig,ax=plt.subplots(figsize=(10,4.2)); t=np.linspace(0,3,300)
ax.plot(t,1-poisson.cdf(2,lam*t),color=NAVY,lw=2.5,label="P(N(t) ≥ 3)  (count view)"); ax.plot(t,gamma.cdf(t,3,scale=1/lam),color=GOLD,lw=4,ls=":",label="P(S₃ ≤ t)  (gap view, Erlang)")
ax.set_xlabel("t (minutes)"); ax.set_ylabel("probability"); ax.legend(frameon=False); ax.set_title("Two views, one curve: the 3rd call has arrived by t  ⟺  at least 3 calls by t",color=NAVY,fontsize=12.5)
save(fig,"SP_Fig_CH07_05.png")
# 7.6 superposition
rng=np.random.default_rng(73); a1=np.cumsum(rng.exponential(1/3,30)); a1=a1[a1<6]; a2=np.cumsum(rng.exponential(1/2,20)); a2=a2[a2<6]
fig,ax=plt.subplots(figsize=(11,3.4)); ax.set_xlim(0,6); ax.set_ylim(-0.5,2.8); ax.set_yticks([0,1,2]); ax.set_yticklabels(["merged (λ = 5)","branch B (λ = 2)","branch A (λ = 3)"]); ax.spines["left"].set_visible(False)
ax.scatter(a1,np.full_like(a1,2),marker="|",s=300,color=NAVY,lw=2); ax.scatter(a2,np.ones_like(a2),marker="|",s=300,color=GOLD,lw=2); ax.scatter(a1,np.zeros_like(a1),marker="|",s=300,color=NAVY,lw=2); ax.scatter(a2,np.zeros_like(a2),marker="|",s=300,color=GOLD,lw=2)
ax.set_xlabel("time (minutes)"); ax.set_title("Superposition: two independent Poisson streams merge into one Poisson stream with rate 3 + 2 = 5",color=NAVY,fontsize=12)
save(fig,"SP_Fig_CH07_06.png")
# 7.7 thinning
rng=np.random.default_rng(74); a=np.cumsum(rng.exponential(1/3,30)); a=a[a<6]; typ=rng.random(len(a))<0.3
fig,ax=plt.subplots(figsize=(11,3.4)); ax.set_xlim(0,6); ax.set_ylim(-0.5,2.8); ax.set_yticks([0,1,2]); ax.set_yticklabels(["sales calls (λ = 2.1)","complaints (λ = 0.9)","all calls (λ = 3)"]); ax.spines["left"].set_visible(False)
ax.scatter(a,np.full_like(a,2),marker="|",s=300,color=NAVY,lw=2); ax.scatter(a[typ],np.ones(typ.sum()),marker="|",s=300,color=BURG,lw=2); ax.scatter(a[~typ],np.zeros((~typ).sum()),marker="|",s=300,color=EMER,lw=2)
ax.set_xlabel("time (minutes)"); ax.set_title("Thinning: each call is a complaint with probability 0.30, independently → two independent Poisson streams",color=NAVY,fontsize=12)
save(fig,"SP_Fig_CH07_07.png")
# 7.8 conditional uniform
rng=np.random.default_rng(75); fig,axs=plt.subplots(3,1,figsize=(11,3.8),gridspec_kw={"hspace":0.9})
for ax in axs:
    pts=np.sort(rng.uniform(0,10,30)); ax.set_xlim(0,10); ax.set_ylim(-0.5,0.5); ax.set_yticks([]); ax.spines["left"].set_visible(False); ax.scatter(pts,np.zeros(30),marker="|",s=250,color=NAVY,lw=1.8); ax.axvspan(0,3,color=GOLD,alpha=0.25)
axs[2].set_xlabel("time (minutes)"); axs[0].set_title("Three realizations of 30 arrivals in [0, 10], given N(10) = 30",color=NAVY,fontsize=12.5)
save(fig,"SP_Fig_CH07_08.png")
# 7.9 nonhomogeneous
fig,axs=plt.subplots(1,2,figsize=(13,4.4),gridspec_kw={"wspace":0.3}); t=np.linspace(8,18,500)
lamt=np.where(t<10,2,np.where(t<13,4,np.where(t<15,2.5,3)))
axs[0].step(t,lamt,where="post",color=NAVY,lw=2.5); axs[0].fill_between(t,lamt,step="post",color=GOLD,alpha=0.3); axs[0].set_xlabel("hour of day"); axs[0].set_ylabel("λ(t) calls per minute"); axs[0].set_ylim(0,5); axs[0].set_title("(a) Time-varying rate λ(t)",color=NAVY)
m=np.cumsum(lamt)*(t[1]-t[0])*60; axs[1].plot(t,m,color=BURG,lw=2.5); axs[1].set_xlabel("hour of day"); axs[1].set_ylabel("m(t) = expected calls since 8:00"); axs[1].set_title("(b) Mean function m(t) = ∫ λ(s) ds",color=NAVY)
sep(fig,[0.5]); save(fig,"SP_Fig_CH07_09.png")
# 7.10 compound Poisson revenue
rng=np.random.default_rng(76); arr=np.cumsum(rng.exponential(1/3,40)); arr=arr[arr<10]; vals=rng.lognormal(np.log(60),0.6,len(arr))
fig,ax=plt.subplots(figsize=(11,4.4)); ax.step(np.r_[0,arr],np.r_[0,np.cumsum(vals)],where="post",color=NAVY,lw=2.5); ax.plot([0,10],[0,10*3*71.8],color=GOLD,ls="--",lw=2.5,label="mean function λ·E[X]·t")
ax.set_xlabel("t (minutes)"); ax.set_ylabel("revenue so far (€)"); ax.legend(frameon=False); ax.set_title("A compound Poisson process: jumps at Poisson instants, jump sizes = order values",color=NAVY,fontsize=12.5)
save(fig,"SP_Fig_CH07_10.png")
# 7.11 simulation check
rng=np.random.default_rng(77); counts=[]
for _ in range(10000):
    s=np.cumsum(rng.exponential(1/lam,60)); counts.append((s<=5).sum())
counts=np.array(counts); k=np.arange(0,35)
fig,ax=plt.subplots(figsize=(11,4.6)); ax.bar(k-0.18,np.bincount(counts,minlength=35)[:35]/10000,width=0.36,color=NAVY,label="simulated N(5) from exponential gaps (10,000 runs, seed 77)"); ax.bar(k+0.18,poisson.pmf(k,15),width=0.36,color=GOLD,label="Poisson(15) pmf")
ax.set_xlabel("calls in 5 minutes"); ax.set_ylabel("probability"); ax.set_ylim(0,0.145); ax.legend(frameon=False,fontsize=11,loc="upper right")
save(fig,"SP_Fig_CH07_11.png"); print("sim N(5) mean",counts.mean(),"var",counts.var(),"P(=12)",(counts==12).mean())
# 7.12 concept map
fig,ax=plt.subplots(figsize=(12,7)); ax.axis("off"); ax.set_xlim(0,12); ax.set_ylim(0,7.3); ax.set_aspect("equal")
def cbox(x,y,t,c=NAVY,fc=IVORY,w=2.9,h=1.0,tc=None): rbox(ax,x-w/2,y-h/2,w,h,fc,c,2.2); ax.text(x,y,t,ha="center",va="center",fontsize=11.5,color=tc or NAVY,fontweight="bold",zorder=3,linespacing=1.3)
def link(p1,p2): ax.add_patch(FancyArrowPatch(p1,p2,arrowstyle="-|>",color=SLATE,lw=1.8,mutation_scale=15,zorder=1))
cbox(6,6.5,"Poisson process N(t), rate λ",NAVY,NAVY,tc="white",w=4.6)
cbox(2.5,4.8,"Def 1: counts\nPois(λt), indep. incr."); cbox(6,4.8,"Def 2: tiny slices\nλh + o(h)"); cbox(9.5,4.8,"Def 3: gaps\nExp(λ), S_k Erlang")
cbox(2.5,3.0,"Superposition &\nthinning",BLUE); cbox(6,3.0,"Conditional uniform\narrival times",EMER); cbox(9.5,3.0,"N(t) ≥ k ⟺ S_k ≤ t",CORAL)
cbox(2.5,1.1,"Nonhomogeneous\nλ(t), m(t)",GOLD); cbox(6,1.1,"Compound Poisson\n(revenue)",GOLD); cbox(9.5,1.1,"Queues (Ch 8),\nCTMC (Ch 11)",GOLD)
for b in [(2.5,5.3),(6,5.3),(9.5,5.3)]: link((6,6.0),b)
for xx in (2.5,6,9.5): link((xx,4.3),(xx,3.5)); link((xx,2.5),(xx,1.6))
save(fig,"SP_Fig_CH07_12.png")
# ---------- checks ----------
def show(l,v): print(f"{l:<62} {v}")
show("Ex 7.1 N(5)~Pois(15): P(=12), P(<=10), P(>=20), E, SD",(round(poisson.pmf(12,15),4),round(poisson.cdf(10,15),4),round(1-poisson.cdf(19,15),4),15,round(np.sqrt(15),2)))
show("Ex 7.2 P(N(2)-N(1)>=2)",round(1-poisson.cdf(1,3),4))
show("Ex 7.3 P(N(1)=2,N(3)=7)=P(N1=2)P(N2=5)",(round(poisson.pmf(2,3),4),round(poisson.pmf(5,6),4),round(poisson.pmf(2,3)*poisson.pmf(5,6),5)))
show("Ex 7.4 P(N(3)=7 | N(1)=2)=P(N(2)=5)",round(poisson.pmf(5,6),4))
show("Ex 7.5 h=1s: lambda h",(3/60,round(1-np.exp(-0.05),4),round(poisson.pmf(0,0.05),4),round(1-poisson.cdf(1,0.05),6)))
show("Ex 7.7 P(X1>1), E, P(X1<0.25)",(round(np.exp(-3),4),round(1/3,3),round(1-np.exp(-0.75),4)))
show("Ex 7.8 S3: E, SD, P(S3>1)=P(N(1)<=2)",(1,round(np.sqrt(3)/3,3),round(poisson.cdf(2,3),4)))
show("Ex 7.9 S10: E, SD, P(S10<=2.5)=P(N(2.5)>=10)",(round(10/3,2),round(np.sqrt(10)/3,3),round(1-poisson.cdf(9,7.5),4)))
show("Ex 7.11 merged 5/min: P(N(2)=10), E",(round(poisson.pmf(10,10),4),10))
show("Ex 7.12 P(next call from A)=3/5; P(first 3 all from A)",(0.6,round(0.6**3,3)))
show("Ex 7.13 complaints 0.9/min: P(0 in 2 min); P(sales N=4 in 1 min)",(round(np.exp(-1.8),4),round(poisson.pmf(4,2.1),4)))
show("Ex 7.14 P(complaints=2 | total=5 in 1 min)=binom",round(binom.pmf(2,5,0.3),4))
show("Ex 7.15 given N(10)=30: E in first 3, P(exactly 9), P(<=5)",(9,round(binom.pmf(9,30,.3),4),round(binom.cdf(5,30,.3),4)))
show("Ex 7.16 given N(1)=3 all in last 15s",round(0.25**3,5))
show("Ex 7.17 expected total wait given n=30 in [0,10]: n*t/2",30*5)
show("Ex 7.18 NHPP 9-12: m = 60*(1*4+... )",(60*(2*2+3*4+2*2.5+3*3)))
show("Ex 7.18 9:00-12:00: (9-10: 2, 10-12: 4) -> 120+480",(600,round(1-norm.cdf((650.5-600)/np.sqrt(600)),4)))
show("Ex 7.19 8:00-8:30 lambda 2: 60; P(N<=50)",round(poisson.cdf(50,60),4))
show("Ex 7.20 compound: E rev 10 min, Var",(round(30*71.8,1),round(np.sqrt(30*(48**2+71.8**2)),1)))
show("Ex 7.21 insurance-like: claims Pois(6) x 300",(1800,round(np.sqrt(6*(200**2+300**2)))))
show("Ex 7.22 estimate: 1,350 calls in 450 min; CI",(3.0,round(1.96*np.sqrt(1350)/450,3)))
show("Ex 7.22 dispersion: counts mean 3.02 var 3.1","ok")
show("Ex 7.23 spatial: 0.5 defects/m2, 4 m2 -> Pois(2): P(0)",round(np.exp(-2),4))
# exercises
show("Exercise: Pois(4/min) N(3)=12: P(=12), P>=15",(round(poisson.pmf(12,12),4),round(1-poisson.cdf(14,12),4)))
show("Exercise: P(N(2)=3, N(5)=9)",(round(poisson.pmf(3,6)*poisson.pmf(6,9),5)))
show("Exercise: P(N(4)=8|N(1)=2)",round(poisson.pmf(6,9),4))
show("Exercise: gap >40s rate 3",round(np.exp(-2),4))
show("Exercise: S5 E,SD, P(S5<=1)",(round(5/3,3),round(np.sqrt(5)/3,3),round(1-poisson.cdf(4,3),4)))
show("Exercise: merged 3+1.5=4.5: P(N(2)=9), P(next from second)",(round(poisson.pmf(9,9),4),round(1.5/4.5,3)))
show("Exercise: thinning 0.25 fraud-like: P(2 in 10 min at 0.75/min)",round(poisson.pmf(2,7.5),4))
show("Exercise: given N(20)=50, first 5 min: Binom(50,.25): E, P(>=20)",(12.5,round(1-binom.cdf(19,50,.25),4)))
show("Exercise: NHPP 2,4,2.5 for 1h each: m, P(N>500)",(60*8.5,round(1-poisson.cdf(500,510),4)))
show("Exercise: compound 20/day repairs mean 300 sd 200: Var",(6000,round(np.sqrt(20*(200**2+300**2)))))
show("Exercise: estimate 480 calls in 120 min -> 4; CI",(4,round(1.96*np.sqrt(480)/120,3)))
show("Boss: N(15) at 3: P(>=55)",round(1-poisson.cdf(54,45),4))
show("Boss: S_20 at 3: E, P(S20>8)=P(N(8)<=19)",(round(20/3,2),round(poisson.cdf(19,24),4)))
show("Boss: peak 4/min thinning 0.3 complaints: 1.2/min; P(0 complaints in 2 min)",round(np.exp(-2.4),4))
show("Boss: given 45 in 15 min, in last 5: Binom(45,1/3) E; P(>=20)",(15,round(1-binom.cdf(19,45,1/3),4)))
