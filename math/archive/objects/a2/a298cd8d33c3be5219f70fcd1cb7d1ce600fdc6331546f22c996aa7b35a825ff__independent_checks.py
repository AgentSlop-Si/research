#!/usr/bin/env python3
"""Independent permutation-screen checks. Imports no source-upload programs."""
from pathlib import Path
from itertools import permutations
from math import factorial,comb
from fractions import Fraction
import json
BASE=Path(__file__).resolve().parent

def every_cut(pi,r,side):
    n=len(pi)
    for t in range(1,n):
        v=n-1-max(pi[-t:]) if side=='suffix' else min(pi[:t])
        if min(t,v)>r:return False
    return True

def boundary(pi,r,side):
    n=len(pi)
    if r>=n-1:return True
    k=r+1
    return max(pi[-k:])>=n-k if side=='suffix' else min(pi[:k])<k

def count_passing(n,k):
    assert n>=2*k
    total=factorial(n)
    one_bad=factorial(n-k)//factorial(n-2*k)*factorial(n-k)
    both_bad=sum((-1)**(a+b)*comb(k,a)**2*factorial(a)*comb(k,b)**2*factorial(b)*factorial(n-a-b)
                 for a in range(k+1) for b in range(k+1))
    return total-2*one_bad+both_bad

cases=0; exhaustive=[]
for n in range(2,9):
    counts={k:0 for k in range(1,n//2+1)}
    for pi in permutations(range(n)):
        for side in ['prefix','suffix']:
            for r in range(n):
                assert every_cut(pi,r,side)==boundary(pi,r,side),(pi,r,side)
                cases+=1
        for k in counts:
            counts[k]+=boundary(pi,k-1,'prefix') and boundary(pi,k-1,'suffix')
    for k,c in counts.items():
        assert c==count_passing(n,k),(n,k,c,count_passing(n,k))
        exhaustive.append({'N':n,'boundary_size':k,'rank_sum':k-1,'passing':c,'total':factorial(n)})
large=[]
for n in [8,9,16,32,64,128,256,1024]:
    c=count_passing(n,3);p=Fraction(c,factorial(n))
    assert 0<c<=factorial(n)
    assert p<=Fraction(81,n*(n-1))
    large.append({'N':n,'rank_sum':2,'passing':str(c),'total':str(factorial(n)),
                  'probability_exact':str(p),'probability_approx':float(p),
                  'union_bound':float(Fraction(81,n*(n-1)))})
result={'every_cut_boundary_equivalence_checks':cases,'all_passed':True,
        'exact_count_comparisons':len(exhaustive),'exhaustive':exhaustive,'rank_sum_two':large,
        'uploaded_programs_executed':False}
(BASE/'CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['exhaustive','rank_sum_two']},indent=2))
print('N=8, rank sum 2:',count_passing(8,3),'/',factorial(8))
