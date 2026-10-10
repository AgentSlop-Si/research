"""Exact counting experiment behind the degree-limited annihilator obstruction."""
from itertools import product
from math import exp
import random


def first_coefficients_binary(a,q):
    n=len(a)
    out=[]
    for i in range(n):
        out.append(sum(q[j]*a[i-j] for j in range(min(i,len(q)-1)+1))%2)
    return tuple(out)


def exhaustive_small_case(n=8,d=3):
    count=0
    for q_tail in product([0,1],repeat=d):
        q=(1,)+q_tail
        image=set()
        for bits in product([0,1],repeat=n):
            image.add(first_coefficients_binary(bits,q))
        if len(image)!=2**n:
            raise AssertionError((q,len(image)))
        count+=1
    print(f'EXHAUSTIVE: {count} binary filters, every one bijects all {2**n} length-{n} arrays')


def random_hard_case(n=1024,d=8):
    rng=random.Random(20261009)
    x=[rng.randrange(2) for _ in range(n)]
    weights=[sum(first_coefficients_binary(x,(1,)+q)) for q in product([0,1],repeat=d)]
    bound=(2**d)*exp(-n/18)
    print(f'RANDOM n={n}, all {2**d} degree<={d} filters: min-weight={min(weights)}, max={max(weights)}, threshold={n//3}')
    print(f'THEORETICAL union Hoeffding upper bound on any weight <=n/3: {bound:.3e}')
    assert min(weights)>n//3

if __name__=='__main__':
    exhaustive_small_case()
    random_hard_case()
