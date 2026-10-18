#!/usr/bin/env python3
"""Independent metadata, field-search, PRNG, and implementation-width checks."""
import hashlib,importlib.util,json,math,sys
from pathlib import Path
R=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('review_arithmetic',R/'review_check.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
I=R/'inputs';C=R.parent/'candidate'
field=json.loads((I/'FIELD_SEARCH.json').read_text());tests=[]
assert field['prime']==53 and field['degree']==19 and field['chosen_constant']==12
for c in range(1,13):
 m.HMOD=[c,1]+[0]*17+[1];x=[0,1];allrem=[]
 for _ in range(19):x=m.ppow(x,53);allrem.append(x)
 g=m.pgcd(m.HMOD,m.pa(allrem[0],[0,1],-1));ok=x==[0,1] and g==[1]
 tests.append({'constant':c,'frobenius19_remainder':x,'gcd_with_X53_minus_X':g,'irreducible':ok})
 assert ok==(c==12)
assert tests==field['tests'];m.HMOD=[12,1]+[0]*17+[1]
certificate=json.loads((I/'DEGREE19_LITERAL_CERTIFICATE.json').read_text());candidate=json.loads((I/'NONSTABLE_CANDIDATE.json').read_text());scope=json.loads((I/'SEARCH_SCOPE.json').read_text())
assert candidate['y']==certificate['y']==certificate['z'] and candidate['H']==certificate['H']
assert candidate['trial']==3411 and candidate['candidates']==3405
assert scope['seed']==202610181330 and scope['executed_trial_indices_inclusive']==[0,3411]
assert scope['cross_nodes_executed']==3412 and scope['zero_cross_nodes_skipped']==0
state=scope['seed'];mask=2**64-1;zero=0;nodes=[];draws=0
while len(nodes)<3412:
 node=[]
 for _ in range(19):
  state=(state ^ (state<<13)) & mask
  state=state ^ (state>>7)
  state=(state ^ (state<<17)) & mask
  node.append(state%53);draws+=1
 if any(node):nodes.append(node)
 else:zero+=1
assert nodes[-1]==candidate['y'] and zero==0 and draws==64828
header='static const int INPUT_Y[D]={'+','.join(map(str,candidate['y']))+'};\nstatic const int INPUT_H[8][D]={'+','.join('{'+','.join(map(str,c))+'}' for c in candidate['H'])+'};\n'
assert (C/'candidate_data.h').read_text()==header
# Bind inherited remote response contents to the presently reviewed local source bytes.
receipts=json.loads((I/'DEGREE17_REMOTE_SOURCE_RECEIPTS.json').read_text());responses=json.loads((I/'DEGREE17_REMOTE_SOURCE_RESPONSES.json').read_text())
assert len(receipts)==len(responses)==3
remote_bindings=[]
for receipt,response in zip(receipts,responses):
 b=response['content'].encode();p=C/receipt['byte_identical_local_path']
 assert b==p.read_bytes() and len(b)==receipt['bytes']
 assert hashlib.sha256(b).hexdigest()==receipt['sha256']
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==receipt['git_blob_sha']
 remote_bindings.append({'url':receipt['url'],'sha256':receipt['sha256'],'check':'Prior fetched response matches present local bytes; no new remote read.'})
order=53**19;future=53**23
assert order.bit_length()==109 and order+3<2**128
assert future.bit_length()==132 and future>=2**128
assert 19*52**2==51376 and 14*19*52**2==719264 and 719264<2**31
assert order%8==5 and 23*23%53==52
assert 208*169+208*13+13==37869 and 208*156+13*207==35139
assert 416*13**3==913952
out={'verdict':'PASS','field_search_tests_independently_recomputed':tests,'first_irreducible_constant':12,'source_receipts_revalidated':remote_bindings,'discovery_json_and_literal_header_bound':True,'independent_prng_replay':{'nonzero_nodes':len(nodes),'zero_nodes':zero,'coordinate_draws':draws,'final_cross_node':nodes[-1]},'discovery_gate_first_hit_independently_reexecuted':False,'scope':'Finite prefix logs are byte-bound; all PRNG draws and the final node were recomputed. The first split claim is not a premise of literal acceptance.','field_order':order,'field_order_bits':order.bit_length(),'uint128_current_safe':True,'coefficient_bound':719264,'coefficient_bound_int32_safe':True,'prepared_evaluation_multiplications':37869,'prepared_evaluation_additions':35139,'dense_inverse_validation_multiplications':913952,'next_degree':23,'next_degree_field_order':future,'next_degree_bits':future.bit_length(),'next_degree_requires_wider_than_uint128':True}
(R/'SUPPLEMENTAL.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['field_search_tests_independently_recomputed','source_receipts_revalidated']},indent=2))
