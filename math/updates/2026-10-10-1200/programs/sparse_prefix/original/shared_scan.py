"""Exact sparse-endpoint cyclic scans and Fourier construction controls.

The evaluator is linear in the explicit plan size. No sub-N-log-N Fourier
plan family is supplied. The general Fourier constructor intentionally has
Theta(N^(3/2)) endpoint size at a balanced split.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import comb, gcd
from typing import Sequence

@dataclass
class Counts:
    additions: int = 0
    multiplications: int = 0
    inversions: int = 0
    @property
    def total(self) -> int:
        return self.additions + self.multiplications + self.inversions

SparseRows = list[list[tuple[int, int]]]

def distinct_prime_factors(n: int) -> list[int]:
    result=[]; d=2
    while d*d<=n:
        if n%d==0:
            result.append(d)
            while n%d==0:n//=d
        d+=1
    if n>1:result.append(n)
    return result

def root_of_order(n: int, p: int, generator: int) -> int:
    if n<1 or (p-1)%n:raise ValueError('Length must divide p-1.')
    w=pow(generator,(p-1)//n,p)
    if pow(w,n,p)!=1 or any(pow(w,n//d,p)==1 for d in distinct_prime_factors(n)):
        raise ValueError('The supplied generator did not yield a primitive root.')
    return w

def root_table(n: int, w: int, p: int) -> list[int]:
    if n<1 or pow(w,n,p)!=1 or any(pow(w,n//d,p)==1 for d in distinct_prime_factors(n)):
        raise ValueError('Nonprimitive supplied root.')
    out=[1]*n
    for j in range(1,n):out[j]=out[j-1]*w%p
    return out

def canonical_rows(rows: Sequence[Sequence[tuple[int,int]]], cols: int, p: int) -> SparseRows:
    result=[]
    for row in rows:
        acc={}
        for j,c in row:
            if not isinstance(j,int) or not 0<=j<cols:raise ValueError('Invalid sparse index.')
            acc[j]=(acc.get(j,0)+int(c))%p
        result.append([(j,c) for j,c in sorted(acc.items()) if c])
    return result

class ScanPlan:
    """T = R G C, G solves v_i = b_i + a_i v_(i-1 mod M)."""
    def __init__(self, n: int, p: int, weights: Sequence[int],
                 C: Sequence[Sequence[tuple[int,int]]],
                 R: Sequence[Sequence[tuple[int,int]]]):
        if n<1 or p<3 or not weights:raise ValueError('Bad dimensions or modulus.')
        self.n=n; self.p=p; self.a=[int(v)%p for v in weights]; self.m=len(weights)
        if len(C)!=self.m or len(R)!=n:raise ValueError('Sparse map dimensions do not agree.')
        self.C=canonical_rows(C,n,p); self.R=canonical_rows(R,self.m,p)
        self.setup=Counts()
        prod=1
        for a in self.a:prod=prod*a%p;self.setup.multiplications+=1
        den=(1-prod)%p;self.setup.additions+=1
        if not den:raise ValueError('Singular cycle: product of weights equals one.')
        self.invden=pow(den,p-2,p);self.setup.inversions+=1
        if den*self.invden%p!=1:raise ValueError('Modulus must be a field for this implementation.')
        self.input_degrees=[0]*n
        for row in self.C:
            for j,_ in row:self.input_degrees[j]+=1
        self.output_degrees=[len(row) for row in self.R]

    @property
    def nnz_C(self):return sum(self.input_degrees)
    @property
    def nnz_R(self):return sum(self.output_degrees)
    @property
    def expected_apply_ops(self):return 4*self.m+2*(self.nnz_C+self.nnz_R)+1

    def green(self, b: Sequence[int], count: Counts | None=None) -> list[int]:
        if len(b)!=self.m:raise ValueError('Bad forcing length.')
        c=count if count is not None else Counts();p=self.p
        tail=0
        for a,u in zip(self.a,b):
            tail=(a*tail+u)%p;c.multiplications+=1;c.additions+=1
        state=tail*self.invden%p;c.multiplications+=1
        out=[]
        for a,u in zip(self.a,b):
            state=(a*state+u)%p;c.multiplications+=1;c.additions+=1;out.append(state)
        return out

    def apply(self, x: Sequence[int]) -> tuple[list[int],Counts]:
        if len(x)!=self.n:raise ValueError('Bad input length.')
        p=self.p;c=Counts();b=[0]*self.m
        for i,row in enumerate(self.C):
            for j,a in row:b[i]=(b[i]+a*x[j])%p;c.additions+=1;c.multiplications+=1
        v=self.green(b,c);out=[0]*self.n
        for i,row in enumerate(self.R):
            for j,a in row:out[i]=(out[i]+a*v[j])%p;c.additions+=1;c.multiplications+=1
        assert c.total==self.expected_apply_ops
        return out,c

    def transpose_plan(self) -> 'ScanPlan':
        # Reverse internal order: J G^T J is a backward cyclic recurrence.
        # Q^T[i,i+1]=-a[i+1], so reversed weights are a[(M-i) mod M].
        m=self.m
        CT=[[] for _ in range(m)]
        RT=[[] for _ in range(self.n)]
        for i,row in enumerate(self.R):
            for j,a in row:CT[m-1-j].append((i,a))
        for i,row in enumerate(self.C):
            for j,a in row:RT[j].append((m-1-i,a))
        weights=[self.a[(m-i)%m] for i in range(m)]
        return ScanPlan(self.n,self.p,weights,CT,RT)

    def internal_columns(self, columns: Sequence[int]) -> list[list[int]]:
        # Expensive independent structural test helper, not a fast executor.
        data=[]
        for j in columns:
            b=[dict(row).get(j,0) for row in self.C]
            data.append(self.green(b))
        return [list(row) for row in zip(*data)]


def projective_key(v: Sequence[int],p: int) -> tuple[int,...] | None:
    for a in v:
        if a%p:
            inv=pow(a,p-2,p)
            return tuple(x*inv%p for x in v)
    return None

def capacity(r: int,s: int) -> int:
    if r<1 or s<1:return 0
    return min(r*comb((r+1)*s,r),s*comb((s+1)*r,s))

def minimum_equal_degree(n: int) -> int:
    if n<1:raise ValueError('n must be positive.')
    lo=1;hi=1
    while capacity(hi,hi)<n:hi*=2
    while lo<hi:
        mid=(lo+hi)//2
        if capacity(mid,mid)>=n:hi=mid
        else:lo=mid+1
    return lo

def histogram_checks(plan: ScanPlan) -> list[dict]:
    """Necessary tests only; passing does not imply Fourier equality."""
    out=[];n=plan.n
    for name,degin,degout in [('forward',plan.input_degrees,plan.output_degrees),
                              ('transpose',plan.output_degrees,plan.input_degrees)]:
        for r in range(1,n):
            k=r+1
            f=min(sum(degin[(i+j)%n] for j in range(k)) for i in range(n))
            targets=sum(d<=r for d in degout)
            # If f<k, full column rank already impossible.
            bound=r*comb(f,r) if f>=r else 0
            out.append(dict(direction=name,r=r,window_forcing_bound=f,low_degree_outputs=targets,
                            bound=bound,passes=(f>=k and targets<=bound)))
    return out

def fourier_two_plan(p: int) -> ScanPlan:
    return ScanPlan(2,p,[1,-1],[[(0,1)],[(1,1)]],[[(0,2)],[(1,-2)]])

def bitreverse(i: int,bits: int) -> int:
    out=0
    for _ in range(bits):out=(out<<1)|(i&1);i>>=1
    return out

def block_tour_plan(n: int,B: int,p: int,w: int) -> ScanPlan:
    """Exact mixed-radix control, not a sub-N-log-N plan.

    Each B-point child is walked through in bit-reversal output order.
    A projective scalar is chosen to balance input injection counts. The
    explicit input map still contains (2 B^2+1)/3 entries per child for dyadic B.
    All remaining output combinations are evaluated as explicit sparse sums.
    """
    if B<1 or B&(B-1) or n%B:raise ValueError('B must be a dyadic divisor.')
    roots=root_table(n,w,p);q=n//B;eta=[roots[(q*j)%n] for j in range(B)]
    order=[bitreverse(j,B.bit_length()-1) for j in range(B)];pos={k:j for j,k in enumerate(order)}
    gammas=[0];counts=[1]*B
    for j in range(1,B):
        delta=(order[j]-order[j-1])%B;period=B//gcd(delta,B)
        best=None
        for residue in range(period):
            after=[v+(u%period!=residue) for u,v in enumerate(counts)]
            score=(max(after),sum(v*v for v in after),residue)
            if best is None or score<best[0]:best=(score,residue,after)
        _,r,counts=best;gammas.append(eta[delta*r%B])
    C=[];weights=[]
    for t in range(q):
        prev=[0]*B
        for at,k in enumerate(order):
            gamma=gammas[at];cur=[eta[k*u%B] for u in range(B)]
            C.append([(t+q*u,(cur[u]-gamma*prev[u])%p) for u in range(B)
                      if (cur[u]-gamma*prev[u])%p])
            weights.append(gamma);prev=cur
    R=[]
    for k in range(n):
        R.append([(t*B+pos[k%B],roots[k*t%n]) for t in range(q)])
    return ScanPlan(n,p,weights,C,R)

def direct_dft(x: Sequence[int],w: int,p: int) -> list[int]:
    n=len(x)
    return [sum(x[j]*pow(w,j*k,p) for j in range(n))%p for k in range(n)]

def weyl_check(plan: ScanPlan,w: int) -> dict:
    n=plan.n;p=plan.p
    seed=plan.apply([1]+[0]*(n-1))[0]
    failures=[];cols=[]
    for j in range(n):
        e=[0]*n;e[j]=1;cols.append(plan.apply(e)[0])
    for j in range(n):
        for k in range(n):
            if cols[(j+1)%n][k] != pow(w,k,p)*cols[j][k]%p:
                failures.append((k,j))
    return dict(seed_ok=(seed==[1]*n),phase_failures=len(failures),
                exact_fourier=(seed==[1]*n and not failures))

def to_prefix(plan: ScanPlan) -> ScanPlan:
    """Convert a weighted cyclic scan to a fixed inclusive prefix scan.

    For nonzero cycle weights, output sparsity increases by at most one.
    When weights vanish, rotate at a zero and subtract block-boundary prefix
    values; output sparsity at most doubles. Input column sparsities do not
    increase. All setup is O(M + nnz(C) + nnz(R)) field/word work.
    """
    m=plan.m;p=plan.p
    zero=next((i for i,a in enumerate(plan.a) if a==0),None)
    start=zero if zero is not None else 0
    order=[(start+i)%m for i in range(m)]
    old_to_new={old:i for i,old in enumerate(order)}
    a=[plan.a[i] for i in order];w=[1]*m;boundary=[-1]*m
    for i in range(1,m):
        if a[i]==0:w[i]=1;boundary[i]=i-1
        else:w[i]=a[i]*w[i-1]%p;boundary[i]=boundary[i-1]
    # All w are nonzero, so these inversions are legitimate. The reference
    # uses M field inversions, still O(M) in the declared unit-cost field model.
    iw=[pow(v,p-2,p) for v in w]
    C=[[(j,c*iw[i]%p) for j,c in plan.C[order[i]]] for i in range(m)]
    R=[]
    if zero is None:
        eta=1
        for v in a:eta=eta*v%p
        rho=eta*plan.invden%p
        for row in plan.R:
            out=[];s=0
            for old,c in row:
                i=old_to_new[old];v=c*w[i]%p;out.append((i,v));s=(s+v)%p
            out.append((m-1,rho*s%p));R.append(out)
    else:
        for row in plan.R:
            out=[]
            for old,c in row:
                i=old_to_new[old];v=c*w[i]%p;out.append((i,v))
                if boundary[i]>=0:out.append((boundary[i],-v))
            R.append(out)
    return ScanPlan(plan.n,p,[0]+[1]*(m-1),C,R)

def fourier_four_plan(p: int,w: int) -> ScanPlan:
    if pow(w,2,p)!=p-1:raise ValueError('Need primitive fourth root.')
    # States: x0, x0+x2, x0-x2, x1, x1+x3, x1-x3.
    C=[[(0,1)],[(2,1)],[(2,-2)],[(1,1)],[(3,1)],[(3,-2)]]
    R=[[(1,1),(4,1)],[(2,1),(5,w)],[(1,1),(4,-1)],[(2,1),(5,-w)]]
    return ScanPlan(4,p,[0,1,1,0,1,1],C,R)
