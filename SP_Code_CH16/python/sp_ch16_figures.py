"""SP_CH16 v2 — figures for the textbook Keshtel algorithm on R6 (reads ka2_results.json, ka2_sweep.json, ka2_ttt.json)."""
import numpy as np, matplotlib, json, sys
matplotlib.use("Agg"); sys.path.insert(0,"/home/claude/ch16/code")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
NAVY, GOLD, EMER, BURG, BLUE, CORAL, IVORY, SLATE = "#0B2545","#C9A227","#1B7F5C","#7A1E2B","#2E86AB","#E07A5F","#FBF8F1","#5B6B7C"
plt.rcParams.update({"font.size":14,"axes.titlesize":15,"axes.labelsize":14,"font.family":"DejaVu Sans","axes.edgecolor":SLATE,"axes.spines.top":False,"axes.spines.right":False,"axes.titlepad":10})
OUT="/home/claude/ch16/fig/"; D="/home/claude/ch16/code/"
R=json.load(open(D+"ka2_results.json")); SW=json.load(open(D+"ka2_sweep.json")); T=json.load(open(D+"ka2_ttt.json"))
def save(fig,n): fig.savefig(OUT+f"SP_Fig_CH16_{n:02d}.png",dpi=300,bbox_inches="tight",facecolor="white",pad_inches=0.15); plt.close(fig)
def rbox(ax,x,y,w,h,fc,ec,lw=2.5): ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0,rounding_size=0.12",fc=fc,ec=ec,lw=lw,zorder=2))
sep=lambda fig,xs: [fig.add_artist(plt.Line2D([x,x],[0.05,0.95],color=SLATE,lw=1.2,ls=":")) for x in xs]
# 16.1 one iteration
fig,ax=plt.subplots(figsize=(13,6.4)); ax.axis("off"); ax.set_xlim(0,13); ax.set_ylim(-0.6,6.4)
for i in range(10):
    c=GOLD if i<2 else (BLUE if i<7 else BURG); ax.add_patch(Rectangle((0.5,5.4-i*0.55),1.4,0.45,fc=c,ec="white")); ax.text(1.2,5.62-i*0.55,f"rank {i+1}",ha="center",va="center",color="white",fontsize=10,fontweight="bold")
ax.text(1.2,5.95,"sorted keshtels",ha="center",fontsize=11.5,color=NAVY,fontweight="bold")
for x,y,t,c,src in [(5.6,4.9,"N1 lucky (2): attract the nearest neighbor,\nask “slope or pit?”, bisection swirl\n(L ± r/2ˢ, …) up to Smax rounds",GOLD,(1.95,5.35)),(5.6,2.7,"N3 remaining (5): move toward the middle\nof two other keshtels, X + α((G + H)/2 − X),\nalways accepted",BLUE,(1.95,3.4)),(5.6,0.5,"N2 unlucky (3): fly away;\nnew keshtels land at random\n(fresh blood)",BURG,(1.95,0.95))]:
    rbox(ax,x-2.6,y-0.8,5.2,1.6,IVORY,c); ax.text(x,y,t,ha="center",va="center",fontsize=10.8,color=NAVY,zorder=3,linespacing=1.35)
    ax.add_patch(FancyArrowPatch(src,(x-2.65,y),arrowstyle="-|>",color=c,lw=2,mutation_scale=15))
rbox(ax,9.8,2.0,2.8,2.2,NAVY,NAVY); ax.text(11.2,3.1,"re-sort;\nnext iteration\n(best never lost)",ha="center",va="center",color="white",fontsize=11.5,fontweight="bold",zorder=3)
for y in (4.9,2.7,0.5): ax.add_patch(FancyArrowPatch((8.25,y),(9.75,3.1),arrowstyle="-|>",color=SLATE,lw=1.8,mutation_scale=14))
ax.text(6.5,-0.45,"Keys in [0, 1]⁶ are decoded by sorting: the job with the smallest key goes first",ha="center",fontsize=11.5,color=BURG,fontweight="bold")
save(fig,1)
# helpers
def arr(name,k): return np.array([o[k] if o[k] is not None else 10**9 for o in T[name]],float)
# 16.2 bound vs actual
e=np.arange(1,201); ka=arr("KA",0); notfound=np.array([np.mean(ka>x) for x in e]); g=np.floor(np.maximum(e-10,0)/48); bound=(718/720)**(np.minimum(e,10)+3*g)
fig,ax=plt.subplots(figsize=(10,4.4)); ax.semilogy(e,np.maximum(notfound,1e-4),color=GOLD,lw=2.5,label="Keshtel: P(optimum not yet found), simulated"); ax.semilogy(e,bound,color=BURG,lw=2.5,ls="--",label="guarantee from the unlucky landings alone")
ax.set_xlabel("evaluations"); ax.set_ylabel("P(optimum not found yet)"); ax.set_ylim(1e-2,1.1); ax.legend(frameon=False,fontsize=11); save(fig,2)
# 16.3 group contributions
a=np.array(R["groups"]["imp"]); b=np.array(R["groups"]["first"]); fig,ax=plt.subplots(figsize=(10,4.4)); x=np.arange(3)
ax.bar(x-0.18,a,0.36,color=NAVY,label="share of all improvements of the best"); ax.bar(x+0.18,b,0.36,color=GOLD,label="share of first discoveries of 11")
for xi,(u,v) in enumerate(zip(a,b)): ax.text(xi-0.18,u+0.015,f"{u:.1%}",ha="center",fontsize=11); ax.text(xi+0.18,v+0.015,f"{v:.1%}",ha="center",fontsize=11)
ax.set_xticks(x); ax.set_xticklabels(["N1 lucky (swirl)","N2 unlucky (landing)","N3 remaining (move)"]); ax.set_ylim(0,1.1); ax.legend(frameon=False); ax.set_ylabel("share (2,000 runs)"); save(fig,3)
# 16.4 ablation
ab=R["ablation"]; labs=["full","N1 = 0","N2 = 0","N3 = 0","N2 only"]; keys=["full","no lucky (N1=0)","no unlucky (N2=0)","no remaining (N3=0)","unlucky only"]; cols=[GOLD,BLUE,BURG,EMER,SLATE]
fig,axs=plt.subplots(1,2,figsize=(14,4.6),gridspec_kw={"wspace":0.3})
for ax,idx,yl,tit,fmt in [(axs[0],1,"P(optimum within 100 evaluations)","(a) Success by 100 evaluations","{:.2f}"),(axs[1],2,"mean evaluations to first optimum","(b) Effort (successful runs)","{:.0f}")]:
    v=[ab[k][idx] for k in keys]; bb=ax.bar(labs,v,color=cols,width=0.55)
    for bi,val in zip(bb,v): ax.text(bi.get_x()+bi.get_width()/2,val*1.02+0.005,fmt.format(val),ha="center",fontsize=11.5)
    ax.set_ylabel(yl); ax.set_title(tit,color=NAVY,fontsize=12.5); ax.set_ylim(0,max(v)*1.2)
sep(fig,[0.5]); save(fig,4)
# 16.5 thirty runs
fig,axs=plt.subplots(1,2,figsize=(13,4.6),gridspec_kw={"wspace":0.3})
for h in R["runs30"]["hist"]:
    e_,b_=zip(*h); axs[0].step(e_,b_,where="post",color=NAVY,lw=0.9,alpha=0.45)
for m in R["runs30"]["means"]: axs[1].plot(range(len(m)),m,color=GOLD,lw=0.9,alpha=0.6)
axs[0].axhline(11,color=EMER,ls="--",lw=2); axs[0].set_xlabel("evaluations"); axs[0].set_ylabel("best tardiness so far"); axs[0].set_xlim(0,200); axs[0].set_title("(a) Best so far, 30 runs",color=NAVY,fontsize=12.5)
axs[1].set_xlabel("iteration"); axs[1].set_ylabel("mean tardiness of the population"); axs[1].set_title("(b) Population mean by iteration",color=NAVY,fontsize=12.5)
sep(fig,[0.5]); save(fig,5)
# 16.6 diversity
fig,ax=plt.subplots(figsize=(10,4.4)); dk=R["div"]["ka"]; dg=R["div"]["ga"]
ax.plot(range(len(dk)),dk,"-o",color=GOLD,lw=2.3,ms=6,label="Keshtel (per iteration, ≈ 48 evaluations)"); ax.plot(range(len(dg)),dg,"-s",color=NAVY,lw=2.3,ms=4,label="GA, p_m = 0.2 (per generation, 9 evaluations)")
ax.set_xlabel("iteration / generation"); ax.set_ylabel("distinct schedules (out of 10)"); ax.set_ylim(0,10.5); ax.legend(frameon=False,fontsize=11); save(fig,6)
# 16.7 sweep
S=SW["S100"]; MF=SW["MF"]; A1=np.array([[S[f"{a},{b}"] for b in range(5)] for a in (1,2,3,4)]); A2=np.array([[MF[f"{a},{b}"] for b in range(5)] for a in (1,2,3,4)])
fig,axs=plt.subplots(1,2,figsize=(13,4.4),gridspec_kw={"wspace":0.35})
for ax,M_,t,fmt,cm in [(axs[0],A1,"(a) P(found by 100 evaluations)","{:.2f}","YlGn"),(axs[1],A2,"(b) mean evaluations to first optimum","{:.0f}","YlOrBr_r")]:
    ax.imshow(M_,cmap=cm,aspect="auto"); lo,hi=M_.min(),M_.max()
    for i in range(4):
        for j in range(5):
            z=(M_[i,j]-lo)/(hi-lo+1e-12); dark=z>0.6 if cm=="YlGn" else z<0.4
            ax.text(j,i,fmt.format(M_[i,j]),ha="center",va="center",fontsize=12,color="white" if dark else "black")
    ax.set_xticks(range(5)); ax.set_xticklabels(["0","1","2","3","4"]); ax.set_yticks(range(4)); ax.set_yticklabels(["1","2","3","4"]); ax.set_xlabel("unlucky N2"); ax.set_ylabel("lucky N1"); ax.set_title(t,color=NAVY,fontsize=12.5)
sep(fig,[0.5]); save(fig,7)
# 16.8 time to target, two counting rules
fig,axs=plt.subplots(1,2,figsize=(14,4.8),sharey=True,gridspec_kw={"wspace":0.08}); x=np.arange(1,201)
for ax,k,tit in [(axs[0],0,"(a) every trial point counted"),(axs[1],1,"(b) distinct schedules only (memory for every method)")]:
    for name,c,lab in [("greedy",EMER,"greedy with ties"),("SA",BURG,"simulated annealing"),("GA",NAVY,"GA, p_m = 0.4"),("KA",GOLD,"Keshtel (2 / 3 / 5, Smax = 2)"),("random",SLATE,"random search")]:
        v=arr(name,k); ax.plot(x,[np.mean(v<=t) for t in x],color=c,lw=2.4,label=lab)
    ax.set_title(tit,color=NAVY,fontsize=12.5); ax.set_xlabel("evaluations"); ax.set_ylim(0,1.02)
axs[0].set_ylabel("P(optimum found)"); axs[1].legend(frameon=False,fontsize=10.5,loc="lower right"); sep(fig,[0.505]); save(fig,8)
# 16.9 concept map
fig,ax=plt.subplots(figsize=(12,7)); ax.axis("off"); ax.set_xlim(0,12); ax.set_ylim(0,7.3); ax.set_aspect("equal")
def cbox(x,y,t,c=NAVY,fc=IVORY,w=2.9,h=1.0,tc=None): rbox(ax,x-w/2,y-h/2,w,h,fc,c,2.2); ax.text(x,y,t,ha="center",va="center",fontsize=11.5,color=tc or NAVY,fontweight="bold",zorder=3,linespacing=1.3)
def link(p1,p2): ax.add_patch(FancyArrowPatch(p1,p2,arrowstyle="-|>",color=SLATE,lw=1.8,mutation_scale=15,zorder=1))
cbox(6,6.5,"Keshtel algorithm = a population with three roles",NAVY,NAVY,tc="white",w=6.6)
cbox(2.5,4.8,"Lucky: swirl that\naccepts only better",GOLD,w=3.1); cbox(6,4.8,"Remaining: move to the\nmiddle of two others",BLUE,w=3.3); cbox(9.5,4.8,"Unlucky: fly away,\nnew ones land",BURG,w=3.0)
cbox(2.5,3.0,"Built-in elitism;\nself-adaptive radius",w=3.1); cbox(6,3.0,"Random keys and\ndecoding; lake memory",w=3.3); cbox(9.5,3.0,"Irreducibility and the\ngeometric guarantee",w=3.1)
cbox(2.5,1.1,"Ch 14: greedy,\nhitting time",GOLD,w=2.9); cbox(6,1.1,"Ch 15: diversity,\nfair comparison",GOLD,w=2.9); cbox(9.5,1.1,"Part V synthesis:\nSA · GA · KA",GOLD,w=2.9)
for b_ in [(2.5,5.3),(6,5.3),(9.5,5.3)]: link((6,6.0),b_)
for xx in (2.5,6,9.5): link((xx,4.3),(xx,3.5)); link((xx,2.5),(xx,1.6))
save(fig,9)
