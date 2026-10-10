"""Concrete exact modular rank certificate at a power-of-two FFT length.

The all-N>=2301 theorem is an analytic COMPLEX statement; this finite-field
certificate is only a supplementary exact sample (doesn't prove all weights).
"""
import json
import random
import functools
from cycle_minor_gate import (permutation_cycles,linearize_perm,find_rectangle,
                              green_perm_submatrix,rank_mod,det_mod)
from small_arc_gate import top_left_fourier_full_minors_threshold


def compute_witness(n=4096,seed=4096,q=65537):
    assert n>=2301 and n&(n-1)==0 and (q-1)%n==0
    z=pow(3,(q-1)//n,q)
    assert pow(z,n,q)==1 and pow(z,n//2,q)!=1
    rng=random.Random(seed)
    perms=[];weights=[];orders=[]
    S=set(range(26))
    for _ in range(2):
        pi=list(range(n));rng.shuffle(pi)
        wi=[rng.randrange(q) for _ in range(n)]
        for cyc in permutation_cycles(pi):
            acc=1
            for i in cyc:acc=acc*wi[i]%q
            if acc==1: wi[cyc[0]]=0
        perms.append(pi);weights.append(wi)
        orders.append([v for v in linearize_perm(pi) if v in S])
    rect=find_rectangle(orders,3)
    R,C=rect['rows'],rect['cols']
    g=[green_perm_submatrix(perms[t],weights[t],R,C,q) for t in range(2)]
    dft=[[pow(z,i*j,q) for j in C]for i in R]
    sumblock=[[(a+b)%q for a,b in zip(ra,rb)]for ra,rb in zip(g[0],g[1])]
    report={
        'N':n,'q':q,'root':z,'seed':seed,
        'root_exact_order_verified':True,
        'cycle_counts':[len(permutation_cycles(pi)) for pi in perms],
        'rows':R,'cols':C,
        'exact_green1_block':g[0], 'exact_green2_block':g[1],
        'exact_dft_block':dft,
        'green1_rank':rank_mod(g[0],q),
        'green2_rank':rank_mod(g[1],q),
        'sum_green_rank':rank_mod(sumblock,q),
        'dft_minor':det_mod(dft,q),
        'dft_rank':rank_mod(dft,q),
        'analytical_all_length_threshold':top_left_fourier_full_minors_threshold(26,3),
        'note':'Exact rank conflict in this finite-field example. The analytical theorem is over complex numbers and all admissible weights.'}
    assert report['green1_rank']<=1 and report['green2_rank']<=1
    assert report['sum_green_rank']<=2
    assert report['dft_rank']==3 and report['dft_minor']!=0
    return report


if __name__=='__main__':
    report=compute_witness()
    print(json.dumps(report,indent=2))
