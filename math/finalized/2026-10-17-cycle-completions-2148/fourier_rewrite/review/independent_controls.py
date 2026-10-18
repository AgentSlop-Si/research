#!/usr/bin/env python3
"""Independent review controls. Imports no supplied or submitted verification code."""
import json, hashlib, itertools, zipfile
from fractions import Fraction as Q
from pathlib import Path
OUT=Path(__file__).resolve().parent
SRC=Path(__file__).resolve().parent / '../candidate'

def case(D):
 N=2**D; h=N//2
 # Exact cyclotomic ring Q[z]/(z^(N/2)+1). Unlike a single-exponent
 # encoding this permits additions, cancellation and general polynomials.
 def p(e=0,q=Q(1)):
  e%=N
  if e>=h:e-=h;q=-q
  return {e:q} if q else {}
 def add(a,b):
  c=dict(a)
  for e,v in b.items():
   c[e]=c.get(e,Q(0))+v
   if not c[e]:del c[e]
  return c
 def mul(a,b):
  c={}
  for e,x in a.items():
   for f,y in b.items():c=add(c,p(e+f,x*y))
  return c
 def mm(A,B):
  C=[]
  for row in A:
   out={}
   for k,x in row.items():
    for j,y in B[k].items():
     out[j]=add(out.get(j,{}),mul(x,y))
     if not out[j]:del out[j]
   C.append(out)
  return C
 I=[{j:p()} for j in range(N)]
 B=[]
 for m in range(1,D+1):
  A=[{} for j in range(N)]
  for a in range(N):
   b=a^(1<<(m-1));lo=min(a,b);hi=max(a,b)
   j=lo% (1<<(m-1));e=j*(N//(1<<m))
   A[a][lo]=p();A[a][hi]=p(e+(N//2 if a==hi else 0))
  B.append(A)
 rev=lambda j:int(format(j,f'0{D}b')[::-1],2)
 A=[{rev(j):p()} for j in range(N)]
 for stage in B:A=mm(stage,A)
 assert all(A[r].get(c,{})==p(r*c) for r in range(N) for c in range(N))
 counts=[];cross=0
 for a in range(D):
  A=I
  for b in range(a,D):
   A=mm(B[b],A);k=b-a+1
   assert all(len(row)==2**k for row in A)
   assert all(sum(c in row for row in A)==2**k for c in range(N))
   unseen=set(range(N));components=[]
   while unseen:
    seed=next(iter(unseen));seen={seed};todo=[seed]
    while todo:
     r=todo.pop()
     for c in A[r]:
      if c not in seen:seen.add(c);todo.append(c)
    unseen-=seen;components.append(seen)
   assert len(components)==N//(2**k)
   assert all(len(c)==2**k for c in components)
   counts.append(len(components))
   if k==1:
    for comp in components:
     r,s=sorted(comp)
     lhs=mul(A[r][r],A[s][s]);rhs=mul(A[r][s],A[s][r])
     assert lhs==mul(p(N//2),rhs)
     cross+=1
 assert sum(counts)==N*(D-1)+1 and cross==N*D//2
 twiddles=[j*(N//(2**m)) for m in range(1,D+1) for q in range(0,N,2**m) for j in range(2**(m-1))]
 paid=sum(e!=0 and 4*e!=N for e in twiddles)
 assert paid==N*D//2-3*N//2+2
 return {'D':D,'N':N,'exact_DFT_entries':N*N,'component_windows':sum(counts),'single_stage_cross_ratios':cross,'general_twiddle_multiplications':paid}

# Exact Gaussian rationals, represented independently as Python complex-like pairs.
def z(a=0,b=0):return (Q(a),Q(b))
def plus(a,b):return tuple(a[j]+b[j] for j in (0,1))
def times(a,b):return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def reciprocal(a):return(a[0]/(a[0]**2+a[1]**2),-a[1]/(a[0]**2+a[1]**2))
def mat(A,B):return [[plus(times(A[r][0],B[0][c]),times(A[r][1],B[1][c])) for c in (0,1)] for r in (0,1)]
def scale(A,a):return [[times(x,a) for x in row] for row in A]
def inv(A):
 det=plus(times(A[0][0],A[1][1]),times(z(-1),times(A[0][1],A[1][0])))
 return scale([[A[1][1],times(z(-1),A[0][1])],[times(z(-1),A[1][0]),A[0][0]]],reciprocal(det))
def chi(A):return times(times(A[0][0],A[1][1]),reciprocal(times(A[0][1],A[1][0])))
C=[[z(Q(1,2),Q(1,2)),z(Q(1,2),Q(-1,2))],[z(Q(1,2),Q(-1,2)),z(Q(1,2),Q(1,2))]]
Z=[[z(1),z()],[z(),z(-1)]]
M=mat(mat(inv(C),Z),C)
assert M==[[z(),z(0,-1)],[z(0,1),z()]]
checks=[]
for rho in [z(3),z(-3),z(0,1),z(0,-1)]:
 diag=[[reciprocal(plus(z(1),times(z(-1),rho))),z()],[z(),reciprocal(plus(z(1),rho))]]
 R=mat(mat(inv(C),diag),C)
 assert chi(R)==reciprocal(times(rho,rho))
 for rp in [(0,1),(1,0)]:
  for cp in [(0,1),(1,0)]:
   A=[[times(times(z(2+r,1),R[rp[r]][cp[c]]),z(3+c,-2)) for c in (0,1)] for r in (0,1)]
   assert chi(A) in [chi(R),reciprocal(chi(R))]
 if rho==z(0,1):
  t=z(2,3);T=[[z(1),z()],[z(),t]]
  assert scale(mat(mat(Z,R),T),z(2))==[[z(1),t],[z(1),times(z(-1),t)]]
 if rho==z(0,-1):
  t=z(2,3);T=[[z(1),z()],[z(),times(z(-1),t)]]
  assert scale(mat(R,T),z(2))==[[z(1),t],[z(1),times(z(-1),t)]]
 checks.append({'rho':str(rho),'cross_ratio':str(chi(R))})
cases=[case(D) for D in range(1,7)]
manifest=json.loads((SRC/'MANIFEST.json').read_text())
result={'status':'PASS','method':'Independent cyclotomic quotient-ring matrix products and Gaussian-rational controls','cases':cases,'gaussian_controls':checks,'supplied_R30_code_executed':False,'submitted_verifier_executed':False,'reviewed_file_sha256':{n:hashlib.sha256((SRC/n).read_bytes()).hexdigest() for n in ['PROOF.md','README.md','SOURCES.md','verify_completion.py','verification.json','verification_summary.json']}}
(OUT/'independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
