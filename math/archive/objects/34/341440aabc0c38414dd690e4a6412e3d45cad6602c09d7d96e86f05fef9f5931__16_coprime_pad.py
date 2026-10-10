"""Coprime short-slack padding for any original FFT length.

Select Q=M*K >= oversample*N with M prime of order log N and
K having no prime factor < M. Hence gcd(Q,d)=1 for every 1<=d<M.

The short-slack search is provably N^o(1) from elementary sieve/inclusion-
exclusion; no prime gap conjecture or table oracle is necessary.
"""
from dataclasses import dataclass
from math import ceil, log2, gcd
from gaussian_lift import GaussianPlan


def sieve_primes(limit: int) -> list[int]:
    if limit<2:return []
    arr=bytearray(b'\x01')*(limit+1)
    arr[0:2]=b'\x00\x00'
    p=2
    while p*p<=limit:
        if arr[p]:
            arr[p*p:limit+1:p]=b'\x00'*(((limit-p*p)//p)+1)
        p+=1
    return [i for i in range(2,limit+1) if arr[i]]


def first_prime_at_least(t: int) -> int:
    if t<=2:return 2
    bound=max(4,2*t+2)
    return next(p for p in sieve_primes(bound) if p>=t)


def find_rough_cofactor(k0: int, m: int) -> tuple[int,int,list[int]]:
    if k0<1 or m<2:raise ValueError('invalid start or block size')
    small=sieve_primes(m-1)
    k=k0
    while any(k%p==0 for p in small):
        k+=1
    return k,k-k0,small


def build_plan(n: int, oversample: int=4, alpha: float=1/3,
               halfwidth: int|None=None, sigma2: float|None=None,
               buckets:int|None=None) -> GaussianPlan:
    if n<64:raise ValueError('prototype n>=64')
    if oversample<4:raise ValueError('proof currently certifies oversample>=4')
    if not 0<alpha<.5:raise ValueError('0<alpha<1/2')
    m=first_prime_at_least(ceil(log2(oversample*n)))
    start=(oversample*n+m-1)//m
    k,offset,_=find_rough_cofactor(start,m)
    q=m*k
    L=max(12,ceil((2*alpha/3.141592653589793)*__import__('math').log(n))) if halfwidth is None else halfwidth
    h=ceil(n**alpha) if buckets is None else buckets
    plan=GaussianPlan(n,oversample,q,m,k,q-oversample*n,L,h,float(L if sigma2 is None else sigma2),max(8,2*L),(n-1)//2)
    assert q>=oversample*n
    assert k>=m
    assert all(gcd(q,d)==1 for d in range(1,m))
    assert plan.tau<=1/(2*oversample)
    assert 2*L+5<q
    return plan


def profile(n:int, alpha:float=1/3):
    p=build_plan(n,alpha=alpha)
    start=(p.c*n+p.m-1)//p.m
    return {'n':n,'m':p.m,'q':p.q,'k':p.k,'cofactor_gap':p.k-start,
            'slack_q_minus_4n':p.slack,'halfwidth':p.halfwidth,
            'phase_buckets':p.buckets,'max_proper_displacement_gcd':max(gcd(p.q,d) for d in range(1,p.m))}

if __name__=='__main__':
    for n in (67,127,257,509,1009,2003,4093,10007,20011,100003,1000003):
        print(profile(n))
