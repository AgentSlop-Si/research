import json,statistics,time
import numpy as np
from pruned_output import first_k_dft
try:
 from scipy import fft as sp_fft
except ImportError:
 sp_fft=None

def med(fn,reps=7):
 v=[]
 for _ in range(reps):
  t=time.perf_counter_ns(); fn(); v.append((time.perf_counter_ns()-t)/1e6)
 return statistics.median(v)

rng=np.random.default_rng(99); rows=[]
for n in (16384,65536,262144):
 x=rng.standard_normal(n)+1j*rng.standard_normal(n)
 for k in (16,64,256):
  if n%k:continue
  full=lambda:(sp_fft.fft(x) if sp_fft else np.fft.fft(x))[:k]
  prune=lambda:first_k_dft(x,k)
  # warm
  a=full();b=prune(); err=float(np.max(np.abs(a-b)))
  tf=med(full);tp=med(prune)
  row={'n':n,'k':k,'full_ms':tf,'pruned_ms':tp,'pruned_speedup':tf/tp,'max_abs_error':err,
       'arithmetic_log_ratio':np.log2(n)/np.log2(k)}
  rows.append(row);print(row)
with open('benchmark_pruned_output_results.json','w') as f:json.dump(rows,f,indent=2)
