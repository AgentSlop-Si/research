"""Exploratory numerical fitting of two arbitrary rook operators; no FFT speed claim."""
import numpy as np
from scipy.optimize import least_squares
from math import pi

def search(s,seed=202616,max_nfev=150):
 n=s*s
 ij=np.arange(n)
 U=np.exp(-2j*pi*np.outer(ij,ij)/n)/s
 mask=np.array([[i//s==j//s or i%s==j%s for j in range(n)]for i in range(n)])
 row,col=np.nonzero(mask);d=len(row)
 rng=np.random.default_rng(seed)
 def unpack(q):
  X=np.zeros((n,n),dtype=complex);Y=X.copy()
  p=q[:2*d];v=p[:d]+1j*p[d:]
  p=q[2*d:];w=p[:d]+1j*p[d:]
  X[row,col]=v;Y[row,col]=w
  return X,Y
 def func(q):
  X,Y=unpack(q)
  Z=Y@X-U
  return np.r_[Z.real.ravel(),Z.imag.ravel()]
 x0=np.r_[rng.normal(scale=.2,size=4*d)]
 # initialize identity blocks
 X,Y=unpack(x0)
 X+=np.eye(n);Y+=np.eye(n)
 x0=np.r_[X[row,col].real, X[row,col].imag,Y[row,col].real,Y[row,col].imag]
 res=least_squares(func,x0,max_nfev=max_nfev,ftol=1e-12,gtol=1e-12,xtol=1e-12)
 X,Y=unpack(res.x)
 print('s',s,'d',d,'success',res.success,'nfev',res.nfev,'resid',np.linalg.norm(Y@X-U),'rankX',np.linalg.matrix_rank(X),'rankY',np.linalg.matrix_rank(Y))
 return X,Y,res
if __name__=='__main__':search(2)
