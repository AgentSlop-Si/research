#!/usr/bin/env python3
"""Exact beta-complete Green frame with O(Q log M) batched input compression.

Still O(Q log Q) total: M separate K-FFTs and M cycle scans remain.
This is a truthful exactness checkpoint, not an asymptotic FFT improvement.
"""
import math, json, pathlib
import numpy as np
from composite_cycle_core import (ChirpState,local_phase_matrix,
                                  compress_blocks,decode_balanced_scan)
from coprime_pad import build_plan

def batch_summaries(x,m,a=1,beta0=0):
    x=np.asarray(x,dtype=complex).reshape(-1)
    q=x.size;k=q//m
    base=local_phase_matrix(q,m,ChirpState(a,beta0%q))
    local=base*x.reshape(k,m)
    # beta_r=beta0+r*K, factor exp(2*pi*i*r*t/M)
    # inverse M-point FFT has + sign and 1/M normalization.
    return (m*np.fft.ifft(local,axis=1)).T

def check(q,m,seed=20261010):
    rng=np.random.default_rng(seed)
    x=rng.normal(size=q)+1j*rng.normal(size=q)
    a=next(a for a in range(1,q) if math.gcd(a,q)==1)
    beta0=2
    batched=batch_summaries(x,m,a,beta0)
    naive=np.array([compress_blocks(x,m,ChirpState(a,(beta0+r*(q//m))%q)) for r in range(m)])
    err_d=float(np.max(abs(batched-naive)))
    assert err_d<1e-11,(q,m,err_d)
    approx_spectrum=np.zeros(q,dtype=complex)
    for r in range(m):
        approx_spectrum+=decode_balanced_scan(batched[r],q,m,
              ChirpState(a,(beta0+r*(q//m))%q))
    approx_spectrum/=m
    truth=np.fft.fft(x)/math.sqrt(q)
    err_fft=float(np.max(abs(approx_spectrum-truth)))
    assert err_fft<1e-10,(q,m,err_fft)
    return {'q':q,'m':m,'k':q//m,
        'batched_input_compression_max_error':err_d,
        'full_exact_transform_max_error':err_fft,
        'batched_compression_arithmetic':'O(Q log M)',
        'remaining_K_FFT_work':'O(Q log(Q/M))',
        'remaining_M_cycle_scans':'O(Q M)',
        'total_cost':'O(Q log Q), no asymptotic advance'}

if __name__=='__main__':
    rec=[check(55,5),check(517,11),check(1067,11),check(build_plan(509).q,build_plan(509).m)]
    pathlib.Path(__file__).with_name('verification_batch.json').write_text(json.dumps(rec,indent=2))
    print(json.dumps(rec,indent=2))
