import numpy as np,json
n=8
F=np.exp(-2j*np.pi*np.outer(np.arange(n),np.arange(n))/n)/np.sqrt(n)
z=np.exp(1j*np.pi/16);q=z**np.array([0,2,0,10,0,2,0,10]);p=z*q
V=p[:,None]*F*q[None,:];X=V.real;Y=V.imag
w,O=np.linalg.eigh(Y@Y);T=O[:,:6]
Ds=[]
for t in range(15):
 x=np.zeros(8);y=np.zeros(8)
 if t<8:x[t]=1
 else:y[t-7]=1
 dY=x[:,None]*X+X*y[None,:]
 Ds.append(T.T@(Y.T@dY+dY.T@Y)@T)
M=np.array([d.ravel() for d in Ds]).T
_,sv,VT=np.linalg.svd(M)
print('tangent singular values',sv)
print('traces',[np.trace(d) for d in Ds])
print('nullspace',VT[sv<1e-8])
print('diagonal',np.diag(X@Y@(T@T.T)))
print('V eigenphases',np.angle(np.linalg.eigvals(V))/np.pi)
print('Y eigenvalues',np.linalg.eigvalsh(Y))
s=np.sin(np.pi/16);c=np.cos(np.pi/16);L=T@T.T;R=np.eye(8)-L;G=T.T@X@Y@T/(s*c);Z=(1.5*np.eye(6)-.5*G)/8
print('Z eig',np.linalg.eigvalsh(Z),'stationarity',[np.trace(Z@d) for d in Ds])
# nonperiodic parameters x[r]=u[r],x[r+4]=-u[r],y similarly
D=[]
for t in range(8):
 x=np.zeros(8);y=np.zeros(8)
 if t<4:x[t]=1;x[t+4]=-1
 else:y[t-4]=1;y[t]=-1
 D.append(x[:,None]+y[None,:])
def eff(u):
 D0=sum(u[k]*D[k] for k in range(8));Y1=X*D0;Y2=-Y*D0**2/2
 H1=Y.T@Y1+Y1.T@Y
 H2=Y1.T@Y1+Y.T@Y2+Y2.T@Y
 return T.T@(H2-H1@R@H1/(c*c-s*s))@T
B=np.zeros((8,8))
for k in range(8):
 e=np.eye(8)[k];B[k,k]=np.trace(Z@eff(e))
 for l in range(k):
  f=np.eye(8)[l];B[k,l]=B[l,k]=(np.trace(Z@eff(e+f))-B[k,k]-B[l,l])/2
print('weighted Hessian',B,'eigs',np.linalg.eigvalsh(B))
