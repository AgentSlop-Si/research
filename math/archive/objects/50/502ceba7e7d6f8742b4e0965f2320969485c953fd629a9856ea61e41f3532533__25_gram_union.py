"""Noncommuting chirp-frame *union* projector, a v14 extension.

For each dyadic length-G input column s, choose q_s (possibly different)
unit-step chirp states. In each consecutive length-M block form the M x q
matrix V of their conjugated phase vectors; form Gram Gamma=V*V and
coefficients c=Gamma^{-1} V* x_block. This is the orthogonal projector on
span(V). Each c_i[r] is decoded using exactly one fast unit-step Green-like
cyclic scan and K-point FFT, followed by a SINGLE shared odd-factor FFT.

The exact-arithmetic error *without any reference Fourier transform* is
||F_N x - y||_2^2 = ||x||_2^2 - sum_r (V*x)^* Gamma^{-1}(V*x).

With q bounded and fixed odd factor, G/M>=M and M~log G, the arithmetic cost
is O(N) (for fixed promised states). Some pairs of chirp projectors are
nonorthogonal and noncommuting. Generic x requires q=Theta(M) for exactness.
Numerical conditioning is NOT an exact bit precision certificate.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence
import math
import numpy as np
import unit_step_core as core
import mixedradix as old
import phase_bank as bank
import one_root_chirp as orc


@dataclass
class GramResult:
    output:np.ndarray
    energy:float
    captured_energy:float
    residual_squared:float
    relative_l2_error_certificate:float
    maximum_gram_condition:float
    state_count:int
    maximum_local_span:int
    g:int
    m:int
    M:int
    K:int
    work_proxy:dict
    # Shaped per-column (K,M), if diagnostic requested.
    projected_input:np.ndarray|None


def example_noncommuting_states(g:int,m:int,M:int)->tuple[tuple[core.ChirpState,...],...]:
    """Well-conditioned two-slope demo for g>=16, even M>=2.

    a_2=1+g/4 is odd when g>=8 and generates a nonorthogonal pair for
    beta offset 1 in the tested even lengths. General noncommutation is
    not claimed for every parameter; test the actual overlaps.
    """
    if g<16 or (g&(g-1)) or M<2:
        raise ValueError('Example needs dyadic g>=16 and M>=2')
    return tuple((core.ChirpState(a=1,beta=(3*s)%g),
                  core.ChirpState(a=1+g//4,beta=(3*s+1)%g))
                 for s in range(m))


def union_projection(x:np.ndarray,
                     families:Sequence[Sequence[core.ChirpState]],
                     block:int|None=None,diagnostic_projected:bool=False,
                     condition_limit:float=1e11)->GramResult:
    """Apply full-N Fourier to the blockwise orthogonal union projection.

    Gamma can be singular if repeated or dependent chirp vectors are chosen.
    Numerical code explicitly refuses severe conditioning rather than
    claiming an exact-arithmetic theorem has been stably implemented.
    """
    vec,g,m,M,K,unused=bank._setup(x,block,None)
    if len(families)!=m:
        raise ValueError('One family of states per odd-part input column')
    if not np.isfinite(condition_limit) or condition_limit<1:
        raise ValueError('condition_limit must be finite and >=1')
    families=[tuple(f) for f in families]
    for fam in families:
        if len(fam)>M:
            raise ValueError('Cannot choose q>M independent local vectors')
        if g>1:
            for st in fam:st.validate(g)
        elif len(fam)>1:
            raise ValueError('Odd-only case M=1')
    cols=vec.reshape(g,m)
    stages=np.zeros((g,m),dtype=np.complex128)
    projection=np.zeros((g,m),dtype=np.complex128) if diagnostic_projected else None
    captured=0.
    max_condition=1.
    total_states=0
    gram_work=0
    if g==1:
        for s,fam in enumerate(families):
            if fam:
                stages[0,s]=vec[s]
                captured+=float(abs(vec[s])**2)
                if projection is not None:projection[0,s]=vec[s]
                total_states+=1
    else:
        roots=orc.one_root_table(g)
        for s,fam in enumerate(families):
            q=len(fam)
            if not q:continue
            total_states+=q
            # V[r,u,i]=conj(S_i[r,u]), unit-norm columns sqrt(M).
            v=np.stack([np.conj(orc.local_phases(g,M,st,roots))
                        for st in fam],axis=2)  # (K,M,q)
            data=cols[:,s].reshape(K,M)
            b=np.einsum('kui,ku->ki',v.conj(),data,optimize=True)
            gamma=np.einsum('kui,kuj->kij',v.conj(),v,optimize=True)
            # Ensure local coordinates span q dimensions in *every* block.
            condition=np.linalg.cond(gamma)
            maximum=float(np.max(condition))
            if not np.isfinite(maximum) or maximum>condition_limit:
                raise ValueError('Gram is singular or too ill-conditioned for this float implementation')
            max_condition=max(max_condition,maximum)
            coeff=np.linalg.solve(gamma,b[...,None])[...,0]
            captured+=float(np.vdot(b,coeff).real)
            if projection is not None:
                projection[:,s]=np.einsum('kui,ki->ku',v,coeff,optimize=True).reshape(g)
            for i,st in enumerate(fam):
                stages[:,s]+=orc.decode(coeff[:,i],g,M,st,roots)
            gram_work+=K*(q*q*M + q*q*q)
    out=bank._final_ct(stages,g,m)
    energy=float(np.vdot(vec,vec).real)
    residual=max(0.,energy-captured)
    proxy={
        'phase_and_projection_work':(total_states*g) if g>1 else 0,
        'dyadic_root_table_preparation':g if g>1 else 0,
        'local_gram_and_solve_proxy':gram_work,
        'dyadic_green_scans':(total_states*g) if g>1 else 0,
        'selected_K_fft_proxy':(total_states*K*math.log2(max(2,K))) if g>1 else 0,
        'shared_odd_fft_proxy':(vec.size*math.log2(max(2,m))) if m>1 else 0,
        'shared_twiddle_and_output_proxy':2*vec.size,
    }
    proxy['total_proxy']=sum(proxy.values())
    return GramResult(out,energy,captured,residual,
                      math.sqrt(residual/energy) if energy else 0.,
                      max_condition,total_states,
                      max((len(f) for f in families),default=0),
                      g,m,M,K,proxy,
                      projection.reshape(-1) if projection is not None else None)


def constructed_union_signal(g:int,m:int,M:int,
                              families:Sequence[Sequence[core.ChirpState]],
                              seed:int=1414)->np.ndarray:
    """Produce a generally dense x in union span(V), independent of DFT."""
    if len(families)!=m:
        raise ValueError('Incorrect number of families')
    K=g//M
    rng=np.random.default_rng(seed)
    x=np.zeros((g,m),dtype=np.complex128)
    for s,fam in enumerate(families):
        for st in fam:
            phase=core.local_phase_matrix(g,M,st)
            coef=rng.normal(size=K)+1j*rng.normal(size=K)
            x[:,s]+=(np.conj(phase)*coef[:,None]).reshape(g)
    return x.reshape(-1)


def sample_commutator(g:int,M:int,
                      left:core.ChirpState,right:core.ChirpState)->dict:
    """Local q=2 commutator, measured on one K block (audit only)."""
    ph1=core.local_phase_matrix(g,M,left)[0,:]
    ph2=core.local_phase_matrix(g,M,right)[0,:]
    u=ph1.conj()/math.sqrt(M)
    v=ph2.conj()/math.sqrt(M)
    p=np.outer(u,u.conj());q=np.outer(v,v.conj())
    overlap=abs(np.vdot(u,v))
    cm=p@q-q@p
    return {'overlap_absolute':float(overlap),
            'commutator_frobenius':float(np.linalg.norm(cm,'fro')),
            'commutator_rank_numerical':int(np.linalg.matrix_rank(cm,tol=1e-10)),
            'gram_condition_estimate':float((1+overlap)/(1-overlap)) if overlap<1 else float('inf')}
