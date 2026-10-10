#!/usr/bin/env python3
"""Optional independent network-flow audit: all 15*255 parity layouts.

Requires networkx, scipy, numpy. Checks exact GF(p) Fourier rank for each
of the 255 masks in two prime fields (510 exact rank calculations), then
checks 3825 exact integer maxflows for all choices of replaced stages.
"""
from pathlib import Path
import json,itertools
from verify_rank_rigidity import N,K,PRIMES,affine,transport,parity,boundary,rank_mod,fourier_matrix
from fast_mincut import ScanFlowOracle

HERE=Path(__file__).resolve().parent
L=json.loads((HERE/'AFFINE_LAYOUT.json').read_text())
perms=[affine(x) for x in L['affine_shuffle_columns']]
saved=json.loads((HERE/'EXACT_CERTIFICATES.json').read_text())['certificates']
paths=[]
for mask in range(1,N):
    trace=[mask]
    for p in perms:trace.append(transport(trace[-1],p))
    R=[i for i in range(N) if parity(i,trace[-1])==1]
    C=[i for i in range(N) if parity(i,trace[0])==0]
    expected= N//4 if (trace[0].bit_length()-1)+(trace[-1].bit_length()-1)<=K-2 else N//2
    paths.append((mask,trace,R,C,expected))
for p in PRIMES:
    F,_=fourier_matrix(p)
    for mask,trace,R,C,rank in paths:
        actual=rank_mod(F[__import__('numpy').ix_(R,C)],p)
        assert actual==rank,(p,mask,actual,rank)
    print('PASS 255 exact Fourier-rank checks modulo',p,flush=True)

cut_checks=0
for count in range(1,5):
    for J0 in itertools.combinations(range(4),count):
        stages=tuple(x+1 for x in J0)
        r=[0 if j in J0 else 1 for j in range(4)]
        oracle=ScanFlowOracle(N,r,perms)
        maxgap=-1
        for mask,trace,R,C,rank in paths:
            flow=oracle.bound(R,C)
            budget=sum(boundary(trace[j]) for j in range(4) if j not in J0)
            assert flow<=budget,(stages,mask,flow,budget)
            maxgap=max(maxgap,rank-flow)
            cut_checks+=1
        matching=next(c for c in saved if tuple(c['replaced_stages'])==stages)
        assert maxgap==matching['rank_correction_lower_bound']
        selected=next(p for p in paths if p[0]==matching['input_mask'])
        assert oracle.bound(selected[2],selected[3])==matching['remaining_stage_capacity']
        print('PASS',stages,'maximum parity-family deficit',maxgap,flush=True)
assert cut_checks==3825
print('PASS 3,825 exact min-cut calculations; 510 independent modular rank checks')
