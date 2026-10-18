import sys,json,time,itertools
import numpy as np
import sympy as sp
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import coo_matrix
N=int(sys.argv[1]);d=int(sys.argv[2]);limit=float(sys.argv[3]) if len(sys.argv)>3 else 30
x=sp.Symbol('x'); phi=sp.Poly(sp.cyclotomic_poly(N,x),x); deg=phi.degree()
roots=[]
for t in range(N):
 p=sp.Poly(x**t,x).rem(phi); roots.append([int(p.nth(k)) for k in range(deg)])
pairs=list(itertools.combinations(range(N),2)); nvars=N*N+N*len(pairs)
rr=[];cc=[];vv=[];lo=[];hi=[]
def con(terms,l,h=None):
 k=len(lo)
 for c,v in terms:
  if v: rr.append(k);cc.append(c);vv.append(v)
 lo.append(l);hi.append(l if h is None else h)
for r in range(N):con([(r*N+c,1) for c in range(N)],d)
for c in range(N):con([(r*N+c,1) for r in range(N)],d)
for a,(j,k) in enumerate(pairs):
 for r in range(N):
  z=N*N+a*N+r;u=r*N+j;v=r*N+k
  con([(z,1),(u,-1)],-np.inf,0);con([(z,1),(v,-1)],-np.inf,0);con([(z,1),(u,-1),(v,-1)],-1,np.inf)
 for b in range(deg): con([(N*N+a*N+r,roots[(r*(k-j))%N][b]) for r in range(N)],0)
if len(sys.argv)>4:
 a=pairs.index((0,1)); con([(N*N+a*N+r,1) for r in range(N)],int(sys.argv[4]))
A=coo_matrix((vv,(rr,cc)),shape=(len(lo),nvars)).tocsc()
start=time.time();res=milp(np.zeros(nvars),integrality=np.ones(nvars),bounds=Bounds(0,1),constraints=LinearConstraint(A,lo,hi),options={'time_limit':limit,'presolve':True})
out={'N':N,'d':d,'message':res.message,'status':res.status,'seconds':time.time()-start,'nodes':getattr(res,'mip_node_count',None)}
if res.x is not None:
 R=np.rint(res.x[:N*N]).astype(int).reshape(N,N);out['R']=R.tolist();out['objective']=res.fun
 # independent exact check
 out['exact_gram']=all(sum(R[r,j]*R[r,k]*roots[(r*(k-j))%N][b] for r in range(N))==(d if j==k and b==0 else 0) for j in range(N) for k in range(N) for b in range(deg))
print(json.dumps(out,indent=2))
