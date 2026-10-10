"""Independent second-audit controls. No research program loaded or executed.
Only the inert JSON parameter certificates named below are read.
"""
from pathlib import Path
from itertools import permutations
from math import gcd,isqrt
import json, random, hashlib
ROOT=Path('[local workspace]')
OUT=ROOT/'research_cycle_0958/matrix'

def eye(n): return [[int(i==j) for j in range(n)] for i in range(n)]
def add(a,b,p): return [[(x+y)%p for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def sub(a,b,p): return [[(x-y)%p for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def mul(a,b,p): return [[sum(x*y for x,y in zip(ar,bc))%p for bc in zip(*b)] for ar in a]
def inverse(a,p):
 n=len(a);t=[r[:]+e for r,e in zip(a,eye(n))]
 for k in range(n):
  s=next(i for i in range(k,n) if t[i][k]%p);t[k],t[s]=t[s],t[k]
  f=pow(t[k][k],-1,p);t[k]=[v*f%p for v in t[k]]
  for i in range(n):
   if i!=k:
    f=t[i][k];t[i]=[(x-f*y)%p for x,y in zip(t[i],t[k])]
 return [r[n:] for r in t]
def rank(a,p):
 if not a:return 0
 t=[r[:] for r in a];k=0
 for j in range(len(t[0])):
  s=next((i for i in range(k,len(t)) if t[i][j]%p),None)
  if s is None: continue
  t[k],t[s]=t[s],t[k];f=pow(t[k][j],-1,p);t[k]=[v*f%p for v in t[k]]
  for i in range(k+1,len(t)):
   f=t[i][j];t[i]=[(x-f*y)%p for x,y in zip(t[i],t[k])]
  k+=1
  if k==len(t):break
 return k

def determinant(a,p):
 t=[r[:] for r in a];d=1;n=len(t)
 for k in range(n):
  s=next((i for i in range(k,n) if t[i][k]%p),None)
  if s is None:return 0
  if s!=k:t[k],t[s]=t[s],t[k];d=-d
  v=t[k][k];d=d*v%p;f=pow(v,-1,p)
  for i in range(k+1,n):
   c=t[i][k]*f%p
   for j in range(k,n):t[i][j]=(t[i][j]-c*t[k][j])%p
 return d%p

def prime(n):return n>=2 and all(n%d for d in range(2,isqrt(n)+1))
def field(n):
 p=n+1
 while not prime(p):p+=n
 for x in range(2,p):
  w=pow(x,(p-1)//n,p)
  if pow(w,n,p)==1 and all(pow(w,n//d,p)!=1 for d in range(2,n+1) if n%d==0 and prime(d)):return p,w
 raise ValueError(n)

# Exact modular Hadamard-Segre witnesses, rebuilt from integer Green parameters.
src=ROOT/'novelty_catalogue_0825/library_delta_extracted/FFT_HADAMARD_SEGRE_EIGEN_GATE_2026-10-10/fft_hadamard_eigen_gate_20261010/CERTIFICATES.json'
results=[];branch_count=0
for c in json.loads(src.read_text()):
 n,p,w=c['N'],c['field'],c['root'];branches=[]
 assert pow(w,n,p)==1 and all(pow(w,d,p)!=1 for d in range(1,n))
 for b in c['branch_parameters']:
  cyc=b['cycle'];assert sorted(cyc)==list(range(n));seen={0};v=cyc[0]
  while v!=0:seen.add(v);v=cyc[v]
  assert len(seen)==n
  q=eye(n)
  for i in range(n):q[i][cyc[i]]=(q[i][cyc[i]]-b['weights'][i])%p
  g=inverse(q,p);g=[[b['left_diag'][i]*g[i][j]*b['right_diag'][j]%p for j in range(n)] for i in range(n)]
  g=[[g[b['row_permutation'][i]][b['col_permutation'][j]] for j in range(n)] for i in range(n)]
  branches.append(g);branch_count+=1
 A=add(branches[0],branches[1],p);B=add(branches[2],branches[3],p);C=eye(n) if len(branches)==4 else add(branches[4],branches[5],p)
 assert (A,B,C)==(c['A'],c['B'],c['C'])
 ai=inverse(A,p);ci=inverse(C,p);inverse(B,p)
 assert all(v%p for row in B for v in row)
 f=[[pow(w,i*j,p) for j in range(n)] for i in range(n)];h=mul(f,ci,p)
 ps=[[[ai[u][i]*h[i][j]*pow(B[u][j],-1,p)%p for i in range(n)] for u in range(n)] for j in range(3)]
 pi=inverse(ps[0],p);t1=mul(pi,ps[1],p);t2=mul(pi,ps[2],p);comm=sub(mul(t1,t2,p),mul(t2,t1,p),p)
 det=determinant(comm,p)
 assert det and det==c['det_commutator']
 assert (ps[0],t1,t2,comm)==(c['P0'],c['T1'],c['T2'],c['commutator'])
 results.append({'N':n,'two_stage':c['two_stage'],'det_mod97':det})

# Permutation extremizers, all N<=9. Direct matrix ranks sampled independently.
perms=0;direct=0;mins=[]
for n in range(1,10):
 p,w=field(n) if n>1 else (3,1)
 best=n;who=[]
 for perm in permutations(range(n)):
  seen=set();z=0
  for i in range(n):
   if i in seen:continue
   cyc=[];j=i
   while j not in seen:seen.add(j);cyc.append(j);j=perm[j]
   z+=sum(cyc)%n==0
  r=n-z;perms+=1
  if r<best:best=r;who=[perm]
  elif r==best:who.append(perm)
  if perms%499==0 or n<=4:
   a=[[int(i==j)*pow(w,i,p)-int(i==perm[j]) for j in range(n)] for i in range(n)]
   assert rank(a,p)==r;direct+=1
 assert best==n//2 and who==[tuple((-j)%n for j in range(n))]
 mins.append({'N':n,'rank':best,'minimizers':len(who)})

# Rotated Weyl Fourier coefficients derived by actual monomial actions.
rng=random.Random(1020958);weyl=[];coeffs=0
for n in [3,5,7,9,15,21,25,27,33,35,45]:
 p,w=field(n); inv4=pow(4,-1,n);inv2=pow(2,-1,n);gamma=sum(pow(w,t*t,p) for t in range(n))*pow(n,-1,p)%p
 for trial in range(7):
  while True:
   u,v,r,s=[rng.randrange(n) for _ in range(4)];D=(u*s-v*r)%n
   if gcd(D,n)==1:break
  powers=[]
  for shift,clock in [(u,v),(r,s)]:
   current=[(t,1) for t in range(n)];pp=[]
   for i in range(n):
    pp.append(current)
    current=[((idx+shift)%n,scale*pow(w,clock*idx,p)%p) for idx,scale in current]
   powers.append(pp)
  cc=[]
  for i in range(n):
   row=[]
   for j in range(n):
    total=0
    for t in range(n):
     idx,fac=powers[1][j][t];idx2,fac2=powers[0][i][idx]
     total+=pow(w,idx2*t,p)*pow(fac*fac2%p,-1,p)
    row.append(total*pow(n,-1,p)%p)
   cc.append(row)
  A=(u*u+v*v)%n;B=(r*r+s*s)%n;h=(u*r+v*s)%n;delta=(D-h)*inv2%n
  expected=[[gamma*pow(w,(-A*i*i*inv4+u*v*i*inv2-B*j*j*inv4+r*s*j*inv2+delta*i*j)%n,p)%p for j in range(n)] for i in range(n)]
  assert cc==expected;coeffs+=n*n
  dd=n//gcd(n,delta);da=n//gcd(n,A);db=n//gcd(n,B);m=(n+1)//2
  assert rank(cc,p)==dd
  assert rank([[cc[a+b][0] for b in range(m)] for a in range(m)],p)==min(m,da)
  assert rank([[cc[0][a+b] for b in range(m)] for a in range(m)],p)==min(m,db)
  bound=max(dd,min(m,da),min(m,db));assert bound*bound>=n
  weyl.append({'N':n,'directions':[u,v,r,s],'mixed_rank':dd,'row_hankel':min(m,da),'col_hankel':min(m,db),'branch_bound':bound})

output={'status':'PASS','hadamard_saved_witnesses':results,'hadamard_branches_reconstructed':branch_count,'hadamard_input_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'displacement_permutations':perms,'displacement_direct_ranks':direct,'displacement_minima':mins,'weyl_pairs':len(weyl),'weyl_coefficients_checked':coeffs,'weyl_results':weyl,'scope':'Independent fresh controls; no supplied program executed/imported/compiled/AST-parsed; source JSON used only as inert parameters.'}
(OUT/'fresh_check_results.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps({k:v for k,v in output.items() if k not in ['weyl_results']},indent=2))
