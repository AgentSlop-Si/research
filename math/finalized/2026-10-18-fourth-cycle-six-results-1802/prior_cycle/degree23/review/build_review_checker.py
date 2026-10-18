#!/usr/bin/env python3
"""Transparent adaptation of the prior independent review method, not candidate code."""
from pathlib import Path
import hashlib
R=Path(__file__).resolve().parent
p=R/'inputs/DEGREE19_review_check.py'
s=p.read_text();source_sha=hashlib.sha256(p.read_bytes()).hexdigest()
assert source_sha=='3e86869cfd6c61af8767a52f989719e88078b902eb339d296fe45be5f67618f1'
replacements=[
 ('degree-19 inert-certificate review','degree-23 inert-certificate review'),
 ('degree-17 independent reviewer','degree-19 independent reviewer'),
 ('P,D,N=53,19,13','P,D,N=53,23,13'),
 ('HMOD=[12,1]+[0]*17+[1]','HMOD=[5,1]+[0]*21+[1]'),
 ('19*52^2','23*52^2'),
 ('-12u^(k-D)','-5u^(k-D)'),
 ('c[k-D]-=12*c[k]','c[k-D]-=5*c[k]'),
 ('DEGREE19_LITERAL_CERTIFICATE.json','DEGREE23_LITERAL_CERTIFICATE.json'),
 ('b10199e01e9e7775c78bf34b6cac41ce8d1e90280a013f0a2b21b4c1dcd9a09e','083ec297a3fde29babcf2fe7a59abe9bc2c531d9ae91461a55b863b9b8858a4e'),
 ('202610181335','202610181509'),
 ('sufficient=[2,3,5,7,11,13,17,19]','sufficient=[2,3,5,7,11,13,17,19,23]'),
 ('modulus==9699690','modulus==223092870'),
 ('math.gcd(d,modulus)==1)==23','math.gcd(d,modulus)==1)==29'),
 ("'next_unclassified_degree':23,'next_degree_field_order':P**23,'next_degree_order_bits':(P**23).bit_length(),'next_degree_exceeds_uint128':P**23>=2**128", "'next_unclassified_degree':29,'next_degree_field_order':P**29,'next_degree_order_bits':(P**29).bit_length(),'next_degree_exceeds_uint128':P**29>=2**128")]
for a,b in replacements:
 assert a in s,a
 s=s.replace(a,b)
(R/'review_check.py').write_text(s)
print('Prior independent reviewer SHA256',source_sha)
print('Adapted independent reviewer SHA256',hashlib.sha256(s.encode()).hexdigest())
