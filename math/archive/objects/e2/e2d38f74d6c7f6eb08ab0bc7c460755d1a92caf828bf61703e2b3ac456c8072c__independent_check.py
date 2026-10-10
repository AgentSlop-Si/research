"""Independent audit: no imports from the factorization/search code.

Checks exact Fourier Vandermonde ranks and Green-stage structural ranks.
This does not constitute a new FFT implementation or an all-length formal proof.
"""
from __future__ import annotations
import json
from pathlib import Path


def echelon_rank(a, mod):
    a=[list(map(lambda z:z%mod,row)) for row in a]
    if not a:return 0
    m=len(a);cols=len(a[0]);pivot=0
    for col in range(cols):
        k=pivot
        while k<m and a[k][col]==0:k+=1
        if k==m:continue
        a[k],a[pivot]=a[pivot],a[k]
        inv=pow(a[pivot][col],-1,mod)
        for j in range(col,cols):a[pivot][j]=a[pivot][j]*inv%mod
        for k in range(pivot+1,m):
            mult=a[k][col]
            if mult:
                for j in range(col,cols):
                    a[k][j]=(a[k][j]-mult*a[pivot][j])%mod
        pivot+=1
        if pivot==m:break
    return pivot


def modular_inverse(x,mod):
    n=len(x)
    a=[[(v%mod) for v in row]+[int(j==i) for j in range(n)] for i,row in enumerate(x)]
    for i in range(n):
        k=next((k for k in range(i,n) if a[k][i]),None)
        if k is None:raise ValueError('not invertible')
        a[i],a[k]=a[k],a[i]
        fac=pow(a[i][i],-1,mod)
        a[i]=[v*fac%mod for v in a[i]]
        for k in range(n):
            if k!=i:
                fac=a[k][i]
                if fac:
                    a[k]=[(u-fac*v)%mod for u,v in zip(a[k],a[i])]
    return [row[n:] for row in a]


def fourier_matrix(n,mod,gen):
    root=pow(gen,(mod-1)//n,mod)
    return [[pow(root,i*j,mod) for j in range(n)] for i in range(n)]


def qsrank_independent(a,mod):
    n=len(a);v=0
    for j in range(1,n):
        v=max(v,echelon_rank([row[j:] for row in a[:j]],mod))
        v=max(v,echelon_rank([row[:j] for row in a[j:]],mod))
    return v


def green(n,mod):
    def get(t):
        mat=[[0]*n for _ in range(n)]
        for i in range(n):
            mat[i][i]=t
            if i:
                mat[i][i-1]=-1
                mat[i-1][i]=-1
        return modular_inverse(mat,mod)
    a=get(3);b=get(4)
    return [[(a[i][j]+b[i][j])%mod for j in range(n)] for i in range(n)]


def run():
    checked=[]
    for p, gen in ((998244353,3),(2013265921,31)):
        for n in (8,16,32,64,128):
            if (p-1)%n:continue
            F=fourier_matrix(n,p,gen);m=n//2
            # The analytic proof is Vandermonde, even if these rank tests pass.
            half_ranks=[echelon_rank([F[i][j:j+m] for i in range(m)],p) for j in (0,m)]
            assert half_ranks==[m,m]
            odds=list(range(1,n,2)); evens=list(range(0,n,2))
            # With only one external permutation the rank stays m.
            assert echelon_rank([[F[i][j] for j in evens] for i in range(m)],p)==m
            assert echelon_rank([[F[i][j] for j in odds] for i in range(m)],p)==m
            assert echelon_rank([F[i][:m] for i in evens],p)==m
            assert echelon_rank([F[i][m:] for i in evens],p)==m
            if n <=32:
                S=green(n,p); qr=qsrank_independent(S,p)
                assert qr<=2,(n,p,qr)
            else: qr=None
            checked.append({'prime':p,'n':n,'full_rank_quadrants':half_ranks,
                            'separate_green_sum_qsrank':qr,'two_r2_stages_ruled_out_by_bound':n>16})
    Path(__file__).with_name('independent_results.json').write_text(json.dumps(checked,indent=2)+'\n')
    print(f'PASS independent: {len(checked)} finite-field Fourier checks')
    print(f'PASS independent: {sum(x["separate_green_sum_qsrank"] is not None for x in checked)} two-Green rank controls')
    print('PASS independent: Vandermonde half-ranks hold in both primes')
    return checked

if __name__=='__main__':run()
