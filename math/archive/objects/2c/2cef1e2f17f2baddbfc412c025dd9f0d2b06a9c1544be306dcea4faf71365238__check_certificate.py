#!/usr/bin/env python3
"""Exact bounded witness checks, not a full Lean theorem verification.
Source: OpenAI math fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb,
preprints/An-explicit-power-saving-for-the-exact-discrete-Fourier-transform-
September-25-2026/build/sections/network.tex.
Candidate modification: use h incidence centers, eliminating total-sum center.
"""
from math import comb
from fractions import Fraction as F
from decimal import Decimal, localcontext
from itertools import combinations
import json
from pathlib import Path

OUT=Path(__file__).resolve().parent

def params(h,q=3):
    t=(q-1)//2; v=comb(h,q); rho=comb(h,t)
    d=sum(comb(q,s)*comb(h-q,q-s) for s in range(0,q,2) if q-s<=h-q)
    m=h**3; I=3*v*v; W=2*v**3+I*(v*d+rho)
    D=2*v*v*(v-3*h*rho); star=1<<(W-1).bit_length()
    with localcontext() as ctx:
        ctx.prec=70
        eps=Decimal(D)/Decimal(m*star)
        gain=-(1-eps).ln()/Decimal(m).ln() if D>0 else Decimal(0)
    return dict(h=h,q=q,t=t,v=v,rho=rho,neighbors=d,m=m,invocations=I,
                W=W,Wstar=star,padding=star-W,Delta=D,S=m*star-D,
                critical_gain_decimal=str(gain))

p=params(24)
assert p['v']==2024 and p['rho']==24 and p['neighbors']==1393
assert p['W']==34666930287616 and p['Delta']==2425172992
assert p['Wstar']==2**45 and p['m']==13824
assert 0 < p['Delta'] < p['m']*p['Wstar']
# Exhaust all input/output triple pairs. Use scale 6 so no floating point.
# 6*RG = 3*intersection-3; 6*JV is its negative on even intersections.
triples=[sum(1<<j for j in T) for T in combinations(range(24),3)]
pairs=0
for S in triples:
    degree=0
    for T in triples:
        s=(S&T).bit_count()
        rg6=3*s-3
        jv6=-rg6 if s%2==0 else 0
        assert rg6+jv6 == (6 if S==T else 0)
        degree += (s%2==0)
        pairs+=1
    assert degree==p['neighbors']
# Exact critical exponent bound: log(m)<191/20=9.55, proved using a
# rational lower Taylor sum for exp(191/20). And Delta/(m W*)>
# (26/50_000_000_000)*(191/20), so theta<1-5.2e-10.
x=F(191,20); term=F(1); exp_lower=F(1)
for j in range(1,41):
    term*=x/j; exp_lower+=term
assert exp_lower > p['m']
critical_bound=F(26,50_000_000_000)
normalized=F(p['Delta'],p['m']*p['Wstar'])
assert normalized > critical_bound*x
# For any fixed logarithmic-logarithmic exponent, choose the smaller
# eventual all-length exponent saving 5e-10; gap is strictly positive.
final_bound=F(1,2_000_000_000)
assert critical_bound>final_bound
# Signed dimension accounting for arbitrary role values, once the
# paper's nested-label lemma is transferred to h=24: only each center's
# one h-dimensional decrease is charged. Auxiliaries are all included.
N=p['v']**3
s=p['W']*p['m']-2*N+2*p['invocations']*p['rho']*24
assert p['W']*p['m']-s==p['Delta']
assert s+p['padding']*p['m']==p['S']
assert 24>2*3 # coordinate unit outside union of two triple supports
# Bounded generic odd-subset scan; numbers are candidates only until
# the rank factorization and residual basis conditions are justified.
scan=[params(h,q) for q in (3,5,7,9) for h in range(2*q+1,129)]
valid=[z for z in scan if z['Delta']>0]
valid.sort(key=lambda z:Decimal(z['critical_gain_decimal']),reverse=True)
report=dict(candidate=p,pairs_checked=pairs,
    checks=['RG+JV=I for all 4,096,576 triple pairs',
            'Every triple has exactly 1,393 even-intersection neighbors',
            'Signed residual sum and power-of-two padding agree exactly',
            'Rational Taylor/log bound proves theta < 1 - 5.2e-10'],
    critical_bound=str(critical_bound),eventual_all_length_bound=str(final_bound),
    exponent_exact_margin=str(normalized-critical_bound*x),
    scan_count=len(scan),scan_positive_count=len(valid),scan_top5=valid[:5],
    limitations=['No Lean build or proof kernel validation performed',
      'No complete astronomical network enumerated',
      'Label transfer, arbitrary-register identity, indexing and recurrence verified by mathematical reduction, not full end-to-end executable',
      'No numerical stability, finite precision, crossover or practical speed claim',
      'Novelty beyond pinned source snapshot not established'])
(OUT/'certificate_results.json').write_text(json.dumps(report,indent=2)+'\n')

# Formal noncommutative-polynomial verification of all eight scalar rows.
# A word ('R','G','x') represents R G x; the dictionary is an exact
# integer linear combination of such words. No numeric values assumed.
def add(a,b,scale=1):
    out=dict(a)
    for w,c in b.items():
        out[w]=out.get(w,0)+scale*c
        if not out[w]: del out[w]
    return out
def op(symbol,a): return {(symbol,)+w:c for w,c in a.items()}
x0={('x',):1}; y0={('y',):1}; A0={('A',):1}; c0={('c',):1}
x,y,A,c=x0,y0,A0,c0
y=add(y,op('J',A),-1)
y=add(y,op('R',c),-1)
A=add(A,op('V',x))
c=add(c,op('G',x))
y=add(y,op('R',c))
y=add(y,op('J',A))
c=add(c,op('G',x),-1)
A=add(A,op('V',x),-1)
assert x==x0 and A==A0 and c==c0
assert y=={('y',):1,('R','G','x'):1,('J','V','x'):1}
report['checks'].append('Formal eight-row replay restores arbitrary A and c; y changes by (RG+JV)x')
# Three scalar bank stages after the certified RG+JV=I identity.
X={('X',):1};Y={('Y',):1}
Y=add(Y,X);X=add(X,Y,-1);Y=add(Y,X)
assert X=={('Y',):-1} and Y=={('X',):1}
report['checks'].append('Three logical stages give signed bank exchange (X,Y)->(-Y,X)')
# Explicit charge for straightforward pointwise scalar implementation:
# J costs 2 scalar gates per shear, V/G add/subtract cost 1, R costs2.
vd=p['v']*p['neighbors']
scalar_per_invocation=6*vd+(4*p['h']+6)*p['v']
shears_per_invocation=4*vd+(2*p['h']+6)*p['v']
report['pointwise_cost']=dict(scalar_gates_per_invocation=scalar_per_invocation,
    scalar_gates_network=p['invocations']*scalar_per_invocation,
    shears_per_invocation=shears_per_invocation,
    C_calls_to_replace_all_pointwise_shears=3*p['invocations']*shears_per_invocation)
(OUT/'certificate_results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
