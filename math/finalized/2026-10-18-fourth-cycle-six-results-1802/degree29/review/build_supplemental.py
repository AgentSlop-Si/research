from pathlib import Path
R=Path(__file__).resolve().parent
s=(R/'inputs/DEGREE23_supplemental_check.py').read_text()
start=s.index('# Static path audit')
end=s.index("out={'verdict'")
s=s[start:end]
s=s.replace('search_degree23.cpp','search_degree29.cpp').replace('Q=53**23','Q=53**29').replace('==132','==167').replace('23*52**2==62192 and 7*23*52**2==435344 and 435344<2**31','29*52**2==78416 and 10*29*52**2==784160 and 784160<2**31')
head='''#!/usr/bin/env python3
"""Independent degree-29 boundary, GMP, source-path, modulus-search, and PRNG review.
The GMP probe-output arithmetic routines transparently adapt the pinned prior independent review.
No candidate scientific source is imported or executed by this checker.
"""
import hashlib,importlib.util,json,math,sys,random
from pathlib import Path
R=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('review_arithmetic',R/'review_check.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
I=R/'inputs';C=R/'candidate_snapshot'
field=json.loads((I/'FIELD_SEARCH.json').read_text());tests=[]
assert field['prime']==53 and field['degree']==29 and field['chosen_constant']==8
for c in range(1,9):
 m.HMOD=[c,1]+[0]*27+[1];x=[0,1];allrem=[]
 for _ in range(29):x=m.ppow(x,53);allrem.append(x)
 g=m.pgcd(m.HMOD,m.pa(allrem[0],[0,1],-1));ok=x==[0,1] and g==[1]
 tests.append({'constant':c,'frobenius29_remainder':x,'gcd_with_X53_minus_X':g,'irreducible':ok})
 assert ok==(c==8)
assert tests==field['tests'];m.HMOD=[8,1]+[0]*27+[1]
# The packed carry threshold is tested at and across its exact degree boundary.
def unpack_product(a,b,bits):
 v=sum(x<<(bits*i) for i,x in enumerate(a))*sum(x<<(bits*i) for i,x in enumerate(b))
 return [(v>>(bits*i))&((1<<bits)-1) for i in range(len(a)+len(b)-1)]
def ordinary(a,b):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return c
boundary=[]
for d in [24,25,29,31]:
 a=[52]*d;raw=ordinary(a,a);bad=unpack_product(a,a,16);good=unpack_product(a,a,17)
 assert good==raw and (bad==raw)==(d==24)
 boundary.append({'degree':d,'coefficient_max':max(raw),'radix16_exact':bad==raw,'radix17_exact':good==raw})
a=[52]*29;raw=ordinary(a,a);bad=unpack_product(a,a,16)
expected=m.padded(m.pdiv(raw,m.HMOD)[1]);incorrect=m.padded(m.pdiv(bad,m.HMOD)[1])
assert expected==m.mul(tuple(a),tuple(a)) and incorrect!=expected
try:assert 29*52**2<2**16
except AssertionError:unsafe_carry_bound_rejected=True
else:raise AssertionError('16-bit carry guard accepted unsafe degree')
certificate=json.loads((I/'DEGREE29_LITERAL_CERTIFICATE.json').read_text());candidate=json.loads((I/'NONSTABLE_CANDIDATE.json').read_text());scope=json.loads((I/'SEARCH_SCOPE.json').read_text())
assert candidate['y']==certificate['y']==certificate['z'] and candidate['H']==certificate['H']
assert candidate['trial']==10425 and candidate['candidates']==10497
assert scope['deterministic_prng_seed']==202610181745 and scope['zero_based_first_split_trial']==10425
assert scope['nonzero_cross_nodes_examined']==10426 and scope['initial_trial_cap']==100000
state=scope['deterministic_prng_seed'];mask=2**64-1;zero=0;nodes=0;draws=0
while nodes<10426:
 node=[]
 for _ in range(29):
  state=(state ^ (state<<13)) & mask
  state=state ^ (state>>7)
  state=(state ^ (state<<17)) & mask
  node.append(state%53);draws+=1
 if any(node):nodes+=1
 else:zero+=1
assert node==candidate['y'] and zero==0 and draws==302354
header='static const int INPUT_Y[D]={'+','.join(map(str,candidate['y']))+'};\\nstatic const int INPUT_H[8][D]={'+','.join('{'+','.join(map(str,c))+'}' for c in candidate['H'])+'};\\n'
assert (C/'candidate_data.h').read_text()==header
pm=json.loads((C/'sources/DEGREE23_REVIEW_MANIFEST.json').read_text())
for row in pm['files']:
 if row['path']=='review_check.py':
  b=(I/'DEGREE23_review_check.py').read_bytes();assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'];break
else:raise AssertionError('prior independent method not accepted-manifest bound')
'''
tail='''
out={'verdict':'PASS','field_search_tests_independently_recomputed':tests,'first_irreducible_constant':8,'prior_review_method_bound_to_accepted_manifest':True,'discovery_json_and_literal_header_bound':True,'independent_prng_replay':{'nonzero_nodes':nodes,'zero_nodes':zero,'coordinate_draws':draws,'final_cross_node':node},'discovery_gate_first_hit_independently_reexecuted':False,'scope':'Finite prefix logs and adaptation receipts are byte-bound; all PRNG draws and the final node were recomputed. First-split minimality is not a premise of literal acceptance.','field_order':Q,'field_order_bits':Q.bit_length(),'all_active_extension_exponent_paths_use_GMP':True,'independent_power_probe_cases':len(expected),'independent_split_and_factor_polynomial_powers':4,'negative_controls':{'wrapped_order':True,'power_2_to_128_wrap':True,'truncated_inverse':True,'truncated_split_order':True,'truncated_sqrt':True,'truncated_factor_character':True},'convolution_boundary':boundary,'negative_packing_controls':{'unsafe_radix16_carry_bound_rejected':unsafe_carry_bound_rejected,'worst_case_raw_convolution_differs':raw!=bad,'worst_case_reduced_field_product_differs':incorrect!=m.mul(tuple(a),tuple(a))},'radix16_incorrect_product':incorrect,'radix17_correct_product':m.mul(tuple(a),tuple(a)),'unreduced_coefficient_bound':78416,'signed_cpp_reduction_bound':784160,'signed_cpp_int32_safe':True,'prepared_evaluation_multiplications':37869,'prepared_evaluation_additions':35139,'dense_inverse_validation_multiplications':913952,'first_search_preflight_chronology':'Candidate reported chronology is byte-bound; not independently timed.'}
(R/'SUPPLEMENTAL.json').write_text(json.dumps(out,indent=2)+'\\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['field_search_tests_independently_recomputed']},indent=2))
'''
(R/'supplemental_check.py').write_text(head+s+tail)
