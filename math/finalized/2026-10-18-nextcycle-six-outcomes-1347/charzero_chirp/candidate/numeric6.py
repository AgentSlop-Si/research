import numpy as np
from scipy.optimize import least_squares
import itertools,time,json
q=np.exp(-2j*np.pi*np.arange(8)**2/16)
rng=np.random.default_rng(611018)
for counts in [(2,2,2,0),(3,0,2,1),(3,1,2,0),(4,0,1,1),(4,1,1,0),(3,0,3,0),(4,0,2,0),(5,0,1,0)]:
 def out(v):
  vv=v[:7]+1j*v[7:];p=np.zeros(8,complex);p[0]=1;jj=0
  for stride,n in enumerate(counts,1):
   f=np.zeros(8,complex);f[0]=1
   for k in range(1,n+1):f[stride*k%8]+=vv[jj];jj+=1
   p=np.fft.ifft(np.fft.fft(p)*np.fft.fft(f))
  return p-vv[-1]*q
 def fun(v):
  o=out(v);return np.r_[o.real,o.imag]
 best=(1e9,None)
 for run in range(40):
  guess=rng.standard_normal(14)
  ans=least_squares(fun,guess,max_nfev=2000,ftol=1e-12,xtol=1e-12,gtol=1e-12)
  err=np.linalg.norm(ans.fun)
  h=ans.x[6]+1j*ans.x[13]
  if abs(h)<1e-5:continue
  if err<best[0]:best=(err,ans.x.tolist())
  if err<1e-9:break
 print(counts,best,flush=True)
