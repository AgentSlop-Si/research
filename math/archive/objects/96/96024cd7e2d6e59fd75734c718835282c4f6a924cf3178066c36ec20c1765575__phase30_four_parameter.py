"""Phase 30: four independently ordered cyclic Green terms in a projective pencil.

The middle matrix is B(lam,mu,rho)=G0+lam G1+mu G2+rho G3. 
All rows and columns are over F_p for exact construction/certification. 
Dense target assembly is an *offline feasibility calculation*, never the linear executor.
"""
from __future__ import annotations
from pathlib import Path
import sys
from random import Random
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'fft_green_phase29_two_parameter'))
from phase29_two_parameter import build_family, P, SEEDS
from phase28_synthesis import inverse, random_cycle, green_matrix, PRIMITIVE

def fourth_green(n:int,seed:int)->list[list[int]]:
    """New *independently seeded* weighted Hamiltonian Green inverse (alpha=1/11)."""
    rng=Random(seed)
    omega=pow(PRIMITIVE,-(P-1)//n,P)
    roots=[1]*n
    for k in range(1,n): roots[k]=roots[k-1]*omega%P
    g=green_matrix(random_cycle(n,rng),inverse(11))
    left=[roots[rng.randrange(n)] for _ in range(n)]
    right=[roots[rng.randrange(n)] for _ in range(n)]
    return [[left[i]*g[i][j]*right[j]%P for j in range(n)] for i in range(n)]

def build_four(n:int,seed:int|None=None):
    if seed is None: seed=SEEDS[n]
    target,g0,g1,g2=build_family(n,seed)
    g3=fourth_green(n,seed*3+7)
    return target, (g0,g1,g2,g3)

def combine(g:list[list[list[int]]],lambdas:list[int]|tuple[int,...]):
    assert len(g)==len(lambdas)
    n=len(g[0])
    return [[sum(lambdas[k]*g[k][i][j] for k in range(len(g)))%P for j in range(n)] for i in range(n)]

class FourGreenExecutor:
    """Four O(N) cyclic solves, exact modulo P; initialization O(N)."""
    def __init__(self,n:int,seed:int|None=None):
        self.n=n
        seed=SEEDS[n] if seed is None else seed
        self.seed=seed
        # Recreate prior three components with same seeds as matrix generator.
        # fourth uses independent seed.
        from phase29_executor import three_term_executor
        self.three=three_term_executor(n,0,0,seed)
        rng=Random(seed*3+7)
        self.succ=random_cycle(n,rng)
        alpha=inverse(11)
        omega=pow(PRIMITIVE,-(P-1)//n,P)
        roots=[1]*n
        for k in range(1,n): roots[k]=roots[k-1]*omega%P
        self.left=[roots[rng.randrange(n)] for _ in range(n)]
        self.right=[roots[rng.randrange(n)] for _ in range(n)]
        self.alpha=alpha
        self.den=inverse(1-pow(alpha,n,P))

    def apply(self,x,coeffs=(1,2,3,5)):
        lam,mu,rho=coeffs[1:]
        if coeffs[0]!=1: raise ValueError('constant Green coefficient must be 1')
        self.three.terms[1].coefficient=lam%P
        self.three.terms[2].coefficient=mu%P
        y=self.three.apply(x)
        u=[x[i]*self.right[i]%P for i in range(self.n)]
        # Solve (I-alpha*W) v = u, W e_j=e_succ[j].
        # v[succ[j]] = alpha*v[j] + u[succ[j]] with wrap condition.
        # v[succ[0]] given v[0], obtain v[0] from cycle-sum recurrence.
        cyc=[0]; cur=self.succ[0]
        while cur!=0:
            cyc.append(cur);cur=self.succ[cur]
        assert len(cyc)==self.n
        # equation v[cyc[t]]=u[cyc[t]]+alpha*v[cyc[t-1]] for t>=1;
        # v[cyc[0]]=u[cyc[0]]+alpha*v[cyc[-1]]
        a=self.alpha;acc=0
        for j in cyc:acc=(u[j]+a*acc)%P
        prev=acc*self.den%P
        v=[0]*self.n
        for j in cyc:
            prev=(u[j]+a*prev)%P
            v[j]=prev
        return [(y[i]+rho*self.left[i]*v[i])%P for i in range(self.n)]
