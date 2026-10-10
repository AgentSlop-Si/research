"""One-primitive-root phase generation for dyadic (even G) v9 chirp decoder.

In abstract exact arithmetic, a primitive Gth root zeta and O(G) recursive
multiplications produce the full root table. All local phase, Green gauge and
boundary factors are then indexed in O(1) per coefficient. In float64 this
is an UN-CERTIFIED numerical implementation: repeated root multiplication
can accumulate O(G*u) error and FFT_K adds its own rounding. The prior
core's np.exp versions are retained as independent numerical references.
"""
from __future__ import annotations
import math
import numpy as np
import unit_step_core as core


def one_root_table(g:int)->np.ndarray:
    if g<2 or g&(g-1):
        raise ValueError('G must be an even power of two')
    omega=np.exp(2j*np.pi/g)
    tab=np.empty(g,dtype=np.complex128)
    tab[0]=1.+0j
    for i in range(1,g):
        tab[i]=tab[i-1]*omega
    tab.flags.writeable=False
    return tab


def local_phases(g:int,M:int,state:core.ChirpState,roots:np.ndarray)->np.ndarray:
    _,K,_=core.validate_dimensions(g,M)
    state.validate(g)
    if roots.shape!=(g,):raise ValueError('Invalid roots table')
    r=np.arange(K,dtype=np.int64)[:,None]
    t=np.arange(M,dtype=np.int64)[None,:]
    exp=(state.a*core._tri_array_mod(t,g)+((state.a*M*r+state.beta)%g)*t)%g
    return roots[exp]


def compress(x:np.ndarray,g:int,M:int,state:core.ChirpState,roots:np.ndarray)->np.ndarray:
    K=g//M
    arr=np.asarray(x,dtype=np.complex128).reshape(K,M)
    return np.sum(local_phases(g,M,state,roots)*arr,axis=1)


def decode(d:np.ndarray,g:int,M:int,state:core.ChirpState,roots:np.ndarray)->np.ndarray:
    _,K,_=core.validate_dimensions(g,M)
    state.validate(g)
    if roots.shape!=(g,):raise ValueError('Invalid roots table')
    data=np.asarray(d,dtype=np.complex128)
    if data.shape!=(K,):raise ValueError('Need exactly K compressed coefficients')
    dfft=np.fft.fft(data)
    j=np.arange(g,dtype=np.int64)
    idx=state.a*j%g
    gexp=(state.a*core._tri_array_mod(j,g)+state.beta*j)%g
    bexp=(-M*(idx+state.beta)-state.a*core.tri_int(M))%g
    forcing=(dfft[idx%K]-roots[bexp]*dfft[(idx+state.a*M)%K])/math.sqrt(g)
    terms=forcing*roots[(-gexp)%g]
    seed=core.pairwise_sum(terms)/2.
    prefix=core.balanced_exclusive_scan(terms)
    out=np.empty(g,dtype=np.complex128)
    out[idx]=roots[gexp]*(seed-prefix)
    return out
