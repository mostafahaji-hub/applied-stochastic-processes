"""SP_CH12 — Chapter 12 figures and number checks."""
import numpy as np, matplotlib, sys
matplotlib.use("Agg"); sys.path.insert(0,"/home/claude/ch12/code")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
from scipy.stats import weibull_min, lognorm
from sp_ch12_reliability import *
NAVY, GOLD, EMER, BURG, BLUE, CORAL, IVORY, SLATE = "#0B2545","#C9A227","#1B7F5C","#7A1E2B","#2E86AB","#E07A5F","#FBF8F1","#5B6B7C"
plt.rcParams.update({"font.size":14,"axes.titlesize":15,"axes.labelsize":14,"font.family":"DejaVu Sans","axes.edgecolor":SLATE,"axes.spines.top":False,"axes.spines.right":False,"axes.titlepad":10})
OUT="/home/claude/ch12/fig/"
def save(fig,name): fig.savefig(OUT+name,dpi=300,bbox_inches="tight",facecolor="white",pad_inches=0.15); plt.close(fig)
def rbox(ax,x,y,w,h,fc,ec,lw=2.5): ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0,rounding_size=0.12",fc=fc,ec=ec,lw=lw,zorder=2))
sep=lambda fig,xs: [fig.add_artist(plt.Line2D([x,x],[0.05,0.95],color=SLATE,lw=1.2,ls=":")) for x in xs]
# 12.1 bathtub
fig,ax=plt.subplots(figsize=(11,4.4)); t=np.linspace(0.01,30,500); h=0.25*np.exp(-t/2)+0.03+0.03*np.exp((t-25)/2)
ax.plot(t,h,color=NAVY,lw=3); ax.axvspan(0,5,color=BURG,alpha=0.12); ax.axvspan(5,22,color=EMER,alpha=0.12); ax.axvspan(22,30,color=GOLD,alpha=0.18)
ax.text(2.5,0.32,"infant mortality\n(k < 1)",ha="center",color=BURG,fontsize=12,fontweight="bold"); ax.text(13.5,0.32,"useful life: constant hazard\n(k = 1, exponential)",ha="center",color=EMER,fontsize=12,fontweight="bold"); ax.text(26,0.32,"wear-out\n(k > 1)",ha="center",color=GOLD,fontsize=12,fontweight="bold")
ax.set_xlabel("age"); ax.set_ylabel("hazard rate h(t)"); ax.set_ylim(0,0.4); ax.set_xticks([])
save(fig,"SP_Fig_CH12_01.png")
# 12.2 Weibull hazards of Nava parts
fig,ax=plt.subplots(figsize=(10,4.6)); t=np.linspace(0.1,24,300)
ax.plot(t,np.full_like(t,1/8),color=NAVY,lw=2.5,label="electronic board: exponential, h = 1/8 per month"); ax.plot(t,weibull_hazard(t,2.5,12),color=BURG,lw=2.5,label="tire: Weibull k = 2.5, η = 12"); ax.plot(t,weibull_hazard(t,3,20),color=EMER,lw=2.5,label="bearing: Weibull k = 3, η = 20")
ax.set_xlabel("age (months)"); ax.set_ylabel("hazard rate (failures per month, given survival)"); ax.set_ylim(0,0.6); ax.legend(frameon=False,fontsize=11)
save(fig,"SP_Fig_CH12_02.png")
# 12.3 structures incl k-of-n
fig,axs=plt.subplots(1,3,figsize=(17,3.4),gridspec_kw={"wspace":0.08})
def comp(ax,x,y,t,c=NAVY,w=1.5,h=0.72): rbox(ax,x-w/2,y-h/2,w,h,IVORY,c); ax.text(x,y,t,ha="center",va="center",fontsize=11.5,color=NAVY,fontweight="bold",zorder=3)
ax=axs[0]; ax.set_xlim(0,8); ax.set_ylim(0,3); ax.axis("off"); ax.set_aspect("equal"); ax.plot([0.2,7.8],[1.5,1.5],color=NAVY,lw=2,zorder=1)
for i,t in enumerate(["M1","M2","M3","M4"]): comp(ax,1.2+i*1.85,1.5,t)
ax.set_title("(a) Series: all must work",color=NAVY)
ax=axs[1]; ax.set_xlim(0,8); ax.set_ylim(0,3); ax.axis("off"); ax.set_aspect("equal")
for y in (0.5,1.5,2.5): ax.plot([1.2,6.8],[y,y],color=NAVY,lw=2,zorder=1)
ax.plot([1.2,1.2],[0.5,2.5],color=NAVY,lw=2); ax.plot([6.8,6.8],[0.5,2.5],color=NAVY,lw=2); ax.plot([0.2,1.2],[1.5,1.5],color=NAVY,lw=2); ax.plot([6.8,7.8],[1.5,1.5],color=NAVY,lw=2)
for y,t in zip((0.5,1.5,2.5),["S3","S2","S1"]): comp(ax,4,y,t,GOLD)
ax.set_title("(b) Parallel: one is enough",color=NAVY)
ax=axs[2]; ax.set_xlim(0,8); ax.set_ylim(0,3); ax.axis("off"); ax.set_aspect("equal")
for y in (0.5,1.5,2.5): ax.plot([1.2,6.8],[y,y],color=NAVY,lw=2,zorder=1)
ax.plot([1.2,1.2],[0.5,2.5],color=NAVY,lw=2); ax.plot([6.8,6.8],[0.5,2.5],color=NAVY,lw=2); ax.plot([0.2,1.2],[1.5,1.5],color=NAVY,lw=2); ax.plot([6.8,7.8],[1.5,1.5],color=NAVY,lw=2)
for y,t in zip((0.5,1.5,2.5),["sensor 3","sensor 2","sensor 1"]): comp(ax,4,y,t,EMER,w=1.9)
ax.text(4,-0.2,"2 of 3 must agree",ha="center",fontsize=11.5,color=EMER,fontweight="bold"); ax.set_title("(c) k-out-of-n: at least k work",color=NAVY)
sep(fig,[0.365,0.64]); save(fig,"SP_Fig_CH12_03.png")
# 12.4 R(t) series vs parallel vs 2of3 with exp components mean 10
fig,ax=plt.subplots(figsize=(10,4.6)); t=np.linspace(0,30,300); R=np.exp(-t/10)
ax.plot(t,R,color=SLATE,lw=2,ls="--",label="one component, MTTF 10"); ax.plot(t,R**4,color=BURG,lw=2.5,label="4 in series, MTTF 2.5"); ax.plot(t,1-(1-R)**3,color=EMER,lw=2.5,label="3 in parallel, MTTF 18.3"); ax.plot(t,3*R**2-2*R**3,color=GOLD,lw=2.5,label="2-of-3, MTTF 8.3")
ax.set_xlabel("t"); ax.set_ylabel("system reliability R(t)"); ax.legend(frameon=False,fontsize=11)
save(fig,"SP_Fig_CH12_04.png")
# 12.5 availability vs repairers + cost
fig,axs=plt.subplots(1,2,figsize=(13,4.4),gridspec_kw={"wspace":0.3}); rs=[1,2,3,4]; A=[line_availability(r)[0] for r in rs]; cost=[3200*(1-a)+300*r for a,r in zip(A,rs)]
axs[0].bar(rs,A,color=NAVY,width=0.5); [axs[0].text(r,a+0.01,f"{a:.3f}",ha="center",fontsize=12,color=NAVY) for r,a in zip(rs,A)]; axs[0].axhline((20/21)**3*7/8,color=GOLD,ls="--",lw=2,label="independent-repair bound 0.756"); axs[0].set_xlabel("repair crews"); axs[0].set_ylabel("line availability"); axs[0].set_ylim(0,1); axs[0].legend(frameon=False,fontsize=10.5); axs[0].set_xticks(rs); axs[0].set_title("(a) Availability of the 4-machine line",color=NAVY,fontsize=12.5)
axs[1].bar(rs,cost,color=[EMER if c==min(cost) else SLATE for c in cost],width=0.5); [axs[1].text(r,c+20,f"{c:.0f} €",ha="center",fontsize=12,color=NAVY) for r,c in zip(rs,cost)]; axs[1].set_xlabel("repair crews"); axs[1].set_ylabel("downtime + crew cost per shift (€)"); axs[1].set_xticks(rs); axs[1].set_title("(b) One crew is cheapest",color=NAVY,fontsize=12.5)
sep(fig,[0.5]); save(fig,"SP_Fig_CH12_05.png"); print("avail",np.round(A,4),"cost",np.round(cost,1))
# 12.6 age vs block replacement tire
Ts=np.linspace(2,14,49); age=[age_replacement_rate(T,lambda x: weibull_min.cdf(x,2.5,scale=12),80,600) for T in Ts]; blk=[block_replacement_rate(T,2.5,12,80,600) for T in Ts]
fig,ax=plt.subplots(figsize=(10,4.6)); ax.plot(Ts,age,color=NAVY,lw=2.5,label="age replacement (replace at age T or at failure)"); ax.plot(Ts,blk,color=GOLD,lw=2.5,label="block replacement (replace all every T, plus failures)"); ax.axhline(600/weibull_min.mean(2.5,scale=12),color=BURG,ls="--",lw=2,label="run to failure: 56.4")
ax.set_xlabel("T (months)"); ax.set_ylabel("cost per month per tire (€)"); ax.set_ylim(20,60); ax.legend(frameon=False,fontsize=10.5)
save(fig,"SP_Fig_CH12_06.png"); print("age min",Ts[np.argmin(age)],min(age),"block min",Ts[np.argmin(blk)],min(blk))
# 12.7 inspection interval
fig,ax=plt.subplots(figsize=(10,4.4)); Ts=np.linspace(1,40,200); r=[inspection_rate(T,1/50,50,100) for T in Ts]
ax.plot(Ts,r,color=NAVY,lw=2.5); Tb=Ts[np.argmin(r)]; ax.scatter([Tb],[min(r)],color=GOLD,s=90,zorder=3); ax.text(Tb+1,min(r)+1,f"best interval ≈ {Tb:.0f} shifts: {min(r):.1f} €/shift",color=GOLD,fontsize=12,fontweight="bold")
ax.set_xlabel("inspection interval T (shifts)"); ax.set_ylabel("inspection + undetected-failure cost per shift (€)"); ax.set_ylim(10,30)
save(fig,"SP_Fig_CH12_07.png"); print("insp best",Tb,min(r))
# 12.8 warranty cost vs W
fig,ax=plt.subplots(figsize=(10,4.4)); W=np.linspace(0,18,100); ax.plot(W,80*weibull_min.cdf(W,2.5,scale=12),color=NAVY,lw=2.5,label="tire (Weibull): 80·F(W)"); ax.plot(W,80*(1-np.exp(-W/8)),color=BURG,lw=2.5,label="board (exponential): 80·(1 − e^(−W/8))")
ax.set_xlabel("warranty length W (months)"); ax.set_ylabel("expected warranty cost per unit (€)"); ax.legend(frameon=False)
save(fig,"SP_Fig_CH12_08.png")
# 12.9 simulation of line availability
rng=np.random.default_rng(12); T=20000; t=0; failed=np.zeros(4,bool); rates=np.array([0.05,0.05,1/7,0.05]); up=0.0; crew_busy=None
# event-driven: next failure among working, next repair of the one being repaired (machine 3 first)
while t<T:
    cand=[]
    for i in range(4):
        if not failed[i]: cand.append((rng.exponential(1/rates[i]),"f",i))
    if failed.any():
        j=2 if failed[2] else int(np.flatnonzero(failed)[0]); cand.append((rng.exponential(1.0),"r",j))
    dt,kind,i=min(cand); dt=min(dt,T-t)
    if not failed.any(): up+=dt
    t+=dt
    if kind=="f": failed[i]=True
    else: failed[i]=False
print("sim availability",up/T)
fig,ax=plt.subplots(figsize=(8,4)); ax.bar(["simulation (20,000 shifts)","CTMC πQ = 0","independent bound"],[up/T,line_availability(1)[0],(20/21)**3*7/8],color=[NAVY,GOLD,SLATE],width=0.5)
for i,v in enumerate([up/T,line_availability(1)[0],(20/21)**3*7/8]): ax.text(i,v+0.01,f"{v:.3f}",ha="center",fontsize=12,color=NAVY)
ax.set_ylabel("availability of the line"); ax.set_ylim(0,1)
save(fig,"SP_Fig_CH12_09.png")
# 12.10 concept map
fig,ax=plt.subplots(figsize=(12,7)); ax.axis("off"); ax.set_xlim(0,12); ax.set_ylim(0,7.3); ax.set_aspect("equal")
def cbox(x,y,t,c=NAVY,fc=IVORY,w=2.9,h=1.0,tc=None): rbox(ax,x-w/2,y-h/2,w,h,fc,c,2.2); ax.text(x,y,t,ha="center",va="center",fontsize=11.5,color=tc or NAVY,fontweight="bold",zorder=3,linespacing=1.3)
def link(p1,p2): ax.add_patch(FancyArrowPatch(p1,p2,arrowstyle="-|>",color=SLATE,lw=1.8,mutation_scale=15,zorder=1))
cbox(6,6.5,"Reliability & maintenance",NAVY,NAVY,tc="white",w=4.2)
cbox(2.5,4.8,"Hazard rate, bathtub,\nMTTF, lifetime laws",w=3.2); cbox(6,4.8,"Structure: series,\nparallel, k-of-n"); cbox(9.5,4.8,"Repairable systems:\navailability via CTMC",w=3.2)
cbox(2.5,3.0,"Age & block\nreplacement (IFR only)",BURG,w=3.2); cbox(6,3.0,"Inspection intervals,\nwarranty cost",EMER,w=3.2); cbox(9.5,3.0,"Redundancy & spares\neconomics",BLUE)
cbox(2.5,1.1,"Ch 2 (structures),\nCh 4 (Weibull)",GOLD); cbox(6,1.1,"Ch 11 (CTMC,\nrenewal-reward)",GOLD); cbox(9.5,1.1,"Simulation (Ch 18)",GOLD)
for b in [(2.5,5.3),(6,5.3),(9.5,5.3)]: link((6,6.0),b)
for xx in (2.5,6,9.5): link((xx,4.3),(xx,3.5)); link((xx,2.5),(xx,1.6))
save(fig,"SP_Fig_CH12_10.png")
# checks
def show(l,v): print(f"{l:<58} {v}")
show("Ex 12.1 board R(12), h",(round(np.exp(-1.5),3),0.125)); show("Ex 12.2 tire h(3,6,12), R(6)",([round(weibull_hazard(t,2.5,12),4) for t in (3,6,12)],round(1-weibull_min.cdf(6,2.5,scale=12),3)))
show("Ex 12.3 bearing h(5,10,20)",[round(weibull_hazard(t,3,20),4) for t in (5,10,20)])
show("Ex 12.5 series exp mean 7: MTTF, R(1), R(2)",(1.75,round(np.exp(-4/7),3),round(np.exp(-8/7),3)))
show("Ex 12.6 parallel 3 servers mean 10: MTTF, R(10)",(round(10*(1+.5+1/3),2),round(1-(1-np.exp(-1))**3,3)))
show("Ex 12.7 2of3: R=.9 ; exp MTTF 100: MTTF, R(50)",(round(R_k_of_n(2,3,0.9),3),round(3*50-2*100/3,1),round(3*np.exp(-1)-2*np.exp(-1.5),3)))
show("Ex 12.9 line availability r=1,2; bound",(round(line_availability(1)[0],4),round(line_availability(2)[0],4),round((20/21)**3*7/8,4)))
show("Ex 12.10 servers 1 crew A",0.9231); show("Ex 12.11 cost r=1,2",(round(3200*(1-line_availability(1)[0])+300),round(3200*(1-line_availability(2)[0])+600)))
show("Ex 12.12 age T*, rate",(round(Ts[np.argmin(age)],1),round(min(age),2))); show("Ex 12.13 block T*, rate",(round(Ts[np.argmin(blk)],1),round(min(blk),2)))
show("Ex 12.14 board age replacement at 4: rate vs 75",round(age_replacement_rate(4,lambda x: 1-np.exp(-x/8),80,600),2))
show("Ex 12.15 inspection T*",(round(Tb),round(min(r),2))); show("Ex 12.16 warranty tire W=6,12",(round(80*weibull_min.cdf(6,2.5,scale=12),2),round(80*weibull_min.cdf(12,2.5,scale=12),2)))
show("Ex 12.17 board W=6",round(80*(1-np.exp(-0.75)),2)); show("Ex 12.18 standby vs active MTTF",(16,12)); show("Ex 12.19 spares 95%",spares_needed(18,0.95))
