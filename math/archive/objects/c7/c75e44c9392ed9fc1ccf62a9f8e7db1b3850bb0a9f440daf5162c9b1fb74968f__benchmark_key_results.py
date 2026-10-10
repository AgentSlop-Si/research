import json,time
import numpy as np
try:
 from scipy.fft import fft
except ImportError:
 from numpy.fft import fft
from lazy_spectrum import LazySpectrum,PreparedBinView,BufferedSpectrum,direct_sparse_correction
rng=np.random.default_rng(202610093)

def med(fn,reps=3):
 ts=[];out=None
 for _ in range(reps):
  t=time.perf_counter_ns();out=fn();ts.append((time.perf_counter_ns()-t)/1e6)
 return float(np.median(ts)),out
rows=[]
# Prepared selective view
n=262144;U=500;k=32;q=64
x0=rng.standard_normal(n)+1j*rng.standard_normal(n);support=rng.choice(n,k,replace=False);bins=np.sort(rng.choice(n,q,replace=False));slots=rng.integers(0,k,U);deltas=rng.normal(scale=.05,size=U)+1j*rng.normal(scale=.05,size=U)
def fresh():
 x=x0.copy();_=fft(x);out=None
 for s,d in zip(slots,deltas):x[support[s]]+=d;out=fft(x)[bins]
 return out
def eager():
 cached=fft(x0);ph=np.exp((-2j*np.pi/n)*np.multiply.outer(support.astype(float),np.arange(n,dtype=float)));out=None
 for s,d in zip(slots,deltas):cached += d*ph[s];out=cached[bins]
 return out,ph.nbytes
def prep():
 v=PreparedBinView(fft(x0),support.tolist(),bins.tolist());out=None
 for s,d in zip(slots,deltas):v.add_edit(int(support[s]),d);out=v.values()
 return out,v.phase_bytes
Tf,Of=med(fresh);Te,Oe=med(eager);Tp,Op=med(prep)
x=x0.copy()
for s,d in zip(slots,deltas):x[support[s]]+=d
truth=fft(x)[bins]
for z in [Of,Oe[0],Op[0]]:assert np.allclose(z,truth,rtol=1e-9,atol=1e-7)
rows.append(dict(case='prepared_bin_view',n=n,updates=U,support=k,bins=q,fresh_ms=Tf,eager_ms=Te,prepared_ms=Tp,speedup_vs_fresh=Tf/Tp,speedup_vs_eager=Te/Tp,phase_bytes=Op[1],full_phase_bytes=Oe[1],memory_reduction=Oe[1]/Op[1]))
# Buffered mixed workload
U=512;H=4;q=64
x0=rng.standard_normal(n)+1j*rng.standard_normal(n);locs=rng.choice(n,U,replace=False);vals=rng.normal(scale=.05,size=U)+1j*rng.normal(scale=.05,size=U);bins=np.sort(rng.choice(n,q,replace=False))
def f2():
 x=x0.copy();_=fft(x);out=None
 for i,(j,d) in enumerate(zip(locs,vals),1):x[j]+=d;out=fft(x)[bins] if i%H==0 else out
 return out
def never():
 s=LazySpectrum.from_spectrum(fft(x0));out=None
 for i,(j,d) in enumerate(zip(locs,vals),1):s.add_edit(int(j),d);out=s.bins(bins) if i%H==0 else out
 return out
def buf():
 s=BufferedSpectrum.from_spectrum(fft(x0),flush_threshold=128,flush_method='native');out=None
 for i,(j,d) in enumerate(zip(locs,vals),1):s.add_edit(int(j),d);out=s.bins(bins) if i%H==0 else out
 return out,s.flush_count
Tf,Of=med(f2);Tn,On=med(never);Tb,Ob=med(buf)
x=x0.copy();x[locs]+=vals;truth=fft(x)[bins]
for z in [Of,On,Ob[0]]:assert np.allclose(z,truth,rtol=1e-9,atol=1e-7)
rows.append(dict(case='buffered_mixed',n=n,updates=U,bins=q,updates_per_query=H,threshold=128,fresh_ms=Tf,never_flush_ms=Tn,buffered_ms=Tb,speedup_vs_fresh=Tf/Tb,speedup_vs_never=Tn/Tb,flushes=Ob[1]))
# Low-rank partial
r=4;k=64;q=64
basis_t=rng.standard_normal((r,n));basis=fft(basis_t,axis=1);coef=rng.normal(size=r);loc=rng.choice(n,k,replace=False);val=rng.normal(size=k);ed=list(zip(loc.tolist(),val.tolist()));bins=np.sort(rng.choice(n,q,replace=False))
def eg():
 dense=np.einsum('r,rn->n',coef,basis);corr=direct_sparse_correction(n,{int(j):complex(v) for j,v in ed});return (dense+corr)[bins]
def lz():return LazySpectrum.from_basis(basis,coef,edits=ed).bins(bins)
Te,Oe=med(eg);Tl,Ol=med(lz);assert np.allclose(Oe,Ol,rtol=1e-9,atol=1e-7)
rows.append(dict(case='low_rank_sparse_partial',n=n,r=r,k=k,bins=q,eager_ms=Te,lazy_ms=Tl,speedup=Te/Tl))
print(json.dumps(rows,indent=2))
open('benchmark_key_results.json','w').write(json.dumps(rows,indent=2))
