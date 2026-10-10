"""Fresh exact controls for the closed augmented-minor condition, including masked endpoints."""
import importlib.util,json,itertools
from pathlib import Path
sp=importlib.util.spec_from_file_location('own_gate',str(Path(__file__).with_name('_projective_gate_helpers.py')));h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h);h.p=241;p=241

def rank(A):
 M=[row[:]for row in A];r=0
 for j in range(len(M[0])):
  k=next((k for k in range(r,len(M))if M[k][j]),None)
  if k is None:continue
  M[r],M[k]=M[k],M[r];v=pow(M[r][j],-1,p);M[r]=[x*v%p for x in M[r]]
  for k in range(r+1,len(M)):
   v=M[k][j];M[k]=[(a-v*b)%p for a,b in zip(M[k],M[r])]
  r+=1
  if r==len(M):break
 return r

def det(A):
 M=[row[:]for row in A];d=1
 for j in range(len(M)):
  k=next((k for k in range(j,len(M))if M[k][j]),None)
  if k is None:return 0
  if k!=j:M[j],M[k]=M[k],M[j];d=-d%p
  v=M[j][j];d=d*v%p;iv=pow(v,-1,p);M[j]=[x*iv%p for x in M[j]]
  for k in range(j+1,len(M)):
   v=M[k][j];M[k]=[(a-v*b)%p for a,b in zip(M[k],M[j])]
 return d

def limit_direction(a,b,c):
 # Pair [a(epsilon), c*b(epsilon)], replacing zero a/b by epsilon.
 terms=[(0,a)if a else(1,1),(0,c*b%p)if b else(1,c%p)]
 valuation=min(e for e,z in terms if z)
 return h.canon([z if e==valuation else 0 for e,z in terms])

def augmented(B,U,V):
 n=len(B);K=h.mul(U,h.mul(B,V));rows=[]
 for i in range(n):
  for j in range(n):
   rr=[0]*(2*n);rr[i]=V[i][j];rr[n+j]=U[i][j];rows.append(rr+[K[i][j]])
 return rows

cases=[];n=5;pi=[1,2,3,4,0];tau=[2,0,3,4,1];ti=h.pinv(tau)
for zeros in(False,True):
 for mask in('none','left0','right1','both'):
  w0=[2]*n;w1=[3]*n
  if zeros:w0[1]=0;w1[3]=0
  l0=[i+1 for i in range(n)];r0=[i+2 for i in range(n)];l1=[i+3 for i in range(n)];r1=[i+4 for i in range(n)]
  if mask in('left0','both'):l0[1]=0;l0[4]=0
  if mask in('right1','both'):r1[0]=0;r1[3]=0
  if mask=='both':r0[2]=0;l1[2]=0
  G0=h.inv(h.sub(h.eye(n),h.mul(h.diag(w0),h.perm(pi))));G1=h.inv(h.sub(h.eye(n),h.mul(h.diag(w1),h.perm(tau))))
  T0=h.mul(h.diag(l0),h.mul(G0,h.diag(r0)));T1=h.mul(h.diag(l1),h.mul(G1,h.diag(r1)));B=h.add(T0,T1)
  U=[[0]*n for i in range(n)];V=[[0]*n for i in range(n)]
  for i in range(n):U[i][i],U[i][pi[i]]=limit_direction(l0[pi[i]],l0[i],-w0[i])
  for j in range(n):V[j][j],V[ti[j]][j]=limit_direction(r1[ti[j]],r1[j],-w1[ti[j]])
  K=h.mul(U,h.mul(B,V));assert all(K[i][j]==0 for i in range(n)for j in range(n)if j not in(i,pi[i],tau[i]))
  rr=rank(augmented(B,U,V));assert rr<=10
  cases.append(dict(N=n,zero_edges=zeros,endpoint_mask=mask,augmented_rank=rr))
# The actual N3 chirp-B positive control, using its explicit Green inverse directions.
n=3;omega=15;t=207;kappa=2;Dinv=h.diag([pow(15,-1,p),1,1]);P=h.perm([1,2,0]);Pi=h.perm([2,0,1]);B=h.target(n,omega)
U=h.scale(pow(kappa,-1,p),h.mul(Dinv,h.mul(h.sub(h.eye(n),h.scale(t,P)),Dinv)))
V=h.scale(pow(kappa,-1,p),h.mul(Dinv,h.mul(h.sub(h.eye(n),h.scale(t,Pi)),Dinv)))
assert h.add(h.inv(U),h.inv(V))==B
AA=augmented(B,U,V);rr=rank(AA);assert rr<=6
minor_count=0
for rows in itertools.combinations(range(9),7):assert det([AA[i]for i in rows])==0;minor_count+=1
result=dict(status='PASS',genuine_N5_controls=cases,singular_endpoint_controls=sum(x['endpoint_mask']!='none'for x in cases),zero_edge_controls=sum(x['zero_edges']for x in cases),N3_actual_chirp_positive_augmented_rank=rr,N3_all_7_by_7_minors_checked=minor_count)
Path(__file__).with_name('MINOR_POSITIVE_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
