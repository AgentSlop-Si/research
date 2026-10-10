"""Exact field-arithmetic five-Green *middle pencil* executor.

Each independently ordered cyclic Hamiltonian Green resolvent is applied with
one O(N) recurrence; the five-sum application costs O(N) arithmetic given
cycle orderings, precomputed parameters, and roots of unity.

It is NOT an FFT: the seeded five-term pencil is provably not phase-equivalent
to the required middle Fourier matrix at the audited lengths.
"""
from __future__ import annotations
from random import Random
from phase31_rectangular import ROOT, P, SEEDS, family
from phase30_four_parameter import FourGreenExecutor
from phase28_synthesis import PRIMITIVE, inverse, random_cycle


class FiveGreenExecutor:
    def __init__(self,n:int,seed:int|None=None):
        seed=SEEDS.get(n,2800+n) if seed is None else seed
        self.n,self.seed=n,seed
        self.four=FourGreenExecutor(n,seed)
        rng=Random(seed*3+11)
        succ=random_cycle(n,rng)
        omega=pow(PRIMITIVE,-(P-1)//n,P)
        roots=[1]*n
        for j in range(1,n):roots[j]=roots[j-1]*omega%P
        self.left=[roots[rng.randrange(n)] for _ in range(n)]
        self.right=[roots[rng.randrange(n)] for _ in range(n)]
        self.alpha=inverse(13)
        self.den=inverse(1-pow(self.alpha,n,P))
        cycle=[0]
        cur=succ[0]
        while cur != 0:
            cycle.append(cur)
            cur=succ[cur]
        assert len(cycle)==n
        self.cycle=cycle

    def apply(self,x,coeffs=(1,2,3,4,5)):
        if len(x)!=self.n or len(coeffs)!=5 or coeffs[0]!=1:
            raise ValueError('expected input length N and coefficients (1,*,*,*,*)')
        y=self.four.apply(x,coeffs[:4])
        a=self.alpha;u=[x[i]*self.right[i]%P for i in range(self.n)]
        accumulator=0
        for j in self.cycle:
            accumulator=(u[j]+a*accumulator)%P
        prev=accumulator*self.den%P
        for j in self.cycle:
            prev=(u[j]+a*prev)%P
            y[j]=(y[j]+coeffs[4]*self.left[j]*prev)%P
        return y


def dense_reference(x,coeffs,gens):
    n=len(x)
    return [sum(coeffs[k]*sum(gens[k][i][j]*x[j] for j in range(n))
                for k in range(5))%P for i in range(n)]
