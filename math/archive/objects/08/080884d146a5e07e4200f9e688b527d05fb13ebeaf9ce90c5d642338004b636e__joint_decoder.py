"""Phase 15: exact-arithmetic collapse of the phase-14 full-rank stationary bank.

For G=KM, 2-adic G, 2<=M<=K, and odd m=N/G, stationary states
    a_i=1+i*K, beta_{s,i}=3*s+i*(K+1)
produce local input x_{s,r,u}=D_{s,r,u} sum_i W_{u,i} c_{s,r,i}.

After q=M, W is invertible, so the sum_i W c can be fused FIRST to yield
D^-1*x directly. The joint noncommuting decoder now takes M K-FFTs and K
M-FFTs per odd column -- i.e. Cooley-Tukey in a diagonal gauge. It eliminates
all q long cyclic scans, but does NOT beat O(N log N).

The numerical implementation is diagnostic (float64, one-root tables); the
proof and exact independent finite-field auditor are in THEOREM.md and
field_joint_audit.py.
"""
from __future__ import annotations
from dataclasses import dataclass
import math
import numpy as np
import sys
from pathlib import Path
import one_root_chirp as orc
import phase_bank as bank
import stationary_toeplitz as st


@dataclass
class JointResult:
    output: np.ndarray
    G: int
    M: int
    K: int
    odd_m: int
    root_table_entries: int
    short_K_ffts: int
    short_M_ffts: int
    short_odd_ffts: int
    long_green_scans: int
    linear_phase_prepost_ops: int
    declared_butterfly_proxy: float


def joint_collapsed(x: np.ndarray, M: int) -> JointResult:
    """Compute normalized FFT_N on all inputs, with *no* G-length scans.

    Two nested short FFT layers are FULLY CHARGED. No N-FFT backend call.
    The decomposition is a conjugated Cooley-Tukey, NOT a new speedup.
    """
    vec,G,m,M,K,_=bank._setup(x,M,None)
    if G<4 or M<2 or K<M:raise ValueError('Require G>=M^2, M>=2')
    roots=orc.one_root_table(G)
    u=np.arange(M,dtype=np.int64)
    r=np.arange(K,dtype=np.int64)[:,None]
    tri=u*(u-1)//2
    cols=vec.reshape(G,m)
    stage=np.empty((G,m),dtype=np.complex128)
    v=np.arange(K,dtype=np.int64)[:,None]
    ell=np.arange(M,dtype=np.int64)
    for s in range(m):
        # D_{r,u}=zeta^{-[tri(u)+(Mr+3s)u]}
        # x / D is the common coefficient stream after Wc is fused.
        prep=roots[(tri[None,:]+(M*r+3*s)*u[None,:])%G]
        streams=(prep*cols[:,s].reshape(K,M))
        # M independent K-point FFTs (the unavoidable remaining expensive layer).
        h=np.fft.fft(streams,axis=0)
        # The shifted index v+u is essential: slope-dependent terms
        # a_i M r u are constant mod G and thus all channels use it.
        gathered=h[((v+u[None,:])%K),u[None,:]]
        phase=roots[(-v*u[None,:]-tri[None,:]-3*s*u[None,:])%G]
        rows=phase*gathered
        # K independent M-point FFTs, not M long G-step Green scans.
        short=np.fft.fft(rows,axis=1)/math.sqrt(G)
        for t in range(M):stage[t*K:(t+1)*K,s]=short[:,t]
    out=bank._final_ct(stage,G,m)
    # The bookkeeping is an arithmetic proxy, not a benchmark or complexity LB.
    k_proxy=m*M*K*math.log2(max(K,2))
    m_proxy=m*K*M*math.log2(max(M,2))
    odd_proxy=G*m*math.log2(max(m,2)) if m>1 else 0
    return JointResult(out,G,M,K,m,G,m*M,m*K,G if m>1 else 0,
                       0,5*G*m, k_proxy+m_proxy+odd_proxy+5*G*m+G)


def explicit_frame_joint_check(x: np.ndarray, M: int) -> tuple[np.ndarray,np.ndarray,float]:
    """Deliberately *slow* mathematical diagnostic, NOT a faster algorithm.

    Build the Phase14 noncommuting W coefficients, do M K-FFTs, and multiply
    by W *after* those FFTs. Compare to pre-fusing W before K-FFTs.
    The slow explicit W readback exposes the commuting diagram.
    """
    vec,G,m,M,K,_=bank._setup(x,M,None)
    if K<M:raise ValueError('K>=M required')
    roots=orc.one_root_table(G)
    W,gram,_=st.construction(G,M,M,roots)
    u=np.arange(M,dtype=np.int64)
    rr=np.arange(K,dtype=np.int64)
    tri=u*(u-1)//2
    stage=np.empty((G,m),complex)
    coeff_err=0.
    for s in range(m):
        dinv=roots[(tri[None,:]+(M*rr[:,None]+3*s)*u[None,:])%G]
        adjusted=dinv*vec.reshape(G,m)[:,s].reshape(K,M)
        # Wc=adjusted. This O(K M^3) generic numerical solve is
        # verification only; never label it fast.
        c=np.linalg.solve(W,adjusted.T).T
        coeff_err=max(coeff_err,float(np.max(abs(c@W.T-adjusted))))
        cfft=np.fft.fft(c,axis=0)
        for v in range(K):
            gathered=cfft[(v+u)%K,:] # (M output u, M frame indices)
            full=np.sum(gathered*W,axis=1)
            row=roots[(-v*u-tri-3*s*u)%G]*full
            fftrow=np.fft.fft(row)/math.sqrt(G)
            for t in range(M):stage[v+K*t,s]=fftrow[t]
    return bank._final_ct(stage,G,m),joint_collapsed(vec,M).output,coeff_err
