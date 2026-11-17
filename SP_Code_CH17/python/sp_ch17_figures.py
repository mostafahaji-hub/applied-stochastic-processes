"""SP_CH17 — Part VI opener and Chapter 17 figures (Monte Carlo basics)."""
import numpy as np, matplotlib, sys
matplotlib.use("Agg"); sys.path.insert(0,"/home/claude/ch17/code")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from scipy.stats import weibull_min
from sp_ch17_mc import *
from sp_ch14_sa import F
NAVY, GOLD, EMER, BURG, BLUE, CORAL, IVORY, SLATE = "#0B2545","#C9A227","#1B7F5C","#7A1E2B","#2E86AB","#E07A5F","#FBF8F1","#5B6B7C"
plt.rcParams.update({"font.size":14,"axes.titlesize":15,"axes.labelsize":14,"font.family":"DejaVu Sans","axes.edgecolor":SLATE,"axes.spines.top":False,"axes.spines.right":False,"axes.titlepad":10})
OUT="/home/claude/ch17/fig/"
def save(fig,name): fig.savefig(OUT+name,dpi=300,bbox_inches="tight",facecolor="white",pad_inches=0.15); plt.close(fig)
def rbox(ax,x,y,w,h,fc,ec,lw=2.5): ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0,rounding_size=0.12",fc=fc,ec=ec,lw=lw,zorder=2))
sep=lambda fig,xs: [fig.add_artist(plt.Line2D([x,x],[0.05,0.95],color=SLATE,lw=1.2,ls=":")) for x in xs]
# Part VI opener
fig,ax=plt.subplots(figsize=(14,5)); ax.axis("off"); ax.set_xlim(0,14); ax.set_ylim(0,5)
parts=[("I","Probability\nfrom Zero","1–5",SLATE),("II","Arrivals\nand Waiting","6–8",SLATE),("III","The Markov\nWorld","9–12",SLATE),("IV","Continuous\nStates","13",SLATE),("V","Inside\nMetaheuristics","14–16",SLATE),("VI","Monte Carlo\nSimulation","17–19",GOLD)]
for i,(n,t,chs,c) in enumerate(parts):
    x=0.4+i*2.3; rbox(ax,x,1.4,2.0,2.4,IVORY if c==SLATE else "#F7F0DC",c,3 if c==GOLD else 1.8); ax.text(x+1,3.3,f"PART {n}",ha="center",fontsize=13,color=c if c==GOLD else NAVY,fontweight="bold",zorder=3); ax.text(x+1,2.45,t,ha="center",va="center",fontsize=12,color=NAVY,zorder=3); ax.text(x+1,1.65,f"Ch {chs}",ha="center",fontsize=11,color=SLATE,zorder=3)
    if i<5: ax.add_patch(FancyArrowPatch((x+2.05,2.6),(x+2.25,2.6),arrowstyle="-|>",color=SLATE,lw=1.5,mutation_scale=14))
ax.text(7,4.6,"You are here: simulation itself becomes the object of study",ha="center",fontsize=14,color=GOLD,fontweight="bold")
ax.text(7,0.6,"Part VI explains where random numbers come from, how processes are simulated, and how precise simulated answers are.",ha="center",fontsize=11.5,color=SLATE)
save(fig,"SP_Fig_CH17_00_PartVI.png")
# 17.1 generators
fig,axs=plt.subplots(1,3,figsize=(17,5),gridspec_kw={"wspace":0.3})
seq=lcg(5,3,16,7,16); axs[0].plot(range(17),seq,"-o",color=NAVY,lw=1.8,ms=6); axs[0].set_xlabel("step k"); axs[0].set_ylabel("xₖ"); axs[0].set_title("(a) x ← (5x + 3) mod 16: all 16 values, then repeats",color=NAVY,fontsize=12); axs[0].set_yticks(range(0,16,3))
x=np.array(lcg(37,1,256,0,256))/256; axs[1].scatter(x[:-1],x[1:],s=10,color=BURG); axs[1].set_xlabel("uₖ"); axs[1].set_ylabel("uₖ₊₁"); axs[1].set_title("(b) small LCG (m = 256): pairs on a lattice",color=NAVY,fontsize=12); axs[1].set_aspect("equal")
rng=np.random.default_rng(1701); y=rng.random(257); axs[2].scatter(y[:-1],y[1:],s=10,color=EMER); axs[2].set_xlabel("uₖ"); axs[2].set_ylabel("uₖ₊₁"); axs[2].set_title("(c) modern generator (PCG64): no visible pattern",color=NAVY,fontsize=12); axs[2].set_aspect("equal")
sep(fig,[0.36,0.65]); save(fig,"SP_Fig_CH17_01.png")
# 17.2 inverse transform Weibull
fig,axs=plt.subplots(1,2,figsize=(13,4.8),gridspec_kw={"wspace":0.3}); t=np.linspace(0,30,400); Fw=weibull_min.cdf(t,2.5,scale=12)
axs[0].plot(t,Fw,color=NAVY,lw=2.5)
for j,(u,c) in enumerate([(0.3,GOLD),(0.5,EMER),(0.9,BURG)]):
    xx=weib_inv(u,2.5,12); axs[0].annotate("",xy=(xx,u),xytext=(0,u),arrowprops=dict(arrowstyle="-",color=c,lw=1.8,ls="--")); axs[0].annotate("",xy=(xx,0),xytext=(xx,u),arrowprops=dict(arrowstyle="-|>",color=c,lw=1.8)); axs[0].text(xx+0.4,0.04+0.08*j,f"x = {xx:.2f}",color=c,fontsize=11,fontweight="bold"); axs[0].text(0.3,u+0.025,f"u = {u}",color=c,fontsize=11)
axs[0].set_xlabel("tire life x (months)"); axs[0].set_ylabel("F(x) = 1 − e^(−(x/12)^2.5)"); axs[0].set_title("(a) from u on the vertical axis to x = F⁻¹(u)",color=NAVY,fontsize=12.5); axs[0].set_xlim(0,30); axs[0].set_ylim(0,1.02)
rng=np.random.default_rng(172); s=weib_inv(rng.random(10000),2.5,12); axs[1].hist(s,bins=50,density=True,color=GOLD,alpha=0.8,edgecolor="white",label="10,000 simulated lives"); axs[1].plot(t,weibull_min.pdf(t,2.5,scale=12),color=NAVY,lw=2.5,label="Weibull(2.5, 12) density"); axs[1].set_xlabel("months"); axs[1].legend(frameon=False,fontsize=11); axs[1].set_title("(b) the samples follow the target law",color=NAVY,fontsize=12.5)
sep(fig,[0.5]); save(fig,"SP_Fig_CH17_02.png")
# 17.3 discrete inverse transform
fig,ax=plt.subplots(figsize=(10,4.6)); vals=[0,20,50,100]; cdf=np.cumsum([0.5,0.3,0.15,0.05]); cols=[NAVY,GOLD,EMER,BURG]
for i,(v,cc) in enumerate(zip(vals,cdf)):
    lo=0 if i==0 else cdf[i-1]; ax.add_patch(plt.Rectangle((0,lo),0.18,cc-lo,fc=cols[i],ec="white",lw=2))
    ax.text(0.24,0.5*(lo+cc),f"u in ({lo:.2f}, {cc:.2f}]   →   refund {v} €   (probability {cc-lo:.2f})",va="center",fontsize=12,color=cols[i],fontweight="bold")
ax.set_xlim(0,1); ax.set_ylim(0,1); ax.set_xticks([]); ax.set_ylabel("u ~ U(0, 1)"); ax.spines["bottom"].set_visible(False); ax.set_title("Cutting [0, 1] into pieces of length 0.5, 0.3, 0.15 and 0.05",color=NAVY,fontsize=12.5)
save(fig,"SP_Fig_CH17_03.png")
# 17.4 acceptance–rejection
rng=np.random.default_rng(174); u1=rng.random(2000); u2=rng.random(2000)*1.5; acc=u2<=6*u1*(1-u1)
fig,ax=plt.subplots(figsize=(10,4.6)); ax.scatter(u1[acc],u2[acc],s=8,color=EMER,label=f"accepted ({acc.mean():.1%})"); ax.scatter(u1[~acc],u2[~acc],s=8,color=BURG,alpha=0.6,label="rejected")
xx=np.linspace(0,1,200); ax.plot(xx,6*xx*(1-xx),color=NAVY,lw=2.5,label="target f(x) = 6x(1 − x)"); ax.axhline(1.5,color=GOLD,lw=2.5,label="envelope c = 1.5")
ax.set_xlabel("x (share of a shift used by a repair)"); ax.set_ylabel("height"); ax.set_ylim(0,2.05); ax.legend(frameon=False,fontsize=10.5,loc="upper center",ncol=2)
save(fig,"SP_Fig_CH17_04.png")
# 17.5 running estimate of P(late)
fig,ax=plt.subplots(figsize=(11,4.6)); n=np.arange(1,20001)
for sd,c in [(1751,NAVY),(1752,GOLD),(1753,EMER)]:
    rng=np.random.default_rng(sd); rain=rng.random(20000)<0.3; late=np.where(rain,rng.random(20000)<0.40,rng.random(20000)<0.157); ax.plot(n,np.cumsum(late)/n,color=c,lw=1.4)
p=0.2299; ax.fill_between(n,p-1.96*np.sqrt(p*(1-p)/n),p+1.96*np.sqrt(p*(1-p)/n),color=SLATE,alpha=0.15,label="p ± 1.96√(p(1−p)/n)"); ax.axhline(p,color=BURG,ls="--",lw=2,label="exact 0.2299 (Chapter 2)")
ax.set_xscale("log"); ax.set_xlim(10,20000); ax.set_ylim(0,0.5); ax.set_xlabel("simulated days n (log scale)"); ax.set_ylabel("running estimate of P(van 7 late)"); ax.legend(frameon=False,fontsize=11)
save(fig,"SP_Fig_CH17_05.png")
# 17.6 SE vs n
fig,ax=plt.subplots(figsize=(10,4.6)); n=np.logspace(2,6,50)
for s_,c,lab in [(np.sqrt(0.23*0.77),NAVY,"P(late): σ = 0.42"),(4.556,GOLD,"tire life: σ = 4.56 months"),(25.55,BURG,"refund: σ = 25.55 €")]: ax.loglog(n,1.96*s_/np.sqrt(n),color=c,lw=2.5,label=lab)
ax.set_xlabel("number of simulated values n"); ax.set_ylabel("95% half-width 1.96σ/√n"); ax.legend(frameon=False,fontsize=11); ax.text(1.5e2,0.006,"four times n  →  half the error",color=SLATE,fontsize=12)
save(fig,"SP_Fig_CH17_06.png")
# 17.7 rare events
fig,ax=plt.subplots(figsize=(10,4.6)); p=np.logspace(-6,-0.3,100); ax.loglog(p,(1.96/0.1)**2*(1-p)/p,color=NAVY,lw=2.5)
for pp,lab,c in [(0.23,"van late 0.23",EMER),(2/720,"random sequence optimal 0.0028",GOLD),(4.8e-5,"cash touches −10k (from 20k) 4.8×10⁻⁵",BURG)]:
    nn=(1.96/0.1)**2*(1-pp)/pp; ax.scatter([pp],[nn],color=c,s=70,zorder=3); ax.text(pp*1.3,nn*1.3,f"{lab}: n ≈ {nn:,.0f}",color=c,fontsize=10.5)
ax.set_xlabel("probability p being estimated"); ax.set_ylabel("runs for ±10% relative error"); ax.set_xlim(1e-6,1)
save(fig,"SP_Fig_CH17_07.png")
# 17.8 variance reduction
rng=np.random.default_rng(178); U=rng.random(200000); L=weib_inv(U,2.5,12); Y=-np.log(1-U); b=np.cov(L,Y)[0,1]/Y.var()
ep=[];ea=[];ec=[]
for r in range(2000):
    u=rng.random(100); l=weib_inv(u,2.5,12); ep.append(l.mean()); u2=rng.random(50); ea.append(0.5*(weib_inv(u2,2.5,12)+weib_inv(1-u2,2.5,12)).mean()); ec.append(l.mean()-b*((-np.log(1-u)).mean()-1))
fig,ax=plt.subplots(figsize=(11,4.6)); bins=np.linspace(9,12.3,70)
ax.hist(ep,bins=bins,color=SLATE,alpha=0.6,label=f"plain (SD {np.std(ep):.3f})"); ax.hist(ec,bins=bins,color=GOLD,alpha=0.7,label=f"control variate (SD {np.std(ec):.3f})"); ax.hist(ea,bins=bins,color=NAVY,alpha=0.8,label=f"antithetic pairs (SD {np.std(ea):.3f})")
ax.axvline(TIRE_MEAN,color=BURG,ls="--",lw=2,label="exact 10.65"); ax.set_xlabel("estimate of mean tire life from 100 uniforms"); ax.set_ylabel("count (2,000 repetitions)"); ax.legend(frameon=False,fontsize=10.5)
save(fig,"SP_Fig_CH17_08.png"); print("VR SDs",np.std(ep).round(4),np.std(ea).round(4),np.std(ec).round(4),"b",round(b,3))
# 17.9 CRN
rng=np.random.default_rng(179); dI=[];dC=[]
for r in range(1000):
    La=weib_inv(rng.random(1000),2.5,12); Lb=weib_inv(rng.random(1000),2.5,12)
    dI.append(tire_cost_rate(Lb,6)-tire_cost_rate(La,5)); dC.append(tire_cost_rate(La,6)-tire_cost_rate(La,5))
fig,ax=plt.subplots(figsize=(11,4.6)); bins=np.linspace(-5,6,80)
ax.hist(dI,bins=bins,color=SLATE,alpha=0.6,label=f"independent random numbers (SD {np.std(dI):.2f}; wrong sign {np.mean(np.array(dI)<0):.0%})"); ax.hist(dC,bins=bins,color=NAVY,alpha=0.8,label=f"common random numbers (SD {np.std(dC):.2f}; wrong sign {np.mean(np.array(dC)<0):.0%})")
ax.axvline(0.867,color=BURG,ls="--",lw=2,label="exact difference 0.87 €/month"); ax.axvline(0,color=GOLD,lw=1.5)
ax.set_xlabel("estimated cost difference: replace at 6 months minus at 5 months (€/month)"); ax.set_ylabel("count (1,000 studies)"); ax.legend(frameon=False,fontsize=10.5,loc="upper center",bbox_to_anchor=(0.5,-0.2),ncol=1)
save(fig,"SP_Fig_CH17_09.png"); print("CRN",np.mean(dI).round(3),np.std(dI).round(3),np.mean(dC).round(3),np.std(dC).round(3),np.mean(np.array(dI)<0).round(3),np.mean(np.array(dC)<0).round(3))
# 17.10 audit
items=[("P(van 7 late), n = 1,000",0.246,0.0136,0.2299),("mean refund (€), n = 1,000",18.69,0.805,18.5),("mean tardiness of a random sequence, n = 100",35.02,0.986,34.1),("cash runway h(2), n = 10,000",0.3805,0.00486,0.382),("mean tire life (months), n = 1,000",10.738,0.142,10.647)]
fig,ax=plt.subplots(figsize=(11,4.6))
for i,(lab,est,se,ex) in enumerate(items):
    ax.errorbar(est/ex,i,xerr=1.96*se/ex,fmt="o",color=NAVY,ms=8,capsize=6,lw=2); ax.text(1.24,i,lab,va="center",fontsize=11,color=NAVY)
ax.axvline(1,color=BURG,ls="--",lw=2); ax.set_yticks([]); ax.set_xlim(0.85,1.75); ax.set_xlabel("estimate ÷ exact value, with 95% interval"); ax.spines["left"].set_visible(False)
save(fig,"SP_Fig_CH17_10.png")
# 17.11 concept map
fig,ax=plt.subplots(figsize=(12,7)); ax.axis("off"); ax.set_xlim(0,12); ax.set_ylim(0,7.3); ax.set_aspect("equal")
def cbox(x,y,t,c=NAVY,fc=IVORY,w=2.9,h=1.0,tc=None): rbox(ax,x-w/2,y-h/2,w,h,fc,c,2.2); ax.text(x,y,t,ha="center",va="center",fontsize=11.5,color=tc or NAVY,fontweight="bold",zorder=3,linespacing=1.3)
def link(p1,p2): ax.add_patch(FancyArrowPatch(p1,p2,arrowstyle="-|>",color=SLATE,lw=1.8,mutation_scale=15,zorder=1))
cbox(6,6.5,"Monte Carlo = answers from many random repetitions",NAVY,NAVY,tc="white",w=6.8)
cbox(2.5,4.8,"Pseudo-random u:\nLCG, seeds, period",w=3.0); cbox(6,4.8,"Any distribution:\ninverse, accept–reject",w=3.2); cbox(9.5,4.8,"Estimate ± error:\nCLT, 1.96σ/√n",w=3.1)
cbox(2.5,3.0,"Reproducibility:\nreport the seed",BLUE,w=3.0); cbox(6,3.0,"Sample size n\n(rare events cost more)",CORAL,w=3.2); cbox(9.5,3.0,"Variance reduction:\nantithetic, control, CRN",EMER,w=3.3)
cbox(2.5,1.1,"Chapters 1, 3, 4\n(u, laws)",GOLD,w=2.9); cbox(6,1.1,"Chapter 5\n(CLT, intervals)",GOLD,w=2.9); cbox(9.5,1.1,"Chapters 18–19\n(processes, output)",GOLD,w=3.0)
for b_ in [(2.5,5.3),(6,5.3),(9.5,5.3)]: link((6,6.0),b_)
for xx in (2.5,6,9.5): link((xx,4.3),(xx,3.5)); link((xx,2.5),(xx,1.6))
save(fig,"SP_Fig_CH17_11.png")
