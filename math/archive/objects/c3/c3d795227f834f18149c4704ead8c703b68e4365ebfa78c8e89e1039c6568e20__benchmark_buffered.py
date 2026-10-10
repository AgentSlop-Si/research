import json,time
import numpy as np
try:
    from scipy.fft import fft
except ImportError:
    from numpy.fft import fft
from lazy_spectrum import LazySpectrum, BufferedSpectrum, suggest_flush_threshold

rng=np.random.default_rng(202610092)
rows=[]

def run_once(fn):
    t0=time.perf_counter_ns();out=fn();return (time.perf_counter_ns()-t0)/1e6,out

for n in [65536,262144]:
  updates=512;q=64
  for H in [4,16,64]:
    x0=rng.standard_normal(n)+1j*rng.standard_normal(n)
    locs=rng.choice(n,size=updates,replace=False)
    vals=rng.normal(scale=.05,size=updates)+1j*rng.normal(scale=.05,size=updates)
    bins=np.sort(rng.choice(n,size=q,replace=False))

    def fresh():
      x=x0.copy();_=fft(x);out=None
      for i,(j,d) in enumerate(zip(locs,vals),1):
        x[j]+=d
        if i%H==0:out=fft(x)[bins]
      return out

    def never_flush():
      x=x0.copy();s=LazySpectrum.from_spectrum(fft(x));out=None
      for i,(j,d) in enumerate(zip(locs,vals),1):
        x[j]+=d;s.add_edit(int(j),complex(d))
        if i%H==0:out=s.bins(bins)
      return out

    tf,of=run_once(fresh)
    tn,on=run_once(never_flush)
    best=(1e99,None,None)
    candidates=sorted(set([16,32,64,128,256,512,suggest_flush_threshold(n,q,H,backend='native')]))
    candrows=[]
    for B in candidates:
      if B>updates: continue
      def buffered(B=B):
        x=x0.copy();s=BufferedSpectrum.from_spectrum(fft(x),flush_threshold=B,flush_method='native');out=None
        for i,(j,d) in enumerate(zip(locs,vals),1):
          x[j]+=d;s.add_edit(int(j),complex(d))
          if i%H==0:out=s.bins(bins)
        return out,s.flush_count,s.pending_count
      tb,ob=run_once(buffered)
      candrows.append((B,tb,ob[1],ob[2]))
      if tb<best[0]:best=(tb,B,ob)
    x=x0.copy();x[locs]+=vals;truth=fft(x)[bins]
    assert np.allclose(of,truth,rtol=1e-9,atol=1e-7)
    assert np.allclose(on,truth,rtol=1e-9,atol=1e-7)
    assert np.allclose(best[2][0],truth,rtol=1e-9,atol=1e-7)
    row=dict(n=n,updates=updates,bins=q,updates_per_query=H,fresh_ms=tf,never_flush_ms=tn,
             best_buffered_ms=best[0],best_threshold=best[1],best_flush_count=best[2][1],
             buffered_vs_fresh=tf/best[0],buffered_vs_never=tn/best[0],proxy_threshold=suggest_flush_threshold(n,q,H,backend='native'),
             candidates=[{'threshold':b,'ms':t,'flushes':f,'pending':p} for b,t,f,p in candrows])
    rows.append(row);print(row)
with open('benchmark_buffered_results.json','w') as f:json.dump(rows,f,indent=2)
