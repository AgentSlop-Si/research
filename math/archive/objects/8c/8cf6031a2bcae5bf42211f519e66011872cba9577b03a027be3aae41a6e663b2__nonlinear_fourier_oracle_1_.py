"""Exact complex rank of selected DFT submatrices with periodic universal columns.

N=2**k, period h|N, E subset {0,...,h-1} a universal Fourier
sampling set of cardinality m. C=E+h*{0,...,N/h-1}.
Then rank_C(F_N[R,C])=sum_{rho=0}^{N/h-1} min(|{r in R:r% (N/h)==rho}|,m).

Any E that is a complete set of residues modulo h/2 (h=2m) is
universal when h is a power of two. In particular, parity sets whose
most significant mask bit is log2(h)-1 satisfy this hypothesis.

The universal sampling-set fact is imported from Osgood et al (2012).
All rank conclusions here are over C and use no finite-field heuristic.
"""
from __future__ import annotations
import numpy as np


def rank_periodic_universal(n: int, period: int, e_size: int, rows) -> int:
    if n <= 0 or n & (n-1) or period <= 0 or period & (period-1) or n % period:
        raise ValueError('n and period must be powers of two, with period dividing n')
    if not 1 <= e_size <= period:
        raise ValueError('bad universal residue-set cardinality')
    R = np.asarray(list(rows), dtype=np.int64)
    if len(R) and (R.min()<0 or R.max()>=n):
        raise ValueError('row index out of range')
    if len(np.unique(R))!=len(R):
        raise ValueError('duplicate row indices')
    d=n//period
    return int(np.minimum(np.bincount(R%d, minlength=d),e_size).sum())


def rank_parity_columns(k: int, input_mask: int, rows) -> int:
    n=1<<k
    if not 0<input_mask<n:
        raise ValueError('nonzero k-bit parity mask required')
    h=1<<input_mask.bit_length()
    return rank_periodic_universal(n,h,h//2,rows)


def parity_columns(k: int,mask: int,sign=0):
    n=1<<k
    if not 0<mask<n:raise ValueError('bad parity mask')
    return [i for i in range(n) if ((i&mask).bit_count()&1)==sign]


def transversal_columns(n: int,period: int,flags):
    """Pick E={a+flags[a]*(period/2):0<=a<period/2}, repeat with period."""
    m=period//2
    if len(flags)!=m or any(v not in (0,1,False,True) for v in flags):
        raise ValueError('flags must be 0/1, length period/2')
    E=[i+(m if flags[i] else 0) for i in range(m)]
    return [e+period*j for j in range(n//period) for e in E]


def boundary_indicator(group)->int:
    g=np.asarray(group,dtype=np.bool_)
    return int(np.count_nonzero(g[:-1]!=g[1:]))


def moving_partition_certificate(k:int,shuffles:list,ranks:list,input_mask:int):
    n=1<<k
    if len(ranks)!=len(shuffles)+1:raise ValueError('wrong number of stage ranks')
    for p in shuffles:
        if len(p)!=n or len(set(map(int,p)))!=n or min(p)<0 or max(p)>=n:
            raise ValueError('not a permutation')
    x=np.arange(n,dtype=np.int64)
    group=np.array([((int(z)&input_mask).bit_count()&1)==0 for z in x],dtype=np.bool_)
    costs=[]
    for j,rank in enumerate(ranks):
        costs.append(rank*boundary_indicator(group))
        if j<len(shuffles):group=group[np.asarray(shuffles[j],dtype=np.int64)]
    rows=np.flatnonzero(~group).tolist()
    required=rank_parity_columns(k,input_mask,rows)
    return {'N':n,'input_mask':input_mask,'output_rows':rows,
            'stage_channel_budget':costs,'capacity_bound':sum(costs),
            'exact_complex_fourier_rank':required,
            'rank_gap':required-sum(costs)}
