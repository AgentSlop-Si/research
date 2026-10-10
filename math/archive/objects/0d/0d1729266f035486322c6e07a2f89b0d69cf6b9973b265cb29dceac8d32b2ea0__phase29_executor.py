"""True O(N) *candidate* three-Green-sum forward executor.

This computes B(lambda,mu) x for the Phase29 seeded Green family without
materializing dense matrices. It is NOT a Fourier transform.
"""
from random import Random
from phase28_synthesis import P,PRIMITIVE,inverse
from phase28_executor import GreenTermExecutor,seeded_executor,GreenSumExecutor
from phase29_two_parameter import SEEDS


def three_term_executor(n,lam,mu,seed=None):
    seed=SEEDS[n] if seed is None else seed
    original=seeded_executor(n,seed*3+2)
    original.terms[1].coefficient=lam%P
    rng=Random(seed*3+4)
    order=list(range(n));rng.shuffle(order)
    omega=pow(PRIMITIVE,-(P-1)//n,P)
    roots=[1]*n
    for j in range(1,n):roots[j]=roots[j-1]*omega%P
    left=[roots[rng.randrange(n)] for j in range(n)]
    right=[roots[rng.randrange(n)] for j in range(n)]
    third=GreenTermExecutor(order,inverse(7),left,right,mu%P)
    return GreenSumExecutor(original.terms+[third])
