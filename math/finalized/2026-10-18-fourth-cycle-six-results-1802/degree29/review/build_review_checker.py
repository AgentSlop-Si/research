#!/usr/bin/env python3
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent
p=R/'inputs/DEGREE23_review_check.py';s=p.read_text()
changes=[
('Independent degree-23 inert-certificate review. Arithmetic and literal-power method adapted from the byte-bound degree-19 independent reviewer.','Independent degree-29 inert-certificate review. Arithmetic and literal-power method adapted from the byte-bound degree-23 independent reviewer, widened to radix 2^17.'),
('P,D,N=53,23,13','P,D,N=53,29,13'),('HMOD=[5,1]+[0]*21+[1]','HMOD=[8,1]+[0]*27+[1]'),
('Integer convolution, carry-free because 23*52^2 < 2^16.','Integer convolution, carry-free because 29*52^2 = 78416 < 2^17.'),
('<<(16*i)','<<(17*i)'),('>>(16*i))&65535','>>(17*i))&131071'),
('-5u^(k-D)','-8u^(k-D)'),('c[k-D]-=5*c[k]','c[k-D]-=8*c[k]'),
('DEGREE23_LITERAL_CERTIFICATE.json','DEGREE29_LITERAL_CERTIFICATE.json'),
('083ec297a3fde29babcf2fe7a59abe9bc2c531d9ae91461a55b863b9b8858a4e','44a1ad9e58b847444e13d6fe72a6b90dc18f4e763f0e10377b973f25a9bf221c'),
('assert D*52**2 < 65536','assert 2**16 <= D*52**2 < 2**17'),
('random.Random(202610181509)','random.Random(202610181754)'),
('sufficient=[2,3,5,7,11,13,17,19,23];modulus=math.prod(sufficient);assert modulus==223092870','sufficient=[2,3,5,7,11,13,17,19,23,29];modulus=math.prod(sufficient);assert modulus==6469693230'),
('math.gcd(d,modulus)==1)==29','math.gcd(d,modulus)==1)==31'),
("'next_unclassified_degree':29,'next_degree_field_order':P**29,'next_degree_order_bits':(P**29).bit_length(),'next_degree_exceeds_uint128':P**29>=2**128","'next_unclassified_degree':31,'next_degree_field_order':P**31,'next_degree_order_bits':(P**31).bit_length(),'next_degree_exceeds_uint128':P**31>=2**128"),
('Independent carry-free integer-convolution','Independent carry-free 17-bit integer-convolution')]
for old,new in changes:
 assert old in s,old;s=s.replace(old,new)
needle=' for a,b in pairs:assert mul(a,b)==padded(pdiv(pm(list(a),list(b)),HMOD)[1])'
s=s.replace(needle," pairs.append(((52,)*D,(52,)*D))\n"+needle)
(R/'review_check.py').write_text(s)
out={'prior_source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'active_source_sha256':hashlib.sha256(s.encode()).hexdigest(),'source_changes':changes,'added_worst_case_dense_differential':True}
(R/'CHECKER_ADAPTATION.json').write_text(json.dumps(out,indent=2)+'\n')
