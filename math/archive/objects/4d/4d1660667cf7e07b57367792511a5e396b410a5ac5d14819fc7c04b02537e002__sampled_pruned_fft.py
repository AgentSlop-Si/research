"""Fresh arbitrary bounded-input *approximate* normalized DFT via sampling.

Different goal from exact FFT: given |x[j]|<=1, estimate all bins of
FFT(x)/N within additive epsilon with probability >=1-failure under
random sampling, using O(N (1+log log N)) Fourier arithmetic for
fixed epsilon/failure and an O(N)-size explicit output.

Ingredients are classical Monte Carlo concentration + pruned radix-2 FFT,
not claimed to be a novel algorithm or a practical SciPy replacement.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import ceil,log,log2
import numpy as np

@dataclass
class SparseStats:
    nonzeros:int=0
    active_nodes:int=0
    butterfly_slots:int=0
    twiddle_multiplications:int=0
    output_length:int=0

def _pruned_fft(n:int, ids, val, tw_cache:dict, stats:SparseStats):
    if len(ids)==0:
        return None
    if n==1:
        stats.active_nodes+=1
        return np.array([complex(val[0])],dtype=np.complex128)
    stats.active_nodes+=1
    half=n//2
    mask=(ids%2)==0
    e=_pruned_fft(half,ids[mask]//2,val[mask],tw_cache,stats) if np.any(mask) else None
    o=_pruned_fft(half,ids[~mask]//2,val[~mask],tw_cache,stats) if np.any(~mask) else None
    stats.butterfly_slots+=half
    if o is None:
        return np.concatenate((e,e))
    if n not in tw_cache:
        tw_cache[n]=np.exp((-2j*np.pi/n)*np.arange(half))
    t=tw_cache[n]*o
    stats.twiddle_multiplications+=half
    if e is None:
        return np.concatenate((t,-t))
    return np.concatenate((e+t,e-t))

def sparse_fft(N:int,indices,values):
    """Exact DFT (to floating arithmetic roundoff) of k-sparse length N vector.
    Duplicate indices are accumulated. Explicit output always length N.
    """
    if N<1 or (N&(N-1)):
        raise ValueError('N must be a positive power of two')
    ids=np.asarray(indices,dtype=np.int64)
    vals=np.asarray(values,dtype=np.complex128)
    if ids.shape!=vals.shape or ids.ndim!=1 or np.any(ids<0) or np.any(ids>=N):
        raise ValueError('bad sparse input')
    fused={}
    for j,v in zip(ids,vals):fused[int(j)]=fused.get(int(j),0j)+complex(v)
    active=sorted(j for j in fused if fused[j]!=0)
    ids=np.asarray(active,dtype=np.int64)
    vals=np.asarray([fused[j] for j in active],dtype=np.complex128)
    stats=SparseStats(nonzeros=len(ids),output_length=N)
    out=_pruned_fft(N,ids,vals,{},stats)
    if out is None:out=np.zeros(N,dtype=np.complex128)
    return out,stats

def sample_count(N:int,epsilon:float,failure_probability:float=0.01):
    """Union-bound Hoeffding: P(any normalized-DFT bin > epsilon)
    <= 4N exp(-m epsilon^2/4) for bounded complex input.
    """
    if N<1 or not (0<epsilon<2) or not (0<failure_probability<1):
        raise ValueError('invalid N, epsilon or failure probability')
    return ceil(4/(epsilon**2)*log(4*N/failure_probability))

def approximate_normalized_fft(x,epsilon:float=0.3,failure_probability:float=0.01,seed:int=0):
    """Randomized all-bin estimator. NO exact DFT promise.
    For every fixed bounded input, union Hoeffding gives confidence >=1-eta.
    """
    x=np.asarray(x,dtype=np.complex128)
    N=len(x)
    if N<1 or (N&(N-1)):
        raise ValueError('N must be power of 2')
    if np.any(abs(x)>1+1e-12):
        raise ValueError('input magnitude must be <=1')
    m=sample_count(N,epsilon,failure_probability)
    rng=np.random.default_rng(seed)
    selected=rng.integers(0,N,size=m)
    unique,counts=np.unique(selected,return_counts=True)
    sparse_vals=(counts/m)*x[unique]
    out,stats=sparse_fft(N,unique,sparse_vals)
    return out,{'samples':m,'unique_sample_positions':len(unique),
                'worst_case_failure_bound':failure_probability,
                'butterfly_slots':stats.butterfly_slots,
                'active_nodes':stats.active_nodes,'twiddle_mults':stats.twiddle_multiplications,
                'standard_butterfly_slots':N//2*(N.bit_length()-1)}

if __name__=='__main__':
    n=4096
    inp=np.ones(n,dtype=complex)
    out,stats=approximate_normalized_fft(inp,epsilon=.4,seed=5)
    print('stats',stats)
    print('worst observed abs error',np.max(abs(out-np.fft.fft(inp)/n)))
