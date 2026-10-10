"""Phase 27: expansion-to-crosscut-rank construction for two Green inverses.

Conditional theorem: if union graph of two directed Hamiltonian cycles
has undirected Laplacian gap >= c>0, then for all but finitely many lambda,
S=G_A + lambda*G_B has rank(S[I,J]) >= c*n/16 for every balanced cut.
Finite certificates for c=1/2, N=32..256 live in phase27_expansion_certificate.py.
Forward S has O(N) arithmetic, and for alpha=1/4,beta=1/5 and lambda>0,
kappa_2(S)<2 via explicit Neumann bounds.

This does NOT assert Fourier covariance or sub-NlogN FFT complexity.
"""
from __future__ import annotations
from itertools import combinations
from random import Random
from phase27_affine_gap import (MOD, direct_green,random_hamiltonian,
                               shift_successor,mod_rank)


def modular_mixer(n:int,seed:int,lambda_num:int=3,lambda_den:int=2):
    z=shift_successor(n)
    w=random_hamiltonian(n,seed)
    alpha=pow(4,-1,MOD);beta=pow(5,-1,MOD)
    scale=lambda_num*pow(lambda_den,-1,MOD)%MOD
    gz=direct_green(z,alpha)
    gw=direct_green(w,beta)
    return [[(gz[i][j]+scale*gw[i][j])%MOD for j in range(n)]
            for i in range(n)]


def partition_rank(matrix:list[list[int]],left:list[int])->int:
    n=len(matrix);l=set(left)
    right=[j for j in range(n) if j not in l]
    return mod_rank([[matrix[i][j] for j in right] for i in left])


def audit_balanced_cuts(n:int,seed:int,*,exhaustive=False,trials:int=512,
                        lambda_num:int=3,lambda_den:int=2)->dict:
    matrix=modular_mixer(n,seed,lambda_num,lambda_den)
    rng=Random(2770+n)
    if exhaustive:
        if n>16:raise ValueError('limit exhaustive to n<=16')
        cuts=combinations(range(n),n//2)
        count='all'
    else:
        cuts=(rng.sample(range(n),n//2) for _ in range(trials))
        count=trials
    minrank=n
    checked=0
    for left in cuts:
        minrank=min(minrank,partition_rank(matrix,list(left)))
        checked+=1
    return {'n':n,'seed':seed,'lambda_fraction':f'{lambda_num}/{lambda_den}',
            'min_rank':minrank,'checked_cuts':checked,'exhaustive':exhaustive,
            'predicted_conditional_lower_bound_strict':n/32 if n>=32 else None}

if __name__=='__main__':
    import json
    print(json.dumps(audit_balanced_cuts(16,2716,exhaustive=True)))
    for n in (32,64,128):
        print(json.dumps(audit_balanced_cuts(n,2700+n,trials=80)))


def two_by_two_phase_report(n:int,seed:int,lambda_num:int=3,lambda_den:int=2)->dict:
    """One exact modular necessary Fourier cross-ratio certificate.

    Warning: finite-field failure rejects the evaluated modular candidate;
    it is not an equivalence proof of a corresponding complex expression.
    The all-positive-real rejection is proved separately in THEOREM.md.
    """
    m=modular_mixer(n,seed,lambda_num,lambda_den)
    a,b,c,d=m[0][0],m[0][1],m[1][0],m[1][1]
    if b*c%MOD==0:
        return {'n':n,'excluded_modular':True,'reason':'zero entry'}
    R=a*d%MOD*pow(b*c%MOD,-1,MOD)%MOD
    return {'n':n,'lambda_fraction':f'{lambda_num}/{lambda_den}',
            'cross_ratio':R,'cross_ratio_power_n':pow(R,n,MOD),
            'excluded_modular':pow(R,n,MOD)!=1}
