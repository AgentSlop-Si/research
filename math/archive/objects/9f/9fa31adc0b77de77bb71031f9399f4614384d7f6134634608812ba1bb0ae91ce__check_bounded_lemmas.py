"""Fresh reviewer checks; no source program is imported or executed."""
from fractions import Fraction as Q
from itertools import combinations, product
from math import comb, exp
from decimal import Decimal, localcontext
import json

def rank(A,p):
 A=[r[:] for r in A];m=len(A);n=len(A[0]) if m else 0;k=0
 for j in range(n):
  u=next((i for i in range(k,m) if A[i][j]%p),None)
  if u is None:continue
  A[k],A[u]=A[u],A[k];z=pow(A[k][j],-1,p);A[k]=[v*z%p for v in A[k]]
  for i in range(k+1,m):
   z=A[i][j];A[i]=[(x-z*y)%p for x,y in zip(A[i],A[k])]
  k+=1
  if k==m:break
 return k

def displacement():
 cases=entries=0
 for N,p in [(5,11),(7,29),(11,23)]:
  w=next(a for a in range(2,p) if pow(a,N,p)==1 and a!=1)
  roots=[pow(w,j,p) for j in range(1,N)]
  for mask in range(1,1<<(N-1)):
   nodes=[roots[j] for j in range(N-1) if mask>>j&1]
   for B in range(1,N):
    V=[[pow(z,r,p) for z in nodes] for r in range(B)]
    for t in range(1,B+1):
     R=[[(V[r][j]*pow(z,t,p)-V[(r+t)%B][j])%p for j,z in enumerate(nodes)] for r in range(B)]
     E=[[0 if r+t<B else (pow(z,B,p)-1)*pow(z,r+t-B,p)%p for z in nodes] for r in range(B)]
     assert R==E and rank(R,p)==min(t,len(nodes));cases+=1;entries+=B*len(nodes)
 # Include resonant columns, t=B, and rectangular matrices over a distinct field.
 resonant=0
 for p in (13,17):
  for B in range(1,9):
   nodes=list(range(1,p))
   for t in range(1,B+1):
    R=[[(pow(z,r+t,p)-pow(z,(r+t)%B,p))%p for z in nodes] for r in range(B)]
    assert rank(R,p)==min(t,sum(pow(z,B,p)!=1 for z in nodes));resonant+=1
 return dict(prime_subset_cases=cases,entries=entries,resonant_cases=resonant)

def other():
 center=0
 for h in range(3,11):
  triples=list(combinations(range(h),3))
  for S in triples:
   for T in triples:
    coefficient=sum(Q(1,2) for j in S if j in T)-Q(len(T),6)
    assert coefficient==Q(len(set(S)&set(T))-1,2);center+=1
 h=24;v=comb(h,3);N0=v**3;I0=3*v*v;dn=comb(h-3,3)+3*(h-3)
 W=2*N0+I0*(v*dn+h);delta=2*N0-2*I0*h*h;m=h**3
 assert (v,W,delta,m)==(2024,34666930287616,2425172992,13824)
 with localcontext() as ctx:
  ctx.prec=70;gap=-(1-Decimal(delta)/(Decimal(2)**45*m)).ln()/Decimal(m).ln()
  assert abs(gap-Decimal('5.2296989632709109282062267e-10'))<Decimal('1e-34')
 house=0
 for s in (2,3,4,5):
  n=s*s+1;H=[[Q(0) if i==j==0 else -Q(1,s) if (i==0)!=(j==0) else Q(i==j)-Q(1,s*s) for j in range(n)] for i in range(n)]
  for i in range(n):
   for j in range(n):assert sum(H[i][k]*H[k][j] for k in range(n))==int(i==j)
  norm=max(sum(abs(H[i][j]) for i in range(n)) for j in range(n));assert norm==s
  house+=1
 moments=0
 for k in range(1,17):
  vals=[(2*j-k,comb(k,j)) for j in range(k+1)]
  assert sum(s*s*c for s,c in vals)==k*2**k
  assert sum(s**4*c for s,c in vals)==(3*k*k-2*k)*2**k
  prob=Q(sum(c for s,c in vals if 2*s*s>=k),2**k);assert prob>=Q(1,12);moments+=1
 # Logical sign convention: S e_j=e_(j+1), F_ij=w^(ij).
 cov=0
 for n,p,w in [(4,17,4),(8,17,2),(16,97,8)]:
  F=[[pow(w,i*j,p) for j in range(n)] for i in range(n)]
  assert all(F[i][(j+1)%n]==pow(w,i,p)*F[i][j]%p for i in range(n) for j in range(n))
  reconstructed=[[pow(w,i*j,p) for j in range(n)] for i in range(n)]
  assert reconstructed==F;cov+=1
 return dict(reduced_center_coefficients=center,wire_count=W,delta=delta,exponent_gap=str(gap),householder_exact_cases=house,rademacher_moment_cases=moments,covariance_controls=cov,union_hoeffding_256_1024=256*exp(-1024/18))
if __name__=='__main__':
 d={'status':'PASS','displacement':displacement(),'other':other(),'scope':'Only stated bounded algebraic lemmas. No uploaded test suite or benchmark executed; no entire network or decoder certification.'}
 print(json.dumps(d,sort_keys=True,indent=2));open('BOUNDED_LEMMA_RESULTS.json','w').write(json.dumps(d,sort_keys=True,indent=2)+'\n')
