#!/usr/bin/env python3
"""Small standalone verifier for the exact nondivisibility witnesses.
This imports no research/review checker, only Python standard-library modules.
"""
import gzip,hashlib,json,math
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
RAW=gzip.decompress((ROOT/'research_cycle_1805/guarded_fourier_reduction/CERTIFICATE.json.gz').read_bytes())
assert hashlib.sha256(RAW).hexdigest()=='8a7f612c361540d427fd33aea8dc6c9710ae969a66ce15e000c9b1e3467859b4'
C=json.loads(RAW)
W=json.loads((HERE/'NONDIVISIBILITY_WITNESSES.json').read_text())
p,z=W['prime'],W['zeta']
assert p==1013 and z==114
assert all(p%d for d in range(2,math.isqrt(p)+1))
assert z!=1 and sum(pow(z,i,p) for i in range(11))%p==0
assert W['variables']==C['variables']

def coefficient(row):
    _,a,d=row
    assert d%p
    return sum(x*pow(z,i,p) for i,x in enumerate(a))*pow(d,-1,p)%p

def evaluate(rows,point):
    total=0
    for row in rows:
        t=coefficient(row)
        for v,e in zip(point,row[0]):t=t*pow(v,e,p)%p
        total=(total+t)%p
    return total

# Check all coefficients lie in the residue-place local ring. The leading
# coefficient of each divisor must be a unit there, which guarantees that a
# characteristic-zero polynomial quotient could also be reduced at this place.
for h in set(C['initial']['equations'].values())|set(C['initial']['guards'].values()):
    for row in C['polynomials'][h]:coefficient(row)
for r in W['points']:
    rows=C['polynomials'][C['initial']['guards'][r['guard']]]
    assert len(r['point'])==len(C['variables']) and all(type(x) is int and 0<=x<p for x in r['point'])
    leading=max(rows,key=lambda row:row[0])
    assert coefficient(leading)==r['leading_coefficient']!=0
    assert evaluate(rows,r['point'])==0
seen=set()
for r in W['tests']:
    key=(r['equation'],r['guard']);assert key not in seen;seen.add(key)
    point=W['points'][r['point_index']];assert point['guard']==r['guard']
    rows=C['polynomials'][C['initial']['equations'][r['equation']]]
    assert evaluate(rows,point['point'])==r['residue']!=0
assert seen=={(e,g) for e in C['initial']['equations'] for g in C['initial']['guards']}
assert len(seen)==826
print('PASS: 826 exact nondivisibility witnesses; 15 points in F_1013, zeta=114; every divisor has unit leading coefficient.')
