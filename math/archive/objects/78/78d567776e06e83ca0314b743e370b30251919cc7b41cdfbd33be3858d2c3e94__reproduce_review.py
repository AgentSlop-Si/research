import os, sys, json, platform, collections
from pathlib import Path
import numpy as np
import scipy
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'latest'/'fft130_adaptive_merge'))
from projected_fourier import ProjectedFourierState
from relation_view import DynamicFourierState
from pruned_output import FirstKDFTPlan,BandDFTPlan

class CountDeque(collections.deque):
    visited=0
    def __iter__(self):
        for row in super().__iter__():
            self.visited+=1
            yield row
class CountList(list):
    copied=0
    def __getitem__(self,key):
        ans=super().__getitem__(key)
        if isinstance(key,slice): self.copied += len(ans)
        return ans

def backing(a):
    while isinstance(a.base,np.ndarray):a=a.base
    return a.nbytes

out={'versions':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__},'projected_log':[]}
for retained in [10,1000,100000]:
    st=ProjectedFourierState(8,[0],np.ones((1,1),complex))
    for _ in range(retained):st.add_coefficient(0,1)
    st.query() # rebuild previous history
    st.events=CountDeque(st.events)
    st.add_coefficient(0,1)
    got=st.query()
    out['projected_log'].append({'old_events':retained,'H':st.last_stats.backlog,'strategy':st.last_stats.strategy,'visited_events':st.events.visited,'correct':bool(got[0]==retained+1),'reported_storage_bytes':st.storage_bytes})

st=DynamicFourierState(np.ones((1,8),complex))
v=st.view([0]);st._events=CountList()
for _ in range(100000):st.add_coefficient(0,1)
got=v.query()
out['full_basis_planner']={'H':v.last_stats.backlog_events,'strategy':v.last_stats.strategy,'events_copied_before_rebuild':st._events.copied,'correct':bool(got[0]==100000)}

n,q=65536,16
full=np.fft.fft(np.arange(n,dtype=float))
proj=full[:q][None,:]
st=ProjectedFourierState(n,np.arange(q),proj,[1])
out['retained_projection']={'n':n,'q':q,'same_input_projection':st.projection is proj,'projection_visible_bytes':st.projection.nbytes,'projection_backing_bytes':backing(st.projection),'reported_storage_bytes':st.storage_bytes}

# Additional finite-size correctness sweeps, including n=1, zero basis, odd n,
# duplicate bins, unprepared complex point edits and cancellation, bounded log,
# wrapped bands, reusable plan across both backends. No perf claim from this.
rng=np.random.default_rng(20261008)
checks=0;max_err=0.0
for n in (1,3,8,31,64,256):
 for r in (0,1,4):
  b=rng.normal(size=(r,n))+1j*rng.normal(size=(r,n))
  c=rng.normal(size=r)+1j*rng.normal(size=r)
  bins=rng.integers(0,n,size=min(n+2,11))
  for cap in (None,0,2,16):
   st=ProjectedFourierState(n,bins,np.fft.fft(b,axis=1)[:,bins],c,event_capacity=cap)
   state=DynamicFourierState(np.fft.fft(b,axis=1),c)
   view=state.view(bins)
   x=c@b
   for t in range(35):
    d=complex(rng.normal()*.1,rng.normal()*.1)
    if r and t%2:
     i=t%r;st.add_coefficient(i,d);state.add_coefficient(i,d);x+=d*b[i]
    else:
     j=t%n;st.add_point(j,d);state.add_point(j,d);x[j]+=d
    if t%3==0:
     expected=np.fft.fft(x)[bins]
     for got in (st.query(),view.query()):
      err=float(np.max(np.abs(got-expected)));max_err=max(max_err,err);checks+=1
      assert np.allclose(got,expected,atol=2e-9,rtol=2e-11),(n,r,cap,t,err)
     # verify independent output handles
     a=st.query();a[:]=123456
     assert np.allclose(st.query(),expected,atol=2e-9,rtol=2e-11)
    if t%11==0:state.compact_event_log()
for n in (1,3,8,12,32,128,1024):
 x=rng.normal(size=n)+1j*rng.normal(size=n); full=np.fft.fft(x)
 for k in (1,2,3,4,8,16,n):
  if k>n or n%k:continue
  for backend in ('numpy','scipy'):
   for start in (0,n-1,n+2,-2):
    got=BandDFTPlan(n,k,start,backend=backend).execute(x)
    expected=full[(np.arange(k)+start)%n]
    err=float(np.max(np.abs(got-expected)));max_err=max(max_err,err);checks+=1
    assert np.allclose(got,expected,atol=2e-9,rtol=2e-11),(n,k,start,backend,err)
out['additional_correctness']={'comparisons':checks,'max_absolute_error':max_err,'passed':True}
print(json.dumps(out,indent=2))
