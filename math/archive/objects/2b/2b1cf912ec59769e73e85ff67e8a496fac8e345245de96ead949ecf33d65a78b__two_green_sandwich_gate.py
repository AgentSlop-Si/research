"""Exact polynomial gate for a single sum-of-two weighted Green solvers.

G_1+G_2 == F is equivalent to A F B == A+B, for A=G_1^-1,B=G_2^-1.
This is an O(N^2) offline factorization verification, NOT a fast DFT algorithm.
"""
from __future__ import annotations
import numpy as np
from phase11_gate import P, eye, fourier, matmul, mod_rank


def sparse_inverse(pi,w):
    pi=np.asarray(pi,dtype=np.int64)
    w=np.asarray(w,dtype=np.int64)%P
    n=len(pi)
    s=eye(n)
    s[np.arange(n),pi]=(s[np.arange(n),pi]-w)%P
    return s


def four_term_residual(n,pi1,w1,pi2,w2):
    pi1=np.asarray(pi1,dtype=np.int64)
    pi2=np.asarray(pi2,dtype=np.int64)
    w1=np.asarray(w1,dtype=np.int64)%P
    w2=np.asarray(w2,dtype=np.int64)%P
    f=fourier(n)
    q=np.argsort(pi2)  # pi2[q[j]] = j
    i=np.arange(n)[:,None]
    j=np.arange(n)[None,:]
    term=(f - w1[:,None]*f[pi1,:] - w2[q][None,:]*f[:,q]
          + w1[:,None]*w2[q][None,:]*f[np.ix_(pi1,q)])%P
    a=sparse_inverse(pi1,w1);b=sparse_inverse(pi2,w2)
    return (term-a-b)%P


def assert_sandwich_equivalence(pi1,w1,pi2,w2):
    n=len(pi1)
    a=sparse_inverse(pi1,w1)
    b=sparse_inverse(pi2,w2)
    f=fourier(n)
    lhs=(matmul(matmul(a,f),b)-a-b)%P
    direct=four_term_residual(n,pi1,w1,pi2,w2)
    assert np.array_equal(lhs,direct)
    return {'n':n,'mismatches_between_equivalent_formulas':int(np.count_nonzero(lhs-direct)),
            'nonzero_sandwich_residual_entries':int(np.count_nonzero(lhs)),
            'sandwich_residual_rank':mod_rank(lhs),
            'full_equality_to_dft':bool(np.count_nonzero(lhs)==0)}

if __name__=='__main__':
    import json
    from green_sum_linear import find_weighted_escape
    for n in (4,16,64):
        x=find_weighted_escape(n)
        y=assert_sandwich_equivalence(x['permutation1'],x['weights1'],x['permutation2'],x['weights2'])
        print(json.dumps(y))
