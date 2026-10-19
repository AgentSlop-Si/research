#!/usr/bin/env python3
"""Exact prime-polynomial irreducibility proof; no extension inverses."""
from pathlib import Path
import json
P=53;D=29;MOD=[8,1]+[0]*27+[1]
def trim(a):
 a=[x%P for x in a]
 while len(a)>1 and a[-1]==0:a.pop()
 return a
def product(a,b):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return trim(c)
def remainder(a,b):
 a=trim(a);inv=pow(b[-1],-1,P)
 while len(a)>=len(b) and a!=[0]:
  q=a[-1]*inv%P;s=len(a)-len(b)
  for j,y in enumerate(b):a[s+j]-=q*y
  a=trim(a)
 return a
def power(a,n):
 r=[1]
 while n:
  if n&1:r=remainder(product(r,a),MOD)
  n//=2
  if n:a=remainder(product(a,a),MOD)
 return r
def gcd(a,b):
 while b!=[0]:a,b=b,remainder(a,b)
 return trim([x*pow(a[-1],-1,P) for x in a])
x=[0,1];rs=[]
for i in range(D):x=power(x,P);rs.append(x)
first=rs[0][:];first[1]=(first[1]-1)%P
g=gcd(MOD,trim(first));assert x==[0,1] and g==[1]
# X^(P^D)-X has derivative -1. Since D=29 is prime, its factors
# have degrees 1 or 29; the gcd removes degree 1, proving the claim.
receipt={'modulus_ascending':MOD,'degree':D,'order':str(P**D),'order_bits':(P**D).bit_length(),'all_frobenius_remainders':rs,'gcd_with_X53_minus_X':g,'criterion':'Prime degree 29: X^(53^29)=X modulo f and gcd(f,X^53-X)=1.'}
(Path(__file__).resolve().parent/'FIELD_IRREDUCIBILITY.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('PASS: u^29+u+8 irreducible over F53; field order',P**D)
