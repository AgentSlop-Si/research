"""Fresh bounded numerical hypothesis probe; not an exact certificate."""
import numpy as np
from scipy.optimize import least_squares
import json, time

N=8
omega=np.exp(2j*np.pi/N)
chi=np.exp(1j*np.pi/N)
z=omega**np.arange(N)
c=chi**(-np.arange(N)**2)
target=sum(c[j]*z**j for j in range(N))

def unpack(x): return x[:7]+1j*x[7:]
def fun(x,a,b):
    r,s,t,u,p,q,g=unpack(x)
    d=(1-r*z)*(1-s*z)*(1-t*z)*(1-u*z)
    n1=(1-s*z)+p*z**a*(1-r*z)
    n2=(1-u*z)+q*z**b*(1-t*z)
    v=(target*d-g*n1*n2)
    return np.r_[v.real,v.imag]

if __name__=='__main__':
    rng=np.random.default_rng(249)
    results=[]
    for a in range(5):
      for b in range(a,5):
        best=None
        for seed in range(4):
          x=rng.normal(size=14)*0.5
          x[6]=1
          fit=least_squares(fun,x,args=(a,b),max_nfev=1200,ftol=1e-12,gtol=1e-12,xtol=1e-12)
          err=float(np.max(np.abs(fun(fit.x,a,b))))
          v=unpack(fit.x)
          guard=float(min(abs(1-v[j]**8) for j in range(4)))
          row={'a':a,'b':b,'seed':seed,'error':err,'guard_min':guard,'nfev':fit.nfev,'values':[[float(w.real),float(w.imag)] for w in v]}
          if best is None or err<best['error']: best=row
          if err<1e-9 and guard>1e-5 and min(abs(w) for w in v)>1e-5:
            print('CANDIDATE',json.dumps(row),flush=True)
        results.append(best)
        print('BEST',json.dumps(best),flush=True)
    with open('shifted_chart_probe_results.json','w') as f:json.dump(results,f,indent=2)
