"""Exact-field verifier and certificates for the Phase-11 Green inverse-rigidity gate.

Uses p=65537 and primitive generator 3; supports N powers of two <= 65536.
No floating-point arithmetic is used in rank, matrix products, or certificates.
This DOES NOT implement a faster arbitrary-input FFT.
"""
from __future__ import annotations
import numpy as np

P = 65537
GEN = 3


def root(n: int) -> int:
    if n < 1 or (P - 1) % n:
        raise ValueError('n must divide 65536')
    z = pow(GEN, (P-1)//n, P)
    assert pow(z,n,P)==1
    for d in (2,):
        if n > 1: assert pow(z,n//d,P)!=1
    return z


def matmul(a, b):
    """Safe for sizes used here: int64 products of <= 256 terms each <=(p-1)^2."""
    return (np.asarray(a,dtype=np.int64) @ np.asarray(b,dtype=np.int64)) % P


def eye(n):
    return np.eye(n, dtype=np.int64)


def mod_rank(a):
    """Exact Gaussian elimination over GF(65537), numpy vectorized."""
    x=np.array(a,dtype=np.int64,copy=True)%P
    n,m=x.shape
    piv=0
    for c in range(m):
        if piv==n: break
        hits=np.flatnonzero(x[piv:,c])
        if len(hits)==0: continue
        idx=piv+int(hits[0])
        if idx!=piv:
            x[[piv,idx]]=x[[idx,piv]]
        x[piv]=(x[piv]*pow(int(x[piv,c]),-1,P))%P
        if piv+1<n:
            f=x[piv+1:,c].copy()
            x[piv+1:]=(x[piv+1:]-f[:,None]*x[piv][None,:])%P
        piv+=1
    return piv


def mod_inverse(a):
    a=np.asarray(a,dtype=np.int64)%P
    n=a.shape[0]
    assert a.shape==(n,n)
    x=np.concatenate([a,eye(n)],axis=1)
    for c in range(n):
        hits=np.flatnonzero(x[c:,c])
        if not len(hits): raise ValueError('singular matrix')
        idx=c+int(hits[0])
        if idx!=c: x[[idx,c]]=x[[c,idx]]
        x[c]=(x[c]*pow(int(x[c,c]),-1,P))%P
        piv=x[c].copy()
        f=x[:,c].copy(); f[c]=0
        x=(x-f[:,None]*piv[None,:])%P
    inv=x[:,n:]
    assert np.array_equal(matmul(inv,a),eye(n))
    return inv


def fourier(n, inverse=False):
    z=root(n)
    if inverse: z=pow(z,-1,P)
    inds=np.arange(n,dtype=np.int64)
    expo=(inds[:,None]*inds[None,:])%n
    powers=np.empty(n,dtype=np.int64); powers[0]=1
    for k in range(1,n): powers[k]=powers[k-1]*z%P
    out=powers[expo]
    if inverse: out=out*pow(n,-1,P)%P
    return out


def random_row_sparse(n,s,rng):
    x=np.zeros((n,n),dtype=np.int64)
    for i in range(n):
        cols=rng.choice(n,size=min(s,n),replace=False)
        x[i,cols]=rng.integers(1,P,size=len(cols),dtype=np.int64)
    return x


def rank_witness(target, sparse, original_row_order=None):
    """Construct a nonzero Fourier Vandermonde minor after removing row-sparse edits.

    target: F_N^{-1}, possibly with rows and columns independently permuted.
    original_row_order: original Fourier row indices at each target row position.
    """
    n=target.shape[0]
    s=int(np.count_nonzero(sparse,axis=1).max())
    m=n//(s+1)
    if m==0: return {'m':0,'s':s,'rows':[],'cols':[],'minor_rank':0}
    if original_row_order is None:
        rows=list(range(m))
    else:
        lookup={int(j):i for i,j in enumerate(original_row_order)}
        rows=[lookup[j] for j in range(m)]
    forbidden=np.any(sparse[rows,:]!=0,axis=0)
    good=np.flatnonzero(~forbidden)
    assert len(good)>=m
    cols=list(map(int,good[:m]))
    selected=(target-sparse)[np.ix_(rows,cols)]%P
    selected_orig=target[np.ix_(rows,cols)]
    assert np.array_equal(selected,selected_orig)
    minor_rank=mod_rank(selected)
    assert minor_rank==m
    return {'m':m,'s':s,'rows':rows,'cols':cols,'minor_rank':minor_rank}


def green_inverse_sparse(n, rng, weight=3):
    """S=I-weight*P where P is a random permutation; exactly <=2 entries/row."""
    pi=rng.permutation(n)
    x=eye(n)
    x[np.arange(n),pi]=(x[np.arange(n),pi]-weight)%P
    assert np.count_nonzero(x,axis=1).max()<=2
    # As 3 has multiplicative order 65536, cycles shorter than 65536 remain invertible.
    return x


def factor_audit(n,L,d=2,rank_per_layer=1,seed=0):
    assert d==2
    rng=np.random.default_rng(seed)
    ss=[]; aas=[]
    for i in range(L):
        s=green_inverse_sparse(n,rng)
        if rank_per_layer:
            u=rng.integers(0,P,size=(n,rank_per_layer),dtype=np.int64)
            v=rng.integers(0,P,size=(rank_per_layer,n),dtype=np.int64)
            e=matmul(u,v)
        else: e=np.zeros((n,n),dtype=np.int64)
        a=(s+e)%P
        ss.append(s); aas.append(a)
    sparse=eye(n); full=eye(n)
    for s,a in zip(ss,aas):
        sparse=matmul(sparse,s)
        full=matmul(full,a)
    supp=int(np.count_nonzero(sparse,axis=1).max())
    lowrank=mod_rank((full-sparse)%P)
    assert supp<=d**L and lowrank<=L*rank_per_layer
    target=fourier(n,inverse=True)
    # Certificates are valid for arbitrary sparse perturbation, not just sampled factorization.
    cert=rank_witness(target,sparse)
    excluded=(d**L+1)*(L*rank_per_layer+1)<=n
    if excluded:
        assert cert['minor_rank']>L*rank_per_layer
        assert not np.array_equal(target,full)
    return {'n':n,'L':L,'d':d,'r_per_layer':rank_per_layer,'max_sparse_row':supp,
            'correction_rank':lowrank,'minor_rank':cert['minor_rank'],
            'forbidden_by_theorem':excluded,'n_greater_than_gate': n>= (d**L+1)*(L*rank_per_layer+1)}


def matrix_realignment(x,a,b):
    """Use row=((input left),(output left)), col=((input right),(output right))."""
    z=np.asarray(x,dtype=np.int64)
    return np.array([[z[c*b+d, i*b+j] for j in range(b) for d in range(b)]
                     for i in range(a) for c in range(a)],dtype=np.int64)


def swap_permutation(a):
    n=a*a
    z=np.zeros((n,n),dtype=np.int64)
    for i in range(a):
        for j in range(a):
            z[j*a+i,i*a+j]=1
    return z


def green_sum_escape(n,seed=0,max_trials=50):
    """Construct an O(N)-applicable sum of two Green solvers with generically dense inverse.

    Not a Fourier factorization: just demonstrates that our inverse-sparsity
    gate DOES NOT cover sums of independently permuted Green operators.
    """
    rng=np.random.default_rng(seed)
    for it in range(max_trials):
        s1=green_inverse_sparse(n,rng,weight=3)
        s2=green_inverse_sparse(n,rng,weight=5)
        try:
            g1=mod_inverse(s1); g2=mod_inverse(s2)
            total=(g1+g2)%P
            inv=mod_inverse(total)
        except ValueError:
            continue
        nnz=np.count_nonzero(inv,axis=1)
        if int(nnz.min())==n:
            assert np.array_equal(matmul(inv,total),eye(n))
            return {'n':n,'trials':it+1,'inverse_nnz_per_row':list(map(int,nnz)),
                    'green1_inverse_row_degree':int(np.count_nonzero(s1,axis=1).max()),
                    'green2_inverse_row_degree':int(np.count_nonzero(s2,axis=1).max())}
    return {'n':n,'failure_to_find_dense_inverse':True}
