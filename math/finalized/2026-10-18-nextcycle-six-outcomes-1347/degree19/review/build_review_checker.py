#!/usr/bin/env python3
"""Transparent adaptation of the previous independent reviewer, not candidate code."""
from pathlib import Path
R=Path(__file__).resolve().parent
s=(R/'inputs'/'DEGREE17_review_check.py').read_text()
s=s.replace('Fresh independent inert-certificate review; no candidate code is imported or run.','Independent degree-19 inert-certificate review. Arithmetic and literal-power method adapted from the byte-bound degree-17 independent reviewer. No candidate code is imported or run.')
s=s.replace('P,D,N=53,17,13','P,D,N=53,19,13').replace('HMOD=[6,1]+[0]*15+[1]','HMOD=[12,1]+[0]*17+[1]')
s=s.replace('17*52^2 < 2^16','19*52^2 < 2^16').replace('for i in range(33)','for i in range(2*D-1)')
s=s.replace('# Reduce u^k = -u^(k-16)-6u^(k-17), largest degree first.','# Reduce u^k = -u^(k-D+1)-12u^(k-D), largest degree first.')
s=s.replace('for k in range(32,16,-1):c[k-16]-=c[k];c[k-17]-=6*c[k]','for k in range(2*D-2,D-1,-1):c[k-D+1]-=c[k];c[k-D]-=12*c[k]')
s=s.replace('DEGREE17_LITERAL_CERTIFICATE.json','DEGREE19_LITERAL_CERTIFICATE.json')
s=s.replace('58a76f5a919c73051aebb4a45defce4e238d7a3eb21bcce57d57bb961a1db3de','b10199e01e9e7775c78bf34b6cac41ce8d1e90280a013f0a2b21b4c1dcd9a09e')
s=s.replace('202610181244','202610181335')
s=s.replace("sufficient=[2,3,5,7,11,13,17];modulus=math.prod(sufficient);assert modulus==510510","sufficient=[2,3,5,7,11,13,17,19];modulus=math.prod(sufficient);assert modulus==9699690")
s=s.replace('if math.gcd(d,modulus)==1)==19','if math.gcd(d,modulus)==1)==23')
s=s.replace("'next_unclassified_degree':19","'next_unclassified_degree':23")
s=s.replace("'method':'Fresh carry-free integer-convolution", "'method':'Independent carry-free integer-convolution")
s=s.replace("and bank['beta']==1", "and type(bank['beta'])is int and bank['beta']==1")
s=s.replace("assert frob==[0,1] and pgcd", "assert D*52**2 < 65536\n assert frob==[0,1] and pgcd")
s=s.replace("y,z=tuple(data['y']),tuple(data['z']);assert y==z and any(y[1:])", """y,z=tuple(data['y']),tuple(data['z']);assert y==z and any(y[1:])
 # Direct exact Frobenius periods, beyond merely nonbase coordinates.
 orbit_lengths=[]
 for node in roots+[y,z]:
  orbit=[];v=node
  while v not in orbit:
   orbit.append(v);v=powf(v,P)
  assert v==node and len(orbit)==D
  orbit_lengths.append(len(orbit))""")
s=s.replace("'nonbase_cross_nodes':True", "'parameter_frobenius_orbit_lengths':orbit_lengths,'nonbase_cross_nodes':True")
s=s.replace("'next_unclassified_degree':23,", "'next_unclassified_degree':23,'next_degree_field_order':P**23,'next_degree_order_bits':(P**23).bit_length(),'next_degree_exceeds_uint128':P**23>=2**128,")
(R/'review_check.py').write_text(s)
