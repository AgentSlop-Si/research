"""Benchmarks for consumer-aware dynamic Fourier views.

All measurements are steady-state relation-maintenance costs after basis spectra
are already supplied.  They do not include the one-time cost of discovering or
FFT-transforming the basis.
"""
from __future__ import annotations
import json
import statistics
import time
import numpy as np

from relation_view import DynamicFourierState, CachedFourierBasis


def median_ms(fn, reps=5):
    vals=[]
    for _ in range(reps):
        t=time.perf_counter_ns(); fn(); vals.append((time.perf_counter_ns()-t)/1e6)
    return statistics.median(vals)


def make_workload(rng, r, prepared_positions, updates, coeff_probability=.72):
    ops=[]
    for _ in range(updates):
        if rng.random() < coeff_probability:
            i=int(rng.integers(r))
            d=complex(rng.standard_normal()*.02, rng.standard_normal()*.02)
            ops.append(('c',i,d))
        else:
            p=int(rng.choice(prepared_positions))
            d=complex(rng.standard_normal()*.02, rng.standard_normal()*.02)
            ops.append(('p',p,d))
    return ops


def run_case(n=16384,r=512,q=64,updates=4096,query_every=8,seed=61422):
    rng=np.random.default_rng(seed)
    # Arbitrary cached basis spectra are enough to benchmark relation handling.
    basis=(rng.standard_normal((r,n))+1j*rng.standard_normal((r,n))).astype(np.complex128)
    coeff0=(rng.standard_normal(r)+1j*rng.standard_normal(r)).astype(np.complex128)
    registered=CachedFourierBasis(basis)
    bins=np.sort(rng.choice(n,size=q,replace=False)).astype(np.intp)
    positions=np.sort(rng.choice(n,size=64,replace=False)).astype(np.intp)
    ops=make_workload(rng,r,positions,updates)

    basis_q=np.ascontiguousarray(basis[:,bins])
    phase_q=np.exp((-2j*np.pi/n)*np.outer(positions.astype(float),bins.astype(float)))
    pos_to_row={int(p):i for i,p in enumerate(positions)}

    # For eager full-spectrum relation maintenance, precompute full phase rows
    # only for the declared editable positions. This is a deliberately strong
    # eager baseline and charges its O(N*P) memory outside steady-state timing.
    phase_full=np.exp((-2j*np.pi/n)*np.outer(positions.astype(float),np.arange(n,dtype=float)))

    def event_view_run():
        state=DynamicFourierState(registered,coeff0)
        view=state.view(bins,prepared_positions=positions,phase_cache_limit=0)
        checksum=0.0
        for t,(kind,key,d) in enumerate(ops,1):
            if kind=='c': state.add_coefficient_trusted(key,d)
            else: state.add_point_trusted(key,d)
            if t%query_every==0:
                y=view.query(strategy='auto')
                checksum += float(y[0].real)
                state.compact_event_log()
        return checksum,view.last_stats.strategy

    def partial_recompute_run():
        c=coeff0.copy(); residual=np.zeros(len(positions),dtype=np.complex128)
        checksum=0.0
        for t,(kind,key,d) in enumerate(ops,1):
            if kind=='c': c[key]+=d
            else: residual[pos_to_row[key]]+=d
            if t%query_every==0:
                y=c@basis_q + residual@phase_q
                checksum += float(y[0].real)
        return checksum

    def eager_dense_run():
        c=coeff0.copy()
        dense=c@basis
        checksum=0.0
        for t,(kind,key,d) in enumerate(ops,1):
            if kind=='c':
                c[key]+=d; dense += d*basis[key]
            else:
                dense += d*phase_full[pos_to_row[key]]
            if t%query_every==0:
                checksum += float(dense[bins[0]].real)
        return checksum

    # Warm-up BLAS/NumPy paths.
    event_view_run(); partial_recompute_run(); eager_dense_run()
    tev=median_ms(event_view_run)
    tpartial=median_ms(partial_recompute_run)
    teager=median_ms(eager_dense_run)

    # Correctness check on one replay of all operations.
    state=DynamicFourierState(registered,coeff0)
    view=state.view(bins,prepared_positions=positions,phase_cache_limit=0)
    c=coeff0.copy(); residual=np.zeros(len(positions),dtype=np.complex128)
    for kind,key,d in ops:
        if kind=='c': state.add_coefficient_trusted(key,d); c[key]+=d
        else: state.add_point_trusted(key,d); residual[pos_to_row[key]]+=d
    got=view.query(strategy='auto')
    expected=c@basis_q+residual@phase_q
    err=float(np.max(np.abs(got-expected)))

    return {
      'n':n,'r':r,'q':q,'updates':updates,'query_every':query_every,
      'queries':updates//query_every,
      'event_view_ms':tev,
      'partial_recompute_ms':tpartial,
      'eager_dense_ms':teager,
      'speedup_vs_partial':tpartial/tev,
      'speedup_vs_eager':teager/tev,
      'max_abs_error':err,
      'basis_bytes':int(basis.nbytes),
      'prepared_partial_phase_bytes':int(phase_q.nbytes),
      'prepared_full_phase_bytes':int(phase_full.nbytes),
    }


def planner_case(n=8192,r=64,q=64,seed=8181):
    rng=np.random.default_rng(seed)
    basis=(rng.standard_normal((r,n))+1j*rng.standard_normal((r,n))).astype(np.complex128)
    coeff=(rng.standard_normal(r)+1j*rng.standard_normal(r)).astype(np.complex128)
    registered=CachedFourierBasis(basis)
    bins=np.sort(rng.choice(n,size=q,replace=False)).astype(np.intp)
    state=DynamicFourierState(registered,coeff)
    view=state.view(bins)
    # Hammer the same few keys: event count is huge, net relation dimension tiny.
    for t in range(10000):
        state.add_coefficient_trusted(t%3, (1e-5 if t%2==0 else -0.7e-5))
    t0=time.perf_counter_ns(); ya=view.query(strategy='auto'); auto_ms=(time.perf_counter_ns()-t0)/1e6
    auto_strategy=view.last_stats.strategy

    # New identical state/view to time forced replay of the 10k-event backlog.
    state2=DynamicFourierState(registered,coeff)
    view2=state2.view(bins)
    for t in range(10000):
        state2.add_coefficient_trusted(t%3, (1e-5 if t%2==0 else -0.7e-5))
    t0=time.perf_counter_ns(); yr=view2.query(strategy='replay'); replay_ms=(time.perf_counter_ns()-t0)/1e6
    err=float(np.max(np.abs(ya-yr)))
    return {'n':n,'r':r,'q':q,'backlog':10000,'auto_ms':auto_ms,
            'forced_replay_ms':replay_ms,'auto_strategy':auto_strategy,
            'speedup':replay_ms/auto_ms if auto_ms else float('inf'),
            'max_abs_difference':err}


if __name__=='__main__':
    results=[]
    for h in (1,4,16,64):
        result=run_case(query_every=h)
        results.append(result)
        print(result)
    planner=planner_case(); print(planner)
    out={'benchmark':'consumer-aware relation views','results':results,'planner_case':planner,
         'notes':'Median 5 steady-state runs. Basis discovery/FFT preprocessing excluded; relation metadata is supplied.'}
    with open('benchmark_relation_view_results.json','w') as f: json.dump(out,f,indent=2)


def multi_consumer_case(n=16384,r=256,updates=4096,seed=92711):
    rng=np.random.default_rng(seed)
    basis=(rng.standard_normal((r,n))+1j*rng.standard_normal((r,n))).astype(np.complex128)
    registered=CachedFourierBasis(basis)
    coeff0=(rng.standard_normal(r)+1j*rng.standard_normal(r)).astype(np.complex128)
    positions=np.sort(rng.choice(n,size=32,replace=False)).astype(np.intp)
    ops=make_workload(rng,r,positions,updates,coeff_probability=.8)
    specs=[(16,1),(64,8),(256,64),(1024,512)]
    bin_sets=[np.sort(rng.choice(n,size=q,replace=False)).astype(np.intp) for q,_ in specs]
    phase_full=np.exp((-2j*np.pi/n)*np.outer(positions.astype(float),np.arange(n,dtype=float)))
    pos_to_row={int(p):i for i,p in enumerate(positions)}

    def lazy_run():
        state=DynamicFourierState(registered,coeff0)
        views=[state.view(bins,prepared_positions=positions,phase_cache_limit=0) for bins in bin_sets]
        checksum=0.0
        for t,(kind,key,d) in enumerate(ops,1):
            if kind=='c': state.add_coefficient_trusted(key,d)
            else: state.add_point_trusted(key,d)
            for v,(_,period) in zip(views,specs):
                if t%period==0:
                    checksum += float(v.query(strategy='auto')[0].real)
            # Auto views are rebuild-capable, so old history can be dropped.
            state.compact_event_log()
        return checksum

    def eager_all_views_run():
        # Maintain a full spectrum eagerly; every consumer gets O(q) slicing.
        dense=coeff0@basis
        checksum=0.0
        for t,(kind,key,d) in enumerate(ops,1):
            if kind=='c': dense += d*basis[key]
            else: dense += d*phase_full[pos_to_row[key]]
            for bins,(_,period) in zip(bin_sets,specs):
                if t%period==0:
                    checksum += float(dense[bins[0]].real)
        return checksum

    # Snapshot-only consumers: no delta replay. This gives the lower-overhead
    # factorized competitor for rare consumers, recomputing exactly their bins.
    basis_q=[np.ascontiguousarray(basis[:,b]) for b in bin_sets]
    phase_q=[np.exp((-2j*np.pi/n)*np.outer(positions.astype(float),b.astype(float))) for b in bin_sets]
    def snapshot_run():
        c=coeff0.copy(); residual=np.zeros(len(positions),dtype=np.complex128); checksum=0.0
        for t,(kind,key,d) in enumerate(ops,1):
            if kind=='c': c[key]+=d
            else: residual[pos_to_row[key]]+=d
            for bq,pq,(_,period) in zip(basis_q,phase_q,specs):
                if t%period==0:
                    y=c@bq+residual@pq
                    checksum += float(y[0].real)
        return checksum

    lazy_run(); eager_all_views_run(); snapshot_run()
    tl=median_ms(lazy_run); te=median_ms(eager_all_views_run); ts=median_ms(snapshot_run)
    return {'n':n,'r':r,'updates':updates,
            'views':[{'q':q,'query_every':p} for q,p in specs],
            'lazy_ms':tl,'snapshot_ms':ts,'eager_full_ms':te,
            'lazy_speedup_vs_eager':te/tl,'lazy_speedup_vs_snapshot':ts/tl}
