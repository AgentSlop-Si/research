"""Independent exact controls. Does not import or run any author/historical script."""
from fractions import Fraction
from math import comb
from random import Random
import json
from pathlib import Path


def choose(n,k):
    return comb(n,k) if 0 <= k <= n else 0


def shift_coeff(f):
    g=[0]*(len(f)+1)
    for j,x in enumerate(f):
        g[j]+=x
        g[j+1]+=x
    return g


def pack(f,p,K,s):
    a=list(f)+[0]*(K-len(f))
    assert len(a)==K
    return [sum(a[r*s+t]*p**t for t in range(s)) for r in range(K//s)]


def rank(rows):
    a=[[Fraction(x) for x in row] for row in rows]
    n=len(a[0]) if a else 0
    r=0
    for c in range(n):
        piv=next((i for i in range(r,len(a)) if a[i][c]),None)
        if piv is None: continue
        a[r],a[piv]=a[piv],a[r]
        v=a[r][c]
        a[r]=[x/v for x in a[r]]
        for i in range(r+1,len(a)):
            v=a[i][c]
            if v: a[i]=[x-v*y for x,y in zip(a[i],a[r])]
        r+=1
        if r==len(a): break
    return r


def lookahead_matrix(K,s,p,h):
    columns=[]
    for i in range(K-h):
        f=[0]*i+[1]
        out=[]
        for j in range(h+1):
            out.extend(pack(f,p,K,s))
            f=shift_coeff(f)
        columns.append(out)
    return list(map(list,zip(*columns)))


def minimal_state(f,p,K,s):
    a=list(f)+[0]*(K-len(f))
    return a[:K-s]+[sum(a[K-s+t]*p**t for t in range(s))]


def next_minimal_state(v,p,K,s):
    q=K-s
    if q==0: return [(p+1)*v[0]]
    return [v[0]]+[v[j]+v[j-1] for j in range(1,q)]+[(p+1)*v[q]+v[q-1]]


def state_readout(v,p,K,s):
    q=K-s
    return [sum(v[r*s+t]*p**t for t in range(s)) for r in range(K//s-1)]+[v[q]]


def row_oracle(i,r,s,p):
    return sum(choose(i,r*s+t)*p**t for t in range(s))


def window_recurrence_checks(K,s,p):
    B=K//s
    row=[1]+[0]*(B-1)
    for i in range(K):
        assert row==[row_oracle(i,r,s,p) for r in range(B)]
        if i+1<K:
            row=[(p+1)*row[r]+choose(i,r*s-1)-p**s*choose(i,(r+1)*s-1) for r in range(B)]
    return K*B


def run():
    rng=Random(12479)
    counts=dict(rank_cases=0,state_cases=0,row_values=0)
    for K in range(1,19):
        for s in range(1,K+1):
            if K%s: continue
            for p in (1,3,7,15):
                counts['row_values']+=window_recurrence_checks(K,s,p)
                for h in range(s):
                    got=rank(lookahead_matrix(K,s,p,h))
                    want=K//s+(K//s-1)*h
                    assert got==want,(K,s,p,h,got,want)
                    counts['rank_cases']+=1
                for _ in range(12):
                    f=[rng.randrange(-100,101) for _ in range(K-1)]
                    v=minimal_state(f,p,K,s)
                    vf=minimal_state(shift_coeff(f),p,K,s)
                    assert next_minimal_state(v,p,K,s)==vf,(K,s,p,f)
                    assert state_readout(v,p,K,s)==pack(f,p,K,s)
                    counts['state_cases']+=1
    return counts

# Producer and product controls are deliberately implemented here independently
# after the initial algebraic controls. The author script is never imported.
def scaled_step(v,i,j,seed):
    if j<0: return 0,0
    if i+1<j: return 0,0
    if i+1==j: return seed,0
    numerator=v*(i+1)
    q,rem=divmod(numerator,i+1-j)
    assert rem==0
    return q,numerator


def independent_producer(a,m,s,counts,force_scalar=False):
    K=len(a); p=(1<<m)-1; B=K//s
    H=m*s+K+1; L=K.bit_length(); G=H+m+L+3
    assert 2**(L-1) < K+1 <= 2**L
    if s==K and not force_scalar:
        counts['scalar_copy_cases']+=1
        return [sum(x<<(m*i) for i,x in enumerate(a))]
    R=1
    for j in range(1,s+1):
        temp=R<<m
        assert temp.bit_length()<=m*j+1
        R=temp-R
        assert R.bit_length()<=m*j
    assert R==p**s
    out=[]
    for r in range(B):
        w=int(r==0)
        jlo=r*s-1; jhi=(r+1)*s-1
        lo=int(jlo==0); hi=R*int(jhi==0)
        u=0
        for i,ai in enumerate(a):
            assert w==row_oracle(i,r,s,p)
            assert lo==choose(i,jlo)
            assert hi==R*choose(i,jhi)
            counts['producer_rows']+=1
            # Standard shift/add multiplication with exactly m rounds.
            prod=0
            for bit in range(m):
                term=w<<bit
                assert term.bit_length()<=G
                if (ai>>bit)&1: prod+=term
                assert prod.bit_length()<=G
            assert prod==ai*w and prod.bit_length()<=H
            u+=prod
            assert u.bit_length()<=H
            if i<K-1:
                shifted=w<<m
                presub=shifted+lo
                assert shifted.bit_length()<=G and presub.bit_length()<=G
                w=presub-hi
                assert w>=0 and w.bit_length()<=G
                lo,nlo=scaled_step(lo,i,jlo,1)
                hi,nhi=scaled_step(hi,i,jhi,R)
                assert nlo.bit_length()<=G and nhi.bit_length()<=G
                assert lo.bit_length()<=G and hi.bit_length()<=G
                counts['exact_ratio_updates']+=int(i>=jlo>=0)+int(i>=jhi>=0)
        out.append(u)
    return out


def direct_oracle(a,m,s):
    K=len(a); p=(1<<m)-1
    c=[sum(choose(i,j)*a[i] for i in range(j,K)) for j in range(K)]
    return pack(c,p,K,s)


def run_producer():
    from itertools import product
    rng=Random(487151)
    counts=dict(producer_cases=0,producer_rows=0,exact_ratio_updates=0,scalar_copy_cases=0,matrix_cases=0)
    cases=[]
    for K in range(1,4):
        for s in range(1,K+1):
            if K%s==0:
                for a in product(range(4),repeat=K): cases.append((a,2,s))
    for K in list(range(1,25))+[31,32,47,48]:
        for s in range(1,K+1):
            if K%s: continue
            for m in (2,3,4,7,13,31):
                p=(1<<m)-1
                variants=[[0]*K,[p]*K,[p*(i%2) for i in range(K)], [rng.randrange(p+1) for i in range(K)]]
                cases.extend((a,m,s) for a in variants)
    for a,m,s in cases:
        K=len(a); p=(1<<m)-1
        got=independent_producer(a,m,s,counts)
        want=direct_oracle(a,m,s)
        assert got==want,(a,m,s,got,want)
        assert sum(x*p**(r*s) for r,x in enumerate(got))==sum(x<<(m*i) for i,x in enumerate(a))
        # Also check the endpoint recurrence mathematically, though the declared
        # algorithm uses a cheap direct-copy branch there.
        if s==K: assert independent_producer(a,m,s,counts,True)==want
        counts['producer_cases']+=1
    for d in (1,2,3):
        for M in (2,3,4):
            K=d*M*M; s=d*M
            for m in (2,3,4,7):
                p=(1<<m)-1; N=m*K; H=m*s+K+1
                for maximum in (False,True):
                    a=[p]*K if maximum else [rng.randrange(p+1) for _ in range(K)]
                    b=[p]*K if maximum else [rng.randrange(p+1) for _ in range(K)]
                    u=independent_producer(a,m,s,counts)
                    v=independent_producer(b,m,s,counts)
                    diag=[sum(u[i]*v[j] for i in range(M) for j in range(M) if i+j==k) for k in range(2*M-1)]
                    assert all(x.bit_length()<=2*H+(M-1).bit_length()+1 for x in diag)
                    ans=0
                    for x in reversed(diag):
                        for _ in range(s):
                            temp=ans<<m
                            assert temp.bit_length()<=2*N+1
                            ans=temp-ans
                            assert ans.bit_length()<=2*N
                        ans+=x
                        assert ans.bit_length()<=2*N
                    X=sum(x<<(m*i) for i,x in enumerate(a))
                    Y=sum(x<<(m*i) for i,x in enumerate(b))
                    assert ans==X*Y
                    counts['matrix_cases']+=1
    return counts

if __name__=='__main__':
    initial=run()
    initial.update(run_producer())
    Path(__file__).with_name('INDEPENDENT_RESULTS.json').write_text(json.dumps(initial,indent=2)+'\n')
    print(json.dumps(initial,indent=2))
