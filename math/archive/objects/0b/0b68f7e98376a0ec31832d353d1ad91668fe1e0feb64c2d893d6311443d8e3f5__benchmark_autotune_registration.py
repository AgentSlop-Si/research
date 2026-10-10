import json,time,statistics
import numpy as np
from arbitrary_output import AutoOutputPlan, FullFFTBinPlan

def med_ms(fn,reps=3):
 vals=[]
 for _ in range(reps):
  t=time.perf_counter_ns(); fn(); vals.append((time.perf_counter_ns()-t)/1e6)
 return statistics.median(vals)

def run(n=262144,q=64,r=16,seed=20261009):
 rng=np.random.default_rng(seed+r)
 bins=np.sort(rng.choice(n,q,replace=False)).astype(np.intp)
 basis=(rng.standard_normal((r,n))+1j*rng.standard_normal((r,n))).astype(np.complex128)
 full=FullFFTBinPlan(n,bins)
 # baseline; projection is the same r*q output object
 def full_run(): return np.stack([full.execute(row) for row in basis])
 tf=med_ms(full_run,3)
 # tuning + first-result reuse + remaining streamed projection
 t=time.perf_counter_ns(); tuner=AutoOutputPlan(n,bins,sample=basis[0],reps=1,max_plan_bytes=64*1024*1024)
 got=tuner.project_stream_with_sample(basis[0],iter(basis[1:])); total=(time.perf_counter_ns()-t)/1e6
 ref=full_run(); err=float(np.max(np.abs(got-ref)))
 # projected steady cost if the chosen plan were known from a prior machine profile
 chosen_ms=tuner.choice.execute_ms
 oracle_est=chosen_ms*r if chosen_ms is not None else None
 return {'n':n,'q':q,'r':r,'full_registration_ms':tf,'autotuned_total_ms':total,
  'autotune_calibration_ms':tuner.calibration_ms,'chosen_strategy':tuner.strategy,
  'chosen_radix':tuner.choice.radix,'chosen_execute_ms':chosen_ms,
  'autotuned_speedup_including_calibration':tf/total,
  'profiled_plan_estimated_total_ms':oracle_est,'profiled_plan_estimated_speedup':tf/oracle_est if oracle_est else None,
  'plan_bytes':tuner.plan_bytes,'projection_bytes':int(got.nbytes),'max_abs_error':err,
  'candidates':tuner.candidates}

if __name__=='__main__':
 rows=[]
 for r in (1,4,16,32):
  x=run(r=r); print('r',r,'full',round(x['full_registration_ms'],2),'tuned',round(x['autotuned_total_ms'],2),'x',round(x['autotuned_speedup_including_calibration'],2),'K',x['chosen_radix'],'cal',round(x['autotune_calibration_ms'],2)); rows.append(x)
 with open('benchmark_autotune_registration_results.json','w') as f:json.dump(rows,f,indent=2)
