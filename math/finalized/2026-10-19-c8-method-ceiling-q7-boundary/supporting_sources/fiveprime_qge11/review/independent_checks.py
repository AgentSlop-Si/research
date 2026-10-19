#!/usr/bin/env python3
"""Independent exact audit. The candidate is read only as text/JSON data.
No candidate or historical program is imported or executed; no floating arithmetic.
"""
from pathlib import Path
from itertools import combinations, combinations_with_replacement, product
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from math import gcd
import json, time
HERE=Path(__file__).resolve().parent
C=Path('/workspace/shared/sparse_fiveq_first_interior_20261019_1344')
EXPECTED='3764006c03cc895ea71d44764391867c17490957a2734007cb52a0b85b04650a'
def dump(name,data): (HERE/name).write_text(json.dumps(data,indent=2)+'\n')
def digest(p): return sha256(p.read_bytes()).hexdigest()
def integrity():
 assert digest(C/'MANIFEST.json')==EXPECTED
 manifest=json.loads((C/'MANIFEST.json').read_text())
 assert len(manifest['files'])==23
 for f in manifest['files']:
  p=C/f['path']; assert p.stat().st_size==f['bytes'] and digest(p)==f['sha256'],f
 sources=json.loads((C/'SOURCE_BINDINGS.json').read_text())
 for s in sources:
  for p in [C/s['copy'],Path(s['source'])]:
   assert p.stat().st_size==s['bytes'] and digest(p)==s['sha256'],str(p)
 assert (C/'SEAL.sha256').read_text().strip()==EXPECTED+'  MANIFEST.json'
 return {'manifest_sha256':EXPECTED,'report_sha256':digest(C/'REPORT.md'),'entries_verified':23,'source_copies_and_originals_verified':len(sources),'seal_matches':True}
def phi5q(q):
 # Phi_(5q)(x)=Phi_5(x^q)/Phi_5(x) for prime q != 5.
 f=[0]*(4*q+1)
 for i in range(5): f[i*q]=1
 quotient=[0]*(4*q-3)
 for j in range(4*q,3,-1):
  v=f[j]; quotient[j-4]=v
  for k in range(5): f[j-4+k]-=v
 assert f==[0]*len(f)
 assert quotient[-1]==1 and len(quotient)==4*(q-1)+1
 return quotient
class Field:
 def __init__(self,q): self.q=q;self.n=5*q;self.phi=phi5q(q);self.degree=len(self.phi)-1;self.powers=[self.reduce([0]*j+[1]) for j in range(self.n)]
 def reduce(self,a):
  a=list(a)+[0]*max(0,self.degree-len(a))
  for j in range(len(a)-1,self.degree-1,-1):
   z=a[j]
   if z:
    for k,c in enumerate(self.phi): a[j-self.degree+k]-=z*c
  return a[:self.degree]
 def sum_powers(self,exponents):
  a=[0]*self.n
  for e in exponents:a[e%self.n]+=1
  return self.reduce(a)
def grams(mask,d,q,h=1,rect_rows=None):
 K=Field(q);n=5*q;out={};zero={};checked=0
 assert gcd(h,n)==1
 orientations=['row','column'] if rect_rows is None else ['row']
 for mode in orientations:
  A=mask if mode=='row' else [list(a) for a in zip(*mask)]
  ids=list(range(n)) if rect_rows is None else rect_rows
  supports=[{c for c,x in enumerate(row) if x} for row in A]
  failures=[];counts=Counter()
  for i in range(len(A)):
   for j in range(len(A)):
    exponent=h*(ids[i]-ids[j])*(1 if mode=='row' else -1)
    residue=K.sum_powers(exponent*c for c in supports[i]&supports[j]);checked+=1
    expected=[d if i==j else 0]+[0]*(K.degree-1)
    if residue!=expected: failures.append({'pair':[i,j],'residue':residue})
    elif i!=j:counts[str(n//gcd(n,ids[i]-ids[j]))]+=1
  out[mode]=failures;zero[mode]=dict(counts)
 return {'failures':out,'offdiagonal_zeros_by_order':zero,'gram_entries':checked,'phi':K.phi}
def summary(label,q,d,g):
 return {'label':label,'q':q,'d':d,'gram_entries':g['gram_entries'],'failure_counts':{k:len(v) for k,v in g['failures'].items()},'offdiagonal_zeros_by_order':g['offdiagonal_zeros_by_order'],'failure_data_sha256':sha256(json.dumps(g['failures'],sort_keys=True,separators=(',',':')).encode()).hexdigest(),'first_failure':{k:v[:1] for k,v in g['failures'].items()}}
def local():
 classes={i:set() for i in range(2,6)};checked=0;valid=0;repeated_valid=0
 for n in range(2,6):
  for family in combinations_with_replacement(range(1,32),n):
   checked+=1
   if any((a&b).bit_count()!=1 for a,b in combinations(family,2)):continue
   valid+=1;repeated_valid+=len(set(family))<n
   union=0;common=31
   for x in family:union|=x;common&=x
   k=union.bit_count();I=sum(x.bit_count() for x in family)
   if common:
    assert common.bit_count()==1 and I==n+k-1
   else:
    assert n<=k;classes[n].add((k,I))
 assert classes=={2:set(),3:{(3,6),(4,7),(5,8)},4:{(4,9),(5,10)},5:{(5,12)}}
 # All numerical patterns come from this independent multiset enumeration.
 def options(n):
  if n==1:return [(k,k,False) for k in range(6)]
  return [(k,n+k-1,False) for k in range(1,6)]+[(k,I,True) for k,I in classes.get(n,())]
 def partitions(total,length,lo=1):
  if length==0:
   if total==0:yield ()
  else:
   for a in range(lo,total//length+1):
    for rest in partitions(total-a,length-1,a):yield(a,)+rest
 patterns=0;saturated=[];counts={}
 # Includes q=11 threshold, new primes, and larger integers: these controls do not supply universal quantification.
 for q in [11,12,13,17,19,23,47,53]:
  ct=0
  for h in range(1,5):
   for sizes in partitions(q,h):
    ct+=1
    for choices in product(*(options(n) for n in sizes)):
     if sum(t[0] for t in choices)>5:continue
     patterns+=1;I=sum(t[1] for t in choices)
     if h==1:assert I<=q+4
     if h==4:assert I<=q+3
     if h==3:
      assert I<=q+4
      if I==q+4:
       assert sizes.count(1)==1
       j=sizes.index(1);assert choices[j][0]==0
       assert sizes==(1,4,q-5) if q>=9 else True
       saturated.append({'q':q,'sizes':sizes,'choices':choices})
     if h==2:
      if 3 in sizes:
       j=sizes.index(3);k=1-j;x=choices[j][1]-3;y=choices[k][1]-sizes[k]
       assert 2*x+3*y<=9 and Fraction(3*q,q-1)<4
      elif 4 in sizes:
       j=sizes.index(4);k=1-j;x=choices[j][1]-4;y=choices[k][1]-sizes[k]
       assert 3*x+5*y<=15 and Fraction(15*q,5*q-8)<4
      else:assert I<=q+3
  counts[str(q)]=ct
 return {'multisets_checked':checked,'valid_pairwise_one_multisets':valid,'valid_with_repeated_restrictions':repeated_valid,'nonstars':{n:sorted(c) for n,c in classes.items()},'partitions_by_q':counts,'local_patterns_checked':patterns,'saturated_h3':saturated}
def boundary():
 local=[]
 for v in range(7):
  if v<3:
   # The long B row cycles among B0,B1,B2; B3 remains short.
   bsets=[{0,1},{0,2},{0,3},{1,2,3}]
   bsets[v],bsets[3]=bsets[3],bsets[v]
   local.append([{4},{4},{4}]+bsets)
  else:
   bsets=[{3},{3},{3},{3,4} if v==3 else {3}]
   local.append([{0,1},{0,2},{1,2}]+bsets)
 rows=[(15*b)%35 for b in range(7)]
 R=[[int(c%5 in local[c%7][b]) for c in range(35)] for b in range(7)]
 assert [sum(row) for row in R]==[11]*7
 for v in range(7):
  for i,j in combinations(range(7),2):assert len(local[v][i]&local[v][j])==int((i<3)==(j<3))
 g=grams(R,11,7,rect_rows=rows);assert not g['failures']['row']
 retained=json.loads((C/'Q7_ROW_GROUP_COUNTERCONTROL.json').read_text())
 assert retained['R_block']==R and retained['row_indices']==rows
 assert retained['all_49_row_gram_residues']==[[11 if i==j else 0]+[0]*23 for i in range(7) for j in range(7)]
 # This rectangular block cannot be claimed to have a 35-column scalar Gram.
 cols=[sum(row[c] for row in R) for c in range(35)]
 assert max(cols)<11 and len(set(cols))>1
 return {'N':35,'degree':11,'shape':[7,35],'row_indices':rows,'R_block':R,'row_degrees':[11]*7,'column_degrees':cols,'row_gram_verified':'11 I_7','row_gram_entries':49,'scope':'Rectangular row-group countercontrol only; no square mask conclusion.'}
def audit_masks():
 summaries=[];count=0
 for filename,positive in [('POSITIVE_CONTROLS.json',True),('NEGATIVE_CONTROLS.json',False)]:
  records=json.loads((C/filename).read_text())
  for a in records:
   R=a['R'];n=a['n'];d=a['d'];q=n//5
   assert all(x in (0,1) for row in R for x in row)
   row=[sum(r) for r in R];col=[sum(c) for c in zip(*R)]
   assert row==col==[d]*n and row==a['row_degrees'] and col==a['column_degrees']
   g=grams(R,d,q)
   for key in ['failures','offdiagonal_zeros_by_order','gram_entries','phi']:assert g[key]==a[key],(a['label'],key)
   assert all((not f)==positive for f in g['failures'].values())
   summaries.append(summary(a['label'],q,d,g));count+=g['gram_entries']
 return {'records':summaries,'full_gram_entries':count}
def fresh_masks():
 records=[]
 for q in [17,19]:
  n=5*q
  data=[]
  for d in [1,5,q,n]:
   # Distinct expression of the divisor construction, in actual index order.
   R=[[int(c%(n//d)<=r//d<c%(n//d)+1) for c in range(n)] for r in range(n)]
   data.append(('divisor',d,R,True))
  R=[[int((r-c)%5==0 or (r-c)%q==0) for c in range(n)] for r in range(n)]
  data.append(('cross-shape',q+4,R,False))
  for t in [1,2,3]:
   R=[]
   for r in range(n):
    a,b=r%5,r%q;line=(a+int(b==0))%5
    R.append([int(c%5==line or (c%q==b and c%5 in {(a+j)%5 for j in range(2,t+2)})) for c in range(n)])
   data.append(('all-split',q+t,R,False))
  for label,d,R,pos in data:
   assert [sum(r) for r in R]==[sum(c) for c in zip(*R)]==[d]*n
   for unit in [1,2]:
    g=grams(R,d,q,h=unit)
    assert all((not f)==pos for f in g['failures'].values())
    if label=='cross-shape':assert all(gcd(n,x['pair'][0]-x['pair'][1])==1 for x in g['failures']['row'])
    if label=='all-split':assert all((x['pair'][0]-x['pair'][1])%5 for x in g['failures']['row'])
    z=summary(label,q,d,g);z['primitive_root_multiplier']=unit;records.append(z)
 return {'records':records,'fresh_masks':16,'root_evaluations':32,'full_gram_entries':sum(x['gram_entries'] for x in records)}
def audit_original():
 a=json.loads((C/'ORIGINAL_MODEL_CONTROL.json').read_text());n=a['n'];d=a['d'];q=n//5;K=Field(q)
 assert (n,d)==(55,11) and a['phi_ascending']==K.phi
 def decode(A):return [[{int(e):v for e,v in entry.items() if v} for entry in row] for row in A]
 B,M,E=map(decode,[a['B_numerators'],a['M_numerators'],a['E_numerators']]);bd=a['B_denominator'];md=a['M_denominator']
 assert a['E_denominator']==md and bd==n-d
 R=a['R'];assert R==[[int(r%5==c%5) for c in range(n)] for r in range(n)]
 for r in range(n):
  for c in range(n):
   assert B[r][c]==({} if R[c][r] else {(-r*c)%n:1})
   diff=dict(M[r][c]);e=(r*c)%n;diff[e]=diff.get(e,0)-md
   assert E[r][c]=={e:z for e,z in diff.items() if z}
 assert [sum(bool(e) for e in row) for row in B]==[n-d]*n
 assert [sum(bool(B[r][c]) for r in range(n)) for c in range(n)]==[n-d]*n
 def adjoint(A):return [[{(-e)%n:z for e,z in A[c][r].items()} for c in range(n)] for r in range(n)]
 def check(A,B,diag):
  for i in range(n):
   for j in range(n):
    coeff=[0]*n
    for k in range(n):
     for e,x in A[i][k].items():
      for f,y in B[k][j].items():coeff[(e+f)%n]+=x*y
    assert K.reduce(coeff)==[diag if i==j else 0]+[0]*(K.degree-1)
  return n*n
 checks={'M_B':check(M,B,md*bd),'B_M':check(B,M,md*bd),'E_Estar':check(E,adjoint(E),md*md*d),'Estar_E':check(adjoint(E),E,md*md*d)}
 assert checks==a['checks']
 g=grams(R,d,q);assert not any(g['failures'].values())
 return {'n':n,'d':d,'definitions_and_budgets_verified':True,'both_inverse_product_entries':checks['M_B']+checks['B_M'],'both_error_gram_entries':checks['E_Estar']+checks['Estar_E'],'both_mask_gram_entries':g['gram_entries'],'exact_denominators':{'B':bd,'M':md,'E':md}}
def crt():
 checks=0
 for q in [7,11,13,17,19,23]:
  n=5*q;e5=q*pow(q,-1,5);eq=5*pow(5,-1,q)
  for r in range(n):
   for c in range(n):
    assert (r*c-e5*(r%5)*(c%5)-eq*(r%q)*(c%q))%n==0;checks+=1
  # All primitive roots preserve the identity because it is a congruence.
  assert e5*e5%n==e5%n and eq*eq%n==eq%n and e5*eq%n==0 and (e5+eq)%n==1
 return {'tested_primes':[7,11,13,17,19,23],'original_index_pair_congruences':checks,'all_primitive_roots_follow_from_congruence':True}
def main():
 start=time.monotonic();first=integrity();dump('CANDIDATE_BINDING.json',first);print('Frozen candidate and source bindings verified.',flush=True)
 z=local();dump('LOCAL_EXACT_CHECKS.json',z);print('Local multisets and incidence inequalities verified.',flush=True)
 z=boundary();dump('Q7_RECTANGULAR_CHECK.json',z);print('Rectangular q=7 boundary independently reconstructed.',flush=True)
 z=audit_masks();dump('CANDIDATE_MASK_AUDIT.json',z);print('All retained positive and negative Gram data independently recalculated.',flush=True)
 f=fresh_masks();dump('FRESH_MASK_CONTROLS.json',f);print('Fresh q=17,19 masks checked in both Gram orders and two primitive roots.',flush=True)
 o=audit_original();dump('ORIGINAL_MODEL_AUDIT.json',o);print('Full original inverse and error products verified.',flush=True)
 c=crt();dump('CRT_CHECKS.json',c)
 last=integrity();assert first==last
 result={'all_passed':True,'candidate_manifest_sha256':EXPECTED,'local_multisets':json.loads((HERE/'LOCAL_EXACT_CHECKS.json').read_text())['multisets_checked'],'local_patterns':json.loads((HERE/'LOCAL_EXACT_CHECKS.json').read_text())['local_patterns_checked'],'candidate_square_gram_entries':z['full_gram_entries']+o['both_mask_gram_entries'],'fresh_square_gram_entries':f['full_gram_entries'],'rectangular_gram_entries':49,'inverse_product_entries':o['both_inverse_product_entries'],'error_gram_entries':o['both_error_gram_entries'],'original_index_pair_congruences':c['original_index_pair_congruences'],'final_candidate_integrity_recheck':True,'candidate_programs_imported_or_executed':False,'floating_arithmetic_used':False,'external_writes':False,'full_mask_census':False,'elapsed_seconds':time.monotonic()-start}
 dump('CHECK_RESULTS.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':main()
