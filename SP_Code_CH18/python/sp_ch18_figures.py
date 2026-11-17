"""SP_CH18 — Chapter 18 figures (discrete-event simulation). Reads des_results.json produced by sp_ch18_simulation.py --all."""
import numpy as np, matplotlib, sys, json
matplotlib.use("Agg"); sys.path.insert(0,"/home/claude/ch18/code")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from sp_ch18_des import *
NAVY, GOLD, EMER, BURG, BLUE, CORAL, IVORY, SLATE = "#0B2545","#C9A227","#1B7F5C","#7A1E2B","#2E86AB","#E07A5F","#FBF8F1","#5B6B7C"
plt.rcParams.update({"font.size":14,"axes.titlesize":15,"axes.labelsize":14,"font.family":"DejaVu Sans","axes.edgecolor":SLATE,"axes.spines.top":False,"axes.spines.right":False,"axes.titlepad":10})
OUT="/home/claude/ch18/fig/"; R=json.load(open("/home/claude/ch18/code/des_results.json"))
def save(fig,name): fig.savefig(OUT+name,dpi=300,bbox_inches="tight",facecolor="white",pad_inches=0.15); plt.close(fig)
def rbox(ax,x,y,w,h,fc,ec,lw=2.5): ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0,rounding_size=0.12",fc=fc,ec=ec,lw=lw,zorder=2))
sep=lambda fig,xs: [fig.add_artist(plt.Line2D([x,x],[0.05,0.95],color=SLATE,lw=1.2,ls=":")) for x in xs]
# 18.1 the event loop
fig,ax=plt.subplots(figsize=(13,5.4)); ax.axis("off"); ax.set_xlim(0,13); ax.set_ylim(0,5.4)
boxes=[(2.0,4.3,"Future event list\n(sorted by time)",NAVY,True),(6.5,4.3,"Take the earliest event;\nadvance the clock to it",BLUE,False),(11.0,4.3,"Update the state\n(servers, queue)",EMER,False),(11.0,1.3,"Schedule new events\n(departures, abandonments)",GOLD,False),(6.5,1.3,"Collect statistics\n(waits, areas, counts)",CORAL,False),(2.0,1.3,"Stop when the list is\nempty or time is up",SLATE,False)]
for x,y,t,c,f in boxes: rbox(ax,x-1.8,y-0.65,3.6,1.3,c if f else IVORY,c); ax.text(x,y,t,ha="center",va="center",fontsize=11.5,color="white" if f else NAVY,fontweight="bold",zorder=3)
for a,b in [((3.85,4.3),(4.65,4.3)),((8.35,4.3),(9.15,4.3)),((11.0,3.6),(11.0,2.0)),((9.15,1.3),(8.35,1.3)),((4.65,1.3),(3.85,1.3)),((2.0,2.0),(2.0,3.6))]: ax.add_patch(FancyArrowPatch(a,b,arrowstyle="-|>",color=SLATE,lw=2,mutation_scale=16))
ax.text(6.5,2.85,"time jumps from event to event — nothing happens in between",ha="center",fontsize=12,color=BURG,fontweight="bold")
save(fig,"SP_Fig_CH18_01.png")
# 18.2 hand trace
fig,axs=plt.subplots(2,1,figsize=(11,5.6),sharex=True,gridspec_kw={"hspace":0.25})
tL=[0,0.6,2.0,2.3,2.4,2.8,3.5,5.2,5.7,6.4,7.3,7.6]; Lv=[0,1,2,3,2,1,0,1,2,1,0,0]; Qv=[0,0,1,2,1,0,0,0,1,0,0,0]
axs[0].step(tL,Lv,where="post",color=NAVY,lw=2.5); axs[0].set_ylabel("in system"); axs[0].set_ylim(-0.2,3.8)
for j,(t,lab) in enumerate([(0.6,"A1"),(2.0,"A2"),(2.3,"A3"),(2.4,"D1"),(2.8,"R3"),(3.5,"D2"),(5.2,"A4"),(5.7,"A5"),(6.4,"D4"),(7.3,"D5")]):
    yy=3.35 if j%2==0 else 2.95; c_=BURG if lab[0]=="R" else (EMER if lab[0]=="A" else BLUE)
    axs[0].plot([t,t],[0,yy-0.15],color=c_,lw=0.8,ls=":"); axs[0].text(t,yy,lab,ha="center",fontsize=10.5,color=c_,fontweight="bold")
axs[1].step(tL,Qv,where="post",color=GOLD,lw=2.5); axs[1].fill_between(tL,Qv,step="post",color=GOLD,alpha=0.3); axs[1].set_ylabel("waiting"); axs[1].set_ylim(-0.2,2.6); axs[1].set_xlabel("minutes")
axs[1].text(4.2,1.8,"shaded area = 1.6 customer-minutes = sum of all waits",fontsize=11.5,color=NAVY)
save(fig,"SP_Fig_CH18_02.png")
# 18.3 audit
wq=np.array(R["audit"]["wq"]); fig,ax=plt.subplots(figsize=(10,4.2))
ax.scatter(wq,np.zeros_like(wq)+0.3,color=SLATE,s=40,label="20 replications (20,000+ calls each)"); m=wq.mean(); h=1.96*wq.std(ddof=1)/np.sqrt(len(wq))
ax.errorbar(m,0,xerr=h,fmt="o",color=NAVY,ms=10,capsize=8,lw=2.5,label=f"mean {m:.1f} s ± {h:.1f} s"); ax.axvline(137.2,color=BURG,ls="--",lw=2,label="Erlang C (Chapter 8): 137.2 s")
ax.set_yticks([]); ax.set_ylim(-0.4,0.8); ax.set_xlabel("average wait in queue (seconds), M/M/5 with λ = 3, mean service 1.5 min"); ax.legend(frameon=False,fontsize=11,loc="upper left"); ax.spines["left"].set_visible(False)
save(fig,"SP_Fig_CH18_03.png")
# 18.4 R1 day: profile and queue
g=np.array(R["grid"]); fig,axs=plt.subplots(2,1,figsize=(11,6.4),sharex=True,gridspec_kw={"hspace":0.2,"height_ratios":[1,2]})
tt=np.linspace(0,600,601); axs[0].plot(tt,[rate(x) for x in tt],color=NAVY,lw=2.5,drawstyle="steps-post"); axs[0].axhline(5*2/3,color=BURG,ls="--",lw=1.8); axs[0].text(430,3.75,"capacity of 5 operators = 3.33 calls/min",color=BURG,fontsize=10.5,va="center"); axs[0].set_ylabel("calls/min"); axs[0].set_ylim(0,4.6)
for k,c,lab in [("A",BURG,"A: 5 operators all day"),("C",GOLD,"C: 7 at 10–13"),("E",EMER,"E: 5 / 7 / 5 / 6")]:
    if k=="E": continue
    q=np.array(R["scen"][k]["qmean"]); axs[1].plot(g,q,color=c,lw=2.5,label=lab)
    if k=="A": axs[1].fill_between(g,R["scen"][k]["q10"],R["scen"][k]["q90"],color=c,alpha=0.15,label="A: 10%–90% of days")
axs[1].set_ylabel("callers waiting"); axs[1].set_xlabel("minutes after 08:00"); axs[1].legend(frameon=False,fontsize=11); axs[1].set_xticks(range(0,721,60)); axs[1].set_xticklabels([f"{8+h}:00" for h in range(13)],fontsize=10)
save(fig,"SP_Fig_CH18_04.png")
# 18.5 service level by period
fig,ax=plt.subplots(figsize=(11,4.6)); per=["08–10","10–13","13–15","15–18"]; x=np.arange(4)
for j,(k,c) in enumerate([("A",BURG),("C",GOLD),("E",EMER)]):
    sl=[p[0] for p in R["scen"][k]["per"]]; ax.bar(x+(j-1)*0.26,sl,0.26,color=c,label={"A":"A: 5 all day","C":"C: 7 at 10–13","E":"E: 5 / 7 / 5 / 6"}[k])
erl=[R["erl"]["2_5"]["SL"],None,R["erl"]["2.5_5"]["SL"],R["erl"]["3_5"]["SL"]]
for xi,v in zip(x,erl):
    if v is not None: ax.scatter([xi-0.26],[v],marker="_",s=600,color=NAVY,lw=3,zorder=3)
ax.scatter([],[],marker="_",s=300,color=NAVY,lw=3,label="Erlang C with 5 operators (steady state)")
ax.set_xticks(x); ax.set_xticklabels(per); ax.set_ylabel("share of calls answered within 30 s"); ax.set_ylim(0,1.05); ax.legend(frameon=False,fontsize=10.5,ncol=2,loc="upper right")
save(fig,"SP_Fig_CH18_05.png")
# 18.6 scenario comparison
ks=["A","B","C","D","E"]; lab={k:f"{k}\n{R['scen'][k]['hours']} h" for k in ks}
fig,axs=plt.subplots(1,3,figsize=(16,5),gridspec_kw={"wspace":0.3}); cols=[BURG,SLATE,GOLD,BLUE,EMER]
for ax,(key,tit,fmt) in zip(axs,[("sl","(a) answered within 30 s","{:.0%}"),("aband","(b) abandoned","{:.1%}"),("wait","(c) mean wait (minutes)","{:.2f}")]):
    v=[R["scen"][k][key] for k in ks]; b_=ax.bar([lab[k] for k in ks],v,color=cols,width=0.6)
    for bi,val in zip(b_,v): ax.text(bi.get_x()+bi.get_width()/2,val*1.03,fmt.format(val),ha="center",fontsize=11.5)
    ax.set_title(tit,color=NAVY,fontsize=13); ax.tick_params(axis="x",labelsize=12); ax.set_ylim(0,max(v)*1.18)
sep(fig,[0.365,0.645]); save(fig,"SP_Fig_CH18_06.png")
# 18.7 CRN
dC=np.array(R["crn_cd"]["dC"]); dI=np.array(R["crn_cd"]["dI"]); fig,ax=plt.subplots(figsize=(10,4.4)); bins=np.linspace(-0.35,0.15,50)
ax.hist(dI,bins=bins,color=SLATE,alpha=0.6,label=f"independent streams (SD {dI.std(ddof=1):.3f})"); ax.hist(dC,bins=bins,color=NAVY,alpha=0.85,label=f"common random numbers (SD {dC.std(ddof=1):.3f})")
ax.axvline(dC.mean(),color=GOLD,ls="--",lw=2,label=f"average difference {dC.mean():.3f}"); ax.axvline(0,color=BURG,lw=1.5)
ax.set_xlabel("difference in daily service level, scenario C minus scenario D"); ax.set_ylabel("days (100)"); ax.legend(frameon=False,fontsize=10.5,loc="upper left")
save(fig,"SP_Fig_CH18_07.png")
# 18.8 warm-up
fig,ax=plt.subplots(figsize=(10,4.4)); gw=np.array(R["warm"]["grid"]); ax.plot(gw,R["warm"]["q"],color=NAVY,lw=2.5,label="average over 300 runs started empty"); ax.axhline(0.762*0.9/0.1,color=BURG,ls="--",lw=2,label="steady state Lq = 6.86 (Chapter 8)")
ax.set_xlabel("minutes after an empty start (λ = 3, 5 operators)"); ax.set_ylabel("callers waiting"); ax.legend(frameon=False,fontsize=11,loc="lower right"); ax.set_ylim(0,9)
save(fig,"SP_Fig_CH18_08.png")
# 18.9 R2 down durations
rng=np.random.default_rng(1812); s_ln=np.sqrt(np.log(1+1.5**2)); m_ln=-s_ln**2/2
fig,ax=plt.subplots(figsize=(10,4.6)); xs=np.linspace(0,6,200)
for k,f,c in [("exponential",lambda g: g.exponential(1.0),NAVY),("constant",lambda g: 1.0,EMER),("lognormal",lambda g: g.lognormal(m_ln,s_ln),BURG)]:
    A,d=line_sim(f,rng); ax.semilogy(xs,[max((d>x).mean(),1e-4) for x in xs],color=c,lw=2.5,label=f"{k} repair: availability {A:.3f}, P(stop > 2 shifts) {np.mean(d>2):.1%}")
ax.set_xlabel("length of a line stoppage (shifts)"); ax.set_ylabel("P(stoppage longer than x)"); ax.set_ylim(1e-3,1.1); ax.legend(frameon=False,fontsize=10.5,loc="lower left")
save(fig,"SP_Fig_CH18_09.png")
# 18.10 R5 fleet bursts
rtf=np.array(R["r5"]["rtf"]); age=np.array(R["r5"]["age"]); fig,ax=plt.subplots(figsize=(10,4.4)); k=np.arange(0,13)
ax.bar(k-0.2,[np.mean(rtf==i) for i in k],0.4,color=BURG,label=f"run to failure (mean {rtf.mean():.2f} per month)"); ax.bar(k+0.2,[np.mean(age==i) for i in k],0.4,color=EMER,label=f"replace at 5 months (mean {age.mean():.2f} per month)")
ax.set_xticks(k); ax.set_xlabel("tire bursts in the 48-tire fleet in one month"); ax.set_ylabel("share of months (1,200 simulated)"); ax.legend(frameon=False,fontsize=11)
save(fig,"SP_Fig_CH18_10.png")
# 18.11 concept map
fig,ax=plt.subplots(figsize=(12,7)); ax.axis("off"); ax.set_xlim(0,12); ax.set_ylim(0,7.3); ax.set_aspect("equal")
def cbox(x,y,t,c=NAVY,fc=IVORY,w=2.9,h=1.0,tc=None): rbox(ax,x-w/2,y-h/2,w,h,fc,c,2.2); ax.text(x,y,t,ha="center",va="center",fontsize=11.5,color=tc or NAVY,fontweight="bold",zorder=3,linespacing=1.3)
def link(p1,p2): ax.add_patch(FancyArrowPatch(p1,p2,arrowstyle="-|>",color=SLATE,lw=1.8,mutation_scale=15,zorder=1))
cbox(6,6.5,"Discrete-event simulation of Nava’s processes",NAVY,NAVY,tc="white",w=6.4)
cbox(2.5,4.8,"State, clock,\nfuture event list"); cbox(6,4.8,"Inputs from Ch 17:\nthinning, inverse transform",w=3.4); cbox(9.5,4.8,"Statistics: waits,\nareas (Little), counts",w=3.1)
cbox(2.5,3.0,"Audit against\nformulas (Ch 8, 11, 12)",EMER,w=3.2); cbox(6,3.0,"R1 day: time-varying λ,\nabandonment, shifts",CORAL,w=3.4); cbox(9.5,3.0,"Scenarios with common\nrandom numbers",BLUE,w=3.2)
cbox(2.5,1.1,"R2: averages insensitive,\ntails sensitive",GOLD,w=3.3); cbox(6,1.1,"R5: bursts per month\nby policy",GOLD,w=3.1); cbox(9.5,1.1,"Warm-up and output\nanalysis (Ch 19)",GOLD,w=3.1)
for b_ in [(2.5,5.3),(6,5.3),(9.5,5.3)]: link((6,6.0),b_)
for xx in (2.5,6,9.5): link((xx,4.3),(xx,3.5)); link((xx,2.5),(xx,1.6))
save(fig,"SP_Fig_CH18_11.png")
