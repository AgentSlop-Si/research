#!/usr/bin/env python3
"""Independent M-step review. Standard library only; no source imports."""
import json,math,random
from pathlib import Path
def field(n):
 p=n+1
 while any(p%d==0 for d in range(2,math.isqrt(p)+1)):p+=n
 for w in range(2,p):
  if pow(w,n,p)==1 and pow(w,n//2,p)!=1:return p,w
 raise AssertionError
def poly_mul(a,b,p):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]=(c[i+j]+x*y)%p
 return c
def evalpoly(a,z,p):
 r=0
 for v in reversed(a):r=(r*z+v)%p
 return r
def ringmul(a,b,eta,p):
 m=len(a);out=[0]*m
 for i,x in enumerate(a):
  for j,y in enumerate(b):out[(i+j)%m]=(out[(i+j)%m]+x*y*(eta if i+j>=m else 1))%p
 return out
def shift(a,j,eta,p):
 m=len(a);out=[0]*m
 for u,v in enumerate(a):out[(u+j)%m]=v*pow(eta,(u+j)//m,p)%p
 return out
def grid_forward(A,w,p):
 m=len(A[0]);eta=pow(w,m,p);rho=pow(w,m//2,p);L=2*m
 # Horner evaluation in X first, lag second; independent direct transforms.
 out=[]
 for h in range(m):
  q=pow(w,1-m*h,p);coeff=[evalpoly(row,q,p) for row in A]
  out.append([evalpoly(coeff,pow(rho,ell,p),p) for ell in range(L)])
 return out
def grid_inverse(G,w,p):
 m=len(G);L=2*m;eta=pow(w,m,p);rho=pow(w,m//2,p)
 lag=[[sum(G[h][ell]*pow(rho,-ell*t,p) for ell in range(L))*pow(L,-1,p)%p for t in range(L)] for h in range(m)]
 return [[sum(lag[h][t]*pow(eta,h*u,p) for h in range(m))*pow(m,-1,p)*pow(w,-u,p)%p for u in range(m)] for t in range(L)]
def run():
 rng=random.Random(202610092211);out={'field_cases':[],'kernel_coefficient_identities':0,'doubling_identities':0,'full_2d_applications':0,'full_output_coefficients':0,'truncated_inversion_cases':0,'wrong_identity_counterexample':None}
 for m in [2,4,8,16,32]:
  p,w=field(m*m);eta=pow(w,m,p);rho=pow(w,m//2,p)
  # Build full P_M in the raw ring by multiplying the actual sparse factors.
  P=[[1]+[0]*(m-1)]
  for j in range(m):
   nxt=[row[:] for row in P]+[[0]*m]
   for t,row in enumerate(P):
    shifted=shift(row,j,eta,p)
    nxt[t+1]=[(a+b)%p for a,b in zip(nxt[t+1],shifted)]
   P=nxt
  PG=grid_forward(P,w,p);zeros=[]
  for h in range(m):
   q=pow(w,1-m*h,p);F=[1];T=[pow(q,s*(s-1)//2,p) for s in range(m+1)]
   for s in range(1,m+1):F.append(F[-1]*(1-pow(q,s,p))%p)
   assert all(F)
   ks=[T[s]*pow(F[s],-1,p)%p for s in range(m)]
   poly=[evalpoly(row,q,p) for row in P]
   for s in range(m+1):
    expected=T[s]*F[m]*pow(F[s],-1,p)*pow(F[m-s],-1,p)%p
    assert poly[s]==expected
    if s:assert (1-pow(q,s,p))*poly[s]%p==(pow(q,s-1,p)-eta)*poly[s-1]%p
    out['kernel_coefficient_identities']+=1
   for s in range(1,m):
    assert (1-pow(eta,s,p))*ks[s]%p==sum(poly[r]*pow(eta,s-r,p)*ks[s-r] for r in range(1,s+1))%p
   for r in [1<<i for i in range(m.bit_length()-1)]:
    a=[1]
    for j in range(r):a=poly_mul(a,[1,pow(q,j,p)],p)
    b=[v*pow(q,r*j,p)%p for j,v in enumerate(a)]
    c=[1]
    for j in range(2*r):c=poly_mul(c,[1,pow(q,j,p)],p)
    assert poly_mul(a,b,p)==c;out['doubling_identities']+=1
   idx=[ell for ell,val in enumerate(PG[h]) if val==0]
   expected=sorted([m,(m-1+m*h)%(2*m)])
   assert idx==expected;zeros.append(idx)
  assert sum(v!=0 for row in PG for v in row)==2*m*m-2*m
  for repeat in range(2):
   A=[[rng.randrange(p) for u in range(m)] for t in range(m)]
   expected=[[0]*m for t in range(2*m)]
   for t,row in enumerate(P):
    for j,col in enumerate(A):
     v=ringmul(row,col,eta,p);expected[t+j]=[(a+b)%p for a,b in zip(expected[t+j],v)]
   AG=grid_forward(A,w,p);product=[[a*b%p for a,b in zip(row,col)] for row,col in zip(AG,PG)]
   actual=grid_inverse(product,w,p);assert actual==expected
   out['full_2d_applications']+=1;out['full_output_coefficients']+=2*m*m
   # Truncated multiplication remains invertible despite zeros in oversampled multiplier.
   recovered=[]
   for t in range(m):
    row=actual[t][:]
    for j in range(1,t+1):
     v=ringmul(P[j],recovered[t-j],eta,p);row=[(a-b)%p for a,b in zip(row,v)]
    recovered.append(row)
   assert recovered==A;out['truncated_inversion_cases']+=1
  e=m.bit_length()-1
  forward=(m*m//2)*e+m*m*(e+1)
  assert 2*forward==3*m*m*e+2*m*m
  out['field_cases'].append({'M':m,'N':m*m,'p':p,'omega':w,'exact_nonzero_grid':2*m*m-2*m,'zeros_by_channel':zeros,'data_dependent_butterflies':2*forward})
 out['wrong_identity_counterexample']={'M':4,'p':17,'eta':13,'input':'a(z)=z','left_z_coefficient':1,'incorrect_right_z_coefficient':13}
 return out
if __name__=='__main__':
 r=run();Path(__file__).with_name('M_STEP_REVIEW_RESULTS.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
