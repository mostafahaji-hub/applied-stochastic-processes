"""SP_CH19 — Chapter 19 figures (output analysis, MCMC, importance sampling, the book in one picture). Reads ch19_results.json."""
import numpy as np, matplotlib, sys, json
matplotlib.use("Agg"); sys.path.insert(0,"/home/claude/ch19/code")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from scipy.stats import gamma as G
from sp_ch19_output import *
NAVY, GOLD, EMER, BURG, BLUE, CORAL, IVORY, SLATE = "#0B2545","#C9A227","#1B7F5C","#7A1E2B","#2E86AB","#E07A5F","#FBF8F1","#5B6B7C"
plt.rcParams.update({"font.size":14,"axes.titlesize":15,"axes.labelsize":14,"font.family":"DejaVu Sans","axes.edgecolor":SLATE,"axes.spines.top":False,"axes.spines.right":False,"axes.titlepad":10})
OUT="/home/claude/ch19/fig/"; R=json.load(open("/home/claude/ch19/code/ch19_results.json"))
def save(fig,name): fig.savefig(OUT+name,dpi=300,bbox_inches="tight",facecolor="white",pad_inches=0.15); plt.close(fig)
def rbox(ax,x,y,w,h,fc,ec,lw=2.5): ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0,rounding_size=0.12",fc=fc,ec=ec,lw=lw,zorder=2))
sep=lambda fig,xs: [fig.add_artist(plt.Line2D([x,x],[0.05,0.95],color=SLATE,lw=1.2,ls=":")) for x in xs]
# 19.1 terminating: days and half-width
sl=np.array(R["sl"]["E"]); fig,axs=plt.subplots(1,2,figsize=(13,4.6),gridspec_kw={"wspace":0.3})
axs[0].scatter(sl,np.random.default_rng(1).uniform(-0.3,0.3,len(sl)),s=18,color=SLATE,alpha=0.7,label="100 simulated days"); m,h=ci(sl); axs[0].errorbar(m,-0.6,xerr=h,fmt="o",color=NAVY,ms=9,capsize=7,lw=2.5,label=f"mean {m:.3f} ± {h:.3f}")
axs[0].set_yticks([]); axs[0].set_ylim(-1,0.6); axs[0].set_xlabel("daily share answered within 30 s (scenario E)"); axs[0].legend(frameon=False,fontsize=10.5,loc="upper left"); axs[0].spines["left"].set_visible(False); axs[0].set_title("(a) Day-to-day variation and the 95% interval",color=NAVY,fontsize=12.5)
n=np.arange(5,1001); s=sl.std(ddof=1); axs[1].loglog(n,1.96*s/np.sqrt(n),color=NAVY,lw=2.5); axs[1].axhline(0.01,color=GOLD,ls="--",lw=1.8); axs[1].axhline(0.005,color=BURG,ls="--",lw=1.8)
axs[1].text(130,0.0108,"±0.01 needs 121 days",color=GOLD,fontsize=11); axs[1].text(500,0.0054,"±0.005 needs 483",color=BURG,fontsize=11); axs[1].set_xlabel("number of simulated days n"); axs[1].set_ylabel("95% half-width"); axs[1].set_title("(b) Precision grows like √n",color=NAVY,fontsize=12.5)
sep(fig,[0.5]); save(fig,"SP_Fig_CH19_01.png")
# 19.2 Welch
g=np.array(R["welch"]["grid"]); fig,ax=plt.subplots(figsize=(11,4.6)); ax.plot(g,R["welch"]["q"],color=SLATE,lw=1,alpha=0.7,label="average of 200 replications started empty"); ax.plot(g,R["welch"]["ma15"],color=NAVY,lw=2.8,label="moving average (window ±75 min)")
ax.axhline(6.86,color=BURG,ls="--",lw=2,label="steady state 6.86"); ax.axvspan(0,150,color=GOLD,alpha=0.15); ax.text(8,8.6,"warm-up to delete ≈ 150 min",color=DGOLD if False else "#8A6D1F",fontsize=11.5,fontweight="bold")
ax.set_xlabel("minutes since an empty start (M/M/5, λ = 3)"); ax.set_ylabel("callers waiting"); ax.set_ylim(0,9.5); ax.legend(frameon=False,fontsize=10.5,loc="lower right")
save(fig,"SP_Fig_CH19_02.png")
# 19.3 autocorrelation
lags=np.array(R["acf"]["lags"]); r=np.array(R["acf"]["r"]); fig,ax=plt.subplots(figsize=(10,4.4)); ax.plot(lags,r,color=NAVY,lw=2.5); ax.axhline(0,color=SLATE,lw=1)
ax.set_xlabel("lag k (customers apart)"); ax.set_ylabel("autocorrelation of waits"); ax.text(600,0.8,"successive waits are almost identical:\nlag 1: 0.99, lag 100: 0.58, lag 1000: ≈ 0",color=BURG,fontsize=12)
save(fig,"SP_Fig_CH19_03.png")
# 19.4 batch means
bm=R["bm"]; fig,ax=plt.subplots(figsize=(10,4.4)); b=[x[0] for x in bm]; se=[x[1] for x in bm]
ax.semilogx(b,se,"-o",color=NAVY,lw=2.5,ms=8); ax.text(1.3,se[0]+0.6,f"naive SE {se[0]:.2f} s",color=BURG,fontsize=11.5); ax.text(1500,se[4]-1.6,"plateau ≈ 8–9 s:\nthe honest standard error",color=EMER,fontsize=11.5)
ax.set_xlabel("batch size b (customers per batch)"); ax.set_ylabel("standard error of the mean wait (s)"); ax.set_ylim(0,11)
save(fig,"SP_Fig_CH19_04.png")
# 19.5 Bonferroni
fig,ax=plt.subplots(figsize=(10,4.2)); ks=["A","B","C","D"]
for i,k in enumerate(ks):
    m,h=R["bonf"][k]; ax.errorbar(m,i,xerr=h,fmt="o",color=NAVY,ms=8,capsize=6,lw=2.5); ax.text(m+h+0.01,i,f"E − {k}: {m:.3f} ± {h:.3f}",va="center",fontsize=11.5,color=NAVY)
ax.axvline(0,color=BURG,ls="--",lw=2); ax.set_yticks([]); ax.set_xlim(-0.05,0.55); ax.set_xlabel("difference in daily service level (paired; simultaneous 95%)"); ax.spines["left"].set_visible(False)
save(fig,"SP_Fig_CH19_05.png")
# 19.6 MCMC posterior of the failure rate
m1=R["mcmc1"]; fig,axs=plt.subplots(1,2,figsize=(13,4.6),gridspec_kw={"wspace":0.3})
axs[0].plot(m1["chain"][:3000],color=NAVY,lw=0.8); axs[0].axvline(1000,color=GOLD,ls="--",lw=1.8); axs[0].text(1050,0.45,"burn-in",color="#8A6D1F",fontsize=11); axs[0].set_xlabel("iteration"); axs[0].set_ylabel("λ (failures per shift)"); axs[0].set_title("(a) Trace: started at 0.5, settles within ~50 steps",color=NAVY,fontsize=12.5)
x=np.linspace(0.02,0.35,300); axs[1].hist(m1["sample"],bins=50,density=True,color=GOLD,alpha=0.8,edgecolor="white",label="MCMC sample"); axs[1].plot(x,G.pdf(x,14,scale=1/94),color=NAVY,lw=2.5,label="exact posterior Gamma(14, 94)")
axs[1].set_xlabel("λ"); axs[1].legend(frameon=False,fontsize=10.5,loc="upper right"); axs[1].set_title("(b) The sample matches the exact posterior",color=NAVY,fontsize=12.5)
sep(fig,[0.5]); save(fig,"SP_Fig_CH19_06.png")
# 19.7 tuning
fig,axs=plt.subplots(1,3,figsize=(17,4.2),sharey=True,gridspec_kw={"wspace":0.12})
for ax,tt,c in zip(axs,R["tuning"],[BURG,EMER,BLUE]):
    ax.plot(tt["trace"],color=c,lw=0.8); ax.set_title(f"proposal SD {tt['sd']}: accept {tt['acc']:.0%}, ESS {tt['ess']:.0f}",color=NAVY,fontsize=12.5); ax.set_xlabel("iteration")
axs[0].set_ylabel("λ"); sep(fig,[0.365,0.645]); save(fig,"SP_Fig_CH19_07.png")
# 19.8 Weibull posterior and T*
W=R["weib"]; fig,axs=plt.subplots(1,2,figsize=(13,4.6),gridspec_kw={"wspace":0.3})
axs[0].scatter(W["k"],W["eta"],s=8,color=NAVY,alpha=0.4); axs[0].scatter([2.5],[12],color=BURG,s=420,marker="*",edgecolor="white",linewidth=1.5,zorder=5,label="values used in Chapters 4–12"); axs[0].set_xlabel("shape k"); axs[0].set_ylabel("scale η (months)"); axs[0].legend(frameon=False,fontsize=11); axs[0].set_title("(a) Posterior of (k, η) from 20 tire lives",color=NAVY,fontsize=12.5)
ts=np.array(W["Tstar"]); vals,cnt=np.unique(ts,return_counts=True); axs[1].bar(vals,cnt/len(ts),width=0.2,color=GOLD); axs[1].axvline(5,color=BURG,ls="--",lw=2,label="policy of Chapter 12: T = 5")
axs[1].set_xlabel("optimal replacement age T* (months)"); axs[1].set_ylabel("posterior probability"); axs[1].legend(frameon=False,fontsize=11); axs[1].set_title("(b) Uncertainty about the best policy",color=NAVY,fontsize=12.5)
sep(fig,[0.5]); save(fig,"SP_Fig_CH19_08.png")
# 19.9 importance sampling
I=R["is"]; fig,ax=plt.subplots(figsize=(11,4.6)); xp=np.arange(len(I["plain_cum"]))*200+1; xi=np.arange(len(I["is_cum"]))*20+1
ax.plot(xp,np.array(I["plain_cum"])*1e5,color=SLATE,lw=2,label=f"plain Monte Carlo ({I['plain_hits']} ruins in 200,000 runs)"); ax.plot(xi,np.array(I["is_cum"])*1e5,color=NAVY,lw=2.5,label="importance sampling (tilted walk, 20,000 runs)")
ax.axhline(I["exact"]*1e5,color=BURG,ls="--",lw=2,label=f"exact {I['exact']:.2e} (dynamic programming)"); ax.set_xscale("log"); ax.set_xlabel("number of simulated quarters"); ax.set_ylabel("estimate × 10⁵"); ax.set_ylim(0,12); ax.legend(frameon=False,fontsize=10.5)
save(fig,"SP_Fig_CH19_09.png")
# 19.10 the book in one picture
fig,ax=plt.subplots(figsize=(14,8.4)); ax.axis("off"); ax.set_xlim(0,14); ax.set_ylim(0,8.4)
parts=[(1.6,7.0,"I  Probability\nfrom zero\nCh 1–5",SLATE),(5.2,7.0,"II  Arrivals\nand waiting\nCh 6–8",BLUE),(8.8,7.0,"III  The Markov\nworld\nCh 9–12",EMER),(12.4,7.0,"IV  Continuous\nstates\nCh 13",CORAL),(8.8,3.9,"V  Inside\nmetaheuristics\nCh 14–16",GOLD),(3.4,3.9,"VI  Monte Carlo\nsimulation\nCh 17–19",BURG)]
for x,y,t,c in parts: rbox(ax,x-1.3,y-0.8,2.6,1.6,IVORY,c,3); ax.text(x,y,t,ha="center",va="center",fontsize=11.5,color=NAVY,fontweight="bold",zorder=3)
for a_,b_ in [((2.95,7.0),(3.85,7.0)),((6.55,7.0),(7.45,7.0)),((10.15,7.0),(11.05,7.0)),((8.8,6.15),(8.8,4.75)),((7.45,3.9),(4.75,3.9)),((3.4,4.75),(1.9,6.15))]:
    ax.add_patch(FancyArrowPatch(a_,b_,arrowstyle="-|>",color=SLATE,lw=2.2,mutation_scale=18))
for x,y,lab in [(3.4,5.85,"conditioning,\nexponential"),(7.0,5.85,"memoryless ⇒ Markov"),(10.6,5.85,"refine the walk ⇒\nBrownian motion"),(10.2,5.3,"chains on\nsolutions"),(6.1,3.2,"every number\nwas simulated"),(1.3,5.0,"LLN, CLT ⇒\n±1.96σ/√n")]:
    ax.text(x,y,lab,ha="center",fontsize=10.5,color=SLATE,style="italic")
rbox(ax,0.6,0.25,12.8,1.75,"#F7F0DC",GOLD,2); ax.text(7,1.45,"Nava Company — six reference problems",ha="center",fontsize=12.5,color=NAVY,fontweight="bold",zorder=3)
ax.text(7,0.75,"R1 call center  ·  R2 packing line  ·  R3 customer club  ·  R4 demand & cash  ·  R5 repair shop & fleet  ·  R6 bottleneck scheduling",ha="center",fontsize=11,color=NAVY,zorder=3)
save(fig,"SP_Fig_CH19_10.png")
# 19.11 concept map
fig,ax=plt.subplots(figsize=(12,7)); ax.axis("off"); ax.set_xlim(0,12); ax.set_ylim(0,7.3); ax.set_aspect("equal")
def cbox(x,y,t,c=NAVY,fc=IVORY,w=2.9,h=1.0,tc=None): rbox(ax,x-w/2,y-h/2,w,h,fc,c,2.2); ax.text(x,y,t,ha="center",va="center",fontsize=11.5,color=tc or NAVY,fontweight="bold",zorder=3,linespacing=1.3)
def link(p1,p2): ax.add_patch(FancyArrowPatch(p1,p2,arrowstyle="-|>",color=SLATE,lw=1.8,mutation_scale=15,zorder=1))
cbox(6,6.5,"Trusting simulated answers; sampling the unknown",NAVY,NAVY,tc="white",w=7.4)
cbox(2.5,4.8,"Terminating runs:\nreplications, CIs",w=3.0); cbox(6,4.8,"Steady state: warm-up\n(Welch), batch means",w=3.3); cbox(9.5,4.8,"Comparisons: paired,\nCRN, Bonferroni",w=3.2)
cbox(2.5,3.0,"MCMC: Metropolis–\nHastings, detailed balance",EMER,w=3.4); cbox(6,3.0,"Diagnostics: trace,\nACF, ESS, tuning",BLUE,w=3.1); cbox(9.5,3.0,"Rare events:\nimportance sampling",CORAL,w=3.1)
cbox(2.5,1.1,"Ch 10, 14\n(stationary law)",GOLD,w=2.8); cbox(6,1.1,"Ch 6, 17\n(AR(1), √n)",GOLD,w=2.8); cbox(9.5,1.1,"Ch 13, 17\n(rare cash risk)",GOLD,w=2.8)
for b_ in [(2.5,5.3),(6,5.3),(9.5,5.3)]: link((6,6.0),b_)
for xx in (2.5,6,9.5): link((xx,4.3),(xx,3.5)); link((xx,2.5),(xx,1.6))
save(fig,"SP_Fig_CH19_11.png")
