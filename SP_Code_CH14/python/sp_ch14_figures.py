"""SP_CH14 — Part V opener and Chapter 14 figures (simulated annealing as a Markov chain on R6)."""
import numpy as np, matplotlib, sys
matplotlib.use("Agg"); sys.path.insert(0,"/home/claude/ch14/code")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
from sp_ch14_sa import *
NAVY, GOLD, EMER, BURG, BLUE, CORAL, IVORY, SLATE = "#0B2545","#C9A227","#1B7F5C","#7A1E2B","#2E86AB","#E07A5F","#FBF8F1","#5B6B7C"
plt.rcParams.update({"font.size":14,"axes.titlesize":15,"axes.labelsize":14,"font.family":"DejaVu Sans","axes.edgecolor":SLATE,"axes.spines.top":False,"axes.spines.right":False,"axes.titlepad":10})
OUT="/home/claude/ch14/fig/"
def save(fig,name): fig.savefig(OUT+name,dpi=300,bbox_inches="tight",facecolor="white",pad_inches=0.15); plt.close(fig)
def rbox(ax,x,y,w,h,fc,ec,lw=2.5): ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0,rounding_size=0.12",fc=fc,ec=ec,lw=lw,zorder=2))
sep=lambda fig,xs: [fig.add_artist(plt.Line2D([x,x],[0.05,0.95],color=SLATE,lw=1.2,ls=":")) for x in xs]
JC=[NAVY,GOLD,EMER,BURG,BLUE,CORAL]
# Part V opener
fig,ax=plt.subplots(figsize=(14,5)); ax.axis("off"); ax.set_xlim(0,14); ax.set_ylim(0,5)
parts=[("I","Probability\nfrom Zero","1–5",SLATE),("II","Arrivals\nand Waiting","6–8",SLATE),("III","The Markov\nWorld","9–12",SLATE),("IV","Continuous\nStates","13",SLATE),("V","Inside\nMetaheuristics","14–16",GOLD),("VI","Monte Carlo\nSimulation","17–19",SLATE)]
for i,(n,t,chs,c) in enumerate(parts):
    x=0.4+i*2.3; rbox(ax,x,1.4,2.0,2.4,IVORY if c==SLATE else "#F7F0DC",c,3 if c==GOLD else 1.8); ax.text(x+1,3.3,f"PART {n}",ha="center",fontsize=13,color=c if c==GOLD else NAVY,fontweight="bold",zorder=3); ax.text(x+1,2.45,t,ha="center",va="center",fontsize=12,color=NAVY,zorder=3); ax.text(x+1,1.65,f"Ch {chs}",ha="center",fontsize=11,color=SLATE,zorder=3)
    if i<5: ax.add_patch(FancyArrowPatch((x+2.05,2.6),(x+2.25,2.6),arrowstyle="-|>",color=SLATE,lw=1.5,mutation_scale=14))
ax.text(7,4.6,"You are here: the heart of the book — algorithms as stochastic processes",ha="center",fontsize=14,color=GOLD,fontweight="bold")
ax.text(7,0.6,"Part V watches three search algorithms on Nava’s scheduling problem R6 and analyzes each one with the tools of Parts I–IV.",ha="center",fontsize=11.5,color=SLATE)
save(fig,"SP_Fig_CH14_00_PartV.png")
# 14.1 Gantt start vs optimum
def gantt(ax,seq,title):
    t=0
    for j in seq:
        p=P_TIMES[j]; ax.barh(0,p,left=t,color=JC[j],edgecolor="white",height=0.6); ax.text(t+p/2,0,NAMES[j],ha="center",va="center",color="white",fontsize=12,fontweight="bold")
        late=max(0,t+p-DUE[j]); 
        if late>0: ax.text(t+p/2,-0.55,f"+{late}",ha="center",fontsize=11,color=BURG,fontweight="bold")
        t+=p
    ax.set_yticks([]); ax.set_xlim(0,29); ax.set_ylim(-0.9,0.7); ax.set_title(title,color=NAVY,fontsize=12.5)
fig,axs=plt.subplots(2,1,figsize=(11,4.6),gridspec_kw={"hspace":0.7})
gantt(axs[0],STATES[START],"(a) Start J1-J2-J3-J4-J5-J6: total tardiness 36 (red numbers = hours late)"); gantt(axs[1],STATES[OPT[1]],"(b) An optimum J4-J2-J6-J1-J5-J3: total tardiness 11"); axs[1].set_xlabel("hours on the bottleneck station")
save(fig,"SP_Fig_CH14_01.png")
# 14.2 density of states
vals,counts=np.unique(F,return_counts=True); fig,ax=plt.subplots(figsize=(11,4.4))
ax.bar(vals,counts,color=[GOLD if v==11 else NAVY for v in vals],width=0.8); ax.axvline(F.mean(),color=BURG,ls="--",lw=2); ax.set_ylim(0,42); ax.text(F.mean()+0.6,38.5,"mean of all 720 = 34.1",color=BURG,fontsize=12)
ax.annotate("optimum 11\n(2 sequences)",xy=(11,2),xytext=(13,22),arrowprops=dict(arrowstyle="->",color=GOLD,lw=1.8),color=GOLD,fontsize=12,fontweight="bold")
ax.set_xlabel("total tardiness (hours)"); ax.set_ylabel("number of sequences"); ax.set_xlim(9,58)
save(fig,"SP_Fig_CH14_03.png")
# 14.3 neighbors of START (adjacent swaps)
fig,ax=plt.subplots(figsize=(12,5.6)); ax.axis("off"); ax.set_xlim(0,12); ax.set_ylim(0,6.2)
rbox(ax,4.2,2.75,3.6,0.9,NAVY,NAVY); ax.text(6,3.2,"J1-J2-J3-J4-J5-J6   36",ha="center",va="center",color="white",fontsize=12.5,fontweight="bold",zorder=3)
pos=[(1.9,5.4),(10.1,5.4),(1.9,1.0),(10.1,1.0),(6,5.6)]; order=[0,1,3,4,2]
for k,(x,y) in zip(order,pos):
    yv=NA[START][k]; v=F[yv]; c=EMER if v<36 else BURG
    rbox(ax,x-1.85,y-0.45,3.7,0.9,IVORY,c); ax.text(x,y,f"{label(STATES[yv])}   {v}",ha="center",va="center",fontsize=11.5,color=NAVY,fontweight="bold",zorder=3)
    ax.add_patch(FancyArrowPatch((6,3.2),(x,y),arrowstyle="-|>",color=c,lw=1.8,mutation_scale=14,zorder=1,shrinkA=40,shrinkB=28))
    mx,my=(6+x)/2,(3.2+y)/2; ax.text(mx,my,f"swap {k+1}–{k+2}",fontsize=10.5,color=c,ha="center",bbox=dict(boxstyle="round,pad=0.15",fc="white",ec="none"),zorder=4)
ax.text(6,0.15,"green = better (lower tardiness), red = worse",ha="center",fontsize=11.5,color=SLATE)
save(fig,"SP_Fig_CH14_02.png")
# 14.4 plateau near the optimum
fig,ax=plt.subplots(figsize=(12,5.2)); ax.axis("off"); ax.set_xlim(0,12); ax.set_ylim(0,5.2)
nodes=[(1.9,3.4,"J6-J4-J2-J1-J5-J3","12",BURG),(6,3.4,"J4-J6-J2-J1-J5-J3","12",GOLD),(10.1,3.4,"J4-J2-J6-J1-J5-J3","11",EMER)]
for x,y,t,v,c in nodes: rbox(ax,x-1.6,y-0.55,3.2,1.1,IVORY,c); ax.text(x,y+0.17,t,ha="center",va="center",fontsize=11,color=NAVY,fontweight="bold",zorder=3); ax.text(x,y-0.25,f"tardiness {v}",ha="center",va="center",fontsize=11,color=c,fontweight="bold",zorder=3)
ax.add_patch(FancyArrowPatch((3.55,3.4),(4.35,3.4),arrowstyle="<|-|>",color=GOLD,lw=2.5,mutation_scale=16)); ax.text(3.95,3.75,"Δ = 0",ha="center",color=GOLD,fontsize=12,fontweight="bold")
ax.add_patch(FancyArrowPatch((7.65,3.4),(8.45,3.4),arrowstyle="-|>",color=EMER,lw=2.5,mutation_scale=16)); ax.text(8.05,3.75,"Δ = −1",ha="center",color=EMER,fontsize=12,fontweight="bold")
for i,v in enumerate([14,17,15,15]):
    xx=0.55+i*0.9; ax.add_patch(Circle((xx,1.4),0.32,fc="white",ec=BURG,lw=1.5,zorder=3)); ax.text(xx,1.4,str(v),ha="center",va="center",fontsize=11,color=BURG,zorder=4)
    ax.plot([xx,1.9],[1.72,2.85],color=BURG,lw=1,ls=":",zorder=1)
ax.text(1.9,0.6,"its other 4 neighbors\nare all worse",ha="center",fontsize=11,color=BURG)
ax.text(8.2,1.3,"strict greedy (accepts only Δ < 0) is stuck at the left box;\nMetropolis accepts Δ = 0 and walks out to the optimum",ha="center",fontsize=11.5,color=SLATE)
save(fig,"SP_Fig_CH14_04.png")
# 14.5 acceptance probability
fig,ax=plt.subplots(figsize=(10,4.4)); d=np.linspace(0,12,200)
for T,c in [(1,BURG),(3,GOLD),(10,EMER)]: ax.plot(d,np.exp(-d/T),color=c,lw=2.5,label=f"T = {T}")
ax.set_xlabel("increase in tardiness Δ (worse move)"); ax.set_ylabel("acceptance probability e^(−Δ/T)"); ax.set_ylim(0,1.05); ax.legend(frameon=False)
save(fig,"SP_Fig_CH14_05.png")
# 14.6 Boltzmann by level
fig,axs=plt.subplots(1,4,figsize=(17,4),sharey=True,gridspec_kw={"wspace":0.15})
for ax,T in zip(axs,[1,3,10,1e9]):
    b=boltzmann(T); lv=[b[F==v].sum() for v in vals]; ax.bar(vals,lv,color=[GOLD if v==11 else NAVY for v in vals],width=0.8)
    ax.set_title(("T = ∞ (uniform)" if T>1e6 else f"T = {T}")+f"\nP(optimum) = {b[OPT].sum():.3f}",color=NAVY,fontsize=12.5); ax.set_xlabel("tardiness")
axs[0].set_ylabel("stationary probability"); axs[0].set_ylim(0,0.62)
sep(fig,[0.31,0.515,0.715]); save(fig,"SP_Fig_CH14_06.png")
# 14.7 stationary check
M3=metropolis_adj(3); pi3=stationary(M3); b3=boltzmann(3)
rng=np.random.default_rng(147); x=START; visits=np.zeros(720); cum=np.cumsum(M3,axis=1)
for k in range(200000):
    x=int(np.searchsorted(cum[x],rng.random())); visits[x]+=1
fr=visits/visits.sum()
fig,axs=plt.subplots(1,2,figsize=(13,4.6),gridspec_kw={"wspace":0.3})
axs[0].loglog(b3,pi3,"o",color=NAVY,ms=4,alpha=0.7); axs[0].plot([1e-6,1],[1e-6,1],color=GOLD,lw=2); axs[0].set_xlabel("Boltzmann e^(−f/T)/Z"); axs[0].set_ylabel("stationary π of the 720×720 chain"); axs[0].set_title("(a) all 720 states lie on the diagonal (T = 3)",color=NAVY,fontsize=12.5); axs[0].set_xlim(1e-6,1); axs[0].set_ylim(1e-6,1)
lb=[b3[F==v].sum() for v in vals]; lf=[fr[F==v].sum() for v in vals]
axs[1].bar(vals-0.2,lb,width=0.4,color=GOLD,label="Boltzmann"); axs[1].bar(vals+0.2,lf,width=0.4,color=NAVY,label="simulated visits (200,000 steps)"); axs[1].set_xlim(9,32); axs[1].set_xlabel("tardiness"); axs[1].set_title("(b) one long run visits levels in Boltzmann proportions",color=NAVY,fontsize=12.5); axs[1].legend(frameon=False,fontsize=10.5)
sep(fig,[0.5]); save(fig,"SP_Fig_CH14_07.png"); print("sim P(opt) T=3",fr[OPT].sum(),"exact",b3[OPT].sum())
# 14.8 hitting times
Ts=np.array([0.5,0.75,1,1.5,2,3,4,6,10,20,50,1e6])
toyh=[hitting_times(toy_matrix(T),[17])[0] for T in Ts]; r6h=[hitting_times(metropolis_adj(T),OPT)[START] for T in Ts]
fig,axs=plt.subplots(1,3,figsize=(17,4.6),gridspec_kw={"wspace":0.32})
axs[0].bar(range(18),TOY,color=[GOLD if i==17 else (BURG if i==5 else NAVY) for i in range(18)],width=0.8); axs[0].set_xlabel("state (one step = one move)"); axs[0].set_ylabel("objective"); axs[0].set_title("(a) A landscape with one barrier",color=NAVY,fontsize=12.5)
axs[0].text(5,TOY[5]+1,"valley",ha="center",color=BURG,fontsize=11,fontweight="bold"); axs[0].text(17,TOY[17]+1,"goal",ha="center",color=GOLD,fontsize=11,fontweight="bold"); axs[0].set_ylim(0,45)
xl=["0.5","0.75","1","1.5","2","3","4","6","10","20","50","∞"]
axs[1].semilogy(range(len(Ts)),toyh,"-o",color=BURG,lw=2.5); axs[1].set_xticks(range(len(Ts))); axs[1].set_xticklabels(xl,fontsize=10); axs[1].set_xlabel("temperature T"); axs[1].set_ylabel("expected steps to the goal"); axs[1].set_title("(b) Barrier landscape: U-shaped, best T ≈ 4",color=NAVY,fontsize=12.5)
axs[2].semilogy(range(len(Ts)),r6h,"-o",color=NAVY,lw=2.5); axs[2].axhline(360,color=SLATE,ls=":",lw=1.5); axs[2].text(0.2,400,"random search: 360",color=SLATE,fontsize=11); axs[2].set_xticks(range(len(Ts))); axs[2].set_xticklabels(xl,fontsize=10); axs[2].set_xlabel("temperature T"); axs[2].set_title("(c) R6: single valley, lower T is faster",color=NAVY,fontsize=12.5)
sep(fig,[0.355,0.64]); save(fig,"SP_Fig_CH14_08.png"); print("toy",np.round(toyh,1)); print("r6",np.round(r6h,1))
# 14.9 30 runs (current value)
rng=np.random.default_rng(149); runs=[run_sa_adj(START,10,0.95,100,rng) for _ in range(30)]
fig,ax=plt.subplots(figsize=(11,4.6))
for h,_,_,_,_ in runs: ax.plot(range(101),h,color=NAVY,lw=0.8,alpha=0.35)
H=np.array([r[0] for r in runs]); ax.plot(range(101),np.median(H,axis=0),color=GOLD,lw=3,label="median of 30 runs"); ax.axhline(11,color=EMER,ls="--",lw=2,label="optimum 11")
ax.set_xlabel("iteration k"); ax.set_ylabel("tardiness of the current sequence"); ax.legend(frameon=False); ax.set_xlim(0,100)
save(fig,"SP_Fig_CH14_09.png"); print("30 runs success",sum(F[r[3]]==11 for r in runs),"first hits",[r[4] for r in runs])
# 14.10 best-so-far; temperature & acceptance rate
rng=np.random.default_rng(1410); acc=np.zeros(100); NR=10000
for r in range(NR):
    x=START
    for k in range(100):
        T=10*0.95**k; y=NA[x][rng.integers(5)]; d=F[y]-F[x]
        if d<=0 or rng.random()<np.exp(-d/T): x=y; acc[k]+=1
acc/=NR
fig,axs=plt.subplots(1,2,figsize=(13,4.6),gridspec_kw={"wspace":0.32})
for _,b,_,_,_ in runs: axs[0].step(range(101),b,where="post",color=NAVY,lw=0.9,alpha=0.4)
axs[0].axhline(11,color=EMER,ls="--",lw=2); axs[0].set_xlabel("iteration k"); axs[0].set_ylabel("best tardiness found so far"); axs[0].set_title("(a) Best-so-far, 30 runs",color=NAVY,fontsize=12.5)
k=np.arange(100); axs[1].plot(k,10*0.95**k,color=BURG,lw=2.5,label="temperature T_k = 10·0.95ᵏ"); axs[1].set_xlabel("iteration k"); axs[1].set_ylabel("temperature",color=BURG); axs[1].set_title("(b) Cooling and acceptance rate",color=NAVY,fontsize=12.5)
a2=axs[1].twinx(); a2.plot(k,acc,color=EMER,lw=2.5); a2.set_ylabel("share of proposals accepted",color=EMER); a2.set_ylim(0,1); a2.spines["top"].set_visible(False)
sep(fig,[0.5]); save(fig,"SP_Fig_CH14_10.png"); print("acc first, k=20, k=50, last",acc[0],acc[20],acc[50],acc[-1])
# 14.11 toy: fast vs slow cooling, 30 runs
fig,axs=plt.subplots(1,2,figsize=(13,4.6),sharey=True,gridspec_kw={"wspace":0.12})
for ax,a,tt in zip(axs,[0.95,0.99],["(a) fast cooling α = 0.95","(b) slow cooling α = 0.99"]):
    rng=np.random.default_rng(1411); ok=0
    for r in range(30):
        h,b=run_sa_toy(10,a,300,rng); ok+=(b==11); ax.plot(range(301),h,color=EMER if b==11 else BURG,lw=0.8,alpha=0.5)
    ax.set_title(f"{tt}: {ok} of 30 reach the goal",color=NAVY,fontsize=12.5); ax.set_xlabel("iteration k"); ax.axhline(25,color=BURG,ls=":",lw=1.2); ax.axhline(11,color=EMER,ls=":",lw=1.2)
axs[0].set_ylabel("objective of the current state"); sep(fig,[0.5]); save(fig,"SP_Fig_CH14_11.png")
# 14.12 comparison
lab=["random search\n(100 samples)","strict greedy\n(random start)","greedy with ties\n(random start)","SA, T₀ = 10,\nα = 0.95, 100 its"]; sr=[1-(718/720)**100,0.8333,1.0,0.9939]
fig,axs=plt.subplots(1,2,figsize=(14,4.6),gridspec_kw={"wspace":0.3})
b=axs[0].bar(lab,sr,color=[SLATE,BURG,EMER,GOLD],width=0.55); [axs[0].text(bi.get_x()+bi.get_width()/2,v+0.02,f"{v:.1%}",ha="center",fontsize=12,color=NAVY,fontweight="bold") for bi,v in zip(b,sr)]
axs[0].set_ylabel("probability of finding tardiness 11"); axs[0].set_ylim(0,1.15); axs[0].tick_params(axis="x",labelsize=10.5); axs[0].set_title("(a) Success rate",color=NAVY,fontsize=12.5)
ev=[360,26.2,28.1,46.8]; b=axs[1].bar(lab,ev,color=[SLATE,BURG,EMER,GOLD],width=0.55); [axs[1].text(bi.get_x()+bi.get_width()/2,v+6,f"{v:.0f}",ha="center",fontsize=12,color=NAVY,fontweight="bold") for bi,v in zip(b,ev)]
axs[1].set_ylabel("mean evaluations until stop / first optimum"); axs[1].tick_params(axis="x",labelsize=10.5); axs[1].set_title("(b) Effort",color=NAVY,fontsize=12.5); axs[1].set_ylim(0,420)
sep(fig,[0.5]); save(fig,"SP_Fig_CH14_12.png")
# 14.13 concept map
fig,ax=plt.subplots(figsize=(12,7)); ax.axis("off"); ax.set_xlim(0,12); ax.set_ylim(0,7.3); ax.set_aspect("equal")
def cbox(x,y,t,c=NAVY,fc=IVORY,w=2.9,h=1.0,tc=None): rbox(ax,x-w/2,y-h/2,w,h,fc,c,2.2); ax.text(x,y,t,ha="center",va="center",fontsize=11.5,color=tc or NAVY,fontweight="bold",zorder=3,linespacing=1.3)
def link(p1,p2): ax.add_patch(FancyArrowPatch(p1,p2,arrowstyle="-|>",color=SLATE,lw=1.8,mutation_scale=15,zorder=1))
cbox(6,6.5,"Simulated annealing = a Markov chain on solutions",NAVY,NAVY,tc="white",w=6.6)
cbox(2.5,4.8,"Landscape: states,\nobjective, neighbors",w=3.2); cbox(6,4.8,"Metropolis rule\nmin(1, e^(−Δ/T))"); cbox(9.5,4.8,"Boltzmann π ∝ e^(−f/T)\n(detailed balance)",w=3.4)
cbox(2.5,3.0,"Greedy = absorbing\nchain (traps, plateaus)",BURG,w=3.3); cbox(6,3.0,"Hitting time vs T:\nexploration–exploitation",CORAL,w=3.3); cbox(9.5,3.0,"Cooling = inhomogeneous\nchain (T₀, α)",EMER,w=3.4)
cbox(2.5,1.1,"Ch 9: absorption,\nfirst-step analysis",GOLD,w=3.1); cbox(6,1.1,"Ch 10: stationary law,\nreversibility",GOLD,w=3.2); cbox(9.5,1.1,"30 runs, CIs (Ch 5),\nGA next (Ch 15)",GOLD,w=3.2)
for b_ in [(2.5,5.3),(6,5.3),(9.5,5.3)]: link((6,6.0),b_)
for xx in (2.5,6,9.5): link((xx,4.3),(xx,3.5)); link((xx,2.5),(xx,1.6))
save(fig,"SP_Fig_CH14_13.png")
