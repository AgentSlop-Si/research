import json,time,statistics
import numpy as np
from arbitrary_output import ArbitraryBinsDFTPlan,FullFFTBinPlan
from multi_view import SharedProjectedFourierStore,union_frequency_sets
from projected_fourier import ProjectedFourierState

def med_ms(fn,reps=5):
 vals=[]
 for _ in range(reps):
  t=time.perf_counter_ns(); val=fn(); vals.append((time.perf_counter_ns()-t)/1e6)
 return statistics.median(vals)

def run(n=262144,r=16,C=8,q=16,updates=4096,seed=20261009,intervals=None):
 rng=np.random.default_rng(seed)
 common=np.sort(rng.choice(n,q//2,replace=False))
 used=set(map(int,common)); view_bins={}
 for c in range(C):
  pool=np.array([x for x in rng.choice(n,4*q,replace=False) if int(x) not in used],dtype=np.intp)
  unique=pool[:q-len(common)]; used.update(map(int,unique))
  view_bins[f'v{c}']=np.concatenate([common,unique]).astype(np.intp)
 union,_,indices=union_frequency_sets(view_bins,n); u=len(union)
 basis=(rng.standard_normal((r,n))+1j*rng.standard_normal((r,n))).astype(np.complex128)
 c0=(rng.standard_normal(r)+1j*rng.standard_normal(r)).astype(np.complex128)
 positions=np.sort(rng.choice(n,32,replace=False)).astype(np.intp)
 ops=[]
 for _ in range(updates):
  if rng.random()<.85:ops.append(('c',int(rng.integers(r)),complex(rng.standard_normal()*.01,rng.standard_normal()*.01)))
  else:ops.append(('p',int(rng.choice(positions)),complex(rng.standard_normal()*.01,rng.standard_normal()*.01)))
 if intervals is None: intervals=[1,2,4,8,16,32,64,128][:C]
 else: intervals=list(intervals)[:C]

 # Union registration: use a practical K about 4u, rounded to a power-of-two divisor.
 K=1
 target=max(1,4*u)
 while K<target:K*=2
 K=min(K,n)
 while n%K:K*=2
 t=time.perf_counter_ns(); plan=ArbitraryBinsDFTPlan(n,union,radix=K); union_proj=plan.project_stream(iter(basis)); pruned_reg=(time.perf_counter_ns()-t)/1e6
 full=FullFFTBinPlan(n,union)
 t=time.perf_counter_ns(); full_proj=np.stack([full.execute(row) for row in basis]); full_reg=(time.perf_counter_ns()-t)/1e6
 reg_err=float(np.max(np.abs(union_proj-full_proj)))

 def shared_run():
  st=SharedProjectedFourierStore(n,union,union_proj,view_bins,c0,prepared_positions=positions,event_capacity=256)
  checksum=0.0
  for t,(kind,key,d) in enumerate(ops,1):
   if kind=='c':st.add_coefficient(key,d)
   else:st.add_point(key,d)
   due=[name for vi,name in enumerate(view_bins) if t%intervals[vi]==0]
   if due:
    ans=st.query_many(due)
    for name in due:checksum += float(ans[name][0].real)
   if t%128==0:st.compact()
  return checksum,st.storage_bytes

 def separate_run():
  states={}
  for name,b in view_bins.items():
   proj=np.ascontiguousarray(union_proj[:,indices[name]])
   states[name]=ProjectedFourierState(n,b,proj,c0,prepared_positions=positions,event_capacity=256)
  checksum=0.0
  for t,(kind,key,d) in enumerate(ops,1):
   # Old architecture: every consumer receives every metadata update.
   for st in states.values():
    if kind=='c':st.add_coefficient(key,d)
    else:st.add_point(key,d)
   for vi,name in enumerate(view_bins):
    if t%intervals[vi]==0:checksum += float(states[name].query()[0].real)
   if t%128==0:
    for st in states.values():st.compact()
  numeric=sum(st.storage_bytes for st in states.values())
  return checksum,numeric

 # warm
 shared_run();separate_run()
 ts=med_ms(shared_run,5);tp=med_ms(separate_run,5)
 cs,shared_bytes=shared_run();cp,separate_bytes=separate_run()
 return {'n':n,'r':r,'consumers':C,'bins_per_consumer':q,'union_bins':u,'updates':updates,
  'query_intervals':intervals,'union_pruned_radix':K,'union_pruned_registration_ms':pruned_reg,
  'full_fft_registration_ms':full_reg,'registration_speedup':full_reg/pruned_reg,
  'registration_max_abs_error':reg_err,'shared_store_ms':ts,'separate_views_ms':tp,
  'shared_speedup_vs_separate':tp/ts,'shared_numeric_bytes':shared_bytes,
  'separate_numeric_bytes':separate_bytes,'numeric_storage_reduction':separate_bytes/shared_bytes,
  'checksum_abs_diff':abs(cs-cp),
  'hypothetical_full_basis_spectra_bytes':int(r*n*16),
  'union_projection_bytes':int(union_proj.nbytes),
  'basis_storage_reduction_vs_full':(r*n*16)/union_proj.nbytes}

if __name__=='__main__':
 rows=[]
 for label,intervals in [('heterogeneous',[1,2,4,8,16,32,64,128]),('synchronized',[64]*8)]:
  x=run(intervals=intervals);x['scenario']=label;print(label,json.dumps(x,indent=2));rows.append(x)
 open('benchmark_multi_view_results.json','w').write(json.dumps(rows,indent=2))
