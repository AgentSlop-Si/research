#!/usr/bin/env python3
"""Exact Frobenius orbit and support checks on inert degree-29 certificate JSON."""
from pathlib import Path
import json,hashlib,math
R=Path(__file__).resolve().parent;P=53;D=29;MOD=[8,1]+[0]*27+[1]
assert all(P%i for i in range(2,math.isqrt(P)+1)) and all(D%i for i in range(2,math.isqrt(D)+1))
Z=(0,)*D;O=(1,)+(0,)*(D-1)
def mul(a,b):
 c=[0]*(2*D-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 for k in range(2*D-2,D-1,-1):
  q=c[k]%P
  for j,v in enumerate(MOD[:-1]):c[k-D+j]-=q*v
 return tuple(x%P for x in c[:D])
def power(a,n):
 z=O
 while n:
  if n&1:z=mul(z,a)
  n//=2
  if n:a=mul(a,a)
 return z
c=json.loads((R/'DEGREE29_LITERAL_CERTIFICATE.json').read_text());assert c['degree']==D and c['field_modulus_ascending']==MOD
roots=[tuple(x) for x in c['roots']];nodes=roots+[tuple(c['y']),tuple(c['z'])];orbits=[]
for node in nodes:
 assert node!=Z and any(node[1:]);orbit=[];a=node
 while a not in orbit:orbit.append(a);a=power(a,P)
 assert a==node and len(orbit)==D
 orbits.append(orbit)
assert {power(x,P) for x in roots}!=set(roots)
out={'verdict':'PASS','degree':D,'primality_of_53_and_29_checked':True,'node_order':'seven support roots, y, z','exact_frobenius_orbit_lengths':[len(o) for o in orbits],'all_support_roots_and_cross_nodes_nonbase':True,'same_sign_support_not_Frobenius_stable':True,'cross_y_equals_z':c['y']==c['z'],'distinct_conjugate_parameter_lists':D,'cross_node_frobenius_orbit':orbits[7],'certificate_sha256':hashlib.sha256((R/'DEGREE29_LITERAL_CERTIFICATE.json').read_bytes()).hexdigest()}
(R/'WITNESS_STRUCTURE.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
