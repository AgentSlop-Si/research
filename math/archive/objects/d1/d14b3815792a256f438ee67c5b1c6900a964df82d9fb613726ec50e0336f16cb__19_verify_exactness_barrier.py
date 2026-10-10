#!/usr/bin/env python3
"""Exact frame identity and constant-row noninjectivity gate.

The rank counterexample chooses x *after* fixing the sampled chirps.
It is a deterministic-per-seed obstruction, not an attack on the
per-fixed-input randomized approximation guarantee.
"""
from __future__ import annotations
import json,math,pathlib
import numpy as np
from coprime_pad import build_plan
from gaussian_lift import prepare_centered_weighted_input
from composite_cycle_core import (ChirpState,local_phase_matrix,
     materialize_projected_signal,one_row_estimate,draw_state)
ROOT=pathlib.Path(__file__).resolve().parent
RNG=np.random.default_rng(20261010)


def exact_frame_identity(q,m):
    k=q//m
    assert k>=m
    a=next(a for a in range(1,q) if math.gcd(a,q)==1)
    beta0=2%k
    x=RNG.normal(size=q)+1j*RNG.normal(size=q)
    sumP=np.zeros(q,dtype=np.complex128)
    sumY=np.zeros(q,dtype=np.complex128)
    for r in range(m):
        st=ChirpState(a,(beta0+r*k)%q)
        sumP+=materialize_projected_signal(x,m,st)
        sumY+=one_row_estimate(x,m,st)
    recon=sumP/m
    spectral=sumY/m
    truth=np.fft.fft(x)/math.sqrt(q)
    timeerr=float(np.max(abs(recon-x)))
    specerr=float(np.max(abs(spectral-truth)))
    assert timeerr<1e-10,(q,timeerr)
    assert specerr<1e-10,(q,specerr)
    return {'q':q,'m':m,'cofactor_k':k,'a':a,'max_time_error':timeerr,
            'max_fourier_error':specerr,
            'separate_Green_row_count':m,
            'straightforward_work':'Theta(Q*M), not a faster FFT'}


def kernel_witness(n,rows=7):
    p=build_plan(n)
    assert rows<p.m
    states=[draw_state(p.q,RNG) for _ in range(rows)]
    support=(np.arange(n)-p.center)%p.q
    # Choose an entirely supported M-cell block.
    occupied=np.unique(support//p.m)
    b=next(int(b) for b in occupied if np.count_nonzero(support//p.m==b)==p.m)
    source_indices=np.flatnonzero(support//p.m==b)
    global_idx=support[source_indices]
    local_idx=global_idx%p.m
    sampling=[]
    for state in states:
        ph=local_phase_matrix(p.q,p.m,state)[b,local_idx]
        sampling.append(ph)
    D=np.stack(sampling)
    _,sv,vh=np.linalg.svd(D,full_matrices=True)
    kern=vh[-1].conjugate()
    kern/=np.linalg.norm(kern)
    z=np.zeros(p.q,dtype=complex)
    z[global_idx]=kern
    rawtime=(global_idx.astype(int))
    tt=np.where(rawtime<=(p.q-1)//2,rawtime,rawtime-p.q)/p.q
    g=np.exp(math.pi*p.sigma2*tt*tt)/math.sqrt(p.sigma2)
    x=np.zeros(n,dtype=complex)
    x[source_indices]=kern/g
    assert np.linalg.norm(x)>0
    max_meas=max(float(np.max(abs(local_phase_matrix(p.q,p.m,s)[b]@z[b*p.m:(b+1)*p.m]))) for s in states)
    max_y=max(float(np.max(abs(one_row_estimate(z,p.m,s)))) for s in states)
    target=np.fft.fft(x)/math.sqrt(n)
    lower_bound=np.linalg.norm(x)/math.sqrt(n)
    assert max_meas<1e-10, max_meas
    assert max_y<1e-9, max_y
    assert np.max(abs(target))+1e-13>=lower_bound
    return {'n':n,'q':p.q,'m':p.m,'number_of_independent_rows':rows,
            'occupied_full_block':b,'nullspace_dimension_at_least':p.m-rows,
            'max_abs_recorded_measurement':max_meas,
            'max_abs_projected_fourier_output':max_y,
            'nonzero_target_fourier_inf':float(np.max(abs(target))),
            'target_l2_norm':float(np.linalg.norm(x)),
            'universal_fourier_inf_lower_bound':float(lower_bound),
            'interpretation':'Witness chosen after fixing seeds, not a fixed-input randomized failure'}


def main():
    frames=[exact_frame_identity(55,5),exact_frame_identity(517,11),exact_frame_identity(1067,11)]
    kernels=[kernel_witness(127),kernel_witness(257),kernel_witness(509)]
    r={'exact_resolution_of_identity':frames,'noninjectivity_witnesses':kernels}
    (ROOT/'verification_exactness.json').write_text(json.dumps(r,indent=2))
    print(json.dumps(r,indent=2))
if __name__=='__main__':main()
