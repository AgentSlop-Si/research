"""Two-Hamilton-path Green mixer: O(N) work, order-robust with high probability.

For N divisible by 16 and >=32, choose a uniformly random permutation p.
M = T^-1 + (1/100) P T^-1 P^T, P implementing p.

Its two path graphs have linear balanced-edge expansion with overwhelming
probability. The proof and explicit failure-probability bound appear in
EXPANDER_THEOREM.md. This is an FFT RESEARCH PRIMITIVE, NOT a DFT algorithm.
"""

from random import Random
from green_solver_standalone import tri_solve
from linear_inverse import MOD


def random_order(n,seed=20261009):
    p=list(range(n))
    Random(seed).shuffle(p)
    return p


def apply_two_path(x,order,eps=None,p=MOD):
    n=len(x)
    # The order is fixed input-independent setup; do not sort it per input.
    assert len(order)==n
    if eps is None:eps=pow(100,-1,p)
    # term one: G x
    g1=tri_solve(x,p)
    # term two: P G P^T x where P rows reorder by 'order'.
    # scatter x to original path coordinates, solve, gather.
    temp=[0]*n
    for i,j in enumerate(order):temp[j]=x[i]
    g2=tri_solve(temp,p)
    return [(g1[i]+eps*g2[order[i]])%p for i in range(n)]


def path_union_edges(order):
    n=len(order)
    inv=[0]*n
    for i,j in enumerate(order):inv[j]=i
    path1=[(i,i+1) for i in range(n-1)]
    # The edge graph of PTP^T is a path in inverse permutation order.
    path2=[(inv[i],inv[i+1]) for i in range(n-1)]
    return path1,path2


def binary_entropy(p):
    from math import log2
    if p<=0 or p>=1:return 0.0
    return -p*log2(p)-(1-p)*log2(1-p)


def union_bound_failure(n):
    """All-order balanced cut failure probability bound (two random paths)."""
    assert n%16==0 and n>=32
    return min(1.0,4*(n+1)*2**(-n*(1-2*binary_entropy(1/16))))
