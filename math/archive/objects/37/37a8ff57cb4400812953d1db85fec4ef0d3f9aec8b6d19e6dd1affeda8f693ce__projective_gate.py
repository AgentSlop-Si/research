"""Fourier phase curvature: exact, row/column monomial-gauge invariant tests.

A is monomially equivalent to the normalized DFT iff every entry is nonzero
and its anchored 2x2 cross-ratio exponent matrix equals alpha*beta (mod N)
with alpha and beta both complete residue permutations.

A 2x2 cross ratio outside the N-th roots immediately excludes *all* outer
permutations and nonzero diagonal scalings, after just two oracle calls.
"""
from __future__ import annotations
from dataclasses import dataclass
import random
from weyl_gate import P, modular_root, ntt, modular_sqrt

@dataclass
class CurvatureReport:
    n:int
    excluded:bool
    reason:str
    rows:tuple[int,int]
    cols:tuple[int,int]
    ratio:int|None
    ratio_power_n:int|None
    circuit_calls:int


def cross_ratio_witness(oracle, n:int, rows=(0,1),cols=(0,1)) -> CurvatureReport:
    """Deterministic one-sided rejection for any outer monomial gauge.

    The selected 2x2 cross ratio of a monomially equivalent DFT must be in
    mu_n: r^n=1. A passing witness is INCONCLUSIVE, not equivalence.
    """
    i,j=rows;k,l=cols
    assert i!=j and k!=l and all(0<=z<n for z in (i,j,k,l))
    e_k=[0]*n;e_k[k]=1
    e_l=[0]*n;e_l[l]=1
    col_k=oracle(e_k)
    col_l=oracle(e_l)
    a,b,c,d=col_k[i],col_l[j],col_l[i],col_k[j]
    if 0 in (a,b,c,d):
        return CurvatureReport(n,True,'zero entry: the DFT has none',rows,cols,None,None,2)
    ratio=a*b%P*pow(c*d%P,-1,P)%P
    power=pow(ratio,n,P)
    return CurvatureReport(n,power!=1,
          'non-root cross ratio' if power!=1 else 'inconclusive: sampled ratio is an Nth root',
          rows,cols,ratio,power,2)

class MaskedPermutedFFT:
    """Known-good positive control with arbitrary nonzero outer row/col
    scalings and permutations. Its application uses a conventional NTT.
    """
    def __init__(self,n:int,seed:int=23):
        self.n=n
        rng=random.Random(seed)
        self.rows=list(range(n));rng.shuffle(self.rows)
        self.cols=list(range(n));rng.shuffle(self.cols)
        self.left=[rng.randrange(1,P) for _ in range(n)]
        self.right=[rng.randrange(1,P) for _ in range(n)]
    def __call__(self,x):
        u=[0]*self.n
        for k in range(self.n):u[self.cols[k]]=self.right[k]*x[k]%P
        v=ntt(u)
        return [self.left[j]*v[self.rows[j]]%P for j in range(self.n)]

@dataclass
class FullGaugeReport:
    n:int
    equivalent:bool
    reason:str
    witness:tuple[int,int]|None
    alpha:list[int]|None
    beta:list[int]|None
    row_scalings:list[int]|None
    col_scalings:list[int]|None


def full_monomial_gate(A:list[list[int]]) -> FullGaugeReport:
    """Complete deterministic exact test for explicitly available A.

    It recognizes A=L * P_row * F_normalized * P_col * R,
    with arbitrary invertible diagonal L,R and permutations. Runtime
    O(N^2) field operations plus O(N log p) prep: NOT an FFT executor.
    """
    n=len(A)
    assert n>=2 and all(len(row)==n for row in A)
    if any(x%P==0 for row in A for x in row):
        return FullGaugeReport(n,False,'zero entry',None,None,None,None,None)
    w=modular_root(n)
    dlog={pow(w,e,P):e for e in range(n)}
    if len(dlog)!=n:raise AssertionError('root not primitive')
    a00=A[0][0]%P
    rb=[a00*pow(A[i][0],-1,P)%P for i in range(n)]
    cb=[pow(A[0][j],-1,P) for j in range(n)]
    exps=[[0]*n for _ in range(n)]
    primitive=None
    for i in range(n):
        for j in range(n):
            ratio=A[i][j]*rb[i]%P*cb[j]%P
            e=dlog.get(ratio)
            if e is None:
                return FullGaugeReport(n,False,'cross ratio not Nth root',(i,j),None,None,None,None)
            exps[i][j]=e
            if e%2 and primitive is None:primitive=(i,j)
    if primitive is None:
        return FullGaugeReport(n,False,'no primitive anchored cross ratio',None,None,None,None,None)
    i0,j0=primitive
    beta=exps[i0][:]
    binv=pow(beta[j0],-1,n)
    alpha=[exps[i][j0]*binv%n for i in range(n)]
    if sorted(alpha)!=list(range(n)) or sorted(beta)!=list(range(n)):
        return FullGaugeReport(n,False,'anchor exponents are not permutations',primitive,None,None,None,None)
    for i in range(n):
        for j in range(n):
            if exps[i][j] != alpha[i]*beta[j]%n:
                return FullGaugeReport(n,False,'nonseparable Fourier exponent grid',(i,j),None,None,None,None)
    sqrt_n=modular_sqrt(n)
    left=[A[i][0]*sqrt_n%P for i in range(n)]
    right=[A[0][j]*pow(a00,-1,P)%P for j in range(n)]
    return FullGaugeReport(n,True,'exact outer monomial Fourier equivalence',None,alpha,beta,left,right)

def dense_from_oracle(oracle,n):
    C=[]
    for j in range(n):
        e=[0]*n;e[j]=1
        C.append(oracle(e))
    return [[C[j][i] for j in range(n)] for i in range(n)]

if __name__=='__main__':
    from weyl_gate import seeded_product,NearResonantGreen
    for n in (8,16,32,64):
        yes=MaskedPermutedFFT(n,17)
        y=cross_ratio_witness(yes,n)
        print(n,'control cross',y)
        good=full_monomial_gate(dense_from_oracle(yes,n))
        print(n,'control full',good.equivalent,good.reason)
        no=seeded_product(n,seed=17)
        z=cross_ratio_witness(no,n)
        print(n,'green cross',z)

@dataclass
class FingerprintReport:
    n:int
    excluded:bool
    reason:str
    column_pair:tuple[int,int]
    subgroup_index:int|None
    distinct_roots:int
    circuit_calls:int


def column_pair_fingerprint(oracle,n:int,cols=(0,1),anchor_row=0)->FingerprintReport:
    """O(N)-work necessary test for equivalence under *arbitrary outer*
    diagonal scalings and row/column permutations.

    The cross ratios of two columns, against one anchor row, must enumerate
    exactly a subgroup of Nth roots, each with the same multiplicity d,
    where d is a proper divisor of N. Not a sufficient test.
    """
    k,l=cols
    assert 0<=k<n and 0<=l<n and k!=l and 0<=anchor_row<n
    a=[0]*n;a[k]=1
    b=[0]*n;b[l]=1
    v0=oracle(a);v1=oracle(b)
    if any(u%P==0 or v%P==0 for u,v in zip(v0,v1)):
        return FingerprintReport(n,True,'one of two columns has a zero',cols,None,0,2)
    root=modular_root(n)
    dlog={pow(root,t,P):t for t in range(n)}
    ratio_base=v0[anchor_row]*pow(v1[anchor_row],-1,P)%P
    counter=[0]*n
    for j in range(n):
        ratio=v1[j]*pow(v0[j],-1,P)%P *ratio_base%P
        exponent=dlog.get(ratio)
        if exponent is None:
            return FingerprintReport(n,True,'cross ratio outside Nth roots',cols,None,0,2)
        counter[exponent]+=1
    d=1
    while d<n:
        if all(count==(d if i%d==0 else 0) for i,count in enumerate(counter)):
            return FingerprintReport(n,False,'valid necessary Fourier subgroup histogram',cols,d,n//d,2)
        d*=2
    return FingerprintReport(n,True,'invalid column-pair Fourier histogram',cols,None,sum(bool(v) for v in counter),2)
