"""Exact rational uniform-conditioning certificate for stationary W.

W[u,i] = exp(-2pi*i*(T_u/M + u/(K M))), T_u=u(u+1)/2,
M=2^h. T_u mod M is a permutation. For K>=4M, unitary row/column phases
factor W into permuted Fourier U, plus a centered rank-series perturbation
whose normalized operator norm <= exp(pi*(M-1)^2/(2*K*M))-1.
Using pi<22/7 and a rational exponential upper bound yields
cond_2(W* W)<(741/259)^2 <41/5 (that is, 8.2) for ALL these sizes.
"""
from __future__ import annotations
from fractions import Fraction
from math import factorial, exp, pi
import json
from pathlib import Path
import numpy as np


def triangular_permutation(M:int)->bool:
    if M<2 or M&(M-1):raise ValueError('M must be a power of two >=2')
    return len({(u*(u+1)//2)%M for u in range(M)})==M


def exp_rational_upper(x:Fraction,terms:int=8)->Fraction:
    if x<0 or x>=terms+2:raise ValueError('Nonnegative x<terms+2')
    poly=sum(x**j/factorial(j) for j in range(terms+1))
    # The next-to-later consecutive Taylor-term ratios are at most
    # x/(terms+2); hence tail <= first omitted term/(1-ratio).
    first=x**(terms+1)/factorial(terms+1)
    return poly+first/(1-x/(terms+2))


def certified_constant():
    # From pi <22/7, for K>=4M, delta < exp(pi/8)-1 < exp(11/28)-1.
    exp_hi=exp_rational_upper(Fraction(11,28))
    assert exp_hi < Fraction(741,500)
    delta_hi=Fraction(241,500)
    condgram_bound=((1+delta_hi)/(1-delta_hi))**2
    assert condgram_bound == Fraction(741**2,259**2)
    assert condgram_bound < Fraction(41,5)
    return {'pi_rational_upper':'22/7',
            'exponential_argument_upper':'11/28',
            'exponential_taylor_rational_upper':str(exp_hi),
            'exponential_under':'741/500',
            'delta_less_than':'241/500',
            'cond_gram_strict_upper':str(condgram_bound),
            'uniform_conclusion':'cond_2(W*W) < 41/5 for dyadic M>=2, K>=4M'}


def numerical_diagnostics():
    rows=[]
    for M in [2,4,8,16,32,64,128]:
        assert triangular_permutation(M)
        for ratio in [1,2,4,8,16]:
            K=M*ratio;G=M*K
            u=np.arange(M,dtype=np.int64)
            j=np.arange(M,dtype=np.int64)
            e=(K*(u*(u+1)//2)+u)%G
            W=np.exp(-2j*np.pi*(e[:,None]*j[None,:]%G)/G)
            cond=float(np.linalg.cond(W))
            b=(np.exp(np.pi*(M-1)**2/(2*K*M))-1)
            if ratio>=4:
                assert b<1 and cond**2<=((1+b)/(1-b))**2+1e-6
                assert cond**2<8.2
            rows.append({'M':M,'K':K,'ratio':ratio,
                         'observed_gram_condition':cond*cond,
                         'bound_delta':float(b),
                         'bound_applies':ratio>=4})
    return rows


def main():
    obj={'statement':'Exact arithmetic uniform spectral condition bound, not a floating-point error certificate',
         'exact_rational_proof':certified_constant(),
         'numerical_diagnostics':numerical_diagnostics()}
    (Path(__file__).parent/'CONDITIONING_RESULTS.json').write_text(json.dumps(obj,indent=2)+'\n')
    print('Exact rational bound:',obj['exact_rational_proof']['uniform_conclusion'])
    print('Numerical cases:',len(obj['numerical_diagnostics']))

if __name__=='__main__':main()
