"""Charged-preparation benchmark for repeated edits at a KNOWN location.

Adaptive method pays for one initial full FFT and preparing N/2+1 phases.
The comparison baseline transforms all 40 modified inputs separately.
This is a structured streaming application, NOT a benchmark of #130.
"""
import time,json
import numpy as np
from scipy.fft import rfft
from prepared_update import PreparedPointEdit
rng=np.random.default_rng(67)
rows=[]
for n in [16384,65536,262144,1048576]:
    x0=rng.standard_normal(n)
    location=n//3
    deltas=rng.normal(scale=0.1,size=40)
    # warmup both methods
    _=rfft(x0)
    pp=PreparedPointEdit(n,location)
    _=pp.update(rfft(x0),0.3)
    times=[]
    for method in ('full_rfft','prepared_point_edit'):
        for _ in range(3):
            x=x0.copy()
            t0=time.perf_counter_ns()
            if method=='prepared_point_edit':
                cached=rfft(x) # count initial FFT
                updater=PreparedPointEdit(n,location) # count phase generation
            for d in deltas:
                x[location]+=d
                if method=='full_rfft':out=rfft(x)
                else:cached=updater.update(cached,d);out=cached
            elapsed=(time.perf_counter_ns()-t0)/1e6
            err=float(np.max(np.abs(out-rfft(x))))
            assert np.allclose(out,rfft(x),atol=1e-7,rtol=1e-10)
            times.append((method,elapsed,err))
    full=float(np.median([v for m,v,e in times if m=='full_rfft']))
    prepared=float(np.median([v for m,v,e in times if m=='prepared_point_edit']))
    errors=[e for m,v,e in times if m=='prepared_point_edit']
    row={'n':n,'updates':40,'full_rfft_ms':full,'prepared_total_ms':prepared,'ratio':full/prepared,'max_abs_error':max(errors),'includes_initial_spectrum_and_phase_prep':True}
    rows.append(row)
    print(f'N={n:8d} updates=40 full={full:9.2f}ms prepared_all={prepared:9.2f}ms speedup={full/prepared:.2f}x max_error={max(errors):.3e}')
with open('benchmark_prepared_results.json','w') as f:json.dump(rows,f,indent=2)
