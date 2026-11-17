"""SP_CH10 — Chapter 10 figures (long-run behavior of Markov chains) and number checks."""
import numpy as np, matplotlib, sys
matplotlib.use("Agg"); sys.path.insert(0,"/home/claude/ch10/code")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
from sp_ch09_markov import *
NAVY, GOLD, EMER, BURG, BLUE, CORAL, IVORY, SLATE = "#0B2545","#C9A227","#1B7F5C","#7A1E2B","#2E86AB","#E07A5F","#FBF8F1","#5B6B7C"
plt.rcParams.update({"font.size":14,"axes.titlesize":15,"axes.labelsize":14,"font.family":"DejaVu Sans","axes.edgecolor":SLATE,"axes.spines.top":False,"axes.spines.right":False,"axes.titlepad":10})
OUT="/home/claude/ch10/fig/"
def save(fig,name): fig.savefig(OUT+name,dpi=300,bbox_inches="tight",facecolor="white",pad_inches=0.15); plt.close(fig)
def rbox(ax,x,y,w,h,fc,ec,lw=2.5): ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0,rounding_size=0.12",fc=fc,ec=ec,lw=lw,zorder=2))
sep=lambda fig,xs: [fig.add_artist(plt.Line2D([x,x],[0.05,0.95],color=SLATE,lw=1.2,ls=":")) for x in xs]
def stat(P):
    n=P.shape[0]; A=np.vstack([P.T-np.eye(n),np.ones(n)]); b=np.r_[np.zeros(n),1]; return np.linalg.lstsq(A,b,rcond=None)[0]
# 10.1 class structure: three chains
fig,axs=plt.subplots(1,3,figsize=(16,5),gridspec_kw={"wspace":0.12})
def node(ax,x,y,t,c): ax.add_patch(Circle((x,y),0.5,fc=c,ec=c,zorder=3)); ax.text(x,y,t,ha="center",va="center",color="white",fontsize=14,fontweight="bold",zorder=4)
def arr(ax,a,b,rad=0.25): ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle="-|>",color=NAVY,lw=1.8,shrinkA=22,shrinkB=22,connectionstyle=f"arc3,rad={rad}"),zorder=2)
for ax in axs: ax.set_xlim(0,6); ax.set_ylim(-0.4,5); ax.axis("off"); ax.set_aspect("equal")
ax=axs[0]; node(ax,1.2,2.2,"W",EMER); node(ax,3,4.0,"S",GOLD); node(ax,4.8,2.2,"M",BURG)
arr(ax,(1.2,2.2),(3,4.0),-0.25); arr(ax,(3,4.0),(1.2,2.2),-0.25); arr(ax,(3,4.0),(4.8,2.2),-0.25); arr(ax,(4.8,2.2),(1.2,2.2),-0.35); arr(ax,(1.2,2.2),(4.8,2.2),-0.35)
ax.add_patch(Rectangle((0.3,1.3),5.4,3.4,fc="none",ec=EMER,lw=2,ls="--")); ax.text(3,0.5,"(a) R2 machine: one closed class\nirreducible and aperiodic",ha="center",fontsize=12,color=NAVY)
ax=axs[1]; node(ax,1,3.8,"S",SLATE); node(ax,3,3.8,"G",GOLD); node(ax,5,3.8,"P",EMER); node(ax,3,1.3,"C",BURG)
arr(ax,(1,3.8),(3,3.8),-0.3); arr(ax,(3,3.8),(1,3.8),-0.3); arr(ax,(3,3.8),(5,3.8),-0.3); arr(ax,(5,3.8),(3,3.8),-0.3); arr(ax,(1,3.8),(3,1.3),0.2); arr(ax,(3,3.8),(3,1.3),0); arr(ax,(5,3.8),(3,1.3),-0.2)
ax.add_patch(Rectangle((0.3,3.1),5.4,1.4,fc="none",ec=SLATE,lw=2,ls="--")); ax.add_patch(Rectangle((2.3,0.6),1.4,1.4,fc="none",ec=BURG,lw=2,ls="--")); ax.text(3,-0.1,"(b) R3 club: transient class {S, G, P}\nand absorbing class {C}",ha="center",fontsize=12,color=NAVY)
ax=axs[2]; node(ax,1.8,2.6,"1",NAVY); node(ax,4.2,2.6,"2",NAVY); arr(ax,(1.8,2.6),(4.2,2.6),-0.45); arr(ax,(4.2,2.6),(1.8,2.6),-0.45); ax.text(3,3.9,"1",fontsize=13,color=NAVY,ha="center"); ax.text(3,1.3,"1",fontsize=13,color=NAVY,ha="center")
ax.text(3,0.3,"(c) Period 2: irreducible but not\naperiodic — Pⁿ never settles",ha="center",fontsize=12,color=NAVY)
sep(fig,[0.365,0.66]); save(fig,"SP_Fig_CH10_01.png")
# 10.2 convergence of P2^n rows
fig,ax=plt.subplots(figsize=(10,4.6)); ns=np.arange(0,16); pi=stat(P2)
for i,(lab,c) in enumerate([("start W",EMER),("start S",GOLD),("start M",BURG)]): ax.plot(ns,[nstep(P2,n)[i,2] for n in ns],"-o",color=c,lw=2.3,ms=5,label=f"P(in maintenance at shift n | {lab})")
ax.axhline(pi[2],color=NAVY,ls="--",lw=2,label=f"π_M = {pi[2]:.4f}"); ax.set_xlabel("shift n"); ax.set_ylabel("probability"); ax.set_ylim(0,0.55); ax.legend(frameon=False,fontsize=11)
save(fig,"SP_Fig_CH10_03.png")
# 10.3 periodic oscillation vs aperiodic
fig,axs=plt.subplots(1,2,figsize=(13,4.2),gridspec_kw={"wspace":0.3}); ns=np.arange(0,13)
Pp=np.array([[0,1],[1,0]]); axs[0].step(ns,[nstep(Pp,n)[0,0] for n in ns],"-o",where="post",color=BURG,lw=2); axs[0].set_title("(a) Period 2: P(state 1 at n | start 1) alternates 1, 0, 1, 0, …",color=NAVY,fontsize=12); axs[0].set_ylim(-0.1,1.1); axs[0].set_xlabel("n")
Pa=np.array([[0.1,0.9],[0.9,0.1]]); axs[1].plot(ns,[nstep(Pa,n)[0,0] for n in ns],"-o",color=EMER,lw=2); axs[1].axhline(0.5,color=NAVY,ls="--"); axs[1].set_title("(b) A little self-loop (0.1) breaks the period: converges to 0.5",color=NAVY,fontsize=12); axs[1].set_ylim(-0.1,1.1); axs[1].set_xlabel("n")
sep(fig,[0.5]); save(fig,"SP_Fig_CH10_02.png")
# 10.4 brand switching
Pb=np.array([[.80,.15,.05],[.10,.75,.15],[.05,.20,.75]]); a=np.array([.5,.3,.2]); ns=np.arange(0,25); D=np.array([a@nstep(Pb,n) for n in ns]); pb=stat(Pb)
fig,ax=plt.subplots(figsize=(10,4.6))
for j,(lab,c) in enumerate([("Nava",NAVY),("Rival X",GOLD),("Rival Y",BURG)]): ax.plot(ns,D[:,j],"-o",color=c,lw=2.3,ms=4,label=f"{lab} (→ {pb[j]:.3f})"); ax.axhline(pb[j],color=c,ls=":",lw=1.2)
ax.set_xlabel("month"); ax.set_ylabel("market share"); ax.set_ylim(0,0.6); ax.legend(frameon=False)
save(fig,"SP_Fig_CH10_04.png")
# 10.5 credit migration: P(default by year n)
Pc=np.array([[.90,.08,.015,.005],[.05,.85,.08,.02],[.01,.10,.80,.09],[0,0,0,1]]); ns=np.arange(0,21)
fig,ax=plt.subplots(figsize=(10,4.6))
for i,(lab,c) in enumerate([("rating A",EMER),("rating B",GOLD),("rating C",BURG)]): ax.plot(ns,[nstep(Pc,n)[i,3] for n in ns],"-o",color=c,lw=2.3,ms=4,label=lab)
ax.set_xlabel("years"); ax.set_ylabel("cumulative probability of default"); ax.legend(frameon=False); ax.set_ylim(0,0.9)
save(fig,"SP_Fig_CH10_05.png")
# 10.6 PageRank graph
fig,ax=plt.subplots(figsize=(9,4.6)); ax.axis("off"); ax.set_xlim(0,9); ax.set_ylim(0,4.6); ax.set_aspect("equal")
pos={1:(1.5,3.4),2:(4.5,3.8),3:(4.5,1.2),4:(7.5,2.5)}; pr=[0.380,0.199,0.384,0.038]
for k,(x,y) in pos.items(): ax.add_patch(Circle((x,y),0.55,fc=[NAVY,GOLD,EMER,SLATE][k-1],ec="none",zorder=3)); ax.text(x,y,f"Page {k}",ha="center",va="center",color="white",fontsize=11,fontweight="bold",zorder=4); ax.text(x,y-0.95,f"rank {pr[k-1]:.3f}",ha="center",fontsize=11,color=NAVY)
for a_,b_,rad in [(1,2,0.2),(1,3,-0.2),(2,3,0),(3,1,0.3),(4,1,0.3),(4,3,-0.3)]: ax.annotate("",xy=pos[b_],xytext=pos[a_],arrowprops=dict(arrowstyle="-|>",color=SLATE,lw=1.8,shrinkA=22,shrinkB=22,connectionstyle=f"arc3,rad={rad}"))
ax.set_title("A random surfer on four pages",color=NAVY,fontsize=13)
save(fig,"SP_Fig_CH10_07.png")
# 10.7 inventory policies cost
fig,ax=plt.subplots(figsize=(9,4.2)); pols=["Policy A: order up to 2","Policy B: order up to 3"]; costs=[3.25,3.27]
b=ax.bar(pols,costs,color=[NAVY,GOLD],width=0.5); [ax.text(bi.get_x()+bi.get_width()/2,v+0.05,f"{v:.2f} €/day",ha="center",fontsize=12,color=NAVY,fontweight="bold") for bi,v in zip(b,costs)]
ax.set_ylabel("long-run average cost per day (€)"); ax.set_ylim(0,4)
save(fig,"SP_Fig_CH10_06.png")
# 10.8 detailed balance picture
fig,ax=plt.subplots(figsize=(10,3.2)); ax.axis("off"); ax.set_xlim(0,10); ax.set_ylim(0,3.2)
for i in range(5):
    x=1+i*2; ax.add_patch(Circle((x,1.6),0.42,fc=IVORY,ec=NAVY,lw=2.5)); ax.text(x,1.6,str(i) if i<4 else "…",ha="center",va="center",fontsize=14,color=NAVY,fontweight="bold")
    if i<4:
        ax.annotate("",xy=(x+1.55,1.95),xytext=(x+0.45,1.95),arrowprops=dict(arrowstyle="-|>",color=NAVY,lw=2,connectionstyle="arc3,rad=-0.4")); ax.annotate("",xy=(x+0.45,1.25),xytext=(x+1.55,1.25),arrowprops=dict(arrowstyle="-|>",color=BURG,lw=2,connectionstyle="arc3,rad=-0.4"))
        ax.text(x+1,2.75,f"π{i}·u{i}",ha="center",fontsize=12,color=NAVY,fontweight="bold"); ax.text(x+1,0.35,f"π{i+1}·d{i+1}",ha="center",fontsize=12,color=BURG,fontweight="bold")
ax.text(5,3.1,"Detailed balance on a birth–death chain: flow right across each edge = flow left",ha="center",fontsize=12,color=SLATE)
save(fig,"SP_Fig_CH10_08.png")
# 10.9 simulation R2 long run
rng=np.random.default_rng(10); path=np.array(simulate(P2,0,10000,rng)); fr=np.array([[np.mean(path[:n]==s) for s in range(3)] for n in range(1,10001)])
fig,ax=plt.subplots(figsize=(10,4.6)); pi=stat(P2)
for s,(lab,c) in enumerate([("W",EMER),("S",GOLD),("M",BURG)]): ax.plot(np.arange(1,10001),fr[:,s],color=c,lw=1.8,label=f"fraction of shifts in {lab} so far"); ax.axhline(pi[s],color=c,ls="--",lw=1.5)
ax.set_xscale("log"); ax.set_xlabel("shifts observed (log scale)"); ax.set_ylabel("running fraction"); ax.legend(frameon=False,fontsize=11); ax.set_ylim(0,1)
save(fig,"SP_Fig_CH10_09.png"); print("sim fractions",fr[-1].round(4),"pi",pi.round(4))
# 10.10 concept map
fig,ax=plt.subplots(figsize=(12,7)); ax.axis("off"); ax.set_xlim(0,12); ax.set_ylim(0,7.3); ax.set_aspect("equal")
def cbox(x,y,t,c=NAVY,fc=IVORY,w=2.9,h=1.0,tc=None): rbox(ax,x-w/2,y-h/2,w,h,fc,c,2.2); ax.text(x,y,t,ha="center",va="center",fontsize=11.5,color=tc or NAVY,fontweight="bold",zorder=3,linespacing=1.3)
def link(p1,p2): ax.add_patch(FancyArrowPatch(p1,p2,arrowstyle="-|>",color=SLATE,lw=1.8,mutation_scale=15,zorder=1))
cbox(6,6.5,"Long-run behavior of a Markov chain",NAVY,NAVY,tc="white",w=5.6)
cbox(2.5,4.8,"Classes: transient,\nrecurrent, absorbing"); cbox(6,4.8,"Stationary π = πP\n(balance equations)"); cbox(9.5,4.8,"Irreducible + aperiodic\n⇒ Pⁿ → π",w=3.2)
cbox(2.5,3.0,"Period & reducibility:\nwhen limits fail",BURG,w=3.2); cbox(6,3.0,"Fraction of time, mean\nreturn 1/πᵢ, average cost",EMER,w=3.4); cbox(9.5,3.0,"Reversibility*\n(detailed balance)",CORAL)
cbox(2.5,1.1,"Brands, credit ratings,\ninventory, PageRank",GOLD,w=3.3); cbox(6,1.1,"Estimating P\nfrom data",GOLD); cbox(9.5,1.1,"Continuous time\n(Ch 11), SA (Ch 14)",GOLD)
for b in [(2.5,5.3),(6,5.3),(9.5,5.3)]: link((6,6.0),b)
for xx in (2.5,6,9.5): link((xx,4.3),(xx,3.5)); link((xx,2.5),(xx,1.6))
save(fig,"SP_Fig_CH10_10.png")
# checks
def show(l,v): print(f"{l:<60} {v}")
show("Ex 10.5 R2 pi, return times",(stat(P2).round(4),(1/stat(P2)).round(2)))
show("Ex 10.6 server pi",stat(np.array([[.9,.1],[.3,.7]])).round(3))
show("Ex 10.7 weather pi",stat(W).round(4))
show("Ex 10.8 inventory pi",stat(np.array([[.5,.5],[.3,.7]])).round(4))
show("Ex 10.9 P2^n rows n=5,10",(nstep(P2,5).round(4),nstep(P2,10).round(4)))
show("Ex 10.12 R2 avg cost (S 800, M 1200)",round(stat(P2)@np.array([0,800,1200]),1))
Pp=np.array([[.86,.10,.04],[0,0,1],[.5,0,.5]]); show("Ex 10.13 proactive pi, cost",(stat(Pp).round(4),round(stat(Pp)@np.array([0,800,1200]),1)))
show("Ex 10.14 brands pi; shares after 1,5,10",(pb.round(4),[(a@nstep(Pb,n)).round(3) for n in (1,5,10)]))
show("Ex 10.15 credit default by 5,10; years to default",([nstep(Pc,n)[:3,3].round(3) for n in (5,10)],hitting_time(Pc,[3])[:3].round(1)))
show("Ex 10.16 inventory policies A,B cost",(3.25,round(stat(np.array([[.5,0,.5],[.3,.5,.2],[.2,.3,.5]]))@np.array([1+1+2,2+0.8,3]),3)))
Lk={0:[1,2],1:[2],2:[0],3:[0,2]}; M=np.zeros((4,4))
for i,ls in Lk.items():
    for j in ls: M[i,j]=1/len(ls)
show("Ex 10.17 pagerank",stat(0.85*M+0.15/4).round(4))
show("Ex 10.19 slotted queue pi0, pi1",(0.4,round(0.4*0.3/0.35,4)))
show("Ex 10.20 estimate from counts: W row (860,100,40)/1000",(0.86,0.10,0.04))
