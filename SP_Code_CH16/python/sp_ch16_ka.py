"""SP_CH16 (v2) — Keshtel algorithm (KA), textbook version of the author's own book, on R6 with random keys.
Population of M keshtels, sorted each iteration into N1 = round(p1 M) lucky (best), N2 = round(p2 M) unlucky (worst)
and N3 = M - N1 - N2 remaining.
 Phase 1 (lucky): attract the nearest neighbor A (Manhattan distance), r = L - A; diagnostic question O = L + r
   ("slope": f(O) < f(L) -> centre moves to O, attract again; "pit": bisection swirl, rounds s = 1..Smax with
   L +/- r/2^s, L + ||r||_2/2^s u (random direction), L +/- ||r||_1/2^s e_j (random coordinate); first strictly better
   point moves the centre; Smax unsuccessful rounds = food finished; at most 10*Smax evaluations per swirl).
 Phase 2 (unlucky): replaced by new random keshtels.  Phase 3 (remaining): X <- X + lam((G + H)/2 - X), lam ~ U(0,1),
   G, H two other random keshtels; the move is always accepted.
 Keys live in [0,1]^6 (clipped); a keshtel is decoded by sorting its keys (job with the smallest key first)."""
import numpy as np, sys
sys.path.insert(0,__file__.rsplit('/',1)[0])
from sp_ch14_sa import STATES, INDEX, F, NA, label, tardiness
def decode(x): return tuple(int(j) for j in np.argsort(x,kind='stable'))
class Run:
    def __init__(s,rng,budget,memory=False):
        s.rng=rng; s.budget=budget; s.evals=0; s.best=10**9; s.first=None; s.first_distinct=None; s.seen=set(); s.memory=memory; s.hist=[]; s.groups=[]
    def f(s,x,grp=0):
        seq=decode(x); idx=INDEX[seq]; val=int(F[idx])
        if not (s.memory and idx in s.seen): s.evals+=1
        s.seen.add(idx)
        if val<s.best:
            s.best=val; s.groups.append(grp)
        if val==11 and s.first is None: s.first=s.evals; s.first_distinct=len(s.seen)
        s.hist.append((s.evals,s.best)); return val
    def left(s): return s.evals<s.budget
def swirl(run,i,P,fv,Smax,axial_only=False,trace=None):
    """phase 1 for lucky keshtel i (positions P, values fv modified in place)."""
    rng=run.rng; used=0; L=P[i].copy(); fL=fv[i]
    while run.left() and used<10*Smax:
        others=[k for k in range(len(P)) if k!=i]; d=[np.abs(P[k]-L).sum() for k in others]; a=others[int(np.argmin(d))]
        r=L-P[a]
        if not np.any(r): break
        O=np.clip(L+r,0,1); fO=run.f(O,1); used+=1
        if trace is not None: trace.append(('diagnostic',a,O.copy(),fO,fO<fL))
        if fO<fL: L,fL=O,fO; continue
        moved=False
        for s_ in range(1,Smax+1):
            cands=[L+r/2**s_,L-r/2**s_]
            if not axial_only:
                u=rng.standard_normal(len(L)); u/=np.linalg.norm(u); cands.append(L+np.linalg.norm(r)/2**s_*u)
                j=rng.integers(len(L)); e=np.zeros(len(L)); e[j]=1.0; cands.append(L+(1 if rng.random()<0.5 else -1)*np.abs(r).sum()/2**s_*e)
            for c in cands:
                if not run.left() or used>=10*Smax: break
                c=np.clip(c,0,1); fc=run.f(c,1); used+=1
                if trace is not None: trace.append((f'round {s_}',a,c.copy(),fc,fc<fL))
                if fc<fL: L,fL=c,fc; moved=True; break
            if moved or not run.left() or used>=10*Smax: break
        if not moved: break
    P[i]=L; fv[i]=fL
def ka_run(rng,M=10,p1=0.2,p2=0.3,Smax=4,budget=200,memory=False,record=False,N1=None,N2=None):
    N1=int(round(p1*M)) if N1 is None else N1; N2=int(round(p2*M)) if N2 is None else N2; N3=M-N1-N2
    run=Run(rng,budget,memory); P=rng.random((M,6)); fv=np.array([run.f(P[k],0) for k in range(M)],float)
    div=[len({decode(P[k]) for k in range(M)})]; means=[fv.mean()]
    while run.left():
        o=np.argsort(fv,kind='stable'); P=P[o]; fv=fv[o]
        for i in range(N1):
            if run.left(): swirl(run,i,P,fv,Smax)
        for i in range(M-N2,M):
            if run.left(): P[i]=rng.random(6); fv[i]=run.f(P[i],2)
        for i in range(N1,N1+N3):
            if not run.left(): break
            g,h=rng.choice([k for k in range(M) if k!=i],2,replace=False); lam=rng.random()
            P[i]=np.clip(P[i]+lam*((P[g]+P[h])/2-P[i]),0,1); fv[i]=run.f(P[i],3)
        div.append(len({decode(P[k]) for k in range(M)})); means.append(fv.mean())
    return dict(first=run.first,first_distinct=run.first_distinct,best=run.best,hist=run.hist,groups=run.groups,div=div,means=means,distinct=len(run.seen))
# ---- the barrier landscape of Chapter 14 with one key: state = floor(18 x); all keshtels start at x = 0.01 ----
TOY=np.array([40,37,34,31,28,25,28,31,29,27,25,23,21,19,17,15,13,11])
def ka_toy(rng,M=10,N1=2,N2=3,Smax=4,budget=200):
    N3=M-N1-N2; ev=[0]; first=[None]
    def f(x):
        ev[0]+=1; v=TOY[min(17,int(18*x[0]))]
        if v==11 and first[0] is None: first[0]=ev[0]
        return v
    P=np.full((M,1),0.01); fv=np.array([f(p) for p in P],float)
    while ev[0]<budget and first[0] is None:
        o=np.argsort(fv,kind='stable'); P=P[o]; fv=fv[o]
        for i in range(N1):
            L=P[i].copy(); fL=fv[i]; used=0
            while used<10*Smax and ev[0]<budget:
                others=[k for k in range(M) if k!=i]; a=others[int(np.argmin([abs(P[k][0]-L[0]) for k in others]))]; r=L-P[a]
                if not np.any(r): break
                O=np.clip(L+r,0,1); fO=f(O); used+=1
                if fO<fL: L,fL=O,fO; continue
                moved=False
                for s_ in range(1,Smax+1):
                    for c in (L+r/2**s_,L-r/2**s_):
                        c=np.clip(c,0,1); fc=f(c); used+=1
                        if fc<fL: L,fL=c,fc; moved=True; break
                    if moved: break
                if not moved: break
            P[i]=L; fv[i]=fL
        for i in range(M-N2,M): P[i]=rng.random(1); fv[i]=f(P[i])
        for i in range(N1,N1+N3):
            g,h=rng.choice([k for k in range(M) if k!=i],2,replace=False); lam=rng.random(); P[i]=np.clip(P[i]+lam*((P[g]+P[h])/2-P[i]),0,1); fv[i]=f(P[i])
    return first[0]
# ---- hand trace (Tables 16.1–16.3): P0 of Chapter 15 written as random keys; M = 6, N1 = 1, N2 = 2, N3 = 3, Smax = 2, axial points only ----
P0_SEQ=[(0,1,2,3,4,5),(5,4,3,2,1,0),(1,0,3,4,2,5),(0,1,5,3,4,2),(4,2,0,5,1,3),(3,0,1,2,5,4)]
def keys_for(seq,rng):
    v=np.sort(np.round(rng.uniform(0.02,0.98,6),2))
    while len(set(v))<6: v=np.sort(np.round(rng.uniform(0.02,0.98,6),2))
    k=np.zeros(6); 
    for pos,job in enumerate(seq): k[job]=v[pos]
    return k
def hand_trace(seed):
    rng=np.random.default_rng(seed); P=np.array([keys_for(s,rng) for s in P0_SEQ]); fv=np.array([tardiness(decode(p)) for p in P],float)
    class R0:
        evals=0
        def f(self,x,g=0): self.evals+=1; return tardiness(decode(x))
        def left(self): return True
    run=R0(); run.rng=rng; o=np.argsort(fv,kind='stable'); P0=P.copy(); P=P[o]; fv=fv[o]; tr=[]
    swirl(run,0,P,fv,2,axial_only=True,trace=tr)
    new=[]
    for i in (4,5):
        k=np.round(rng.uniform(0.02,0.98,6),2); new.append((o[i],k,tardiness(decode(k)))); P[i]=k; fv[i]=tardiness(decode(k))
    moves=[]
    for i in (1,2,3):
        g,h=rng.choice([k for k in range(6) if k!=i],2,replace=False); lam=round(float(rng.random()),2)
        before=fv[i]; P[i]=np.clip(P[i]+lam*((P[g]+P[h])/2-P[i]),0,1); fv[i]=tardiness(decode(P[i])); moves.append((o[i],o[g],o[h],lam,P[i].copy(),before,fv[i]))
    return P0,o,tr,new,moves,P,fv
