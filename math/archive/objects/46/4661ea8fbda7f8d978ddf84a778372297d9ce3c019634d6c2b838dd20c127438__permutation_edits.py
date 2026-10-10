"""Exact rank-distance robustness for arbitrary nonlinear index shuffles."""
from __future__ import annotations
from itertools import combinations
import numpy as np


def affine_from_columns(columns, offset=0):
    k=len(columns); n=1<<k
    p=np.empty(n,dtype=np.int64);p[0]=offset
    for x in range(1,n):
        lsb=x&-x
        p[x]=int(p[x^lsb])^int(columns[lsb.bit_length()-1])
    if len(np.unique(p))!=n:raise ValueError('GF2 columns not invertible')
    return p


def mcnot_permutation(k,controls,target):
    if target in controls or any(c<0 or c>=k for c in controls) or not 0<=target<k or len(set(controls))!=len(controls):
        raise ValueError('invalid controls/target')
    n=1<<k; mask=sum(1<<c for c in controls)
    return np.fromiter((x ^ ((1<<target) if (x&mask)==mask else 0) for x in range(n)),dtype=np.int64)


def rank_permutation_difference(p,a):
    """Exact rank_C(P-A) = N - #(cycles in A^{-1}∘P), no matrices."""
    p=np.asarray(p,dtype=np.int64);a=np.asarray(a,dtype=np.int64)
    n=len(p)
    if len(a)!=n or sorted(p.tolist())!=list(range(n)) or sorted(a.tolist())!=list(range(n)):
        raise ValueError('inputs must be permutations of equal length')
    inv=np.empty(n,dtype=np.int64);inv[a]=np.arange(n,dtype=np.int64)
    q=inv[p];visited=np.zeros(n,dtype=np.bool_);cycles=0
    for x in range(n):
        if visited[x]:continue
        cycles+=1
        y=x
        while not visited[y]:
            visited[y]=True;y=int(q[y])
    return n-cycles


def gate_edit_rank(k, number_of_controls):
    return (1<<k)//(1<<(number_of_controls+1))


def robust_rank_limit(base_capacity:int,shuffle_edit_ranks:list[int]):
    """Telescoping subadditivity: rank(M[R,C]) <= cap(base)+sum(rank(Pj-Aj))."""
    return base_capacity+sum(shuffle_edit_ranks)
