import json,statistics,time
import numpy as np
from pruned_output import FirstKDFTPlan
try:
 from scipy import fft as sp_fft
except ImportError: sp_fft=None

def med(fn,reps=7):
 a=[]
 for _ in range(reps):
  t=time.perf_counter_ns(); fn(); a.append((time.perf_counter_ns()-t)/1e6)
 return statistics.median(a)
rng=np.random.default_rng(132);out=[]
for n in (65536,262144,1048576):
 x=rng.standard_normal(n)+1j*rng.standard_normal(n)
 for k in (16,64,256):
  if n%k:continue
  t=time.perf_counter_ns(); plan=FirstKDFTPlan(n,k); prep=(time.perf_counter_ns()-t)/1e6
  full=lambda:(sp_fft.fft(x) if sp_fft else np.fft.fft(x))[:k]
  prune=lambda:plan.execute(x)
  a=full();b=prune();err=float(np.max(np.abs(a-b)))
  tf=med(full,5);tp=med(prune,5)
  row={'n':n,'k':k,'plan_prep_ms':prep,'plan_bytes':plan.plan_bytes,'full_ms':tf,'planned_pruned_ms':tp,
       'speedup':tf/tp,'max_abs_error':err,'storage_reduction_if_full_basis':n/k}
  print(row);out.append(row)
with open('benchmark_pruned_plan_results.json','w') as f:json.dump(out,f,indent=2)
