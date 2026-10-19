import numpy as np
from scipy.optimize import minimize
import json, sys
N=int(sys.argv[1]); r=int(sys.argv[2]); trials=int(sys.argv[3]) if len(sys.argv)>3 else 12
rng=np.random.default_rng(9917+N*100+r)
F=np.exp(-2j*np.pi*np.outer(np.arange(N),np.arange(N))/N)/np.sqrt(N)
def fun(x):
 V=np.exp(1j*x[:N,None])*F*np.exp(1j*np.r_[0,x[N:]][None,:])
 return np.linalg.svd(V.imag,compute_uv=False)[2*r]
best=2
for i in range(trials):
 x=rng.uniform(-np.pi,np.pi,2*N-1) if i else np.r_[np.full(N,np.pi/4),np.zeros(N-1)]
 out=minimize(fun,x,method='Powell',options={'maxiter':400,'xtol':1e-8,'ftol':1e-10})
 if out.fun<best:
  best=out.fun
  print(json.dumps({'N':N,'r':r,'trial':i,'value':out.fun,'lower':np.sin(np.pi/4-np.pi*(2*r+1)/(2*N)),'angles_pi':(out.x/np.pi).tolist()}),flush=True)
