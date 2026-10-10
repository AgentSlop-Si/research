import os
os.environ['OPENBLAS_NUM_THREADS']='1'
from pathlib import Path
import numpy as np,scipy.linalg as la,json,sys
root=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(root/'seed_compatibility_gate'))
from check_lift_defects import cover_and_splice,fiber
from check_hierarchical_lift import lift
from check_n16_outer_gate import LABELS
p=json.loads((root/'n16_existence_milestone/DYADIC_AFFINE_CHART.json').read_text());s=2.**p['dyadic_exponent']
a=(np.asarray(p['center_real'],dtype=float)+1j*np.asarray(p['center_imag'],dtype=float))/s
v=(np.asarray(p['directions_real'],dtype=float)+1j*np.asarray(p['directions_imag'],dtype=float))/s
gs=[]
for j,label in enumerate(LABELS):
 t,pp,_=cover_and_splice(4,4,label);_,q,_=lift(t,pp,4,4,label);tau=1/(j+2);g=np.zeros((64,64))
 for col in range(64):
  r=col;c=1/(1-tau**64)
  for _ in range(64):g[r,col]=c;r=q[r];c*=tau
 gs.append(g)
gs=np.asarray(gs)
aa=np.zeros((2,64,8),complex);vv=np.zeros((2,64,8,256),complex)
for small in range(16):
 for large in fiber(small,4,4):aa[:,large]=a[:2,small];vv[:,large]=v[:2,small]
h=np.einsum('lij,jik->lik',aa,gs);dh=np.einsum('lijt,jik->likt',vv,gs)
u=np.exp(2j*np.pi/64);bank=np.eye(64,dtype=complex)
for x in [0,1,4,5]:bank[8*x:8*x+8,8*x:8*x+8]=u**(8*np.arange(8)[:,None]*np.arange(8)[None,:])
x=h[1]@bank@h[0];hh=np.max(np.sum(abs(h.real)+abs(h.imag),axis=2),axis=1);ll=np.max(np.sum(abs(dh.real)+abs(dh.imag),axis=(2,3)),axis=1)
for i in range(3):
 templates=gs[:,i,:]@x;target=u**(i*np.arange(64));mat=np.concatenate([templates,target[None,:]])
 scales=np.maximum(np.max(np.abs(mat),axis=1),1e-300);_,_,columns=la.qr((mat/scales[:,None]),pivoting=True,mode='economic');cols=columns[:9]
 inverse=la.inv(mat[:,cols]);f=inverse[:,:8]@gs[:,i,:];fbound=np.sum(abs(f.real)+abs(f.imag),axis=1)
 variation=9*fbound*8*(ll[1]*2e-12*(hh[0]+ll[0]*2e-12)+hh[1]*ll[0]*2e-12)
 print(i,cols.tolist(),np.max(abs(inverse@mat[:,cols]-np.eye(9))),max(fbound),hh,ll,max(variation))
 if i==0:np.savez(Path(__file__).resolve().parent/'PROPOSED_MINOR.npz',row=i,columns=cols,inverse=inverse)
