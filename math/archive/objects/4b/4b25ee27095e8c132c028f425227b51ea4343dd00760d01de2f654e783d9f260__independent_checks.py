#!/usr/bin/env python3
"""Independent nonlinear routing rank checks; source scripts never imported."""
from pathlib import Path
from itertools import combinations
import json,random
from exact_utils import Field,prime_by_trial_division
from flow_utils import network_bound
BASE=Path(__file__).parent

def affine(cols,offset=0):
 p=[]
 for v in range(1<<len(cols)):
  out=offset
  for j,c in enumerate(cols):
   if (v>>j)&1:out^=c
  p.append(out)
 assert sorted(p)==list(range(len(p)));return p

def mcnot(k,cs,t):
 assert len(set(cs))==len(cs) and t not in cs and all(0<=j<k for j in [*cs,t])
 return [v^(1<<t) if all(v&(1<<c) for c in cs) else v for v in range(1<<k)]
def compose(a,b):return [a[v] for v in b]
def cycle_rank(p,a):
 inv=[0]*len(a)
 for i,j in enumerate(a):inv[j]=i
 rel=[inv[v] for v in p];seen=set();cc=0
 for v in range(len(p)):
  if v in seen:continue
  cc+=1
  while v not in seen:seen.add(v);v=rel[v]
 return len(p)-cc

def parity(n,a):return [v for v in range(n) if (v&a).bit_count()%2==0]
def boundary(n,s):
 s=set(s);return sum((v in s)!=(v+1 in s) for v in range(n-1))
def oracle(n,h,m,rows):
 counts=[0]*(n//h)
 for r in rows:counts[r%(n//h)]+=1
 return sum(min(m,c) for c in counts)
def moving(n,perms,mask):
 a=set(parity(n,mask));bs=[boundary(n,a)]
 for p in perms:a={j for j in range(n) if p[j] in a};bs.append(boundary(n,a))
 rows=sorted(set(range(n))-a);h=1<<mask.bit_length()
 return rows,bs,oracle(n,h,h//2,rows)
def primitive(n,p):
 assert prime_by_trial_division(p) and (p-1)%n==0
 for g in range(2,p):
  w=pow(g,(p-1)//n,p)
  if pow(w,n//2,p)!=1:return w
 raise AssertionError

def rank_f(n,R,C,p):
 if not R or not C:return 0
 w=primitive(n,p);powers=[pow(w,j,p) for j in range(n)]
 return Field(p).rank([[powers[i*j%n] for j in C] for i in R])

def core_certificates():
 src=json.loads((BASE/'sources/EXACT_CERTIFICATES.json').read_text());r=src['nonaffine_256'];n=256
 ps=[affine(c) for c in r['affine_shuffle_columns']];base=moving(n,ps,112)
 assert base[1]==[11,53,43,60] and base[2]==128 and sum(base[1])==167
 changed=[p[:] for p in ps];progress=[]
 for gate in r['toffoli_gate_sequence_in_shuffle_2']:
  changed[2]=compose(changed[2],mcnot(8,gate['controls'],gate['target']))
  R,bs,rank=moving(n,changed,112);progress.append({'boundaries':bs,'rank':rank,'gap':rank-sum(bs)})
 R,bs,rank=moving(n,changed,112);assert R==r['witness']['output_rows'] and bs==[11,53,43,17] and rank==128
 p=changed[2];offset=p[0];linear=affine([p[1<<j]^offset for j in range(8)],offset)
 mismatches=sum(a!=b for a,b in zip(p,linear));assert mismatches==160
 mr=[rank_f(n,R,parity(n,112),p) for p in (12289,65537)];assert mr==[128,128]
 flow=network_bound(n,changed,parity(n,112),R);assert flow==124
 robust=[]
 for ns,r in src['edit_robust'].items():
  n=int(ns);k=r['k'];ps=[affine(c) for c in r['affine_shuffle_columns']];R,bs,rank=moving(n,ps,r['base_input_mask'])
  assert bs==r['base_stage_boundaries'] and sum(bs)==r['base_capacity'] and rank==r['exact_complex_fourier_rank']==n//2
  assert R==[v for v in range(n) if (v&r['base_output_mask']).bit_count()%2]
  edits=[]
  for gate in r['nonlinear_edits']:
   j=gate['shuffle_index'];changed=compose(ps[j],mcnot(k,gate['controls'],gate['target']));edits.append(cycle_rank(changed,ps[j]))
  assert edits==r['edit_ranks']==[n//8]*2
  cap=sum(bs)+sum(edits);assert cap==r['perturbed_network_rank_bound_on_original_endpoint_sets'] and rank-cap==r['strict_gap']>0
  robust.append({'N':n,'baseline_boundaries':bs,'edit_ranks':edits,'rank':rank,'cap':cap,'gap':rank-cap})
 return {'nonaffine_256':{'boundaries':[11,53,43,17],'rank':128,'flow':flow,'active_graph_vertices_excluding_source_sink':4*(8*256-4),'nonaffine_mismatches':mismatches,'modular_ranks':mr,'fixed_mask_progress':progress},'two_Toffoli_robustness':robust}

def rank_oracle_controls():
 parity_count=0;rng=random.Random(17332)
 for k in range(3,7):
  n=1<<k
  for a in range(1,n):
   h=1<<a.bit_length();C=parity(n,a)
   for _ in range(5):
    R=rng.sample(range(n),rng.randrange(n+1));wanted=oracle(n,h,h//2,R)
    for p in (12289,65537):assert rank_f(n,R,C,p)==wanted
    parity_count+=1
 rng=random.Random(15889);universal_count=0
 for k in range(3,7):
  n=1<<k
  for h in (1<<j for j in range(1,k+1)):
   m=h//2
   for _ in range(20):
    flags=[rng.randrange(2) for j in range(m)];E=[j+m*flags[j] for j in range(m)]
    for d in (1<<j for j in range(h.bit_length())):
     counts=[sum(e%d==r for e in E) for r in range(d)];assert max(counts)-min(counts)<=1
    C=[e+h*j for e in E for j in range(n//h)];R=rng.sample(range(n),rng.randrange(n+1));wanted=oracle(n,h,m,R)
    for p in (12289,65537):assert rank_f(n,R,C,p)==wanted
    universal_count+=1
 oldpairs=0
 for k in range(2,8):
  n=1<<k
  for a in range(1,n):
   h=1<<a.bit_length()
   for b in range(1,n):
    R=[v for v in range(n) if (v&b).bit_count()%2]
    wanted=n//(4 if a.bit_length()+b.bit_length()<=k else 2)
    assert oracle(n,h,h//2,R)==wanted;oldpairs+=1
 assert (parity_count,universal_count,oldpairs)==(580,360,21342)
 # Characteristic-zero full spark need not survive a chosen finite field.
 E=[0,1,2,3,4,13,6,7];R=[0,1,2,3,4,6,7,12]
 assert oracle(16,16,8,R)==8
 bad=[rank_f(16,R,E,p) for p in (12289,65537)];assert bad==[7,8]
 return {'parity_arbitrary_row_cases_each_of_two_fields':parity_count,'universal_transversal_cases_each_of_two_fields':universal_count,'parity_pair_formula_cases':oldpairs,'bad_specialization_control':{'complex_rank':8,'modular_ranks':bad,'primes':[12289,65537]}}

def edit_controls():
 count=0;matrix_count=0;rng=random.Random(798)
 for k in range(3,8):
  n=1<<k
  for m in range(1,min(k,4)):
   for _ in range(12):
    cs=rng.sample(range(k),m);t=next(j for j in range(k) if j not in cs);g=mcnot(k,cs,t);wanted=n//(1<<(m+1))
    assert cycle_rank(g,list(range(n)))==wanted;count+=1
    if n<=64:
     mat=[[int(g[i]==j)-int(i==j) for j in range(n)] for i in range(n)]
     for p in (2,12289):assert Field(p).rank(mat)==wanted;matrix_count+=1
 # Fresh actual products; generator zeros and singular stages are allowed.
 product_results=[]
 for p in (12289,65537):
  f=Field(p);n=64;rng=random.Random(9536);stages=[]
  for ell in range(4):
   a,b,c,d,e=[[rng.randrange(1,p) for i in range(n)] for _ in range(5)]
   stages.append([[(a[i]*b[j] if i>j else c[i]*d[j] if i<j else e[i])%p for j in range(n)] for i in range(n)])
  old=stages[0];new=stages[0]
  for ell in range(1,4):
   old=f.mul(stages[ell],old)
   if ell<3:
    perm=mcnot(6,([0,2] if ell==1 else [1,3]),5);new=[new[v] for v in perm]
   new=f.mul(stages[ell],new)
  base=f.rank([row[:32] for row in old[32:]]);edited=f.rank([row[:32] for row in new[32:]])
  defect=f.rank([[(a-b)%p for a,b in zip(r,s)] for r,s in zip(new,old)])
  assert base<=4 and defect<=16 and edited<=base+defect<32 and rank_f(n,list(range(32,64)),list(range(32)),p)==32
  product_results.append({'p':p,'base_cross_rank':base,'edited_cross_rank':edited,'full_defect_rank':defect,'Fourier_rank':32})
 thresholds=[]
 for t in range(1,9):
  for r in range(1,5):
   q=(8*r*t-1).bit_length();k=t*q+1;n=1<<k;bound=r*t*(n//(1<<q)-1)+n//8
   assert bound<n//4;thresholds.append({'t':t,'r':r,'q':q,'first_k':k,'strict_margin':n//4-bound})
 return {'gate_cycle_cases':count,'direct_matrix_gate_cases':matrix_count,'fresh_actual_QS_products':product_results,'uniform_single_Toffoli_thresholds':thresholds}

if __name__=='__main__':
 core=core_certificates();print('Core certificates and maxflow PASS',flush=True)
 ranks=rank_oracle_controls();print('940 two-field oracle cases and 21342 parity pairs PASS',flush=True)
 edits=edit_controls();print('Permutation edits and fresh products PASS',flush=True)
 (BASE/'VERIFIED_RESULTS.json').write_text(json.dumps({'status':'PASS','core':core,'rank_oracles':ranks,'edits':edits,'source_programs_executed':False},indent=2,sort_keys=True)+'\n')
