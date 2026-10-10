"""Exact, fully finite-field cut-rank audit for global O(N)-work scan stages.

The proof is mathematical; this file checks representative finite matrices.
No FFT outputs or intermediate convolution are cached, and there are no threads.
"""
from __future__ import annotations

from itertools import combinations
import random

P = 998244353
G = 3


def dft(n: int, p: int = P, primitive_root: int = G) -> list[list[int]]:
    if n < 2 or n & (n-1) or (p-1)%n:
        raise ValueError('n must be a supported power of two >=2')
    omega = pow(primitive_root, (p-1)//n, p)
    return [[pow(omega, i*j, p) for j in range(n)] for i in range(n)]


def rank(rows: list[list[int]], p: int = P) -> int:
    if not rows:
        return 0
    w = len(rows[0])
    if any(len(row) != w for row in rows):
        raise ValueError('matrix is not rectangular')
    a = [[int(v)%p for v in row] for row in rows]
    h=len(a); r=0
    for c in range(w):
        pivot = next((i for i in range(r,h) if a[i][c]), None)
        if pivot is None: continue
        a[r], a[pivot] = a[pivot], a[r]
        inv = pow(a[r][c],-1,p)
        for j in range(c,w):
            a[r][j] = a[r][j]*inv%p
        for i in range(r+1,h):
            f=a[i][c]
            if f:
                for j in range(c,w):
                    a[i][j]=(a[i][j]-f*a[r][j])%p
        r+=1
        if r==h: break
    return r


def offdiag_ranks(a:list[list[int]], cut:int, p:int=P) -> tuple[int,int]:
    n=len(a)
    if not 0<cut<n or any(len(row)!=n for row in a):
        raise ValueError('square matrix with nontrivial cut required')
    upper=rank([row[cut:] for row in a[:cut]],p)
    lower=rank([row[:cut] for row in a[cut:]],p)
    return upper,lower


def diag(values:list[int],p:int=P)->list[list[int]]:
    n=len(values)
    return [[values[i]%p if i==j else 0 for j in range(n)] for i in range(n)]


def forward(a:list[int],b:list[int],p:int=P)->list[list[int]]:
    """y[0]=b0*x0, y[i]=a[i]*y[i-1]+b[i]*x[i]."""
    n=len(a)
    if len(b)!=n: raise ValueError('coefficient mismatch')
    out=[[0]*n for _ in range(n)]
    for i in range(n):
        if i:
            out[i]=[(a[i]*t)%p for t in out[i-1]]
        out[i][i]=b[i]%p
    return out


def backward(a:list[int],b:list[int],p:int=P)->list[list[int]]:
    """y[n-1]=b[n-1]*x[n-1], y[i]=a[i]*y[i+1]+b[i]*x[i]."""
    n=len(a)
    if len(b)!=n: raise ValueError('coefficient mismatch')
    out=[[0]*n for _ in range(n)]
    for i in range(n-1,-1,-1):
        if i<n-1:
            out[i]=[(a[i]*t)%p for t in out[i+1]]
        out[i][i]=b[i]%p
    return out


def matmul(a:list[list[int]],b:list[list[int]],p:int=P)->list[list[int]]:
    if len(a)!=len(b) or any(len(row)!=len(a) for row in a+b):
        raise ValueError('square equal-size matrices required')
    n=len(a)
    out=[[0]*n for _ in range(n)]
    for i in range(n):
        for k,v in enumerate(a[i]):
            if v:
                for j,w in enumerate(b[k]):
                    out[i][j]=(out[i][j]+v*w)%p
    return out


def permute(a:list[list[int]],row_order:list[int],col_order:list[int]) -> list[list[int]]:
    n=len(a)
    if sorted(row_order)!=list(range(n)) or sorted(col_order)!=list(range(n)):
        raise ValueError('permutations required')
    return [[a[i][j] for j in col_order] for i in row_order]


def bit_reverse_order(n:int)->list[int]:
    if n<2 or n&(n-1):raise ValueError('power of two required')
    k=n.bit_length()-1
    return [int(f'{i:0{k}b}'[::-1],2) for i in range(n)]


def gray_order(n:int)->list[int]:
    if n<2 or n&(n-1):raise ValueError('power of two required')
    return [i^(i>>1) for i in range(n)]


def parity_order(n:int)->list[int]:
    return list(range(0,n,2))+list(range(1,n,2))


def crossing_count(order:list[int],cut:int)->int:
    n=len(order)
    if sorted(order)!=list(range(n)):raise ValueError('permutation required')
    return sum(1 for x in order[:cut] if x>=cut)


def balanced_rank_report(n:int)->dict:
    f=dft(n);cut=n//2
    orders={'natural':list(range(n)), 'bit_reverse':bit_reverse_order(n),
            'parity':parity_order(n),'gray':gray_order(n)}
    results={}
    for label,order in orders.items():
        results[label]={
            'upper_lower':offdiag_ranks(permute(f,order,order),cut),
            'permutation_cut_crossings':crossing_count(order,cut),
        }
    return {'n':n,'balanced_cut':cut,'data':results}


def exact_min_balanced_submatrix_rank(n:int)->dict:
    """Exhaust all row and column subsets of size n/2 (practical at n<=8)."""
    if n>8:raise ValueError('Exhaustive subset search limited to n<=8')
    f=dft(n);h=n//2
    best=n; witnesses=[];hist={}
    row_sets=list(combinations(range(n),h))
    for rs in row_sets:
        for cs in row_sets:
            r=rank([[f[i][j] for j in cs] for i in rs])
            hist[r]=hist.get(r,0)+1
            if r<best:
                best=r;witnesses=[{'rows':rs,'cols':cs}]
            elif r==best and len(witnesses)<3:
                witnesses.append({'rows':rs,'cols':cs})
    return {'n':n, 'submatrix_count':len(row_sets)**2,'minimum_rank':best,
            'witnesses':witnesses, 'histogram':hist}


def random_scan_compositions(n:int=10,trials:int=30,seed:int=20261009)->dict:
    rng=random.Random(seed)
    worst_violation=0
    checked=0
    for _ in range(trials):
        M=diag([rng.randint(1,20) for _ in range(n)])
        used_f=used_b=0
        for __ in range(rng.randint(1,10)):
            typ=rng.choice(['f','b','d'])
            a=[rng.randrange(1,P) for _ in range(n)]
            b=[rng.randrange(1,P) for _ in range(n)]
            if typ=='f':
                layer=forward(a,b);used_f+=1
            elif typ=='b':
                layer=backward(a,b);used_b+=1
            else:layer=diag(b)
            M=matmul(layer,M)
            for cut in range(1,n):
                upper,lower=offdiag_ranks(M,cut)
                worst_violation=max(worst_violation,upper-used_b,lower-used_f)
                assert upper<=used_b and lower<=used_f
                checked+=1
    return {'n':n,'trials':trials,'checked_cut_bounds':checked,'max_violation':worst_violation}


if __name__=='__main__':
    import json
    print(json.dumps([balanced_rank_report(n) for n in (8,16,32,64,128)],indent=2))
    print(json.dumps(exact_min_balanced_submatrix_rank(8),indent=2))
    print(json.dumps(random_scan_compositions(),indent=2))


def cut_rank_potential(a:list[list[int]],p:int=P)->int:
    """Sum of upper and lower off-diagonal ranks over all contiguous cuts."""
    return sum(sum(offdiag_ranks(a,c,p)) for c in range(1,len(a)))


def permutation_matrix(order:list[int],p:int=P)->list[list[int]]:
    n=len(order)
    if sorted(order)!=list(range(n)):raise ValueError('permutation required')
    return [[int(j==order[i]) for j in range(n)] for i in range(n)]


def footrule(order:list[int])->int:
    n=len(order)
    if sorted(order)!=list(range(n)):raise ValueError('permutation required')
    return sum(abs(i-order[i]) for i in range(n))


def multichannel(n:int,r_forward:int,r_backward:int,seed:int=10)->list[list[int]]:
    rng=random.Random(seed)
    a=diag([rng.randrange(1,P) for _ in range(n)])
    for direction,num in ((forward,r_forward),(backward,r_backward)):
        for _ in range(num):
            b=direction([rng.randrange(1,P) for _ in range(n)],[rng.randrange(1,P) for _ in range(n)])
            for i in range(n):
                for j in range(n):
                    a[i][j]=(a[i][j]+b[i][j])%P
    return a


def independent_balanced_bound_check(n:int=8)->dict:
    """Exhaustive balanced subsets at N=8, exact rank and optimality witness."""
    if n!=8:raise ValueError('designed for exhaustive N=8')
    f=dft(n)
    all_sets=list(combinations(range(n),n//2))
    nchecks=0
    worst_slack=n
    for rs in all_sets:
        for cs in all_sets:
            sub=[[f[i][j] for j in cs] for i in rs]
            r=rank(sub)
            assert r* n >= len(rs)*len(cs)
            worst_slack=min(worst_slack,r-n//4)
            nchecks+=1
    return {'pairs':nchecks,'bound':'rank >= |R||C|/N', 'min_excess_over_bound':worst_slack}
