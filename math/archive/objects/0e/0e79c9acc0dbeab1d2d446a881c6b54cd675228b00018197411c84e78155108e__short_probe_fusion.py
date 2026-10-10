"""Phase23: exact short-prefix reciprocal Hankel search, fully certified.

Substantive modification over Phase22: phase21/22 two Hankel pencils use
T[0..2*s+1], i.e. 2*s+2 frequency probes, not 4*s. We cannot use the old
uniqueness shortcut which needed 4*s, so every spectral candidate gets its
own full N-coordinate cyclic convolution certificate, with ordinary DFT
fallback on failure. All-input exactness comes from that full certificate.

We also stream 2*s+2 Fourier probes in a common loop, sharing the powers
omega^j and avoiding re-generating the full frequency powers separately.
No claimed sub-NlogN worst-case result.
"""
from dataclasses import dataclass
from annihilator_engine import Work, batch_inverse_nonzero
from annihilator_engine import sparse_direct_fourier
from compressed_resultant import compressed_U_from_inverse_probes
from joint_pencil import shared_res_at
from trace_subgroup import (trace_subgroup_sieve,
    shifts_from_linear_trace_gcd,shifts_from_trace_gcd_scan)
from reciprocal_union import (det_pencil_samples,recover_four_terms,
    check_cyclic_certificate,factor_sparse_hypercube)
from blind_sparse_rational import poly_gcd
from rational_forcing import bluestein_transform

@dataclass
class ShortMeta:
    probe_count:int=0
    determinant_samples:int=0
    witness_samples:int=0
    trace_gcd_degree:int=-1
    trace_rejected:bool=False
    trace_linear_extracted:bool=False
    trace_half_scan:bool=False
    candidate_shifts:int=0
    parameter_candidates:int=0
    cyclic_checks:int=0
    cyclic_entries:int=0
    singular_denominators:int=0
    failed_certificates:int=0
    selected:str='fallback'
    reason:str='no-certificate'


def prefix_fourier_stream(r,powers,m,p,co=None):
    """Compute [sum_j r_j omega^(kj)]_(k=0..m-1).

    Preinitialized table powers[j] = omega^j. Per input j maintain
    v=r[j]*(omega^j)^k. Exactly N*m additions and N*(m-1)
    multiplications; no FFT, no hidden free transforms. All intermediate
    powers are local and input-dependent terms are read once.
    """
    if not 1<=m<=len(powers) or len(r)!=len(powers):
        raise ValueError('bad prefix size')
    out=[0]*m
    for j,val in enumerate(r):
        w=powers[j];u=val
        for k in range(m):
            out[k]=(out[k]+u)%p
            if k+1<m:u=u*w%p
    if co is not None:
        co.multiplies+=len(r)*(m-1)
        co.additions+=len(r)*m
        co.reads+=len(r)+m*len(r)
        co.writes+=m*len(r)
    return out


def discover_short_probe(r,engine,co=None,s=4,extra_witness=3):
    if co is None:co=Work()
    n,p=engine.n,engine.p
    m=2*s+2
    meta=ShortMeta(probe_count=m)
    b=s*(s+1)*(2*s+1)//6
    if not 1<=s<=8 or n<m or p<=4*b+20:
        meta.reason='unsupported-field-or-length'
        return None,meta
    R=prefix_fourier_stream(r,engine.powers,m,p,co)
    if any(v==0 for v in R):
        meta.reason='zero-Fourier-probe';return None,meta
    T=batch_inverse_nonzero(R,p,co)
    U,details=compressed_U_from_inverse_probes(T,p,s,co,extra_witness,resultant_evaluator=shared_res_at)
    if U is None or not any(U):
        meta.reason='zero-resultant';return None,meta
    meta.determinant_samples=details['samples']
    meta.witness_samples=details['witnesses']
    trace=trace_subgroup_sieve(details['V'],n,p,co)
    meta.trace_gcd_degree=trace.gcd_degree
    if not trace.possible:
        meta.trace_rejected=True;meta.reason='trace-gcd-one';return None,meta
    if trace.gcd_degree==1:
        candidates=shifts_from_linear_trace_gcd(trace,engine,co)
        meta.trace_linear_extracted=True
    else:
        candidates=shifts_from_trace_gcd_scan(trace,engine,co)
        meta.trace_half_scan=True
    meta.candidate_shifts=len(candidates)
    # Nonzero resultant has at most 2*b admissible nonidentity roots.
    if len(candidates)>2*b:
        meta.reason='too-many-shift-candidates';return None,meta
    for delta in candidates:
        w=engine.powers[delta]
        P0=det_pencil_samples(T,w,0,p,co,s)
        P1=det_pencil_samples(T,w,1,p,co,s)
        g=poly_gcd(P0,P1,p,co)
        if len(g)!=2:continue
        alpha=(-g[0])%p
        if alpha==0:continue
        meta.parameter_candidates+=1
        Y=[];wk=1
        for f in T:
            Y.append(f*(1-alpha*wk)%p)
            wk=wk*w%p
            co.multiplies+=3;co.additions+=1
        A=recover_four_terms(Y,engine.powers,p,co,s)
        if not A:continue
        Ahat=sparse_direct_fourier(A,n,engine.powers,p,co)
        if any(z==0 for z in Ahat):
            meta.singular_denominators+=1
            continue
        meta.cyclic_checks+=1
        accepted,checked=check_cyclic_certificate(r,A,delta,alpha,p,co)
        meta.cyclic_entries+=checked
        if not accepted:
            # IMPORTANT: reduced probes do not justify uniqueness of the
            # represented rational function. Continue checking candidates.
            meta.failed_certificates+=1
            continue
        meta.selected='short-prefix-certified'
        meta.reason='full-cyclic-certificate'
        return (A,delta,alpha,Ahat),meta
    meta.reason='no-certified-model'
    return None,meta


def transform_short_probe(engine,x,s=4):
    n,p=engine.n,engine.p
    if len(x)!=n:raise ValueError('wrong input length')
    co=Work()
    r=engine.P.apply(x)
    co.multiplies+=2*n;co.additions+=n;co.reads+=2*n;co.writes+=n
    found,meta=discover_short_probe(r,engine,co,s)
    factors=None
    if found is None:
        forcing,_=bluestein_transform(r,n,engine.omega,p,engine.primitive_gen,co.sparse)
        selection='fallback'
    else:
        A,delay,alpha,Ahat=found
        if len(A) in (2,4,8,16):
            factors=factor_sparse_hypercube(A,delay,alpha,n,p,
                    (len(A).bit_length()-1),co)
        wk=1;w=engine.powers[delay]
        numerator=[]
        for k in range(n):
            numerator.append((1-alpha*wk)%p)
            wk=wk*w%p
            co.multiplies+=2;co.additions+=1
        inverse=batch_inverse_nonzero(Ahat,p,co)
        forcing=[numerator[k]*inverse[k]%p for k in range(n)]
        co.multiplies+=n;co.writes+=n
        selection='short-prefix-certified'
    y=engine.L.solve(forcing)
    co.multiplies+=3*n+1;co.additions+=2*n;co.reads+=3*n;co.writes+=2*n
    return y,{'selected':selection,'meta':meta,'work':co,'graph_factors':factors}
