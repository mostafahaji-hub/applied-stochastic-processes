"""SP_CH13 — Part IV opener and Chapter 13 figures (Brownian motion, Gaussian processes) + number checks."""
import numpy as np, matplotlib, sys
matplotlib.use("Agg"); sys.path.insert(0,"/home/claude/ch13/code")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from scipy.stats import norm
from sp_ch13_brownian import *
NAVY, GOLD, EMER, BURG, BLUE, CORAL, IVORY, SLATE = "#0B2545","#C9A227","#1B7F5C","#7A1E2B","#2E86AB","#E07A5F","#FBF8F1","#5B6B7C"
plt.rcParams.update({"font.size":14,"axes.titlesize":15,"axes.labelsize":14,"font.family":"DejaVu Sans","axes.edgecolor":SLATE,"axes.spines.top":False,"axes.spines.right":False,"axes.titlepad":10})
OUT="/home/claude/ch13/fig/"
def save(fig,name): fig.savefig(OUT+name,dpi=300,bbox_inches="tight",facecolor="white",pad_inches=0.15); plt.close(fig)
def rbox(ax,x,y,w,h,fc,ec,lw=2.5): ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0,rounding_size=0.12",fc=fc,ec=ec,lw=lw,zorder=2))
sep=lambda fig,xs: [fig.add_artist(plt.Line2D([x,x],[0.05,0.95],color=SLATE,lw=1.2,ls=":")) for x in xs]
mu,s=MU_R4,SIG_R4
# Part IV opener
fig,ax=plt.subplots(figsize=(14,5)); ax.axis("off"); ax.set_xlim(0,14); ax.set_ylim(0,5)
parts=[("I","Probability\nfrom Zero","1–5",SLATE),("II","Arrivals\nand Waiting","6–8",SLATE),("III","The Markov\nWorld","9–12",SLATE),("IV","Continuous\nStates","13",GOLD),("V","Inside\nMetaheuristics","14–16",SLATE),("VI","Monte Carlo\nSimulation","17–19",SLATE)]
for i,(n,t,chs,c) in enumerate(parts):
    x=0.4+i*2.3; rbox(ax,x,1.4,2.0,2.4,IVORY if c==SLATE else "#F7F0DC",c,3 if c==GOLD else 1.8); ax.text(x+1,3.3,f"PART {n}",ha="center",fontsize=13,color=c if c==GOLD else NAVY,fontweight="bold",zorder=3); ax.text(x+1,2.45,t,ha="center",va="center",fontsize=12,color=NAVY,zorder=3); ax.text(x+1,1.65,f"Ch {chs}",ha="center",fontsize=11,color=SLATE,zorder=3)
    if i<5: ax.add_patch(FancyArrowPatch((x+2.05,2.6),(x+2.25,2.6),arrowstyle="-|>",color=SLATE,lw=1.5,mutation_scale=14))
ax.text(7,4.6,"You are here: the state itself becomes continuous",ha="center",fontsize=14,color=GOLD,fontweight="bold")
ax.text(7,0.6,"Part IV follows quantities that can take any value at any instant: cash, cumulative demand, prices.",ha="center",fontsize=11.5,color=SLATE)
save(fig,"SP_Fig_CH13_00_PartIV.png")
# 13.1 refining the walk
rng=np.random.default_rng(131); fig,axs=plt.subplots(1,3,figsize=(16,4.6),gridspec_kw={"wspace":0.25})
for ax,(dt,lab) in zip(axs,[(1,"(a) 1 step per day, size ±1"),(0.25,"(b) 4 steps per day, size ±0.5"),(0.01,"(c) 100 steps per day, size ±0.1")]):
    n=int(30/dt); t=np.linspace(0,30,n+1)
    for k,c in enumerate([NAVY,GOLD,EMER]):
        st=np.where(rng.random(n)<0.5,1,-1)*np.sqrt(dt); ax.plot(t,np.r_[0,np.cumsum(st)],color=c,lw=1.6 if dt==1 else 1.1,drawstyle="steps-post" if dt==1 else "default")
    tt=np.linspace(0,30,200); ax.plot(tt,2*np.sqrt(tt),color=SLATE,ls="--",lw=1.3); ax.plot(tt,-2*np.sqrt(tt),color=SLATE,ls="--",lw=1.3)
    ax.set_ylim(-13,13); ax.set_xlabel("days"); ax.set_title(lab,color=NAVY,fontsize=12.5)
axs[0].set_ylabel("cash change (thousand €)"); sep(fig,[0.365,0.645]); save(fig,"SP_Fig_CH13_01.png")
# 13.2 standard BM paths with bands
rng=np.random.default_rng(132); t,X=bm_paths(6,30,0.01,rng)
fig,ax=plt.subplots(figsize=(11,4.6)); cols=[NAVY,GOLD,EMER,BURG,BLUE,CORAL]
for k in range(6): ax.plot(t,X[k],color=cols[k],lw=1.2)
ax.fill_between(t,-2*np.sqrt(t),2*np.sqrt(t),color=SLATE,alpha=0.10,label="± 2√t (95%)"); ax.fill_between(t,-np.sqrt(t),np.sqrt(t),color=SLATE,alpha=0.18,label="± √t (68%)")
ax.set_xlabel("t (days)"); ax.set_ylabel("W(t)"); ax.legend(frameon=False,loc="upper left"); ax.set_xlim(0,30)
save(fig,"SP_Fig_CH13_02.png")
# 13.3 self-similarity zoom
rng=np.random.default_rng(133); n=100000; dW=rng.standard_normal(n)*np.sqrt(1/n); W=np.r_[0,np.cumsum(dW)]; t=np.linspace(0,1,n+1)
fig,axs=plt.subplots(1,2,figsize=(13,4.4),gridspec_kw={"wspace":0.3})
axs[0].plot(t,W,color=NAVY,lw=0.7); axs[0].axvspan(0,0.01,color=GOLD,alpha=0.4); axs[0].set_title("(a) one path on [0, 1]; gold strip = [0, 0.01]",color=NAVY,fontsize=12.5); axs[0].set_xlabel("t")
m=t<=0.01; axs[1].plot(t[m]*100,W[m]*10,color=BURG,lw=0.8); axs[1].set_title("(b) the strip stretched ×100 in time, ×10 in value",color=NAVY,fontsize=12.5); axs[1].set_xlabel("100·t")
sep(fig,[0.5]); save(fig,"SP_Fig_CH13_03.png")
# 13.4 quadratic vs total variation
rng=np.random.default_rng(134); N=2**16; dW=rng.standard_normal(N)*np.sqrt(1/N); ns=2**np.arange(2,17)
qv=[]; tv=[]
for nn in ns:
    inc=dW.reshape(nn,-1).sum(axis=1); qv.append((inc**2).sum()); tv.append(np.abs(inc).sum())
fig,axs=plt.subplots(1,2,figsize=(13,4.4),gridspec_kw={"wspace":0.3})
axs[0].semilogx(ns,qv,"-o",color=NAVY,lw=2,ms=5); axs[0].axhline(1,color=GOLD,ls="--",lw=2); axs[0].set_title("(a) Σ (ΔW)² → t = 1 (quadratic variation)",color=NAVY,fontsize=12.5); axs[0].set_xlabel("number of pieces n"); axs[0].set_ylim(0,2)
axs[1].loglog(ns,tv,"-o",color=BURG,lw=2,ms=5); axs[1].loglog(ns,np.sqrt(2*ns/np.pi),color=GOLD,ls="--",lw=2,label="√(2n/π)"); axs[1].set_title("(b) Σ |ΔW| → ∞ (no finite length)",color=NAVY,fontsize=12.5); axs[1].set_xlabel("number of pieces n"); axs[1].legend(frameon=False)
sep(fig,[0.5]); save(fig,"SP_Fig_CH13_04.png")
# 13.5 Brownian bridge (90-day project)
rng=np.random.default_rng(135); T=90; t,X=bm_paths(6,T,0.05,rng); Bb=X-(t/T)*X[:,-1:]
fig,ax=plt.subplots(figsize=(11,4.6))
for k in range(6): ax.plot(t,Bb[k],color=cols[k],lw=1.2)
ax.fill_between(t,-2*np.sqrt(t*(T-t)/T),2*np.sqrt(t*(T-t)/T),color=GOLD,alpha=0.25,label="bridge ± 2 SD: 2√(t(90−t)/90)"); ax.plot(t,2*np.sqrt(t),color=SLATE,ls="--",lw=1.5,label="free walk ± 2√t"); ax.plot(t,-2*np.sqrt(t),color=SLATE,ls="--",lw=1.5)
ax.set_xlabel("project day"); ax.set_ylabel("net project cash (thousand €)"); ax.legend(frameon=False,loc="upper left",fontsize=11); ax.set_xlim(0,90)
save(fig,"SP_Fig_CH13_05.png")
# 13.6 R4 cash with drift
rng=np.random.default_rng(136); t,X=bm_paths(12,90,0.1,rng,mu=mu,sigma=s,x0=20)
fig,ax=plt.subplots(figsize=(11,4.8))
for k in range(12): ax.plot(t,X[k],color=NAVY,lw=0.9,alpha=0.55)
ax.plot(t,20+mu*t,color=GOLD,lw=2.5,label="mean 20 + 0.1t"); ax.fill_between(t,20+mu*t-2*s*np.sqrt(t),20+mu*t+2*s*np.sqrt(t),color=GOLD,alpha=0.15,label="± 2σ√t"); ax.axhline(-10,color=BURG,ls="--",lw=2,label="credit limit −10")
ax.set_xlabel("day"); ax.set_ylabel("cash (thousand €)"); ax.set_xlim(0,90); ax.legend(frameon=False,loc="upper left",fontsize=11)
save(fig,"SP_Fig_CH13_06.png")
# 13.7 reflection principle
rng=np.random.default_rng(13); 
while True:
    t,X=bm_paths(1,1,0.0005,rng); w=X[0]; a=0.8; idx=np.argmax(w>=a)
    if w.max()>=a and 0.25<t[idx]<0.6 and w[-1]<a-0.2: break
ref=w.copy(); ref[idx:]=2*a-w[idx:]
fig,ax=plt.subplots(figsize=(11,4.6)); ax.plot(t,w,color=NAVY,lw=1.5,label="path W(t)"); ax.plot(t[idx:],ref[idx:],color=BURG,lw=1.3,ls="--",label="reflected after the first hit")
ax.axhline(a,color=GOLD,lw=2); ax.text(0.02,a+0.05,"level a",color=GOLD,fontsize=12,fontweight="bold"); ax.axvline(t[idx],color=SLATE,ls=":",lw=1.5); ax.text(t[idx]+0.01,-0.45,"τ_a (first hit)",color=SLATE,fontsize=12)
ax.scatter([1,1],[w[-1],ref[-1]],color=[NAVY,BURG],s=50,zorder=3); ax.text(1.01,w[-1],"W(t)",color=NAVY,fontsize=12,va="center"); ax.text(1.01,ref[-1],"2a − W(t)",color=BURG,fontsize=12,va="center")
ax.set_xlabel("t"); ax.set_ylabel("value"); ax.set_xlim(0,1.12); ax.legend(frameon=False,loc="upper left",fontsize=11)
save(fig,"SP_Fig_CH13_07.png")
# 13.8 hitting probability vs horizon (start 5, limit -10)
Ts=np.arange(5,366,5); fig,ax=plt.subplots(figsize=(10,4.6))
ax.plot(Ts,[p_hit_below(15,mu,s,T) for T in Ts],color=BURG,lw=2.5,label="touch −10 at some time in [0, T]"); ax.plot(Ts,[p_end_below(15,mu,s,T) for T in Ts],color=NAVY,lw=2.5,label="below −10 at day T only"); ax.axhline(p_ever_below(15,mu,s),color=GOLD,ls="--",lw=2,label=f"ever (T → ∞): {p_ever_below(15,mu,s):.3f}")
ax.axvline(90,color=SLATE,ls=":",lw=1.5); ax.text(93,0.002,"one quarter",color=SLATE,fontsize=11)
ax.set_xlabel("horizon T (days)"); ax.set_ylabel("probability"); ax.set_ylim(0,0.055); ax.legend(frameon=False,fontsize=11,loc="center right")
save(fig,"SP_Fig_CH13_08.png")
# 13.9 GBM fuel price
rng=np.random.default_rng(139); n=250; tt=np.linspace(0,1,n+1); fig,ax=plt.subplots(figsize=(11,4.6))
for k in range(12):
    z=rng.standard_normal(n); path=1.6*np.exp(np.r_[0,np.cumsum((0.04-0.03125)/n+0.25*np.sqrt(1/n)*z)]); ax.plot(tt,path,color=NAVY,lw=0.9,alpha=0.55)
ax.plot(tt,1.6*np.exp(0.04*tt),color=GOLD,lw=2.5,label="mean 1.6·e^(0.04t)"); ax.plot(tt,1.6*np.exp(0.00875*tt),color=EMER,lw=2.5,ls="--",label="median 1.6·e^(0.00875t)")
ax.fill_between(tt,1.6*np.exp(0.00875*tt-1.645*0.25*np.sqrt(tt)),1.6*np.exp(0.00875*tt+1.645*0.25*np.sqrt(tt)),color=GOLD,alpha=0.15,label="5%–95% band"); ax.axhline(2.0,color=BURG,ls=":",lw=2)
ax.text(0.02,2.03,"2.00 €/liter",color=BURG,fontsize=11); ax.set_xlabel("years"); ax.set_ylabel("fuel price (€/liter)"); ax.legend(frameon=False,fontsize=11,loc="upper left"); ax.set_ylim(0.9,2.8)
save(fig,"SP_Fig_CH13_09.png")
# 13.10 OU vs random-walk demand forecast
h=np.arange(0,31); th=-np.log(0.6)
fig,axs=plt.subplots(1,2,figsize=(13,4.6),gridspec_kw={"wspace":0.3})
m,sd=ou_forecast(600,500,th,50,h); axs[0].plot(h,m,color=EMER,lw=2.5); axs[0].fill_between(h,m-2*sd,m+2*sd,color=EMER,alpha=0.2); axs[0].axhline(500,color=SLATE,ls=":"); axs[0].set_ylim(0,1100); axs[0].set_title("(a) Mean-reverting (OU / AR(1)): band saturates at ± 100",color=NAVY,fontsize=12); axs[0].set_xlabel("days ahead"); axs[0].set_ylabel("forecast demand")
axs[1].plot(h,np.full_like(h,600.0),color=BURG,lw=2.5); axs[1].fill_between(h,600-2*40*np.sqrt(h),600+2*40*np.sqrt(h),color=BURG,alpha=0.2); axs[1].set_ylim(0,1100); axs[1].set_title("(b) Random-walk demand: band grows like 2·40·√h",color=NAVY,fontsize=12); axs[1].set_xlabel("days ahead")
sep(fig,[0.5]); save(fig,"SP_Fig_CH13_10.png")
# 13.11 monitoring bias
rng=np.random.default_rng(1311); grids=[1.0,0.25,0.05,0.02]; Ns=[400000,200000,100000,50000]; est=[hit_freq(5,-10,mu,s,90,dt,N,rng,chunk=5000) for dt,N in zip(grids,Ns)]; th_p=p_hit_below(15,mu,s,90)
fig,ax=plt.subplots(figsize=(10,4.4)); labs=["check daily","every 6 h","every 1.2 h","every 29 min","continuous\n(formula)"]; vals=est+[th_p]
b=ax.bar(labs,vals,color=[SLATE,SLATE,SLATE,SLATE,GOLD],width=0.55)
for bi,v in zip(b,vals): ax.text(bi.get_x()+bi.get_width()/2,v+0.0004,f"{v:.4f}",ha="center",fontsize=11.5,color=NAVY,fontweight="bold")
ax.set_ylabel("P(cash touches −10 within 90 days)"); ax.set_ylim(0,0.024)
save(fig,"SP_Fig_CH13_11.png"); print("monitoring",dict(zip(grids,est)),"formula",th_p)
# 13.12 concept map
fig,ax=plt.subplots(figsize=(12,7)); ax.axis("off"); ax.set_xlim(0,12); ax.set_ylim(0,7.3); ax.set_aspect("equal")
def cbox(x,y,t,c=NAVY,fc=IVORY,w=2.9,h=1.0,tc=None): rbox(ax,x-w/2,y-h/2,w,h,fc,c,2.2); ax.text(x,y,t,ha="center",va="center",fontsize=11.5,color=tc or NAVY,fontweight="bold",zorder=3,linespacing=1.3)
def link(p1,p2): ax.add_patch(FancyArrowPatch(p1,p2,arrowstyle="-|>",color=SLATE,lw=1.8,mutation_scale=15,zorder=1))
cbox(6,6.5,"Brownian motion = refined random walk",NAVY,NAVY,tc="white",w=5.6)
cbox(2.5,4.8,"N(0, t) increments,\nindependent, continuous",w=3.4); cbox(6,4.8,"Gaussian processes:\nmean & covariance"); cbox(9.5,4.8,"Drift & volatility,\n√t scaling")
cbox(2.5,3.0,"Rough paths:\nquadratic variation t",BLUE); cbox(6,3.0,"Bridge, OU\n(mean reversion)",EMER); cbox(9.5,3.0,"Reflection, first\npassage, ruin",CORAL)
cbox(2.5,1.1,"Itô’s rule*,\nEuler–Maruyama*",GOLD); cbox(6,1.1,"GBM for prices\n(mean ≠ median)",GOLD); cbox(9.5,1.1,"Simulation &\nmonitoring bias",GOLD)
for b_ in [(2.5,5.3),(6,5.3),(9.5,5.3)]: link((6,6.0),b_)
for xx in (2.5,6,9.5): link((xx,4.3),(xx,3.5)); link((xx,2.5),(xx,1.6))
save(fig,"SP_Fig_CH13_12.png")
