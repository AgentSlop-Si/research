#!/usr/bin/env python3
"""Original arithmetic census of the precisely stated accepted-domain union."""
from pathlib import Path
from fractions import Fraction
from math import isqrt
import json

root = Path(__file__).resolve().parent
limit=10000
smallest=list(range(limit+1))
for p in range(2,int(limit**.5)+1):
    if smallest[p]==p:
        for n in range(p*p,limit+1,p):
            if smallest[n]==n:
                smallest[n]=p
def factors(n):
    result={}
    while n>1:
        p=smallest[n]
        result[p]=result.get(p,0)+1
        n//=p
    return result
def divs(f):
    result=[1]
    for p,e in f.items():
        result=[d*p**i for d in result for i in range(e+1)]
    return result
old=[]; new=[]
for n in range(2,limit+1):
    f=factors(n)
    D=min(d+n//d for d in divs(f))
    accepted=(D*D<12*n or any(p>n//p for p in f) or n in (1331,2197)
              or (len(f)==2 and f.get(11)==1
                  and any(q>11 and e==2 for q,e in f.items())))
    if not accepted:
        old.append(n)
        if n!=2873:
            new.append(n)
assert old[0]==2873 and new[0]==3757
assert set(old)-set(new)=={2873}
n=3757
D=min(d+n//d for d in divs(factors(n)))
assert D==238 and 12*n<D*D<16*n
assert Fraction(3,102)+Fraction(102,n)<Fraction(D,n)
# An integer scalar witness; it is not asserted to have Fourier rank three.
a,b=102,110
assert a*b<=3*n and Fraction(3,a)+Fraction(3,b)<Fraction(D,n)
result={'status':'PASS','limit':limit,'previous_residuals':old,'residuals_after_2873':new,
        'added_domain':'isolated target 2873 only','next_residual':3757,
        'next_rank_three_scalar_obstruction':[a,b],
        'scalar_obstruction_is_not_a_fourier_counterexample':True}
# Correct the dated structural-gate framing: integer stable rank already closes 2873.
n=2873
minimum=None; minimizers=[]; count=0; obstructions=[]
for a in range(1,isqrt(3*n)+1):
    for b in range(a,min(n,3*n//a)+1):
        density=Fraction(3,a)+Fraction(3,b)
        count+=1
        if minimum is None or density<minimum:
            minimum=density; minimizers=[(a,b)]
        elif density==minimum:
            minimizers.append((a,b))
        if density<=Fraction(186,n):
            obstructions.append((a,b))
assert minimum==Fraction(62,957) and minimizers==[(87,99)] and not obstructions
assert minimum-Fraction(186,n)==Fraction(124,2749461)
assert Fraction(12,185)>minimum and Fraction(187,n)>minimum
assert 186**2-4*3*n==120 and 10**2<120<=12**2
assert (186**2-12**2)//4==8613
result['unrestricted_integer_stable_rank_control']={
    'N':n,'shapes':count,'minimum':str(minimum),'minimizers':minimizers,
    'baseline_gap':'124/2749461','obstructions':obstructions,
    'new_side_cutoff_used':False,
    'interpretation':'Integer stable rank alone closes target 2873; the new structural theorem strengthens its penalty.'}
(root/'DOMAIN_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
