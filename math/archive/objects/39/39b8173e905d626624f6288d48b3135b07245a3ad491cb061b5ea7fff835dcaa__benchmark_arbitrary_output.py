import json,time,statistics,gc
import numpy as np
from arbitrary_output import ArbitraryBinsDFTPlan, FullFFTBinPlan, candidate_radices

def med_ms(fn,reps=3):
 vals=[]
 for _ in range(reps):
  t=time.perf_counter_ns(); fn(); vals.append((time.perf_counter_ns()-t)/1e6)
 return statistics.median(vals)

def run_one(n,q,seed=20261009):
 rng=np.random.default_rng(seed+n+q)
 bins=np.sort(rng.choice(n,q,replace=False)).astype(np.intp)
 x=rng.standard_normal(n)+1j*rng.standard_normal(n)
 full=FullFFTBinPlan(n,bins)
 # Phase storage is q*(N/K) complex numbers. Restrict the sweep to <=4N
 # complex phase cells so benchmarking candidates itself cannot explode memory.
 cand=[]
 for k in candidate_radices(n,q):
  if k>=n: continue
  if q*(n//k) <= 4*n:
   cand.append(k)
 # ensure q-bracketing power-of-two-like choices are represented when divisors
 if not cand:
  cand=[min((d for d in candidate_radices(n,q) if d<n), default=1)]
 cand=sorted(set(cand))
 plans=[]
 for k in cand:
  t=time.perf_counter_ns(); p=ArbitraryBinsDFTPlan(n,bins,radix=k); prep=(time.perf_counter_ns()-t)/1e6
  p.execute(x)
  tm=med_ms(lambda p=p:p.execute(x),3)
  ref=full.execute(x); got=p.execute(x)
  err=float(np.max(np.abs(got-ref)))
  plans.append({'radix':k,'prep_ms':prep,'execute_ms':tm,'plan_bytes':p.plan_bytes,'proxy':p.arithmetic_proxy,'max_abs_error':err})
  del p,ref,got; gc.collect()
 tf=med_ms(lambda:full.execute(x),5)
 best=min(plans,key=lambda z:z['execute_ms'])
 return {'n':n,'q':q,'bin_pattern':'uniform_random','full_fft_gather_ms':tf,
         'best_pruned':best,'pruned_speedup':tf/best['execute_ms'],'candidates':plans}

if __name__=='__main__':
 rows=[]
 for n,qs in [(262144,(1,4,16,64,256,1024)),(1048576,(4,16,64,256))]:
  for q in qs:
   row=run_one(n,q); print(n,q,'full',round(row['full_fft_gather_ms'],3),'bestK',row['best_pruned']['radix'],round(row['best_pruned']['execute_ms'],3),'x',round(row['pruned_speedup'],2),'memMiB',round(row['best_pruned']['plan_bytes']/2**20,2)); rows.append(row)
 with open('benchmark_arbitrary_output_results.json','w') as f: json.dump(rows,f,indent=2)
