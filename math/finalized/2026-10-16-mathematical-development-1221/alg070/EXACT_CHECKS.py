"""Original checks for the ALG-070 scoped theorem; no inherited code imported.

Finite checks support the written proof, not unrestricted correctness/novelty.
"""
from itertools import product
from fractions import Fraction
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent

def conv(a, b, p):
    n = len(a)
    return [sum(a[i] * b[(j-i) % n] for i in range(n)) % p for j in range(n)]

def filtered_formula(a0, b0, h, la, lb, p):
    n = len(a0)
    x, y = conv(a0, h, p), conv(b0, h, p)
    z = conv(conv(a0, b0, p), h, p)
    a, b = list(a0), list(b0)
    for i, d in la: a[i] = (a[i] + d) % p
    for i, d in lb: b[i] = (b[i] + d) % p
    direct = conv(conv(a,b,p),h,p)
    formula = [(z[j]
        + sum(d*y[(j-i)%n] for i,d in la)
        + sum(d*x[(j-i)%n] for i,d in lb)
        + sum(d*e*h[(j-i-k)%n] for i,d in la for k,e in lb)) % p
        for j in range(n)]
    assert direct == formula
    return direct

def online(seq, F, B, weights=(1,1,1)):
    a = b = rent = cost = 0
    for event in seq:
        if event == 'A': a += 1
        elif event == 'B': b += 1
        else:
            r = event*(weights[0]*a+weights[1]*b+weights[2]*a*b)
            if rent+r >= F:
                cost += F; a=b=rent=0
            else: cost+=r; rent+=r
        if a+b >= B:
            cost += F; a=b=rent=0
    return cost

def offline(seq, F, B, weights=(1,1,1)):
    states={(0,0):0}
    for event in seq:
        nxt={}
        for (a,b),cost in states.items():
            if event == 'A': a+=1; r=0
            elif event == 'B': b+=1; r=0
            else: r=event*(weights[0]*a+weights[1]*b+weights[2]*a*b)
            if a+b < B:
                nxt[a,b] = min(nxt.get((a,b),10**30),cost+r)
            # A query can be served from a freshly rebased core without rent.
            nxt[0,0] = min(nxt.get((0,0),10**30),cost+F)
        states=nxt
    return min(states.values())

def run():
    formula_cases=0
    # All binary length-3 anchor/kernel triples, several two-sided event lists.
    vectors=list(product(range(2),repeat=3))
    lists=[[],[(0,1)],[(0,1),(0,-1)],[(1,2),(2,-1)],[(2,1),(0,2),(2,1)]]
    for p in (3,5):
        for a,b,h in product(vectors,repeat=3):
            for la,lb in product(lists,repeat=2):
                filtered_formula(a,b,h,la,lb,p); formula_cases+=1
    # Full enumeration over length-7 events includes empty-rent queries,
    # both operands, no-query prefixes, and large indivisible query charges.
    scheduling_cases=0; max_ratio=Fraction(0); witness=None
    alphabet=('A','B',0,1,3)
    for F in (1,2,3,5,8):
        for B in (1,2,3,5):
            for seq in product(alphabet,repeat=7):
                a=online(seq,F,B); o=offline(seq,F,B)
                assert a <= 2*o, (seq,F,B,a,o)
                scheduling_cases+=1
                if o and Fraction(a,o)>max_ratio:
                    max_ratio=Fraction(a,o); witness=[list(seq),F,B,a,o]
    # Repeated unit queries approach the factor two for this policy.
    near=('A',)+(1,)*100
    assert online(near,100,3)==199 and offline(near,100,3)==100
    # Unequal positive weights preserve the proof; sampled deterministic grid.
    weighted_cases=0
    for weights in ((2,3,5),(1,4,0)):
        for F in (2,7):
            for B in (1,3):
                for seq in product(('A','B',0,2),repeat=6):
                    assert online(seq,F,B,weights)<=2*offline(seq,F,B,weights)
                    weighted_cases+=1
    # Canonical sparse expansion of binary-shift factors.
    expansion=[]
    for d in range(1,9):
        n=2**d; value=[1]+[0]*(n-1)
        for i in range(d):
            factor=[0]*n; factor[0]=factor[2**i]=1
            value=conv(value,factor,101)
        assert value==[1]*n
        expansion.append({'depth':d,'nonzero_explicit_terms':n})
    result={'formula_cases':formula_cases,'schedule_cases':scheduling_cases,
        'weighted_schedule_cases':weighted_cases,'failures':0,
        'maximum_enumerated_ratio':str(max_ratio),'witness':witness,
        'near_two_example':{'F':100,'B':3,'online':199,'offline':100},
        'normal_form_expansion':expansion,
        'scope':'Original finite exact checks only; no inherited research programs or timing benchmarks.'}
    (OUT/'VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__': run()
