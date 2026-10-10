"""Output-pruned DFT helpers for projected Fourier views.

The fast path implements the classical first-K-output pruning for N=K*M:
reshape into M strided length-K transforms, compute those K-point FFTs, then
sum each desired output with its Cooley--Tukey twiddle.  Arithmetic complexity
is O(N log K) and working storage is O(N) for one streamed basis vector.

This is classical pruning, not a new FFT algorithm.  The purpose here is to
avoid ever storing an r-by-N basis spectrum when a consumer only needs K bins.
"""
from __future__ import annotations
import numpy as np
try:
    from scipy import fft as sp_fft
except ImportError:
    sp_fft=None


def first_k_dft(x, k: int, *, backend='scipy') -> np.ndarray:
    a=np.asarray(x,dtype=np.complex128)
    if a.ndim!=1 or a.size<1: raise ValueError('x must be nonempty 1-D')
    n=a.size; k=int(k)
    if k<1 or k>n or n%k: raise ValueError('k must divide n and satisfy 1<=k<=n')
    m=n//k
    # group[m,r] = x[m + M*r]
    groups=np.ascontiguousarray(a.reshape(k,m).T)
    if backend=='scipy' and sp_fft is not None:
        inner=sp_fft.fft(groups,axis=1)
    elif backend in ('scipy','numpy'):
        inner=np.fft.fft(groups,axis=1)
    else: raise ValueError('backend must be scipy or numpy')
    mm=np.arange(m,dtype=np.float64)[:,None]
    kk=np.arange(k,dtype=np.float64)[None,:]
    tw=np.exp((-2j*np.pi/n)*(mm*kk))
    return np.sum(inner*tw,axis=0)


def stream_basis_first_k(basis_vectors, k:int, *, backend='scipy') -> np.ndarray:
    """Build an r-by-k projection one basis vector at a time.

    ``basis_vectors`` may be a generator, so only one N-vector plus the final
    r-by-k projection need be live if the caller streams its basis source.
    """
    rows=[first_k_dft(row,k,backend=backend) for row in basis_vectors]
    if not rows:return np.empty((0,int(k)),dtype=np.complex128)
    return np.ascontiguousarray(np.stack(rows))


class FirstKDFTPlan:
    """Reusable first-K-output pruning plan for many length-N inputs."""
    def __init__(self,n:int,k:int,*,backend='scipy'):
        self.n=int(n); self.k=int(k); self.backend=backend
        if self.n<1 or self.k<1 or self.k>self.n or self.n%self.k:
            raise ValueError('k must divide n')
        self.m=self.n//self.k
        mm=np.arange(self.m,dtype=np.float64)[:,None]
        kk=np.arange(self.k,dtype=np.float64)[None,:]
        self.twiddle=np.exp((-2j*np.pi/self.n)*(mm*kk))
    @property
    def plan_bytes(self): return int(self.twiddle.nbytes)
    def execute(self,x):
        a=np.asarray(x,dtype=np.complex128)
        if a.shape!=(self.n,): raise ValueError('input has wrong length')
        groups=np.ascontiguousarray(a.reshape(self.k,self.m).T)
        if self.backend=='scipy' and sp_fft is not None:
            inner=sp_fft.fft(groups,axis=1)
        elif self.backend in ('scipy','numpy'):
            inner=np.fft.fft(groups,axis=1)
        else: raise ValueError('backend must be scipy or numpy')
        return np.einsum('mk,mk->k',inner,self.twiddle,optimize=False)
    def project_stream(self,basis_vectors):
        rows=[self.execute(row) for row in basis_vectors]
        return np.ascontiguousarray(np.stack(rows)) if rows else np.empty((0,self.k),dtype=np.complex128)

class BandDFTPlan:
    """Reusable pruning plan for K consecutive bins starting at ``start``.

    Modulation shifts the requested band to bins 0..K-1, then FirstKDFTPlan
    applies.  Complexity remains O(N log K), with one extra O(N) multiply.
    """
    def __init__(self,n:int,k:int,start:int,*,backend='scipy'):
        self.n=int(n); self.k=int(k); self.start=int(start)%self.n
        self.inner=FirstKDFTPlan(self.n,self.k,backend=backend)
        idx=np.arange(self.n,dtype=np.float64)
        self.modulation=np.exp((-2j*np.pi*self.start/self.n)*idx)
    @property
    def plan_bytes(self): return int(self.inner.plan_bytes+self.modulation.nbytes)
    def execute(self,x):
        a=np.asarray(x,dtype=np.complex128)
        if a.shape!=(self.n,): raise ValueError('input has wrong length')
        return self.inner.execute(a*self.modulation)
