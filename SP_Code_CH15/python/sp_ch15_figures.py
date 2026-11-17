"""SP_CH15 — Chapter 15 figures (genetic algorithm on R6). Usage: python sp_ch15_figures.py A   (diagrams, WF, heat maps, diversity, 30 runs)
                                                                 python sp_ch15_figures.py B   (mutation/crossover sweep, time-to-target)"""
import numpy as np, matplotlib, sys
matplotlib.use("Agg"); sys.path.insert(0,"/home/claude/ch15/code")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from sp_ch15_ga import *
from sp_ch14_sa import NA, run_sa_adj, metropolis_adj, hitting_times
NAVY, GOLD, EMER, BURG, BLUE, CORAL, IVORY, SLATE = "#0B2545","#C9A227","#1B7F5C","#7A1E2B","#2E86AB","#E07A5F","#FBF8F1","#5B6B7C"
plt.rcParams.update({"font.size":14,"axes.titlesize":15,"axes.labelsize":14,"font.family":"DejaVu Sans","axes.edgecolor":SLATE,"axes.spines.top":False,"axes.spines.right":False,"axes.titlepad":10})
OUT="/home/claude/ch15/fig/"
def save(fig,name): fig.savefig(OUT+name,dpi=300,bbox_inches="tight",facecolor="white",pad_inches=0.15); plt.close(fig)
def rbox(ax,x,y,w,h,fc,ec,lw=2.5): ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0,rounding_size=0.12",fc=fc,ec=ec,lw=lw,zorder=2))
sep=lambda fig,xs: [fig.add_artist(plt.Line2D([x,x],[0.05,0.95],color=SLATE,lw=1.2,ls=":")) for x in xs]
JC=[NAVY,GOLD,EMER,BURG,BLUE,CORAL]
POP0=[(0,1,2,3,4,5),(5,4,3,2,1,0),(1,0,3,4,2,5),(0,1,5,3,4,2),(4,2,0,5,1,3),(3,0,1,2,5,4)]
part=sys.argv[1] if len(sys.argv)>1 else "A"
if part=="A":
    # 15.1 GA loop
    fig,ax=plt.subplots(figsize=(13,5.8)); ax.axis("off"); ax.set_xlim(0,13); ax.set_ylim(-0.7,5.2)
    steps=[(1.4,2.6,"Population\nof N sequences",NAVY,True),(4.0,4.2,"Evaluate\ntardiness",SLATE,False),(7.0,4.2,"Select parents\n(tournament)",BLUE,False),(10.2,4.2,"Crossover\n(OX, p_c)",EMER,False),(10.2,1.0,"Mutation\n(adjacent swap, p_m)",CORAL,False),(6.4,1.0,"Elitism:\nkeep the best",GOLD,False)]
    for x,y,t,c,fillc in steps:
        rbox(ax,x-1.25,y-0.55,2.5,1.1,c if fillc else IVORY,c); ax.text(x,y,t,ha="center",va="center",fontsize=11.5,color="white" if fillc else NAVY,fontweight="bold",zorder=3)
    arr=[((2.65,3.0),(2.75,4.0)),((5.25,4.2),(5.75,4.2)),((8.25,4.2),(8.95,4.2)),((10.2,3.65),(10.2,1.55)),((8.95,1.0),(7.65,1.0)),((5.15,1.0),(2.4,2.1))]
    for a,b in arr: ax.add_patch(FancyArrowPatch(a,b,arrowstyle="-|>",color=SLATE,lw=2,mutation_scale=16,zorder=1))
    ax.text(3.8,1.25,"new generation",fontsize=11,color=SLATE,rotation=12)
    ax.text(6.5,-0.45,"one generation = one step of a Markov chain whose state is the whole population",ha="center",fontsize=12.5,color=BURG,fontweight="bold")
    save(fig,"SP_Fig_CH15_01.png")
    # 15.2 selection probabilities for POP0
    f=np.array([tardiness(s) for s in POP0]); g=57-f; pr=g/g.sum(); rank=np.argsort(np.argsort(f))+1; pt=(2*(6-rank)+1)/36
    fig,ax=plt.subplots(figsize=(11,4.6)); x=np.arange(6)
    ax.bar(x-0.18,pr,0.36,color=GOLD,label="roulette, g = 57 − f"); ax.bar(x+0.18,pt,0.36,color=NAVY,label="binary tournament")
    for xi,(a,b) in enumerate(zip(pr,pt)): ax.text(xi-0.18,a+0.008,f"{a:.3f}",ha="center",fontsize=10); ax.text(xi+0.18,b+0.008,f"{b:.3f}",ha="center",fontsize=10)
    ax.set_xticks(x); ax.set_xticklabels([f"#{i+1}\nf = {v}" for i,v in enumerate(f)]); ax.set_ylabel("probability of being chosen as a parent"); ax.set_ylim(0,0.36); ax.legend(frameon=False)
    save(fig,"SP_Fig_CH15_02.png")
    # 15.3 OX and failed one-point
    def row(ax,y,seq,lab,hl=None,bad=None):
        ax.text(-0.3,y,lab,ha="right",va="center",fontsize=11.5,color=NAVY,fontweight="bold")
        for i,j in enumerate(seq):
            fc=JC[j] if j is not None else "white"; ec=BURG if (bad is not None and i in bad) else (GOLD if (hl is not None and hl[0]<=i<=hl[1]) else SLATE)
            ax.add_patch(Rectangle((i,y-0.4),0.92,0.8,fc=fc,ec=ec,lw=3 if ec!=SLATE else 1)); ax.text(i+0.46,y,"" if j is None else NAMES[j],ha="center",va="center",color="white",fontsize=11.5,fontweight="bold")
    fig,axs=plt.subplots(1,2,figsize=(15,4.4),gridspec_kw={"wspace":0.45})
    P1=(0,1,5,3,4,2); P2=(1,0,3,4,2,5)
    ax=axs[0]; ax.set_xlim(-2.2,6.3); ax.set_ylim(-0.2,3.6); ax.axis("off")
    row(ax,3.0,P1,"parent 1",hl=(2,3)); row(ax,2.0,P2,"parent 2"); row(ax,0.6,ox(P1,P2,2,3),"child",hl=(2,3))
    ax.set_title("(a) Order crossover, positions 3–4 from parent 1",color=NAVY,fontsize=12.5)
    ax=axs[1]; ax.set_xlim(-2.2,6.3); ax.set_ylim(-0.2,3.6); ax.axis("off")
    A=(0,1,2,3,4,5); Bq=EDD; ch=one_point(A,Bq,3); dup=[i for i,j in enumerate(ch) if list(ch).count(j)>1]
    row(ax,3.0,A,"parent 1"); row(ax,2.0,Bq,"parent 2"); row(ax,0.6,ch,"child",bad=dup)
    ax.text(3,-0.1,"J1 and J3 twice, J4 and J6 missing: not a schedule",ha="center",fontsize=11,color=BURG)
    ax.set_title("(b) One-point crossover after position 3 fails",color=NAVY,fontsize=12.5)
    sep(fig,[0.5]); save(fig,"SP_Fig_CH15_03.png")
    # 15.4 Wright–Fisher
    N=10; ks=np.arange(0,N+1)
    fig,axs=plt.subplots(1,2,figsize=(13,4.6),gridspec_kw={"wspace":0.3})
    for rule,c,lab in [("neutral",SLATE,"no selection (k/N)"),("roulette",GOLD,"roulette g = 57 − f"),("tournament",NAVY,"binary tournament")]:
        B,_=absorption(wf_matrix(N,rule)); fx=np.r_[0,B[:,1],1]; axs[0].plot(ks,fx,"-o",color=c,lw=2.3,ms=5,label=lab)
    axs[0].plot(ks,np.r_[0,np.ones(N)],"--",color=EMER,lw=2,label="with elitism (any rule)")
    axs[0].set_xlabel("copies of EDD (f = 11) now, out of N = 10 (rest SPT, f = 14)"); axs[0].set_ylabel("P(EDD takes over the population)"); axs[0].legend(frameon=False,fontsize=10.5); axs[0].set_title("(a) Fixation probabilities",color=NAVY,fontsize=12.5)
    rng=np.random.default_rng(154)
    for rule,c in [("roulette",GOLD),("tournament",NAVY)]:
        for r in range(12):
            k=1; path=[k]
            for gen in range(20):
                p=select_prob(k/N,rule); k=rng.binomial(N,p); path.append(k)
            axs[1].plot(range(21),np.array(path)+rng.normal(0,0.08,21),color=c,lw=1.2,alpha=0.7)
    axs[1].set_xlabel("generation"); axs[1].set_ylabel("copies of EDD"); axs[1].set_title("(b) 12 runs each from one copy: navy tournament, gold roulette",color=NAVY,fontsize=12); axs[1].set_ylim(-0.5,10.5)
    sep(fig,[0.5]); save(fig,"SP_Fig_CH15_04.png")
    # 15.5 stationary with mutation
    fig,ax=plt.subplots(figsize=(11,4.4))
    for rule,c,dx in [("roulette",GOLD,-0.2),("tournament",NAVY,0.2)]:
        pi=stationary(wf_matrix(10,rule,0.01)); ax.bar(ks+dx,pi,0.4,color=c,label=f"{rule}: P(no EDD) = {pi[0]:.3g}")
    ax.set_xticks(ks); ax.set_xlabel("copies of EDD in the population (N = 10)"); ax.set_ylabel("stationary probability"); ax.legend(frameon=False)
    save(fig,"SP_Fig_CH15_05.png")
    # 15.6 heat maps (2,000 runs)
    rng=np.random.default_rng(156); gens=[0,2,5,10]; H={g:np.zeros((6,6)) for g in gens}; R=2000
    for r in range(R):
        out=ga_run(10,10,0.9,0.2,rng,record=True)
        for g in gens: H[g]+=position_matrix(out["pops"][g])
    fig,axs2=plt.subplots(2,2,figsize=(12,10.5),gridspec_kw={"wspace":0.25,"hspace":0.35}); axs=axs2.ravel()
    for ax,g in zip(axs,gens):
        Mh=H[g]/R; im=ax.imshow(Mh,cmap="YlOrBr",vmin=0,vmax=1)
        for i in range(6):
            for j in range(6): ax.text(j,i,f"{Mh[i,j]:.2f}",ha="center",va="center",fontsize=12,color="black" if Mh[i,j]<0.6 else "white")
        ax.set_xticks(range(6)); ax.set_xticklabels([str(p) for p in range(1,7)]); ax.set_yticks(range(6)); ax.set_yticklabels(NAMES); ax.set_xlabel("position"); ax.set_title(f"generation {g}",color=NAVY,fontsize=14)
    fig.add_artist(plt.Line2D([0.5,0.5],[0.05,0.95],color=SLATE,lw=1.2,ls=":")); fig.add_artist(plt.Line2D([0.05,0.95],[0.5,0.5],color=SLATE,lw=1.2,ls=":")); save(fig,"SP_Fig_CH15_06.png")
    np.save("/home/claude/ch15/code/heat_gen10.npy",H[10]/R)
    # 15.7 diversity
    rng=np.random.default_rng(157); R=2000; G=21
    D={}; C={}
    for pm in (0.2,0.0):
        div=np.zeros(G+1); conv=np.zeros(G+1)
        for r in range(R):
            out=ga_run(10,G,0.9,pm,rng); div+=out["div"]; conv+=(out["div"]==1)
        D[pm]=div/R; C[pm]=conv/R
    fig,axs=plt.subplots(1,2,figsize=(13,4.4),gridspec_kw={"wspace":0.3})
    axs[0].plot(range(G+1),D[0.2],"-o",color=NAVY,ms=4,lw=2.2,label="p_m = 0.2"); axs[0].plot(range(G+1),D[0.0],"-s",color=BURG,ms=4,lw=2.2,label="p_m = 0 (no mutation)")
    axs[0].set_xlabel("generation"); axs[0].set_ylabel("distinct sequences in the population (N = 10)"); axs[0].legend(frameon=False); axs[0].set_title("(a) Diversity",color=NAVY,fontsize=12.5); axs[0].set_ylim(0,10.5)
    axs[1].plot(range(G+1),C[0.0],"-s",color=BURG,ms=4,lw=2.2,label="p_m = 0"); axs[1].plot(range(G+1),C[0.2],"-o",color=NAVY,ms=4,lw=2.2,label="p_m = 0.2")
    axs[1].set_xlabel("generation"); axs[1].set_ylabel("share of runs with all 10 identical"); axs[1].legend(frameon=False); axs[1].set_title("(b) Absorption: a uniform population",color=NAVY,fontsize=12.5); axs[1].set_ylim(0,1)
    sep(fig,[0.5]); save(fig,"SP_Fig_CH15_07.png"); print("div pm .2 g5,g10,g21",D[0.2][[5,10,21]].round(2),"pm0",D[0.0][[5,10,21]].round(2),"conv pm0 g10,g21",C[0.0][[10,21]].round(3),"pm.2",C[0.2][[10,21]].round(3))
    # 15.8 thirty runs
    rng=np.random.default_rng(158); runs=[ga_run(10,21,0.9,0.2,rng) for _ in range(30)]
    fig,axs=plt.subplots(1,2,figsize=(13,4.6),gridspec_kw={"wspace":0.3})
    for o in runs: axs[0].step(range(22),o["best"],where="post",color=NAVY,lw=0.9,alpha=0.45); axs[1].plot(range(22),o["mean"],color=GOLD,lw=0.9,alpha=0.6)
    axs[0].axhline(11,color=EMER,ls="--",lw=2); axs[0].set_xlabel("generation"); axs[0].set_ylabel("best tardiness in the population"); axs[0].set_title("(a) Best in population, 30 runs",color=NAVY,fontsize=12.5)
    Mm=np.array([o["mean"] for o in runs]); axs[1].plot(range(22),np.median(Mm,axis=0),color=BURG,lw=3,label="median of 30 runs"); axs[1].axhline(11,color=EMER,ls="--",lw=2); axs[1].set_xlabel("generation"); axs[1].set_ylabel("mean tardiness of the population"); axs[1].legend(frameon=False); axs[1].set_title("(b) Population mean, 30 runs",color=NAVY,fontsize=12.5)
    sep(fig,[0.5]); save(fig,"SP_Fig_CH15_08.png"); print("30 runs success",sum(o["first"] is not None for o in runs),"first",[o["first"] for o in runs])
    # 15.11 concept map
    fig,ax=plt.subplots(figsize=(12,7)); ax.axis("off"); ax.set_xlim(0,12); ax.set_ylim(0,7.3); ax.set_aspect("equal")
    def cbox(x,y,t,c=NAVY,fc=IVORY,w=2.9,h=1.0,tc=None): rbox(ax,x-w/2,y-h/2,w,h,fc,c,2.2); ax.text(x,y,t,ha="center",va="center",fontsize=11.5,color=tc or NAVY,fontweight="bold",zorder=3,linespacing=1.3)
    def link(p1,p2): ax.add_patch(FancyArrowPatch(p1,p2,arrowstyle="-|>",color=SLATE,lw=1.8,mutation_scale=15,zorder=1))
    cbox(6,6.5,"Genetic algorithm = a Markov chain on populations",NAVY,NAVY,tc="white",w=6.6)
    cbox(2.5,4.8,"Selection = sampling\n(roulette, tournament)",w=3.2); cbox(6,4.8,"Crossover OX &\nmutation for permutations",w=3.4); cbox(9.5,4.8,"Elitism keeps\nthe best",w=3.0)
    cbox(2.5,3.0,"Wright–Fisher: drift,\nfixation, absorption",BURG,w=3.2); cbox(6,3.0,"Mutation restores\nirreducibility",EMER,w=3.2); cbox(9.5,3.0,"Rudolph: elitism ⇒\nconvergence",CORAL,w=3.2)
    cbox(2.5,1.1,"Heat maps &\ndiversity",GOLD); cbox(6,1.1,"Tuning p_m, p_c,\nN by experiment",GOLD,w=3.1); cbox(9.5,1.1,"Fair comparison:\ntime-to-target",GOLD,w=3.1)
    for b_ in [(2.5,5.3),(6,5.3),(9.5,5.3)]: link((6,6.0),b_)
    for xx in (2.5,6,9.5): link((xx,4.3),(xx,3.5)); link((xx,2.5),(xx,1.6))
    save(fig,"SP_Fig_CH15_11.png")
else:
    # 15.9 sweep
    rng=np.random.default_rng(151); pms=[0.0,0.1,0.2,0.4,0.6,0.8,1.0]; res={}
    for pc in (0.9,0.0):
        res[pc]=[sum(ga_run(10,21,pc,pm,rng)["first"] is not None for _ in range(3000))/3000 for pm in pms]
    fig,ax=plt.subplots(figsize=(10,4.6))
    ax.plot(pms,res[0.9],"-o",color=NAVY,lw=2.5,label="with crossover (p_c = 0.9)"); ax.plot(pms,res[0.0],"-s",color=GOLD,lw=2.5,label="mutation only (p_c = 0)")
    ax.set_xlabel("mutation probability p_m (one adjacent swap per child)"); ax.set_ylabel("success within 199 evaluations"); ax.set_ylim(0,1.05); ax.legend(frameon=False,loc="lower right")
    save(fig,"SP_Fig_CH15_09.png"); print("sweep",{k:np.round(v,3).tolist() for k,v in res.items()})
    # 15.10 time to target
    rng=np.random.default_rng(1510); B=200; R=5000
    def ecdf(firsts): firsts=np.array([f if f is not None else 10**9 for f in firsts]); return np.array([(firsts<=e).mean() for e in range(1,B+1)])
    ga=[ga_run(10,21,0.9,0.2,rng)["first"] for _ in range(R)]; ga4=[ga_run(10,21,0.9,0.4,rng)["first"] for _ in range(R)]
    sa=[]; 
    for _ in range(R):
        st=int(rng.integers(720)); h,b,a,best,first=run_sa_adj(st,10,(0.06/10)**(1/200),200,rng); sa.append(None if first is None else first+1)   # +1: the start counts as an evaluation
    gr=[]
    for _ in range(R):
        x=int(rng.integers(720)); e=1; hit=1 if F[x]==11 else None
        while hit is None and e<B:
            y=NA[x][rng.integers(5)]; e+=1
            if F[y]<=F[x]: x=y
            if F[x]==11: hit=e
        gr.append(hit)
    e=np.arange(1,B+1)
    fig,ax=plt.subplots(figsize=(11,4.8))
    for arr,c,lab in [(ecdf(gr),EMER,"greedy with ties"),(ecdf(sa),GOLD,"simulated annealing (200-step schedule)"),(ecdf(ga4),BLUE,"GA, N = 10, p_m = 0.4"),(ecdf(ga),NAVY,"GA, N = 10, p_m = 0.2"),(1-(718/720)**e,SLATE,"random search")]: ax.plot(e,arr,color=c,lw=2.5,label=lab)
    ax.set_xlabel("evaluations of the objective"); ax.set_ylabel("P(optimum found)"); ax.set_ylim(0,1.02); ax.legend(frameon=False,fontsize=11,loc="lower right")
    save(fig,"SP_Fig_CH15_10.png")
    for nm,arr in [("greedy",gr),("SA",sa),("GA4",ga4),("GA",ga)]:
        a=np.array([f for f in arr if f is not None]); print(nm,"success",round(len(a)/R,4),"mean first",round(a.mean(),1),"P by 100",round((a<=100).sum()/R,3))
