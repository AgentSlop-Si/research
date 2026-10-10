import json,time,statistics
import numpy as np
from arbitrary_output import ProductiveProjectionPlanner, FullFFTBinPlan

def med_ms(fn,reps=3):
 vals=[]
 for _ in range(reps):
  t=time.perf_counter_ns(); fn(); vals.append((time.perf_counter_ns()-t)/1e6)
 return statistics.median(vals)

def run(n=262144,q=64,r=16,seed=20261010):
 rng=np.random.default_rng(seed+r)
 bins=np.sort(rng.choice(n,q,replace=False)).astype(np.intp)
 basis=(rng.standard_normal((r,n))+1j*rng.standard_normal((r,n))).astype(np.complex128)
 full=FullFFTBinPlan(n,bins)
 def baseline(): return np.stack([full.execute(row) for row in basis])
 tf=med_ms(baseline,3)
 # The productive planner consumes each basis exactly once. Repeat whole runs
 # with fresh planner objects; all trial transforms are useful output rows.
 totals=[]; last=None
 for _ in range(3):
  p=ProductiveProjectionPlanner(n,bins,max_plan_bytes=64*1024*1024,max_pruned_trials=3)
  t=time.perf_counter_ns(); got=p.project(iter(basis),expected_count=r); totals.append((time.perf_counter_ns()-t)/1e6); last=(p,got)
 total=statistics.median(totals); p,got=last
 ref=baseline(); err=float(np.max(np.abs(got-ref)))
 return {'n':n,'q':q,'r':r,'full_registration_ms':tf,'productive_planner_ms':total,
  'speedup_including_planning':tf/total,'chosen_strategy':p.stats.chosen_strategy,
  'chosen_radix':p.stats.chosen_radix,'planning_ms_last_run':p.stats.planning_ms,
  'trials_last_run':p.stats.trials,'projection_bytes':int(got.nbytes),'max_abs_error':err}

if __name__=='__main__':
 rows=[]
 for r in (2,4,8,16,32):
  x=run(r=r); print('r',r,'full',round(x['full_registration_ms'],2),'planner',round(x['productive_planner_ms'],2),'x',round(x['speedup_including_planning'],2),'chosen',x['chosen_strategy'],x['chosen_radix'],'plan',round(x['planning_ms_last_run'],2));rows.append(x)
 with open('benchmark_productive_planner_results.json','w') as f:json.dump(rows,f,indent=2)
