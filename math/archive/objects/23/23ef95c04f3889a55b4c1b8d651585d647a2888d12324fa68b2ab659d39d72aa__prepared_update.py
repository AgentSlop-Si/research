"""Practical streaming update for a FIXED, KNOWN sample index.

Useful complement to the conditional OpenAI-#130/sparse factoring result.
This is the classical Fourier rank-one update, not a new theorem.
"""
import numpy as np

class PreparedPointEdit:
    """Maintain rFFT(x) for repeated known changes at one input position."""
    def __init__(self,n:int,index:int):
        if n<1 or index<0 or index>=n:
            raise ValueError('invalid length or index')
        self.n,self.index=n,index
        k=np.arange(n//2+1,dtype=np.float64)
        self.phase=np.exp((-2j*np.pi*index/n)*k)
    def update(self,cached_rfft,delta):
        arr=np.asarray(cached_rfft)
        if arr.ndim!=1 or arr.size!=self.phase.size:
            raise ValueError('incorrect spectrum')
        if complex(delta).imag!=0:
            raise ValueError('only real delta supported by rFFT')
        return arr + delta*self.phase
