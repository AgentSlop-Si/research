"""Independent audit written for this review; does not execute/import archive code."""
import hashlib,json,random
from pathlib import Path
P=998244353
G=3

def eye(n): return [[int(i==j) for j in range(n)] for i in range(n)]
def mul(A,B,p=P):
 return [[sum(a*b for a,b in zip(row,col))%p for col in zip(*B)] for row in A]
def inv(A,p=P):
 n=len(A);W=[[(v%p) for v in row]+idrow for row,idrow in zip(A,eye(n))]
 for j in range(n):
  k=next((i for i in range(j,n) if W[i][j]),None)
  if k is None:raise ArithmeticError('singular')
  W[j],W[k]=W[k],W[j]
  c=pow(W[j][j],-1,p);W[j]=[c*x%p for x in W[j]]
  for i in range(n):
   if i!=j:
    c=W[i][j];W[i]=[(x-c*y)%p for x,y in zip(W[i],W[j])]
 return [r[n:] for r in W]
def rank(A,p=P):
 if not A:return 0
 W=[r[:] for r in A];r=0
 for j in range(len(W[0])):
  k=next((i for i in range(r,len(W)) if W[i][j]%p),None)
  if k is None:continue
  W[r],W[k]=W[k],W[r]
  c=pow(W[r][j]%p,-1,p);W[r]=[c*x%p for x in W[r]]
  for i in range(r+1,len(W)):
   c=W[i][j];W[i]=[(x-c*y)%p for x,y in zip(W[i],W[r])]
  r+=1
  if r==len(W):break
 return r

def scan_matrix(a,up=False,p=P):
 n=len(a);M=eye(n)
 for i in (range(n-2,-1,-1) if up else range(1,n)):
  prev=i+1 if up else i-1
  M[i]=[(x+a[i]*y)%p for x,y in zip(M[i],M[prev])]
 return M

def independent_fft(x,p=P,g=G):
 n=len(x);L=n.bit_length()-1
 # Iterative bit reversal without strings.
 order=[]
 for i in range(n):
  rev=0;k=i
  for _ in range(L):rev=2*rev+k%2;k//=2
  order.append(rev)
 y=[x[j] for j in order]
 root=pow(g,(p-1)//n,p);half_inv=pow(2,-1,p)
 for ell in range(1,L+1):
  m=1<<ell;h=m//2
  q=[v for start in range(0,n,m) for j in range(h) for v in (start+j,start+j+h)]
  z=[y[i] for i in q]
  for k in range(n//2):z[2*k+1]=(-2*pow(root,(k%h)*n//m,p)*z[2*k+1])%p
  b=z[:]
  for i in range(n-1,-1,-1):
   if i%2==0:b[i]=(z[i]-half_inv*b[i+1])%p
  f=b[:]
  for i in range(n):
   if i%2:f[i]=(b[i]+f[i-1])%p
  for k,i in enumerate(q):y[i]=f[k]
 return y

out={}
r=Path('latest_scan_audit/input/fft_interleaved_scan_barrier')
out['archive_hashes']={}
for line in (r/'SHA256SUMS.txt').read_text().splitlines():
 digest,name=line.split(maxsplit=1)
 out['archive_hashes'][name]=(hashlib.sha256((r/name).read_bytes()).hexdigest()==digest)
assert all(out['archive_hashes'].values())
out['two_scan_basis_counts']={}
for p,g in [(998244353,3),(2013265921,31)]:
 count=0
 for n in [2,4,8,16,32,64,128]:
  w=pow(g,(p-1)//n,p)
  for j in range(n):
   y=independent_fft([int(i==j) for i in range(n)],p,g)
   assert y==[pow(w,j*k,p) for k in range(n)]
   count+=1
 out['two_scan_basis_counts'][str(p)]=count
out['bidirectional_sum']=[]
for n in [4,8,16,32,64]:
 A=scan_matrix([0]+[j+2 for j in range(1,n)])
 B=scan_matrix([j+3 for j in range(n-1)]+[0],True)
 H=[[(x+y)%P for x,y in zip(a,b)] for a,b in zip(A,B)]
 Hinv=inv(H)
 nnz=sum(v!=0 for row in Hinv for v in row)
 residual=[[(Hinv[i][j] if i!=j else 0) for j in range(n)] for i in range(n)]
 assert mul(H,Hinv)==eye(n)
 out['bidirectional_sum'].append({'N':n,'inverse_nnz':nnz,'own_diagonal_residual_rank':rank(residual),'identity_residual_rank':rank([[(Hinv[i][j]-int(i==j))%P for j in range(n)] for i in range(n)])})
 assert nnz==n*n
out['rank_one_counterexample']=[]
for n in [4,8,16,32]:
 H=[[1+int(i==j) for j in range(n)] for i in range(n)];Hinv=inv(H)
 own_diag_removed=[[Hinv[i][j] if i!=j else 0 for j in range(n)] for i in range(n)]
 I_removed=[[(Hinv[i][j]-int(i==j))%P for j in range(n)] for i in range(n)]
 assert rank(own_diag_removed)==n and rank(I_removed)==1
 out['rank_one_counterexample'].append({'N':n,'own_diagonal_residual_rank':rank(own_diag_removed),'identity_residual_rank':rank(I_removed)})
rng=random.Random(772619);checks=0
for p,g in [(998244353,3),(2013265921,31)]:
 for n in [4,8,16,32,64]:
  w=pow(g,(p-1)//n,p)
  for s in range(n):
   q=n//(s+1)
   if not q:continue
   supports=[set(rng.sample(range(n),s)) for _ in range(q)]
   covered=set().union(*supports)
   free=[j for j in range(n) if j not in covered][:q]
   assert len(free)==q
   V=[[pow(w,i*j,p) for j in free] for i in range(q)]
   assert rank(V,p)==q;checks+=1
out['independent_vandermonde_checks']=checks
# Exact combinatorial minimization of the stated tradeoff, not realizability.
out['pass_budget_lower_bounds']=[]
for L in range(1,17):
 n=2**L
 pairs=[(t,n//((1<<t)+1)) for t in range(L+2)]
 # If B=0, stronger boundary-row condition must hold.
 pairs=[(t,b) for t,b in pairs if b or t>=L+1]
 out['pass_budget_lower_bounds'].append({'N':n,'minimum_t_plus_B_allowed_by_combined_bounds':min(t+b for t,b in pairs)})
out['status']='PASS'
Path('latest_scan_audit/independent_check_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
