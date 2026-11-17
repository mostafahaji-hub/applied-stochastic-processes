"""SP_CH02 — Level 2 figures (clean layout, book palette) and number checks."""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, FancyArrowPatch, Circle
NAVY, GOLD, EMER, BURG, BLUE, CORAL, IVORY, SLATE = "#0B2545","#C9A227","#1B7F5C","#7A1E2B","#2E86AB","#E07A5F","#FBF8F1","#5B6B7C"
plt.rcParams.update({"font.size":14,"axes.titlesize":15,"axes.labelsize":14,"font.family":"DejaVu Sans","axes.edgecolor":SLATE,"axes.spines.top":False,"axes.spines.right":False,"axes.titlepad":10})
OUT="/home/claude/ch02/fig/"
def save(fig,name): fig.savefig(OUT+name,dpi=300,bbox_inches="tight",facecolor="white",pad_inches=0.15); plt.close(fig)
def rbox(ax,x,y,w,h,fc,ec,lw=2.5): ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0,rounding_size=0.12",fc=fc,ec=ec,lw=lw,zorder=2))

# Fig 2.1 prior -> posterior for four Nava situations
fig,ax=plt.subplots(figsize=(11,5.2))
cases=["Van 7 late\n(news: rain)","Defective parcel\n(news: scanner flag)","Customer leaves\n(news: Silver tier)","Fraudulent order\n(news: alarm)"]
prior=[0.23,0.03,0.146,0.005]; post=[0.40,0.269,0.20,0.184]
x=np.arange(4); w=0.36
b1=ax.bar(x-w/2,prior,w,color=SLATE,label="before the news (prior)"); b2=ax.bar(x+w/2,post,w,color=GOLD,label="after the news (posterior)")
for b,v in zip(list(b1)+list(b2),prior+post): ax.text(b.get_x()+b.get_width()/2,v+0.012,f"{v:.3f}",ha="center",fontsize=12,color=NAVY)
ax.set_xticks(x); ax.set_xticklabels(cases,fontsize=12); ax.set_ylabel("probability"); ax.set_ylim(0,0.5); ax.legend(frameon=False)
save(fig,"SP_Fig_CH02_01.png")

# Fig 2.2 churn by tier as 10x10 grids (per 100 customers of each tier)
fig,axs=plt.subplots(1,3,figsize=(14,5),gridspec_kw={"wspace":0.3})
data=[("Silver (550 customers)",20,NAVY),("Gold (300 customers)",10,GOLD),("Platinum (150 customers)",4,EMER)]
for ax,(t,ch,c) in zip(axs,data):
    ax.set_xlim(0,10); ax.set_ylim(0,10); ax.set_aspect("equal"); ax.axis("off")
    k=0
    for r in range(10):
        for col in range(10):
            ax.add_patch(Rectangle((col,9-r),0.92,0.92,fc=(BURG if k<ch else IVORY),ec=c,lw=1.2)); k+=1
    ax.set_title(f"{t}\nchurn rate = {ch}/100 = {ch/100:.2f}",color=NAVY,fontsize=13)
for xpos in (0.36,0.655): fig.add_artist(plt.Line2D([xpos,xpos],[0.05,0.92],color=SLATE,lw=1.2,ls=":"))
save(fig,"SP_Fig_CH02_02.png")

# Fig 2.3 chain tree: three parcels without replacement (12 parcels, 4 damaged)
fig,ax=plt.subplots(figsize=(12,5.6)); ax.axis("off"); ax.set_xlim(0,12); ax.set_ylim(0,6.4)
bb=dict(boxstyle="round,pad=0.25",fc="white",ec="none")
ax.scatter([0.7],[3],s=300,color=NAVY,zorder=3)
ax.plot([0.7,3.6],[3,4.6],color=EMER,lw=3,zorder=1); ax.plot([0.7,3.6],[3,1.4],color=SLATE,lw=2,zorder=1)
ax.text(2.15,4.15,"good  8/12",color=EMER,fontsize=13,fontweight="bold",ha="center",bbox=bb,zorder=4); ax.text(2.15,1.85,"damaged  4/12",color=SLATE,fontsize=12,ha="center",bbox=bb,zorder=4)
ax.scatter([3.6,3.6],[4.6,1.4],s=240,color=[EMER,SLATE],zorder=3)
ax.plot([3.6,6.8],[4.6,5.5],color=EMER,lw=3,zorder=1); ax.plot([3.6,6.8],[4.6,3.7],color=SLATE,lw=2,zorder=1)
ax.text(5.2,5.35,"good | good  7/11",color=EMER,fontsize=12.5,fontweight="bold",ha="center",bbox=bb,zorder=4); ax.text(5.2,3.85,"damaged | good  4/11",color=SLATE,fontsize=11.5,ha="center",bbox=bb,zorder=4)
ax.scatter([6.8,6.8],[5.5,3.7],s=200,color=[EMER,SLATE],zorder=3)
ax.plot([6.8,10.0],[5.5,6.0],color=EMER,lw=3,zorder=1); ax.plot([6.8,10.0],[5.5,5.0],color=SLATE,lw=2,zorder=1)
ax.text(8.4,6.05,"good | 2 good  6/10",color=EMER,fontsize=12.5,fontweight="bold",ha="center",bbox=bb,zorder=4); ax.text(8.4,4.95,"damaged | 2 good  4/10",color=SLATE,fontsize=11.5,ha="center",bbox=bb,zorder=4)
ax.scatter([10.0,10.0],[6.0,5.0],s=180,color=[EMER,SLATE],zorder=3)
ax.text(10.3,6.0,"all good",color=EMER,fontsize=12,va="center",fontweight="bold")
ax.text(6,0.45,"P(all three good) = 8/12 × 7/11 × 6/10 = 336/1,320 ≈ 0.255",ha="center",color=NAVY,fontsize=14,fontweight="bold")
ax.text(3.6,0.95,"(other branches continue the same way)",ha="center",color=SLATE,fontsize=11,style="italic")
save(fig,"SP_Fig_CH02_03.png")

# Fig 2.4 total probability with three suppliers
fig,ax=plt.subplots(figsize=(11,5.8)); ax.axis("off"); ax.set_xlim(0,11); ax.set_ylim(0,6.2)
ax.scatter([0.7],[3.1],s=300,color=NAVY,zorder=3)
sup=[(5.1,"Supplier A  0.50",0.50,0.02,NAVY),(3.1,"Supplier B  0.30",0.30,0.04,GOLD),(1.1,"Supplier C  0.20",0.20,0.08,BURG)]
for y,t,ps,pd,c in sup:
    ax.plot([0.7,3.6],[3.1,y],color=c,lw=2.5); ax.scatter([3.6],[y],s=240,color=c,zorder=3); ax.text(2.15,(3.1+y)/2+(0.3 if y==3.1 else 0.05),t,color=NAVY,fontsize=12,fontweight="bold",ha="center",bbox=dict(boxstyle="round,pad=0.2",fc="white",ec="none"),zorder=4)
    ax.plot([3.6,6.6],[y,y+0.45],color=BURG,lw=2); ax.plot([3.6,6.6],[y,y-0.45],color=SLATE,lw=1.5)
    ax.text(5.0,y+0.62,f"defective | {t[9]}  {pd:.2f}",color=BURG,fontsize=11,ha="center"); ax.text(5.0,y-0.75,f"good | {t[9]}  {1-pd:.2f}",color=SLATE,fontsize=11,ha="center")
    ax.scatter([6.6],[y+0.45],s=170,color=BURG,zorder=3); ax.scatter([6.6],[y-0.45],s=150,color=SLATE,zorder=3)
    ax.text(6.9,y+0.45,f"{t[9]} ∩ defective = {ps:.2f} × {pd:.2f} = {ps*pd:.3f}",va="center",color=NAVY,fontsize=12)
ax.text(5.5,-0.05,"P(defective) = 0.010 + 0.012 + 0.016 = 0.038",ha="center",color=BURG,fontsize=14,fontweight="bold")
save(fig,"SP_Fig_CH02_04.png")

# Fig 2.5 natural frequencies for Bayes: 10,000 parcels
fig,ax=plt.subplots(figsize=(11,6)); ax.axis("off"); ax.set_xlim(0,11); ax.set_ylim(0,6.4)
def nb(x,y,t,fc,ec,w=2.6,h=1.0,tc=NAVY): rbox(ax,x-w/2,y-h/2,w,h,fc,ec); ax.text(x,y,t,ha="center",va="center",fontsize=12.5,color=tc,fontweight="bold",zorder=3,linespacing=1.3)
nb(5.5,5.7,"10,000 parcels",NAVY,NAVY,tc="white")
nb(2.8,3.9,"300 defective\n(3%)",'#F3E0E0',BURG); nb(8.2,3.9,"9,700 good\n(97%)",IVORY,EMER)
nb(1.5,1.9,"285 flagged\n(95% of 300)",BURG,BURG,tc="white",w=2.4); nb(4.1,1.9,"15 missed",IVORY,SLATE,w=2.0)
nb(6.9,1.9,"776 flagged\n(8% of 9,700)",GOLD,GOLD,w=2.6); nb(9.6,1.9,"8,924 passed",IVORY,SLATE,w=2.4)
for a,b in [((5.5,5.2),(2.8,4.4)),((5.5,5.2),(8.2,4.4)),((2.8,3.4),(1.5,2.4)),((2.8,3.4),(4.1,2.4)),((8.2,3.4),(6.9,2.4)),((8.2,3.4),(9.6,2.4))]:
    ax.add_patch(FancyArrowPatch(a,b,arrowstyle="-|>",color=SLATE,lw=1.8,mutation_scale=15,zorder=1))
ax.add_patch(Rectangle((0.2,1.25),8.1,1.3,fc="none",ec=GOLD,lw=2,ls="--"))
ax.text(5.5,0.45,"P(defective | flagged) = 285 / (285 + 776) = 285 / 1,061 ≈ 0.27",ha="center",color=NAVY,fontsize=15,fontweight="bold")
save(fig,"SP_Fig_CH02_05.png")

# Fig 2.6 posterior vs base rate
fig,ax=plt.subplots(figsize=(10,5))
base=np.linspace(0.001,0.5,500)
for fp,c,lab in [(0.08,NAVY,"false-alarm rate 8%"),(0.02,GOLD,"false-alarm rate 2%"),(0.005,EMER,"false-alarm rate 0.5%")]:
    post=0.95*base/(0.95*base+fp*(1-base)); ax.plot(base*100,post,color=c,lw=2.5,label=lab)
ax.axvline(3,color=SLATE,ls=":",lw=1.5); ax.text(3.3,0.05,"Nava: 3% defective",color=SLATE,fontsize=11)
ax.set_xlabel("base rate of defective parcels (%)"); ax.set_ylabel("P(defective | flagged)"); ax.set_ylim(0,1.02); ax.legend(frameon=False,loc="lower right",title="sensitivity fixed at 95%")
save(fig,"SP_Fig_CH02_06.png")

# Fig 2.7 independence check bars
fig,axs=plt.subplots(1,2,figsize=(12,4.8),gridspec_kw={"wspace":0.35})
for ax,(t,vals,c) in zip(axs,[("Machine stop vs. weather",[0.14,0.14,0.14],EMER),("Van 7 late vs. weather",[0.23,0.40,0.157],BURG)]):
    bars=ax.bar(["overall","given rain","given dry"],vals,color=[SLATE,c,c],width=0.55)
    for b,v in zip(bars,vals): ax.text(b.get_x()+b.get_width()/2,v+0.01,f"{v:.3f}",ha="center",color=NAVY,fontsize=12,fontweight="bold")
    ax.set_ylim(0,0.5); ax.set_title(t,color=NAVY); ax.set_ylabel("probability")
axs[0].text(1,0.42,"same bars → independent",ha="center",color=EMER,fontsize=12,fontweight="bold"); axs[1].text(1,0.46,"different bars → dependent",ha="center",color=BURG,fontsize=12,fontweight="bold")
fig.add_artist(plt.Line2D([0.5,0.5],[0.05,0.95],color=SLATE,lw=1.2,ls=":"))
save(fig,"SP_Fig_CH02_08.png")

# Fig 2.8 at least one failure vs n
fig,ax=plt.subplots(figsize=(10,5)); n=np.arange(1,31)
for p,c in [(0.02,EMER),(0.05,GOLD),(0.10,BURG)]:
    ax.plot(n,1-(1-p)**n,"-o",color=c,lw=2.2,ms=5,label=f"p = {p:.2f} per component")
ax.axhline(0.5,color=SLATE,ls=":",lw=1.2); ax.set_xlabel("number of independent components n"); ax.set_ylabel("P(at least one fails) = 1 − (1 − p)ⁿ"); ax.set_ylim(0,1.02); ax.legend(frameon=False)
save(fig,"SP_Fig_CH02_09.png")

# Fig 2.9 series / parallel / mixed diagrams
fig,axs=plt.subplots(1,3,figsize=(17,3.4),gridspec_kw={"wspace":0.08})
def comp(ax,x,y,t,c=NAVY,w=1.6,h=0.72): rbox(ax,x-w/2,y-h/2,w,h,IVORY,c); ax.text(x,y,t,ha="center",va="center",fontsize=11.5,color=NAVY,fontweight="bold",zorder=3)
ax=axs[0]; ax.set_xlim(0,8); ax.set_ylim(0,3); ax.axis("off"); ax.set_aspect("equal")
ax.plot([0.2,7.8],[1.5,1.5],color=NAVY,lw=2,zorder=1)
for i,t in enumerate(["M1 0.95","M2 0.95","M3 0.95","M4 0.95"]): comp(ax,1.2+i*1.85,1.5,t,w=1.5)
ax.set_title("(a) Series",color=NAVY)
ax=axs[1]; ax.set_xlim(0,8); ax.set_ylim(0,3); ax.axis("off"); ax.set_aspect("equal")
for y in (0.5,1.5,2.5): ax.plot([1.2,6.8],[y,y],color=NAVY,lw=2,zorder=1)
ax.plot([1.2,1.2],[0.5,2.5],color=NAVY,lw=2); ax.plot([6.8,6.8],[0.5,2.5],color=NAVY,lw=2); ax.plot([0.2,1.2],[1.5,1.5],color=NAVY,lw=2); ax.plot([6.8,7.8],[1.5,1.5],color=NAVY,lw=2)
for y,t in zip((0.5,1.5,2.5),["S3 0.90","S2 0.90","S1 0.90"]): comp(ax,4,y,t,GOLD,w=1.6)
ax.set_title("(b) Parallel",color=NAVY)
ax=axs[2]; ax.set_xlim(0,8); ax.set_ylim(0,3); ax.axis("off"); ax.set_aspect("equal")
ax.plot([0.2,0.9],[1.5,1.5],color=NAVY,lw=2); ax.plot([0.9,0.9],[0.6,2.4],color=NAVY,lw=2); ax.plot([0.9,5.0],[2.4,2.4],color=NAVY,lw=2); ax.plot([0.9,5.0],[0.6,0.6],color=NAVY,lw=2); ax.plot([5.0,5.0],[0.6,2.4],color=NAVY,lw=2); ax.plot([5.0,7.8],[1.5,1.5],color=NAVY,lw=2)
comp(ax,1.9,2.4,"A 0.90",w=1.4); comp(ax,3.9,2.4,"B 0.90",w=1.4); comp(ax,2.95,0.6,"C 0.85",GOLD,w=1.4); comp(ax,6.4,1.5,"D 0.98",EMER,w=1.4)
ax.set_title("(c) Mixed",color=NAVY)
for xpos in (0.365,0.64): fig.add_artist(plt.Line2D([xpos,xpos],[0.05,0.95],color=SLATE,lw=1.2,ls=":"))
save(fig,"SP_Fig_CH02_10.png")

# Fig 2.10 Simpson-style: teams X and Y
fig,ax=plt.subplots(figsize=(10,5))
cats=["Small orders","Large orders","All orders"]; X=[0.90,0.50,0.82]; Y=[0.95,0.60,0.67]
x=np.arange(3); w=0.36
b1=ax.bar(x-w/2,X,w,color=NAVY,label="Team X"); b2=ax.bar(x+w/2,Y,w,color=GOLD,label="Team Y")
for b,v in zip(list(b1)+list(b2),X+Y): ax.text(b.get_x()+b.get_width()/2,v+0.015,f"{v:.0%}",ha="center",fontsize=12,color=NAVY,fontweight="bold")
ax.set_xticks(x); ax.set_xticklabels(cats); ax.set_ylabel("on-time rate"); ax.set_ylim(0,1.1); ax.legend(frameon=False)
ax.text(2,1.0,"Y wins both categories,\nX wins overall",ha="center",color=BURG,fontsize=12,fontweight="bold")
save(fig,"SP_Fig_CH02_11.png")

# Fig 2.11 Monte Carlo check of Bayes
rng=np.random.default_rng(22); N=100000
defect=rng.random(N)<0.03; flag=np.where(defect,rng.random(N)<0.95,rng.random(N)<0.08)
idx=np.flatnonzero(flag); run=np.cumsum(defect[idx])/np.arange(1,len(idx)+1)
fig,ax=plt.subplots(figsize=(10,4.8))
ax.plot(np.arange(1,len(idx)+1),run,color=NAVY,lw=1.8,label="running fraction of defective among flagged")
ax.axhline(285/1061,color=GOLD,lw=2.5,ls="--",label="Bayes: 0.269"); ax.set_xscale("log"); ax.set_ylim(0,0.6)
ax.set_xlabel("number of flagged parcels seen so far (log scale)"); ax.set_ylabel("fraction defective"); ax.legend(frameon=False)
save(fig,"SP_Fig_CH02_07.png")
print("MC: flagged",len(idx),"posterior est",run[-1])

# Fig 2.12 concept map
fig,ax=plt.subplots(figsize=(12,7)); ax.axis("off"); ax.set_xlim(0,12); ax.set_ylim(0,7.3); ax.set_aspect("equal")
def cbox(x,y,t,c=NAVY,fc=IVORY,w=2.9,h=1.0,tc=None): rbox(ax,x-w/2,y-h/2,w,h,fc,c,2.2); ax.text(x,y,t,ha="center",va="center",fontsize=11.5,color=tc or NAVY,fontweight="bold",zorder=3,linespacing=1.3)
def link(a,b,c=SLATE): ax.add_patch(FancyArrowPatch(a,b,arrowstyle="-|>",color=c,lw=1.8,mutation_scale=15,zorder=1))
cbox(6,6.5,"Conditional probability\nP(A|B) = P(A∩B)/P(B)",NAVY,NAVY,tc="white",w=4.2)
cbox(2.5,4.8,"Multiplication rule\nP(A∩B) = P(B)P(A|B)"); cbox(6,4.8,"Total probability\nΣ P(Bᵢ)P(A|Bᵢ)"); cbox(9.5,4.8,"Independence\nP(A|B) = P(A)")
cbox(2.5,3.0,"Chains without\nreplacement",BLUE); cbox(6,3.0,"Bayes’ rule\nP(B|A) = P(B)P(A|B)/P(A)",CORAL,w=3.4); cbox(9.5,3.0,"Reliability:\nseries & parallel",EMER)
cbox(2.5,1.1,"Trees & tables",GOLD); cbox(6,1.1,"Natural frequencies\n& odds form",GOLD); cbox(9.5,1.1,"Pitfalls: base rate,\nSimpson, mixed-up conditions",GOLD,w=3.4)
for b in [(2.5,5.3),(6,5.3),(9.5,5.3)]: link((6,6.0),b)
for xx in (2.5,6,9.5): link((xx,4.3),(xx,3.5)); link((xx,2.5),(xx,1.6))
link((4.0,4.8),(4.5,4.8)); link((7.5,4.8),(8.05,4.8))
save(fig,"SP_Fig_CH02_12.png")

# ---------- number checks ----------
print("churn:",110/550,30/300,6/150,146/1000,110/146)
print("call long:",0.4*0.1+0.35*0.2+0.25*0.3, 0.075/0.185)
print("three good:",8/12*7/11*6/10)
print("hiring:",0.6*0.5*0.8)
print("suppliers:",0.5*0.02+0.3*0.04+0.2*0.08, 0.016/0.038, 0.010/0.038, 0.012/0.038)
print("scanner:",0.03*0.95+0.97*0.08, 0.0285/(0.0285+0.0776))
print("fraud:",0.005*0.9/(0.005*0.9+0.995*0.02))
o=0.03/0.97*(0.95/0.08); print("odds after 1:",o,o/(1+o)," after 2:",o*11.875/(1+o*11.875))
print("two vans:",0.23**2,1-0.77**2,2*0.23*0.77)
print("n comps:",[(n,round(1-0.95**n,4)) for n in (4,10,20)])
print("series:",0.95**4,"parallel:",1-0.1**3,"mixed:",(1-(1-0.81)*0.15)*0.98)
print("spares:",[(n,round(1-0.2**n,4)) for n in (1,2,3)])
print("simpson:",72/80,10/20,82/100,19/20,48/80,67/100)
