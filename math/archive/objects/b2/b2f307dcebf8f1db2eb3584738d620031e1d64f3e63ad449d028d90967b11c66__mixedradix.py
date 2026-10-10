"""Hero #1 v13: independent dyadic sketches before an exact odd-part FFT.

This is a randomized *approximate* Fourier transform for arbitrary dense data.
The mean is exactly the normalized DFT in exact arithmetic, without a Bessel
truncation. For N = G * m, G the largest power of two dividing N, the error
variance at EVERY output is bounded by (M/N)||x||_2^2, where M is the sketch
block size on the dyadic factor G and independently sampled chirp states are
used for each of the m input columns.

Cost per row = O(N + N log m + (N/M) log(G/M)), which is O(N log(m+1))
for M roughly log G. For odd N, G=1 and the algorithm is an ordinary FFT.
No claim of exact o(N log N) FFT is made. Numerical calls to np.fft and np.exp
are not certified bit-complexity/rounding results.
"""
from __future__ import annotations
from dataclasses import dataclass
import math
from typing import Any
import numpy as np
import unit_step_core as core


def dyadic_odd_split(n: int) -> tuple[int,int]:
    if n < 1:
        raise ValueError('N must be positive')
    g = n & -n
    return g, n//g


def sketch_block(g:int) -> int:
    """A dyadic M with K>=M and log(G/M)=O(M) for large G."""
    if g<1 or (g&(g-1)):
        raise ValueError('G must be a positive power of two')
    if g<=4:
        return 1
    m=1<<int(math.log2(max(1.0,math.log2(g))))
    while m*m>g:
        m//=2
    return max(1,m)


def twiddle_one_root(g:int,m:int)->np.ndarray:
    """Generate all exp(-2 pi i k*s/(gm)) with ONE transcendental root.

    O(g*m) complex multiplies, O(g*m) storage. This is algebraically exact,
    but approximate-root error is O(N*u) in finite precision, so an appropriate
    p=O(log N) precision/reanchoring contract is needed for certified accuracy.
    """
    n=g*m
    if n<1:raise ValueError('Lengths must be positive')
    omega=np.exp(-2j*math.pi/n)
    out=np.ones((g,m),dtype=np.complex128)
    current=1.+0j
    for k in range(g):
        power=1.+0j
        for s in range(1,m):
            power*=current
            out[k,s]=power
        current*=omega
    return out


def exact_mixedradix_reference(x:np.ndarray)->np.ndarray:
    """Check exact Cooley--Tukey orientation without FFT_N oracle."""
    v=np.asarray(x,dtype=np.complex128)
    n=v.size
    g,m=dyadic_odd_split(n)
    a=np.fft.fft(v.reshape(g,m),axis=0)/math.sqrt(g)
    k1=np.arange(g)[:,None]
    s=np.arange(m)[None,:]
    a*=np.exp(-2j*np.pi*k1*s/n)
    out=np.fft.fft(a,axis=1)/math.sqrt(m)
    return out.T.copy().reshape(n)


def one_row_mixedradix(x:np.ndarray,rng:np.random.Generator,
                       block:int|None=None,dtype:Any=np.complex128,
                       states:list[core.ChirpState]|None=None,
                       twiddles:np.ndarray|None=None)->np.ndarray:
    """Unbiased row: fresh *independent* state for every dyadic input column.

    For g=1, this is exactly the ordinary length-N FFT. Otherwise:
      n = m*n1 + s,       k = k1 + g*k2.
      u[k1,s] = normalized_SKETCH_F_g(x[m*n1+s] over n1)
      w[k1,s] = u[k1,s] exp(-2pi*i*k1*s/N)
      output[k1+g*k2] = normalized_F_m(w[k1,:])[k2].
    """
    arr=np.asarray(x,dtype=np.complex128)
    n=arr.size
    g,m=dyadic_odd_split(n)
    if states is not None and len(states)!=m:
        raise ValueError('One state per odd-part column required')
    if g==1:
        if block not in (None,1):
            raise ValueError('Block must be 1 for g=1')
        return np.fft.fft(arr)/math.sqrt(n)
    if block is None:
        block=sketch_block(g)
    core.validate_dimensions(g,block)
    source=arr.reshape(g,m)
    stages=np.empty((g,m),dtype=np.complex128)
    for s in range(m):
        state=states[s] if states is not None else core.draw_state(g,rng)
        # Crucial: independent states across s are required for the M/N bound.
        stages[:,s]=core.one_row_estimate(source[:,s],block,state,dtype)
    if twiddles is None:
        twiddles=twiddle_one_root(g,m)
    twiddles=np.asarray(twiddles,dtype=np.complex128)
    if twiddles.shape!=(g,m):
        raise ValueError('Twiddle table must have shape (G,m)')
    stages*=twiddles
    out=np.fft.fft(stages,axis=1)/math.sqrt(m)
    return out.T.copy().reshape(n)


def mixedradix_variance_bound(x:np.ndarray,block:int|None=None)->float:
    """Exact arithmetic, maximal variance over all output coordinates."""
    arr=np.asarray(x,dtype=np.complex128)
    n=arr.size
    g,m=dyadic_odd_split(n)
    if g==1:
        return 0.
    if block is None:block=sketch_block(g)
    core.validate_dimensions(g,block)
    if block==1:
        return 0.
    return (block/n)*float(np.vdot(arr,arr).real)


def mixedradix_variance_exact(x:np.ndarray,k1:int,block:int|None=None)->float:
    """Exact mathematical covariance contraction from inherited dyadic theorem.

    Computes an O(g^2) dense covariance matrix for audit ONLY, NOT execution.
    """
    arr=np.asarray(x,dtype=np.complex128)
    n=arr.size
    g,m=dyadic_odd_split(n)
    if k1<0 or k1>=g:
        raise ValueError('k1 outside dyadic length')
    if g==1:return 0.
    if block is None:block=sketch_block(g)
    cov=core.covariance_matrix_formula(g,block,k1)
    cols=arr.reshape(g,m)
    return float(sum(np.vdot(cols[:,s],cov@cols[:,s]).real for s in range(m))/m)


def work_proxy(n:int,block:int|None=None)->dict:
    """Transparent unit-weighted scalar work proxy, not a calibrated benchmark."""
    g,m=dyadic_odd_split(n)
    if block is None:block=sketch_block(g)
    if g>1:core.validate_dimensions(g,block)
    elif block!=1:raise ValueError('Block must equal one when g=1')
    fft_k=m*(g/block)*math.log2(max(2,g/block)) if g>1 else 0
    # One full set of randomized local sums and gauged scans (N),
    # one set of twiddles (N), one write per output (N), and m FFT_m.
    # This does not include phase/root generation, sampling, or constant factors.
    proxy=(3*n + fft_k + n*math.log2(max(1,m))) if g>1 else n*math.log2(max(2,n))+n
    return {'n':n,'g':g,'odd_part':m,'block':block,
            'charged_scan_and_compression':n if g>1 else 0,
            'charged_short_fft_proxy':fft_k,
            'charged_odd_fft_proxy':n*math.log2(max(1,m)),
            'charged_twiddles_and_output':2*n if g>1 else 0,
            'work_proxy':proxy,'variance_factor':0 if block==1 or g==1 else block/n}


def robust_mixedradix_fft(x:np.ndarray,rows:int,gain:float,
                          rng:np.random.Generator,block:int|None=None,
                          dtype:Any=np.complex128)->np.ndarray:
    """Three-grid streaming robust estimator, inherited from v9.

    In exact arithmetic the v9 grid guarantee applies verbatim using
    sigma^2 <= M/N ||x||_2^2 and independent rows; no Bessel bias.
    """
    arr=np.asarray(x,dtype=np.complex128)
    n=arr.size
    g,m=dyadic_odd_split(n)
    if rows<1 or rows%2!=1:raise ValueError('rows must be odd and positive')
    if gain<=math.sqrt(2):raise ValueError('gain must exceed sqrt(2)')
    if float(np.vdot(arr,arr).real)==0:
        return np.zeros_like(arr)
    if block is None:block=sketch_block(g)
    if g==1 or block==1:
        return exact_mixedradix_reference(arr)
    tau=gain*math.sqrt(block/n)*float(np.linalg.norm(arr))
    rs=core.MajorityGridState.zeros(n)
    is_=core.MajorityGridState.zeros(n)
    twiddles=twiddle_one_root(g,m)
    for _ in range(rows):
        y=one_row_mixedradix(arr,rng,block,dtype,twiddles=twiddles)
        core.majority_grid_update(rs,y.real,tau)
        core.majority_grid_update(is_,y.imag,tau)
    return core.majority_grid_finalize(rs,tau)+1j*core.majority_grid_finalize(is_,tau)


def robust_uniform_bound(x:np.ndarray,block:int|None,gain:float)->float:
    arr=np.asarray(x,dtype=np.complex128)
    g,m=dyadic_odd_split(arr.size)
    if block is None:block=sketch_block(g)
    if block==1 or g==1:return 0.
    return (5/math.sqrt(2))*gain*math.sqrt(block/arr.size)*float(np.linalg.norm(arr))


def failure_probability(n:int,rows:int,gain:float)->float:
    if gain<=math.sqrt(2):raise ValueError('gain > sqrt(2) required')
    return core.majority_failure_bound(n,rows,gain)


def exact_beta_frame(x:np.ndarray,rng:np.random.Generator,
                     block:int|None=None,dtype:Any=np.complex128,
                     base_states:list[core.ChirpState]|None=None)->np.ndarray:
    """Construct an EXACT (in exact arithmetic) all-output FFT from M frames.

    For G=K*M, fix a unit chirp a_s and beta_s in every input column s,
    and take M beta values beta_s + t*K, t=0,...,M-1. The local phase rows
    form an M-by-M DFT (up to fixed diagonal gauges) and their rank-K
    physical projectors satisfy sum_t P_{s,t}=M*I_G. Thus averaging the
    M complete (random-looking) sketch rows returns F_N x identically.

    Rank obstruction: any linear sum of fewer than M fixed single-row sketch
    maps has rank < N, so cannot equal F_N. This frame construction meets
    the rank lower bound, but costs >= Omega(M*N), i.e. does NOT beat FFT.
    """
    arr=np.asarray(x,dtype=np.complex128)
    n=arr.size
    g,m=dyadic_odd_split(n)
    if g==1:
        return np.fft.fft(arr)/math.sqrt(n)
    if block is None:block=sketch_block(g)
    core.validate_dimensions(g,block)
    if base_states is None:
        base_states=[core.draw_state(g,rng) for _ in range(m)]
    if len(base_states)!=m:
        raise ValueError('One base state per column required')
    k=g//block
    twiddle=twiddle_one_root(g,m)
    total=np.zeros(n,dtype=np.complex128)
    for t in range(block):
        states=[core.ChirpState(a=st.a,beta=(st.beta+t*k)%g)
                for st in base_states]
        total+=one_row_mixedradix(arr,rng,block,dtype,states,twiddle)
    return total/block
