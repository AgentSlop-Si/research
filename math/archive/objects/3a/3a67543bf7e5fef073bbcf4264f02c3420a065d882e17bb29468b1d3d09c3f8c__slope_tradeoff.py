"""Phase15 second family: exact-rank nonstationary chirps and precision barrier.

Choose G=KM, dyadic M<=K, d=2^h|K, d>=2, L=K/d.
    a_i=1+d*i, beta_i=beta0+d*i, i=0..M-1.
V_{r,u,i}=D_{r,u} W_r[u,i] with
    W_r[u,i] = exp(-2pi*i*i*(T_u + M*r*u)/(L*M))
where T_u=u(u+1)/2. The T_u residues permute modulo dyadic M,
so every local W_r is nonsingular, for every block r and size.
W_r has exact period L in r. At r=0, the Vandermonde nodes lie in an
arc of width <=pi*(M-1)/L, forcing exponential conditioning when L/M
is large. This exposes the precision cost of making the frame truly
nonstationary; it is NOT a lower bound on all possible FFT algorithms.
"""
from __future__ import annotations
from math import comb, pi, log10
from fractions import Fraction
import numpy as np
import json
from pathlib import Path


def validate(M:int,K:int,d:int):
    if M<2 or M&(M-1) or K<M or K&(K-1) or d<2 or d&(d-1) or K%d:
        raise ValueError('Dyadic M<=K, even power-of-two d dividing K')


def triangular_nodes(M:int,K:int,d:int,r:int):
    validate(M,K,d)
    L=K//d
    if not(0<=r<K):raise ValueError('r outside 0..K-1')
    E=tuple((u*(u+1)//2+M*r*u)%(L*M) for u in range(M))
    assert len(set(E))==M
    return E


def W_complex(M:int,K:int,d:int,r:int):
    E=triangular_nodes(M,K,d,r)
    L=K//d
    return np.exp(-2j*np.pi*np.outer(E,np.arange(M))/(L*M))


def exact_cond_gram_lower(M:int,K:int,d:int):
    """Rational strict lower bound at r=0, using pi<22/7."""
    validate(M,K,d)
    L=K//d
    ratio=Fraction(7*L,22*(M-1))
    lower=Fraction(comb(2*M-2,M-1))*(ratio**(2*(M-1)))
    return lower


def modular_rank_cases():
    rows=[]
    for M in (2,4,8,16,32):
        for K in (M,2*M,4*M):
            for d in (2,4,8,16,32,64):
                if d>K:continue
                L=K//d
                for r in range(K):
                    E=triangular_nodes(M,K,d,r)
                    assert len(set(E))==M
                    assert E==triangular_nodes(M,K,d,r%L)
                rows.append({'M':M,'K':K,'d':d,'period':L,'full_rank_all_blocks':True})
    return rows


def diagnostics():
    rows=[]
    for M in (4,8,16,32):
        for ratio in (1,2,4,8,16,32,64):
            L=M*ratio
            K=2*L
            W=W_complex(M,K,2,0)
            c=float(np.linalg.cond(W))
            bound=exact_cond_gram_lower(M,K,2)
            log_lower=log10(float(bound))
            rows.append({'M':M,'L':L,'K':K,'d':2,
                         'observed_cond_W_float64_diagnostic':c,
                         'analytic_log10_lower_bound_cond_Gram':log_lower,
                         'ratio_L_over_M':ratio,
                         'float64_warning':c>1e12})
    return rows


def main():
    cases=modular_rank_cases()
    out={'claim':'Every local W_r full rank; exact period L=K/d; large L/M implies provably expensive conditioning at r=0',
         'all_block_rank_cases':cases,
         'rational_inequality':'cond_2(W0* W0) > C(2M-2,M-1)*(7L/(22(M-1)))^(2(M-1))',
         'not_a_lower_bound_on_general_fft':True,
         'numerical_diagnostics':diagnostics()}
    (Path(__file__).parent/'SLOPE_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(f'{len(cases)} all-block exact rank/period cases verified; {len(out["numerical_diagnostics"])} floating diagnostics')

if __name__=='__main__':main()
