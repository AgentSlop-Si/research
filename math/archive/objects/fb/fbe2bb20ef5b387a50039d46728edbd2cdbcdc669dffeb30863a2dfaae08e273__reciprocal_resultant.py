"""Optional accelerated Phase21 root search via exact finite resultant.

Reconstruct the polynomial resultant of the two Hankel determinants at D+1
known field elements, where D=(s+1)^2(2s+1) is a proven degree bound. Divide
out only per-instance exact factors w and w-1, then evaluate the result at
all Nth roots using sparse/short convolution routines. No assumption that
its experimentally observed degree/palindromicity is universal.
"""
from dataclasses import dataclass
from annihilator_engine import Work, direct_one_frequency, batch_inverse_nonzero
from resultant_pattern import find_resultant_coeff
from resultant_gate import sparse_group_eval
from reciprocal_union import discover_reciprocal_union, factor_sparse_hypercube
from rational_forcing import bluestein_transform


@dataclass
class ResultantMeta:
    outcome:str='fallback'
    resultant_degree:int=-1
    reduced_degree:int=-1
    zero_factor:int=0
    one_factor:int=0
    palindromic:bool=False
    root_candidates:int=0
    dot_probes:int=0
    failed_reason:str=''


def discover_resultant_reciprocal(r,engine,co=None,s=4):
    if co is None:co=Work()
    meta=ResultantMeta()
    n,p=engine.n,engine.p
    if n<4*s or p <= (s+1)**2*(2*s+1)+4:
        meta.failed_reason='invalid-length-or-field';return None,meta
    R=[direct_one_frequency(r,engine.powers[k],p,co) for k in range(4*s)]
    meta.dot_probes=4*s
    if not all(R):
        meta.failed_reason='zero-spectral-probe';return None,meta
    T=batch_inverse_nonzero(R,p,co)
    details,coeff,reduced=find_resultant_coeff(T,p,s,co)
    meta.resultant_degree=details['degree']
    meta.reduced_degree=details['reduced_degree']
    meta.zero_factor=details['zero_factor'];meta.one_factor=details['one_factor']
    meta.palindromic=details['palindromic']
    if not coeff:
        meta.failed_reason='identically-zero-resultant';return None,meta
    values,_=sparse_group_eval(reduced,engine,co)
    roots=[d for d in range(1,n) if values[d]==0]
    meta.root_candidates=len(roots)
    bound=(s+1)**2*(2*s+1)
    if len(roots)>bound:
        meta.failed_reason='resultant-root-count-exceeds-bound';return None,meta
    found,detail=discover_reciprocal_union(r,engine,co,probes=R,max_terms=s,
                                            candidate_shifts=roots)
    meta.outcome='certified' if found else 'fallback'
    meta.failed_reason=detail.reason
    return found,meta


def transform_resultant_reciprocal(engine,x,max_terms=4):
    n,p=engine.n,engine.p
    if len(x)!=n:raise ValueError('bad input')
    co=Work()
    r=engine.P.apply(x)
    co.multiplies+=2*n;co.additions+=n;co.reads+=2*n;co.writes+=n
    found,meta=discover_resultant_reciprocal(r,engine,co,s=max_terms)
    factors=None
    if found is None:
        forcing,_=bluestein_transform(r,n,engine.omega,p,engine.primitive_gen,co.sparse)
        selection='fallback'
    else:
        from annihilator_engine import batch_inverse_nonzero, sparse_direct_fourier
        A,d,a,Ahat=found
        factors=factor_sparse_hypercube(A,d,a,n,p,
                     (len(A).bit_length()-1),co) if len(A) in (2,4,8,16) else None
        wk=1;root=engine.powers[d];bhat=[]
        for k in range(n):
            bhat.append((1-a*wk)%p)
            wk=wk*root%p
            co.multiplies+=2;co.additions+=1
        invs=batch_inverse_nonzero(Ahat,p,co)
        forcing=[bhat[k]*invs[k]%p for k in range(n)]
        co.multiplies+=n;co.writes+=n
        selection='reciprocal-resultant-certified'
    y=engine.L.solve(forcing)
    co.multiplies+=3*n+1;co.additions+=2*n;co.reads+=3*n;co.writes+=2*n
    return y,{'selected':selection,'resultant':meta,'work':co,'graph_factors':factors}
