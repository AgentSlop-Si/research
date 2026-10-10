"""Unrestricted complex edge-gain comparison: all N-1 two-row Fourier ratios.

Exact rank certificates over split primes show generic dominance of full
2-row projective ratios for explicitly chosen graph orders, but do NOT prove
that the *particular* Fourier target is attainable.
"""
from __future__ import annotations
import sys, json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent.parent/'fft_green_phase40_four_middle'))
from phase40_holonomy import random_problem, normalize_gauge
from phase40_local_synthesis import dense_green, small_rank

def full_jac(n,p,seed=40040):
    cycles,ws=random_problem(n,p,seed)
    norm=normalize_gauge(n,cycles,ws,p)
    w=[norm['edge_weights'][:n],norm['edge_weights'][n:]]
    gs=[dense_green(cycles[s],w[s],p) for s in range(2)]
    M=[[(gs[0][i][j]+gs[1][i][j])%p for j in range(n)] for i in range(n)]
    assert all(M[i][j] for i in (0,1) for j in range(n))
    inv={ (r,j):pow(M[r][j],p-2,p) for r in (0,1) for j in range(n) }
    J=[]
    for j in range(1,n):
        row=[]
        for idx in norm['chord']:
            e=norm['edges'][idx]
            G=gs[e.cycle]
            def term(r,col):return G[r][e.target]*G[e.source][col]%p*inv[r,col]%p
            row.append((term(0,j)+term(1,0)-term(1,j)-term(0,0))%p)
        J.append(row)
    return dict(N=n,prime=p,target_ratios=n-1,free_chord_gains=n+1,
                jacobian_rank=small_rank(J,p),cycle_orders=cycles,chords=norm['chord'])

if __name__=='__main__':
    data=[]
    for n in (8,16,32,64,128):
        for p in (998244353,2013265921):
            a=full_jac(n,p)
            data.append({k:v for k,v in a.items() if k not in ('cycle_orders','chords')})
            print(data[-1],flush=True)
    Path(__file__).with_name('phase41_arbitrary_amplitude_audit.json').write_text(json.dumps(data,indent=2))
