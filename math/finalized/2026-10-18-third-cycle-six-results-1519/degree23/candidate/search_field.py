#!/usr/bin/env python3
"""Deterministic first-irreducible search in u^23+u+c; no extension inverses."""
from pathlib import Path
import json
P=53;D=23;MOD=[5,1]+[0]*21+[1]
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
ledger=[]
for c in range(1,53):
 MOD=[c,1]+[0]*21+[1];x=[0,1];rs=[]
 for i in range(D):x=power(x,P);rs.append(x)
 f=rs[0][:];f[1]=(f[1]-1)%P;g=gcd(MOD,trim(f));ok=x==[0,1] and g==[1]
 ledger.append({'constant':c,'frobenius23_remainder':x,'gcd_with_X53_minus_X':g,'irreducible':ok})
 if ok:break
assert c==5
out={'family':'u^23+u+c; c=1,...,52, first irreducible','prime':P,'degree':D,'tests':ledger,'chosen_constant':c}
(Path(__file__).resolve().parent/'FIELD_SEARCH.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: first irreducible has constant',c)
