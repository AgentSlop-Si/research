#!/usr/bin/env python3
"""Fresh exact controls. Only Python standard library; no author program imported."""
from fractions import Fraction
from itertools import permutations
from random import Random
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
SOURCE_PATHS=[Path('research_cycle_1535/resultant_structure/RESULTANT_STRUCTURAL_REFINEMENT.md'),Path('research_cycle_1535/resultant_refinement_independent_audit/INDEPENDENT_AUDIT.md'),Path('research_cycle_0958/algebra/final_v1/PROOF_CLOSURE.md')]
def hashes():return {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in SOURCE_PATHS}
class Field:
 def __init__(self,p=0):self.p=p;self.count=0
 def v(self,x):return x%self.p if self.p else Fraction(x)
 def add(self,a,b):self.count+=1;return self.v(a+b)
 def sub(self,a,b):self.count+=1;return self.v(a-b)
 def mul(self,a,b):self.count+=1;return self.v(a*b)
 def div(self,a,b):
  assert b!=0;self.count+=1
  return a*pow(b,-1,self.p)%self.p if self.p else a/b
 def pow(self,a,k):
  if k<0:a=self.div(self.v(1),a);k=-k
  r=self.v(1)
  while k:
   if k&1:r=self.mul(r,a)
   k>>=1
   if k:a=self.mul(a,a)
  return r

def trim(a):
 while a and a[-1]==0:a.pop()
 return a

def pa(a,b,F):
 c=[F.v(0)]*max(len(a),len(b))
 for i in range(len(c)):c[i]=F.add(a[i] if i<len(a) else F.v(0),b[i] if i<len(b) else F.v(0))
 return trim(c)
def pm(a,b,F):
 if not a or not b:return []
 c=[F.v(0)]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]=F.add(c[i+j],F.mul(x,y))
 return trim(c)
def saxpy(a,b,c,shift,F):
 r=a[:]+[F.v(0)]*max(0,len(b)+shift-len(a))
 for i,x in enumerate(b):r[i+shift]=F.sub(r[i+shift],F.mul(c,x))
 return trim(r)
def lead(row):
 d=max((len(a)-1 for a in row),default=-1)
 if d<0:return (-1,-1)
 return (d,max(i for i,a in enumerate(row) if len(a)-1==d))
def det_pencil(C,E,F,stats=None):
 """Classical successive weak-Popov determinant algorithm, specialized d <= 1."""
 n=len(C);T=[[trim([F.v(C[i][j]),F.v(E[i][j])]) for j in range(n)] for i in range(n)]
 factors=[];reductions=0;max_side=0;zero_factor=False
 for q in range(n,1,-1):
  M=[[a[:] for a in row[:-1]] for row in T];W=[row[-1][:] for row in T]
  leads=[lead(row) for row in M]
  while True:
   seen={};pair=None
   for j,(d,k) in enumerate(leads):
    if k<0:continue
    if k in seen:pair=(seen[k],j);break
    seen[k]=j
   if pair is None:break
   s,t=pair
   if leads[s][0]>leads[t][0]:s,t=t,s
   ds,k=leads[s];dt,_=leads[t];shift=dt-ds
   coeff=F.div(M[t][k][-1],M[s][k][-1])
   M[t]=[saxpy(a,b,coeff,shift,F) for a,b in zip(M[t],M[s])]
   W[t]=saxpy(W[t],W[s],coeff,shift,F)
   leads[t]=lead(M[t]);reductions+=1
   max_side=max(max_side,max((len(a)-1 for a in W),default=-1))
   assert all(len(a)<=2 for row in M for a in row)
   assert max_side<=2*n+3
  zeros=[i for i,x in enumerate(leads) if x[0]<0]
  assert zeros
  k=zeros[0];factor=W[k]
  if (k+q-1)%2:factor=[F.sub(F.v(0),x) for x in factor]
  if not factor:zero_factor=True;factors=[];break
  factors.append(factor)
  T=[row for i,row in enumerate(M) if i!=k]
 product=[]
 if not zero_factor and T[0][0]:
  factors.append(T[0][0]);assert sum(len(a)-1 for a in factors)<=n
  product=[F.v(1)]
  for factor in factors:product=pm(product,factor,F)
 assert reductions<=2*n*n
 if stats is not None:stats.update(reductions=reductions,max_side_degree=max_side,zero_factor=zero_factor)
 return trim(product)
def permutation_det_polynomial(C,E,F):
 n=len(C);out=[]
 for p in permutations(range(n)):
  term=[F.v(1)]
  for i,j in enumerate(p):term=pm(term,trim([F.v(C[i][j]),F.v(E[i][j])]),F)
  if sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))%2:term=[F.sub(F.v(0),a) for a in term]
  out=pa(out,term,F)
 return out

def determinant(A,F):
 T=[[F.v(v) for v in row] for row in A];n=len(T);r=F.v(1)
 for k in range(n):
  row=next((i for i in range(k,n) if T[i][k]),None)
  if row is None:return F.v(0)
  if row!=k:T[k],T[row]=T[row],T[k];r=F.sub(F.v(0),r)
  z=T[k][k];r=F.mul(r,z)
  for i in range(k+1,n):
   if T[i][k]:
    c=F.div(T[i][k],z)
    for j in range(k+1,n):T[i][j]=F.sub(T[i][j],F.mul(c,T[k][j]))
 return r

def resultant(f,g,m,F):
 # Fixed degree-(m,m), with m leading zero coefficients retained.
 ff=[F.v(0)]*(m+1);gg=ff[:]
 ff[:len(f)]=f;gg[:len(g)]=g;ff=ff[::-1];gg=gg[::-1]
 S=[]
 for coeff in [ff,gg]:
  for k in range(m):S.append([F.v(0)]*k+coeff+[F.v(0)]*(m-1-k))
 return determinant(S,F)
def ordinary_resultant(f,g,F):
 r=len(f)-1;s=len(g)-1
 if r<0 or s<0:return F.v(0)
 ff=f[::-1];gg=g[::-1];S=[]
 for k in range(s):S.append([F.v(0)]*k+ff+[F.v(0)]*(s-1-k))
 for k in range(r):S.append([F.v(0)]*k+gg+[F.v(0)]*(r-1-k))
 return determinant(S,F)

def poly_remainder(f,g,F):
 h=f[:]
 while h and len(h)>=len(g):
  h=saxpy(h,g,F.div(h[-1],g[-1]),len(h)-len(g),F)
 return h
def euclidean_resultant(f,g,F):
 if not f or not g:return F.v(0)
 r=len(f)-1;s=len(g)-1
 if s==0:return F.pow(g[0],r)
 if r<s:
  z=euclidean_resultant(g,f,F)
  return F.sub(F.v(0),z) if r*s%2 else z
 h=poly_remainder(f,g,F)
 if not h:return F.v(0)
 t=len(h)-1;z=F.mul(F.pow(g[-1],r-t),euclidean_resultant(g,h,F))
 return F.sub(F.v(0),z) if r*s%2 else z
def padded_euclidean_resultant(f,g,m,F):
 if not f or not g:return F.v(0)
 r=len(f)-1;s=len(g)-1
 if r<m and s<m:return F.v(0)
 z=euclidean_resultant(f,g,F)
 if r<m:
  z=F.mul(z,F.pow(g[-1],m-r))
  if m*(m-r)%2:z=F.sub(F.v(0),z)
 elif s<m:z=F.mul(z,F.pow(f[-1],m-s))
 return z

def evaluate(A,B,w,F,stats=None):
 m=len(A);w=F.v(w)
 if not w:raise ValueError('w=0 does not define w+w^-1')
 if w==F.v(1):
  C=[[F.mul(F.v(i+j),F.v(A[i][j])) for j in range(m)] for i in range(m)]
  E=[[F.mul(F.v(i+j+1),F.v(B[i][j])) for j in range(m)] for i in range(m)]
  f=det_pencil(C,A,F);g=det_pencil(E,B,F)
  return resultant(f,g,m,F)
 pp=[F.v(1)]
 for k in range(2*m-1):pp.append(F.mul(pp[-1],w))
 C=[[F.sub(F.v(0),F.mul(pp[i+j],F.v(A[i][j]))) for j in range(m)] for i in range(m)]
 E=[[F.sub(F.v(0),F.mul(pp[i+j+1],F.v(B[i][j]))) for j in range(m)] for i in range(m)]
 f=det_pencil(A,C,F);g=det_pencil(B,E,F)
 r=resultant(f,g,m,F);den=F.mul(F.pow(w,m*m*(m-1)),F.pow(F.sub(w,F.v(1)),m*m))
 return F.div(r,den)
def direct_N(A,B,w,F):
 m=len(A);w=F.v(w)
 lo=3-2*m;hi=2*m-1;S={0:F.v(0)}
 for k in range(1,hi+1):S[k]=F.add(S[k-1],F.pow(w,k-1))
 for k in range(-1,lo-1,-1):S[k]=F.sub(S[k+1],F.pow(w,k))
 N=[[F.mul(F.mul(F.v(A[i][j]),F.v(B[k][l])),S[1+k-i+l-j]) for j in range(m) for l in range(m)] for i in range(m) for k in range(m)]
 return determinant(N,F)
def mat(n,rng,p=0):return [[rng.randrange(p) if p else rng.randint(-2,2) for j in range(n)] for i in range(n)]
def ser(x):
 if isinstance(x,Fraction):return str(x)
 raise TypeError(type(x).__name__)
def main():
 before=hashes();rng=Random(104105);records=[]
 # Arbitrary pencils, including forced singular, not just C03 pencils.
 for p in [0,2,3,5,101]:
  for m in range(1,5):
   for case in range(18):
    C=mat(m,rng,p);E=mat(m,rng,p)
    if case%6==0:C[-1]=[0]*m;E[-1]=[0]*m
    if case%6==1 and m>1:C[-1]=C[0][:];E[-1]=E[0][:]
    if case%6==2:E=[[0]*m for _ in range(m)]
    F=Field(p);st={};a=det_pencil(C,E,F,st);b=permutation_det_polynomial(C,E,F)
    assert a==b,(p,m,C,E,a,b)
    records.append(dict(kind='arbitrary_pencil',p=p,m=m,case=case,coefficients=a,**st))
 # C03 singular-safe values, reciprocal symmetry and endpoint branches.
 for p in [0,2,3,5,7,101]:
  for m in range(1,7):
   for case in range(14):
    A=mat(m,rng,p);B=mat(m,rng,p)
    if case%7==0:A[-1]=[0]*m
    if case%7==1 and m>1:A[-1]=A[0][:]
    if case%7==2 and m>1:A[-1]=A[0][:];B[-1]=B[0][:]
    if case%7==3:A=[[int(i==j) for j in range(m)] for i in range(m)];B=[row[:] for row in A]
    nodes=[1,-1,2,3] if not p else list(dict.fromkeys([1,p-1,2%p,3%p]))
    for w in nodes:
     if Field(p).v(w)==0:continue
     F=Field(p);v=evaluate(A,B,w,F);cost=F.count;direct=direct_N(A,B,w,F)
     assert v==direct,(p,m,case,w,v,direct)
     reciprocal=evaluate(A,B,F.div(F.v(1),F.v(w)),F)
     assert v==reciprocal
     records.append(dict(kind='C03_value',p=p,m=m,case=case,w=w,value=v,field_ops=cost))
 # A separate quadratic resultant backend, including all degree padding strata.
 for p in [0,2,3,5,101]:
  for m in range(1,8):
   for r in range(-1,m+1):
    for ss in range(-1,m+1):
     F=Field(p)
     f=trim([F.v(rng.randint(-5,5)) for _ in range(r+1)])
     g=trim([F.v(rng.randint(-5,5)) for _ in range(ss+1)])
     z=padded_euclidean_resultant(f,g,m,F)
     assert z==resultant(f,g,m,F),(p,m,f,g,z,resultant(f,g,m,F))
     if f and g:assert euclidean_resultant(f,g,F)==ordinary_resultant(f,g,F)
     records.append(dict(kind='padded_euclidean_resultant',p=p,m=m,requested_r=r,requested_s=ss,value=z))
 # Strict padding controls.
 A=[[1,1],[1,1]];B=[[1,0],[0,1]];F=Field();w=F.v(2)
 C=[[-A[i][j]*w**(i+j) for j in range(2)] for i in range(2)]
 E=[[-B[i][j]*w**(i+j+1) for j in range(2)] for i in range(2)]
 f=det_pencil(A,C,F);g=det_pencil(B,E,F)
 assert resultant(f,g,2,F)==16 and ordinary_resultant(f,g,F)==1 and evaluate(A,B,w,F)==1
 records.append(dict(kind='strict_padding_nonendpoint',padded=16,ordinary=1,correct_V=1))
 C=[[F.v(i+j) for j in range(2)] for i in range(2)];E=[[F.v(i+j+1) for j in range(2)] for i in range(2)]
 f=det_pencil(C,A,F);g=det_pencil(E,A,F)
 assert resultant(f,g,2,F)==0 and ordinary_resultant(f,g,F)==1
 records.append(dict(kind='strict_padding_tangent',f=f,g=g,padded=0,ordinary=1))
 for p in [0,2,3]:
  try:evaluate([[1]],[[1]],0,Field(p))
  except ValueError:records.append(dict(kind='zero_node_rejected',p=p))
  else:raise AssertionError('zero node accepted')
 after=hashes();assert before==after
 out=dict(status='PASS',record_count=len(records),counts={k:sum(r['kind']==k for r in records) for k in sorted({r['kind'] for r in records})},source_hashes_before=before,source_hashes_after=after,records=records)
 (ROOT/'EXACT_CONTROL_RESULTS.json').write_text(json.dumps(out,indent=2,default=ser)+'\n')
 print(json.dumps({k:v for k,v in out.items() if k!='records'},indent=2))
if __name__=='__main__':main()
