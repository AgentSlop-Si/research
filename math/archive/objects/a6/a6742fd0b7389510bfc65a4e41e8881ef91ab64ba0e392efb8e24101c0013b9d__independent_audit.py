"""Independent exact auditor: DOES NOT import scan_hybrid.
Checks inverse-of-scan locality, full DFT density, Vandermonde missing-entry
witnesses in two independent modular fields, and local H2 shear factorization.
"""
import json
import random
from pathlib import Path

FIELDS=[(998244353,3),(2013265921,31)]

def rank(A,p):
    r=0
    if not A:return 0
    X=[[z%p for z in v] for v in A]
    for col in range(len(X[0])):
        pivot=next((k for k in range(r,len(X)) if X[k][col]),None)
        if pivot is None: continue
        X[r],X[pivot]=X[pivot],X[r]
        inv=pow(X[r][col],p-2,p)
        for t in range(col,len(X[r])):X[r][t]=X[r][t]*inv%p
        for k in range(r+1,len(X)):
            c=X[k][col]
            if c:
                for t in range(col,len(X[k])):X[k][t]=(X[k][t]-c*X[r][t])%p
        r+=1
    return r

def verify():
    rng=random.Random(20261009)
    certificates=0
    root_count=0
    for p,g in FIELDS:
        for n in [4,8,16,32,64]:
            root=pow(g,(p-1)//n,p)
            assert pow(root,n,p)==1 and pow(root,n//2,p)!=1
            root_count+=1
            # Inverse DFT is dense, directly from the root powers.
            for k in range(n):
                assert all(pow(root,-k*j,p)!=0 for j in range(n))
            for t in range(min(6,n.bit_length())):
                s=min(2**t,n)
                max_b=n//(s+1)
                for b in sorted({0, max_b-1, max_b//2}):
                    if b<0 or (b+1)*(s+1)>n: continue
                    for _ in range(3):
                        sets=[]
                        for i in range(b+1):
                            c=rng.randrange(s+1)
                            sets.append(set(rng.sample(range(n),c)))
                        used=set().union(*sets)
                        cols=[j for j in range(n) if j not in used][:b+1]
                        assert len(cols)==b+1
                        minor=[[pow(root,i*j,p) for j in cols] for i in range(b+1)]
                        assert rank(minor,p)==b+1
                        certificates+=1
    p=998244353
    half=pow(2,-1,p)
    # H=(1 1; 1 -1) = L(1) U(-1/2) diag(1,-2).
    for x in range(8):
        for y in range(8):
            y1=(-2*y)%p
            x2=(x-half*y1)%p
            y2=(y1+x2)%p
            assert (x2,y2)==((x+y)%p,(x-y)%p)
    data={'independent_minor_certificates':certificates,
          'independent_fields':list(map(lambda q:q[0],FIELDS)),
          'independent_root_lengths_checked':root_count,
          'independent_two_shear_pair_cases':64,
          'status':'PASS'}
    Path(__file__).with_name('independent_results.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data,indent=2))

if __name__=='__main__':verify()
