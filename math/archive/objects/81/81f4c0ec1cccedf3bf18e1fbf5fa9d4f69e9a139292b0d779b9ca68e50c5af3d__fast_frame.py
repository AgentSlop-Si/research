"""Uniformly conditioned stationary-frame *approximate* inverse, K>=4M.

A = U + E, where U is an M-point Fourier matrix with triangular-row
permutation. A can be applied to accuracy controlled by a Fourier-based
centered exponential series, requiring (P+1) M-point FFTs rather than a
quadratic dense matrix multiply. A left-Fourier preconditioned stationary
iteration converges geometrically since ||U^-1 E||_2 <= delta < 1.

Approximating W^-1 is not an exact transform and does not eliminate the
M K-point FFTs in the full-rank decoder. Float64 numerical output is NOT
an interval error certificate; the exact-arithmetic norm bounds are proved
in THEOREM.md.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import exp, factorial, pi, sqrt
import numpy as np


def validate(M:int,K:int):
    if M<2 or M&(M-1) or K<M*4 or K&(K-1):
        raise ValueError('Require dyadic M>=2 and dyadic K>=4M')


def triangular_perm(M:int):
    return np.array([(u*(u+1)//2)%M for u in range(M)],dtype=int)


def parameters(M:int,K:int):
    validate(M,K)
    uc=(M-1)/2.
    u=np.arange(M,dtype=float)-uc
    i=np.arange(M,dtype=float)-uc
    phase_scalar=np.exp(2j*pi*uc*uc/(K*M))
    row=np.exp(-2j*pi*uc*np.arange(M)/(K*M))
    col=np.exp(-2j*pi*uc*np.arange(M)/(K*M))
    return u,i,row,col,phase_scalar,triangular_perm(M)


def U_apply(x,perm):
    return np.fft.fft(x)[perm]


def U_inverse(x,perm):
    reorder=np.empty_like(x)
    reorder[perm]=x
    return np.fft.ifft(reorder)


def A_series(z:np.ndarray,M:int,K:int,P:int,params=None):
    if params is None:params=parameters(M,K)
    u,i,_,_,_,perm=params
    if P<0:raise ValueError('P must be nonnegative')
    coeff=1.+0j
    lhs=np.zeros(M,complex)
    i_pow=np.ones(M)
    u_pow=np.ones(M)
    for p in range(P+1):
        lhs+=coeff*u_pow*U_apply(i_pow*z,perm)
        if p<P:
            coeff*=(-2j*pi/(K*M))/(p+1)
            i_pow*=i
            u_pow*=u
    return lhs


def W_series(c:np.ndarray,M:int,K:int,P:int):
    params=parameters(M,K)
    _,_,row,col,scale,_=params
    return scale*row*A_series(col*c,M,K,P,params)


def fast_inverse(y:np.ndarray,M:int,K:int,P:int,iterations:int):
    """Return approximate coefficient c solving Wc=y, plus rigorous
    exact-arithmetic *relative operator* bound on ||c-c_true||.
    """
    params=parameters(M,K)
    _,_,row,col,scale,perm=params
    y=np.asarray(y,dtype=complex)
    if y.shape!=(M,):raise ValueError('y has wrong length')
    if iterations<0:raise ValueError('iterations must be nonnegative')
    b=np.conj(scale*row)*y
    z=np.zeros(M,complex)
    for _ in range(iterations):
        z+=U_inverse(b-A_series(z,M,K,P,params),perm)
    c=np.conj(col)*z
    lam=pi*(M-1)**2/(2*K*M)
    delta=exp(lam)-1
    deltaP=sum(lam**p/factorial(p) for p in range(1,P+1))
    # Tail bound from positive exponential power series.
    tau=lam**(P+1)/factorial(P+1)/(1-lam/(P+2))
    assert delta<1 and deltaP<1
    bound= (deltaP**iterations/(1-deltaP)+
            tau/((1-delta)*(1-deltaP)))*np.linalg.norm(y)/sqrt(M)
    return c,bound,{'M':M,'K':K,'truncation_degree':P,
                    'iterations':iterations,'lambda':lam,
                    'neumann_contraction_upper':delta,
                    'series_tail_upper':tau,
                    'local_M_ffts_charged':iterations*(P+2)}
