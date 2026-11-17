"""SP_CH11 — Chapter 11 figures and number checks."""
import numpy as np, matplotlib, sys
matplotlib.use("Agg"); sys.path.insert(0,"/home/claude/ch11/code")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
from scipy.stats import weibull_min, lognorm, expon
from sp_ch11_ctmc import *
NAVY, GOLD, EMER, BURG, BLUE, CORAL, IVORY, SLATE = "#0B2545","#C9A227","#1B7F5C","#7A1E2B","#2E86AB","#E07A5F","#FBF8F1","#5B6B7C"
plt.rcParams.update({"font.size":14,"axes.titlesize":15,"axes.labelsize":14,"font.family":"DejaVu Sans","axes.edgecolor":SLATE,"axes.spines.top":False,"axes.spines.right":False,"axes.titlepad":10})
OUT="/home/claude/ch11/fig/"
def save(fig,name): fig.savefig(OUT+name,dpi=300,bbox_inches="tight",facecolor="white",pad_inches=0.15); plt.close(fig)
def rbox(ax,x,y,w,h,fc,ec,lw=2.5): ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0,rounding_size=0.12",fc=fc,ec=ec,lw=lw,zorder=2))
sep=lambda fig,xs: [fig.add_artist(plt.Line2D([x,x],[0.05,0.95],color=SLATE,lw=1.2,ls=":")) for x in xs]
# 11.1 sample path of CTMC machine 3
rng=np.random.default_rng(111); t,s=simulate_ctmc(Q3,0,40,rng)
fig,ax=plt.subplots(figsize=(11,3.8)); cols=[EMER,GOLD,BURG]
ax.step(t,s,where="post",color=SLATE,lw=1.2,alpha=0.6)
for i in range(len(t)-1): ax.hlines(s[i],t[i],t[i+1],color=cols[s[i]],lw=6)

ax.set_yticks([0,1,2]); ax.set_yticklabels(["Working","Stopped","Maintenance"]); ax.set_xlabel("time (shifts)"); ax.set_xlim(0,40); ax.set_title("A sample path: random holding times (exponential) and random jumps (jump chain)",color=NAVY,fontsize=12.5)
save(fig,"SP_Fig_CH11_02.png")
# 11.2 rate diagram 3-state
fig,ax=plt.subplots(figsize=(10,4.6)); ax.axis("off"); ax.set_xlim(0,10); ax.set_ylim(0,4.6)
pos={"W":(1.8,2.3),"S":(5,3.6),"M":(8.2,2.3)}; col={"W":EMER,"S":GOLD,"M":BURG}
for k,(x,y) in pos.items(): ax.add_patch(Circle((x,y),0.7,fc=col[k],ec=col[k],zorder=3)); ax.text(x,y,k,ha="center",va="center",color="white",fontsize=16,fontweight="bold",zorder=4)
def arrow(a,b,t,rad,off): (x1,y1),(x2,y2)=pos[a],pos[b]; ax.annotate("",xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle="-|>",color=NAVY,lw=1.8,shrinkA=38,shrinkB=38,connectionstyle=f"arc3,rad={rad}"),zorder=2); ax.text((x1+x2)/2+off[0],(y1+y2)/2+off[1],t,ha="center",fontsize=12,color=NAVY,bbox=dict(boxstyle="round,pad=0.15",fc="white",ec="none"),zorder=5)
arrow("W","S","0.12 /shift",-0.3,(-0.3,0.7)); arrow("S","W","3.0 /shift",-0.3,(0.3,-0.6)); arrow("S","M","0.5 /shift",-0.3,(0.3,0.7)); arrow("M","W","1.0 /shift",-0.45,(0,-1.3)); arrow("W","M","0.05 /shift",-0.45,(0,1.55))
ax.text(5,0.3,"Rates, not probabilities: each arrow is an exponential alarm clock; the fastest clock rings first",ha="center",fontsize=11.5,color=SLATE)
save(fig,"SP_Fig_CH11_01.png")
# 11.3 two-state transient
fig,ax=plt.subplots(figsize=(10,4.4)); t=np.linspace(0,14,300); l,m=1/7,1.0
ax.plot(t,two_state(l,m,t),color=EMER,lw=2.5,label="P(working at t | working at 0)"); ax.plot(t,1-two_state(m,l,t),color=BURG,lw=2.5,label="P(working at t | in repair at 0)"); ax.axhline(m/(l+m),color=NAVY,ls="--",lw=2,label="long-run availability 7/8")
ax.set_xlabel("t (shifts)"); ax.set_ylabel("probability"); ax.set_ylim(0,1.05); ax.legend(frameon=False,fontsize=11)
save(fig,"SP_Fig_CH11_03.png")
# 11.4 birth-death continuous rate diagram
fig,ax=plt.subplots(figsize=(12,3.2)); ax.axis("off"); ax.set_xlim(0,12); ax.set_ylim(0,3.2)
for i in range(6):
    x=1+i*2; ax.add_patch(Circle((x,1.6),0.45,fc=IVORY,ec=NAVY,lw=2.5)); ax.text(x,1.6,str(i) if i<5 else "…",ha="center",va="center",fontsize=14,color=NAVY,fontweight="bold")
    if i<5:
        ax.annotate("",xy=(x+1.5,1.95),xytext=(x+0.5,1.95),arrowprops=dict(arrowstyle="-|>",color=NAVY,lw=2,connectionstyle="arc3,rad=-0.4")); ax.text(x+1,2.75,f"λ{i}",ha="center",fontsize=13,color=NAVY,fontweight="bold")
        ax.annotate("",xy=(x+0.5,1.25),xytext=(x+1.5,1.25),arrowprops=dict(arrowstyle="-|>",color=BURG,lw=2,connectionstyle="arc3,rad=-0.4")); ax.text(x+1,0.35,f"μ{i+1}",ha="center",fontsize=13,color=BURG,fontweight="bold")
ax.text(6,3.05,"General birth–death process with state-dependent rates",ha="center",fontsize=12,color=SLATE)
save(fig,"SP_Fig_CH11_04.png")
# 11.5 Yule paths
rng=np.random.default_rng(115); fig,ax=plt.subplots(figsize=(10,4.4))
for k in range(5):
    n=3; t=0; T=[0]; N=[3]
    while t<12 and n<200: t+=rng.exponential(1/(0.2*n)); n+=1; T.append(t); N.append(n)
    ax.step(T,N,where="post",color=NAVY,lw=1.5,alpha=0.6)
tt=np.linspace(0,12,100); ax.plot(tt,3*np.exp(0.2*tt),color=GOLD,lw=3,ls="--",label="E[N(t)] = 3·e^(0.2t)"); ax.set_xlim(0,12); ax.set_ylim(0,60); ax.set_xlabel("days"); ax.set_ylabel("customers in the referral program"); ax.legend(frameon=False)
save(fig,"SP_Fig_CH11_05.png")
# 11.6 CTMC pi vs discrete pi
fig,ax=plt.subplots(figsize=(9,4.4)); pi_c=stationary_Q(Q3); pi_d=np.array([0.813,0.102,0.085]); x=np.arange(3)
ax.bar(x-0.18,pi_d,0.36,color=SLATE,label="discrete chain (Table 6.4): fraction of shift-ends"); ax.bar(x+0.18,pi_c,0.36,color=NAVY,label="continuous process (rates): fraction of time")
for xi,(a,b) in enumerate(zip(pi_d,pi_c)): ax.text(xi-0.18,a+0.01,f"{a:.3f}",ha="center",fontsize=11); ax.text(xi+0.18,b+0.01,f"{b:.3f}",ha="center",fontsize=11)
ax.set_xticks(x); ax.set_xticklabels(["Working","Stopped","Maintenance"]); ax.set_ylabel("long-run fraction"); ax.set_ylim(0,1.05); ax.legend(frameon=False,fontsize=10.5)
save(fig,"SP_Fig_CH11_06.png")
# 11.7 Jackson network
fig,ax=plt.subplots(figsize=(11,3.2)); ax.axis("off"); ax.set_xlim(0,11); ax.set_ylim(0,3.2)
ax.annotate("",xy=(2.2,1.6),xytext=(0.3,1.6),arrowprops=dict(arrowstyle="-|>",color=NAVY,lw=3)); ax.text(1.2,2.1,"orders\nλ = 3/min",ha="center",fontsize=11,color=NAVY)
rbox(ax,2.3,0.9,2.6,1.4,IVORY,EMER); ax.text(3.6,1.6,"Station A: pick\nM/M/1, μ = 4",ha="center",va="center",fontsize=11.5,color=NAVY,zorder=3)
ax.annotate("",xy=(6.1,1.6),xytext=(5.0,1.6),arrowprops=dict(arrowstyle="-|>",color=NAVY,lw=3)); ax.text(5.55,2.1,"Poisson(3)",ha="center",fontsize=10.5,color=SLATE)
rbox(ax,6.2,0.9,2.6,1.4,IVORY,GOLD); ax.text(7.5,1.6,"Station B: pack\nM/M/1, μ = 3.5",ha="center",va="center",fontsize=11.5,color=NAVY,zorder=3)
ax.annotate("",xy=(10.7,1.6),xytext=(8.9,1.6),arrowprops=dict(arrowstyle="-|>",color=NAVY,lw=3)); ax.text(9.8,2.1,"shipped",ha="center",fontsize=11,color=NAVY)
ax.text(5.5,0.25,"Burke’s theorem: the output of an M/M/1 in equilibrium is Poisson(λ) — so station B is also M/M/1, and L = L_A + L_B",ha="center",fontsize=11,color=SLATE)
save(fig,"SP_Fig_CH11_07.png")
# 11.8 renewal counting with Weibull gaps
rng=np.random.default_rng(118); gaps=weibull_min.rvs(2.5,scale=12,size=12,random_state=rng); S=np.cumsum(gaps)
fig,ax=plt.subplots(figsize=(11,4)); ax.step(np.r_[0,S],np.arange(0,13),where="post",color=NAVY,lw=2.5,label="N(t): tire replacements so far"); tt=np.linspace(0,S[-1],100); ax.plot(tt,tt/weibull_min.mean(2.5,scale=12),color=GOLD,ls="--",lw=2.5,label="t/μ, μ = mean tire life = 10.65 months")
ax.scatter(S,np.zeros(12)-0.4,marker="|",s=250,color=BURG); ax.set_xlabel("months"); ax.set_ylabel("count"); ax.legend(frameon=False); ax.set_ylim(-0.8,14)
save(fig,"SP_Fig_CH11_08.png")
# 11.9 alternating renewal timeline
rng=np.random.default_rng(119); fig,ax=plt.subplots(figsize=(11,2.6)); ax.axis("off"); ax.set_xlim(0,40); ax.set_ylim(0,2.6)
t=0
while t<40:
    up=weibull_min.rvs(2.5,scale=7.9,random_state=rng); ax.add_patch(Rectangle((t,0.8),min(up,40-t),1.0,fc=EMER,ec="white")); t+=up
    if t>=40: break
    dn=lognorm.rvs(0.5,scale=0.9,random_state=rng); ax.add_patch(Rectangle((t,0.8),min(dn,40-t),1.0,fc=BURG,ec="white")); t+=dn
ax.text(20,2.2,"Alternating renewal: up (green) and down (red) periods",ha="center",fontsize=12.5,color=NAVY); ax.text(20,0.3,"time (shifts)",ha="center",fontsize=11,color=SLATE)
save(fig,"SP_Fig_CH11_09.png")
# 11.10 inspection paradox
rng=np.random.default_rng(120); gaps=rng.exponential(20,40); S=np.cumsum(gaps); fig,ax=plt.subplots(figsize=(11,3)); ax.set_xlim(0,400); ax.set_ylim(-0.5,1.5); ax.set_yticks([]); ax.spines["left"].set_visible(False)
for a,b in zip(np.r_[0,S[:-1]],S): ax.hlines(0.5,a,b,color=NAVY if b-a<20 else GOLD,lw=8,alpha=0.8)
ax.scatter(S,np.full_like(S,0.5),marker="|",s=200,color="white",zorder=3); ax.axvline(233,color=BURG,lw=2.5,ls="--"); ax.text(236,1.1,"a random inspection instant\nlands in a long gap more often",color=BURG,fontsize=11)
ax.set_xlabel("time (seconds); gaps longer than the mean (20 s) in gold"); ax.set_title("The inspection paradox: the gap you fall into has mean 2 × 20 = 40 s for exponential gaps",color=NAVY,fontsize=12)
save(fig,"SP_Fig_CH11_11.png")
# 11.11 age replacement cost rate
F=lambda x: weibull_min.cdf(x,2.5,scale=12); Ts=np.linspace(2,24,60); rates=[age_replacement_rate(T,F,80,600) for T in Ts]; Tbest=Ts[int(np.argmin(rates))]
fig,ax=plt.subplots(figsize=(10,4.4)); ax.plot(Ts,rates,color=NAVY,lw=2.5); ax.axhline(age_replacement_rate(1000,F,80,600),color=BURG,ls="--",lw=2,label=f"replace only at failure: {age_replacement_rate(1000,F,80,600):.1f} €/month")
ax.scatter([Tbest],[min(rates)],color=GOLD,s=90,zorder=3); ax.text(Tbest+0.5,min(rates)+1.5,f"best T ≈ {Tbest:.1f} months: {min(rates):.1f} €/month",color=GOLD,fontsize=12,fontweight="bold")
ax.set_xlabel("planned replacement age T (months)"); ax.set_ylabel("long-run cost per month per tire (€)"); ax.legend(frameon=False); ax.set_ylim(20,65)
save(fig,"SP_Fig_CH11_10.png"); print("best T",Tbest,min(rates),"failure-only",age_replacement_rate(1000,F,80,600))
# 11.12 simulation CTMC long run
rng=np.random.default_rng(121); t,s=simulate_ctmc(Q3,0,20000,rng); dur=np.diff(t); fr=[dur[s[:-1]==k].sum()/t[-1] for k in range(3)]
fig,ax=plt.subplots(figsize=(9,4.2)); x=np.arange(3); ax.bar(x-0.18,fr,0.36,color=NAVY,label="simulated fraction of time (20,000 shifts)"); ax.bar(x+0.18,stationary_Q(Q3),0.36,color=GOLD,label="πQ = 0")
for xi,(a,b) in enumerate(zip(fr,stationary_Q(Q3))): ax.text(xi-0.18,a+0.01,f"{a:.3f}",ha="center",fontsize=11); ax.text(xi+0.18,b+0.01,f"{b:.3f}",ha="center",fontsize=11)
ax.set_xticks(x); ax.set_xticklabels(["W","S","M"]); ax.set_ylim(0,1.05); ax.legend(frameon=False,fontsize=10.5)
save(fig,"SP_Fig_CH11_12.png"); print("sim fr",np.round(fr,4))
# 11.13 concept map
fig,ax=plt.subplots(figsize=(12,7)); ax.axis("off"); ax.set_xlim(0,12); ax.set_ylim(0,7.3); ax.set_aspect("equal")
def cbox(x,y,t,c=NAVY,fc=IVORY,w=2.9,h=1.0,tc=None): rbox(ax,x-w/2,y-h/2,w,h,fc,c,2.2); ax.text(x,y,t,ha="center",va="center",fontsize=11.5,color=tc or NAVY,fontweight="bold",zorder=3,linespacing=1.3)
def link(p1,p2): ax.add_patch(FancyArrowPatch(p1,p2,arrowstyle="-|>",color=SLATE,lw=1.8,mutation_scale=15,zorder=1))
cbox(6,6.5,"Continuous time: rates instead of probabilities",NAVY,NAVY,tc="white",w=6.4)
cbox(2.5,4.8,"Holding times Exp(qᵢ)\n+ jump chain"); cbox(6,4.8,"Rate matrix Q,\nKolmogorov P′ = PQ"); cbox(9.5,4.8,"Stationary πQ = 0\n(balance of rates)")
cbox(2.5,3.0,"Birth–death: Poisson,\nYule, M/M/1, M/M/c",BLUE,w=3.2); cbox(6,3.0,"Uniformization*,\nJackson networks*",EMER); cbox(9.5,3.0,"Renewal processes:\nany gap distribution",CORAL,w=3.2)
cbox(2.5,1.1,"Availability, renewal-\nreward, inspection paradox",GOLD,w=3.4); cbox(6,1.1,"Reliability &\nmaintenance (Ch 12)",GOLD); cbox(9.5,1.1,"Simulation of\nCTMCs (Ch 18)",GOLD)
for b in [(2.5,5.3),(6,5.3),(9.5,5.3)]: link((6,6.0),b)
for xx in (2.5,6,9.5): link((xx,4.3),(xx,3.5)); link((xx,2.5),(xx,1.6))
save(fig,"SP_Fig_CH11_13.png")
# checks
def show(l,v): print(f"{l:<60} {v}")
show("Ex 11.1 Q3 holding means, jump chain",((-1/np.diag(Q3)).round(3),jump_chain(Q3).round(3)))
show("Ex 11.4 two-state pWW(t) t=1,3,7; pi",([round(two_state(1/7,1,t),4) for t in (1,3,7)],0.875))
show("Ex 11.5 P(t) row W t=1,5",(transition(Q3,1)[0].round(4),transition(Q3,5)[0].round(4)))
show("Ex 11.6 Yule E[N(10)]",round(3*np.exp(2),2)); show("Ex 11.7 linear bd E[N(5)]",round(10*np.exp(-1),2))
show("Ex 11.9 pi Q3",stationary_Q(Q3).round(4)); show("Ex 11.10 M/M/1 as CTMC rho .75: p0",0.25)
show("Ex 11.12 uniformization P",(np.eye(3)+Q3/3.5).round(4))
show("Ex 11.13 Jackson L_A, L_B, W",(3,6,3))
show("Ex 11.14 tire mean, replacements/yr/tire, fleet",(round(weibull_min.mean(2.5,scale=12),2),round(12/weibull_min.mean(2.5,scale=12),3),round(48*12/weibull_min.mean(2.5,scale=12),1)))
show("Ex 11.15 availability 7/(7+1)",0.875)
show("Ex 11.16 renewal reward: cost per month failure-only 600/10.65",round(600/10.647,2))
show("Ex 11.17 age replacement best T, rate",(round(Tbest,1),round(min(rates),2)))
show("Ex 11.18 inspection exp mean 20s -> 40s; Weibull k2.5 eta12: E[L^2]/E[L]",round(weibull_min.moment(2,2.5,scale=12)/weibull_min.mean(2.5,scale=12),2))
