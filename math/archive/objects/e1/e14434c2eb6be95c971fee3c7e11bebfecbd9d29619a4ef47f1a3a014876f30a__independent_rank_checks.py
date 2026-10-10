#!/usr/bin/env python3
"""Independent exact checks; never imports or executes submitted research code."""
from collections import Counter
from fractions import Fraction
from itertools import permutations, product
from math import comb, ceil, exp, log2
from pathlib import Path
import json, random

def successor(order):
    n=len(order); out=[None]*n
    for i,j in enumerate(order):
        if not isinstance(j,int) or not 0<=j<n or out[j] is not None:
            raise ValueError('not a permutation')
        out[j]=order[(i+1)%n]
    return out

def stable_successor(bits):
    return successor([j for j,x in enumerate(bits) if not x]+[j for j,x in enumerate(bits) if x])

def cycle_data(w,a):
    n=len(w); seen=[False]*n; cycles=[]
    for j in range(n):
        if seen[j]:continue
        length=0;k=j
        while not seen[k]:
            seen[k]=True;length+=1;k=(w[k]-a)%n
        cycles.append(length)
    return n-len(cycles),sorted(x for x in cycles if x>1)

def rank_mod(matrix,p):
    a=[[x%p for x in row] for row in matrix];r=0
    for c in range(len(a[0])):
        hit=next((i for i in range(r,len(a)) if a[i][c]),None)
        if hit is None:continue
        a[r],a[hit]=a[hit],a[r];iv=pow(a[r][c],-1,p)
        a[r]=[x*iv%p for x in a[r]]
        for i in range(r+1,len(a)):
            t=a[i][c]
            a[i]=[(x-t*y)%p for x,y in zip(a[i],a[r])]
        r+=1
        if r==len(a):break
    return r

def probability_bound(n):
    a=min(n-1,ceil(3*log2(n)))
    return max(0,1-exp(-n/32)-a*(a+1)*exp(-n/(16*(a+1)))-n*2**(-a))

def run():
    out={'uploaded_code_executed':False,'checks':[]}
    exhaustive=[];matching_checks=0;boundary_count=0
    for n in range(2,17):
        counts=Counter()
        for bits in product((0,1),repeat=n):
            w=stable_successor(bits);r,cycles=cycle_data(w,1)
            t=sum(x!=y for x,y in zip(bits,bits[1:]));s=sum(w[j]!=(j+1)%n for j in range(n))
            assert r==2*(t//2)
            assert s==(r+1 if t>=2 else 0)
            assert cycles==([r+1] if t>=2 else [])
            if t==1:boundary_count+=1
            counts[r]+=1
            if n<=10:
                for a in range(1,n):
                    matches=sum(w[j]==(j+a)%n for j in range(n))
                    q=sum(bits[j]==bits[j+a] and all(bits[k]!=bits[j] for k in range(j+1,j+a)) for j in range(n-a))
                    ra,_=cycle_data(w,a)
                    assert matches<=q+2
                    assert 2*ra>=n-matches
                    matching_checks+=1
        expected={r:2*comb(n,r+1) for r in range(0,n,2)}
        assert dict(counts)==expected
        mean=sum(Fraction(r*c,2**n) for r,c in counts.items())
        variance=sum(Fraction(c,2**n)*(r-mean)**2 for r,c in counts.items())
        assert mean==Fraction(n,2)-1
        if n>=3:assert variance==Fraction(n,4)
        exhaustive.append({'n':n,'words':2**n,'counts':dict(sorted(counts.items())),'mean':str(mean),'variance':str(variance)})
    exact_matrix_checks=0
    for n in range(2,6):
        for order in permutations(range(n)):
            w=successor(order)
            for stride in range(n):
                r,_=cycle_data(w,stride)
                for p in (2,3,5):
                    m=[[int(i==w[j])-int(i==(j+stride)%n) for j in range(n)] for i in range(n)]
                    assert rank_mod(m,p)==r
                    exact_matrix_checks+=1
    rng=random.Random(202610091845);samples=[]
    for n in (32,64,128,256,512):
        ranks=[]
        for _ in range(6):
            b=[rng.randrange(2) for _ in range(n)];w=stable_successor(b)
            rank=min(cycle_data(w,a)[0] for a in range(1,n))
            assert 8*rank>=n
            ranks.append(rank)
        samples.append({'n':n,'all_stride_minima':ranks})
    out.update(status='PASS',exhaustive=exhaustive,total_binary_words=sum(x['words'] for x in exhaustive),
               all_stride_matching_checks=matching_checks,exact_matrix_checks=exact_matrix_checks,
               corrected_one_transition_cases=boundary_count,random_samples=samples,
               explicit_probability_bound={str(n):probability_bound(n) for n in (16,64,256,1024,4096,8192,16384)},
               minimal_boundary_counterexample={'bits':[0,1],'successor':[1,0],'rank':0,'changed_edges':0,'nontrivial_cycles':0})
    return out

if __name__=='__main__':
    result=run();path=Path(__file__).with_name('CHECK_RESULTS.json')
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','total_binary_words','all_stride_matching_checks','exact_matrix_checks','corrected_one_transition_cases')},indent=2))
