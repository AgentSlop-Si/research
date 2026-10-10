"""Hero #1 phase14: orthogonal beta-bank energy certificates & fused decoding.

For N=G*m, G=2^v2(N), M|G, K=G/M, K>=M, fixed unit-step chirp
states for each odd-part column, the normalized projectors Q_{s,t}
form an orthogonal resolution of the identity.

Any selected masks S_s yield the deterministic approximation
    Y=F_N Q_S x
and the EXACT-ARITHMETIC energy certificate
    ||Y-F_N x||_2^2=||x||_2^2 - sum_{s,t in S_s} ||d_{s,t}||_2^2/M.

Two interfaces:
  known_banks(): O(L G + (L K)log K + N log(m+1)) work for L
                 selected column/bank pairs, plus O(N) setup. It certifies
                 its l2 error without any reference FFT.
  analyze_banks()+adaptive_banks(): O(N log M) for all local spectra,
                 select optimal L bank/column pairs, decode L passes.

These are arithmetic-model (exact-root) claims. NumPy float64 is *not*
an interval-certified implementation. For generic inputs L may be m*M,
recovering ordinary O(NlogN) work, NOT an exact o(NlogN) algorithm.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence
import math
import numpy as np
import unit_step_core as core
import mixedradix as old
import one_root_chirp as orc

BankMask = tuple[tuple[int, ...], ...]


def base_states(g:int, m:int) -> tuple[core.ChirpState,...]:
    if g < 1 or m < 1:
        raise ValueError('G,m must be positive')
    return tuple(core.ChirpState(a=1, beta=(3*s + 1) % g) for s in range(m))


def normalize_mask(mask:Sequence[Sequence[int]],m:int,M:int)->BankMask:
    if len(mask)!=m:
        raise ValueError('Expected one bank mask per odd-part input column')
    result=[]
    for col in mask:
        c=tuple(sorted(set(int(t) for t in col)))
        if any(t<0 or t>=M for t in c):
            raise ValueError('Bank index outside [0,M)')
        result.append(c)
    return tuple(result)


def _setup(x:np.ndarray,block:int|None,states:Sequence[core.ChirpState]|None):
    vec=np.asarray(x,dtype=np.complex128).reshape(-1)
    if not vec.size:
        raise ValueError('Empty signal')
    g,m=old.dyadic_odd_split(vec.size)
    M=old.sketch_block(g) if block is None else int(block)
    if g>1:
        _,K,_=core.validate_dimensions(g,M)
    else:
        if M!=1:
            raise ValueError('For odd N, block=1 only')
        K=1
    sts=base_states(g,m) if states is None else tuple(states)
    if len(sts)!=m:
        raise ValueError('Expected one independent chirp base per column')
    if g>1:
        for st in sts:st.validate(g)
    return vec,g,m,M,K,sts


@dataclass
class BankResult:
    output:np.ndarray
    mask:BankMask
    total_energy:float
    captured_energy:float
    squared_error_certificate:float
    theoretical_relative_l2_error:float
    selected_column_banks:int
    total_column_banks:int
    G:int
    m:int
    M:int
    K:int
    method:str
    # Total scalar-work counts are transparent proxies, not wall-clock claims.
    work_proxy:dict


def _final_ct(stage:np.ndarray,g:int,m:int) -> np.ndarray:
    n=g*m
    if g==1:
        return np.fft.fft(stage.reshape(n))/math.sqrt(n)
    stage*=old.twiddle_one_root(g,m)
    return (np.fft.fft(stage,axis=1)/math.sqrt(m)).T.copy().reshape(n)


def _finish(vec:np.ndarray,mask:BankMask,g:int,m:int,M:int,K:int,
            stage:np.ndarray,captured:float,method:str,
            extra_work:dict|None=None)->BankResult:
    out=_final_ct(stage,g,m)
    total=float(np.vdot(vec,vec).real)
    # Clamp tiny negative residues due to double-precision sums; certificate
    # equation is mathematically exact, but *floating* value is diagnostic.
    tail=max(0.,total-captured)
    L=sum(map(len,mask))
    tiny_ffts=L*(K*math.log2(max(2,K))) if g>1 else 0.
    work={'dyadic_full_scans':L*g if g>1 else 0,
          'selected_K_fft_proxy':tiny_ffts,
          'local_compression':L*g if method=='known' and g>1 else 0,
          'odd_factor_fft_proxy':vec.size*math.log2(max(2,m)) if m>1 else 0,
          'shared_twiddle_generation_and_output':2*vec.size if g>1 else vec.size,
          'local_bank_energy_analysis':0,
          'dyadic_root_table_preparation':g if g>1 else 0,
          'bank_selection_sort_proxy':0}
    if extra_work:work.update(extra_work)
    work['declared_work_proxy']=sum(v for k,v in work.items()
                                     if k!='declared_work_proxy')
    return BankResult(output=out,mask=mask,total_energy=total,
                      captured_energy=captured,squared_error_certificate=tail,
                      theoretical_relative_l2_error=math.sqrt(tail/total) if total else 0.,
                      selected_column_banks=L,total_column_banks=m*M,
                      G=g,m=m,M=M,K=K,method=method,work_proxy=work)


def known_banks(x:np.ndarray,mask:Sequence[Sequence[int]],block:int|None=None,
                states:Sequence[core.ChirpState]|None=None)->BankResult:
    """User-specified bank masks, no energy-screen FFT. Full l2 certificate.

    For <=C selected banks per input column with fixed odd part m and
    M~=log G, both decoding and energy certification cost O(N).
    The output is F_N Q_S x in exact arithmetic. Empty mask yields zero.
    """
    vec,g,m,M,K,sts=_setup(x,block,states)
    mask=normalize_mask(mask,m,M)
    stage=np.zeros((g,m),dtype=np.complex128)
    cap=0.
    if g==1:
        for s in range(m):
            if 0 in mask[s]:
                stage[0,s]=vec[s]
                cap+=float(abs(vec[s])**2)
    else:
        roots=orc.one_root_table(g)
        cols=vec.reshape(g,m)
        for s in range(m):
            for t in mask[s]:
                st=core.ChirpState(sts[s].a,(sts[s].beta+t*K)%g)
                d=orc.compress(cols[:,s],g,M,st,roots)
                cap+=float(np.vdot(d,d).real)/M
                stage[:,s]+=orc.decode(d,g,M,st,roots)/M
    return _finish(vec,mask,g,m,M,K,stage,cap,'known')


@dataclass
class BankAnalysis:
    vector:np.ndarray
    states:tuple[core.ChirpState,...]
    compressed:np.ndarray # shape (m,K,M); reused in decoder; O(N) storage
    energy:np.ndarray # shape (m,M)
    roots:np.ndarray|None # one-root table, shared across selected decoders
    G:int
    m:int
    M:int
    K:int


def analyze_banks(x:np.ndarray,block:int|None=None,
                  states:Sequence[core.ChirpState]|None=None)->BankAnalysis:
    """All local bank energy profiles with positive-sign FFT_M, O(N log M).

    For each input column and each local length-M block, the Fourier_M
    coefficients are precisely the M orthogonal chirp projections' d data.
    Neither the complete Fourier_G nor Fourier_N is evaluated here.
    """
    vec,g,m,M,K,sts=_setup(x,block,states)
    saved=vec.copy();saved.flags.writeable=False
    compressed=np.empty((m,K,M),dtype=np.complex128)
    energy=np.empty((m,M),dtype=np.float64)
    cols=vec.reshape(g,m)
    roots=None if g==1 else orc.one_root_table(g)
    if g==1:
        compressed[:,0,0]=saved
        energy[:,0]=np.abs(saved)**2
    else:
        for s in range(m):
            base_phase=orc.local_phases(g,M,sts[s],roots)
            local=base_phase*cols[:,s].reshape(K,M)
            d=np.fft.ifft(local,axis=1)*M # sum_u exp(+2πitu/M)*local[u]
            compressed[s,:,:]=d
            energy[s,:]=np.sum(np.abs(d)**2,axis=0)/M
    compressed.flags.writeable=False
    energy.flags.writeable=False
    return BankAnalysis(saved,sts,compressed,energy,roots,g,m,M,K)


def fixed_count_mask(a:BankAnalysis,keep:int)->BankMask:
    """Deterministic energy-optimal rank-L mask (ties: column, then bank)."""
    if not (0<=keep<=a.m*a.M):
        raise ValueError('keep outside bank count')
    # Sorting is O(mM log(mM)); count it explicitly, instead of calling it O(N).
    ranked=sorted(range(a.m*a.M),key=lambda pos:(-float(a.energy.flat[pos]),pos))
    selected=[[] for _ in range(a.m)]
    for pos in ranked[:keep]:
        s,t=divmod(pos,a.M)
        selected[s].append(t)
    return normalize_mask(selected,a.m,a.M)


def budget_mask(a:BankAnalysis,relative_error:float)->BankMask:
    """Min bank/column count for exact-arithmetic target ||err||<=eps||x||.

    With eps=0, conservatively keep every bank (no float-zero guessing).
    """
    eps=float(relative_error)
    if not np.isfinite(eps) or eps<0:
        raise ValueError('relative_error must be finite nonnegative')
    if eps==0:
        return tuple(tuple(range(a.M)) for _ in range(a.m))
    total=float(np.sum(a.energy))
    if total==0 or eps>=1:
        return tuple(() for _ in range(a.m))
    target=(1.0-eps*eps)*total
    ranked=sorted(range(a.m*a.M),key=lambda pos:(-float(a.energy.flat[pos]),pos))
    selected=[[] for _ in range(a.m)]
    accumulated=0.
    for pos in ranked:
        s,t=divmod(pos,a.M)
        selected[s].append(t)
        accumulated+=float(a.energy[s,t])
        if accumulated>=target:
            break
    return normalize_mask(selected,a.m,a.M)


def evaluate_mask(a:BankAnalysis,mask:Sequence[Sequence[int]])->BankResult:
    """Decode precomputed compressed streams and do odd-FFT exactly once."""
    mask=normalize_mask(mask,a.m,a.M)
    g,m,M,K=a.G,a.m,a.M,a.K
    stage=np.zeros((g,m),dtype=np.complex128)
    captured=0.
    for s in range(m):
        for t in mask[s]:
            captured+=float(a.energy[s,t])
            if g==1:
                stage[0,s]+=a.vector[s]
            else:
                st=core.ChirpState(a.states[s].a,(a.states[s].beta+t*K)%g)
                stage[:,s]+=orc.decode(a.compressed[s,:,t],g,M,st,a.roots)/M
    extra={'dyadic_root_table_preparation':0,
           'local_bank_energy_analysis':a.vector.size*math.log2(max(2,M)) if g>1 else 0,
           'bank_selection_sort_proxy':a.m*a.M*math.log2(max(2,a.m*a.M))}
    return _finish(a.vector,mask,g,m,M,K,stage,captured,'analyzed',extra)


def adaptive_banks(x:np.ndarray,relative_error:float,block:int|None=None,
                   states:Sequence[core.ChirpState]|None=None)->BankResult:
    a=analyze_banks(x,block,states)
    return evaluate_mask(a,budget_mask(a,relative_error))


def projected_input(x:np.ndarray,mask:Sequence[Sequence[int]],
                    block:int|None=None,
                    states:Sequence[core.ChirpState]|None=None)->np.ndarray:
    """Audit-only independent Q_S x; costs O(L G)."""
    vec,g,m,M,K,sts=_setup(x,block,states)
    mask=normalize_mask(mask,m,M)
    out=np.zeros((g,m),dtype=np.complex128)
    if g==1:
        for s in range(m):
            if 0 in mask[s]:out[0,s]=vec[s]
    else:
        col=vec.reshape(g,m)
        for s in range(m):
            for t in mask[s]:
                st=core.ChirpState(sts[s].a,(sts[s].beta+t*K)%g)
                out[:,s]+=core.materialize_projected_signal(col[:,s],M,st)/M
    return out.reshape(-1)


def constructed_bank_signal(g:int,m:int,M:int,
                            mask:Sequence[Sequence[int]],seed:int=14,
                            states:Sequence[core.ChirpState]|None=None)->np.ndarray:
    """Construct a generally dense signal supported EXACTLY on selected banks."""
    n=g*m
    x=np.random.default_rng(seed).normal(size=n)+1j*np.random.default_rng(seed+1).normal(size=n)
    return projected_input(x,mask,M,states)
