import json,time,statistics
import numpy as np
try:
 from scipy import fft as sp_fft
except ImportError:
 sp_fft=None
from arbitrary_output import ArbitraryBinsDFTPlan,FullFFTBinPlan
from projected_fourier import ProjectedFourierState

def med_ms(fn,reps=3):
 vals=[]
 for _ in range(reps):
  t=time.perf_counter_ns();fn();vals.append((time.perf_counter_ns()-t)/1e6)
 return statistics.median(vals)

def run(n=262144,r=16,q=64,updates=512,H=4,seed=20261011):
 rng=np.random.default_rng(seed)
 bins=np.sort(rng.choice(n,q,replace=False)).astype(np.intp)
 basis=(rng.standard_normal((r,n))+1j*rng.standard_normal((r,n))).astype(np.complex128)
 c0=(rng.standard_normal(r)+1j*rng.standard_normal(r)).astype(np.complex128)
 positions=np.sort(rng.choice(n,32,replace=False)).astype(np.intp)
 ops=[]
 for _ in range(updates):
  if rng.random()<.8:ops.append(('c',int(rng.integers(r)),complex(rng.standard_normal()*.01,rng.standard_normal()*.01)))
  else:ops.append(('p',int(rng.choice(positions)),complex(rng.standard_normal()*.01,rng.standard_normal()*.01)))
 # practical random-bin radix near 4q
 K=1
 while K<4*q:K*=2
 K=min(K,n)
 t=time.perf_counter_ns();plan=ArbitraryBinsDFTPlan(n,bins,radix=K);projection=plan.project_stream(iter(basis));reg=(time.perf_counter_ns()-t)/1e6
 full=FullFFTBinPlan(n,bins)
 t=time.perf_counter_ns();refproj=np.stack([full.execute(row) for row in basis]);fullreg=(time.perf_counter_ns()-t)/1e6
 regerr=float(np.max(np.abs(projection-refproj)))
 def projected():
  st=ProjectedFourierState(n,bins,projection,c0,prepared_positions=positions,event_capacity=r+len(positions)+16)
  s=0.0
  for t,(kind,key,d) in enumerate(ops,1):
   if kind=='c':st.add_coefficient(key,d)
   else:st.add_point(key,d)
   if t%H==0:s+=float(st.query()[0].real);st.compact()
  return s
 def dense():
  c=c0.copy();x=c@basis;s=0.0
  for t,(kind,key,d) in enumerate(ops,1):
   if kind=='c':c[key]+=d;x+=d*basis[key]
   else:x[key]+=d
   if t%H==0:
    y=sp_fft.fft(x) if sp_fft else np.fft.fft(x);s+=float(y[bins[0]].real)
  return s
 tp=med_ms(projected,3);td=med_ms(dense,3)
 # final correctness
 st=ProjectedFourierState(n,bins,projection,c0,prepared_positions=positions,event_capacity=128);c=c0.copy();x=c@basis
 for kind,key,d in ops:
  if kind=='c':st.add_coefficient(key,d);c[key]+=d;x+=d*basis[key]
  else:st.add_point(key,d);x[key]+=d
 err=float(np.max(np.abs(st.query()-(sp_fft.fft(x) if sp_fft else np.fft.fft(x))[bins])))
 return {'n':n,'r':r,'q':q,'updates':updates,'query_every':H,'radix':K,
  'arbitrary_pruned_registration_ms':reg,'full_fft_registration_ms':fullreg,'registration_speedup':fullreg/reg,
  'registration_max_abs_error':regerr,'projected_steady_ms':tp,'dense_fft_steady_ms':td,'steady_speedup':td/tp,
  'projection_bytes':int(projection.nbytes),'hypothetical_full_basis_spectra_bytes':int(r*n*16),
  'persistent_storage_reduction':n/q,'max_abs_error':err}
if __name__=='__main__':
 x=run();print(json.dumps(x,indent=2));open('benchmark_arbitrary_end_to_end_results.json','w').write(json.dumps(x,indent=2))
