#!/usr/bin/env python3
"""Fresh exact controls. No historical checker is imported or executed."""
from pathlib import Path
from itertools import combinations,product
from math import gcd,lcm
from collections import Counter
from fractions import Fraction
import json,time
from sympy import cyclotomic_poly,Poly,Symbol
from sympy.polys.domains import QQ
from sympy.polys.matrices import DomainMatrix
ROOT=Path(__file__).resolve().parent
X=Symbol('X')
def dump(name,obj): (ROOT/name).write_text(json.dumps(obj,indent=2)+'\n')
class Ring:
 def __init__(self,n):
  self.n=n;self.phi=list(reversed([int(x) for x in Poly(cyclotomic_poly(n,X),X).all_coeffs()]));self.k=len(self.phi)-1
 def reduce(self,h):
  a=list(h)+[0]*max(0,self.k-len(h))
  for j in range(len(a)-1,self.k-1,-1):
   v=a[j]
   if v:
    for k,c in enumerate(self.phi[:-1]):
     if c:a[j-self.k+k]-=v*c
  return a[:self.k]
 def total(self,terms):
  h=[0]*self.n
  for j,v in terms:h[j%self.n]+=v
  return self.reduce(h)
def crt(q):return q*pow(q,-1,5),5*pow(5,-1,q)
def divisor(n,d):return [[int(r//d==c%(n//d)) for c in range(n)] for r in range(n)]
def grams(R,d):
 n=len(R);K=Ring(n);out={};counts={};entries=0
 for orient in ['row','column']:
  A=R if orient=='row' else list(map(list,zip(*R)));fail=[];zero=Counter()
  for r in range(n):
   for s in range(n):
    delta=(r-s) if orient=='row' else (s-r)
    val=K.total(((delta*c,1) for c in range(n) if A[r][c] and A[s][c]));entries+=1
    expected=[d if r==s else 0]+[0]*(K.k-1)
    if val!=expected:fail.append({'pair':[r,s],'residue':val})
    elif r!=s:zero[str(n//gcd(n,r-s))]+=1
  out[orient]=fail;counts[orient]=dict(zero)
 return {'failures':out,'offdiagonal_zeros_by_order':counts,'gram_entries':entries,'phi':K.phi}
def record(label,R,d,positive):
 n=len(R);row=[sum(x) for x in R];col=[sum(x) for x in zip(*R)]
 assert row==[d]*n and col==[d]*n
 g=grams(R,d)
 for failures in g['failures'].values():assert (len(failures)==0)==positive
 return {'label':label,'n':n,'d':d,'R':R,'row_degrees':row,'column_degrees':col,**g}
def parts(n,h,minimum=1):
 if h==0:
  if n==0:yield ()
 else:
  for a in range(minimum,n//h+1):
   for b in parts(n-a,h-1,a):yield (a,)+b
def local_controls():
 nonstars={n:set() for n in range(2,6)}; examples={};tested=0
 for n in range(2,6):
  for fam in combinations(range(1,32),n):
   tested+=1
   if not all((a&b).bit_count()==1 for a,b in combinations(fam,2)):continue
   union=0;common=31
   for a in fam:union|=a;common&=a
   k=union.bit_count();I=sum(a.bit_count() for a in fam)
   if common:
    assert I==n+k-1
   else:
    assert n<=k
    nonstars[n].add((k,I));examples.setdefault(str((n,k,I)),fam)
 assert nonstars=={2:set(),3:{(3,6),(4,7),(5,8)},4:{(4,9),(5,10)},5:{(5,12)}}
 def choices(n):
  if n==1:return [(k,k,False) for k in range(6)]
  return [(k,n+k-1,False) for k in range(1,6)]+[(k,I,True) for k,I in nonstars.get(n,[])]
 partition_counts={};patterns_checked=0;saturated_h3=0
 for q in [11,13,17,19,23,29,31,37,41,43]:
  count=0
  for h in range(1,5):
   for ns in parts(q,h):
    count+=1
    for cs in product(*(choices(n) for n in ns)):
     if sum(z[0] for z in cs)>5:continue
     patterns_checked+=1;I=sum(z[1] for z in cs)
     if h==1:assert I<=q+4
     elif h==4:assert I<=q+3
     elif h==3:
      assert I<=q+4
      if I==q+4:
       assert 1 in ns and cs[ns.index(1)][0]==0
       assert any(n==4 and z[2] for n,z in zip(ns,cs));saturated_h3+=1
     else:
      if 3 in ns:
       i=ns.index(3);j=1-i;x=cs[i][1]-3;y=cs[j][1]-ns[j]
       assert 2*x+3*y<=9
       assert Fraction(3*q,q-1)<4
      elif 4 in ns:
       i=ns.index(4);j=1-i;x=cs[i][1]-4;y=cs[j][1]-ns[j]
       assert 3*x+5*y<=15
       assert Fraction(15*q,5*q-8)<4
      else:assert I<=q+3
  partition_counts[str(q)]=count
 return {'no_common_point_families':{str(n):sorted(x) for n,x in nonstars.items()},'example_bitmasks':examples,'families_tested':tested,'partitions_by_q':partition_counts,'local_patterns_checked':patterns_checked,'three_component_saturated_cases_force_empty_singleton':saturated_h3}
def q7_block():
 # Row coordinates b=0,1,2 are A; b=3,4,5,6 are B, all a=0.
 local=[]
 for v in range(7):
  if v<3:
   A=[{4}]*3
   B=[{0,1},{0,2},{0,3},{1,2,3}]
   B[v],B[3]=B[3],B[v]
  else:
   A=[{0,1},{0,2},{1,2}];B=[{3} for _ in range(4)]
   if v==3:B[3]={3,4}
  local.append(A+B)
 R=[[int(c%5 in local[c%7][b]) for c in range(35)] for b in range(7)]
 assert all(sum(row)==11 for row in R)
 e5,eq=crt(7);rows=[(b*eq)%35 for b in range(7)];K=Ring(35);vals=[]
 for i,r in enumerate(rows):
  for j,s in enumerate(rows):
   val=K.total((((r-s)*c,1) for c in range(35) if R[i][c] and R[j][c]))
   assert val==[11 if i==j else 0]+[0]*(K.k-1);vals.append(val)
 return {'n':35,'row_indices':rows,'row_degree':11,'R_block':R,'row_gram':'11 I_7','all_49_row_gram_residues':vals,'scope':'rectangular exact row-group control only; not a square equality mask'}
def clean(d):return {e:v for e,v in d.items() if v}
def add(A,B,sign=1):
 d=dict(A)
 for e,v in B.items():d[e]=d.get(e,0)+sign*v
 return clean(d)
def conj(A,n):return {(-e)%n:v for e,v in A.items()}
def product_checks(A,B,den,n,diagonal_value,K,kind):
 # A,B store sparse integer polynomial numerators, in original index order.
 checked=0
 for r in range(n):
  for s in range(n):
   h=[0]*n
   for j in range(n):
    for u,v in A[r][j].items():
     for w,z in B[j][s].items():h[(u+w)%n]+=v*z
   residue=K.reduce(h)
   assert residue==[den*diagonal_value if r==s else 0]+[0]*(K.k-1),(kind,r,s,residue)
   checked+=1
 return checked
def original_model(q=11):
 n=5*q;e5,eq=crt(q);K=Ring(n)
 L=QQ.cyclotomic_field(5);alpha=L.unit
 baseB=[[(L.zero if a==u else alpha**((-a*u)%5)/4) for u in range(5)] for a in range(5)]
 baseM=DomainMatrix(baseB,(5,5),L).inv().to_list()
 coeff=[[[Fraction(str(v)) for v in reversed(x.to_list())] for x in row] for row in baseM]
 md=lcm(*(c.denominator for row in coeff for a in row for c in a));bd=4*q
 M=[];B=[];E=[];R=[]
 for r in range(n):
  a,b=r%5,r%q;mr=[];br=[];er=[];rr=[]
  for c in range(n):
   u,v=c%5,c%q
   m=clean({(j*e5+b*v*eq)%n:int(x*md) for j,x in enumerate(coeff[a][u])})
   z={} if a==u else {(-r*c)%n:1}
   e=add(m,{r*c%n:md},-1)
   mr.append(m);br.append(z);er.append(e);rr.append(int(a==u))
  M.append(mr);B.append(br);E.append(er);R.append(rr)
 assert all(sum(bool(z) for z in row)==n-q for row in B)
 assert all(sum(bool(B[r][c]) for r in range(n))==n-q for c in range(n))
 checks={}
 checks['M_B']=product_checks(M,B,md*bd,n,1,K,'M B');print('Original product M B passed',flush=True)
 checks['B_M']=product_checks(B,M,md*bd,n,1,K,'B M');print('Original product B M passed',flush=True)
 Estar=[[conj(E[c][r],n) for c in range(n)] for r in range(n)]
 checks['E_Estar']=product_checks(E,Estar,md*md,n,q,K,'E E*');print('Original error E E* passed',flush=True)
 checks['Estar_E']=product_checks(Estar,E,md*md,n,q,K,'E* E');print('Original error E* E passed',flush=True)
 g=grams(R,q);assert not any(g['failures'].values())
 return {'n':n,'d':q,'R':R,'phi_ascending':K.phi,'coefficient_encoding':'each entry is exponent-to-integer-numerator map in Q[zeta_N]; matrices use actual index order 0,...,N-1','B_denominator':bd,'B_numerators':B,'M_denominator':md,'M_numerators':M,'E_denominator':md,'E_numerators':E,'inverse_row_budget':n-q,'inverse_column_budget':n-q,'checks':checks,'gram_entries':g['gram_entries'],'normalization':'M_normalized=M_tilde/sqrt(N); inverse=sqrt(N) B_tilde; squared error=d/N'}
def main():
 start=time.time();lc=local_controls();dump('LOCAL_CONTROLS.json',lc);dump('Q7_ROW_GROUP_COUNTERCONTROL.json',q7_block());print('Local proofs and q7 boundary control passed',flush=True)
 positives=[];negatives=[]
 for q in [7,11,13]:
  n=5*q
  for d in [1,5,q,n]:
   positives.append(record(f'Original divisor N={n}, d={d}',divisor(n,d),d,True))
 print('Twelve positive masks passed',flush=True)
 for q in [11,13]:
  n=5*q
  R=[[int(r%5==c%5 or r%q==c%q) for c in range(n)] for r in range(n)]
  rec=record(f'Cross-shape degree q+4, q={q}',R,q+4,False)
  assert all(n//gcd(n,r['pair'][0]-r['pair'][1])==n for r in rec['failures']['row'])
  negatives.append(rec)
  for t in [1,2,3]:
   R=[]
   for r in range(n):
    a,b=r%5,r%q;u0=a if b else (a+1)%5
    R.append([int(c%5==u0 or (c%q==b and (c%5-a)%5 in range(2,t+2))) for c in range(n)])
   rec=record(f'All-split q+{t}, q={q}',R,q+t,False)
   assert all((x['pair'][0]-x['pair'][1])%5!=0 for x in rec['failures']['row'])
   negatives.append(rec)
 print('Eight regular same-group-valid negative masks passed',flush=True)
 dump('POSITIVE_CONTROLS.json',positives);dump('NEGATIVE_CONTROLS.json',negatives)
 congruences=0
 for q in [7,11,13,17,19]:
  n=5*q;e5,eq=crt(q)
  for h in range(1,n):
   if gcd(h,n)!=1:continue
   for r in range(n):
    for c in range(n):
     assert h*(r*c-(r%5)*(c%5)*e5-(r%q)*(c%q)*eq)%n==0;congruences+=1
 print('Original CRT congruences passed',flush=True)
 witness=original_model();dump('ORIGINAL_MODEL_CONTROL.json',witness)
 result={'all_passed':True,'positive_masks':len(positives),'negative_masks':len(negatives),'full_gram_entries':sum(r['gram_entries'] for r in positives+negatives)+witness['gram_entries'],'q7_rectangular_gram_entries':49,'original_inverse_product_entries':witness['checks']['M_B']+witness['checks']['B_M'],'original_error_gram_entries':witness['checks']['E_Estar']+witness['checks']['Estar_E'],'crt_congruences':congruences,'local_patterns_checked':lc['local_patterns_checked'],'elapsed_seconds':time.time()-start,'historical_code_imported_or_executed':False,'floating_tolerances_used':False,'full_mask_census':False,'external_writes':False}
 dump('RESULTS.json',result);print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':main()
