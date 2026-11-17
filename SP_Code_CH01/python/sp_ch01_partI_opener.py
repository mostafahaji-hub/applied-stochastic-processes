"""SP_CH01 — Part I opener figure (book map with Part I highlighted)."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
NAVY, GOLD, IVORY, SLATE = "#0B2545","#C9A227","#FBF8F1","#5B6B7C"
plt.rcParams.update({"font.family":"DejaVu Sans"})
def rbox(ax,x,y,w,h,fc,ec,lw): ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0,rounding_size=0.12",fc=fc,ec=ec,lw=lw,zorder=2))
fig,ax=plt.subplots(figsize=(14,5)); ax.axis("off"); ax.set_xlim(0,14); ax.set_ylim(0,5)
parts=[("I","Probability\nfrom Zero","1–5",GOLD),("II","Arrivals\nand Waiting","6–8",SLATE),("III","The Markov\nWorld","9–12",SLATE),("IV","Continuous\nStates","13",SLATE),("V","Inside\nMetaheuristics","14–16",SLATE),("VI","Monte Carlo\nSimulation","17–19",SLATE)]
for i,(n,t,chs,c) in enumerate(parts):
    x=0.4+i*2.3; rbox(ax,x,1.4,2.0,2.4,IVORY if c==SLATE else "#F7F0DC",c,3 if c==GOLD else 1.8)
    ax.text(x+1,3.3,f"PART {n}",ha="center",fontsize=13,color=c if c==GOLD else NAVY,fontweight="bold",zorder=3); ax.text(x+1,2.45,t,ha="center",va="center",fontsize=12,color=NAVY,zorder=3); ax.text(x+1,1.65,f"Ch {chs}",ha="center",fontsize=11,color=SLATE,zorder=3)
    if i<5: ax.add_patch(FancyArrowPatch((x+2.05,2.6),(x+2.25,2.6),arrowstyle="-|>",color=SLATE,lw=1.5,mutation_scale=14))
ax.text(7,4.6,"You are here: the language of probability",ha="center",fontsize=14,color=GOLD,fontweight="bold")
ax.text(7,0.6,"Part I builds the vocabulary — events, conditioning, random variables, distributions and sums — that every later part uses.",ha="center",fontsize=11.5,color=SLATE)
fig.savefig("/home/claude/ch01/fig/SP_Fig_CH01_00_PartI.png",dpi=300,bbox_inches="tight",facecolor="white",pad_inches=0.15)
