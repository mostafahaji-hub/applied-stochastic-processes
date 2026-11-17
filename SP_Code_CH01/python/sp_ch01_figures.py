"""SP_CH01 — figures (v2: clean layout, full borders, separators, no overlapping text) and number checks."""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch, FancyArrowPatch
from math import comb, perm, factorial
NAVY, GOLD, EMER, BURG, BLUE, CORAL, IVORY, SLATE = "#0B2545","#C9A227","#1B7F5C","#7A1E2B","#2E86AB","#E07A5F","#FBF8F1","#5B6B7C"
plt.rcParams.update({"font.size":14,"axes.titlesize":15,"axes.labelsize":14,"font.family":"DejaVu Sans","axes.edgecolor":SLATE,"axes.spines.top":False,"axes.spines.right":False,"axes.titlepad":10})
OUT="/home/claude/ch01/fig/"
def save(fig,name): fig.savefig(OUT+name,dpi=300,bbox_inches="tight",facecolor="white",pad_inches=0.15); plt.close(fig)
def rbox(ax,x,y,w,h,fc,ec,lw=2.5): ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0,rounding_size=0.15",fc=fc,ec=ec,lw=lw,mutation_aspect=1,zorder=2))

# ---------- Fig 1.1 ----------
fig,ax=plt.subplots(figsize=(11,6)); ax.axis("off"); ax.set_xlim(0,11); ax.set_ylim(0,6); ax.set_aspect("equal")
rbox(ax,3.9,2.3,3.2,1.4,NAVY,NAVY); ax.text(5.5,3.0,"Nava\nOperations",color="white",ha="center",va="center",fontsize=17,fontweight="bold",zorder=3)
nodes=[(1.6,4.9,"CALL CENTER\nHow many calls\nin the next minute?",BLUE),(9.4,4.9,"PACKING LINE\nWill machine 3\nstop today?",EMER),
       (1.6,1.1,"CUSTOMER CLUB\nWho upgrades,\nwho leaves?",CORAL),(9.4,1.1,"CASH & DEMAND\nHow many orders\ntomorrow?",GOLD)]
for x,y,t,c in nodes:
    rbox(ax,x-1.5,y-0.8,3.0,1.6,IVORY,c); ax.text(x,y,t,ha="center",va="center",fontsize=12,color=NAVY,zorder=3,linespacing=1.4)
    ex=x+1.5 if x<5.5 else x-1.5; tx=3.9 if x<5.5 else 7.1; ty=3.5 if y>3 else 2.5
    ax.plot([ex,tx],[y,ty],color=c,lw=2.2,ls="--",zorder=1)
save(fig,"SP_Fig_CH01_01.png")

# ---------- Fig 1.2 ----------
fig,axs=plt.subplots(1,3,figsize=(15,4.8),gridspec_kw={"wspace":0.45})
ax=axs[0]; ax.set_xlim(-0.6,1.6); ax.set_ylim(-0.6,1.6); ax.set_aspect("equal"); ax.set_xticks([0,1]); ax.set_yticks([0,1])
ax.set_xticklabels(["On time","Late"]); ax.set_yticklabels(["On time","Late"]); ax.set_xlabel("Van A"); ax.set_ylabel("Van B")
for i in range(2):
    for j in range(2):
        ax.add_patch(Rectangle((i-0.45,j-0.45),0.9,0.9,fc=IVORY,ec=NAVY,lw=2)); ax.text(i,j,f"({'OL'[i]}, {'OL'[j]})",ha="center",va="center",fontsize=15,color=NAVY,fontweight="bold")
ax.set_title("(a) Finite\ntwo vans, 4 outcomes",color=NAVY)
ax=axs[1]; ks=np.arange(0,8); ax.scatter(ks,np.zeros_like(ks),s=180,color=NAVY,zorder=3); ax.text(7.9,-0.02,"…",fontsize=22,color=NAVY,va="center")
for k in ks: ax.text(k,-0.16,str(k),ha="center",fontsize=13)
ax.set_xlim(-0.6,8.6); ax.set_ylim(-0.4,0.4); ax.axis("off"); ax.set_title("(b) Countably infinite\nnumber of calls in a minute",color=NAVY)
ax=axs[2]; ax.hlines(0,0,9.3,color=NAVY,lw=4); ax.scatter([0],[0],s=180,color=NAVY,zorder=3); ax.annotate("",xy=(10,0),xytext=(9,0),arrowprops=dict(arrowstyle="-|>",color=NAVY,lw=3))
ax.scatter([3.7],[0],s=220,color=GOLD,zorder=4); ax.text(3.7,0.13,"t = 3.7 min",ha="center",color=NAVY,fontweight="bold",fontsize=13)
ax.text(0,-0.16,"0",ha="center",fontsize=13); ax.set_xlim(-0.6,10.5); ax.set_ylim(-0.4,0.4); ax.axis("off"); ax.set_title("(c) Continuous\nwaiting time to the next call",color=NAVY)
for xpos in (0.355,0.675): fig.add_artist(plt.Line2D([xpos,xpos],[0.08,0.95],color=SLATE,lw=1.2,ls=":"))
save(fig,"SP_Fig_CH01_02.png")

# ---------- Fig 1.3 ----------
fig,axs=plt.subplots(1,3,figsize=(15,5.2),gridspec_kw={"wspace":0.25})
titles=["(a) Union  F ∪ E","(b) Intersection  F ∩ E","(c) Complement  F′"]
for k,ax in enumerate(axs):
    ax.set_xlim(0,10); ax.set_ylim(0,6.4); ax.axis("off"); ax.set_aspect("equal")
    ax.add_patch(Rectangle((0.3,0.3),9.4,5.6,fc=("#D9E2F1" if k==2 else IVORY),ec=NAVY,lw=2))
    if k==0: ax.add_patch(Circle((4,3),2.1,fc="#D9E2F1",ec="none")); ax.add_patch(Circle((6,3),2.1,fc="#F3E7B8",ec="none"))
    if k==1: p=Circle((6,3),2.1,fc=GOLD,ec="none"); ax.add_patch(p); p.set_clip_path(Circle((4,3),2.1,transform=ax.transData))
    if k==2: ax.add_patch(Circle((6,3),2.1,fc="#D9E2F1",ec="none")); ax.add_patch(Circle((4,3),2.1,fc="white",ec="none"))
    ax.add_patch(Circle((4,3),2.1,fc="none",ec=NAVY,lw=2.5)); ax.add_patch(Circle((6,3),2.1,fc="none",ec=GOLD,lw=2.5))
    ax.text(2.2,5.35,"F",color=NAVY,fontsize=17,fontweight="bold"); ax.text(7.5,5.35,"E",color=GOLD,fontsize=17,fontweight="bold")
    ax.text(9.4,0.55,"S",color=NAVY,fontsize=15,fontweight="bold",ha="right")
    for xx,tt in ((3.0,"20"),(5.0,"10"),(7.0,"15")): ax.text(xx,3,tt,ha="center",va="center",fontsize=15,color=NAVY,fontweight="bold")
    ax.text(1.0,0.75,"55",fontsize=15,color=NAVY,fontweight="bold")
    ax.set_title(titles[k],color=NAVY,fontsize=15)
for xpos in (0.36,0.655): fig.add_artist(plt.Line2D([xpos,xpos],[0.05,0.95],color=SLATE,lw=1.2,ls=":"))
save(fig,"SP_Fig_CH01_03.png")

# ---------- Fig 1.4 ----------
days=200; late_counts={"Van 2":19,"Van 3":28,"Van 7":46,"Van 11":61}
fig,ax=plt.subplots(figsize=(10,5))
vans=list(late_counts); vals=[late_counts[v]/days for v in vans]
bars=ax.bar(vans,vals,color=[EMER,BLUE,NAVY,BURG],width=0.55)
for b,v,cnt in zip(bars,vals,[late_counts[v] for v in vans]):
    ax.text(b.get_x()+b.get_width()/2,v+0.012,f"{cnt} / 200",ha="center",color=NAVY,fontsize=13,fontweight="bold")
    ax.text(b.get_x()+b.get_width()/2,v/2,f"{v:.3f}",ha="center",va="center",color="white",fontsize=14,fontweight="bold")
ax.set_ylim(0,0.4); ax.set_ylabel("Relative frequency of a late day"); ax.set_xlabel("Delivery van")
save(fig,"SP_Fig_CH01_04.png")

# ---------- Fig 1.5 ----------
fig,ax=plt.subplots(figsize=(10,4)); ax.axis("off"); ax.set_xlim(0,10); ax.set_ylim(0,4)
ax.add_patch(Rectangle((0.5,2.7),3.0,0.8,fc="#D9E2F1",ec=NAVY,lw=2)); ax.text(2.0,3.1,"P(F) = 0.30",ha="center",va="center",color=NAVY,fontsize=14)
ax.add_patch(Rectangle((2.5,1.6),2.5,0.8,fc="#F3E7B8",ec=GOLD,lw=2)); ax.text(3.75,2.0,"P(E) = 0.25",ha="center",va="center",color=NAVY,fontsize=14)
ax.add_patch(Rectangle((2.5,0.4),1.0,0.8,fc=GOLD,ec=NAVY,lw=2)); ax.text(3.0,0.8,"0.10",ha="center",va="center",color="white",fontsize=14,fontweight="bold")
ax.text(3.8,0.8,"P(F ∩ E): counted twice → subtract once",va="center",color=BURG,fontsize=13)
ax.text(5.6,3.1,"P(F ∪ E) = 0.30 + 0.25 − 0.10 = 0.45",fontsize=15,color=NAVY,fontweight="bold",va="center")
for yy in (2.7,3.5): ax.plot([0.5,0.5],[0.3,yy],color=SLATE,lw=0.8,ls=":")
save(fig,"SP_Fig_CH01_05.png")

# ---------- Fig 1.6 ----------
fig,ax=plt.subplots(figsize=(10,5.6)); ax.axis("off"); ax.set_xlim(0,10.5); ax.set_ylim(-0.6,6.2)
ax.scatter([1],[3],s=320,color=NAVY,zorder=3); ax.text(1,3.5,"start",ha="center",color=NAVY,fontsize=13)
for y,r in zip([5,3,1],["Route A","Route B","Route C"]):
    ax.plot([1,4],[3,y],color=NAVY,lw=2); ax.scatter([4],[y],s=260,color=BLUE,zorder=3); ax.text(4,y+0.45,r,ha="center",color=NAVY,fontsize=13)
    for dy,v in zip([0.5,-0.5],["Van 1","Van 2"]):
        ax.plot([4,7],[y,y+dy],color=GOLD,lw=2); ax.scatter([7],[y+dy],s=220,color=GOLD,zorder=3); ax.text(7.35,y+dy,f"{r[-1]} – {v}",va="center",color=NAVY,fontsize=13)
ax.text(5.2,-0.3,"3 routes × 2 vans = 6 plans",ha="center",fontsize=16,color=NAVY,fontweight="bold")
save(fig,"SP_Fig_CH01_06.png")

# ---------- Fig 1.7 ----------
rng=np.random.default_rng(7); n=1000; p=0.30
x=(rng.random(n)<p).astype(int); run=np.cumsum(x)/np.arange(1,n+1)
fig,ax=plt.subplots(figsize=(11,5))
ax.plot(np.arange(1,n+1),run,color=NAVY,lw=2,label="running relative frequency")
ax.axhline(p,color=GOLD,lw=2.5,ls="--",label="true probability p = 0.30")
for k,dx,dy in [(10,1.6,0.14),(100,1.6,0.12),(1000,0.55,0.14)]:
    ax.annotate(f"n = {k}: {run[k-1]:.3f}",xy=(k,run[k-1]),xytext=(k*dx,run[k-1]+dy),arrowprops=dict(arrowstyle="->",color=SLATE),color=NAVY,fontsize=12,ha="center")
ax.set_xscale("log"); ax.set_xlabel("number of simulated days n (log scale)"); ax.set_ylabel("fraction of late days so far"); ax.set_ylim(0,0.7)
ax.legend(frameon=False,loc="upper right")
save(fig,"SP_Fig_CH01_08.png")

# ---------- Fig 1.8 ----------
ns=np.arange(2,8); pdiff=[perm(7,k)/7**k for k in ns]; pshare=[1-v for v in pdiff]
fig,ax=plt.subplots(figsize=(10,5))
ax.plot(ns,pshare,"-o",color=NAVY,lw=2.5,ms=9,label="P(at least two share a rest day)")
ax.plot(ns,pdiff,"-s",color=GOLD,lw=2.5,ms=8,label="P(all rest days different)")
for k,v in zip(ns,pshare): ax.text(k,v+0.05,f"{v:.2f}",ha="center",color=NAVY,fontsize=12)
ax.set_xlabel("number of drivers"); ax.set_ylabel("probability"); ax.set_ylim(0,1.15); ax.set_xticks(ns); ax.legend(frameon=False,loc="center right")
save(fig,"SP_Fig_CH01_07.png")

# ---------- Fig 1.9 concept map ----------
fig,ax=plt.subplots(figsize=(12,7)); ax.axis("off"); ax.set_xlim(0,12); ax.set_ylim(0,7.3); ax.set_aspect("equal")
def cbox(x,y,t,c=NAVY,fc=IVORY,w=2.9,h=1.0,tc=None):
    rbox(ax,x-w/2,y-h/2,w,h,fc,c,2.2); ax.text(x,y,t,ha="center",va="center",fontsize=11.5,color=tc or NAVY,fontweight="bold",zorder=3,linespacing=1.3)
def link(a,b,c=SLATE): ax.add_patch(FancyArrowPatch(a,b,arrowstyle="-|>",color=c,lw=1.8,mutation_scale=15,zorder=1))
cbox(6,6.5,"Random experiment",NAVY,NAVY,tc="white")
cbox(2.5,4.8,"Sample space S\n(all outcomes)"); cbox(6,4.8,"Event A ⊆ S"); cbox(9.5,4.8,"Set operations\n∪   ∩   ′")
cbox(2.5,3.0,"Classical\n|A| / |S|",BLUE); cbox(6,3.0,"Frequency\nn(A) / n",EMER); cbox(9.5,3.0,"Conditional\nP(A | B)",CORAL)
cbox(2.5,1.1,"Counting tools\n+, ×, P(n,k), C(n,k)",GOLD); cbox(6,1.1,"Rules: complement,\naddition, bounds",GOLD); cbox(9.5,1.1,"Simulation\n(Chapter 17)",GOLD)
for b in [(2.5,5.3),(6,5.3),(9.5,5.3)]: link((6,6.0),b)
for xx in (2.5,6,9.5): link((xx,4.3),(xx,3.5)); link((xx,2.5),(xx,1.6))
link((4.55,4.8),(3.95,4.8)); link((7.45,4.8),(8.05,4.8)); link((7.45,3.0),(8.05,3.0))
save(fig,"SP_Fig_CH01_11.png")

# ---------- Fig 1.10 conditional probability: two-way table as areas ----------
fig,ax=plt.subplots(figsize=(10,5.4)); ax.axis("off"); ax.set_xlim(0,10); ax.set_ylim(0,5.4); ax.set_aspect("equal")
# 200 days: rain 60 (late 24), no rain 140 (late 22)
ax.add_patch(Rectangle((0.5,0.5),3.0,4.0,fc="#D9E2F1",ec=NAVY,lw=2)); ax.add_patch(Rectangle((0.5,0.5),3.0,4.0*24/60,fc=NAVY,ec=NAVY,lw=2))
ax.add_patch(Rectangle((3.5,0.5),7.0,4.0,fc=IVORY,ec=NAVY,lw=2)); ax.add_patch(Rectangle((3.5,0.5),7.0,4.0*22/140,fc=GOLD,ec=NAVY,lw=2))
ax.text(2.0,4.75,"Rainy days: 60",ha="center",color=NAVY,fontsize=13,fontweight="bold"); ax.text(7.0,4.75,"Dry days: 140",ha="center",color=NAVY,fontsize=13,fontweight="bold")
ax.text(2.0,0.5+4.0*24/60/2,"late: 24",ha="center",va="center",color="white",fontsize=13,fontweight="bold"); ax.text(2.0,3.2,"on time: 36",ha="center",color=NAVY,fontsize=13)
ax.text(7.0,0.5+4.0*22/140/2,"late: 22",ha="center",va="center",color=NAVY,fontsize=13,fontweight="bold"); ax.text(7.0,2.9,"on time: 118",ha="center",color=NAVY,fontsize=13)
ax.text(2.0,0.1,"P(late | rain) = 24/60 = 0.40",ha="center",color=NAVY,fontsize=13,fontweight="bold"); ax.text(7.0,0.1,"P(late | dry) = 22/140 ≈ 0.16",ha="center",color=NAVY,fontsize=13,fontweight="bold")
save(fig,"SP_Fig_CH01_09.png")

# ---------- Fig 1.11 tree for conditional probability ----------
fig,ax=plt.subplots(figsize=(11,5.6)); ax.axis("off"); ax.set_xlim(0,11); ax.set_ylim(0,6)
ax.scatter([0.8],[3],s=300,color=NAVY,zorder=3)
br=[(4.6,"Rain  0.30",NAVY),(1.4,"Dry  0.70",GOLD)]
for y,t,c in br:
    ax.plot([0.8,4],[3,y],color=c,lw=2.5); ax.scatter([4],[y],s=260,color=c,zorder=3); ax.text(2.3,(3+y)/2+0.25,t,ha="center",color=NAVY,fontsize=13,fontweight="bold")
leaves=[(4.6,5.4,"Late | Rain  0.40","Rain ∩ Late  = 0.30 × 0.40 = 0.12"),(4.6,3.8,"On time | Rain  0.60","Rain ∩ On time = 0.30 × 0.60 = 0.18"),
        (1.4,2.2,"Late | Dry  0.16","Dry ∩ Late  = 0.70 × 0.16 = 0.11"),(1.4,0.6,"On time | Dry  0.84","Dry ∩ On time = 0.70 × 0.84 = 0.59")]
for y0,y1,t,r in leaves:
    ax.plot([4,7],[y0,y1],color=SLATE,lw=2); ax.scatter([7],[y1],s=200,color=EMER if "Late |" in t else SLATE,zorder=3)
    ax.text(5.5,(y0+y1)/2+0.22,t,ha="center",color=NAVY,fontsize=12,bbox=dict(boxstyle="round,pad=0.15",fc="white",ec="none")); ax.text(7.3,y1,r,va="center",color=NAVY,fontsize=12.5)
ax.text(5.5,-0.0,"each leaf = product of its branches   (adding leaves: Chapter 2)",ha="center",color=NAVY,fontsize=13,fontweight="bold")
save(fig,"SP_Fig_CH01_10.png")
print("figures done")
