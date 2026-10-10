"""v12: globally centered Jacobi--Anger lift for v11's shared-state FFT research.

The exact mathematical identity and the associated tail bound work for every
N.  `centered_fused_row` invokes the inherited randomized v9 dyadic decoder;
its outputs are therefore randomized approximations, not exact DFTs.

The source `prototype.py` and `unit_step_core.py` are byte-for-byte copied
from the supplied v11 checkpoint. This file changes the *center* of the
Bessel expansion, not the dyadic solver or its O(RN) work.
"""
from __future__ import annotations
import math
from typing import Any

import numpy as np
from scipy.special import jv

import prototype as base
import unit_step_core as core


def support_center(n: int, q: int | None = None) -> float:
    """Unique minimax center for all potentially nonzero input positions 0..n-1."""
    if n<1: raise ValueError('n must be positive')
    if q is None:q=base.next_power_of_two(n)
    if q<n:raise ValueError('q smaller than n')
    return (n-1)/(2*q)


def certified_tail(rank: int, zmax: float) -> float:
    """Validated analytic upper bound on the Jacobi-Anger r>=rank tail.

    For alpha=|zmax|/2, |J_r(z)| <= alpha^r/r! * exp(alpha^2/(r+1)).
    Sum a geometric bound from order rank with ratio <=alpha/(rank+1).
    """
    if rank<1:raise ValueError('rank must be >=1')
    if zmax<0:raise ValueError('zmax must be nonnegative')
    a=zmax/2
    if a>=rank+1:return float('inf')
    if a==0:return 0.0
    return 2*math.exp(a*a/(rank+1))*(a**rank)/math.factorial(rank)/(1-a/(rank+1))


def certified_rank(n: int, target: float, centered: bool=True) -> int:
    """Minimal retained Bessel orders under *the same* conservative bound."""
    if target<=0:raise ValueError('target must be positive')
    q=base.next_power_of_two(n)
    z=math.pi*(n-1)/q
    if centered:z/=2
    for r in range(1,100):
        if certified_tail(r,z)<=target:return r
    raise OverflowError('rank search range exhausted')


def shared_carrier(n: int, indices: np.ndarray | None = None) -> np.ndarray:
    """Balanced O(N) complex-product scan; only TWO phase exponential setups.

    delta_j = j_{k+1} - j_k is 1 or 2 because 1<=Q/N<2.
    phase[k+1]/phase[k] = exp(-2pi*i*c*(Q-N*delta_j)/N).
    A Blelloch exclusive scan limits multiplication depth to O(log N).
    """
    if n<1:raise ValueError('n must be positive')
    q=base.next_power_of_two(n)
    if indices is None:indices=base.exact_nearest_grid_map(n,q)[0]
    indices=np.asarray(indices,dtype=np.int64)
    if indices.shape!=(n,):raise ValueError('invalid indices shape')
    c=support_center(n,q)
    # Only two transcendental evaluations regardless of N.
    r1=np.exp(-2j*math.pi*c*(q-n)/n)
    r2=np.exp(-2j*math.pi*c*(q-2*n)/n)
    if n>1:
        steps=np.diff(indices)
        if not np.all((steps==1)|(steps==2)):
            raise ValueError('nearest-grid increments not 1 or 2')
    m=base.next_power_of_two(n)
    work=np.ones(m,dtype=np.complex128)
    if n>1:work[:n-1]=np.where(steps==1,r1,r2)
    # upsweep: products on disjoint subtrees, O(m)
    stride=1
    while stride<m:
        r=np.arange(2*stride-1,m,2*stride)
        work[r]=work[r]*work[r-stride]
        stride*=2
    # downsweep: exclusive prefixes, O(m)
    work[-1]=1+0j
    stride=m//2
    while stride:
        r=np.arange(2*stride-1,m,2*stride)
        old=work[r-stride].copy()
        work[r-stride]=work[r]
        work[r]=work[r]*old
        stride//=2
    return work[:n].copy()


def _offsets(n: int):
    q=base.next_power_of_two(n)
    ids, _, theta=base.exact_nearest_grid_map(n,q)
    center=support_center(n,q)
    factor=shared_carrier(n,ids)
    return q,ids,theta,center,factor


def centered_truncated_center(x: np.ndarray, rank: int) -> np.ndarray:
    """Deterministic rank-R center with exact dyadic FFTs (up to floating point)."""
    v=np.asarray(x, dtype=np.complex128)
    n=v.size
    q,indices,theta,c,correction=_offsets(n)
    nodes=np.arange(n,dtype=np.float64)/q-c
    def provide(r: int):
        buf=np.zeros(q,dtype=np.complex128)
        buf[:n]=v*jv(r,math.pi*nodes)
        return base.normalized_dft(buf)[indices]
    out=base._clenshaw_selected_series(theta,rank,provide)
    return math.sqrt(q/n)*correction*out


def centered_fused_center(x: np.ndarray,rank: int, block: int,halfwidth: int=0)->np.ndarray:
    """Deterministic center of the local-channel-fused centered approximation."""
    if halfwidth<0:raise ValueError('halfwidth negative')
    v=np.asarray(x,dtype=np.complex128)
    n=v.size
    q,indices,theta,c,correction=_offsets(n)
    if q%block:raise ValueError('block must divide q')
    k=q//block
    buf=np.zeros(q,dtype=np.complex128);buf[:n]=v
    local_z=math.pi*np.arange(block,dtype=np.float64)/q
    orders=np.arange(-halfwidth,halfwidth+1)
    local_weights=np.stack([jv(int(h),local_z) for h in orders],axis=1)
    block_z=math.pi*(np.arange(k,dtype=np.float64)/k-c)
    def provide(r: int):
        factors=np.stack([jv(int(r-h),block_z) for h in orders],axis=1)
        approx_weights=local_weights@factors.T
        f=base.normalized_dft(buf*approx_weights.T.reshape(q))
        return f[indices]
    out=base._clenshaw_selected_series(theta,rank,provide)
    return math.sqrt(q/n)*correction*out


def centered_fused_row(x: np.ndarray,rank:int,block:int,state:core.ChirpState,
                       halfwidth:int=0,dtype:Any=np.complex128,center_override:float|None=None,
                       carrier: np.ndarray | None = None)->np.ndarray:
    """One *randomized* chirp row, with one-pass Neumann input compression.

    `center_override=0.0` is a positive regression control reproducing v11.
    The decoder cost remains R transforms and R scans of length Q.
    """
    if rank<1:raise ValueError('rank must be >=1')
    if halfwidth<0:raise ValueError('halfwidth negative')
    v=np.asarray(x,dtype=np.complex128)
    n=v.size
    q,indices,theta,c,correction=_offsets(n)
    if center_override is not None:
        c=float(center_override)
        correction=np.exp(-2j*math.pi*c*theta)
    elif carrier is not None:
        if np.asarray(carrier).shape!=(n,):raise ValueError('carrier must have length n')
        correction=np.asarray(carrier,dtype=np.complex128)
    _,k,_=core.validate_dimensions(q,block)
    plan=base.SelectedDecoderPlan.build(q,block,state,indices)
    buf=np.zeros(q,dtype=np.complex128);buf[:n]=v
    phase=core.local_phase_matrix(q,block,state)
    perblock=phase*buf.reshape(k,block)
    local_z=math.pi*np.arange(block,dtype=np.float64)/q
    orders=np.arange(-halfwidth,halfwidth+1)
    local_weights=np.stack([jv(int(h),local_z) for h in orders],axis=1)
    channels=perblock@local_weights
    block_z=math.pi*(np.arange(k,dtype=np.float64)/k-c)
    def provide(r: int):
        factors=np.stack([jv(int(r-h),block_z) for h in orders],axis=1)
        summaries=np.sum(channels*factors,axis=1)
        return plan.decode_selected(summaries,dtype)
    out=base._clenshaw_selected_series(theta,rank,provide)
    return math.sqrt(q/n)*correction*out


def bessel_l1_envelope(zmax: float) -> float:
    """Bound sum_{r in Z}|J_r(z)| for all real |z|<=zmax.

    From |J_r(z)| <= (|z|/2)^r/r! * exp(z^2/(4(r+1))),
    and using r+1>=2 for r>=1, |J0(z)|<=1.
    """
    if zmax<0:raise ValueError('zmax must be nonnegative')
    a=zmax/2
    return 1+2*math.exp(a*a/2)*math.expm1(a)


def addition_bound_rank_independent(n:int,block:int,halfwidth:int=0)->float:
    """New convolution-l1 bound: independent of global Bessel rank R.

    For each retained r, J_r(zb+delta) - sum_|h|<=H J_(r-h)(zb)J_h(delta)
    is the omitted convolution. Summing over *all* positive and negative r
    costs at most (sum_|t| |J_t(zb)|)(sum_|h|>H |J_h(delta)|).
    Keeping only |r|<R cannot increase this absolute bound.
    """
    if n<1:raise ValueError('n must be >=1')
    q=base.next_power_of_two(n)
    if block<1 or q%block:raise ValueError('block must be a positive divisor of q')
    z=math.pi*(n-1)/(2*q)
    delta=math.pi*(block-1)/q
    return bessel_l1_envelope(z)*base.small_argument_bessel_tail(delta,halfwidth)


def centered_deterministic_bound(n:int,rank:int,block:int,halfwidth:int=0)->float:
    """Operator l2->linfty bound in units of ||x||2, not a random confidence radius."""
    q=base.next_power_of_two(n)
    z=math.pi*(n-1)/(2*q)
    return certified_tail(rank,z)+addition_bound_rank_independent(n,block,halfwidth)


def centered_row_variance_bound(x:np.ndarray,rank:int,block:int,halfwidth:int=0)->float:
    """Upper bound on E|row_k - E(row_k)|^2 for each output k."""
    v=np.asarray(x,dtype=np.complex128)
    eps=centered_deterministic_bound(v.size,rank,block,halfwidth)
    return (block/v.size)*(1+eps)**2*float(np.linalg.norm(v))**2


def work_proxy(n:int,rank:int,block:int,halfwidth:int)->float:
    """Transparent scalar-work PROXY; not a certified precise operation count.

    Includes Q-sized input compression, O(R K) Bessel syntheses, R K-FFTs,
    R full-Q scans, R output accumulation, O(N) carrier, and output writes.
    It omits numeric-library-dependent root/Bessel generation and constant
    factors in the scan; cannot be used as a multiplication bit-complexity claim.
    """
    q=base.next_power_of_two(n)
    k=q//block
    H2=2*halfwidth+1
    return H2*q + H2*rank*k + rank*(q+k*math.log2(max(k,2))+n)+n


def choose_parameters(n:int,target:float,block:int|None=None,
                      old_v11:bool=False)->dict:
    """Search finite rank, local halfwidth satisfying a deterministic error goal.

    This prices the two competing constructions under the *same* proxy.
    R,H are small algorithm parameters, not an exhaustive proof of optimum.
    """
    if not 0<target<1:raise ValueError('target must be in (0,1)')
    q=base.next_power_of_two(n)
    if block is None:block=base.choose_dyadic_block(q)
    if block<1 or q%block:raise ValueError('invalid block')
    best=None
    for rank in range(1,50):
        for H in range(12):
            if old_v11:
                eps=base.bessel_tail_bound(rank)+base.addition_kernel_error_bound(n,rank,block,H)
            else:
                eps=centered_deterministic_bound(n,rank,block,H)
            if eps<=target:
                work=work_proxy(n,rank,block,H)
                row={'n':n,'q':q,'block':block,'target':target,
                     'rank':rank,'halfwidth':H,'deterministic_error_bound':eps,
                     'work_proxy':work,'algorithm':'v11_uncentered' if old_v11 else 'v12_centered'}
                if best is None or row['work_proxy']<best['work_proxy']:
                    best=row
    if best is None:raise RuntimeError('search grid too small to certify target')
    return best


def centered_robust_fft(x: np.ndarray,rank:int,rows:int,g:float,
                        rng: np.random.Generator,halfwidth:int=0,
                        dtype:Any=np.complex128)->np.ndarray:
    """End-to-end randomized approximation with inherited v11 majority grid.

    Actual return is approximate: it is NOT an exact FFT or bit complexity result.
    """
    v=np.asarray(x,dtype=np.complex128)
    n=v.size
    if rows<1 or rows%2!=1:raise ValueError('rows must be positive odd')
    if g<=0:raise ValueError('g must be positive')
    norm=float(np.linalg.norm(v))
    if norm==0:return np.zeros(n,dtype=np.complex128)
    q=base.next_power_of_two(n)
    block=base.choose_dyadic_block(q)
    eps=centered_deterministic_bound(n,rank,block,halfwidth)
    tau=g*(1+eps)*math.sqrt(block/n)*norm
    real_state=core.MajorityGridState.zeros(n)
    imag_state=core.MajorityGridState.zeros(n)
    # One complete Fourier-correction carrier shared across randomized rows.
    carrier=shared_carrier(n)
    for _ in range(rows):
        state=core.draw_state(q,rng)
        row=centered_fused_row(v,rank,block,state,halfwidth,dtype,carrier=carrier)
        core.majority_grid_update(real_state,row.real,tau)
        core.majority_grid_update(imag_state,row.imag,tau)
    return (core.majority_grid_finalize(real_state,tau)
            +1j*core.majority_grid_finalize(imag_state,tau))


def robust_uniform_bound(x:np.ndarray,rank:int,g:float,halfwidth:int=0)->float:
    """Same v11 probability-contract radius with the sharpened error epsilon."""
    v=np.asarray(x,dtype=np.complex128);n=v.size
    block=base.choose_dyadic_block(base.next_power_of_two(n))
    eps=centered_deterministic_bound(n,rank,block,halfwidth)
    return (eps+(5/math.sqrt(2))*g*(1+eps)*math.sqrt(block/n))*float(np.linalg.norm(v))


def demo_rank_table():
    rows=[]
    for n in [37,93,127,255,511,1001,4095,10007]:
        for tol in [1e-4,1e-8,1e-12]:
            rb=certified_rank(n,tol,False)
            rc=certified_rank(n,tol,True)
            rows.append({'N':n,'Q':base.next_power_of_two(n),'target_tail':tol,
                         'uncentered_rank':rb,'centered_rank':rc,
                         'fewer_decoder_passes':rb-rc,
                         'fraction_saved':(rb-rc)/rb})
    return rows

if __name__=='__main__':
    import json
    print(json.dumps(demo_rank_table(),indent=2))
