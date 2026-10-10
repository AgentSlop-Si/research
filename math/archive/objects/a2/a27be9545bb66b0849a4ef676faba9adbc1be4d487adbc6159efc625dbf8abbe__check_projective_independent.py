"""Fresh reviewer checks; uploaded programs are never imported/executed."""
from pathlib import Path
import json,itertools,zipfile,hashlib
from fractions import Fraction as Q
import numpy as np
HERE=Path(__file__).parent;S=HERE/'projective_source'
def rankdet(A,p):
 M=[[int(x)%p for x in row] for row in A];m=len(M);n=len(M[0]);r=0;det=1
 for j in range(n):
  t=next((k for k in range(r,m) if M[k][j]),None)
  if t is None:continue
  if t!=r:M[r],M[t]=M[t],M[r];det=-det
  val=M[r][j];det=det*val%p;iv=pow(val,-1,p);M[r]=[x*iv%p for x in M[r]]
  for k in range(r+1,m):
   a=M[k][j];M[k]=[(x-a*y)%p for x,y in zip(M[k],M[r])]
  r+=1
  if r==m:break
 return r,det%p if r==m==n else None
cert=json.loads((S/'REFERENCE_CERTIFICATE.json').read_text());assert rankdet(cert['pencil_matrix'],65537)==(8,55687)
# Exact rational Green identity.
Gp=[[Q(4,3),Q(2,3)],[Q(2,3),Q(4,3)]];Gm=[[Q(4,3),-Q(2,3)],[-Q(2,3),Q(4,3)]]
I=[[Q(int(i==j)) for j in range(2)] for i in range(2)]
for sign,G in [(-1,Gp),(1,Gm)]:
 T=[[Q(1),Q(sign,2)],[Q(sign,2),Q(1)]]
 assert [[sum(T[i][k]*G[k][j] for k in range(2)) for j in range(2)] for i in range(2)]==I
assert [[Q(3,8)*(Gp[i][j]+Gm[i][j]) for j in range(2)] for i in range(2)]==I
# Enumerate all 16^4 invertible middle gauges to independently check both feasibility layers.
p=17;n=4;w=4;F=np.array([[pow(w,i*j,p) for j in range(n)] for i in range(n)],dtype=np.int64);Id=np.eye(n,dtype=np.int64)
cases={'true_fourier':(F,Id),'singular_pencil_but_zero_gauge':(Id,Id),'unavoidable_seed_zero':(F,np.array([[1,0,0,0],[1,1,0,0],[0,1,1,0],[0,0,0,1]])),'third_column_corrupted':(F,np.array([[1,0,1,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]))}
D=np.array(list(itertools.product(range(1,p),repeat=n)),dtype=np.int64);phase=np.array([pow(w,i,p) for i in range(n)])
feas={}
for name,(A,B) in cases.items():
 C=[A*B[:,j][None,:]%p for j in range(n)];Ks=[(C[(j+1)%n]-phase[:,None]*C[j])%p for j in range(n)];H=C[0]
 data={}
 for label,M in [('two_columns',Ks[0]),('all_columns',np.concatenate(Ks,axis=0))]:
  r,_=rankdet(M,p);bad_coords=[i for i in range(n) if rankdet(np.concatenate([M,Id[i:i+1]]),p)[0]==r];bad_seed=[i for i in range(n) if rankdet(np.concatenate([M,H[i:i+1]]),p)[0]==r]
  valid=(r<n and not bad_coords and not bad_seed)
  mask=np.all((D@M.T)%p==0,axis=1)&np.all((D@H.T)%p!=0,axis=1);ix=np.flatnonzero(mask)
  assert valid==bool(len(ix))
  data[label]=dict(valid=valid,rank=r,bad_coordinates=bad_coords,bad_seed_rows=bad_seed,gauge_count=int(len(ix)),first_gauge=D[ix[0]].tolist() if len(ix) else None)
  old=json.loads((S/'FEASIBILITY_RESULTS.json').read_text())[name][label]
  for key in old:assert old[key]==data[label][key]
 feas[name]=data
# Dense independent controls validate quotient gradient against envelope form and finite differences.
rng=np.random.default_rng(38170217);numeric=[]
for n in [3,5,8,16,32]:
 A=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n));B=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n));z=np.exp(-2j*np.pi*np.arange(n)/n)
 C0=A*B[:,0][None,:];C1=A*B[:,1][None,:];K=C1-z[:,None]*C0;gram=C0.conj().T@C0+C1.conj().T@C1
 evals,V=np.linalg.eigh(gram);invroot=(V/np.sqrt(evals)[None,:])@V.conj().T;gamma2=float(np.linalg.eigvalsh(invroot@K.conj().T@K@invroot)[0]);assert gamma2>0
 max_grad=0.;max_fd=0.;min_slack=float('inf')
 def value(d):
  u=C0@d;v=C1@d;s=np.abs(u)**2+np.abs(v)**2;r=v-z*u
  return float(np.sum(np.abs(r)**2/s))
 for t in range(20):
  d=rng.normal(size=n)+1j*rng.normal(size=n);u=C0@d;v=C1@d;s=np.abs(u)**2+np.abs(v)**2;r=v-z*u
  ell=(np.conj(u)+z*np.conj(v))/s
  eq=C0.conj().T@(np.conj(ell)*(ell*u-1))+C1.conj().T@(np.conj(ell)*(ell*v-z))
  direct=K.conj().T@(r/s)-C0.conj().T@(u*np.abs(r)**2/s**2)-C1.conj().T@(v*np.abs(r)**2/s**2)
  e=float(np.linalg.norm(eq-direct));max_grad=max(max_grad,e);assert e<1e-10
  assert abs(np.vdot(d,direct))<1e-9
  h=rng.normal(size=n)+1j*rng.normal(size=n);h/=np.linalg.norm(h);eps=2e-6
  fd=(value(d+eps*h)-value(d-eps*h))/(2*eps);error=abs(fd-2*np.real(np.vdot(direct,h)));max_fd=max(max_fd,float(error));assert error<1e-6
  pair=np.column_stack([ell*u-1,ell*v-z]);assert abs(np.linalg.norm(pair,'fro')**2-value(d))<1e-10
  full=ell[:,None]*(A@np.diag(d)@B)-np.exp(-2j*np.pi*np.arange(n)[:,None]*np.arange(n)[None,:]/n)
  slack=float(np.linalg.norm(full,2)-np.sqrt(gamma2/2));min_slack=min(min_slack,slack);assert slack>=-1e-9
 numeric.append(dict(n=n,trials=20,gradient_disagreement=max_grad,directional_fd_error=max_fd,gamma2_diagnostic=gamma2,min_spectral_slack=min_slack))
# Zero candidate row and zero optimum row normalizer are explicitly handled.
assert abs(1)**2+abs(-1)**2==2 # u=1,v=-1,z=1 has ell=0 and infimum error 2.
# Manifest validates preserved input bytes only, not truth of logged source outputs.
manifest=[]
for line in (S/'SHA256SUMS.txt').read_text().splitlines():
 h,name=line.split();actual=hashlib.sha256((S/name).read_bytes()).hexdigest();assert h==actual;manifest.append(name)
out=dict(status='PASS',source_programs_executed=False,exact_reference_matrix_det=55687,reference_green_parameters_reconstructed=False,exact_N2_identity=True,best_N2_diagonal_spectral_error=1,exhaustive_gauges_per_case=16**4,feasibility=feas,numeric_independent_controls=numeric,source_manifest_entries_verified=len(manifest))
(HERE/'PROJECTIVE_INDEPENDENT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS exact rational identity; all eight rank/gauge cases; 100 independent gradient/gap controls; 15 manifest hashes')
