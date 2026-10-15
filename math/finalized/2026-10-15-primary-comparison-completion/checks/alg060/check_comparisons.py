"""Fresh exact algebra controls. No imported research code; not a production executor."""
import json
from fractions import Fraction as Q
from pathlib import Path

def eye(n): return [[Q(i==j) for j in range(n)] for i in range(n)]
def mul(A,B): return [[sum(a*b for a,b in zip(row,col)) for col in zip(*B)] for row in A]
def inv(A):
 n=len(A);M=[list(map(Q,A[i]))+eye(n)[i] for i in range(n)]
 for j in range(n):
  k=next(i for i in range(j,n) if M[i][j]);M[j],M[k]=M[k],M[j]
  d=M[j][j];M[j]=[v/d for v in M[j]]
  for i in range(n):
   if i!=j:
    d=M[i][j];M[i]=[a-d*b for a,b in zip(M[i],M[j])]
 return [r[n:] for r in M]
def rank(A,p=None):
 if not A:return 0
 M=[list(map(Q,row)) if p is None else [int(v)%p for v in row] for row in A];n=len(M);m=len(M[0]);r=0
 for j in range(m):
  k=next((i for i in range(r,n) if M[i][j]),None)
  if k is None: continue
  M[r],M[k]=M[k],M[r];d=M[r][j];d=1/d if p is None else pow(d,-1,p)
  M[r]=[v*d if p is None else v*d%p for v in M[r]]
  for i in range(n):
   if i!=r:
    d=M[i][j];M[i]=[a-d*b if p is None else (a-d*b)%p for a,b in zip(M[i],M[r])]
  r+=1
  if r==n: break
 return r
def sub(A,I,J):return [[A[i][j] for j in J]for i in I]
def colsp(A):return max(sum(v!=0 for v in col)for col in zip(*A))
res={'scope':'Exact local algebra controls only; no external theorem reproof or production certificate','dense_quasiseparable':[],'cyclic_green':[],'fixed_line_permutation':[],'fourier_displacement':[]}
for n in range(2,11):
 A=[[Q(1+(i==j))for j in range(n)]for i in range(n)];B=inv(A)
 assert colsp(A)==colsp(B)==n
 for k in range(1,n):
  for M in [A,B]:
   assert rank(sub(M,range(k),range(k,n)))==rank(sub(M,range(k,n),range(k)))==1
 res['dense_quasiseparable'].append({'N':n,'cut_rank':1,'inverse_column_support':n})
 A=eye(n)
 for j in range(n):A[(j+1)%n][j]-=2
 G=inv(A)
 assert colsp(A)==2 and colsp(G)==n
 for k in range(1,n):
  assert rank(sub(G,range(k),range(k,n)))==rank(sub(G,range(k,n),range(k)))==1
  assert rank(sub(G,range(k,n),range(k+1)))==1
 res['cyclic_green'].append({'N':n,'alpha':2,'inverse_column_support':2,'column_support':n,'strict_cut_ranks':1})
for n in [4,6,8,10,12]:
 k=n//2;P=[[Q(j==(i+k)%n)for j in range(n)]for i in range(n)]
 assert colsp(P)==1 and rank(sub(P,range(k),range(k,n)))==k
 res['fixed_line_permutation'].append({'N':n,'column_support':1,'middle_cut_rank':k,'line_border_edges':1})
for n,p,w in [(2,5,4),(3,7,2),(4,5,2),(5,11,3),(6,7,3),(7,29,16),(8,17,2)]:
 assert pow(w,n,p)==1 and all(pow(w,d,p)!=1 for d in range(1,n))
 F=[[pow(w,i*j,p)for j in range(n)]for i in range(n)]
 E=[[(pow(w,i,p)*F[i][j]-(F[i][j+1]if j+1<n else 0))%p for j in range(n)]for i in range(n)]
 assert E==[[int(j==n-1)for j in range(n)]for i in range(n)] and rank(E,p)==1
 Finv=[[pow(n,-1,p)*pow(w,(-i*j)%n,p)%p for j in range(n)]for i in range(n)]
 assert [[v%p for v in row]for row in mul(F,Finv)]==eye(n)
 assert colsp(Finv)==n
 res['fourier_displacement'].append({'N':n,'prime':p,'root':w,'sylvester_rank':1,'inverse_column_support':n,'dense_endpoint_cancelled':True})
# Conditional one-layer lift: B has column support two, D has rank one,
# H=(B+D)^-1, G=B^-1; G itself is dense and that is permitted.
res['conditional_sparse_lift']=[]
for n in range(2,11):
 B=eye(n)
 for j in range(n):B[(j+1)%n][j]-=2
 D=[[Q(1)for j in range(n)]for i in range(n)]
 A=[[B[i][j]+D[i][j]for j in range(n)]for i in range(n)]
 H=inv(A);G=inv(B);R=[[H[i][j]-G[i][j]for j in range(n)]for i in range(n)]
 rhs=[[-v for v in row]for row in mul(mul(H,D),G)]
 assert R==rhs and rank(R)==rank(D)==1
 assert inv(G)==B and colsp(inv(G))==2 and colsp(G)==n
 res['conditional_sparse_lift'].append({'N':n,'rank_D':1,'rank_R':1,'column_support_B':2,'column_support_G':n,'inverse_G_support':2})
# Ax takes the kernel of A_(H,K) into the inverse cut kernel; A^-1 reverses it.
A=[[Q(1),Q(1),Q(1)],[Q(0),Q(2),Q(0)],[Q(0),Q(0),Q(3)]]
Ai=inv(A);x=[[Q(0)],[Q(1)],[Q(-1)]];z=mul(A,x)
assert z==[[Q(0)],[Q(2)],[Q(-3)]] and mul(Ai,z)==x
assert mul(sub(A,[0],[1,2]),x[1:])==[[0]]
assert mul(sub(Ai,[0],[1,2]),z[1:])==[[0]]
res['cut_kernel_direction']={'cases':1,'A_times_x':[0,2,-3],'inverse_returns_x':[0,1,-1],'both_cut_kernels_verified':True}
path=Path(__file__).with_name('CONTROL_RESULTS.json');path.write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps({'verdict':'PASS','dense_quasiseparable':len(res['dense_quasiseparable']),'cyclic_green':len(res['cyclic_green']),'fixed_line_permutation':len(res['fixed_line_permutation']),'fourier_displacement':len(res['fourier_displacement']),'conditional_sparse_lift':len(res['conditional_sparse_lift']),'cut_kernel_direction':res['cut_kernel_direction']['cases']}))
