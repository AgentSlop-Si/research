"""Exact tests of multicut rank accounting with free vs nonfree permutations.
All rank operations are exact over 998244353.
"""
from __future__ import annotations
import random
from wide_scan import (dft, bit_reverse_order, parity_order, gray_order,
                       forward, backward, diag, rank, offdiag_ranks,
                       matmul, permutation_matrix, permute,
                       cut_rank_potential, footrule, crossing_count, P)


def cut_budget_experiment(n:int=16,trials:int=36,seed:int=101)->dict:
    rng=random.Random(seed)
    cut = n//2
    bad=0; checked=0
    for _ in range(trials):
        a=diag([1]*n)
        budget_up=budget_lo=0
        for i in range(8):
            kind=rng.choice(('forward','backward','permutation','diagonal'))
            if kind=='forward':
                op=forward([rng.randrange(1,20) for _ in range(n)],[rng.randrange(1,20) for _ in range(n)])
                budget_lo+=1
            elif kind=='backward':
                op=backward([rng.randrange(1,20) for _ in range(n)],[rng.randrange(1,20) for _ in range(n)])
                budget_up+=1
            elif kind=='permutation':
                order=list(range(n));rng.shuffle(order)
                op=permutation_matrix(order)
                budget_up+=crossing_count(order,cut)
                budget_lo+=crossing_count(order,cut)
            else:
                op=diag([rng.randrange(1,20) for _ in range(n)])
            a=matmul(op,a)
            up,lo=offdiag_ranks(a,cut)
            if up>budget_up or lo>budget_lo:bad+=1
            checked+=1
    assert bad==0
    rows=[]
    for n in (8,16,32,64):
        f=dft(n)
        row={'n':n,'fourier_potential':cut_rank_potential(f),'one_scan_max_potential':n-1}
        for label,order in [('bit_reverse',bit_reverse_order(n)),('parity',parity_order(n)),('gray',gray_order(n)),('reverse',list(reversed(range(n))))]:
            row[label+'_footrule']=footrule(order)
            row[label+'_balanced_crossings']=crossing_count(order,n//2)
        rows.append(row)
    return {'randomized_factorizations_checked':checked,'violations':bad,
            'balanced_cut_budget_example':{
            'N':n,
            'fixed_order_no_permutations_min_scan_passes':n,
            'with_one_bit_reverse_min_scan_passes_by_cut_rank':n//2,
            'important':'Necessary rank budgets, not sufficiency or universal gate-count bounds'},
            'multicut':rows}


if __name__=='__main__':
    import json
    print(json.dumps(cut_budget_experiment(),indent=2))
