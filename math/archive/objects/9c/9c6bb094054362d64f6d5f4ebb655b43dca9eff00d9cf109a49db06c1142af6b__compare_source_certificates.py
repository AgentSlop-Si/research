#!/usr/bin/env python3
"""Independently verify certificate data, using ONLY our own arithmetic module."""
from pathlib import Path
import json,sys
from independent_checks import E,ei,edet,erank,augmented,target,cycles,rowskey,domain
root=Path(__file__).resolve().parent
own=json.loads((root/'INDEPENDENT_RESULTS.json').read_text());source=json.loads((root/'source/COMPLETION_SCREEN_RESULTS.json').read_text())['branches'];orders=cycles(5);B=target(5,91)
def decode(vv):return [[E(*z) for z in v] for v in vv]
ownset={};srcset={};count=0
for rec in own['branch_certificates']:
 pair=tuple(rec['pair']);signature=(rowskey(decode(rec['rows'])),rowskey(decode(rec['columns'])));assert signature not in ownset.setdefault(pair,set());ownset[pair].add(signature)
for rec in source:
 pair=rec['first'],rec['second'];pi,tau=[orders[k] for k in pair];u=decode(rec['row_directions']);v=decode(rec['column_directions']);signature=(rowskey(u),rowskey(v));assert signature not in srcset.setdefault(pair,set());srcset[pair].add(signature)
 U=[[E() for j in range(5)] for i in range(5)];V=[[E() for j in range(5)] for i in range(5)]
 for i,(a,b) in enumerate(u):U[i][i]=a;U[i][pi[i]]=b
 for j,(a,b) in enumerate(v):V[j][j]=a;V[tau.index(j)][j]=b
 M,K=augmented(B,U,V);cert=rec['augmented_minor_certificate'];positions=cert['positions'];ids=[5*i+j for i,j in positions];d=edet([M[k] for k in ids]);assert d==E(*cert['determinant']) and d
 rd=[sum(a==i for a,b in positions)-1 for i in range(5)];cd=[sum(b==j for a,b in positions)-1 for j in range(5)];assert rd==cert['row_multidegrees'] and cd==cert['column_multidegrees'];assert min(rd+cd)>=0 and sum(rd)==sum(cd)==6;count+=1
assert ownset==srcset
# Rebuild <=3-quadratic emptiness witnesses from our independently chosen forests.
witnesses=[];distribution={}
for rec in own['order_records']:
 if rec['status']!='ROW_EMPTY':continue
 for pr in rec['component_proofs']:
  qq=pr['quadratics'];roots,_=domain(qq)
  if roots:continue
  first=next(i for i,q in enumerate(qq) if any(q));candidates,_=domain([qq[first]]);selected={first}
  from independent_checks import peval
  for v in candidates:selected.add(next(i for i,q in enumerate(qq) if peval(q,v)))
  assert len(selected)<=3 and not domain([qq[i] for i in selected])[0];distribution[len(selected)]=distribution.get(len(selected),0)+1;witnesses.append({'pair':rec['pair'],'quadratics':[qq[i] for i in sorted(selected)]});break
assert len(witnesses)==384
# Exact cyclotomic arithmetic for the target denominator guard.
G=[1,0,2,2];s=[0]*7
for i,a in enumerate(G):
 for j,b in enumerate(G):s[i+j]+=a*b
for k in range(len(s)-1,3,-1):
 a=s[k]
 for j in range(5):s[k-4+j]-=a
assert s[:4]==[5,0,0,0]
result={'status':'PASS','all_source_branch_sets_equal_independent_sets':True,'source_nonzero_minor_values_verified':count,'source_multidegrees_verified':count,'independent_rejection_witnesses':len(witnesses),'witness_size_distribution':distribution,'characteristic_zero_G_squared':5,'target_denominator_specialization':34,'source_code_executed':False,'row_empty_witnesses':witnesses}
out=Path(sys.argv[1]) if len(sys.argv)>1 else root/'SOURCE_CERTIFICATE_COMPARISON.json';out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='row_empty_witnesses'},indent=2))
