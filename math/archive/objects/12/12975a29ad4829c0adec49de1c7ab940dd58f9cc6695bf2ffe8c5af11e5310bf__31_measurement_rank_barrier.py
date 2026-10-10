#!/usr/bin/env python3
"""Distributional rank barrier for measurement-only Green-compressed FFTs.

For centered N-point padded data, one phase state records at most one
complex scalar per occupied M-cell. Even with arbitrary postprocessing,
s<M phase measurements leave >=(M-s)*B full-block directions unknown.
This does NOT apply to algorithms that reread input or use other measurements.
"""
from __future__ import annotations
import json, math, pathlib
import numpy as np
from joint_phase_collapse import chirp_base
ROOT=pathlib.Path(__file__).resolve().parent

def evaluate(n:int,q:int,m:int,s:int):
    assert q%m==0 and q>=4*n and q//m>=m and 1<=s<m
    center=(n-1)//2
    src=(np.arange(n)-center)%q
    base=chirp_base(q,m,a=1,beta=2)
    src_blocks=src//m
    sig2=12.
    g=np.exp(math.pi*sig2*((np.arange(n)-center)/q)**2)/math.sqrt(sig2)
    ks=np.arange(n)
    jj=np.arange(n)
    # Test oracle matrix only. It is not part of the proposed Green decoder.
    U=np.exp(-2j*np.pi*np.outer(ks,jj)/n)/math.sqrt(n)
    diag_posterior=np.zeros(n,dtype=float)
    total_rank=0
    full_blocks=0
    min_whole_rank=999
    biggest_block_kernel=None
    num_blocks=0
    for b in np.unique(src_blocks):
        indices=np.flatnonzero(src_blocks==b)
        tt=src[indices]%m
        cc=len(indices)
        if cc==m:full_blocks+=1
        # Every sampled phase is one linear measurement per occupied block.
        A=np.stack([base[b,tt]*np.exp(2j*np.pi*r*tt/m)*g[indices]
                   for r in range(s)])
        _,sing,vh=np.linalg.svd(A,full_matrices=True)
        rank=int(np.sum(sing>max(sing[0],1.)*1e-10))
        total_rank+=rank
        assert rank==min(s,cc),(n,q,m,s,b,rank,cc)
        if cc==m:min_whole_rank=min(min_whole_rank,rank)
        null=vh[rank:].conj().T
        assert null.shape[1]==cc-rank
        assert np.linalg.norm(A@null)<1e-9
        diag_posterior+=np.sum(abs(U[:,indices]@null)**2,axis=1)
        if biggest_block_kernel is None and cc==m and cc>rank:
            witness=np.zeros(n,dtype=complex)
            witness[indices]=null[:,0]
            biggest_block_kernel=witness
        num_blocks+=1
    defect=n-total_rank
    guaranteed=full_blocks*(m-s)
    trace=float(np.sum(diag_posterior))
    min_var=float(np.min(diag_posterior))
    max_var=float(np.max(diag_posterior))
    assert defect>=guaranteed
    assert abs(trace-defect)<1e-8*max(defect,1)
    assert max_var+1e-10>=defect/n
    assert biggest_block_kernel is not None
    target=np.fft.fft(biggest_block_kernel)/math.sqrt(n)
    assert np.linalg.norm(target)>1e-8
    return {
       'N':n,'Q':q,'M':m,'s_measurement_rows':s,'occupied_blocks':num_blocks,
       'fully_occupied_blocks':full_blocks,'rank_of_all_recorded_measurements':total_rank,
       'unobserved_complex_dimensions':defect,
       'guaranteed_deficit_full_blocks':guaranteed,
       'posterior_fourier_variance_trace':trace,
       'trace_relative_error':abs(trace-defect)/defect,
       'average_posterior_output_variance':float(np.mean(diag_posterior)),
       'maximum_posterior_output_variance':max_var,
       'minimum_posterior_output_variance':min_var,
       'nonzero_omitted_kernel_Fourier_l2':float(np.linalg.norm(target)),
       'interpretation':'Rank and posterior variance under an N-dimensional isotropic complex Gaussian prior; measurement-only architecture.'
    }

def main():
    cases=[(127,517,11,1),(127,517,11,3),(127,517,11,10),
           (257,1067,11,3),(257,1067,11,10),
           (509,2057,11,3)]
    out=[evaluate(*v) for v in cases]
    (ROOT/'measurement_barrier.json').write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
