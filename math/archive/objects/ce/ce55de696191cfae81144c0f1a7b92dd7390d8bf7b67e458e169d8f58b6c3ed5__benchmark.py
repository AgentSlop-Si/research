"""Exploratory numeric benchmark; tests a factoring strategy, NOT OpenAI #130."""
import json, time
import numpy as np
from hybrid_sparse import sparse_dft
try:
    from scipy import fft as spfft
    direct_fft=spfft.fft
except ImportError:
    direct_fft=np.fft.fft

rng=np.random.default_rng(370)
records=[]
for n in [16384,65536,262144]:
    for k in [1,2,8,32,128,1024]:
        if k>n:continue
        idx=rng.choice(n,size=k,replace=False)
        vals=rng.standard_normal(k)+1j*rng.standard_normal(k)
        edits=list(zip(idx.tolist(),vals.tolist()))
        sparse=np.zeros(n,dtype=complex);sparse[idx]=vals
        candidates=[]
        for typ in ['full','hybrid']:
            samples=[]
            for _ in range(5):
                t0=time.perf_counter_ns()
                if typ=='full':out=direct_fft(sparse)
                else:out=sparse_dft(n,edits)
                samples.append((time.perf_counter_ns()-t0)/1e6)
            candidates.append(float(np.median(samples)))
        y,plan=sparse_dft(n,edits,return_plan=True)
        err=float(np.max(np.abs(y-direct_fft(sparse))))
        assert np.allclose(y,direct_fft(sparse),rtol=1e-9,atol=1e-8)
        records.append(dict(n=n,k=k,b=plan.b,m=plan.m,full_ms=candidates[0],hybrid_ms=candidates[1],speedup=candidates[0]/candidates[1],max_abs_error=err,classical_inner_butterflies=plan.classical_inner_butterflies,classical_full_butterflies=plan.classical_full_butterflies))
        print(f'N={n:7d} k={k:4d} block={plan.b:4d} direct={candidates[0]:8.3f}ms hybrid={candidates[1]:8.3f}ms ratio={candidates[0]/candidates[1]:6.2f}x abs_err={err:8.1e}')
with open('benchmark_results.json','w') as f:json.dump(records,f,indent=2)
