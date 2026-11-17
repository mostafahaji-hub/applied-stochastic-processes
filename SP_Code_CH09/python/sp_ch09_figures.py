"""SP_CH09 — Chapter 9 figures (Markov chains, first steps) and number checks."""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
NAVY, GOLD, EMER, BURG, BLUE, CORAL, IVORY, SLATE = "#0B2545","#C9A227","#1B7F5C","#7A1E2B","#2E86AB","#E07A5F","#FBF8F1","#5B6B7C"
plt.rcParams.update({"font.size":14,"axes.titlesize":15,"axes.labelsize":14,"font.family":"DejaVu Sans","axes.edgecolor":SLATE,"axes.spines.top":False,"axes.spines.right":False,"axes.titlepad":10})
OUT="/home/claude/ch09/fig/"
def save(fig,name): fig.savefig(OUT+name,dpi=300,bbox_inches="tight",facecolor="white",pad_inches=0.15); plt.close(fig)
def rbox(ax,x,y,w,h,fc,ec,lw=2.5): ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0,rounding_size=0.12",fc=fc,ec=ec,lw=lw,zorder=2))
sep=lambda fig,xs: [fig.add_artist(plt.Line2D([x,x],[0.05,0.95],color=SLATE,lw=1.2,ls=":")) for x in xs]
P3=np.array([[.70,.10,0,.20],[.05,.75,.10,.10],[0,.06,.90,.04],[0,0,0,1]]); P2=np.array([[.86,.10,.04],[.70,.20,.10],[.50,0,.50]]); W=np.array([[.6,.4],[.17,.83]])
# Part III opener
fig,ax=plt.subplots(figsize=(14,5)); ax.axis("off"); ax.set_xlim(0,14); ax.set_ylim(0,5)
parts=[("I","Probability\nfrom Zero","1–5",SLATE),("II","Arrivals\nand Waiting","6–8",SLATE),("III","The Markov\nWorld","9–12",GOLD),("IV","Continuous\nStates","13",SLATE),("V","Inside\nMetaheuristics","14–16",SLATE),("VI","Monte Carlo\nSimulation","17–19",SLATE)]
for i,(n,t,chs,c) in enumerate(parts):
    x=0.4+i*2.3; rbox(ax,x,1.4,2.0,2.4,IVORY if c==SLATE else "#F7F0DC",c,3 if c==GOLD else 1.8); ax.text(x+1,3.3,f"PART {n}",ha="center",fontsize=13,color=c if c==GOLD else NAVY,fontweight="bold",zorder=3); ax.text(x+1,2.45,t,ha="center",va="center",fontsize=12,color=NAVY,zorder=3); ax.text(x+1,1.65,f"Ch {chs}",ha="center",fontsize=11,color=SLATE,zorder=3)
    if i<5: ax.add_patch(FancyArrowPatch((x+2.05,2.6),(x+2.25,2.6),arrowstyle="-|>",color=SLATE,lw=1.5,mutation_scale=14))
ax.text(7,4.6,"You are here: the present is enough",ha="center",fontsize=14,color=GOLD,fontweight="bold")
ax.text(7,0.6,"Part III studies systems whose future depends on the past only through the present: machines, customers, inventories, repairs.",ha="center",fontsize=11.5,color=SLATE)
save(fig,"SP_Fig_CH09_00_PartIII.png")
# 9.1 R2 transition graph
fig,ax=plt.subplots(figsize=(10,4.6)); ax.axis("off"); ax.set_xlim(0,10); ax.set_ylim(0,4.6)
pos={"W":(1.8,2.3),"S":(5,2.3),"M":(8.2,2.3)}; col={"W":EMER,"S":GOLD,"M":BURG}; names={"W":"Working","S":"Stopped","M":"Maintenance"}
for k,(x,y) in pos.items(): ax.add_patch(Circle((x,y),0.75,fc=col[k],ec=col[k],zorder=3)); ax.text(x,y,k,ha="center",va="center",color="white",fontsize=16,fontweight="bold",zorder=4); ax.text(x,y-1.1,names[k],ha="center",fontsize=11,color=col[k])
def arrow(a,b,t,rad,off): (x1,y1),(x2,y2)=pos[a],pos[b]; ax.annotate("",xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle="-|>",color=NAVY,lw=1.8,shrinkA=40,shrinkB=40,connectionstyle=f"arc3,rad={rad}"),zorder=2); ax.text((x1+x2)/2+off[0],(y1+y2)/2+off[1],t,ha="center",fontsize=12,color=NAVY,bbox=dict(boxstyle="round,pad=0.15",fc="white",ec="none"),zorder=5)
arrow("W","S","0.10",-0.3,(0,0.8)); arrow("S","W","0.70",-0.3,(0,-0.8)); arrow("S","M","0.10",-0.3,(0,0.8)); arrow("M","W","0.50",-0.5,(0,-1.6)); arrow("W","M","0.04",-0.45,(0,1.5))
for k,s in [("W","stay 0.86"),("S","stay 0.20"),("M","stay 0.50")]: x,y=pos[k]; ax.text(x,y+1.0,s,ha="center",fontsize=11.5,color=col[k],fontweight="bold")
save(fig,"SP_Fig_CH09_01.png")
# 9.2 matrix multiplication picture (two-step from W to M)
fig,ax=plt.subplots(figsize=(11,4.2)); ax.axis("off"); ax.set_xlim(0,11); ax.set_ylim(0,4.2)
ax.add_patch(Circle((1,2.1),0.45,fc=EMER,ec=EMER)); ax.text(1,2.1,"W",ha="center",va="center",color="white",fontsize=14,fontweight="bold")
mids=[("W",3.4,EMER,"0.86","0.04"),("S",2.1,GOLD,"0.10","0.10"),("M",0.8,BURG,"0.04","0.50")]
for k,y,c,p1,p2 in mids:
    ax.add_patch(Circle((5,y),0.45,fc=c,ec=c)); ax.text(5,y,k,ha="center",va="center",color="white",fontsize=14,fontweight="bold")
    ax.annotate("",xy=(4.5,y),xytext=(1.45,2.1),arrowprops=dict(arrowstyle="-|>",color=SLATE,lw=1.8)); ax.text(3,(2.1+y)/2+0.2,p1,fontsize=12,color=NAVY,ha="center",bbox=dict(boxstyle="round,pad=0.1",fc="white",ec="none"))
    ax.annotate("",xy=(8.55,2.1),xytext=(5.45,y),arrowprops=dict(arrowstyle="-|>",color=SLATE,lw=1.8)); ax.text(7,(2.1+y)/2+0.2,p2,fontsize=12,color=NAVY,ha="center",bbox=dict(boxstyle="round,pad=0.1",fc="white",ec="none"))
ax.add_patch(Circle((9,2.1),0.45,fc=BURG,ec=BURG)); ax.text(9,2.1,"M",ha="center",va="center",color="white",fontsize=14,fontweight="bold")
ax.text(5.5,-0.0,"P²(W→M) = 0.86×0.04 + 0.10×0.10 + 0.04×0.50 = 0.0644   (row W of P  ·  column M of P)",ha="center",fontsize=13,color=NAVY,fontweight="bold")
save(fig,"SP_Fig_CH09_02.png")
# 9.3 weather chain rows converge
fig,ax=plt.subplots(figsize=(10,4.6)); ns=np.arange(0,16); r1=[np.linalg.matrix_power(W,n)[0,0] for n in ns]; r2=[np.linalg.matrix_power(W,n)[1,0] for n in ns]
ax.plot(ns,r1,"-o",color=NAVY,lw=2.5,ms=6,label="P(rain on day n | rain today)"); ax.plot(ns,r2,"-s",color=GOLD,lw=2.5,ms=6,label="P(rain on day n | dry today)"); ax.axhline(0.17/0.57,color=BURG,ls="--",lw=2,label="long-run 0.298")
ax.set_xlabel("days ahead n"); ax.set_ylabel("probability of rain"); ax.set_ylim(0,1.05); ax.legend(frameon=False)
save(fig,"SP_Fig_CH09_03.png")
# 9.4 distribution of X_n for a Silver customer
fig,ax=plt.subplots(figsize=(11,4.8)); ns=np.arange(0,37); D=np.array([np.linalg.matrix_power(P3,n)[0] for n in ns])
ax.stackplot(ns,D[:,0],D[:,1],D[:,2],D[:,3],labels=["Silver","Gold","Platinum","Churned"],colors=[SLATE,GOLD,EMER,BURG],alpha=0.9)
ax.set_xlabel("months after joining as Silver"); ax.set_ylabel("probability"); ax.set_ylim(0,1); ax.set_xlim(0,36); ax.legend(frameon=False,loc="center right")
save(fig,"SP_Fig_CH09_04.png")
# 9.5 first-step equations picture
fig,ax=plt.subplots(figsize=(11,4.2)); ax.axis("off"); ax.set_xlim(0,11); ax.set_ylim(0,4.2)
ax.add_patch(Circle((1.2,2.1),0.55,fc=SLATE,ec=SLATE)); ax.text(1.2,2.1,"S",ha="center",va="center",color="white",fontsize=16,fontweight="bold"); ax.text(1.2,1.2,"m_S = ?",ha="center",fontsize=12,color=NAVY)
targets=[("S",3.5,SLATE,"0.70","1 + m_S"),("G",2.1,GOLD,"0.10","1 + m_G"),("C",0.7,BURG,"0.20","1 + 0")]
for k,y,c,p,v in targets:
    ax.add_patch(Circle((5.5,y),0.5,fc=c,ec=c)); ax.text(5.5,y,k,ha="center",va="center",color="white",fontsize=14,fontweight="bold"); ax.annotate("",xy=(4.95,y),xytext=(1.8,2.1),arrowprops=dict(arrowstyle="-|>",color=NAVY,lw=1.8)); ax.text(3.3,(2.1+y)/2+0.22,p,fontsize=12,color=NAVY,ha="center",bbox=dict(boxstyle="round,pad=0.1",fc="white",ec="none")); ax.text(6.3,y,"→ remaining months: "+v,va="center",fontsize=12,color=NAVY)
ax.text(5.5,-0.05,"m_S = 1 + 0.70·m_S + 0.10·m_G + 0.20·0      (one month passes, then start again from where you land)",ha="center",fontsize=12.5,color=EMER,fontweight="bold")
save(fig,"SP_Fig_CH09_05.png")
# 9.6 cash runway: P(reach 10 before 0)
fig,ax=plt.subplots(figsize=(10,4.6)); i=np.arange(0,11)
for p,c,lab in [(0.5,SLATE,"fair steps p = 0.5"),(0.55,NAVY,"p = 0.55 (Nava)"),(0.45,BURG,"p = 0.45")]:
    r=(1-p)/p; h=i/10 if p==0.5 else (1-r**i)/(1-r**10); ax.plot(i,h,"-o",color=c,lw=2.5,ms=6,label=lab)
ax.set_xlabel("starting cash (thousand €), targets 0 (credit limit) and 10"); ax.set_ylabel("P(reach 10 before 0)"); ax.set_ylim(0,1.05); ax.legend(frameon=False)
save(fig,"SP_Fig_CH09_06.png")
# 9.7 branching tree
rng=np.random.default_rng(9); fig,ax=plt.subplots(figsize=(11,4.6)); ax.axis("off"); ax.set_xlim(0,11); ax.set_ylim(-0.5,4.2)
gen=[[(5.5,3.8)]]; ax.scatter([5.5],[3.8],s=200,color=NAVY,zorder=3)
pts=[(5.5,3.8)]; 
for g in range(1,4):
    new=[]
    for (x,y) in pts:
        k=rng.choice([0,1,2],p=[0.2,0.5,0.3]); 
        for j in range(k): new.append((x+(j-(k-1)/2)*1.6/g**1.2+rng.normal(0,0.1),y-1.1))
        for nx,ny in new[-k:] if k else []: ax.plot([x,nx],[y,ny],color=SLATE,lw=1.5,zorder=1)
    pts=new; 
    if pts: ax.scatter([p[0] for p in pts],[p[1] for p in pts],s=160,color=[NAVY,GOLD,EMER][g%3],zorder=3)
for g in range(4): ax.text(0.3,3.8-1.1*g,f"generation {g}",fontsize=11,color=SLATE)
ax.set_title("A referral tree (branching process)",color=NAVY,fontsize=13)
save(fig,"SP_Fig_CH09_07.png")
# 9.8 slotted queue chain graph
fig,ax=plt.subplots(figsize=(12,3.0)); ax.axis("off"); ax.set_xlim(0,12); ax.set_ylim(0,3.0)
for i in range(6):
    x=1+i*2; ax.add_patch(Circle((x,1.5),0.42,fc=IVORY,ec=NAVY,lw=2.5)); ax.text(x,1.5,str(i) if i<5 else "…",ha="center",va="center",fontsize=14,color=NAVY,fontweight="bold")
    if i<5:
        ax.annotate("",xy=(x+1.55,1.85),xytext=(x+0.45,1.85),arrowprops=dict(arrowstyle="-|>",color=NAVY,lw=2,connectionstyle="arc3,rad=-0.4")); ax.text(x+1,2.6,"p(1−q)" if i>0 else "p",ha="center",fontsize=12,color=NAVY,fontweight="bold")
        if i>0: pass
        ax.annotate("",xy=(x+0.45,1.15),xytext=(x+1.55,1.15),arrowprops=dict(arrowstyle="-|>",color=BURG,lw=2,connectionstyle="arc3,rad=-0.4")); ax.text(x+1,0.3,"q(1−p)",ha="center",fontsize=12,color=BURG,fontweight="bold")
ax.set_title("A slotted (discrete-time) queue",color=NAVY,fontsize=13)
save(fig,"SP_Fig_CH09_08.png")
# 9.9 simulation R3
rng=np.random.default_rng(93); n=10000; state=np.zeros(n,int); counts=[]
for m in range(24):
    u=rng.random(n); cum=np.cumsum(P3,axis=1); state=np.array([np.searchsorted(cum[s],u[i]) for i,s in enumerate(state)]); counts.append(np.bincount(state,minlength=4)/n)
counts=np.array(counts); th=np.array([np.linalg.matrix_power(P3,m+1)[0] for m in range(24)])
fig,ax=plt.subplots(figsize=(11,4.6)); ms=np.arange(1,25)
for j,(lab,c) in enumerate([("Silver",SLATE),("Gold",GOLD),("Platinum",EMER),("Churned",BURG)]): ax.plot(ms,th[:,j],color=c,lw=2.5,label=f"{lab} (α·Pⁿ)"); ax.scatter(ms,counts[:,j],color=c,s=28,zorder=3)
ax.set_xlabel("month n"); ax.set_ylabel("fraction of 10,000 simulated Silver customers"); ax.legend(frameon=False,ncol=2,fontsize=11); ax.set_ylim(0,1)
save(fig,"SP_Fig_CH09_09.png"); print("sim month 24:",counts[-1].round(3),"theory",th[-1].round(3))
# 9.10 concept map
fig,ax=plt.subplots(figsize=(12,7)); ax.axis("off"); ax.set_xlim(0,12); ax.set_ylim(0,7.3); ax.set_aspect("equal")
def cbox(x,y,t,c=NAVY,fc=IVORY,w=2.9,h=1.0,tc=None): rbox(ax,x-w/2,y-h/2,w,h,fc,c,2.2); ax.text(x,y,t,ha="center",va="center",fontsize=11.5,color=tc or NAVY,fontweight="bold",zorder=3,linespacing=1.3)
def link(p1,p2): ax.add_patch(FancyArrowPatch(p1,p2,arrowstyle="-|>",color=SLATE,lw=1.8,mutation_scale=15,zorder=1))
cbox(6,6.5,"Markov chain: states + transition matrix P",NAVY,NAVY,tc="white",w=6.2)
cbox(2.5,4.8,"Transition graph,\nstochastic matrix"); cbox(6,4.8,"n-step: Pⁿ\nChapman–Kolmogorov"); cbox(9.5,4.8,"Distribution αPⁿ,\njoint probabilities")
cbox(2.5,3.0,"First-step analysis:\nabsorption & hitting",CORAL,w=3.2); cbox(6,3.0,"Birth–death chains,\ncash runway",BLUE); cbox(9.5,3.0,"Branching, slotted\nqueue, martingale*",EMER,w=3.2)
cbox(2.5,1.1,"R2 machine,\nR3 customers",GOLD); cbox(6,1.1,"Long run (Ch 10)",GOLD); cbox(9.5,1.1,"Simulation of\nchains (Ch 18)",GOLD)
for b in [(2.5,5.3),(6,5.3),(9.5,5.3)]: link((6,6.0),b)
for xx in (2.5,6,9.5): link((xx,4.3),(xx,3.5)); link((xx,2.5),(xx,1.6))
save(fig,"SP_Fig_CH09_10.png")
# checks
def show(l,v): print(f"{l:<62} {v}")
show("Ex 9.4 R2 P^2 row W",np.linalg.matrix_power(P2,2)[0].round(4))
show("Ex 9.5 R3 P^2 row S, P^3 row S",(np.linalg.matrix_power(P3,2)[0].round(4),np.linalg.matrix_power(P3,3)[0].round(4)))
show("Ex 9.6 weather W^2,W^5,W^10 row rain",[np.linalg.matrix_power(W,n)[0].round(4) for n in (2,5,10)])
a=np.array([.55,.30,.15,0]); show("Ex 9.7 club after 1,6,12 months from α",[(a@np.linalg.matrix_power(P3,n)).round(3) for n in (1,6,12)])
show("Ex 9.8 joint P(X1=G,X3=P | X0=S)",round(P3[0,1]*np.linalg.matrix_power(P3,2)[1,2],4))
Q=P3[:3,:3]; N=np.linalg.inv(np.eye(3)-Q); show("Ex 9.9 expected months (S,G,P)",(N@np.ones(3)).round(2))
show("Ex 9.10 P(reach Platinum) S,G",np.linalg.solve(np.array([[.3,-.1],[-.05,.25]]),np.array([0,.1])).round(4))
show("Ex 9.11 lifetime value",(N@np.array([20,45,110])).round(1))
show("Ex 9.12 R2 expected shifts to M from W,S",np.linalg.solve(np.array([[.14,-.10],[-.70,.80]]),np.ones(2)).round(2))
r=.45/.55; show("Ex 9.13 runway P(10 before 0) from 2,5,8; fair",([round((1-r**i)/(1-r**10),3) for i in (2,5,8)],0.2))
show("Ex 9.14 expected duration fair from 2 of 10: i(N-i)",16)
show("Ex 9.15 branching mean .9^n, n=1..5",[round(.9**n,3) for n in range(1,6)])
show("Ex 9.16 extinction mean 1.1",round(2/3,4))
show("Ex 9.17 slotted queue p=.3 q=.5: stationary rho",( (0.3*0.5)/(0.5*0.7) ))
show("Ex 9.18 martingale fair cash: E[X_n]=X_0",20000)
