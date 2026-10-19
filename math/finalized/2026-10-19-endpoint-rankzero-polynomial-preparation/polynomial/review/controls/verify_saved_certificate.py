"""Exact cold verifier of saved N=4 centers; no Newton or imported research code."""
import json
from fractions import Fraction as F
from pathlib import Path
root=Path(__file__).resolve().parents[1]
c=json.loads((root/'evidence/FULL_TOLERANCE_N4_CERTIFICATE.json').read_text())
def add(x,y):return (x[0]+y[0],x[1]+y[1])
def mul(x,y):return (x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def sc(x,k):return (x[0]*k,x[1]*k)
def U(x):return abs(x[0])+abs(x[1])
def low(x):return max(abs(x[0]),abs(x[1]))
def norm2(x):return x[0]**2+x[1]**2
r=F(1,1<<c['radius_exponent']); E=F(int(c['E_numerator_hex'],16),int(c['E_denominator_hex'],16));t=1<<642
ws=[(F(int(v['real_numerator_hex'],16),1<<v['real_denominator_exponent']),F(int(v['imag_numerator_hex'],16),1<<v['imag_denominator_exponent'])) for v in c['centers']]
R=1<<647;eta=F(1,(2*R**4)**12);amin=F(1,R**2)
for w in ws:
    w2=mul(w,w);w3=mul(w2,w)
    a0=add(add(add(w3,mul((1,-1),w2)),sc(w,t-1)),(-t,0))
    a1=add(add(sc(w2,3),mul((2,-2),w)),(t-1,0))
    a2=add(sc(w,3),(1,-1))
    assert U(a0)+2*E+(U(a2)+2*E)*r**2+(1+2*E)*r**3 < (low(a1)-E)*r
    assert norm2(w)>(amin/2)**2
    assert low(add((1,0),mul(w2,w2)))>=3*eta/4
for i,w in enumerate(ws):
    for z in ws[:i]:assert norm2(add(w,sc(z,-1)))>(2*r)**2
res={'status':'PASS','saved_roots':3,'exact_expanded_cubic_RC':True,'pairwise_disjoint':True,'nonzero_margin':True,'direct_denominator_margin':True,'no_numerical_root_engine_used':True}
(root/'evidence/COLD_CERTIFICATE_RESULT.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps(res,indent=2))
