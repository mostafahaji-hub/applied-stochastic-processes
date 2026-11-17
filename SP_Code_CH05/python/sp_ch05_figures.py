"""SP_CH05 — Chapter 5 figures and number checks (several random variables, conditioning, LLN, CLT)."""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from scipy.stats import norm, binom, poisson
NAVY, GOLD, EMER, BURG, BLUE, CORAL, IVORY, SLATE = "#0B2545","#C9A227","#1B7F5C","#7A1E2B","#2E86AB","#E07A5F","#FBF8F1","#5B6B7C"
plt.rcParams.update({"font.size":14,"axes.titlesize":15,"axes.labelsize":14,"font.family":"DejaVu Sans","axes.edgecolor":SLATE,"axes.spines.top":False,"axes.spines.right":False,"axes.titlepad":10})
OUT="/home/claude/ch05/fig/"
def save(fig,name): fig.savefig(OUT+name,dpi=300,bbox_inches="tight",facecolor="white",pad_inches=0.15); plt.close(fig)
def rbox(ax,x,y,w,h,fc,ec,lw=2.5): ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0,rounding_size=0.12",fc=fc,ec=ec,lw=lw,zorder=2))
sep=lambda fig,xs: [fig.add_artist(plt.Line2D([x,x],[0.05,0.95],color=SLATE,lw=1.2,ls=":")) for x in xs]
J=np.array([[0.45,0.10,0.02],[0.15,0.12,0.05],[0.03,0.05,0.03]])  # rows X=0,1,2 (late vans among 2); cols Y=0,1,2 (complaints)
# Fig 5.1 joint table heat
fig,ax=plt.subplots(figsize=(9,5.6)); ax.axis("off"); ax.set_xlim(0,9); ax.set_ylim(0,6)
for i in range(3):
    for j in range(3):
        v=J[i,j]; c=plt.cm.Blues(0.15+1.6*v); rbox(ax,1.8+j*1.7,4.0-i*1.2,1.5,1.0,c,NAVY,1.5); ax.text(2.55+j*1.7,4.5-i*1.2,f"{v:.2f}",ha="center",va="center",fontsize=15,color=NAVY if v<0.3 else "white",fontweight="bold",zorder=3)
for i in range(3): ax.text(1.2,4.5-i*1.2,f"X = {i}",ha="center",va="center",fontsize=14,color=NAVY,fontweight="bold"); rbox(ax,7.1,4.0-i*1.2,1.4,1.0,IVORY,GOLD); ax.text(7.8,4.5-i*1.2,f"{J[i].sum():.2f}",ha="center",va="center",fontsize=14,color=NAVY,fontweight="bold",zorder=3)
for j in range(3): ax.text(2.55+j*1.7,5.4,f"Y = {j}",ha="center",va="center",fontsize=14,color=NAVY,fontweight="bold"); rbox(ax,1.8+j*1.7,0.7,1.5,1.0,IVORY,GOLD); ax.text(2.55+j*1.7,1.2,f"{J[:,j].sum():.2f}",ha="center",va="center",fontsize=14,color=NAVY,fontweight="bold",zorder=3)
ax.text(7.8,5.4,"P(X = x)",ha="center",fontsize=12,color=GOLD,fontweight="bold"); ax.text(0.9,1.2,"P(Y = y)",ha="center",fontsize=12,color=GOLD,fontweight="bold")
ax.text(4.25,5.85,"Y = complaints in the day",ha="center",fontsize=12,color=SLATE); ax.text(0.25,3.3,"X = late vans\n(of two)",ha="center",va="center",fontsize=11,color=SLATE,rotation=90)
save(fig,"SP_Fig_CH05_01.png")
# Fig 5.2 conditional pmfs of Y given X
fig,axs=plt.subplots(1,3,figsize=(15,4.2),gridspec_kw={"wspace":0.3})
for i,ax in enumerate(axs):
    cond=J[i]/J[i].sum(); b=ax.bar([0,1,2],cond,color=[SLATE,GOLD,BURG][i],width=0.55)
    for bi,v in zip(b,cond): ax.text(bi.get_x()+bi.get_width()/2,v+0.02,f"{v:.2f}",ha="center",fontsize=12,color=NAVY,fontweight="bold")
    ax.set_xticks([0,1,2]); ax.set_ylim(0,1); ax.set_xlabel("y (complaints)"); ax.set_ylabel("P(Y = y | X = x)"); ax.set_title(f"({'abc'[i]}) given X = {i} late vans   E[Y | X={i}] = {(cond*np.array([0,1,2])).sum():.2f}",color=NAVY,fontsize=12.5)
sep(fig,[0.365,0.66]); save(fig,"SP_Fig_CH05_02.png")
# Fig 5.3 correlation clouds
rng=np.random.default_rng(5)
fig,axs=plt.subplots(1,3,figsize=(15,4.4),gridspec_kw={"wspace":0.3})
for ax,r,t in zip(axs,[-0.8,0,0.8],["(a) ρ = −0.8: more staff → fewer long waits","(b) ρ = 0: unrelated","(c) ρ = +0.8: more rain → more late vans"]):
    z=rng.multivariate_normal([0,0],[[1,r],[r,1]],400); ax.scatter(z[:,0],z[:,1],s=14,color=NAVY,alpha=0.6); ax.set_title(t,color=NAVY,fontsize=12); ax.set_xticks([]); ax.set_yticks([]); ax.set_xlabel("X"); ax.set_ylabel("Y")
sep(fig,[0.365,0.66]); save(fig,"SP_Fig_CH05_03.png")
# Fig 5.4 variance of a sum vs correlation (two routes with sd 30 each)
fig,ax=plt.subplots(figsize=(10,4.6)); rho=np.linspace(-1,1,200); sd=np.sqrt(2*30**2+2*rho*30**2)
ax.plot(rho,sd,color=NAVY,lw=2.5); ax.axhline(np.sqrt(2)*30,color=GOLD,ls="--",lw=2); ax.text(-0.95,44,"independent: 30√2 ≈ 42.4",color=GOLD,fontsize=12,fontweight="bold")
ax.scatter([-1,0,1],[0,30*np.sqrt(2),60],color=BURG,s=70,zorder=3); ax.text(1,56,"ρ = 1: 60",ha="right",color=BURG,fontsize=12); ax.text(-0.98,3,"ρ = −1: 0",color=BURG,fontsize=12)
ax.set_xlabel("correlation ρ between the two routes’ daily demands"); ax.set_ylabel("SD of total demand"); ax.set_ylim(0,65)
save(fig,"SP_Fig_CH05_04.png")
# Fig 5.5 tower rule tree
fig,ax=plt.subplots(figsize=(12,4.8)); ax.axis("off"); ax.set_xlim(0,12); ax.set_ylim(0,5)
ax.scatter([0.8],[2.5],s=300,color=NAVY,zorder=3)
ax.plot([0.8,3.9],[2.5,3.8],color=NAVY,lw=2.5); ax.plot([0.8,3.9],[2.5,1.2],color=GOLD,lw=2.5)
ax.text(2.3,3.45,"Rain  0.30",color=NAVY,fontsize=13,fontweight="bold",ha="center",bbox=dict(boxstyle="round,pad=0.2",fc="white",ec="none")); ax.text(2.3,1.55,"Dry  0.70",color=NAVY,fontsize=13,fontweight="bold",ha="center",bbox=dict(boxstyle="round,pad=0.2",fc="white",ec="none"))
rbox(ax,3.9,3.3,7.4,1.0,IVORY,NAVY); ax.text(7.6,3.8,"E[X | Rain] = 12 × 0.40 = 4.80 late vans",ha="center",va="center",fontsize=12.5,color=NAVY,zorder=3)
rbox(ax,3.9,0.7,7.4,1.0,IVORY,GOLD); ax.text(7.6,1.2,"E[X | Dry] = 12 × 0.157 = 1.88 late vans",ha="center",va="center",fontsize=12.5,color=NAVY,zorder=3)
ax.text(6.0,-0.0,"E[X] = 0.30 × 4.80 + 0.70 × 1.88 = 2.76   (tower rule)",ha="center",color=EMER,fontsize=14,fontweight="bold")
save(fig,"SP_Fig_CH05_05.png")
# Fig 5.6 mixture: rainy/dry late vans vs plain binomial
rng=np.random.default_rng(12); n=20000; rain=rng.random(n)<0.3; p=np.where(rain,0.40,0.157); mix=rng.binomial(12,p); plain=rng.binomial(12,0.23,n)
fig,ax=plt.subplots(figsize=(11,4.8)); k=np.arange(13)
ax.bar(k-0.18,np.bincount(plain,minlength=13)/n,width=0.36,color=GOLD,label=f"one weather, p = 0.23  (var {plain.var():.2f})"); ax.bar(k+0.18,np.bincount(mix,minlength=13)/n,width=0.36,color=NAVY,label=f"rain/dry mixture  (var {mix.var():.2f})")
ax.set_xticks(k); ax.set_xlabel("late vans in a day (of 12)"); ax.set_ylabel("frequency"); ax.legend(frameon=False)
save(fig,"SP_Fig_CH05_06.png"); print("mix var",mix.var(),"plain var",plain.var(),"means",mix.mean(),plain.mean())
# Fig 5.7 random sum diagram
fig,ax=plt.subplots(figsize=(11,3.8)); ax.axis("off"); ax.set_xlim(0,11); ax.set_ylim(0,3.8)
rbox(ax,0.3,1.3,2.6,1.2,NAVY,NAVY); ax.text(1.6,1.9,"N orders today\n~ Pois(500)",ha="center",va="center",color="white",fontsize=12.5,fontweight="bold",zorder=3)
for i,x in enumerate([3.5,5.0,6.5]): rbox(ax,x,1.3,1.2,1.2,IVORY,GOLD); ax.text(x+0.6,1.9,f"X{i+1}\n€",ha="center",va="center",color=NAVY,fontsize=12,zorder=3)
ax.text(8.1,1.9,"…",fontsize=22,color=NAVY,va="center"); rbox(ax,8.6,1.3,1.2,1.2,IVORY,GOLD); ax.text(9.2,1.9,"X_N\n€",ha="center",va="center",color=NAVY,fontsize=12,zorder=3)
ax.text(5.5,0.5,"S = X₁ + X₂ + ⋯ + X_N  (a random number of random terms)",ha="center",color=NAVY,fontsize=13,fontweight="bold")
ax.text(5.5,3.3,"E[S] = E[N]·E[X]        Var(S) = E[N]·Var(X) + Var(N)·E[X]²",ha="center",color=EMER,fontsize=13,fontweight="bold")
save(fig,"SP_Fig_CH05_07.png")
# Fig 5.8 LLN running mean of exponential waits
rng=np.random.default_rng(7); w=rng.exponential(1/3,5000); run=np.cumsum(w)/np.arange(1,5001)
fig,ax=plt.subplots(figsize=(11,4.6)); ax.plot(np.arange(1,5001),run,color=NAVY,lw=1.8,label="running average of waiting times"); ax.axhline(1/3,color=GOLD,ls="--",lw=2.5,label="true mean 1/λ = 0.333 min")
ax.set_xscale("log"); ax.set_xlabel("number of calls observed (log scale)"); ax.set_ylabel("average wait so far (min)"); ax.set_ylim(0,0.7); ax.legend(frameon=False)
save(fig,"SP_Fig_CH05_09.png")
# Fig 5.9 CLT panels
rng=np.random.default_rng(55); fig,axs=plt.subplots(2,3,figsize=(15,7.2),gridspec_kw={"wspace":0.3,"hspace":0.45})
for row,(gen,name) in enumerate([(lambda m: rng.random((20000,m)),"uniform(0,1)"),(lambda m: rng.exponential(1,(20000,m)),"exponential(1)")]):
    for col,m in enumerate([1,5,30]):
        ax=axs[row,col]; s=gen(m).mean(axis=1); ax.hist(s,bins=50,density=True,color=NAVY if row==0 else BURG,alpha=0.85,edgecolor="white")
        mu=s.mean(); sd=s.std(); x=np.linspace(s.min(),s.max(),200); ax.plot(x,norm.pdf(x,mu,sd),color=GOLD,lw=2.5)
        ax.set_title(f"mean of n = {m} {name}",color=NAVY,fontsize=12); ax.set_yticks([])
save(fig,"SP_Fig_CH05_10.png")
# Fig 5.10 Chebyshev vs normal
fig,ax=plt.subplots(figsize=(10,4.6)); k=np.linspace(1,4,200); ax.plot(k,1/k**2,color=BURG,lw=2.5,label="Chebyshev bound 1/k² (any distribution)"); ax.plot(k,2*(1-norm.cdf(k)),color=NAVY,lw=2.5,label="exact for the normal")
ax.set_xlabel("k (number of standard deviations from the mean)"); ax.set_ylabel("P(|X − μ| ≥ kσ)"); ax.set_ylim(0,1.05); ax.legend(frameon=False)
save(fig,"SP_Fig_CH05_08.png")
# Fig 5.11 concept map
fig,ax=plt.subplots(figsize=(12,7)); ax.axis("off"); ax.set_xlim(0,12); ax.set_ylim(0,7.3); ax.set_aspect("equal")
def cbox(x,y,t,c=NAVY,fc=IVORY,w=2.9,h=1.0,tc=None): rbox(ax,x-w/2,y-h/2,w,h,fc,c,2.2); ax.text(x,y,t,ha="center",va="center",fontsize=11.5,color=tc or NAVY,fontweight="bold",zorder=3,linespacing=1.3)
def link(p1,p2): ax.add_patch(FancyArrowPatch(p1,p2,arrowstyle="-|>",color=SLATE,lw=1.8,mutation_scale=15,zorder=1))
cbox(6,6.5,"Several random variables together",NAVY,NAVY,tc="white",w=5.2)
cbox(2.5,4.8,"Joint, marginal,\nconditional pmf/pdf",w=3.2); cbox(6,4.8,"Covariance, correlation\nVar(X+Y)"); cbox(9.5,4.8,"Conditional expectation\n& the tower rule",w=3.2)
cbox(2.5,3.0,"Independence of\nrandom variables",BLUE); cbox(6,3.0,"Random sums\nE[N]E[X]",EMER); cbox(9.5,3.0,"Computing by\nconditioning (Ch 9)",CORAL)
cbox(2.5,1.1,"Markov & Chebyshev\ninequalities",GOLD); cbox(6,1.1,"Law of large numbers",GOLD); cbox(9.5,1.1,"Central limit theorem\n(why the normal)",GOLD)
for b in [(2.5,5.3),(6,5.3),(9.5,5.3)]: link((6,6.0),b)
for xx in (2.5,6,9.5): link((xx,4.3),(xx,3.5)); link((xx,2.5),(xx,1.6))
save(fig,"SP_Fig_CH05_11.png")
# ---- checks ----
def show(l,v): print(f"{l:<62} {v}")
x=np.array([0,1,2]); pX=J.sum(axis=1); pY=J.sum(axis=0)
EX=(x*pX).sum(); EY=(x*pY).sum(); EXY=sum(i*j*J[i,j] for i in range(3) for j in range(3))
VX=(x**2*pX).sum()-EX**2; VY=(x**2*pY).sum()-EY**2; cov=EXY-EX*EY; rho=cov/np.sqrt(VX*VY)
show("joint: pX, pY",(pX.round(2),pY.round(2)))
show("E[X],E[Y],E[XY],Cov,VarX,VarY,rho",(round(EX,3),round(EY,3),round(EXY,3),round(cov,4),round(VX,4),round(VY,4),round(rho,3)))
show("P(Y|X=2), E[Y|X=2]; P(X|Y=2)",((J[2]/J[2].sum()).round(3),round((x*J[2]/J[2].sum()).sum(),3),(J[:,2]/J[:,2].sum()).round(3)))
show("E[Y|X=x] for x=0,1,2",[round((x*J[i]/J[i].sum()).sum(),3) for i in range(3)])
show("tower check sum pX*E[Y|X]",round(sum(pX[i]*(x*J[i]/J[i].sum()).sum() for i in range(3)),3))
show("Var(X+Y) = VX+VY+2cov",round(VX+VY+2*cov,4))
show("independence test J[0,0] vs pX0*pY0",(J[0,0],round(pX[0]*pY[0],4)))
show("two routes sd 30, rho 0.5: sd total",round(np.sqrt(2*900+2*0.5*900),2))
show("mixture E, Var (law of total variance)",(round(0.3*4.8+0.7*1.884,3),round(0.3*12*.4*.6+0.7*12*.157*.843 + (0.3*4.8**2+0.7*1.884**2-(0.3*4.8+0.7*1.884)**2),3)))
show("first-step E[trials] p=0.4",2.5)
show("random sum N~Pois(500), X mean 71.8 sd 48: E[S], SD[S]",(round(500*71.8),round(np.sqrt(500*48**2+500*71.8**2),0)))
show("Markov: E=18.5 refund, P(X>=100)<=",round(18.5/100,3))
show("Chebyshev k=2,3",(0.25,round(1/9,3)))
show("CLT 100 exp service mean 2 sd 2: P(sum>230)",round(1-norm.cdf((230-200)/20),4))
show("CLT 50 orders lognormal mean 71.8 sd 48: P(mean<65)",round(norm.cdf((65-71.8)/(48/np.sqrt(50))),4))
show("B(400,.23) via CLT P>=110",round(1-norm.cdf((109.5-92)/np.sqrt(400*.23*.77)),4))
show("CI preview n=100 xbar=21 s=5: 95% CI",(21-1.96*0.5,21+1.96*0.5))
