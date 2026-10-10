"""Exploratory q=7 rectangular 3x5 test; *sampled*, not exhaustive."""
from __future__ import annotations
from random import Random
from phase31_rectangular import family,SEEDS,P
from phase31_six_control import additional_green,all_rect_minors
from phase30_dimension_gate import lifted_general
from phase30_macaulay import rank_pivots

def run(n=8,samples=3):
    seed=SEEDS.get(n,2800+n)
    target, g5=family(n,seed)
    g6=additional_green(n,seed*7+29,17)
    g7=additional_green(n,seed*7+31,19)
    gens=(*g5,g6,g7)
    rng=Random(3300+n)
    hist={}
    for _ in range(samples):
        rs=rng.sample(range(n),3)
        cs=rng.sample(range(n),5)
        rows=lifted_general(all_rect_minors(target,gens,rs,cs),7,3)
        rk,_=rank_pivots(rows)
        hist[rk]=hist.get(rk,0)+1
    return {'N':n,'prime':P,'generators':7,'window':[3,5],
            'degree':3,'basis_dimension':84,'checked':samples,'exhaustive':False,
            'rank_histogram':hist}

if __name__=='__main__':
    import json
    for n in (8,16):print(json.dumps(run(n),sort_keys=True),flush=True)
