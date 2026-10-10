"""Phase 20: exact Weyl-covariance black-box tester and actual O(N)-apply
noncommuting Green-sum examples, over the prime field F_998244353.

The test is ONE-SIDED Monte Carlo, not a proof of equality in C from
finite-field sampling. For a nonzero defect matrix, one uniform field vector
misses it with probability <=1/p. The calibration is deterministic.
"""
from __future__ import annotations
from dataclasses import dataclass
import random
from typing import Callable

P = 998244353
GEN = 3

def modular_root(n: int) -> int:
    assert n >= 2 and n & (n-1) == 0 and (P-1) % n == 0
    return pow(GEN, -(P-1)//n, P)

def modular_sqrt(a: int) -> int:
    """Tonelli-Shanks; required for normalized Fourier controls."""
    a %= P
    if a == 0: return 0
    if pow(a, (P-1)//2, P) != 1: raise ValueError('non-square')
    q = P-1; s=0
    while q % 2 == 0: q//=2; s+=1
    z=2
    while pow(z, (P-1)//2, P) != P-1: z+=1
    c=pow(z,q,P); r=pow(a,(q+1)//2,P); t=pow(a,q,P); m=s
    while t != 1:
        x=t*t%P; i=1
        while x != 1: x=x*x%P; i+=1
        b=pow(c,1<<(m-i-1),P)
        r=r*b%P; t=t*b*b%P; c=b*b%P; m=i
    return r

def ntt(x: list[int], normalized=True) -> list[int]:
    """Reference exact Cooley-Tukey: genuinely O(N log N), not a claimed speedup."""
    n=len(x); w=modular_root(n)
    a=list(x)
    j=0
    for i in range(1,n):
        b=n>>1
        while j & b: j ^=b; b >>=1
        j ^=b
        if i<j:a[i],a[j]=a[j],a[i]
    size=2
    while size<=n:
        step=pow(w,n//size,P)
        for lo in range(0,n,size):
            tw=1
            for j in range(size//2):
                u=a[lo+j]; v=a[lo+j+size//2]*tw%P
                a[lo+j]=(u+v)%P
                a[lo+j+size//2]=(u-v)%P
                tw=tw*step%P
        size <<=1
    if normalized:
        inv_scale=pow(modular_sqrt(n),-1,P)
        a=[v*inv_scale%P for v in a]
    return a

def shift(x: list[int]) -> list[int]:
    """Z e_k=e_{k+1}, so (Zx)[j]=x[j-1]."""
    return [x[-1]]+x[:-1]

def inverse_shift(x: list[int]) -> list[int]:
    """(Z^-1 x)[j]=x[j+1]."""
    return x[1:]+x[:1]

def modulate(x: list[int]) -> list[int]:
    w=modular_root(len(x)); p=1; out=[]
    for a in x:
        out.append(a*p%P);p=p*w%P
    return out

def random_nonzero(n,rng): return [rng.randrange(P) for _ in range(n)]

@dataclass
class GateReport:
    n: int
    calibrated: bool
    first_equation: bool
    second_equation: bool
    passed: bool
    trials: int
    circuit_calls: int
    nonzero_first: int
    nonzero_second: int
    one_sided_false_accept_bound: str


def check_weyl(oracle: Callable[[list[int]], list[int]], n:int, *,
               trials:int=2, seed:int|None=None, normalized:bool=True) -> GateReport:
    """Check MZ=DM and MD=Z^-1 M by randomized exact vectors.

    Requires 3 calls per random vector (M(r), M(Zr), M(Dr)), plus
    1 separate M(e0) scalar normalization probe. All other work O(N).
    A failing modular test is a definitive rejection of the mapped circuit;
    passing finitely many tests does not prove a complex-number identity.
    With seed=None, draw from the OS-backed SystemRandom for the rigorous
    one-sided probability bound. A fixed seed yields a reproducible test
    but NOT an independent randomness guarantee.
    """
    if trials<1:raise ValueError('need at least one random trial')
    base=[0]*n;base[0]=1
    base_out=oracle(base)
    c0=pow(modular_sqrt(n),-1,P) if normalized else 1
    calibrated=base_out[0]%P==c0
    rng=random.SystemRandom() if seed is None else random.Random(seed)
    first=True;second=True;num_first=0;num_second=0
    for _ in range(trials):
        vec=random_nonzero(n,rng)
        out=oracle(vec)
        mz=oracle(shift(vec))
        md=oracle(modulate(vec))
        ref1=modulate(out)
        ref2=inverse_shift(out)
        bad1=sum(x!=y for x,y in zip(mz,ref1))
        bad2=sum(x!=y for x,y in zip(md,ref2))
        num_first+=bad1;num_second+=bad2
        first &= bad1==0;second &= bad2==0
    return GateReport(n, calibrated, first,second,
                      calibrated and first and second, trials, 1+3*trials,
                      num_first,num_second,f'{P}^-{trials} (independent uniform trials)')

@dataclass
class TridiagonalLU:
    """Exact precomputed tridiagonal LU with O(N) memory and solve cost.
    lower[i] is at (i,i-1), upper[i] is at (i,i+1).
    This implementation needs nonzero unpivoted pivots in the chosen field.
    """
    lower:list[int]
    invdiag:list[int]
    upper_normalized:list[int]

    @classmethod
    def build(cls,lo:list[int],diag:list[int],up:list[int]) -> 'TridiagonalLU':
        n=len(diag); assert len(lo)==len(up)==n
        invdiag=[0]*n; upper_normalized=[0]*n
        for i in range(n):
            pivot=(diag[i] - (lo[i]*upper_normalized[i-1] if i else 0))%P
            if not pivot:raise ZeroDivisionError(f'zero unpivoted pivot at {i}')
            invdiag[i]=pow(pivot,-1,P)
            if i<n-1:upper_normalized[i]=up[i]*invdiag[i]%P
        return cls(lo[:],invdiag,upper_normalized)

    def solve(self,b:list[int])->list[int]:
        n=len(self.invdiag);assert len(b)==n
        v=[0]*n;v[0]=b[0]*self.invdiag[0]%P
        for i in range(1,n):v[i]=(b[i]-self.lower[i]*v[i-1])*self.invdiag[i]%P
        x=v
        for i in range(n-2,-1,-1):x[i]=(x[i]-self.upper_normalized[i]*x[i+1])%P
        return x

@dataclass
class GreenTerm:
    solver:TridiagonalLU
    perm:list[int]
    left:list[int]
    right:list[int]

    def apply_add(self,x:list[int],out:list[int])->None:
        n=len(x)
        local=[self.right[i]*x[self.perm[i]]%P for i in range(n)]
        solved=self.solver.solve(local)
        for i in range(n):
            j=self.perm[i]
            out[j]=(out[j]+self.left[i]*solved[i])%P

class GreenSum:
    def __init__(self,terms:list[GreenTerm]):
        self.terms=terms
        self.n=len(terms[0].perm)

    def __call__(self,x:list[int])->list[int]:
        out=[0]*self.n
        for term in self.terms:term.apply_add(x,out)
        return out

class GreenProduct:
    def __init__(self,stages:list[GreenSum]):
        self.stages=stages;self.n=stages[0].n
    def __call__(self,x:list[int])->list[int]:
        for stage in self.stages:x=stage(x)
        return x


def seeded_product(n:int, *, terms_per_stage=2, stages=2, seed=20)->GreenProduct:
    """Independent path orders and cyclotomic phase gauges. Construction
    cost O(stages*terms_per_stage*n*log p) field arithmetic to invert pivots.
    Calls cost O(stages*terms_per_stage*n) field arithmetic and movement.
    """
    rng=random.Random(seed)
    w=modular_root(n)
    phase=[pow(w,k,P) for k in range(n)]
    sums=[]
    for _ in range(stages):
        terms=[]
        for _ in range(terms_per_stage):
            diag=[(9+phase[rng.randrange(n)])%P for i in range(n)]
            lo=[0]+[(1+phase[rng.randrange(n)])%P for i in range(1,n)]
            up=[(1+phase[rng.randrange(n)])%P for i in range(n-1)]+[0]
            solver=TridiagonalLU.build(lo,diag,up)
            perm=list(range(n));rng.shuffle(perm)
            left=[phase[rng.randrange(n)] for _ in range(n)]
            right=[phase[rng.randrange(n)] for _ in range(n)]
            terms.append(GreenTerm(solver,perm,left,right))
        sums.append(GreenSum(terms))
    return GreenProduct(sums)

class DiagonalAfter:
    """M=diag(row_factors)*FFT; passes first Weyl identity only."""
    def __init__(self,n):
        self.n=n;self.row=[(1+i*i)%P for i in range(n)]
        self.row[0]=1
    def __call__(self,x):
        return [a*b%P for a,b in zip(self.row,ntt(x))]

class ScaledFFT:
    def __init__(self,n,s):self.n=n;self.s=s
    def __call__(self,x):return [self.s*a%P for a in ntt(x)]

class NearResonantGreen:
    """Field reduction of B_N^-1 for B=I-(1-1/N)*T_path/2.
    Singular values/conditioning are real-numeric concepts, not field order.
    """
    def __init__(self,n):
        self.n=n
        c=-(n-1)
        self.solver=TridiagonalLU.build([0]+[c]*(n-1),[2*n]*n,[c]*(n-1)+[0])
    def __call__(self,x):
        return [2*self.n*v%P for v in self.solver.solve(x)]


def seeded_near_resonant_product(n:int,*,terms_per_stage=2,stages=2,seed=20)->GreenProduct:
    """Noncommuting independently permuted *near-resonant* path solves.

    Denominators are scaled integer forms of
      B=I-[(n-1-r)/(2*n)]*T_path,
    whose real spectral gaps are O(1/n) for each fixed r.
    The finite-field experiment tests exact phase algebra, not conditioning.
    """
    rng=random.Random(seed)
    roots=[pow(modular_root(n),k,P) for k in range(n)]
    sums=[]
    for stage in range(stages):
        terms=[]
        for term in range(terms_per_stage):
            r=(stage+term)%3
            off=-(n-1-r)
            lu=TridiagonalLU.build([0]+[off]*(n-1),[2*n]*n,[off]*(n-1)+[0])
            perm=list(range(n));rng.shuffle(perm)
            left=[2*n*roots[rng.randrange(n)]%P for _ in range(n)]
            right=[roots[rng.randrange(n)] for _ in range(n)]
            terms.append(GreenTerm(lu,perm,left,right))
        sums.append(GreenSum(terms))
    return GreenProduct(sums)
