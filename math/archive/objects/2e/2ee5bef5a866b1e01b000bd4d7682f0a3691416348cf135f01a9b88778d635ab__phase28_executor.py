"""True O(N) forward executor for Phase 28 two-resolvent Green sum.

Dense matrix generation in phase28_synthesis.py is *only* for offline proof
certificates. This routine shows the candidate still has O(N) application
cost per Green term. It is NOT an FFT; it deliberately fails phase synthesis.
"""
from __future__ import annotations
from dataclasses import dataclass
from random import Random
from phase28_synthesis import P,PRIMITIVE,inverse,green_sum


def cyclic_solve_order(x:list[int],order:list[int],alpha:int,den_inv:int)->list[int]:
    n=len(order)
    accum=0
    for j in order:accum=(alpha*accum+x[j])%P
    prev=accum*den_inv%P
    out=[0]*n
    for j in order:
        prev=(alpha*prev+x[j])%P
        out[j]=prev
    return out

@dataclass
class GreenTermExecutor:
    order:list[int]
    alpha:int
    left:list[int]
    right:list[int]
    coefficient:int

    def __post_init__(self):
        n=len(self.order)
        if sorted(self.order)!=list(range(n)):raise ValueError('not Hamiltonian')
        self.den_inv=inverse(1-pow(self.alpha,n,P))

    def apply(self,x:list[int])->list[int]:
        n=len(self.order)
        z=[x[j]*self.right[j]%P for j in range(n)]
        y=cyclic_solve_order(z,self.order,self.alpha,self.den_inv)
        return [self.coefficient*self.left[j]*y[j]%P for j in range(n)]

class GreenSumExecutor:
    def __init__(self,terms:list[GreenTermExecutor]):self.terms=terms
    def apply(self,x:list[int])->list[int]:
        n=len(x);out=[0]*n
        for term in self.terms:
            y=term.apply(x)
            for j in range(n):out[j]=(out[j]+y[j])%P
        return out


def seeded_executor(n:int,seed:int)->GreenSumExecutor:
    rng=Random(seed)
    omega=pow(PRIMITIVE,-(P-1)//n,P)
    roots=[pow(omega,j,P) for j in range(n)]
    terms=[]
    for t,alpha in enumerate((inverse(4),inverse(5))):
        order=list(range(n));rng.shuffle(order)
        left=[roots[rng.randrange(n)] for _ in range(n)]
        right=[roots[rng.randrange(n)] for _ in range(n)]
        coeff=1 if t==0 else 3*inverse(2)%P
        terms.append(GreenTermExecutor(order,alpha,left,right,coeff))
    return GreenSumExecutor(terms)

if __name__=='__main__':
    for n in (8,16,64,128):
        seed=2800+n
        exec=seeded_executor(n,seed)
        dense=green_sum(n,seed)
        x=list(range(n))
        ans=exec.apply(x)
        direct=[sum(dense[i][j]*x[j] for j in range(n))%P for i in range(n)]
        assert ans==direct
        print(n,'exact match,',len(exec.terms),'linear-time Green terms')
