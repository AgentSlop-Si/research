"""Vectorized numerical backend for the sparse-surrogate experiment.

Same radix identity as hybrid_sparse.sparse_dft, but vectorizes the O(N)
phase construction to avoid Python loops over sampled support.
"""
from __future__ import annotations
import math
import numpy as np
try:
    from scipy import fft as sp_fft
except Exception:
    sp_fft=None


def sparse_dft_vectorized(n:int, sparse:dict[int,complex]) -> tuple[np.ndarray,int]:
    if n<1 or n&(n-1): raise ValueError('n must be power of two')
    if not sparse: return np.zeros(n,dtype=np.complex128),1
    js=np.fromiter(sparse.keys(),dtype=np.int64,count=len(sparse))
    vals=np.fromiter(sparse.values(),dtype=np.complex128,count=len(sparse))
    k=len(js); b=1<<(max(1,k)-1).bit_length(); m=n//b
    r=(js % b).astype(np.intp); t=(js//b).astype(np.float64)
    q=np.arange(m,dtype=np.float64)
    # phase[s,q] = exp(-2pi i * t_s*q/m), at most k*m <= N terms.
    phase=np.exp((-2j*np.pi/m)*np.outer(t,q))
    contrib=vals[:,None]*phase
    intermediate=np.zeros((b,m),dtype=np.complex128)
    # Scatter-add sampled rows by residue r, fully in compiled NumPy.
    np.add.at(intermediate,r,contrib)
    active=np.unique(r)
    if active.size:
        tw=np.exp((-2j*np.pi/n)*np.outer(active.astype(float),q))
        intermediate[active,:]*=tw
    a=intermediate.T # (m,b)
    if sp_fft is not None: freq=sp_fft.fft(a,axis=1)
    else: freq=np.fft.fft(a,axis=1)
    return np.asarray(freq.T.reshape(n),dtype=np.complex128),b
