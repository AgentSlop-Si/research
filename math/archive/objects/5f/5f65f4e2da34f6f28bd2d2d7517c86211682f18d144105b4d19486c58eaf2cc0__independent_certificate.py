"""An independent modular audit; does not import the proposed scan/rank engine.
The general complex-number theorem is separately proved in RESEARCH.md.
"""
from itertools import combinations
import json
import random


def elimination(matrix, prime):
    if not matrix: return 0
    m=[row[:] for row in matrix]
    h=len(m);w=len(m[0]);r=0
    for j in range(w):
        pivot=-1
        for i in range(r,h):
            if m[i][j] %prime:
                pivot=i;break
        if pivot<0:continue
        m[r],m[pivot]=m[pivot],m[r]
        inv=pow(m[r][j],prime-2,prime)
        for i in range(r+1,h):
            f=(m[i][j]*inv)%prime
            if f:
                for k in range(j,w):
                    m[i][k]=(m[i][k]-f*m[r][k])%prime
        r+=1
        if r==h:break
    return r


def fourier(n,p,g):
    w=pow(g,(p-1)//n,p)
    assert pow(w,n,p)==1 and pow(w,n//2,p)!=1
    return [[pow(w,i*j,p) for j in range(n)] for i in range(n)]


def run():
    cases=[]
    for p,g in ((998244353,3),(2013265921,31)):
        for n in (8,16,32,64):
            f=fourier(n,p,g);h=n//2
            natural=elimination([row[h:] for row in f[:h]],p)
            order=list(range(0,n,2))+list(range(1,n,2))
            parity=elimination([[f[i][j] for j in order[h:]] for i in order[:h]],p)
            assert natural==h and parity==h//2
            rec={'modulus':p,'length':n,'natural_rank':natural,'parity_rank':parity}
            if n==8:
                subsets=list(combinations(range(n),h))
                rmin=n; histogram={}
                for row_indices in subsets:
                    for col_indices in subsets:
                        rr=elimination([[f[i][j] for j in col_indices] for i in row_indices],p)
                        assert rr>=n//4
                        histogram[rr]=histogram.get(rr,0)+1
                        rmin=min(rr,rmin)
                assert sum(histogram.values())==4900
                rec['exhaustive_submatrices']=4900
                rec['minimum_exhaustive_rank']=rmin
                rec['exhaustive_histogram']=histogram
            else:
                rng=random.Random(2026+n)
                for _ in range(45):
                    rows=rng.sample(range(n),h)
                    cols=rng.sample(range(n),h)
                    rr=elimination([[f[i][j] for j in cols] for i in rows],p)
                    assert rr>=n//4
                rec['random_submatrices_tested']=45
            cases.append(rec)
    return {'cases':cases,'verdict':'all exact checks passed','proof':'RESEARCH.md (complex Frobenius-operator norm inequality)'}

if __name__=='__main__':
    result=run()
    print(json.dumps(result,indent=2))
