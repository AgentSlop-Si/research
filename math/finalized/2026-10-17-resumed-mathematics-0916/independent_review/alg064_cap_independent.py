"""Fresh Gaussian-rational recurrence and dyadic bridge check, no author imports."""
from pathlib import Path
import json,hashlib
from fractions import Fraction as F
from alg064_independent import decode, add, mul, scale, nu, Z, O, rnd
import sys
P=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).parent.parent/'reports'/'alg064'
def sub(a,b):return a[0]-b[0],a[1]-b[1]
def inv(a):
 d=a[0]**2+a[1]**2;assert d;return a[0]/d,-a[1]/d

def discover(x,d):
 if d==0:return [O] if all(nu(t)==0 for t in x) else None
 m=[[tuple(x[j-i]) for i in range(1,d+1)]+[scale(x[j],-1)] for j in range(d,len(x))];r=0;piv=[]
 for c in range(d):
  t=next((i for i in range(r,len(m)) if m[i][c]!=Z),None)
  if t is None:continue
  m[r],m[t]=m[t],m[r];v=inv(m[r][c]);m[r]=[mul(v,a) for a in m[r]]
  for i in range(len(m)):
   if i!=r:
    v=m[i][c];m[i]=[sub(a,mul(v,b)) for a,b in zip(m[i],m[r])]
  piv.append(c);r+=1
  if r==len(m):break
 if any(all(v==Z for v in row[:-1]) and row[-1]!=Z for row in m):return None
 c=[Z]*d
 for i,k in enumerate(piv):c[k]=m[i][-1]
 return [O]+c

def total(v):
 z=Z
 for x in v:z=add(z,x)
 return z
cases=decode(json.loads((P/'OUTPUT_VECTORS.json').read_text()));counts={};roundings=0;maxbc=0
for case in cases:
 x=case['raw_dyadic_input'];d=case['declared_cap'];eps=case['epsilon'];n=len(x)
 assert case['claimed_error_bound']<=eps
 c=discover(x,d)
 expected='copy' if n==1 else ('certified_direct_fallback' if c is None else ('zero' if d==0 else 'recurrence'))
 assert expected==case['branch'],case['name']
 counts[expected]=counts.get(expected,0)+1
 if c is None or not d:continue
 assert all(total(mul(c[i],x[j-i]) for i in range(d+1))==Z for j in range(d,n))
 S=sum(nu(t) for t in x);tau=F(1,(2*n)**d);bc=max(v.denominator.bit_length()-1 for a in x for v in a)
 while F(1,1<<bc)>eps*tau/(8*d*(S+1)):bc+=1
 ch=[O]+[(rnd(a,bc),rnd(b,bc)) for a,b in c[1:]]
 err=sum(nu(total(mul(ch[i],x[j-i]) for i in range(d+1))) for j in range(d,n))
 assert err<=d*F(1,1<<bc)*S<=eps*tau/8
 # Exact coefficientwise cyclic residual identity, independently convolve then wrap.
 con=[Z]*(n+d)
 for i,a in enumerate(ch):
  for j,b in enumerate(x):con[i+j]=add(con[i+j],mul(a,b))
 cyc=con[:n]
 for j in range(n,n+d):cyc[j-n]=add(cyc[j-n],con[j])
 A=[total([mul(ch[i],x[j-i]) for i in range(j+1)]+[mul(ch[i],x[n+j-i]) for i in range(j+1,d+1)]) for j in range(d)]
 E=[total(mul(ch[i],x[j-i]) for i in range(d+1)) for j in range(d,n)]
 assert cyc==A+E
 roundings+=1;maxbc=max(maxbc,bc)
# Closed-form cap-one comparator independent of RREF, exhaustive ternary input.
from itertools import product
count=0
for n in range(2,7):
 for t in product((-1,0,1),repeat=n):
  x=[(F(a),F(0)) for a in t];first=next((j for j in range(1,n) if t[j-1]),None)
  direct=all(v==0 for v in t[1:]) if first is None else all(t[j]*t[first-1]==t[first]*t[j-1] for j in range(1,n))
  assert (discover(x,1) is not None)==direct;count+=1
manifest=json.loads((P/'SHA256SUMS.json').read_text());assert all(hashlib.sha256((P/k).read_bytes()).hexdigest()==v for k,v in manifest.items())
out={'status':'PASS','cases':len(cases),'branch_counts':counts,'independent_complex_rational_cap_solves':len(cases),'coefficient_bridge_and_cyclic_identity_cases':roundings,'exhaustive_cap1_decisions':count,'max_coefficient_fraction_bits':maxbc,'report_sha256':manifest['REPORT.md'],'candidate_manifest_sha256':hashlib.sha256((P/'SHA256SUMS.json').read_bytes()).hexdigest(),'method':'Independent complex-field RREF, rather than author real-block RREF; independently rounded coefficients and direct convolution; exhaustive adjacent cross-product comparator.'}
Path(__file__).with_name('ALG064_CAP_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
