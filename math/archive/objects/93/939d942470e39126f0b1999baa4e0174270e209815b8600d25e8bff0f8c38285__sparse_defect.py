"""Exact finite-field certificates for the sparse+low-rank FFT stage obstruction.

Research target: F_N and its inverse (both Fourier-character matrices).
All determinant checks are exact over a field containing a primitive N-th root.
The proofs over C are in PROOF_CERTIFICATE.md; finite-field tests are controls.

Requires only numpy.  No external solver, no caching of FFT inputs.
"""
from __future__ import annotations
import random
from dataclasses import dataclass
import numpy as np


def primitive_root(p: int) -> int:
    """Find a generator of F_p^*, for our two known field primes."""
    n = p - 1
    fs = []
    d = 2
    while d*d <= n:
        if n % d == 0:
            fs.append(d)
            while n % d == 0: n //= d
        d += 1
    if n > 1: fs.append(n)
    for g in range(2,p):
        if all(pow(g,(p-1)//d,p) != 1 for d in fs): return g
    raise ValueError('cannot find primitive root')


def root_of_unity(p: int, n: int) -> int:
    assert (p-1) % n == 0
    w = pow(primitive_root(p),(p-1)//n,p)
    assert pow(w,n,p) == 1
    for d in range(1,n):
        if n % d == 0: assert pow(w,d,p) != 1
    return w


def det_mod(M: np.ndarray,p: int) -> int:
    a = np.array(M,dtype=np.int64,copy=True) % p
    n,k = a.shape
    assert n == k
    out = 1
    for i in range(n):
        rows = np.flatnonzero(a[i:,i])
        if not len(rows): return 0
        j=i+int(rows[0])
        if i != j:
            a[[i,j]] = a[[j,i]]
            out = -out
        v=int(a[i,i]);out=out*v%p
        inv=pow(v,-1,p)
        if i+1<n:
            factors = a[i+1:,i]*inv % p
            a[i+1:,i:] = (a[i+1:,i:]-factors[:,None]*a[None,i,i:])%p
    return int(out%p)


def rank_mod(M: np.ndarray,p: int) -> int:
    a=np.array(M,dtype=np.int64,copy=True)%p
    m,n=a.shape
    row=0
    for j in range(n):
        if row==m: break
        cand=np.flatnonzero(a[row:,j])
        if not len(cand):continue
        ix=row+int(cand[0])
        if ix!=row:a[[row,ix]]=a[[ix,row]]
        inv=pow(int(a[row,j]),-1,p)
        if row+1<m:
            factors=a[row+1:,j]*inv%p
            a[row+1:,j:]=(a[row+1:,j:]-factors[:,None]*a[None,row,j:])%p
        row+=1
    return row


def fourier_mod(n:int,p:int,w:int|None=None,row_perm=None,col_perm=None)->np.ndarray:
    if w is None:w=root_of_unity(p,n)
    if row_perm is None:row_perm=list(range(n))
    if col_perm is None:col_perm=list(range(n))
    # Multiply exponents mod n *before* exponentiating to avoid overflow.
    return np.array([[pow(w,(int(row_perm[i])*int(col_perm[j]))%n,p)
                      for j in range(n)] for i in range(n)],dtype=np.int64)


@dataclass
class MinorCertificate:
    n:int
    p:int
    q:int
    m:int
    row_perm:list[int]
    col_perm:list[int]
    rows:list[int]
    cols:list[int]
    pivot_determinant:int
    vandermonde_determinant:int
    nonzero_sparse_in_chosen_block:int


def sparse_fourier_minor(n:int,q:int,p:int,seed:int=73021)->MinorCertificate:
    """Construct a Vandermonde witness for arbitrary random q-row-sparse errors.
    The minor exists for *every* B, not just the sampled one.
    """
    if not (0 <=q<n):raise ValueError('q must lie in [0,n)')
    rng=random.Random(seed+17*n+41*q+101*p)
    rows=list(range(n));cols=list(range(n));rng.shuffle(rows);rng.shuffle(cols)
    m=n//(q+1)
    assert m>=1
    B=np.zeros((n,n),dtype=np.int64)
    for i in range(n):
        ix=rng.sample(range(n),q)
        for j in ix:B[i,j]=rng.randrange(1,p)
    # Reorder selected rows by *their original Fourier frequency*, making
    # the square submatrix exactly a Vandermonde (up to column scales).
    R=[rows.index(k) for k in range(m)]
    forbidden={j for i in R for j in np.flatnonzero(B[i,:])}
    C=[j for j in range(n) if j not in forbidden][:m]
    assert len(C)==m and not np.any(B[np.ix_(R,C)])
    w=root_of_unity(p,n)
    F=fourier_mod(n,p,w,rows,cols)
    det=det_mod((F-B)[np.ix_(R,C)],p)
    xs=[pow(w,cols[j],p) for j in C]
    vd=1
    for v in range(len(xs)):
        for u in range(v):vd=(vd*(xs[v]-xs[u]))%p
    assert det==vd and det!=0,(n,q,p,det,vd)
    return MinorCertificate(n,p,q,m,rows,cols,R,C,det,vd,0)


def sparse_matrix(n:int,s:int,p:int,rng:random.Random):
    M=np.zeros((n,n),dtype=np.int64)
    for i in range(n):
        chosen={i}
        while len(chosen)<s:chosen.add(rng.randrange(n))
        for j in chosen:M[i,j]=rng.randrange(1,p)
    return M


def check_telescoping(n:int,t:int,s:int,r:int,p:int,seed:int=1197):
    rng=random.Random(seed+7*n+13*t+11*r+p)
    base=[sparse_matrix(n,s,p,rng) for _ in range(t)]
    corrections=[]
    for _ in range(t):
        U=np.array([[rng.randrange(p) for _ in range(r)] for _ in range(n)],dtype=np.int64)
        V=np.array([[rng.randrange(p) for _ in range(r)] for _ in range(n)],dtype=np.int64)
        corrections.append(U@V.T%p)
    perms=[]
    for _ in range(t-1):
        pp=list(range(n));rng.shuffle(pp);perms.append(pp)
    def product(stages):
        z=stages[0].copy()
        for j in range(1,t):z=(stages[j]@z[perms[j-1],:])%p
        return z
    target=product([(x+y)%p for x,y in zip(base,corrections)])
    sparse=product(base)
    rankdiff=rank_mod((target-sparse)%p,p)
    assert rankdiff<=t*r
    rowsparsity=max(int(np.count_nonzero(sparse[i])) for i in range(n))
    assert rowsparsity<=s**t
    return {'n':n,'t':t,'s':s,'r':r,'p':p,'rank_difference':rankdiff,
            'rank_budget':t*r,'max_sparse_base_row_support':rowsparsity,
            'support_budget':s**t}


def minimal_depth(n:int,s:int,r:int)->int:
    """Smallest depth not rejected by this NECESSARY condition."""
    for t in range(n+5):
        if t==0: continue
        if t*r >= n//(s**t+1):return t
    raise AssertionError('loop should terminate')


if __name__=='__main__':
    import json
    for p in (12289,65537):
        for n in (8,16,32,64,128):
            for q in (0,1,2,3):
                c=sparse_fourier_minor(n,q,p)
                print('rank witness', json.dumps({'n':n,'p':p,'q':q,'rank_at_least':c.m,'det':c.pivot_determinant}))
    print('depths',[(n,minimal_depth(n,3,1),minimal_depth(n,3,2)) for n in (16,64,256,1024,65536)])
