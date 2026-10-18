import numpy as np,json
from scipy.optimize import minimize
from scipy.special import logsumexp
from pathlib import Path
folder=Path(__file__).parent
A=-2*np.pi*np.outer(np.arange(8),np.arange(8))/8
rng=np.random.default_rng(2112)
def obj(x,tau):
 phase=x[:8,None]+np.r_[0,x[8:]][None,:]+A
 Y=np.sin(phase)/np.sqrt(8);C=np.cos(phase)/np.sqrt(8)
 v,U=np.linalg.eigh(Y@Y.T); w=np.exp((v[:6]-v[5])/tau);w/=sum(w)
 dY=2*(U[:,:6]*w)@U[:,:6].T@Y
 D=dY*C
 return v[5]+tau*np.log(np.sum(np.exp((v[:6]-v[5])/tau))),np.r_[D.sum(axis=1),D.sum(axis=0)[1:]]
def sv(x):return np.linalg.svd(np.sin(x[:8,None]+np.r_[0,x[8:]][None,:]+A)/np.sqrt(8),compute_uv=False)
best=1;out=[]
for it in range(100):
 x=rng.uniform(-np.pi,np.pi,15)
 if it==0:x=np.array(json.loads((folder/'numeric_best.json').read_text())['x'])
 for tau in [0.05,0.01,0.002,0.0004,0.00008,0.000016,0.0000032,0.00000064,1e-8]:
  r=minimize(obj,x,args=(tau,),jac=True,method='BFGS',options={'maxiter':1000,'gtol':1e-10});x=r.x
 s=sv(x);entry={'it':it,'value':float(s[2]),'x':x.tolist(),'singular':s.tolist()};out.append(entry)
 if s[2]<best:
  best=s[2];print(it,best,s,np.mod(x,np.pi)/np.pi,flush=True);(folder/'smooth_best.json').write_text(json.dumps(entry,indent=2))
(folder/'smooth_runs.json').write_text(json.dumps(out,indent=2))
