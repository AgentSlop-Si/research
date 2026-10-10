#!/usr/bin/env python3
"""New, standard-library-only controls. Does not import research programs."""
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
import json, math, random

P = 1009
rng = random.Random(540)

def eye(n): return [[int(i == j) for j in range(n)] for i in range(n)]
def zero(n): return [[0]*n for _ in range(n)]
def add(a,b): return [[(x+y)%P for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def neg(a): return [[-x%P for x in row] for row in a]
def sub(a,b): return add(a,neg(b))
def scale(c,a): return [[c*x%P for x in row] for row in a]
def mul(a,b):
    n=len(a); out=zero(n)
    for i in range(n):
        for k in range(n):
            if a[i][k]:
                for j in range(n): out[i][j]=(out[i][j]+a[i][k]*b[k][j])%P
    return out

def rank(a):
    a=[row[:] for row in a]; n=len(a); r=0
    for j in range(n):
        u=next((i for i in range(r,n) if a[i][j]),None)
        if u is None: continue
        a[r],a[u]=a[u],a[r]; z=pow(a[r][j],-1,P)
        a[r]=[z*x%P for x in a[r]]
        for i in range(r+1,n):
            z=a[i][j]
            if z: a[i]=[(x-z*y)%P for x,y in zip(a[i],a[r])]
        r+=1
    return r

def inv(a):
    n=len(a); b=[row[:]+e for row,e in zip(a,eye(n))]
    for j in range(n):
        u=next((i for i in range(j,n) if b[i][j]),None)
        if u is None: raise ValueError('singular')
        b[j],b[u]=b[u],b[j]; z=pow(b[j][j],-1,P)
        b[j]=[z*x%P for x in b[j]]
        for i in range(n):
            if i!=j:
                z=b[i][j]
                b[i]=[(x-z*y)%P for x,y in zip(b[i],b[j])]
    return [row[n:] for row in b]

def mpow(a,k):
    v=eye(len(a))
    while k:
        if k&1:v=mul(v,a)
        k//=2
        if k:a=mul(a,a)
    return v

def perm(p,w=None):
    n=len(p); a=zero(n); w=w or [1]*n
    for j in range(n): a[p[j]][j]=w[j]%P
    return a

def root(r):
    if r==1:return 1
    for z in range(2,P):
        if pow(z,r,P)==1 and all(pow(z,d,P)!=1 for d in range(1,r) if r%d==0):return z
    raise AssertionError('root absent')

def cmax(a):return max(sum(a[i][j]!=0 for i in range(len(a))) for j in range(len(a)))
def random_monomial(n,partial=True):
    p=list(range(n));rng.shuffle(p)
    return perm(p,[rng.randrange(0 if partial else 1,8) for _ in range(n)])

def run_field_cases():
    records=[]; equalities=0; noncommuting_controls=0
    for n in (3,4,5,6,7,8,9,10,12,15,17):
        p=perm([(j+1)%n for j in range(n)]); I=eye(n)
        for r in (1,2,3,4,6):
            a=pow(2,-1,P); z=root(r); pr=mpow(p,r); b=pow(a,r,P)
            Q=sub(I,scale(b,pr))
            try: qi=inv(Q)
            except ValueError:continue
            G=[]; H=[]
            for i in range(r):
                lam=a*pow(z,i,P)%P; h=zero(n); power=I
                for s in range(r):h=add(h,scale(pow(lam,s,P),power));power=mul(power,p)
                g=inv(sub(I,scale(lam,p)))
                assert g==mul(h,qi);equalities+=n*n; G.append(g);H.append(h)
            # Inherited distinct-branch root-packet identity, independently checked.
            avg=zero(n)
            for g in G:avg=add(avg,g)
            avg=scale(pow(r,-1,P),avg)
            assert avg==qi;equalities+=n*n
            # Arbitrary left monomials; compatible independent right cyclic routes.
            T=M=zero(n)
            for i in range(r):
                L=random_monomial(n);R=mpow(p,(3*i+1)%n)
                T=add(T,mul(mul(L,G[i]),R));M=add(M,mul(mul(L,H[i]),R))
            assert cmax(M)<=min(n,r*r)
            assert T==mul(M,qi);equalities+=n*n
            # Shared right route and independent diagonal left weights give <=r.
            T=M=zero(n);R=mpow(p,2)
            for i in range(r):
                L=perm(list(range(n)),[rng.randrange(8) for _ in range(n)])
                T=add(T,mul(mul(L,G[i]),R));M=add(M,mul(mul(L,H[i]),R))
            assert cmax(M)<=min(n,r)
            assert T==mul(M,qi);equalities+=n*n
            # Arbitrary right routes, including zero endpoint weights.
            T=M=E=zero(n);K=0
            for i in range(r):
                L=random_monomial(n);R=random_monomial(n)
                C=sub(mul(R,Q),mul(Q,R));K+=rank(sub(mul(R,pr),mul(pr,R)))
                T=add(T,mul(mul(L,G[i]),R));M=add(M,mul(mul(L,H[i]),R))
                E=add(E,mul(mul(mul(mul(L,H[i]),qi),C),qi))
            assert cmax(M)<=min(n,r*r)
            assert T==add(mul(M,qi),E);equalities+=n*n
            assert rank(E)<=K
            if T!=mul(M,qi):noncommuting_controls+=1
            records.append({'N':n,'r':r,'K':K,'correction_rank':rank(E)})
    # The guard is real: no false inversion is admitted at a resonant pole.
    try: inv(sub(eye(5),perm([1,2,3,4,0])))
    except ValueError:pass
    else:raise AssertionError('singular guard failed')
    assert noncommuting_controls>0
    return {'cases':len(records),'matrix_entry_equalities':equalities,
            'noncommuting_negative_controls':noncommuting_controls,'details':records}

# Exact characteristic-zero density tests, with independently built Phi_N.
def trim(a):
    a=a[:]
    while len(a)>1 and a[-1]==0:a.pop()
    return a

def divrem(a,b):
    a=[Fraction(x) for x in a];b=[Fraction(x) for x in b]
    q=[Fraction(0)]*max(1,len(a)-len(b)+1)
    while any(a) and len(a)>=len(b):
        k=len(a)-len(b);c=a[-1]/b[-1];q[k]=c
        for j,x in enumerate(b):a[j+k]-=c*x
        a=trim(a)
    return trim(q),trim(a)

@lru_cache(None)
def phi(n):
    a=[-1]+[0]*(n-1)+[1]
    for d in range(1,n):
        if n%d==0:
            a,rem=divrem(a,phi(d));assert not any(rem)
    assert all(x.denominator==1 for x in map(Fraction,a))
    return tuple(int(x) for x in a)

def run_charzero_density():
    entries=0;cases=0
    for n in (1,2,3,4,5,6,7,8,9,10,11,12,15,16,17,21):
        for r in range(1,7):
            order=list(range(n));rng.shuffle(order)
            route=[0]*n
            for i in range(n):route[order[i]]=order[(i+1)%n]
            pr=list(range(n))
            for _ in range(r):pr=[route[j] for j in pr]
            for j in range(n):
                for k in range(n):
                    # 2^r sqrt(N)*(UQ)[j,k] = 2^r z^(jk)-z^(j P^r(k)).
                    f=[0]*n;f[j*k%n]+=2**r;f[j*pr[k]%n]-=1
                    _,rem=divrem(trim(f),phi(n));assert any(rem);entries+=1
            cases+=1
    return {'cases':cases,'exact_nonzero_entries':entries,'lengths':'1,2,3,4,5,6,7,8,9,10,11,12,15,16,17,21'}

class Counter:
    def __init__(self):self.adds=0;self.mults=0
    def add(self,x,y):self.adds+=1;return (x+y)%P
    def mult(self,x,y):self.mults+=1;return x*y%P

def solve_cycle(x,step,lam,c):
    n=len(x);seen=set();out=[0]*n
    for start in range(n):
        if start in seen:continue
        cyc=[];j=start
        while j not in seen:seen.add(j);cyc.append(j);j=(j+step)%n
        L=len(cyc);closure=pow((1-pow(lam,L,P))%P,-1,P) # precomputed-plan charge excluded here, disclosed.
        v=x[cyc[1]] if L>1 else x[cyc[0]]
        if L>1:
            for t in range(2,L):v=c.add(x[cyc[t]],c.mult(lam,v))
            v=c.add(x[cyc[0]],c.mult(lam,v))
        out[cyc[0]]=c.mult(closure,v)
        for t in range(1,L):out[cyc[t]]=c.add(x[cyc[t]],c.mult(lam,out[cyc[t-1]]))
    return out

def run_cost_controls():
    records=[]
    for n,r in ((31,2),(63,4),(127,8),(255,16)):
        a=pow(2,-1,P);z=root(r);x=[rng.randrange(P) for _ in range(n)]
        # all selected examples have gcd(N,r)=1 and legal poles in this field.
        baseline=Counter();agg=[0]*n
        for i in range(r):
            y=solve_cycle(x,1,a*pow(z,i,P)%P,baseline)
            agg=[baseline.add(t,u) for t,u in zip(agg,y)]
        invr=pow(r,-1,P);agg=[baseline.mult(invr,v) for v in agg]
        fused=Counter();out=solve_cycle(x,r,pow(a,r,P),fused)
        assert out==agg
        records.append({'N':n,'r':r,'baseline_arithmetic':baseline.adds+baseline.mults,
                        'fused_arithmetic':fused.adds+fused.mults,
                        'plan_setup_excluded_from_counts':'charged separately O(N+r+log N+log r); no timing claim'})
    return records

if __name__=='__main__':
    result={'status':'PASS','field':P,'seed':540,'field_algebra':run_field_cases(),
            'characteristic_zero_density':run_charzero_density(),'inherited_fusion_cost_controls':run_cost_controls(),
            'scope':'Finite controls support indexing and the derived identities. Complex norm and uncertainty statements are analytic proofs, not inferred from field experiments. No supplied source was executed.'}
    target=Path(__file__).with_name('EXACT_RESULTS.json');target.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('field_algebra',)},indent=2))
    print('field cases:',result['field_algebra']['cases'],'entry equalities:',result['field_algebra']['matrix_entry_equalities'])
