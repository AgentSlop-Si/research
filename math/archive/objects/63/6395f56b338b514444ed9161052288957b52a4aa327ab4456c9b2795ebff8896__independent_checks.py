#!/usr/bin/env python3
"""Independent exact checks; no imported/executed uploaded source. Python stdlib only."""
from collections import Counter, deque
from itertools import permutations, combinations
from pathlib import Path
import json, math, random

ROOT=Path(__file__).resolve().parent

def rank(A,p):
    A=[list(row) for row in A]
    if not A:return 0
    m,n=len(A),len(A[0]);q=0
    for j in range(n):
        pivot=next((i for i in range(q,m) if A[i][j]%p),None)
        if pivot is None:continue
        A[q],A[pivot]=A[pivot],A[q]
        inv=pow(A[q][j],-1,p)
        A[q]=[x*inv%p for x in A[q]]
        for i in range(q+1,m):
            c=A[i][j]%p
            A[i]=[(x-c*y)%p for x,y in zip(A[i],A[q])]
        q+=1
        if q==m:break
    return q

def inv(A,p):
    n=len(A);T=[list(A[i])+[int(i==j) for j in range(n)] for i in range(n)]
    for j in range(n):
        k=next(i for i in range(j,n) if T[i][j]%p)
        T[j],T[k]=T[k],T[j]; c=pow(T[j][j],-1,p)
        T[j]=[c*x%p for x in T[j]]
        for i in range(n):
            if i!=j:
                c=T[i][j];T[i]=[(x-c*y)%p for x,y in zip(T[i],T[j])]
    return [r[n:] for r in T]

def mul(A,B,p):return [[sum(x*y for x,y in zip(row,col))%p for col in zip(*B)] for row in A]
def sub(A,R,H):return [[A[i][j] for j in H] for i in R]
def qs(A,p):
    n=len(A)
    return (max((rank(sub(A,range(k),range(k,n)),p) for k in range(1,n)),default=0),
            max((rank(sub(A,range(k,n),range(k)),p) for k in range(1,n)),default=0))

def root(n,p):
    prime_divisors=[d for d in range(2,n+1) if n%d==0 and all(d%e for e in range(2,math.isqrt(d)+1))]
    for b in range(2,p):
        z=pow(b,(p-1)//n,p)
        if pow(z,n,p)==1 and all(pow(z,n//d,p)!=1 for d in prime_divisors):return z
    raise ValueError('No primitive root')

def gate_values(pi,u,v,ranks):
    cu,cd,bu,bd=ranks;n=len(pi);a=min(pi[u:v+1]);b=max(pi[u:v+1]);t=v-u+1
    budget=(bu if u else 0)+(bd if v+1<n else 0)
    return ((min(t,a),budget+(cu if a else 0)),
            (min(t,n-1-b),budget+(cd if b+1<n else 0)),
            (min(t,n-1-b+a),budget+(cu if a else 0)+(cd if b+1<n else 0)))

def slow_screen(pi,ranks=(1,1,1,1)):
    return all(x<=y for u in range(len(pi)) for v in range(u,len(pi)) for x,y in gate_values(pi,u,v,ranks))

def rolling_extrema(a,width):
    lo,hi=deque(),deque()
    for j,x in enumerate(a):
        while lo and a[lo[-1]]>=x:lo.pop()
        while hi and a[hi[-1]]<=x:hi.pop()
        lo.append(j);hi.append(j)
        while lo and lo[0]<=j-width:lo.popleft()
        while hi and hi[0]<=j-width:hi.popleft()
        if j+1>=width:yield j-width+1,a[lo[0]],a[hi[0]]

def fast_screen(pi,ranks=(1,1,1,1)):
    """Exact all-window reduction: at most six endpoint and three sliding tests."""
    n=len(pi);cu,cd,bu,bd=ranks
    for typ,cr in enumerate((cu,cd,cu+cd)):
        for side,br in ((0,bd),(1,bu)):
            w=br+cr+1
            if w<n:
                u,v=(0,w-1) if side==0 else (n-w,n-1)
                x,y=gate_values(pi,u,v,ranks)[typ]
                if x>y:return False
        w=bu+bd+cr+1
        if w<=n-2:
            for u,a,b in rolling_extrema(pi,w):
                if 1<=u and u+w<=n-1:
                    if typ==0 and a>=w:return False
                    if typ==1 and n-1-b>=w:return False
                    if typ==2 and a>0 and b<n-1 and n-1-b+a>=w:return False
    return True

def old_screen(pi):
    n=len(pi)
    return all(min(t,min(pi[:t]))<=2 and min(t,n-1-max(pi[-t:]))<=2 for t in range(1,n))

def general_checks(M,C,B,pi,p):
    n=len(pi);cu,cd=qs(C,p);bu,bd=qs(B,p)
    assert mul(M,[[row[j] for j in pi] for row in C],p)==B
    count=0
    for u in range(n):
        for v in range(u,n):
            a,b=min(pi[u:v+1]),max(pi[u:v+1]);t=v-u+1
            R=list(range(u))+list(range(v+1,n));beta=(bu if u else 0)+(bd if v+1<n else 0)
            for H,extra in ((range(a,n),cu if a else 0),(range(b+1),cd if b+1<n else 0),(range(a,b+1),(cu if a else 0)+(cd if b+1<n else 0))):
                assert t-len(H)+rank(sub(M,R,H),p)<=beta+extra
                count+=1
    return count

def ct_control(a,b,p):
    """Derive two stages from j=s+a*t, k=q+b*p, with dyadic small orders."""
    n=a*b;z=root(n,p)
    oa=list(range(a)) if a==2 else [0,2,1,3]
    ob=[0,2,1,3]
    input_pairs=[(s,t) for s in range(a) for t in ob]
    after_first=[(s,q) for s in range(a) for q in ob]
    after_shuffle=[(s,q) for q in range(b) for s in oa]
    output_pairs=[(ell,q) for q in range(b) for ell in oa]
    A=[[pow(z,a*q*t,p) if s==ss else 0 for ss,t in input_pairs] for s,q in after_first]
    B=[[pow(z,(q+b*ell)*s,p) if q==qq else 0 for s,qq in after_shuffle] for ell,q in output_pairs]
    pi=[after_first.index(pair) for pair in after_shuffle]
    inp=[s+a*t for s,t in input_pairs];out=[q+b*ell for ell,q in output_pairs]
    M=[[pow(z,k*j,p) for j in inp] for k in out]
    assert mul(B,[A[k] for k in pi],p)==M
    C=inv(A,p);assert qs(A,p)==qs(B,p)==qs(C,p)==(1,1)
    checks=general_checks(M,C,B,pi,p)
    h=max(pi[:3])+1; actual=rank(sub(M,range(3,n),range(h)),p)
    assert actual==h-1 and not slow_screen(pi)
    return dict(n=n,prime=p,root=z,input_order=inp,output_order=out,pi=pi,stage_qs=[1,1],checks=checks,witness_rank=actual,naive_rank=h,corrected_lower=3-h+actual,naive_lower=3)

def main():
    rng=random.Random(782518)
    counts=Counter();fast_equal=0
    for pi in permutations(range(8)):
        a=slow_screen(pi);b=fast_screen(pi);assert a==b;fast_equal+=1
        counts[str((old_screen(pi),a))]+=1
    assert counts=={'(True, True)':15728,'(True, False)':12856,'(False, False)':11736}
    for n in range(2,11):
        for _ in range(120):
            pi=list(range(n));rng.shuffle(pi);rs=tuple(rng.randrange(4) for _ in range(4))
            assert slow_screen(pi,rs)==fast_screen(pi,rs);fast_equal+=1
    for n in (16,32,64,100):
        for _ in range(30):
            pi=list(range(n));rng.shuffle(pi);rs=tuple(rng.randrange(10) for _ in range(4))
            assert slow_screen(pi,rs)==fast_screen(pi,rs);fast_equal+=1
    witness=[8,0,13,4,9,3,15,5,6,1,12,11,10,2,14,7]
    assert slow_screen(witness)
    marker_controls=[]
    for n in (16,17,18):
        good=[]
        for loc in combinations(range(n),4):
            if loc[0]<=2 and loc[-1]>=n-3 and max(y-x for x,y in zip(loc,loc[1:]))<=4:good.append(loc)
        marker_controls.append({'n':n,'allowed_extreme_four_position_sets':len(good),'sets':good if n>=17 else None})
    assert marker_controls[1]['sets']==[(2,6,10,14)] and marker_controls[2]['sets']==[]
    ct=[ct_control(a,4,12289) for a in (2,4)]
    gen=0
    for n in (3,5,8,12):
        p=12289
        for _ in range(4):
            def stage():
                while True:
                    u=[rng.randrange(1,p) for i in range(n)];v=[rng.randrange(1,p) for i in range(n)]
                    if (1+sum(x*y for x,y in zip(u,v)))%p:break
                return [[(int(i==j)+u[i]*v[j])%p for j in range(n)] for i in range(n)]
            C,B=stage(),stage();pi=list(range(n));rng.shuffle(pi)
            M=mul(B,inv([[row[j] for j in pi] for row in C],p),p)
            gen+=general_checks(M,C,B,pi,p)
    vd=0
    for p in (12289,65537):
        for n in (8,16,32,64):
            z=root(n,p)
            for _ in range(16):
                rho=list(range(n));rng.shuffle(rho);c=rng.randrange(n);d=rng.choice([d for d in range(1,n) if math.gcd(d,n)==1])
                M=[[pow(z,rho[i]*(c+d*j),p) for j in range(n)] for i in range(n)]
                R=rng.sample(range(n),rng.randrange(n+1));lo=rng.randrange(n);hi=rng.randrange(lo+1,n+1);H=range(lo,hi)
                assert rank(sub(M,R,H),p)==min(len(R),len(H));vd+=1
    out={'status':'PASS','stdlib_only':True,'uploaded_code_executed':False,'N8_counts':dict(counts),'fast_slow_screen_equivalences':fast_equal,'N16_screen_witness':witness,'marker_controls':marker_controls,'CT_controls':ct,'general_rank_inequalities':gen,'affine_Vandermonde_checks':vd,'scope':'Exact finite-field and combinatorial controls; proof in WINDOW_AUDIT.md. Passing is not sufficient for factorization.'}
    (ROOT/'CHECK_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
