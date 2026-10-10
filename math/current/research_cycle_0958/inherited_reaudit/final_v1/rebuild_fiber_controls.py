"""Fresh F015 recognizer/control implementation; all historical code remains inert.
Finite tests supplement, but do not replace, the all-size mathematical proof.
"""
from pathlib import Path
from random import Random
import json

def dense(x,w,p):
    n=len(x)
    return [sum(a*pow(w,j*k,p) for j,a in enumerate(x))%p for k in range(n)]
def prune(items,n,w,p):
    if not items:return [0]*n
    if n==1:return [items[0][1]%p]
    a=prune([(i//2,v) for i,v in items if i%2==0],n//2,w*w%p,p)
    b=prune([(i//2,v) for i,v in items if i%2],n//2,w*w%p,p)
    out=[0]*n;t=1
    for k in range(n//2):
        z=t*b[k]%p;out[k]=(a[k]+z)%p;out[k+n//2]=(a[k]-z)%p;t=t*w%p
    return out
def bm(y,p):
    C=[1]+[0]*len(y);old=C[:];r=0;last=1;shift=1
    for n in range(len(y)):
        err=(y[n]+sum(C[j]*y[n-j] for j in range(1,r+1)))%p
        if not err:shift+=1;continue
        saved=C[:];fac=err*pow(last,-1,p)%p
        for j in range(len(y)+1-shift):C[j+shift]=(C[j+shift]-fac*old[j])%p
        if 2*r<=n:r=n+1-r;old=saved;last=err;shift=1
        else:shift+=1
    return C[:r+1]
def horner(c,z,p):
    a=0
    for v in reversed(c):a=(a*z+v)%p
    return a
def recognize(y,b,eta,p):
    M=len(y);C=bm(y[:2*b],p);r=len(C)-1
    if r>b:return None
    if r==0:return [] if not any(y) else None
    vals=prune([(j,c) for j,c in enumerate(C) if c],M,eta,p)
    H=[h for h,v in enumerate(vals) if v==0]
    if len(H)!=r:return None
    A=[sum(C[j]*y[u-j] for j in range(u+1))%p for u in range(r)]
    deriv=[j*C[j]%p for j in range(1,r+1)];modes=[]
    for h in H:
        z=pow(eta,h,p);den=horner(deriv,z,p)
        if not den:return None
        amp=-pow(z,-1,p)*horner(A,z,p)*pow(den,-1,p)%p
        if not amp:return None
        modes.append((h,amp))
    return modes if prune(modes,M,pow(eta,-1,p),p)==y else None
def synth(mode_lists,Q,M,w,p):
    buckets=[[] for _ in range(M)]
    for t,modes in enumerate(mode_lists):
        for h,a in modes:buckets[h].append((t,a*pow(w,h*t,p)%p))
    out=[0]*(Q*M)
    for h,items in enumerate(buckets):
        vals=prune(items,Q,pow(w,M,p),p)
        for v,a in enumerate(vals):out[h+M*v]=M*a%p
    return out
def transform(x,w,p,b=None,budget=None):
    N=len(x);k=N.bit_length()-1;Q=1<<(k//2);M=N//Q;eta=pow(w,Q,p)
    assert pow(w,N,p)==1 and pow(w,N//2,p)!=1
    agg=budget is not None
    if agg:b=min(M//2,max(1,(budget+Q-1)//Q)*(M.bit_length()-1))
    found=[];K=0;heavy=0
    for t in range(Q):
        y=x[t::Q];z=recognize(y,b,eta,p)
        if z is None:
            if not agg:return None,heavy
            vals=dense(y,eta,p);iv=pow(M,-1,p)
            z=[(h,a*iv%p) for h,a in enumerate(vals) if a];heavy+=1
            assert len(z)>b
        found.append(z);K+=len(z)
        if agg and K>budget:
            assert heavy<=budget//(b+1)+1
            return None,heavy
    if agg:assert heavy<=budget//(b+1)
    return synth(found,Q,M,w,p),heavy
def solve_green(z,w,p):
    N=len(z);aa=[];bb=[];A=1;B=0
    for j in range(N):
        d=(7+pow(w,j,p))%p
        if not d:return None
        a=-2*pow(d,-1,p)%p;b=z[j]*pow(d,-1,p)%p
        aa.append(a);bb.append(b);A=a*A%p;B=(a*B+b)%p
    if A==1:return None
    prev=B*pow(1-A,-1,p)%p;out=[]
    for a,b in zip(aa,bb):prev=(a*prev+b)%p;out.append(prev)
    return out
def run():
    rng=Random(958015);counts={'cap_cases':0,'accepted':0,'rejected':0,'aggregate_cases':0,'aggregate_heavy':0,'green_cases':0,'explicit_output_coordinates':0,'late_mutations':0}
    for p,g,maxk in [(17,3,4),(97,5,5),(257,3,7),(65537,3,7)]:
      for k in range(2,maxk+1):
        N=1<<k;Q=1<<(k//2);M=N//Q;w=pow(g,(p-1)//N,p);eta=pow(w,Q,p)
        assert pow(w,N//2,p)!=1
        for b in sorted(set([1,max(1,M//4),M//2])):
          for trial in range(15):
            if trial<8:
                modes=[]
                for t in range(Q):
                    r=rng.randrange(b+1);hs=rng.sample(range(M),r)
                    modes.append([(h,rng.randrange(1,p)) for h in hs])
                fibers=[prune(m,M,pow(eta,-1,p),p) for m in modes]
                x=[fibers[j%Q][j//Q] for j in range(N)]
                if trial==7 and 2*b<M:
                    x[-1]=(x[-1]+1)%p;counts['late_mutations']+=1
            else:x=[rng.randrange(p) for _ in range(N)]
            true_modes=[sum(a!=0 for a in dense(x[t::Q],eta,p)) for t in range(Q)]
            expected=max(true_modes)<=b
            out,_=transform(x,w,p,b=b)
            assert (out is not None)==expected
            counts['cap_cases']+=1;counts['accepted' if expected else 'rejected']+=1
            if out is not None:assert out==dense(x,w,p);counts['explicit_output_coordinates']+=N
            for K0 in set([0,sum(true_modes),max(0,sum(true_modes)-1)]):
                out,hv=transform(x,w,p,budget=K0)
                assert (out is not None)==(sum(true_modes)<=K0)
                counts['aggregate_cases']+=1;counts['aggregate_heavy']+=hv
                if out is not None:assert out==dense(x,w,p);counts['explicit_output_coordinates']+=N
            if trial==0:
                residual=[((7+2*pow(w,-j,p))*x[j]+x[(j-1)%N])%p for j in range(N)]
                fr=dense(residual,w,p);out=solve_green(fr,w,p)
                if out is not None:assert out==dense(x,w,p);counts['green_cases']+=1
    # Explicit guard counterexample: invertibility does not imply this solver's local guards.
    N=16;p=17;w=3;ds=[(7+pow(w,j,p))%p for j in range(N)]
    bad=[j for j,d in enumerate(ds) if d==0]
    prod=1
    for d in ds:prod=prod*d%p
    det=(prod-pow(2,N,p))%p
    assert bad and det and solve_green([0]*N,w,p) is None
    result={'fresh_controls':counts,'green_guard_counterexample':{'N':N,'p':p,'primitive_root':w,'zero_diagonal_positions':bad,'determinant_of_L':det,'meaning':'L is invertible but the declared divide-by-diagonal scan is invalid; guarded Green contract is essential.'},'historical_programs_executed':False,'claim':'Exact field algorithm controls, not bit complexity, numerical stability, source-code replay, or timing.'}
    (Path(__file__).resolve().parent/'FIBER_FRESH_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':run()
