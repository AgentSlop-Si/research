"""Exact full-rank *stationary Toeplitz* noncommuting chirp frame.

For G=KM, K>=M, choose q<=M states indexed i:
  a_i=1+i*K, beta_{s,i}=3s+i*(K+1)   modulo G.
All a_i are odd units when G is a power of 2. In block r, the conjugated
chirp vectors factor as V_{s,r}=D_{s,r} W where D diagonal unimodular and
  W[u,i] = z_u^i, z_u = zeta^(-[K*C(u,2)+(K+1)*u]).
The nodes are DISTINCT: their exponents reduce to u (mod K), with 0<=u<M<=K.
Thus any q columns are linearly independent; q=M spans every input block.
Gamma=W*W is Hermitian TOEPLITZ, independent of s,r and input data.
Factor the same qxq Gram ONCE, not once per block. Decoders still require
q separate length-G scans per input column: exact full-rank q=M has O(NM)
scan work, NOT an exact sub-NlogN FFT for M~log G.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import math
import numpy as np
import one_root_chirp as orc
import phase_bank as bank
import unit_step_core as core


@dataclass
class ToeplitzResult:
    output:np.ndarray
    q:int
    M:int
    K:int
    G:int
    m:int
    input_energy:float
    captured_energy:float
    squared_residual_formula:float
    gram_condition:float
    gram_toeplitz_defect:float
    used_all_full_rank_channels:bool
    operation_proxy:dict


def stationary_states(g:int,m:int,M:int,q:int):
    if g<4 or g&(g-1) or M<2 or q<1 or q>M or g//M<M:
        raise ValueError('Requires dyadic g>=M*M, M>=2, 1<=q<=M')
    K=g//M
    return tuple(tuple(core.ChirpState(1+i*K,(3*s+i*(K+1))%g)
                       for i in range(q)) for s in range(m))


def construction(g:int,M:int,q:int,roots:np.ndarray|None=None):
    if g<4 or g&(g-1) or M<2 or q<1 or q>M or g//M<M:
        raise ValueError('Invalid full-rank frame dimensions')
    K=g//M
    if roots is None:roots=orc.one_root_table(g)
    u=np.arange(M,dtype=np.int64)
    e=(K*(u*(u-1)//2)+(K+1)*u)%g
    assert np.unique(e%K).size==M # exactly u, so Vandermonde nodes distinct
    w=roots[(-np.outer(e,np.arange(q,dtype=np.int64)))%g] # (M,q)
    gram=w.conj().T@w
    delta=float(np.max(np.abs(gram[1:,1:]-gram[:-1,:-1]))) if q>1 else 0.
    return w,gram,delta


def stationary_eval(x:np.ndarray,block:int,q:int)->ToeplitzResult:
    v,g,m,M,K,unused=bank._setup(x,block,None)
    if g<4 or M<2:raise ValueError('Dyadic G>=4 and M>=2 required')
    if not(1<=q<=M):raise ValueError('q outside 1..M')
    roots=orc.one_root_table(g)
    W,Gamma,toep_def=construction(g,M,q,roots)
    cond=float(np.linalg.cond(Gamma))
    if not np.isfinite(cond) or cond>1e11:
        raise ValueError('Stationary Gram too ill-conditioned for float64 demo')
    families=stationary_states(g,m,M,q)
    stage=np.zeros((g,m),dtype=np.complex128)
    cols=v.reshape(g,m)
    captured=0.
    # Constant Gram reused over all K blocks and all m columns.
    # np.linalg.solve is passed K RHS per input column, one matrix reused.
    for s in range(m):
        base_state=families[s][0]
        D=np.conj(orc.local_phases(g,M,base_state,roots)) # (K,M)
        adjusted=np.conj(D)*cols[:,s].reshape(K,M)
        B=adjusted@W.conj() # (K,q), b=V^*x
        C=np.linalg.solve(Gamma,B.T).T # (K,q)
        captured+=float(np.vdot(B,C).real)
        for i,st in enumerate(families[s]):
            stage[:,s]+=orc.decode(C[:,i],g,M,st,roots)
    output=bank._final_ct(stage,g,m)
    energy=float(np.vdot(v,v).real)
    proxy={
        'shared_root_table':g,
        'shared_toeplitz_gram_construction':M*q*q,
        'shared_gram_inversion_proxy':q*q*q,
        'all_block_coefficients':m*K*M*q,
        'all_block_reused_gram_solves':m*K*q*q,
        'dyadic_green_scans':m*q*g,
        'short_K_ffts':m*q*K*math.log2(max(2,K)),
        'shared_odd_fft':v.size*math.log2(max(2,m)) if m>1 else 0,
        'twiddle_and_output':2*v.size,
    }
    proxy['total_proxy']=sum(proxy.values())
    return ToeplitzResult(output,q,M,K,g,m,energy,captured,
                          max(0.,energy-captured),cond,toep_def,
                          q==M,proxy)
