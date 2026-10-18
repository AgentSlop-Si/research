"""Fresh numeric discovery only. Never an infeasibility certificate."""
import numpy as np
from scipy.optimize import least_squares
import json,time,os
P=np.array([7,0,6,3,4,1,2,5]); n=8
F=np.exp(2j*np.pi*np.outer(np.arange(n),np.arange(n))/n)
def stages(z, derivatives=False):
 d=z[:8]; m=np.r_[1,z[8:14],0]; u=np.r_[1,z[14:20],0]; v=np.r_[0,z[20:26],1]
 A=np.diag(d)+np.tril(np.outer(np.ones(8),m),-1)+np.triu(np.outer(u,v),1)
 d=z[26:34]; l=np.r_[0,z[34:40],1]; m=z[40:47]; u=np.r_[1,z[47:53],0]; v=np.r_[0,z[53:60]]
 B=np.diag(d)+np.tril(np.outer(l,np.r_[m,0]),-1)+np.triu(np.outer(u,v),1)
 return A,B
def residual(x):
 z=x[:60]+1j*x[60:]; A,B=stages(z); E=B[:,P]@A-F
 return np.r_[E.real.ravel(),E.imag.ravel()]
def jac(x):
 z=x[:60]+1j*x[60:]; A,B=stages(z); J=np.zeros((64,60),complex)
 # Each variable occurs affinely in the product in this disjoint stage chart.
 for k in range(60):
  zz=z.copy();zz[k]+=1
  AA,BB=stages(zz);J[:,k]=((BB-B)[:,P]@A+B[:,P]@(AA-A)).ravel()
 return np.block([[J.real,-J.imag],[J.imag,J.real]])
if __name__=='__main__':
 rng=np.random.default_rng(6081218);records=[]
 for k in range(12):
  x=rng.normal(size=120)*0.6
  start=time.time();r=least_squares(residual,x,jac=jac,method='lm',max_nfev=600,ftol=1e-11,xtol=1e-11,gtol=1e-11)
  norm=float(np.linalg.norm(r.fun)); z=r.x[:60]+1j*r.x[60:];A,B=stages(z)
  rec=dict(start=k,norm=norm,cost=float(r.cost),nfev=r.nfev,seconds=time.time()-start,max_param=float(np.max(np.abs(z))),detA=abs(np.linalg.det(A)),detB=abs(np.linalg.det(B)))
  records.append(rec);print(json.dumps(rec),flush=True)
  np.savez(f'numeric_{k:02d}.npz',x=r.x,residual=r.fun)
  open('NUMERIC_DISCOVERY.json','w').write(json.dumps(records,indent=2)+'\n')
  if norm<1e-9:break
