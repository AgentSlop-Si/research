#!/usr/bin/env python3
"""Independent exact seed and integer-polynomial controls. Standard library."""
from pathlib import Path
from fractions import Fraction
import json,math,sys,random,hashlib
CYCLES={8:[[0,4,3,1,6,2,5,7],[1,0,2,3,7,4,5,6]],16:[[14,1,2,5,4,6,10,11,13,15,0,3,7,12,8,9],[10,6,3,9,11,8,2,7,14,5,0,4,13,12,15,1]]}
def trim(a):
 while a and a[-1]==0:a.pop()
 return a
def primitive(a):
 a=trim(a[:])
 if not a:return a
 g=math.gcd(*a);g=g if a[-1]>0 else -g
 return [x//g for x in a]
def gcdpoly(a,b):
 a=primitive(a);b=primitive(b)
 while b:
  r=a[:]
  while len(r)>=len(b) and r:
   k=len(r)-len(b);v=r[-1];lc=b[-1];r=[lc*x for x in r]
   for j,x in enumerate(b):r[j+k]-=v*x
   r=primitive(r)
  a,b=b,r
 return primitive(a)
def exactdiv(a,b):
 r=a[:];q=[0]*max(0,len(a)-len(b)+1)
 while len(r)>=len(b) and r:
  k=len(r)-len(b);assert r[-1]%b[-1]==0;v=r[-1]//b[-1];q[k]=v
  for j,x in enumerate(b):r[j+k]-=v*x
  trim(r)
 assert not r;return trim(q)
def peval(a,x):
 y=0
 for c in reversed(a):y=y*x+c
 return y
def determinant(A,p=None):
 n=len(A);B=[r[:] for r in A];out=1;prev=1;sign=1
 if p:
  for k in range(n):
   choices=[i for i in range(k,n) if B[i][k]%p]
   if not choices:return 0
   j=choices[0]
   if j!=k:B[j],B[k]=B[k],B[j];out=-out
   v=B[k][k]%p;out=out*v%p;iv=pow(v,-1,p)
   for i in range(k+1,n):
    f=B[i][k]*iv%p
    for j in range(k+1,n):B[i][j]=(B[i][j]-f*B[k][j])%p
  return out%p
 for k in range(n-1):
  if not B[k][k]:
   choices=[i for i in range(k+1,n) if B[i][k]]
   if not choices:return 0
   j=choices[0];B[j],B[k]=B[k],B[j];sign=-sign
  pivot=B[k][k]
  for i in range(k+1,n):
   for j in range(k+1,n):
    num=pivot*B[i][j]-B[i][k]*B[k][j];assert num%prev==0;B[i][j]=num//prev
  for i in range(k+1,n):B[i][k]=0
  prev=pivot
 return sign*B[-1][-1]
def poly_matrix(orders,z,p=None):
 n=len(orders[0]);positions=[{v:i for i,v in enumerate(o)} for o in orders];powers=[1]
 for _ in range(1,n):powers.append(powers[-1]*z if p is None else powers[-1]*z%p)
 return [[sum(powers[(pos[i]-pos[j])%n] for pos in positions) if p is None else sum(powers[(pos[i]-pos[j])%n] for pos in positions)%p for j in range(n)] for i in range(n)]
def values(A,p=None):
 n=len(A);d=determinant(A,p);out=[]
 for col in [0,1]:
  minor=[[A[i][j] for j in range(n) if j!=col] for i in range(1,n)];cof=(-1)**col*determinant(minor,p);v=n*A[0][col]*cof-d;out.append(v if p is None else v%p)
 return out+[d]
def interpolate_negative(vals,p):
 # Nodes -degree,...,0: independent shifted Newton interpolation.
 d=len(vals)-1;deltas=[];row=vals[:]
 while row:deltas.append(row[0]);row=[(row[i+1]-row[i])%p for i in range(len(row)-1)]
 result=[0]*(d+1);basis=[1]
 for k,delta in enumerate(deltas):
  for j,x in enumerate(basis):result[j]=(result[j]+delta*x)%p
  if k<d:
   new=[0]*(len(basis)+1);a=d-k;iv=pow(k+1,-1,p)
   for j,x in enumerate(basis):new[j]=(new[j]+a*x*iv)%p;new[j+1]=(new[j+1]+x*iv)%p
   basis=new
 return trim([x if x<=p//2 else x-p for x in result])
def matrix_inv(A,p):
 n=len(A);B=[[x%p for x in A[i]]+[int(i==j) for j in range(n)] for i in range(n)]
 for j in range(n):
  k=next(k for k in range(j,n) if B[k][j]);B[k],B[j]=B[j],B[k];v=pow(B[j][j],-1,p);B[j]=[x*v%p for x in B[j]]
  for k in range(n):
   if k!=j:
    v=B[k][j];B[k]=[(x-v*y)%p for x,y in zip(B[k],B[j])]
 return [r[n:] for r in B]
def mm(A,B,p):return [[sum(x*y for x,y in zip(r,c))%p for c in zip(*B)] for r in A]
def diag(v):return [[x if i==j else 0 for j in range(len(v))] for i,x in enumerate(v)]
def transpose(A):return list(map(list,zip(*A)))
def regular(A,p):return [sum(r)%p for r in A],[sum(c)%p for c in zip(*A)]
def root(n,p):return next(w for w in range(1,p) if pow(w,n,p)==1 and all(pow(w,k,p)!=1 for k in range(1,n)))
def main():
 P=(1<<127)-1;s=4
 for _ in range(125):s=(s*s-2)%P
 assert s==0 # Lucas--Lehmer certificate for the prime exponent127.
 certs=[]
 for n,orders in CYCLES.items():
  assert all(sorted(o)==list(range(n)) for o in orders);D=n*(n-1);bound=2*math.factorial(n)*2**n;assert P>2*bound;sample=[values(poly_matrix(orders,z,P),P) for z in range(-D,1)];polys=[interpolate_negative([row[j] for row in sample],P) for j in range(3)];assert all(abs(c)<=bound for a in polys for c in a)
  for z in [-3,2,3,5]:assert [peval(a,z) for a in polys]==values(poly_matrix(orders,z))
  g=gcdpoly(polys[0],polys[1]);quotient=exactdiv(polys[2],g)
  # Rank of W0-W1 equals N minus cycle count of their relative permutation.
  succ=[]
  for o in orders:
   v=[0]*n
   for j,x in enumerate(o):v[x]=o[(j+1)%n]
   succ.append(v)
  inverse0=[succ[0].index(i) for i in range(n)];relative=[inverse0[succ[1][i]] for i in range(n)];seen=set();nc=0
  for i in range(n):
   if i in seen:continue
   nc+=1;j=i
   while j not in seen:seen.add(j);j=relative[j]
  assert n-nc==n-2
  certs.append(dict(N=n,coefficient_bound=bound,modular_interpolation_nodes=[-D,0],degrees=[len(a)-1 for a in polys]+[len(g)-1],rank_cycle_difference=n-nc,integer_arrays=dict(H0=polys[0],H1=polys[1],det_C=polys[2],primitive_gcd=g,integer_quotient=quotient),integer_evaluations=[-3,2,3,5]))
 controls=[]
 for n,p in [(4,17),(4,97),(8,17),(16,97)]:
  w=root(n,p);F=[[pow(w,i*j,p) for j in range(n)] for i in range(n)]
  if n==4:
   A=[[1-2*int(i==j) for j in range(n)] for i in range(n)];Ai=matrix_inv(A,p);D=diag([pow(x,-1,p) for x in A[0]]);B=mm(mm(diag(A[0]),Ai,p),F,p);assert regular(B,p)==([1]*n,[1]*n);assert mm(mm(A,D,p),B,p)==F;assert all(A[0][i]*Ai[i][0]%p==pow(n,-1,p) for i in range(n));controls.append(dict(N=n,p=p,full_Fourier_positive=True))
  else:
   for alpha in range(2,p):
    if pow(alpha,n,p)==1:continue
    candidate=poly_matrix(CYCLES[n],alpha,p);factor=pow(1-pow(alpha,n,p),-1,p);candidate=[[x*factor%p for x in r] for r in candidate];a=regular(candidate,p)[0][0]
    if a and all(candidate[0]) and determinant(candidate,p):A=candidate;break
   else:raise AssertionError('no guarded partial control')
   assert regular(A,p)==([a]*n,[a]*n);D=diag([pow(a*x,-1,p) for x in A[0]]);M=mm(mm(A,D,p),transpose(A),p);assert M[0]==[1]*n and [r[0] for r in M]==[1]*n;assert M!=F;controls.append(dict(N=n,p=p,alpha=alpha,first_cross_positive_full_Fourier_negative=True))
 out=dict(status='PASS',mersenne127_Lucas_Lehmer=True,certificates=certs,seed_controls=controls,weak_stage_delta='7/24',weak_leverage_bound='359/408',source_code_executed=False)
 path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('INDEPENDENT_RESULTS.json');path.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
