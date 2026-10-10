import json,time
import numpy as np
try:
 from scipy import fft as sp_fft
except ImportError:
 sp_fft=None
from pruned_output import FirstKDFTPlan

rng=np.random.default_rng(20261009)
configs=[(262144,64,16),(1048576,16,8)]
rows=[]
for n,k,r in configs:
    basis=(rng.standard_normal((r,n))+1j*rng.standard_normal((r,n))).astype(np.complex128)
    # Full transform registration; keep only requested projection for a fair
    # output object, but report what storing all spectra would have cost.
    t=time.perf_counter_ns()
    full_proj=[]
    for row in basis:
        y=sp_fft.fft(row) if sp_fft else np.fft.fft(row)
        full_proj.append(y[:k].copy())
    full_ms=(time.perf_counter_ns()-t)/1e6
    full_proj=np.stack(full_proj)

    t=time.perf_counter_ns(); plan=FirstKDFTPlan(n,k); prep_ms=(time.perf_counter_ns()-t)/1e6
    t=time.perf_counter_ns(); pruned_proj=plan.project_stream((row for row in basis)); exec_ms=(time.perf_counter_ns()-t)/1e6
    total=prep_ms+exec_ms
    err=float(np.max(np.abs(full_proj-pruned_proj)))
    result={
      'n':n,'k':k,'r':r,'full_fft_registration_ms':full_ms,
      'pruned_plan_ms':prep_ms,'pruned_stream_ms':exec_ms,'pruned_total_ms':total,
      'speedup_including_plan':full_ms/total,
      'projection_bytes':int(pruned_proj.nbytes),'plan_bytes':plan.plan_bytes,
      'hypothetical_full_basis_spectra_bytes':int(r*n*16),
      'persistent_storage_reduction':float(n/k), 'max_abs_error':err
    }
    rows.append(result);print(result)
with open('benchmark_registration_results.json','w') as f:json.dump(rows,f,indent=2)
