"""SP_CH06 — Chapter 6 figures (what is a stochastic process; Nava reference problems) and number checks."""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
NAVY, GOLD, EMER, BURG, BLUE, CORAL, IVORY, SLATE = "#0B2545","#C9A227","#1B7F5C","#7A1E2B","#2E86AB","#E07A5F","#FBF8F1","#5B6B7C"
plt.rcParams.update({"font.size":14,"axes.titlesize":15,"axes.labelsize":14,"font.family":"DejaVu Sans","axes.edgecolor":SLATE,"axes.spines.top":False,"axes.spines.right":False,"axes.titlepad":10})
OUT="/home/claude/ch06/fig/"
def save(fig,name): fig.savefig(OUT+name,dpi=300,bbox_inches="tight",facecolor="white",pad_inches=0.15); plt.close(fig)
def rbox(ax,x,y,w,h,fc,ec,lw=2.5): ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0,rounding_size=0.12",fc=fc,ec=ec,lw=lw,zorder=2))
sep=lambda fig,xs: [fig.add_artist(plt.Line2D([x,x],[0.05,0.95],color=SLATE,lw=1.2,ls=":")) for x in xs]
# Part II opener figure: book map
fig,ax=plt.subplots(figsize=(14,5)); ax.axis("off"); ax.set_xlim(0,14); ax.set_ylim(0,5)
parts=[("I","Probability\nfrom Zero","1–5",SLATE),("II","Arrivals\nand Waiting","6–8",GOLD),("III","The Markov\nWorld","9–12",SLATE),("IV","Continuous\nStates","13",SLATE),("V","Inside\nMetaheuristics","14–16",SLATE),("VI","Monte Carlo\nSimulation","17–19",SLATE)]
for i,(n,t,chs,c) in enumerate(parts):
    x=0.4+i*2.3; rbox(ax,x,1.4,2.0,2.4,IVORY if c==SLATE else "#F7F0DC",c,3 if c==GOLD else 1.8); ax.text(x+1,3.3,f"PART {n}",ha="center",fontsize=13,color=c if c==GOLD else NAVY,fontweight="bold",zorder=3); ax.text(x+1,2.45,t,ha="center",va="center",fontsize=12,color=NAVY,zorder=3); ax.text(x+1,1.65,f"Ch {chs}",ha="center",fontsize=11,color=SLATE,zorder=3)
    if i<5: ax.add_patch(FancyArrowPatch((x+2.05,2.6),(x+2.25,2.6),arrowstyle="-|>",color=SLATE,lw=1.5,mutation_scale=14))
ax.text(7,4.6,"You are here: time enters the book",ha="center",fontsize=14,color=GOLD,fontweight="bold")
ax.text(7,0.6,"Part I gave you one random number at a time. Part II follows random numbers through time: processes, Poisson arrivals, and queues.",ha="center",fontsize=11.5,color=SLATE)
save(fig,"SP_Fig_CH06_00_PartII.png")
# Fig 6.1 four cells
fig,ax=plt.subplots(figsize=(12,6.2)); ax.axis("off"); ax.set_xlim(0,12); ax.set_ylim(0,6.2)
cells=[(1.2,3.2,"Discrete time · Discrete state","Late vans per day (0–12)\nTier of a customer each month\nMachine 3 running/stopped each shift",NAVY),(6.5,3.2,"Discrete time · Continuous state","Daily demand (orders ≈ continuous)\nDaily cash balance\nAverage call length each day",BLUE),(1.2,0.4,"Continuous time · Discrete state","Number of calls arrived by time t\nNumber of busy operators at time t\nMachine state at any instant",EMER),(6.5,0.4,"Continuous time · Continuous state","Cash position at any instant\nTemperature of the cold room\nFuel level of a van",BURG)]
for x,y,t,ex,c in cells:
    rbox(ax,x,y,4.6,2.5,IVORY,c); ax.text(x+2.3,y+2.15,t,ha="center",fontsize=12.5,color=c,fontweight="bold",zorder=3); ax.text(x+2.3,y+1.0,ex,ha="center",va="center",fontsize=11,color=NAVY,zorder=3,linespacing=1.5)
ax.text(6,6.0,"TIME INDEX  →   discrete (days, shifts, months)            continuous (any instant)",ha="center",fontsize=11.5,color=SLATE)
ax.text(0.45,3.1,"STATE SPACE ↓",rotation=90,va="center",fontsize=11.5,color=SLATE)
save(fig,"SP_Fig_CH06_02.png")
# Fig 6.2 three sample paths of late vans per day (B(12,.23) i.i.d.)
rng=np.random.default_rng(6); fig,ax=plt.subplots(figsize=(11,4.6)); days=np.arange(1,31)
for k,(c,m) in enumerate([(NAVY,"o"),(GOLD,"s"),(EMER,"^")]):
    x=rng.binomial(12,0.23,30); ax.plot(days,x,"-"+m,color=c,lw=1.6,ms=5,alpha=0.9,label=f"sample path {k+1} (one possible month)")
ax.axhline(2.76,color=BURG,ls="--",lw=2,label="mean function m(t) = 2.76"); ax.set_xlabel("day t"); ax.set_ylabel("late vans X(t)"); ax.set_ylim(-0.3,9); ax.legend(frameon=False,fontsize=11,ncol=2)
save(fig,"SP_Fig_CH06_01.png")
# Fig 6.3 Bernoulli process & its counting process
rng=np.random.default_rng(61); b=(rng.random(25)<0.23).astype(int); N=np.cumsum(b)
fig,axs=plt.subplots(2,1,figsize=(11,5.6),gridspec_kw={"hspace":0.5})
ax=axs[0]; ax.bar(np.arange(1,26),b,color=[BURG if v else SLATE for v in b],width=0.6); ax.set_yticks([0,1]); ax.set_yticklabels(["on time","late"]); ax.set_xlabel("day"); ax.set_title("(a) Bernoulli process: Van 7 each day, p = 0.23",color=NAVY)
ax=axs[1]; ax.step(np.arange(0,26),np.r_[0,N],where="post",color=NAVY,lw=2.5); ax.set_xlabel("day"); ax.set_ylabel("late days so far"); ax.set_title("(b) Its counting process N(t): a staircase that rises on late days",color=NAVY)
save(fig,"SP_Fig_CH06_03.png")
# Fig 6.4 random walk paths of cash
rng=np.random.default_rng(62); fig,ax=plt.subplots(figsize=(11,5))
T=60; t=np.arange(0,T+1)
for k in range(8):
    steps=np.where(rng.random(T)<0.5,1000,-1000); path=np.r_[0,np.cumsum(steps)]; ax.plot(t,path,color=NAVY,lw=1.3,alpha=0.55)
ax.plot(t,1000*np.sqrt(t),color=GOLD,lw=2.5,ls="--",label="± 1 SD = ±1000·√t"); ax.plot(t,-1000*np.sqrt(t),color=GOLD,lw=2.5,ls="--"); ax.axhline(0,color=BURG,lw=2,label="mean function = 0")
ax.set_xlabel("day t"); ax.set_ylabel("cash change since day 0 (€)"); ax.legend(frameon=False)
save(fig,"SP_Fig_CH06_04.png")
# Fig 6.5 counting process in continuous time (arrivals)
rng=np.random.default_rng(63); arr=np.cumsum(rng.exponential(1/3,12)); fig,ax=plt.subplots(figsize=(11,4.2))
ax.step(np.r_[0,arr],np.arange(0,13),where="post",color=NAVY,lw=2.5); ax.scatter(arr,np.zeros_like(arr)-0.3,marker="|",s=200,color=BURG,label="arrival instants")
for i,a in enumerate(arr[:4]): ax.text(a,-0.9,f"S{i+1}",ha="center",fontsize=11,color=BURG)
ax.set_xlabel("time t (minutes)"); ax.set_ylabel("N(t) = calls arrived by t"); ax.set_ylim(-1.3,13); ax.legend(frameon=False,loc="upper left")
save(fig,"SP_Fig_CH06_05.png")
# Fig 6.6 mean & covariance functions: iid vs random walk
fig,axs=plt.subplots(1,2,figsize=(13,4.6),gridspec_kw={"wspace":0.3}); t=np.arange(0,31)
ax=axs[0]; ax.plot(t,np.full_like(t,2.76,dtype=float),color=BURG,lw=2.5,label="m(t)"); ax.fill_between(t,2.76-1.46,2.76+1.46,color=GOLD,alpha=0.35,label="m(t) ± SD(t)"); ax.set_ylim(0,6); ax.set_title("(a) i.i.d. late-van process: flat mean, constant spread",color=NAVY,fontsize=12.5); ax.set_xlabel("day t"); ax.legend(frameon=False)
ax=axs[1]; ax.plot(t,np.zeros_like(t),color=BURG,lw=2.5,label="m(t) = 0"); ax.fill_between(t,-1000*np.sqrt(t),1000*np.sqrt(t),color=GOLD,alpha=0.35,label="± SD(t) = ±1000√t"); ax.set_title("(b) cash random walk: flat mean, growing spread",color=NAVY,fontsize=12.5); ax.set_xlabel("day t"); ax.legend(frameon=False)
sep(fig,[0.5]); save(fig,"SP_Fig_CH06_06.png")
# Fig 6.7 stationary AR(1) vs random walk
rng=np.random.default_rng(64); T=200; e=rng.normal(0,40,T); ar=np.zeros(T); 
for i in range(1,T): ar[i]=0.6*ar[i-1]+e[i]
rw=np.cumsum(rng.normal(0,40,T))
fig,axs=plt.subplots(1,2,figsize=(13,4.4),gridspec_kw={"wspace":0.3})
axs[0].plot(500+ar,color=NAVY,lw=1.5); axs[0].axhline(500,color=GOLD,ls="--",lw=2); axs[0].set_title("(a) Stationary: demand = 500 + 0.6·(yesterday − 500) + noise",color=NAVY,fontsize=12); axs[0].set_xlabel("day"); axs[0].set_ylabel("orders")
axs[1].plot(500+rw,color=BURG,lw=1.5); axs[1].axhline(500,color=GOLD,ls="--",lw=2); axs[1].set_title("(b) Not stationary: demand = yesterday + noise (random walk)",color=NAVY,fontsize=12); axs[1].set_xlabel("day")
sep(fig,[0.5]); save(fig,"SP_Fig_CH06_07.png")
# Fig 6.8 autocorrelation of AR(1)
fig,ax=plt.subplots(figsize=(9,4.2)); k=np.arange(0,11); ax.bar(k,0.6**k,color=NAVY,width=0.5)
for ki,v in zip(k,0.6**k): ax.text(ki,v+0.02,f"{v:.2f}",ha="center",fontsize=11,color=NAVY)
ax.set_xticks(k); ax.set_xlabel("lag k (days apart)"); ax.set_ylabel("autocorrelation ρ(k) = 0.6ᵏ"); ax.set_ylim(0,1.15)
save(fig,"SP_Fig_CH06_08.png")
# Fig 6.9 Nava company map with R1-R6
fig,ax=plt.subplots(figsize=(13,7)); ax.axis("off"); ax.set_xlim(0,13); ax.set_ylim(0,7)
rbox(ax,4.9,2.9,3.2,1.3,NAVY,NAVY); ax.text(6.5,3.55,"NAVA\nservice & logistics",ha="center",va="center",color="white",fontsize=14,fontweight="bold",zorder=3)
nodes=[(2.0,5.8,"R1  Call center\n5 operators · 3 servers\narrivals ≈ 3/min",BLUE),(6.5,6.2,"R2  Packing line\n4 machines in series\nmachine 3 stop rate 0.14/day",EMER),(11.0,5.8,"R3  Customer club\n1,000 members · 3 tiers\nmonthly tier moves & churn",CORAL),(2.0,1.0,"R4  Demand & cash\nN(500, 80²) orders/day\ncash ±1,000 €/day",GOLD),(6.5,0.6,"R5  Repair shop & fleet\n12 vans · boards Exp(8 mo)\ntires Weibull(2.5, 12 mo)",BURG),(11.0,1.0,"R6  Scheduling\n6 jobs on the bottleneck\nstation (720 sequences)",SLATE)]
for x,y,t,c in nodes:
    rbox(ax,x-1.8,y-0.75,3.6,1.5,IVORY,c); ax.text(x,y,t,ha="center",va="center",fontsize=11,color=NAVY,zorder=3,linespacing=1.45)
    ex=x+(1.8 if x<6.5 else -1.8) if x!=6.5 else x; ey=y-0.75 if y>3.5 else y+0.75
    tx=4.9 if x<6.5 else (8.1 if x>6.5 else 6.5); ty=4.2 if y>3.5 else 2.9
    ax.plot([ex,tx],[ey if x==6.5 else y,ty],color=c,lw=2,ls="--",zorder=1)
save(fig,"SP_Fig_CH06_09.png")
# Fig 6.10 R3 tier transition diagram (preview of Ch 9)
fig,ax=plt.subplots(figsize=(11,5.2)); ax.axis("off"); ax.set_xlim(0,11); ax.set_ylim(0,5.2)
pos={"Silver":(1.8,3.6),"Gold":(5.5,3.6),"Platinum":(9.2,3.6),"Churned":(5.5,0.9)}
col={"Silver":SLATE,"Gold":GOLD,"Platinum":EMER,"Churned":BURG}
for k,(x,y) in pos.items(): ax.add_patch(plt.Circle((x,y),0.75,fc=col[k],ec=col[k],zorder=3)); ax.text(x,y,k,ha="center",va="center",color="white",fontsize=12,fontweight="bold",zorder=4)
def arrow(a,b,t,rad=0.25,off=(0,0)):
    (x1,y1),(x2,y2)=pos[a],pos[b]; ax.annotate("",xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle="-|>",color=NAVY,lw=1.8,shrinkA=38,shrinkB=38,connectionstyle=f"arc3,rad={rad}"),zorder=2); mx,my=(x1+x2)/2+off[0],(y1+y2)/2+off[1]; ax.text(mx,my,t,ha="center",fontsize=11.5,color=NAVY,bbox=dict(boxstyle="round,pad=0.15",fc="white",ec="none"),zorder=5)
arrow("Silver","Gold","0.10",rad=-0.3,off=(0,0.75)); arrow("Gold","Silver","0.05",rad=-0.3,off=(0,-0.75)); arrow("Gold","Platinum","0.10",rad=-0.3,off=(0,0.75)); arrow("Platinum","Gold","0.06",rad=-0.3,off=(0,-0.75))
arrow("Silver","Churned","0.20",rad=0.2,off=(-0.6,-0.3)); arrow("Gold","Churned","0.10",rad=0,off=(0.45,0)); arrow("Platinum","Churned","0.04",rad=-0.2,off=(0.6,-0.3))
for k,s in [("Silver","stay 0.70"),("Gold","stay 0.75"),("Platinum","stay 0.90"),("Churned","stay 1.00")]: x,y=pos[k]; ax.text(x,y+1.05 if k!="Churned" else y-1.05,s,ha="center",fontsize=11,color=col[k],fontweight="bold")
save(fig,"SP_Fig_CH06_10.png")
# Fig 6.11 R6 jobs Gantt for one sequence
jobs=[("J1",6,14),("J2",3,8),("J3",8,20),("J4",2,6),("J5",5,18),("J6",4,12)]
fig,ax=plt.subplots(figsize=(11,3.6)); t=0; cols=[NAVY,GOLD,EMER,BURG,BLUE,CORAL]
for i,(n,p,d) in enumerate(jobs):
    ax.barh(0,p,left=t,color=cols[i],edgecolor="white",height=0.6); ax.text(t+p/2,0,n,ha="center",va="center",color="white",fontsize=12,fontweight="bold"); ax.plot([d,d],[-0.6,0.6],color=cols[i],ls=":",lw=1.5); ax.text(d,0.65,f"due {n}",ha="center",fontsize=9,color=cols[i]); t+=p
ax.set_yticks([]); ax.set_xlabel("time on the bottleneck packing station (hours)"); ax.set_xlim(0,30); ax.set_ylim(-1,1.1); ax.set_title("Sequence J1-J2-J3-J4-J5-J6: completion times vs. due dates (dotted)",color=NAVY,fontsize=12.5)
save(fig,"SP_Fig_CH06_11.png")
C=np.cumsum([p for _,p,_ in jobs]); D=np.array([d for _,_,d in jobs]); print("R6 sequence J1..J6: completion",C,"tardiness",np.maximum(C-D,0),"total",np.maximum(C-D,0).sum())
# Fig 6.12 simulation: random walk mean/var at t=20
rng=np.random.default_rng(65); paths=np.cumsum(np.where(rng.random((10000,20))<0.5,1000,-1000),axis=1)
fig,ax=plt.subplots(figsize=(10,4.4)); ax.hist(paths[:,19],bins=21,color=NAVY,alpha=0.85,edgecolor="white"); ax.axvline(0,color=GOLD,lw=2.5,ls="--",label="theory: mean 0, SD 1000·√20 ≈ 4,472")
ax.set_xlabel("cash change after 20 days (€), 10,000 simulated months"); ax.set_ylabel("count"); ax.set_ylim(0,2300); ax.legend(frameon=False,loc="upper left",fontsize=11)
save(fig,"SP_Fig_CH06_12.png"); print("sim t=20 mean",paths[:,19].mean(),"sd",paths[:,19].std(),"P(>5000)",(paths[:,19]>5000).mean())
# Fig 6.13 concept map
fig,ax=plt.subplots(figsize=(12,7)); ax.axis("off"); ax.set_xlim(0,12); ax.set_ylim(0,7.3); ax.set_aspect("equal")
def cbox(x,y,t,c=NAVY,fc=IVORY,w=2.9,h=1.0,tc=None): rbox(ax,x-w/2,y-h/2,w,h,fc,c,2.2); ax.text(x,y,t,ha="center",va="center",fontsize=11.5,color=tc or NAVY,fontweight="bold",zorder=3,linespacing=1.3)
def link(p1,p2): ax.add_patch(FancyArrowPatch(p1,p2,arrowstyle="-|>",color=SLATE,lw=1.8,mutation_scale=15,zorder=1))
cbox(6,6.5,"Stochastic process {X(t)}\na random variable for every t",NAVY,NAVY,tc="white",w=5.2)
cbox(2.5,4.8,"Sample path vs.\ndistribution at t"); cbox(6,4.8,"Four cells: time × state\n(discrete / continuous)",w=3.4); cbox(9.5,4.8,"Mean & covariance\nfunctions m(t), C(s,t)",w=3.2)
cbox(2.5,3.0,"Building blocks: i.i.d.,\nBernoulli, random walk,\ncounting",BLUE,w=3.2,h=1.2); cbox(6,3.0,"Stationarity\n(strict, weak)",EMER); cbox(9.5,3.0,"Markov property\n(first look → Ch 9)",CORAL)
cbox(2.5,1.1,"Poisson process\n(Ch 7)",GOLD); cbox(6,1.1,"Nava reference\nproblems R1–R6",GOLD); cbox(9.5,1.1,"Simulation of\nsample paths (Ch 18)",GOLD)
for b in [(2.5,5.3),(6,5.3),(9.5,5.3)]: link((6,6.0),b)
for xx in (2.5,6,9.5): link((xx,4.3),(xx,3.6)); link((xx,2.4),(xx,1.6))
save(fig,"SP_Fig_CH06_13.png")
# checks
print("RW: var per step",0.5*1e6+0.5*1e6,"sd t=20",1000*np.sqrt(20),"P(S20>5000) normal",1-__import__('scipy').stats.norm.cdf(5000/4472.1))
print("RW drift p=0.55: mean step",0.55*1000-0.45*1000,"var step",1e6-100**2,"after 60: mean",60*100,"sd",np.sqrt(60*990000))
print("AR(1) phi .6 sigma 40: var",1600/(1-0.36),"sd",np.sqrt(1600/0.64),"cov lag 2",0.36*1600/0.64)
print("Bernoulli counting: N(30) mean var",30*.23,30*.23*.77,"cov N(10),N(30)",10*.23*.77)
