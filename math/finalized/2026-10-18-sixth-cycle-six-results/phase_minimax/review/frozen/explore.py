import numpy as np
from scipy.optimize import minimize
from pathlib import Path
F=np.exp(-2j*np.pi*np.outer(np.arange(8),np.arange(8))/8)/np.sqrt(8)
def sy(x):return np.linalg.svd(np.imag(np.exp(1j*x[:8,None])*F*np.exp(1j*np.r_[0,x[8:]][None,:])),compute_uv=False)
def f(x):return sy(x)[2]
rng=np.random.default_rng(18102111)
best=1
rows=[]
for it in range(60):
 x=rng.uniform(-np.pi,np.pi,15)
 if it==0:
  # A=1, G=e^{i pi/8}; q=(1,e^{i pi/8},1,i e^{i pi/8})
  p=np.array([0,np.pi/8,0,5*np.pi/8]*2); q=np.array([0,np.pi/8,0,5*np.pi/8]*2);x=np.r_[p,q[1:]]
 r=minimize(f,x,method='Powell',options={'maxiter':1500,'xtol':1e-9,'ftol':1e-10})
 rows.append({'it':it,'value':r.fun,'x':r.x.tolist(),'singular':sy(r.x).tolist(),'success':bool(r.success)})
 if r.fun<best:
  best=r.fun;print(it,best,sy(r.x),np.mod(r.x,np.pi)/np.pi,flush=True)
  import json;(Path(__file__).resolve().parent / 'numeric_best.json').write_text(json.dumps(rows[-1],indent=2))
import json;(Path(__file__).resolve().parent / 'numeric_runs.json').write_text(json.dumps(rows,indent=2))
