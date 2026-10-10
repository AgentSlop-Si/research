import json,statistics,time
import numpy as np
try:
 from scipy import fft as sp_fft
except ImportError:
 sp_fft=None
from pruned_output import FirstKDFTPlan
from projected_fourier import ProjectedFourierState

def med(fn,reps=3):
 vals=[]
 for _ in range(reps):
  t=time.perf_counter_ns(); v=fn(); vals.append(((time.perf_counter_ns()-t)/1e6,v))
 vals.sort(key=lambda x:x[0]); return vals[len(vals)//2]

def run(n=262144,r=16,q=64,updates=512,H=4,seed=1701):
 rng=np.random.default_rng(seed)
 basis=(rng.standard_normal((r,n))+1j*rng.standard_normal((r,n))).astype(np.complex128)
 c0=(rng.standard_normal(r)+1j*rng.standard_normal(r)).astype(np.complex128)
 positions=np.sort(rng.choice(n,32,replace=False)).astype(np.intp)
 pos_idx={int(p):i for i,p in enumerate(positions)}
 ops=[]
 for _ in range(updates):
  if rng.random()<.8:
   ops.append(('c',int(rng.integers(r)),complex(rng.standard_normal()*.01,rng.standard_normal()*.01)))
  else:
   ops.append(('p',int(rng.choice(positions)),complex(rng.standard_normal()*.01,rng.standard_normal()*.01)))

 # Registration of only needed first-q bins.
 t=time.perf_counter_ns(); plan=FirstKDFTPlan(n,q); projection=plan.project_stream((row for row in basis)); reg_ms=(time.perf_counter_ns()-t)/1e6

 def projected_run():
  st=ProjectedFourierState(n,np.arange(q),projection,c0,prepared_positions=positions,event_capacity=r+len(positions)+8)
  checksum=0.0
  for t,(kind,key,d) in enumerate(ops,1):
   if kind=='c': st.add_coefficient(key,d)
   else: st.add_point(key,d)
   if t%H==0:
    checksum += float(st.query()[0].real); st.compact()
  return checksum

 def dense_fft_run():
  c=c0.copy(); x=c@basis; checksum=0.0
  for t,(kind,key,d) in enumerate(ops,1):
   if kind=='c': c[key]+=d; x += d*basis[key]
   else: x[key]+=d
   if t%H==0:
    y=sp_fft.fft(x) if sp_fft else np.fft.fft(x)
    checksum += float(y[0].real)
  return checksum

 # correctness final state
 st=ProjectedFourierState(n,np.arange(q),projection,c0,prepared_positions=positions,event_capacity=128)
 c=c0.copy(); x=c@basis
 for kind,key,d in ops:
  if kind=='c': st.add_coefficient(key,d); c[key]+=d; x+=d*basis[key]
  else: st.add_point(key,d); x[key]+=d
 got=st.query(); expected=(sp_fft.fft(x) if sp_fft else np.fft.fft(x))[:q]
 err=float(np.max(np.abs(got-expected)))

 tp,_=med(projected_run); td,_=med(dense_fft_run)
 return {'n':n,'r':r,'q':q,'updates':updates,'query_every':H,'queries':updates//H,
  'projected_registration_ms':reg_ms,'projected_steady_ms':tp,'dense_fft_steady_ms':td,
  'steady_speedup':td/tp,'max_abs_error':err,
  'projection_bytes':int(projection.nbytes),'full_basis_spectrum_bytes_if_cached':int(r*n*16),
  'persistent_storage_reduction':n/q}

if __name__=='__main__':
 out=[]
 for H in (1,4,16,64):
  x=run(H=H);print(x);out.append(x)
 with open('benchmark_end_to_end_view_results.json','w') as f:json.dump(out,f,indent=2)
