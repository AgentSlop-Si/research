"""Benchmarks for deferred relation-aware spectrum state.

All methods pay for the initial FFT.  Results are exploratory wall-clock
measurements, not complexity-theorem evidence.
"""
from __future__ import annotations
import json, time
import numpy as np
try:
    from scipy.fft import fft
except ImportError:
    from numpy.fft import fft

from lazy_spectrum import LazySpectrum, direct_sparse_correction
from hybrid_sparse import sparse_dft

rng = np.random.default_rng(20261009)

def timed(fn, reps=3):
    vals=[]
    out=None
    for _ in range(reps):
        t0=time.perf_counter_ns(); out=fn(); vals.append((time.perf_counter_ns()-t0)/1e6)
    return float(np.median(vals)),out

records=[]

# A. Repeated edits at one known location, and only q bins consumed after each edit.
for n in [16384,65536,262144]:
    updates=500
    qcount=64
    x0=rng.standard_normal(n)
    loc=n//3
    deltas=rng.normal(scale=0.05,size=updates)
    bins=np.sort(rng.choice(n,size=qcount,replace=False))

    def fresh_fft_queries():
        x=x0.copy(); out=None
        base=fft(x)  # charged initial transform
        for d in deltas:
            x[loc]+=d
            out=fft(x)[bins]
        return out

    def eager_rank1_dense():
        x=x0.copy()
        cached=fft(x) # charged
        k=np.arange(n,dtype=np.float64)
        phase=np.exp((-2j*np.pi*loc/n)*k) # charged preparation
        out=None
        for d in deltas:
            x[loc]+=d
            cached=cached+d*phase
            out=cached[bins]
        return out

    def lazy_selected_bins():
        x=x0.copy()
        state=LazySpectrum.from_spectrum(fft(x)) # charged
        out=None
        for d in deltas:
            x[loc]+=d
            state.add_edit(loc,d)
            out=state.bins(bins)
        return out

    tf,of=timed(fresh_fft_queries,3)
    te,oe=timed(eager_rank1_dense,3)
    tl,ol=timed(lazy_selected_bins,3)
    # independent truth, not included in timings
    xx=x0.copy();xx[loc]+=float(np.sum(deltas)); truth=fft(xx)[bins]
    assert np.allclose(of,truth,rtol=1e-9,atol=1e-7)
    assert np.allclose(oe,truth,rtol=1e-9,atol=1e-7)
    assert np.allclose(ol,truth,rtol=1e-9,atol=1e-7)
    row=dict(case='fixed_location_partial_bins',n=n,updates=updates,bins=qcount,
             fresh_fft_ms=tf,eager_dense_rank1_ms=te,lazy_ms=tl,
             lazy_vs_fresh=tf/tl,lazy_vs_eager=te/tl)
    records.append(row)
    print('A',row)

# B. Random-location metadata, partial queries every 10 edits, then one final dense flush.
for n in [16384,65536,262144]:
    updates=256
    query_every=16
    qcount=64
    x0=rng.standard_normal(n)+1j*rng.standard_normal(n)
    locs=rng.choice(n,size=updates,replace=False)
    deltas=rng.normal(scale=.05,size=updates)+1j*rng.normal(scale=.05,size=updates)
    bins=np.sort(rng.choice(n,size=qcount,replace=False))

    def fresh_on_queries():
        x=x0.copy(); base=fft(x); out=None
        for i,(j,d) in enumerate(zip(locs,deltas),1):
            x[j]+=d
            if i%query_every==0: out=fft(x)[bins]
        final=fft(x)
        return out,final

    def lazy_with_final_flush():
        x=x0.copy(); state=LazySpectrum.from_spectrum(fft(x)); out=None
        for i,(j,d) in enumerate(zip(locs,deltas),1):
            x[j]+=d; state.add_edit(int(j),complex(d))
            if i%query_every==0: out=state.bins(bins)
        final,plan=state.materialize(method='auto')
        return out,final,plan.method

    tf,of=timed(fresh_on_queries,3)
    tl,ol=timed(lazy_with_final_flush,3)
    xx=x0.copy();xx[locs]+=deltas; truth=fft(xx)
    assert np.allclose(of[1],truth,rtol=1e-9,atol=1e-7)
    assert np.allclose(ol[1],truth,rtol=1e-9,atol=1e-7)
    row=dict(case='random_locations_partial_then_dense',n=n,updates=updates,
             query_every=query_every,bins=qcount,fresh_fft_ms=tf,lazy_ms=tl,
             speedup=tf/tl,dense_flush_method=ol[2])
    records.append(row)
    print('B',row)

# C. Dense-flush crossover: direct sparse phase sum vs grouped factorization vs fresh FFT(delta).
for n in [16384,65536,262144]:
    for k in [1,2,4,8,16,32,64,128,256,512,1024]:
        if k>n: continue
        locs=rng.choice(n,size=k,replace=False)
        vals=rng.normal(size=k)+1j*rng.normal(size=k)
        edits={int(j):complex(v) for j,v in zip(locs,vals)}
        sparse=np.zeros(n,dtype=np.complex128); sparse[locs]=vals
        td,od=timed(lambda: direct_sparse_correction(n,edits),3)
        th,oh=timed(lambda: sparse_dft(n,edits.items()),3)
        tf,of=timed(lambda: fft(sparse),3)
        assert np.allclose(od,of,rtol=1e-9,atol=1e-7)
        assert np.allclose(oh,of,rtol=1e-9,atol=1e-7)
        row=dict(case='dense_flush_crossover',n=n,k=k,direct_ms=td,factorized_ms=th,fresh_sparse_fft_ms=tf,
                 best=min((td,'direct'),(th,'factorized'),(tf,'fresh_sparse_fft'))[1])
        records.append(row)
        print('C',row)

# D. Low-rank + sparse, selected bins only.
for n in [65536,262144]:
    r=4;k=64;qcount=64
    basis_time=rng.standard_normal((r,n))
    basis_spec=fft(basis_time,axis=1)
    coeff=rng.normal(size=r)
    locs=rng.choice(n,size=k,replace=False)
    vals=rng.normal(size=k)
    edits=list(zip(locs.tolist(),vals.tolist()))
    bins=np.sort(rng.choice(n,size=qcount,replace=False))

    def eager():
        dense=np.einsum('r,rn->n',coeff,basis_spec)
        corr=direct_sparse_correction(n,{int(j):complex(v) for j,v in edits})
        return (dense+corr)[bins]
    def lazy():
        s=LazySpectrum.from_basis(basis_spec,coeff,edits=edits)
        return s.bins(bins)
    te,oe=timed(eager,3);tl,ol=timed(lazy,3)
    assert np.allclose(oe,ol,rtol=1e-9,atol=1e-7)
    row=dict(case='low_rank_sparse_partial_bins',n=n,r=r,k=k,bins=qcount,eager_dense_ms=te,lazy_ms=tl,speedup=te/tl)
    records.append(row);print('D',row)

with open('benchmark_lazy_results.json','w') as f:json.dump(records,f,indent=2)
