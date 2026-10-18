#!/usr/bin/env python3
"""Independent packing-boundary audit before support search; standard library only.
The active literal checker uses ordinary convolution. This also makes the inherited
reviewer's radix boundary explicit, verifies the 17-bit replacement against general
long division, and rejects dense 16-bit corruption and an unsafe carry assertion.
"""
from pathlib import Path
import json,random,hashlib
R=Path(__file__).resolve().parent;P=53;D=29;MOD=[8,1]+[0]*27+[1]
def conv(a,b):
 z=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):z[i+j]+=x*y
 return z
def generic_reduce(c):
 c=[x%P for x in c]
 while len(c)>=len(MOD):
  lead=c[-1]*pow(MOD[-1],-1,P)%P;off=len(c)-len(MOD)
  for j,v in enumerate(MOD):c[off+j]=(c[off+j]-lead*v)%P
  c.pop()
 return tuple(c+[0]*(D-len(c)))
def packedconv(a,b,bits):
 aa=sum(x<<(bits*i) for i,x in enumerate(a));bb=sum(x<<(bits*i) for i,x in enumerate(b));c=aa*bb
 return [(c>>(bits*i))&((1<<bits)-1) for i in range(2*D-1)]
def packed(a,b,bits):
 c=packedconv(a,b,bits)
 for k in range(2*D-2,D-1,-1):c[k-D+1]-=c[k];c[k-D]-=8*c[k]
 return tuple(x%P for x in c[:D])
bound=D*(P-1)**2;assert bound==78416 and 2**16<=bound<2**17
boundary=[]
for d in [24,25,29]:
 a=[52]*d;c=conv(a,a);low=packedconv(a,a,16)[:2*d-1]
 boundary.append({'degree':d,'max_coefficient':max(c),'radix16_exact':c==low})
assert boundary[0]['radix16_exact'] and not boundary[1]['radix16_exact'] and not boundary[2]['radix16_exact']
a=[52]*D;dense=conv(a,a);bad=packedconv(a,a,16);good=packedconv(a,a,17)
assert good==dense and bad!=dense and packed(a,a,16)!=generic_reduce(dense)
unsafe_guard_rejected=False
try:assert bound<2**16
except AssertionError:unsafe_guard_rejected=True
assert unsafe_guard_rejected
rng=random.Random(202610181745);basis=[tuple(int(i==j) for i in range(D)) for j in range(D)]
pairs=[(a,b) for a in basis for b in basis]+[(tuple(rng.randrange(P) for _ in range(D)),tuple(rng.randrange(P) for _ in range(D))) for _ in range(100)]+[(tuple([52]*D),tuple([52]*D))]
for a,b in pairs:
 assert packedconv(a,b,17)==conv(a,b)
 assert packed(a,b,17)==generic_reduce(conv(a,b))
out={'verdict':'PASS','degree':D,'modulus_ascending':MOD,'ordinary_convolution_coefficient_bound':bound,'minimum_safe_slot_bits':17,'selected_literal_checker':'ordinary coefficient convolution; no packed-integer carry risk','tests_before_support_search':True,'boundary_examples':boundary,'basis_pair_tests':D*D,'dense_random_pair_tests':100,'worst_case_dense_pair_tests':1,'radix17_matches_ordinary_convolution_and_generic_long_division':True,'negative_controls':{'unsafe_radix16_carry_assertion_rejected':unsafe_guard_rejected,'radix16_raw_convolution_mismatch_detected':True,'radix16_reduced_field_product_mismatch_detected':True},'worst_case_raw_coefficient_mismatch_indices':[i for i in range(2*D-1) if dense[i]!=bad[i]],'radix16_wrong_reduced_product':packed([52]*D,[52]*D,16),'ordinary_correct_reduced_product':generic_reduce(dense),'signed_cpp_reduction_bound':(1+1+8)*bound,'signed_cpp_int32_safe':(1+1+8)*bound<2**31,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(R/'CONVOLUTION_BOUNDARY_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
