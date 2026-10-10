"""Rank certificate for nonlinear feature banks + linear readout.

If a bank has M=N scalar features and its linear readout computes all N
independent Fourier outputs on {0,1}^N, then each feature must itself be a
Boolean-linear function. A nonlinear degree of freedom needs an EXTRA feature.
This is a restricted feature-bank model, NOT a general FFT lower bound.
"""
from __future__ import annotations
from itertools import product
import json
from pathlib import Path
from degree_boundary import P, direct_dft, matrix_rank_mod


def verify(n):
    assert n<=10 and n>=2 and not n & (n-1)
    E=[];F=[];Sq=[];linear=[]
    for bits in product((0,1),repeat=n):
        s=sum(bits)%P
        z=s*s%P
        E.append([(t+z)%P for t in bits])
        F.append(direct_dft(bits))
        Sq.append([z])
        linear.append(list(bits))
    rA=matrix_rank_mod(E)
    with_outputs=[e+f for e,f in zip(E,F)]
    with_extra=[e+sq for e,sq in zip(E,Sq)]
    with_extra_outputs=[e+sq+f for e,sq,f in zip(E,Sq,F)]
    rAF=matrix_rank_mod(with_outputs)
    rAE=matrix_rank_mod(with_extra)
    rAEF=matrix_rank_mod(with_extra_outputs)
    assert (rA,rAF,rAE,rAEF)==(n,n+1,n+1,n+1), (n,rA,rAF,rAE,rAEF)
    return {'N':n,'rank_N_nonlinear_features':rA,
            'rank_after_adding_all_FFT_outputs':rAF,
            'rank_after_adding_one_square_of_sum_feature':rAE,
            'rank_after_adding_square_and_FFT_outputs':rAEF,
            'conclusion':'N mixed features cannot linearly read out all FFT outputs; N+1 features can'}

if __name__=='__main__':
    out=[verify(n) for n in (2,4,8)]
    Path(__file__).with_name('feature_rank_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
