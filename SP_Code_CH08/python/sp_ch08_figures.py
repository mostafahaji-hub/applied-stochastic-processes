"""SP_CH08 — Chapter 8 figures (queueing theory on R1) and number checks."""
import numpy as np, matplotlib, sys
matplotlib.use("Agg"); sys.path.insert(0,"/home/claude/ch08/code")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Circle
from sp_ch08_queue import *
NAVY, GOLD, EMER, BURG, BLUE, CORAL, IVORY, SLATE = "#0B2545","#C9A227","#1B7F5C","#7A1E2B","#2E86AB","#E07A5F","#FBF8F1","#5B6B7C"
plt.rcParams.update({"font.size":14,"axes.titlesize":15,"axes.labelsize":14,"font.family":"DejaVu Sans","axes.edgecolor":SLATE,"axes.spines.top":False,"axes.spines.right":False,"axes.titlepad":10})
OUT="/home/claude/ch08/fig/"
def save(fig,name): fig.savefig(OUT+name,dpi=300,bbox_inches="tight",facecolor="white",pad_inches=0.15); plt.close(fig)
def rbox(ax,x,y,w,h,fc,ec,lw=2.5): ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0,rounding_size=0.12",fc=fc,ec=ec,lw=lw,zorder=2))
sep=lambda fig,xs: [fig.add_artist(plt.Line2D([x,x],[0.05,0.95],color=SLATE,lw=1.2,ls=":")) for x in xs]
lam,mu=3.0,2/3
# 8.1 anatomy
fig,ax=plt.subplots(figsize=(13,4.6)); ax.axis("off"); ax.set_xlim(0,13); ax.set_ylim(0,4.6)
ax.annotate("",xy=(3.2,2.3),xytext=(0.3,2.3),arrowprops=dict(arrowstyle="-|>",color=NAVY,lw=3)); ax.text(1.7,2.75,"ARRIVALS\nPoisson, rate λ",ha="center",fontsize=12,color=NAVY,fontweight="bold")
for i in range(5): rbox(ax,3.4+i*0.75,1.9,0.6,0.8,IVORY,GOLD)
ax.text(5.2,3.05,"QUEUE (waiting line)\nLq customers, wait Wq",ha="center",fontsize=12,color=GOLD,fontweight="bold")
for i in range(3): ax.add_patch(Circle((8.6,1.3+i*1.0),0.4,fc=EMER,ec=EMER)); ax.text(8.6,1.3+i*1.0,f"S{i+1}",ha="center",va="center",color="white",fontsize=11,fontweight="bold")
ax.text(8.6,4.1,"c SERVERS\nservice Exp(μ) each",ha="center",fontsize=12,color=EMER,fontweight="bold")
ax.annotate("",xy=(12.5,2.3),xytext=(9.3,2.3),arrowprops=dict(arrowstyle="-|>",color=NAVY,lw=3)); ax.text(10.9,2.75,"DEPARTURES",ha="center",fontsize=12,color=NAVY,fontweight="bold")
ax.annotate("",xy=(8.0,2.3),xytext=(7.2,2.3),arrowprops=dict(arrowstyle="-|>",color=SLATE,lw=2))
ax.add_patch(Rectangle((3.1,0.5),6.4,3.0,fc="none",ec=SLATE,ls="--",lw=1.5)); ax.text(6.3,0.2,"SYSTEM: L customers inside, time in system W = Wq + 1/μ",ha="center",fontsize=12,color=SLATE)
save(fig,"SP_Fig_CH08_01.png")
# 8.2 Little's law area
rng=np.random.default_rng(81); arr=np.cumsum(rng.exponential(1,8)); dep=arr+rng.exponential(2.5,8); dep=np.maximum.accumulate(dep)
fig,ax=plt.subplots(figsize=(11,4.6)); T=max(dep)+0.5; t=np.linspace(0,T,2000); Lt=np.array([((arr<=x)&(dep>x)).sum() for x in t])
ax.fill_between(t,Lt,step="post",color=GOLD,alpha=0.4); ax.step(t,Lt,where="post",color=NAVY,lw=2)
for i,(a,d) in enumerate(zip(arr,dep)): ax.hlines(-0.5-i*0.35,a,d,color=BURG,lw=3)
ax.set_xlabel("time"); ax.set_ylabel("L(t) = customers in system"); ax.set_ylim(-3.5,max(Lt)+1); ax.text(T*0.55,max(Lt)+0.4,"shaded area = Σ (time each customer spent inside) = N·W̄ = (λT)·W̄  ⇒  L̄ = λ W̄",fontsize=11.5,color=NAVY,ha="center")
ax.text(0.2,-3.2,"red bars: each customer’s stay (arrival → departure)",fontsize=10.5,color=BURG)
save(fig,"SP_Fig_CH08_02.png")
# 8.3 rate diagram M/M/1
fig,ax=plt.subplots(figsize=(12,3.2)); ax.axis("off"); ax.set_xlim(0,12); ax.set_ylim(0,3.2)
for i in range(6):
    x=1+i*2; ax.add_patch(Circle((x,1.6),0.45,fc=IVORY,ec=NAVY,lw=2.5)); ax.text(x,1.6,str(i) if i<5 else "…",ha="center",va="center",fontsize=14,color=NAVY,fontweight="bold")
    if i<5:
        ax.annotate("",xy=(x+1.5,1.95),xytext=(x+0.5,1.95),arrowprops=dict(arrowstyle="-|>",color=NAVY,lw=2,connectionstyle="arc3,rad=-0.4")); ax.text(x+1,2.75,"λ",ha="center",fontsize=14,color=NAVY,fontweight="bold")
        ax.annotate("",xy=(x+0.5,1.25),xytext=(x+1.5,1.25),arrowprops=dict(arrowstyle="-|>",color=BURG,lw=2,connectionstyle="arc3,rad=-0.4")); ax.text(x+1,0.35,"μ",ha="center",fontsize=14,color=BURG,fontweight="bold")
ax.plot([4,4],[0.2,3.0],color=GOLD,ls="--",lw=2.5); ax.text(4.1,3.0,"cut: λ·p₁ = μ·p₂",fontsize=12,color=GOLD,fontweight="bold")
save(fig,"SP_Fig_CH08_03.png")
# 8.4 M/M/1 L vs rho
fig,ax=plt.subplots(figsize=(10,4.8)); r=np.linspace(0,0.98,300); ax.plot(r,r/(1-r),color=NAVY,lw=2.5,label="L = ρ/(1−ρ)")
for rr in (0.5,0.75,0.9,0.95): ax.scatter([rr],[rr/(1-rr)],color=BURG,s=60,zorder=3); ax.text(rr-0.02,rr/(1-rr)+0.8,f"ρ={rr}: L={rr/(1-rr):.0f}",fontsize=11,color=BURG,ha="right")
ax.set_xlabel("utilization ρ = λ/μ"); ax.set_ylabel("average number in system L"); ax.set_ylim(0,22); ax.legend(frameon=False)
save(fig,"SP_Fig_CH08_05.png")
# 8.5 p_n for rho .75
fig,ax=plt.subplots(figsize=(10,4.2)); n=np.arange(0,15); r=0.75; ax.bar(n,(1-r)*r**n,color=NAVY,width=0.6)
for ni,v in zip(n,(1-r)*r**n):
    if v>0.01: ax.text(ni,v+0.006,f"{v:.3f}",ha="center",fontsize=10,color=NAVY)
ax.set_xticks(n); ax.set_xlabel("n = customers in the one-operator system"); ax.set_ylabel("pₙ = (1−ρ)ρⁿ, ρ = 0.75"); ax.set_ylim(0,0.3)
save(fig,"SP_Fig_CH08_04.png")
# 8.6 M/M/c rate diagram
fig,ax=plt.subplots(figsize=(13,3.2)); ax.axis("off"); ax.set_xlim(0,13); ax.set_ylim(0,3.2)
labs=["0","1","2","…","c","c+1","…"]; downs=["μ","2μ","3μ","cμ","cμ","cμ"]
for i,l in enumerate(labs):
    x=1+i*1.85; ax.add_patch(Circle((x,1.6),0.42,fc=IVORY,ec=NAVY,lw=2.5)); ax.text(x,1.6,l,ha="center",va="center",fontsize=13,color=NAVY,fontweight="bold")
    if i<6:
        ax.annotate("",xy=(x+1.4,1.95),xytext=(x+0.45,1.95),arrowprops=dict(arrowstyle="-|>",color=NAVY,lw=2,connectionstyle="arc3,rad=-0.4")); ax.text(x+0.92,2.75,"λ",ha="center",fontsize=13,color=NAVY,fontweight="bold")
        ax.annotate("",xy=(x+0.45,1.25),xytext=(x+1.4,1.25),arrowprops=dict(arrowstyle="-|>",color=BURG,lw=2,connectionstyle="arc3,rad=-0.4")); ax.text(x+0.92,0.35,downs[i],ha="center",fontsize=13,color=BURG,fontweight="bold")
ax.text(6.5,3.05,"departure rate grows with the number of busy servers, up to cμ",ha="center",fontsize=12,color=SLATE)
save(fig,"SP_Fig_CH08_06.png")
# 8.7 staffing curves
cs=np.arange(5,11); Wq=[mmc(lam,mu,c)["Wq"]*60 for c in cs]; SL=[1-pwait_gt(lam,mu,c,0.5) for c in cs]; PW=[mmc(lam,mu,c)["Pwait"] for c in cs]
fig,axs=plt.subplots(1,2,figsize=(13,4.6),gridspec_kw={"wspace":0.3})
axs[0].plot(cs,Wq,"-o",color=NAVY,lw=2.5,ms=8); [axs[0].text(c,w+6,f"{w:.0f}s",ha="center",fontsize=11,color=NAVY) for c,w in zip(cs,Wq)]; axs[0].set_xlabel("number of operators c"); axs[0].set_ylabel("average wait in queue Wq (seconds)"); axs[0].set_title("(a) Wq collapses as c grows (λ = 3/min, 1/μ = 1.5 min)",color=NAVY,fontsize=12); axs[0].set_ylim(0,max(Wq)*1.25)
axs[1].plot(cs,SL,"-o",color=EMER,lw=2.5,ms=8,label="P(wait ≤ 30 s)"); axs[1].plot(cs,PW,"-s",color=BURG,lw=2.5,ms=7,label="P(wait > 0)"); axs[1].axhline(0.9,color=GOLD,ls="--",lw=2); axs[1].set_xlabel("number of operators c"); axs[1].set_ylabel("probability"); axs[1].set_ylim(0,1.05); axs[1].legend(frameon=False); axs[1].set_title("(b) Service level and probability of waiting",color=NAVY,fontsize=12)
sep(fig,[0.5]); save(fig,"SP_Fig_CH08_07.png")
print("staffing:",[(int(c),round(w,1),round(s,3),round(p,3)) for c,w,s,p in zip(cs,Wq,SL,PW)])
# 8.8 Erlang B
fig,ax=plt.subplots(figsize=(10,4.6)); a=4.5; cs2=np.arange(1,13); B=[erlangB(a,c) for c in cs2]
ax.plot(cs2,B,"-o",color=NAVY,lw=2.5,ms=7); ax.axhline(0.01,color=GOLD,ls="--",lw=2); ax.text(1.2,0.03,"1% blocking target",color=GOLD,fontsize=12,fontweight="bold")
for c,b in zip(cs2,B):
    if c in (4,6,8,10): ax.text(c,b+0.03,f"{b:.3f}",ha="center",fontsize=11,color=NAVY)
ax.set_xlabel("number of lines c"); ax.set_ylabel("blocking probability (Erlang B), a = λ/μ = 4.5"); ax.set_ylim(0,0.85); ax.set_xticks(cs2)
save(fig,"SP_Fig_CH08_08.png"); print("ErlangB:",[(int(c),round(b,4)) for c,b in zip(cs2,B)])
# 8.9 P-K: Lq vs CV^2
fig,ax=plt.subplots(figsize=(10,4.6)); cv2=np.linspace(0,2,200)
for r_,c in [(0.5,EMER),(0.75,NAVY),(0.9,BURG)]: ax.plot(cv2,r_**2*(1+cv2)/(2*(1-r_)),color=c,lw=2.5,label=f"ρ = {r_}")
ax.axvline(1,color=GOLD,ls=":",lw=2); ax.text(1.02,ax.get_ylim()[1]*0.9 if False else 7.5,"exponential service (CV² = 1)",color=GOLD,fontsize=11); ax.axvline(0,color=SLATE,ls=":",lw=1.5); ax.text(0.03,7.5,"constant service (CV² = 0)",color=SLATE,fontsize=11)
ax.set_xlabel("squared coefficient of variation of service time, CV² = σ²μ²"); ax.set_ylabel("Lq (customers waiting)"); ax.set_ylim(0,8.5); ax.legend(frameon=False)
save(fig,"SP_Fig_CH08_09.png")
# 8.10 pooling
fig,ax=plt.subplots(figsize=(11,4.4)); ax.axis("off"); ax.set_xlim(0,11); ax.set_ylim(0,4.4)
sep_=mm1(1.5,2/3); pool=mmc(3,2/3,2) if mmc(3,2/3,2) else None
# with lam=1.5 each and mu=2/3 -> rho=2.25 >1 : choose numbers for the figure: lam 0.5 each, mu 2/3
s1=mm1(0.5,2/3); p2=mmc(1.0,2/3,2)
rbox(ax,0.4,0.6,4.6,3.2,IVORY,NAVY); ax.text(2.7,3.4,"TWO SEPARATE LINES",ha="center",fontsize=13,color=NAVY,fontweight="bold"); ax.text(2.7,2.1,f"each: λ = 0.5/min, 1/μ = 1.5 min\nρ = {s1['rho']:.2f}\nWq = {s1['Wq']:.2f} min\nLq (total) = {2*s1['Lq']:.2f}",ha="center",va="center",fontsize=12,color=NAVY)
rbox(ax,6.0,0.6,4.6,3.2,IVORY,EMER); ax.text(8.3,3.4,"ONE POOLED LINE, 2 OPERATORS",ha="center",fontsize=13,color=EMER,fontweight="bold"); ax.text(8.3,2.1,f"λ = 1.0/min, c = 2, 1/μ = 1.5 min\nρ = {p2['rho']:.2f} (same)\nWq = {p2['Wq']:.2f} min\nLq = {p2['Lq']:.2f}",ha="center",va="center",fontsize=12,color=NAVY)
ax.annotate("",xy=(5.9,2.2),xytext=(5.1,2.2),arrowprops=dict(arrowstyle="-|>",color=GOLD,lw=3)); ax.text(5.5,0.25,"same utilization, less than half the waiting",ha="center",fontsize=12.5,color=BURG,fontweight="bold")
save(fig,"SP_Fig_CH08_10.png"); print("pooling:",s1,p2)
# 8.11 simulation of M/M/5
rng=np.random.default_rng(88)
def sim_mmc(lam,mu,c,n=1000000,warm=100000):
    arr=np.cumsum(rng.exponential(1/lam,n)); serv=rng.exponential(1/mu,n); free=np.zeros(c); wq=np.zeros(n)
    for i in range(n):
        k=np.argmin(free); start=max(arr[i],free[k]); wq[i]=start-arr[i]; free[k]=start+serv[i]
    return wq[warm:]
wq=sim_mmc(lam,mu,5); th=mmc(lam,mu,5)
fig,ax=plt.subplots(figsize=(10,4.4)); ax.hist(wq[wq>0]*60,bins=60,density=True,color=NAVY,alpha=0.8,edgecolor="white",label="simulated waits of those who waited (seconds)")
t=np.linspace(0,600,300); ax.plot(t,(5*mu-lam)/60*np.exp(-(5*mu-lam)*t/60),color=GOLD,lw=3,label="theory: Exp(cμ − λ) given wait > 0")
ax.set_xlabel("waiting time in queue (seconds)"); ax.set_ylabel("density"); ax.legend(frameon=False); ax.set_xlim(0,600)
save(fig,"SP_Fig_CH08_11.png"); print("sim M/M/5: mean Wq",wq.mean()*60,"P(wait)",(wq>0).mean(),"theory Wq",th["Wq"]*60,"Pwait",th["Pwait"])
# 8.12 concept map
fig,ax=plt.subplots(figsize=(12,7)); ax.axis("off"); ax.set_xlim(0,12); ax.set_ylim(0,7.3); ax.set_aspect("equal")
def cbox(x,y,t,c=NAVY,fc=IVORY,w=2.9,h=1.0,tc=None): rbox(ax,x-w/2,y-h/2,w,h,fc,c,2.2); ax.text(x,y,t,ha="center",va="center",fontsize=11.5,color=tc or NAVY,fontweight="bold",zorder=3,linespacing=1.3)
def link(p1,p2): ax.add_patch(FancyArrowPatch(p1,p2,arrowstyle="-|>",color=SLATE,lw=1.8,mutation_scale=15,zorder=1))
cbox(6,6.5,"Queue = arrivals + service + servers + capacity",NAVY,NAVY,tc="white",w=6.4)
cbox(2.5,4.8,"Kendall A/B/c/K\nmeasures L, Lq, W, Wq"); cbox(6,4.8,"Little’s law\nL = λW"); cbox(9.5,4.8,"Rate diagram &\nbalance equations",w=3.2)
cbox(2.5,3.0,"M/M/1, M/M/1/K",BLUE); cbox(6,3.0,"M/M/c (Erlang C),\nM/M/c/c (Erlang B), M/M/∞",EMER,w=3.6); cbox(9.5,3.0,"M/G/1\n(Pollaczek–Khinchine)",CORAL,w=3.2)
cbox(2.5,1.1,"Finite source\n(machine repair)",GOLD); cbox(6,1.1,"Economics: cost vs.\ncapacity, pooling",GOLD,w=3.2); cbox(9.5,1.1,"Simulation (Ch 18),\nCTMC (Ch 11)",GOLD)
for b in [(2.5,5.3),(6,5.3),(9.5,5.3)]: link((6,6.0),b)
for xx in (2.5,6,9.5): link((xx,4.3),(xx,3.5)); link((xx,2.5),(xx,1.6))
save(fig,"SP_Fig_CH08_12.png")
# ---------- checks ----------
def show(l,v): print(f"{l:<58} {v}")
show("Ex 8.3 Little warehouse: L=λW: 40 orders/h, 3h -> L",120)
show("Ex 8.4 call center L from λ=3, W=2.4 min",7.2)
show("Ex 8.5 bank: L=12, λ=30/h -> W (min)",24)
show("Ex 8.6 M/M/1 λ=.5 μ=2/3",{k:round(v,3) for k,v in mm1(0.5,2/3).items()})
show("Ex 8.8 p0,p1,p2, P(n>=3) rho .75",(0.25,0.1875,0.1406,round(0.75**3,4)))
show("Ex 8.9 M/M/1 P(W>2 min), P(Wq>2)",(round(np.exp(-(2/3-0.5)*2),4),round(0.75*np.exp(-(2/3-0.5)*2),4)))
show("Ex 8.10 rho .9 vs .75: L",(9,3))
show("Ex 8.11 M/M/1/3 λ=.5 μ=2/3",{k:(round(v,4) if not hasattr(v,'__len__') else v.round(4)) for k,v in mm1k(0.5,2/3,3).items()})
show("Ex 8.12 M/M/5 λ=3 μ=2/3",{k:round(v,4) for k,v in mmc(3,2/3,5).items()})
show("Ex 8.13 M/M/6",{k:round(v,4) for k,v in mmc(3,2/3,6).items()})
show("Ex 8.14 P(W_q>0.5min) c=5,6,7",[round(pwait_gt(3,2/3,c,0.5),4) for c in (5,6,7)])
show("Ex 8.15 Erlang B a=4.5: c=6,8,10",[round(erlangB(4.5,c),4) for c in (6,8,10)])
show("Ex 8.16 M/M/inf: lam 20/min, mean 6 min -> L=120, P(>140) poisson",round(1-__import__('scipy').stats.poisson.cdf(140,120),4))
show("Ex 8.17 finite source 4 machines lam 1/7 mu 1",{k:(round(v,4) if not hasattr(v,'__len__') else v.round(4)) for k,v in finite_source(4,1/7,1).items()})
show("Ex 8.18 M/G/1 deterministic vs exp λ=.5 μ=2/3",(round(mg1(0.5,2/3,0)["Lq"],4),round(mg1(0.5,2/3,1.5)["Lq"],4)))
show("Ex 8.19 M/G/1 sigma=3 (CV=2)",round(mg1(0.5,2/3,3)["Lq"],4))
show("Ex 8.21 cost: c operators 25€/h, wait 2€/min/customer: total per hour",[(c,round(25*c+ 2*60*mmc(3,2/3,c)["Lq"],1)) for c in range(5,11)])
show("Ex 8.22 pooling",(round(mm1(0.5,2/3)["Wq"],3),round(mmc(1.0,2/3,2)["Wq"],3)))
# exercises
show("Exercise mm1 λ=4/h μ=6/h",{k:round(v,3) for k,v in mm1(4,6).items()})
show("Exercise mm1 P(n>=4) rho 2/3",round((2/3)**4,4))
show("Exercise mmc λ=4 μ=2/3 c=7,8",[{k:round(v,3) for k,v in mmc(4,2/3,c).items()} for c in (7,8)])
show("Exercise mm1k K=5 λ=.5 μ=.4 (rho>1 ok)",{k:(round(v,4) if not hasattr(v,'__len__') else v.round(3)) for k,v in mm1k(0.5,0.4,5).items()})
show("Exercise erlangB a=6: c for <2%",[(c,round(erlangB(6,c),4)) for c in range(8,14)])
show("Exercise finite source 6 machines lam 1/10 mu 1/2",{k:(round(v,4) if not hasattr(v,'__len__') else v.round(3)) for k,v in finite_source(6,0.1,0.5).items()})
show("Exercise mg1 λ=2/h service mean 20 min sd 10",{k:round(v,3) for k,v in mg1(2,3,1/6).items()})
show("Boss: c for P(Wq>30s)<=0.1 at λ=4 peak",[(c,round(pwait_gt(4,2/3,c,0.5),3)) for c in (7,8,9,10)])
