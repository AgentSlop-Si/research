"""Reviewer-created finite-field controls; no source implementation imports."""
import itertools,collections,json,csv
from pathlib import Path
import numpy as np
HERE=Path(__file__).parent
rng=np.random.default_rng(2421700)
def rank(A,p):
 A=np.asarray(A,dtype=np.int64).copy()%p;r=0
 for c in range(A.shape[1]):
  pp=np.flatnonzero(A[r:,c])
  if not len(pp):continue
  k=r+int(pp[0]);A[[r,k]]=A[[k,r]];A[r]=A[r]*pow(int(A[r,c]),-1,p)%p
  for i in range(r+1,A.shape[0]):A[i]=(A[i]-A[i,c]*A[r])%p
  r+=1
  if r==A.shape[0]:break
 return r
def inv(A,p):
 n=len(A);M=np.concatenate([A.copy()%p,np.eye(n,dtype=np.int64)],axis=1)
 for j in range(n):
  k=next(k for k in range(j,n) if M[k,j]);M[[k,j]]=M[[j,k]];M[j]=M[j]*pow(int(M[j,j]),-1,p)%p
  for i in range(n):
   if i!=j:M[i]=(M[i]-M[i,j]*M[j])%p
 return M[:,n:]
def root_of_order(q,p,ell):
 return next(z for z in range(2,ell) if pow(z,q,ell)==1 and pow(z,q//p,ell)!=1)
# Enumerate every symplectic basis rather than replaying the absent source BFS.
p=3;V=list(itertools.product(range(p),repeat=4));zero=(0,0,0,0)
def pair(a,b):return (a[0]*b[2]+a[1]*b[3]-a[2]*b[0]-a[3]*b[1])%3
count=collections.Counter()
for a in V:
 if a==zero:continue
 for b in V:
  if pair(a,b)!=1:continue
  perp=[x for x in V if pair(a,x)==pair(b,x)==0]
  assert len(perp)==9
  for c in perp:
   if c==zero:continue
   for d in perp:
    if pair(c,d)==1:
     # Columns (a,c,b,d); top-right block columns are b,d.
     x,y,z,t=b[0],d[0],b[1],d[1]
     r=2 if (x*t-y*z)%3 else int(any([x,y,z,t]));count[r]+=1
assert count=={0:1296,1:15552,2:34992}
controls=[]
for p,n,ell in [(3,2,19),(3,3,109),(5,2,101)]:
 N=p**n;zeta=root_of_order(N,p,ell);omega=pow(zeta,N//p,ell);vs=np.array(list(itertools.product(range(p),repeat=n)),dtype=np.int64);lookup={tuple(x):i for i,x in enumerate(vs)}
 J=np.block([[np.zeros((n,n),dtype=np.int64),np.eye(n,dtype=np.int64)],[-np.eye(n,dtype=np.int64),np.zeros((n,n),dtype=np.int64)]])%p
 tensor=np.array([[pow(omega,int(x@y)%p,ell) for y in vs] for x in vs],dtype=np.int64)
 def generator(kind):
  S=np.eye(2*n,dtype=np.int64)
  if kind==0:
   h=int(rng.integers(n));S[h,h]=S[n+h,n+h]=0;S[h,n+h]=p-1;S[n+h,h]=1
   U=np.zeros((N,N),dtype=np.int64)
   for i,x in enumerate(vs):
    for j,y in enumerate(vs):
     if all(x[k]==y[k] for k in range(n) if k!=h):U[i,j]=pow(omega,int(x[h]*y[h]),ell)
  elif kind==1:
   R=rng.integers(p,size=(n,n));R=(R+R.T)%p;S[n:,:n]=R
   U=np.diag([pow(omega,int(x@R@x)*pow(2,-1,p)%p,ell) for x in vs]).astype(np.int64)
  else:
   while True:
    L=rng.integers(p,size=(n,n))
    if rank(L,p)==n:break
   S[:n,:n]=L;S[n:,n:]=inv(L,p).T
   U=np.zeros((N,N),dtype=np.int64)
   for j,y in enumerate(vs):U[lookup[tuple(L@y%p)],j]=1
  assert np.array_equal(S.T@J@S%p,J)
  return S,U
 dense=0;crosschecks=0;subadd=0
 for trial in range(100):
  S=np.eye(2*n,dtype=np.int64);U=np.eye(N,dtype=np.int64)
  for _ in range(int(rng.integers(1,10))):
   T,W=generator(int(rng.integers(3)));r0=rank(S[:n,n:],p);r1=rank(T[:n,n:],p);S=T@S%p;U=W@U%ell
   assert rank(S[:n,n:],p)<=r0+r1;subadd+=1
  r=rank(S[:n,n:],p);assert set(np.count_nonzero(U,axis=0))==set(np.count_nonzero(U,axis=1))=={p**r}
  if r==n:
   dense+=1
   for _ in range(40):
    i,j,k,l=map(int,rng.integers(N,size=4));cr=int(U[i,k])*int(U[j,l])*pow(int(U[i,l])*int(U[j,k])%ell,-1,ell)%ell
    assert pow(cr,p,ell)==1;crosschecks+=1
 # Every coordinate Fourier generator once gives exact tensor kernel, no scalar ambiguity here.
 U=np.eye(N,dtype=np.int64)
 for h in range(n):
  W=np.zeros((N,N),dtype=np.int64)
  for i,x in enumerate(vs):
   for j,y in enumerate(vs):
    if all(x[k]==y[k] for k in range(n) if k!=h):W[i,j]=pow(omega,int(x[h]*y[h]),ell)
  U=W@U%ell
 assert np.array_equal(U,tensor)
 # Bilinear kernel x^T M y is column relabeling y -> M y.
 for _ in range(20):
  while True:
   M=rng.integers(p,size=(n,n))
   if rank(M,p)==n:break
  perm=[lookup[tuple(M@y%p)] for y in vs]
  bilinear=np.array([[pow(omega,int(x@M@y)%p,ell) for y in vs] for x in vs],dtype=np.int64)
  assert np.array_equal(bilinear,tensor[:,perm])
 # Cyclic rows/columns 0,1 have cross ratio zeta, order exactly p^n.
 assert pow(zeta,N,ell)==1 and pow(zeta,N//p,ell)!=1 and pow(zeta,p,ell)!=1
 controls.append(dict(p=p,n=n,N=N,coefficient_prime=ell,primitive_cyclic_root=zeta,words=100,dense_words=dense,cross_ratio_checks=crosschecks,rank_subadditivity_checks=subadd,bilinear_relabelings=20,cyclic_cross_ratio_order=N))
ledger=list(csv.DictReader((HERE/'tensor_source/OPERATION_LEDGER.csv').open()))
for row in ledger:
 p,n,N,r,s,c,w=[int(row[k]) for k in ['p','n','dimension','partial_rank','row_nonzeros','dense_terms','writes']]
 assert N==p**n and s==p**r and c==r*p*N and w==r*N
out=dict(status='PASS',source_programs_executed=False,sp4_3_group_size=sum(count.values()),sp4_3_rank_B_distribution=dict(count),word_controls=controls,operation_ledger_rows=len(ledger),main_source_acceptance='dependency-pending',scope='Odd prime p, supplied primitive roots, exact coefficient fields; core ledger only')
(HERE/'TENSOR_INDEPENDENT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
