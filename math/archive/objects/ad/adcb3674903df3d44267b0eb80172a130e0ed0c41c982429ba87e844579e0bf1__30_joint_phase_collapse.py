#!/usr/bin/env python3
"""HERO #0 Phase 5: exact joint-phase collapse and scoped moment tests.

Independent complex implementation. No large-Q direct FFT occurs INSIDE
joint_exact_from_summaries; direct np.fft.fft(x) is TEST ORACLE only.

Main fact: for all M Green phases, aggregate the channels *before* the
long scans. The result is the ordinary mixed-radix Cooley--Tukey transform,
O(Q log Q), not a breakthrough in asymptotic FFT complexity.
"""
from __future__ import annotations
import json, math, time, pathlib, itertools
import numpy as np

ROOT=pathlib.Path(__file__).resolve().parent

def chirp_base(q:int,m:int,a:int=1,beta:int=2)->np.ndarray:
    if q%m or q//m<m or math.gcd(a,q)!=1:
        raise ValueError('require Q=KM, K>=M, and gcd(a,Q)=1')
    k=q//m
    b=np.arange(k,dtype=np.int64)[:,None]
    t=np.arange(m,dtype=np.int64)[None,:]
    tri=t*(t-1)//2
    pn=(((a*m)%q)*b*t+a*tri+beta*t)%q
    exp=(2*pn+(q&1)*t)%(2*q)
    return np.exp(1j*np.pi*exp/q)

def all_phase_summaries(x:np.ndarray,base:np.ndarray)->np.ndarray:
    """D[b,r]=sum_t base[b,t] x[b,t] exp(+2 pi i r t / M)."""
    k,m=base.shape
    x=np.asarray(x,dtype=np.complex128).reshape(k,m)
    return m*np.fft.ifft(base*x,axis=1)

def recover_from_summaries(d:np.ndarray,base:np.ndarray)->np.ndarray:
    """Exactly invertible local phase transform; O(Q log M)."""
    return (np.fft.fft(d,axis=1)/base.shape[1])*np.conj(base)

def joint_exact_from_summaries(d:np.ndarray,base:np.ndarray)->np.ndarray:
    """Exact complete-frame aggregate, without M separate Green scans.

    It remains O(Q log Q): an inverse local M transform, M K-FFTs,
    and K local M-FFTs (the classical Cooley--Tukey factorization).
    """
    k,m=base.shape
    q=k*m
    local=recover_from_summaries(d,base)
    v=np.fft.fft(local,axis=0)                    # M independent K FFTs
    ell=np.arange(k,dtype=np.float64)[:,None]
    t=np.arange(m,dtype=np.float64)[None,:]
    twiddle=np.exp(-2j*np.pi*(ell*t)/q)
    spectrum=np.fft.fft(v*twiddle,axis=1)          # K M-point FFTs
    return spectrum.T.reshape(q)/math.sqrt(q)     # k = ell + j*K

def projector_from_summaries(d:np.ndarray,base:np.ndarray,r:int)->np.ndarray:
    k,m=base.shape
    tt=np.arange(m)
    # sampled S_r=base*exp(+2pi i r t/M); P_r z=conj(S_r)*D_r
    factor=np.exp(-2j*np.pi*r*tt/m)
    return np.conj(base)*factor[None,:]*d[:,r,None]

def exact_frame_check(q:int,m:int,seed:int=1081)->dict:
    rng=np.random.default_rng(seed+q)
    x=rng.standard_normal(q)+1j*rng.standard_normal(q)
    base=chirp_base(q,m,a=1,beta=2)
    d=all_phase_summaries(x,base)
    reconstructed=recover_from_summaries(d,base).reshape(-1)
    ys=joint_exact_from_summaries(d,base)
    truth=np.fft.fft(x)/math.sqrt(q)
    projectors=np.stack([projector_from_summaries(d,base,r) for r in range(m)])
    frame=np.sum(projectors,axis=0).reshape(-1)/m
    d_independent=np.zeros_like(d)
    for r in range(m):
        for b in range(q//m):
            d_independent[b,r]=np.sum(base[b]*x.reshape(q//m,m)[b]
                             *np.exp(2j*np.pi*r*np.arange(m)/m))
    assert np.max(abs(d_independent-d))<5e-10
    checks={
      'Q':q,'M':m,'K':q//m,
      'D_independent_max_error':float(np.max(abs(d_independent-d))),
      'full_frame_max_error':float(np.max(abs(frame-x))),
      'recovered_input_max_error':float(np.max(abs(reconstructed-x))),
      'joint_spectrum_max_error':float(np.max(abs(ys-truth))),
      'input_energy':float(np.vdot(x,x).real),
      'status':'exact algebra / floating approximation verified; O(Q log Q) work'
    }
    assert checks['full_frame_max_error']<2e-10
    assert checks['joint_spectrum_max_error']<2e-10
    return checks

def finite_population_moments(q:int,m:int,seed:int=303)->dict:
    """Exhaustively check E ||((1/s)sum_{r in S} P_r-I)x||^2=(M-s)/s ||x||^2.

    Distinct chirp phases are sampled without replacement from an EXACT M-frame.
    This is a global squared l2-energy identity, not a pointwise error guarantee.
    """
    rng=np.random.default_rng(seed+q)
    x=rng.normal(size=q)+1j*rng.normal(size=q)
    base=chirp_base(q,m)
    d=all_phase_summaries(x,base)
    projections=np.stack([projector_from_summaries(d,base,r).reshape(-1) for r in range(m)])
    norm=float(np.vdot(x,x).real)
    output=[]
    for s in range(1,m+1):
        errors=[]
        for subset in itertools.combinations(range(m),s):
            recovered=np.mean(projections[list(subset)],axis=0)
            e=recovered-x
            errors.append(np.vdot(e,e).real)
        measured=float(np.mean(errors)/norm)
        theoretical=(m-s)/s
        assert abs(measured-theoretical)<2e-12, (q,m,s,measured,theoretical)
        output.append({'s':s,'mean_squared_relative_error':measured,
                       'theorem':theoretical,'subset_count':len(errors)})
    # An adversarial, deterministic per-subset input lying in an omitted phase.
    missing=m-1
    t=np.arange(m)
    kernel=np.zeros((q//m,m),dtype=complex)
    kernel[0]=np.conj(base[0])*np.exp(-2j*np.pi*missing*t/m)
    witness=kernel.reshape(-1)
    for r in range(missing):
        d_r=all_phase_summaries(witness,base)
        assert np.max(abs(projector_from_summaries(d_r,base,r)))<1e-10
    return {'Q':q,'M':m,'identity':'E_S relative l2^2=(M-s)/s, uniform size-s subsets',
            'moments':output,
            'omitted_phase_witness_norm':float(np.linalg.norm(witness)),
            'witness_results':'first M-1 phase projectors all vanish on nonzero signal'}

def benchmark(q:int,m:int,rounds:int=3)->dict:
    rng=np.random.default_rng(42)
    x=rng.normal(size=q)+1j*rng.normal(size=q)
    base=chirp_base(q,m)
    d=all_phase_summaries(x,base)
    ts=[]
    for _ in range(rounds):
        begin=time.perf_counter()
        _=joint_exact_from_summaries(d,base)
        ts.append((time.perf_counter()-begin)*1e3)
    return {'Q':q,'M':m,'joint_collapse_ms_median':float(np.median(ts)),
            'work':'Q log M (local inverse) + Q log K + Q log M'}

def main():
    qr=[(25,5),(32,4),(55,5),(77,7),(121,11),(128,8),(143,11),(517,11),(1067,11),(2057,11)]
    frames=[exact_frame_check(q,m) for q,m in qr]
    moments=[finite_population_moments(q,m) for q,m in [(15,3),(16,4),(55,5),(77,7)]]
    times=[benchmark(q,m) for q,m in [(517,11),(1067,11),(2057,11)]]
    record={'frames':frames,'finite_population':moments,'timings':times,
            'global_claim':'No new sub-Q-log-Q exact FFT; exact scan elimination reduces to Cooley--Tukey'}
    (ROOT/'verification_joint.json').write_text(json.dumps(record,indent=2))
    print(json.dumps({'n_frames':len(frames),'frame_max':max(f['full_frame_max_error'] for f in frames),
                      'fft_max':max(f['joint_spectrum_max_error'] for f in frames),
                      'finite_pop_cases':sum(len(r['moments']) for r in moments),
                      'timings':times},indent=2))
if __name__=='__main__': main()
