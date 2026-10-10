"""Independent all-order family counts by forward matching enumeration.
Does not run or import the reviewer or source programs.
"""
import json,pathlib,itertools,time,hashlib
import numpy as np
import sympy as sp
R=pathlib.Path(__file__).resolve().parent
L=json.loads((R/'topology_11.json').read_text())['layers']
start=time.monotonic();stats=[];certs=[];count_hash=hashlib.sha256()
for k in range(1,12):
 subs=list(itertools.combinations(range(11),k));idx={sum(1<<x for x in s):i for i,s in enumerate(subs)};N=len(subs)
 matrices=[]
 for layer in L:
  choices=[[r for r,c in layer if c==s] for s in range(11)]
  M=np.zeros((N,N),dtype=np.int64)
  for j,S in enumerate(subs):
   # Expand each input's possible destinations, carrying the used destination mask.
   states={0:1}
   for col in S:
    new={}
    for used,count in states.items():
     for row in choices[col]:
      bit=1<<row
      if not used&bit:new[used|bit]=min(2,new.get(used|bit,0)+count)
    states=new
   for mask,count in states.items():M[idx[mask],j]=count
  matrices.append(M)
 # Integer maxima before each cap are ≤4*N, so int64 cannot overflow.
 BA=np.minimum(matrices[1]@matrices[0],2)
 CBA=np.minimum(matrices[2]@BA,2)
 assert int(CBA.min())>=0 and int(CBA.max())<=2
 single=np.argwhere(CBA==1)
 stats.append({'order':k,'minor_count':N*N,'zero_family':int(np.sum(CBA==0)),'one_family':len(single),'at_least_two_families':int(np.sum(CBA==2))})
 for i,j in single:certs.append({'order':k,'rows':list(subs[i]),'cols':list(subs[j]),'required_valuation':k*(k-1)//2})
 count_hash.update(CBA.tobytes())
 print(stats[-1],flush=True)
review=json.loads((R.parent.parent/'research_cycle_1735/pole_escape_review/ALL_MONOMIAL_MINORS.json').read_text())
rc={(x['order'],tuple(x['rows']),tuple(x['cols'])):x for x in review['certificates']}
assert len(rc)==len(certs)==26
rows=[];rhs=[]
for x in certs:
 y=rc[x['order'],tuple(x['rows']),tuple(x['cols'])]
 row=[0]*99
 for e in y['edges']:row[e]+=1
 # Independently verify that these edges form a k-disjoint matching in each layer,
 # with the claimed outer endpoint sets and matching intermediate endpoint sets.
 parts=[]
 for z in range(3):
  edges=[L[z][e-33*z] for e in y['edges'] if 33*z<=e<33*(z+1)]
  assert len(edges)==x['order']
  outs=[r for r,c in edges];ins=[c for r,c in edges]
  assert len(set(outs))==len(outs) and len(set(ins))==len(ins)
  parts.append((set(outs),set(ins)))
 assert parts[0][1]==set(x['cols']) and parts[2][0]==set(x['rows'])
 assert parts[0][0]==parts[1][1] and parts[1][0]==parts[2][1]
 rows.append(row);rhs.append(x['required_valuation'])
A=sp.Matrix(rows);rank=A.rank();aug=A.row_join(sp.Matrix(rhs)).rank()
assert rank==aug==26
out={'status':'PASS','method':'Forward destination-set matching enumeration with counts capped at2; exact integer matrix products capped at2','all_minor_count':sum(x['minor_count'] for x in stats),'statistics':stats,'unique_families':certs,'rank':rank,'augmented_rank':aug,'reviewer_certificates_checked':26,'runtime_seconds':time.monotonic()-start,'capped_matrix_checksum':count_hash.hexdigest(),'source_or_reviewer_programs_run_or_imported':False}
(R/'all_order_monomial_verification.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS',out['all_minor_count'],rank,aug,out['runtime_seconds'],flush=True)
