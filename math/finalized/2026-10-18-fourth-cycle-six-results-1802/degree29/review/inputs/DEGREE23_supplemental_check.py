#!/usr/bin/env python3
"""Independent field-search, metadata, source-chain, and GMP boundary-output checks."""
import hashlib,importlib.util,json,math,sys
from pathlib import Path
R=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('review_arithmetic',R/'review_check.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
I=R/'inputs';C=R/'candidate_snapshot'
field=json.loads((I/'FIELD_SEARCH.json').read_text());tests=[]
assert field['prime']==53 and field['degree']==23 and field['chosen_constant']==5
for c in range(1,6):
 m.HMOD=[c,1]+[0]*21+[1];x=[0,1];allrem=[]
 for _ in range(23):x=m.ppow(x,53);allrem.append(x)
 g=m.pgcd(m.HMOD,m.pa(allrem[0],[0,1],-1));ok=x==[0,1] and g==[1]
 tests.append({'constant':c,'frobenius23_remainder':x,'gcd_with_X53_minus_X':g,'irreducible':ok})
 assert ok==(c==5)
assert tests==field['tests'];m.HMOD=[5,1]+[0]*21+[1]
certificate=json.loads((I/'DEGREE23_LITERAL_CERTIFICATE.json').read_text());candidate=json.loads((I/'NONSTABLE_CANDIDATE.json').read_text());scope=json.loads((I/'SEARCH_SCOPE.json').read_text())
assert candidate['y']==certificate['y']==certificate['z'] and candidate['H']==certificate['H']
assert candidate['trial']==675 and candidate['candidates']==676
assert scope['seed']==202610181502 and scope['first_split_trial_zero_based']==675
assert scope['nonzero_cross_nodes_through_hit']==676 and scope['declared_trial_cap']==100000
state=scope['seed'];mask=2**64-1;zero=0;nodes=[];draws=0
while len(nodes)<676:
 node=[]
 for _ in range(23):
  state=(state ^ (state<<13)) & mask
  state=state ^ (state>>7)
  state=(state ^ (state<<17)) & mask
  node.append(state%53);draws+=1
 if any(node):nodes.append(node)
 else:zero+=1
assert nodes[-1]==candidate['y'] and zero==0 and draws==15548
header='static const int INPUT_Y[D]={'+','.join(map(str,candidate['y']))+'};\nstatic const int INPUT_H[8][D]={'+','.join('{'+','.join(map(str,c))+'}' for c in candidate['H'])+'};\n'
assert (C/'candidate_data.h').read_text()==header
receipts=json.loads((I/'DEGREE17_REMOTE_SOURCE_RECEIPTS.json').read_text());responses=json.loads((I/'DEGREE17_REMOTE_SOURCE_RESPONSES.json').read_text())
assert len(receipts)==len(responses)==3
remote_bindings=[]
for receipt,response in zip(receipts,responses):
 b=response['content'].encode();p=C/receipt['byte_identical_local_path']
 assert b==p.read_bytes() and len(b)==receipt['bytes']
 assert hashlib.sha256(b).hexdigest()==receipt['sha256']
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==receipt['git_blob_sha']
 remote_bindings.append({'url':receipt['url'],'sha256':receipt['sha256'],'check':'Prior fetched response matches present local bytes; no new remote read.'})
# Prior independent method is bound to the accepted degree-19 review manifest.
pm=json.loads((C/'sources/DEGREE19_REVIEW_MANIFEST.json').read_text())
for row in pm['files']:
 if row['path']=='review_check.py':
  b=(I/'DEGREE19_review_check.py').read_bytes();assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'];break
else:raise AssertionError('prior review method missing from accepted manifest')
# Static path audit plus independently recomputed inert C++ probe values.
s=(C/'search_degree23.cpp').read_text();v=(C/'verify_literal.cpp').read_text()
for token in ['using Big=mpz_class;','const Big ORDER=','F power(Big e)','Poly powmod(Poly x,Big e','power(ORDER-2)','powmod({F(0),F(1)},ORDER,h)','d.power((ORDER+3)/8)']:assert token in s
assert 'powmod(r,(ORDER-1)/2,h)' in v
assert not any(t in s+v for t in ['__uint128','__int128','get_ui','get_si','get_d'])
Q=53**23;M=2**128-1;Z=m.Z;O=m.O
assert Q.bit_length()==132 and Q%8==5 and 23*23%53==52
assert 23*52**2==62192 and 7*23*52**2==435344 and 435344<2**31
assert 208*169+208*13+13==37869 and 208*156+13*207==35139 and 416*13**3==913952
p=json.loads((I/'ARITHMETIC_PROBE.json').read_text())
assert int(p['order'])==Q and p['bits']==132 and int(p['wrapped_order'])==Q&M
A=tuple(p['a']);B=tuple(p['b'])
assert m.mul(A,B)==tuple(p['a_times_b']) and m.inv(A)==tuple(p['inverse'])
expected=[2**128-1,2**128,2**128+1,2**127-1,2**127,Q-2,Q-1,Q,(Q+3)//8,(Q-1)//2]
assert [int(row['exponent']) for row in p['power_cases']]==expected
for row in p['power_cases']:assert m.powf(A,int(row['exponent']))==tuple(row['value'])
def polytrim(a):
 while len(a)>1 and a[-1]==Z:a.pop()
 return a
def polymulmod(a,b,h):
 c=[Z]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]=m.add(c[i+j],m.mul(x,y))
 while len(c)>=len(h):
  lead=c[-1];k=len(c)-len(h)
  for i,x in enumerate(h):c[k+i]=m.sub(c[k+i],m.mul(lead,x))
  assert c[-1]==Z;c.pop()
 return polytrim(c)
def polypow(a,n,h):
 result=[O]
 while n:
  if n&1:result=polymulmod(result,a,h)
  a=polymulmod(a,a,h);n>>=1
 return result
def evalpoly(a,x):
 r=Z
 for c in a[::-1]:r=m.add(m.mul(r,x),c)
 return r
H=list(map(tuple,p['split_polynomial']));roots=[m.add(A,m.const(j)) for j in range(1,8)]
assert len(H)==8 and H[-1]==O and len(set(roots))==7 and all(evalpoly(H,x)==Z for x in roots)
for key,e in [('exact_split',Q),('wrapped_split',Q&M)]:assert polypow([Z,O],e,H)==list(map(tuple,p[key]))
assert list(map(tuple,p['exact_split']))==[Z,O] and list(map(tuple,p['wrapped_split']))!=[Z,O]
for key,e in [('exact_factor_power',(Q-1)//2),('truncated_factor_power',((Q-1)//2)&M)]:assert polypow(list(map(tuple,p['factor_base'])),e,H)==list(map(tuple,p[key]))
characters=[evalpoly(list(map(tuple,p['exact_factor_power'])),x) for x in roots]
badcharacters=[evalpoly(list(map(tuple,p['truncated_factor_power'])),x) for x in roots]
assert all(m.mul(x,x)==O for x in characters) and any(m.mul(x,x)!=O for x in badcharacters)
assert m.mul(tuple(p['exact_sqrt']),tuple(p['exact_sqrt']))==tuple(p['square'])
assert m.mul(tuple(p['truncated_sqrt']),tuple(p['truncated_sqrt']))!=tuple(p['square'])
assert m.mul(A,tuple(p['truncated_inverse']))!=O
assert m.powf(A,2**128)!=O and m.powf(A,Q)!=m.powf(A,Q&M)
for key,e in [('inverse',Q-2),('sqrt',(Q+3)//8),('factor',(Q-1)//2)]:
 assert e>M and int(p['exponent_low128'][key])==e&M
# Independently reproduce truncated inverse and square-root output as well.
assert m.powf(A,(Q-2)&M)==tuple(p['truncated_inverse'])
for key,e in [('exact_sqrt',(Q+3)//8),('truncated_sqrt',((Q+3)//8)&M)]:
 val=m.powf(tuple(p['square']),e)
 if m.mul(val,val)!=tuple(p['square']):val=m.sc(val,23)
 assert val==tuple(p[key])
out={'verdict':'PASS','field_search_tests_independently_recomputed':tests,'first_irreducible_constant':5,'source_receipts_revalidated':remote_bindings,'prior_review_method_bound_to_accepted_manifest':True,'discovery_json_and_literal_header_bound':True,'independent_prng_replay':{'nonzero_nodes':len(nodes),'zero_nodes':zero,'coordinate_draws':draws,'final_cross_node':nodes[-1]},'discovery_gate_first_hit_independently_reexecuted':False,'scope':'Finite prefix logs are byte-bound; all PRNG draws and the final node were recomputed. The first split claim is not a premise of literal acceptance.','field_order':Q,'field_order_bits':Q.bit_length(),'all_active_extension_exponent_paths_use_GMP':True,'independent_power_probe_cases':len(expected),'independent_split_and_factor_polynomial_powers':4,'negative_controls':{'wrapped_order':True,'power_2_to_128_wrap':True,'truncated_inverse':True,'truncated_split_order':True,'truncated_sqrt':True,'truncated_factor_character':True},'coefficient_bound':435344,'coefficient_bound_int32_safe':True,'prepared_evaluation_multiplications':37869,'prepared_evaluation_additions':35139,'dense_inverse_validation_multiplications':913952,'first_search_preflight_chronology':'Candidate reported chronology is byte-bound; not independently timed.'}
(R/'SUPPLEMENTAL.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['field_search_tests_independently_recomputed','source_receipts_revalidated']},indent=2))
