"""Exact dynamic-programming search across ALL independent row/column permutations.

The DP enumerates pairs of nested prefix subsets, not (n!)**2 orders.
It minimizes max strict off-diagonal cut rank of the endpoint-permuted DFT,
which is a necessary channel count for ONE bidirectional-sum stage.

For finite-field computations, a nonzero modular minor implies that the
corresponding cyclotomic minor is nonzero over C. An ordering found modulo p
must be independently validated over a cyclotomic field before claiming a
complex-field upper bound. The n=4 and n=8 positive witnesses below can be
checked exactly in Q[z]/Phi_n(z).
"""
from __future__ import annotations
from functools import lru_cache
from itertools import combinations
from exact_scan_macro import dft_matrix, rank_mod, P, G


def _subset(mask, n):
    return [i for i in range(n) if mask >> i & 1]


def optimal_orders(n: int, p: int=P, g: int=G) -> dict:
    if n not in (2,4,8):
        raise ValueError('exhaustive two-order subset DP currently limited to n<=8')
    F=dft_matrix(n,p,g)
    full=(1<<n)-1
    states_examined=0
    ranks_computed=0
    @lru_cache(None)
    def cross_ranks(r_mask:int,c_mask:int)->tuple[int,int]:
        nonlocal ranks_computed
        ranks_computed+=1
        row0=_subset(r_mask,n)
        row1=_subset(full^r_mask,n)
        col0=_subset(c_mask,n)
        col1=_subset(full^c_mask,n)
        if not row0 or not row1: return (0,0)
        up=rank_mod([[F[i][j] for j in col1] for i in row0],p)
        down=rank_mod([[F[i][j] for j in col0] for i in row1],p)
        return (up,down)
    # state -> (minimax rank, ordered-row prefix, ordered-column prefix)
    dp={(0,0):(0,(),())}
    layer_sizes=[1]
    for size in range(1,n+1):
        new={}
        for (R,C),(cost,ro,co) in dp.items():
            rrem=full^R;crem=full^C
            for i in _subset(rrem,n):
                rr=R|(1<<i)
                for j in _subset(crem,n):
                    cc=C|(1<<j)
                    ranks=cross_ranks(rr,cc)
                    next_cost=max(cost,*ranks)
                    key=(rr,cc)
                    current=new.get(key)
                    # Deterministic lexicographic tie-break: reproducibility.
                    if current is None or (next_cost,(ro+(i,),co+(j,))) < (current[0],(current[1],current[2])):
                        new[key]=(next_cost,ro+(i,),co+(j,))
        dp=new
        states_examined+=len(dp)
        layer_sizes.append(len(dp))
    optimum,row_order,col_order=dp[(full,full)]
    return {'n':n,'p':p,'optimum':optimum,'row_order':row_order,'col_order':col_order,
            'layer_state_counts':layer_sizes,'states_examined':states_examined,
            'ranks_computed':ranks_computed}


if __name__=='__main__':
    import json
    for n in (2,4,8):
        d=optimal_orders(n)
        print(json.dumps(d))
