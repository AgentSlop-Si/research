#!/usr/bin/env python3
"""Hero #0: exact arithmetic identity + composite-modulus random chirp projector.

For ANY n=k*m, k>=m, the unit-multiplier chirp Fourier projection can be
computed by one length-k FFT and one n-long Green/cycle scan, O(n+k log k).

No assumption about the factorization of n into a prime power is needed for
that identity. Uniformly random (a,beta) gives an unbiased full n-output
estimator with VARIANCE <= m(m-1)/phi(n) * ||x||2^2 per output (proved in
RESEARCH.md). For m=Theta(log n), one row takes O(n) in the ideal complex
arithmetic model and has small polynomially shrinking variance.

This is RANDOMIZED APPROXIMATE, not exact DFT for a single random state.
"""
from __future__ import annotations
from dataclasses import dataclass
import math
import numpy as np
import composite_cycle_core as core


@dataclass(frozen=True)
class CompositePlan:
    n:int
    m:int
    k:int

    @classmethod
    def build(cls,n:int,window_low:float=0.5,window_high:float=2.0)->'CompositePlan':
        if n<2:raise ValueError('n>=2 required')
        target=max(2.0,math.log2(n))
        low=max(2,math.floor(window_low*target))
        high=min(math.isqrt(n),math.ceil(window_high*target))
        divisors=[m for m in range(low,high+1) if n%m==0]
        if not divisors:
            raise ValueError(f'no divisor m=Theta(log n) in searched window [{low},{high}]')
        m=min(divisors,key=lambda m:(abs(math.log(m/target)), -m))
        core.validate_dimensions(n,m)
        return cls(n=n,m=m,k=n//m)


def row_estimate(x,plan:CompositePlan,state:core.ChirpState):
    arr=np.asarray(x,dtype=np.complex128).reshape(-1)
    if arr.size!=plan.n:raise ValueError('length mismatch')
    return core.one_row_estimate(arr,plan.m,state)


def robust_estimate(x,plan:CompositePlan,rows:int,seed:int=20261009):
    if rows<1 or rows%2!=1:raise ValueError('odd positive rows required')
    rng=np.random.default_rng(seed)
    arr=np.asarray(x,dtype=np.complex128).reshape(-1)
    buf=np.empty((rows,plan.n),dtype=np.complex128)
    for j in range(rows):
        buf[j]=row_estimate(arr,plan,core.draw_state(plan.n,rng))
    return np.median(buf.real,axis=0)+1j*np.median(buf.imag,axis=0)


def totient(n:int)->int:
    # Only for theoretical bound inspection / test; NOT used in the algorithm.
    if n<1:raise ValueError(n)
    result=n;d=2;z=n
    while d*d<=z:
        if z%d==0:
            while z%d==0:z//=d
            result-=result//d
        d+=1
    if z>1:result-=result//z
    return result


def variance_bound(x,plan:CompositePlan)->float:
    xx=np.asarray(x,dtype=np.complex128)
    return plan.m*(plan.m-1)/totient(plan.n)*float(np.vdot(xx,xx).real)


def theoretical_work_proxy(plan:CompositePlan)->float:
    return plan.n+plan.k*math.log2(max(2,plan.k))


def reference(x):
    arr=np.asarray(x,dtype=np.complex128)
    return np.fft.fft(arr)/math.sqrt(arr.size)


def chebyshev_median_failure_bound(n,m,rows,alpha):
    if not(0<alpha<0.5) or rows<1 or rows%2!=1:
        raise ValueError('invalid parameter')
    p=min(1.0,m*(m-1)/totient(n)*n**(2*alpha))
    return min(1.0,2*n*(2**rows)*(p**((rows+1)//2)))
