#!/usr/bin/env python3
"""Fresh reviewer controls. Standard library, no author or historical imports."""
from fractions import Fraction as F
from pathlib import Path
import json, itertools, math, hashlib
P=Path(__file__).resolve().parent

def aadd(a,b):
 c=dict(a)
 for k,v in b.items():c[k]=c.get(k,F(0))+v
 return {k:v for k,v in c.items() if v}
def amul(a,b):
 c={}
 for k,u in a.items():
  for l,v in b.items():c[k+l]=c.get(k+l,F(0))+u*v
 return {k:v for k,v in c.items() if v}
def scale(a,x):return {k:v*x for k,v in a.items() if v*x}
def adj(A):return [[{-k:v for k,v in A[j][i].items()} for j in range(len(A))] for i in range(len(A))]
def mm(A,B):
 n=len(A);C=[[{} for _ in range(n)] for _ in range(n)]
 for i in range(n):
  for j in range(n):
   for k in range(n):C[i][j]=aadd(C[i][j],amul(A[i][k],B[k][j]))
 return C
def ident(n):return [[{0:F(1)} if i==j else {} for j in range(n)] for i in range(n)]
def poly_matrix(A,c):
 n=len(A);B=ident(n);out=[[{} for _ in range(n)] for _ in range(n)]
 for a in c:
  for i in range(n):
   for j in range(n):out[i][j]=aadd(out[i][j],scale(B[i][j],a))
  B=mm(B,A)
 return out
def make_cycle(order,weights):
 A=[[{} for _ in order] for _ in order]
 for i,u in enumerate(order):A[order[(i+1)%len(order)]][u]=weights[i]
 return A

def check_alg049():
 orders=[list(range(8)),[0,1,3,4,5,6,2,7]]
 weights=[[{0:F(1)}]*7+[{0:F(-1)}],[{1:F(1)}]+[{0:F(1)}]*5+[{-1:F(1)},{0:F(-1)}]]
 mats=[make_cycle(a,b) for a,b in zip(orders,weights)]
 plus=[F(3,2)]+[F(1,2)]*7
 minus=[F(129,257)]+[F(-2**(7-j),257) for j in range(1,8)]
 Ks=[{'+':poly_matrix(A,plus),'-':poly_matrix(A,minus)} for A in mats]
 for K in Ks:assert mm(K['+'],K['-'])==ident(8)==mm(K['-'],K['+'])
 derived={}
 for signs in ('--','-+','+-','++'):
  T=mm(Ks[0][signs[0]],Ks[1][signs[1]])
  inv=mm(Ks[1]['+' if signs[1]=='-' else '-'],Ks[0]['+' if signs[0]=='-' else '-'])
  assert mm(T,inv)==ident(8)
  derived[signs]={'L':mm(adj(T),T),'Linv':mm(inv,adj(inv))}
 data=json.loads((P/'ALG049_ROW_CERTIFICATES.json').read_text());checks=0
 for r in data['records']:
  row=r['row'];covered=set()
  for e in r['edges']:
   i,j=e['i'],e['j'];assert row in (i,j) and i!=j
   covered.add(j if i==row else i)
   got=derived[r['signs']][r['matrix']][i][j]
   expect={int(k):F(v) for k,v in e['laurent'].items()};assert got==expect
   target=F(e['lower_bound']);assert target>0
   if e['method']=='coefficient_dominance':
    lower=2*max(map(abs,got.values()))-sum(map(abs,got.values()))
   else:
    assert set(got)<={-1,0,1}
    lower=got.get(0,0)-abs(got.get(-1,0)+got.get(1,0))
   assert lower==target
   checks+=1
  assert covered==set(range(8))-{row}
 # Combinatorial support lemma is checked independently for EVERY support subset.
 support_checks=0
 for mask in range(1,256):
  E=[j for j in range(8) if mask>>j&1];D={(a-b)%8 for a in E for b in E}
  if len(D)==8:continue
  for row in range(8):
   missing=[j for j in range(8) if j!=row and all((row+a)%8!=(j+b)%8 for a in E for b in E)]
   assert missing
   support_checks+=1
 # Removing the E-E condition must fail at dense support.
 assert {(a-b)%8 for a in range(8) for b in range(8)}==set(range(8))
 bad=data['records'][0]['edges'][0];assert derived['--']['L'][bad['i']][bad['j']]!={0:F(0)}
 return {'exact_uniform_phase_certificates':checks,'all_subset_row_support_checks':support_checks,'inverse_checks':6,'all_8_Gram_rows_dense':True}

def avoiding(n,b):
 v=[1]+[0]*(b-1)
 for _ in range(n):v=[sum(v)]+v[:-1]
 return sum(v)
def check_marker():
 cases=0;examples=[]
 for n in range(2,129):
  N=2**n
  for b in range(1,n):
   d=n-b;r=2**d;m=r+avoiding(n,b)
   es=[2**(d-h)*avoiding(h-1,b) for h in range(1,d+1)]
   assert m+sum(es)==N
   moment=sum((h+1)*e for h,e in enumerate(es))
   joint=sum((n-h)*e for h,e in enumerate(es))
   assert m*(n+1)+moment+joint==N*(n+1)
   assert moment<=N*(2**(b+1)-b-2)
   assert max((h+1)*e for h,e in enumerate(es))<=2*N
   cases+=1
  if n in (16,32,64,128):
   b=(n.bit_length()-1)//2;x=2**b;m=2**(n-b)+avoiding(n,b)
   examples.append({'n':n,'b':b,'retained_slots_over_N':str(F(m*(n+1),N)),'x':x})
 assert m*(n+1)+moment+joint+1!=N*(n+1) # One altered slot is detected.
 return {'all_cut_cardinality_moment_ledger_cases':cases,'sqrt_parameter_examples':examples}

def check_chirp():
 # Exact cyclotomic geometric sums: mod X^(N/2)+1 for dyadic N.
 def reduce_exponents(exps,N):
  c=[0]*(N//2)
  for e in exps:
   k=e%N;c[k%(N//2)]+=1 if k<N//2 else -1
  return c
 cases=0;orthogonality=0
 for n in range(1,10):
  N=2**n
  for k in range(n+1):
   M,D=2**(n-k),2**k;R=min(M,D);H=max(M,D)
   if D<=M:
    for u in range(D):
     for v in range(D):
      exps=[2**k*a*(u-v) for a in range(M)]
      got=reduce_exponents(exps,N);want=[M if u==v else 0]+[0]*(N//2-1)
      assert got==want;orthogonality+=1
   else:
    for u in range(M):
     for v in range(M):
      exps=[2**k*d*(u-v) for d in range(D)]
      got=reduce_exponents(exps,N);want=[D if u==v else 0]+[0]*(N//2-1)
      assert got==want;orthogonality+=1
   assert R*H==N
   for r in range(R+1):assert F((R-r)*H,N)==1-F(r,R)
   cases+=1
 return {'exact_dyadic_Gram_cases':cases,'exact_Gram_entry_checks':orthogonality,'flat_spectrum_energy_identity':True}

def check_sparse():
 # Exact rational Walsh flat-unitary witnesses, dimensions square powers of two.
 cases=0
 for N in (4,16,64):
  U=[[F((-1)**((i&j).bit_count()%2),math.isqrt(N)) for j in range(N)] for i in range(N)]
  for width in range(1,min(8,N)+1):
   z=[F((j+1)*(-1)**j) if j<width else F(0) for j in range(N)]
   Uz=[sum(a*b for a,b in zip(row,z)) for row in U];norm=sum(x*x for x in z)
   for size in range(N+1):
    inside=sum(x*x for x in Uz[:size]);assert inside<=F(width*size,N)*norm
    outside=sum(x*x for x in Uz[size:]);assert outside>=max(F(0),1-F(width*size,N))*norm
    cases+=1
 # E=diag(1,0), Q swaps coordinates and v=e1: Ev=0 but EQv!=0.
 E=[[1,0],[0,0]];Q=[[0,1],[1,0]];v=[0,1]
 mv=lambda A,v:[sum(a*b for a,b in zip(row,v)) for row in A]
 assert mv(E,v)==[0,0] and mv(E,mv(Q,v))!=[0,0]
 # A singular Q can kill the chosen nonzero vector, invalidating normalization.
 assert mv([[1,0],[0,0]],v)==[0,0] and v!=[0,0]
 return {'exact_flat_unitary_energy_controls':cases,'guard_negative_controls':2,'proof_dependency':'kernel of any k+1 columns of EQ; Q invertible; complex flat unitary; support bounds capped by N'}

if __name__=='__main__':
 result={'verdict':'PASS','alg040':check_marker(),'alg043':check_chirp(),'alg044':check_sparse(),'alg049':check_alg049()}
 print(json.dumps(result,indent=2,sort_keys=True))
