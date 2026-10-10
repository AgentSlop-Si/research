#!/usr/bin/env python3
"""Unitarity/full-rank gate for local transfer between complete Green phases.

The MxM coefficient coupling between phase summaries D[b,r] and outputs
k=ell+jK is U_M diag(conj(s[b,t])*omega_Q^(ell*t)) U_M^T.
Every singular value is one. Exact local rank reduction r<M incurs
spectral error >=1 (Eckart-Young), independent of input distribution.
"""
import json, math, pathlib
import numpy as np
from joint_phase_collapse import chirp_base,all_phase_summaries
ROOT=pathlib.Path(__file__).resolve().parent

def gate(q,m,ell,b):
    k=q//m
    assert 0<=ell<k and 0<=b<k
    base=chirp_base(q,m)
    t=np.arange(m)
    unit=np.fft.fft(np.eye(m),axis=0)/math.sqrt(m)
    weights=np.conj(base[b])*np.exp(-2j*np.pi*ell*t/q)
    return unit@np.diag(weights)@unit.T

def verify(q,m,ells=None,bs=None):
    k=q//m
    if ells is None:ells=[0,min(1,k-1),k//2,k-1]
    if bs is None:bs=[0,min(1,k-1),k//2,k-1]
    rng=np.random.default_rng(q+m)
    xx=rng.normal(size=q)+1j*rng.normal(size=q)
    base=chirp_base(q,m)
    D=all_phase_summaries(xx,base)
    errors=[];singular=[];single_block_errors=[]
    for ell in ells:
        for b in bs:
            T=gate(q,m,ell,b)
            errors.append(float(np.linalg.norm(T.conj().T@T-np.eye(m),ord=2)))
            s=np.linalg.svd(T,compute_uv=False)
            singular.extend(float(z) for z in s)
            # Isolate one supported source block. Frequency response uses
            # omega_K^(ell*b) T D_b / sqrt(Q), for all j in 0..M-1.
            xb=np.zeros(q,dtype=complex)
            xb[b*m:(b+1)*m]=xx[b*m:(b+1)*m]
            oracle=np.fft.fft(xb)/math.sqrt(q)
            targets=oracle[ell+k*np.arange(m)]
            blockfactor=np.exp(-2j*np.pi*ell*b/k)
            predicted=blockfactor*(T@D[b])/math.sqrt(q)
            single_block_errors.append(float(np.max(abs(predicted-targets))))
    assert max(errors)<2e-12
    assert min(singular)>1-2e-12 and max(singular)<1+2e-12
    assert max(single_block_errors)<2e-12
    return {'Q':q,'M':m,'K':k,'number_of_transfer_matrices':len(ells)*len(bs),
            'max_unitarity_residual':max(errors),'smallest_singular_value':min(singular),
            'largest_singular_value':max(singular),
            'max_one_block_frequency_response_error':max(single_block_errors),
            'low_rank_obstruction':'for any rank r<M, best operator-norm error equals 1'}

def main():
    res=[verify(q,m) for q,m in [(25,5),(32,4),(55,5),(77,7),(121,11),(128,8),(143,11),(517,11),(1067,11),(2057,11)]]
    (ROOT/'phase_transfer_gate.json').write_text(json.dumps(res,indent=2))
    print(json.dumps(res,indent=2))
if __name__=='__main__':main()
