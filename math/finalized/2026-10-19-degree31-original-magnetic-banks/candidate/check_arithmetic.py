#!/usr/bin/env python3
"""Independent Python arbitrary-integer and generic polynomial arithmetic checks.
This consumes only inert C++ output; it imports no discovery or literal checker.
Must pass before any degree-31 support search.
"""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parent;P=53;D=31;Q=P**D;MOD=[11,2]+[0]*29+[1];MASK=2**128-1
probe=json.loads((R/'ARITHMETIC_PROBE.json').read_text())
def trim(x):
 x=[i%P for i in x]
 while len(x)>1 and x[-1]==0:x.pop()
 return x
def rem(a,b):
 a=trim(a);b=trim(b)
 while len(a)>=len(b) and a!=[0]:
  c=a[-1]*pow(b[-1],-1,P)%P;off=len(a)-len(b)
  for i,v in enumerate(b):a[off+i]-=c*v
  a=trim(a)
 return a
def mul(a,b):
 z=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):z[i+j]+=x*y
 z=rem(z,MOD);return z+[0]*(D-len(z))
Z=[0]*D;O=[1]+[0]*(D-1)
def add(a,b):return [(x+y)%P for x,y in zip(a,b)]
def sub(a,b):return [(x-y)%P for x,y in zip(a,b)]
def power(a,e):
 z=O
 while e:
  if e%2:z=mul(z,a)
  e//=2
  if e:a=mul(a,a)
 return z
def ptr(a):
 while len(a)>1 and a[-1]==Z:a.pop()
 return a
def pmulmod(a,b,h):
 z=[Z]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):z[i+j]=add(z[i+j],mul(x,y))
 while len(z)>=len(h):
  c=z[-1];off=len(z)-len(h)
  for j,v in enumerate(h):z[off+j]=sub(z[off+j],mul(c,v))
  z.pop()
 return ptr(z)
def ppow(a,e,h):
 z=[O]
 while e:
  if e%2:z=pmulmod(z,a,h)
  e//=2
  if e:a=pmulmod(a,a,h)
 return z
def peval(h,a):
 z=Z
 for c in h[::-1]:z=add(mul(z,a),c)
 return z
assert int(probe['order'])==Q and probe['bits']==Q.bit_length()==178
assert int(probe['wrapped_order'])==Q&MASK and int(probe['wrapped_order'])!=Q
A=probe['a'];B=probe['b'];assert mul(A,B)==probe['a_times_b']
assert power(A,Q-2)==probe['inverse'] and mul(A,probe['inverse'])==O
expected=[2**128-1,2**128,2**128+1,2**127-1,2**127,Q-2,Q-1,Q,(Q+3)//8,(Q-1)//2]
assert [int(x['exponent']) for x in probe['power_cases']]==expected
for row in probe['power_cases']:assert power(A,int(row['exponent']))==row['value']
H=probe['split_polynomial'];assert H[-1]==O and len(H)==8
roots=[add(A,[j]+[0]*(D-1)) for j in range(1,8)]
assert len({tuple(x) for x in roots})==7 and all(peval(H,a)==Z for a in roots)
for key,exp in [('exact_split',Q),('wrapped_split',Q&MASK)]:assert ppow([Z,O],exp,H)==probe[key]
assert probe['exact_split']==[Z,O] and probe['wrapped_split']!=[Z,O]
for key,exp in [('exact_factor_power',(Q-1)//2),('truncated_factor_power',((Q-1)//2)&MASK)]:assert ppow(probe['factor_base'],exp,H)==probe[key]
characters=[peval(probe['exact_factor_power'],a) for a in roots]
assert all(mul(v,v)==O for v in characters)
truncated_characters=[peval(probe['truncated_factor_power'],a) for a in roots]
assert any(mul(v,v)!=O for v in truncated_characters)
assert mul(probe['exact_sqrt'],probe['exact_sqrt'])==probe['square']
assert mul(probe['truncated_sqrt'],probe['truncated_sqrt'])!=probe['square']
assert mul(A,probe['truncated_inverse'])!=O
# Independent falsification: wrapping 2^128 to zero changes the powering value.
assert power(A,2**128)!=power(A,0)
assert power(A,Q)!=power(A,Q&MASK)
# Every order-derived exponent is above 128 bits, including the sqrt exponent.
for k,e in [('inverse',Q-2),('sqrt',(Q+3)//8),('factor',(Q-1)//2)]:
 assert e>MASK and int(probe['exponent_low128'][k])==e&MASK
receipt={'verdict':'PASS','degree':D,'field_order':str(Q),'field_order_bits':Q.bit_length(),'cpp_integer_backend':'GMP mpz_class, arbitrary precision','gmp_version':probe['gmp_version'],'python_backend':'unbounded Python int, generic prime-polynomial long division','exact_exponents':[str(e) for e in expected],'power_cases':len(expected),'field_product_and_inverse':True,'seven_known_roots_split':True,'factor_character_values_valid':True,'negative_controls':{'wrapped_order_detected':True,'power_2_to_128_wrap_detected':True,'inverse_exponent_truncation_detected':True,'splitting_order_truncation_detected':True,'sqrt_exponent_truncation_detected':True,'factor_exponent_truncation_detected':True},'probe_sha256':hashlib.sha256((R/'ARITHMETIC_PROBE.json').read_bytes()).hexdigest(),'check_completed_before_support_search':True}
(R/'ARITHMETIC_CHECK.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
