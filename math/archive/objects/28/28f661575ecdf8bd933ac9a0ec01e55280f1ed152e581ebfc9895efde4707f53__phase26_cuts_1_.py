"""Phase 26: exact simultaneous modular cuts for affine-run cyclic Green circuits.

Mathematical scope: power-of-two N, cycles with bounded affine increments,
products of sums of their Green resolvents, arbitrary diagonal gates/gauges,
external monomial gauges. No internal arbitrary coordinate permutations.

Does not construct a faster general FFT.
"""
from __future__ import annotations
from dataclasses import dataclass
import math

P = 998244353


def int_root_floor(value: int, degree: int) -> int:
    if value < 1 or degree < 1:
        raise ValueError('positive value and degree required')
    lo, hi = 1, value + 1
    while lo + 1 < hi:
        mid = (lo + hi)//2
        if mid**degree <= value:
            lo = mid
        else:
            hi = mid
    return lo


def signed_residue(x: int, n: int) -> int:
    r = x % n
    return r if r <= n//2 else r-n


def simultaneous_cut(n: int, strides: list[int]) -> tuple[int,int, list[int]]:
    """Construct k, r, and actual modular shifts. r^s < N via pigeonhole.

    k is nonzero mod N and satisfies |k*a_i mod N| <= floor(N/r)
    with centred residues. A simple O(sN) exhaustive witness search is used
    for reproducibility; this is a structural audit, not the FFT executor.
    """
    if n < 4 or n & (n - 1):
        raise ValueError('power of two n>=4 required')
    distinct = sorted({a % n for a in strides if a % n})
    if not distinct:
        return (1, n-1, [])
    s = len(distinct)
    r = int_root_floor(n-1, s)
    threshold = n/r
    for k in range(1, n):
        h = [signed_residue(k*a, n) for a in distinct]
        if all(abs(t) < threshold + 1e-12 for t in h):
            return k, r, h
    raise AssertionError('simultaneous pigeonhole guarantee failed')


def optimal_phase_cut(n: int, strides: list[int]) -> tuple[int,int]:
    """Find min sum of translation-boundary sizes over nonzero frequencies.

    Offline O(s*N) diagnostic, not an algorithm for computing arbitrary DFTs.
    """
    distinct = sorted({a%n for a in strides if a % n})
    candidates=((sum(abs(signed_residue(k*a,n)) for a in distinct), k)
                for k in range(1,n))
    score,k = min(candidates)
    return k,score


def phase_partition(n:int,k:int)->tuple[list[int],list[int]]:
    if n < 4 or (n & (n-1)) or not 0 < k < n:
        raise ValueError('power-of-two size and nonzero frequency required')
    a=[j for j in range(n) if (k*j % n) < n//2]
    b=[j for j in range(n) if (k*j % n) >= n//2]
    if len(a)!=n//2 or len(b)!=n//2:
        raise AssertionError('unbalanced Fourier-character cut')
    return a,b


def successor(order:list[int])->list[int]:
    n=len(order)
    if set(order)!=set(range(n)):
        raise ValueError('order must permute vertices')
    s=[0]*n
    for t,j in enumerate(order):
        s[j]=order[(t+1)%n]
    return s


def two_run_zigzag(n:int,a:int)->list[int]:
    if n<8 or n & (n-1) or a%2 or math.gcd(a//2,n//2)!=1:
        raise ValueError('even stride a=2u with odd u required')
    m=n//2
    order=[a*t%n for t in range(m)]+[(n-1-a*t)%n for t in range(m)]
    assert len(set(order))==n
    return order


def generic_cycle(n:int,seed:int)->list[int]:
    import random
    rng=random.Random(seed)
    out=list(range(n))
    rng.shuffle(out)
    return out


def crossing_edges(order:list[int],left:list[int],right:list[int])->int:
    s=successor(order)
    L=set(left)
    return sum(s[j] in L for j in right)


def translation_crossing(n:int,k:int,stride:int)->int:
    left,right=phase_partition(n,k)
    L=set(left)
    return sum(((j+stride)%n in L) for j in right)


def affine_edge_defects(order:list[int], steps:list[int])->int:
    """Number of edges not matching an allowed circular translation."""
    n=len(order)
    S={a%n for a in steps}
    s=successor(order)
    return sum((s[j]-j)%n not in S for j in range(n))


def green_apply(order:list[int],alpha:int,x:list[int],p:int=P)->list[int]:
    """(I-alpha W)^-1 x via a single circular first-order recurrence."""
    n=len(order)
    if len(x)!=n:
        raise ValueError('dimension mismatch')
    alpha%=p
    den=(1-pow(alpha,n,p))%p
    if not den:
        raise ArithmeticError('singular cyclic Green operator')
    # y_last*(1-alpha^n) = sum_s alpha^(n-1-s) b_s
    t=0
    for j in order:
        t=(alpha*t+x[j])%p
    y_last=t*pow(den,-1,p)%p
    out=[0]*n
    previous=y_last
    for j in order:
        previous=(alpha*previous+x[j])%p
        out[j]=previous
    assert previous==y_last
    return out


@dataclass
class Term:
    order:list[int]
    alpha:int
    left:list[int] | None = None
    right:list[int] | None = None
    coeff:int=1

    def apply(self,x:list[int],p:int=P)->list[int]:
        n=len(x)
        y=[x[i]*self.right[i]%p for i in range(n)] if self.right else x
        out=green_apply(self.order,self.alpha,y,p)
        if self.left:
            out=[out[i]*self.left[i]%p for i in range(n)]
        if self.coeff!=1:
            out=[v*self.coeff%p for v in out]
        return out


@dataclass
class Layer:
    terms:list[Term]
    diag:list[int] | None=None

    def apply(self,x:list[int],p:int=P)->list[int]:
        n=len(x)
        result=[0]*n
        for term in self.terms:
            y=term.apply(x,p)
            result=[(a+b)%p for a,b in zip(result,y)]
        if self.diag:
            result=[v*self.diag[i]%p for i,v in enumerate(result)]
        return result


def circuit_apply(x:list[int],layers:list[Layer],p:int=P)->list[int]:
    result=x
    for layer in layers:
        result=layer.apply(result,p)
    return result


def cut_rank_upper(layers:list[Layer],left:list[int],right:list[int])->int:
    # Sum-of-products cut-rank inequality.
    return sum(crossing_edges(term.order,left,right)
               for layer in layers for term in layer.terms)


def cut_minor(layers:list[Layer],left:list[int],right:list[int],p:int=P)->list[list[int]]:
    n=len(left)+len(right)
    out=[[0]*len(right) for _ in left]
    for col,j in enumerate(right):
        e=[0]*n;e[j]=1
        result=circuit_apply(e,layers,p)
        for row,i in enumerate(left):
            out[row][col]=result[i]
    return out


def mod_rank(matrix:list[list[int]],p:int=P)->int:
    if not matrix:
        return 0
    a=[row.copy() for row in matrix]
    nr=len(a);nc=len(a[0]);rank=0
    for col in range(nc):
        pivot=next((j for j in range(rank,nr) if a[j][col]%p),None)
        if pivot is None:
            continue
        a[rank],a[pivot]=a[pivot],a[rank]
        inv=pow(a[rank][col]%p,-1,p)
        for k in range(col,nc):a[rank][k]=a[rank][k]*inv%p
        for i in range(rank+1,nr):
            v=a[i][col]%p
            if v:
                for k in range(col,nc):a[i][k]=(a[i][k]-v*a[rank][k])%p
        rank+=1
        if rank==nr:break
    return rank


def fourier_rank_minimum(n:int)->int:
    if n%4:raise ValueError('n divisible by 4 required')
    return n//4


def error_floor(n:int,cutrank:int)->float:
    if not 0<=cutrank<n//2:raise ValueError('bad rank')
    return math.sqrt(max(0.0,(n/4-cutrank)/(n/2-cutrank)))


def denominator_edge_bound(n:int,k:int,steps:list[int],exceptions:int)->int:
    """For a Hamiltonian cycle using edges from +-steps except exceptions.

    Translating by each signed stride crosses the balanced phase cut in
    exactly the absolute centered residue. Use union bound per sign.
    """
    return min(n//2,2*sum(abs(signed_residue(k*a,n)) for a in steps)+exceptions)


def affine_permutation(n:int,u:int,b:int)->list[int]:
    if n<4 or math.gcd(u,n)!=1:
        raise ValueError('invertible affine permutation multiplier required')
    return [(u*j+b)%n for j in range(n)]


def permute_apply(p:list[int],x:list[int])->list[int]:
    out=[0]*len(x)
    for j,v in enumerate(x):
        out[p[j]]=v
    return out


def exact_coarse_cut_bound(n:int,term_count:int,stride_count:int,bridges_per_term:int=2)->tuple[int,int]:
    """Integer ceiling of 2Q N / r + B, r=floor((N-1)^(1/s)).

    Assumes each term's cycle has edges of slopes +-one of s strides,
    except <= bridges_per_term exceptional edges. No unstructured
    intermediate permutations.
    """
    r=int_root_floor(n-1,stride_count)
    return ((2*term_count*n+r-1)//r+bridges_per_term*term_count,r)


def forbidden_by_coarse_cut(n:int,Q:int,s:int|None=None,bridges_per_term:int=2)->bool:
    if s is None:s=Q
    value,_=exact_coarse_cut_bound(n,Q,s,bridges_per_term)
    return value<n//4


def weighted_green_apply(order:list[int],weights:list[int],x:list[int],p:int=P)->list[int]:
    """Solve [I-diag(weights)*W]y=x in O(N), W the cyclic successor.

    Works for highly nonnormal/nonstationary cyclic systems. No restriction on
    weights except 1-product(weights) != 0 in the coefficient field.
    """
    n=len(order)
    if len(weights)!=n or len(x)!=n:
        raise ValueError('dimension mismatch')
    v=0; product=1
    for j in order:
        w=weights[j]%p
        v=(w*v+x[j])%p
        product=product*w%p
    den=(1-product)%p
    if not den:
        raise ArithmeticError('singular weighted cyclic Green operator')
    final=v*pow(den,-1,p)%p
    result=[0]*n
    prev=final
    for j in order:
        prev=(weights[j]*prev+x[j])%p
        result[j]=prev
    assert prev==final
    return result


@dataclass
class WeightedTerm:
    order:list[int]
    weights:list[int]
    left:list[int] | None=None
    right:list[int] | None=None
    coeff:int=1

    def apply(self,x:list[int],p:int=P)->list[int]:
        n=len(x)
        y=[x[i]*self.right[i]%p for i in range(n)] if self.right else x
        out=weighted_green_apply(self.order,self.weights,y,p)
        if self.left:
            out=[out[i]*self.left[i]%p for i in range(n)]
        if self.coeff!=1:
            out=[v*self.coeff%p for v in out]
        return out


def conjugate_affine_layer(layer:Layer,p:list[int])->Layer:
    n=len(p)
    def diag_permute(d):
        if d is None: return None
        out=[0]*n
        for j,v in enumerate(d):out[p[j]]=v
        return out
    terms=[]
    for term in layer.terms:
        if isinstance(term,WeightedTerm):
            terms.append(WeightedTerm([p[j] for j in term.order],
                                      diag_permute(term.weights),
                                      diag_permute(term.left),
                                      diag_permute(term.right),term.coeff))
        else:
            terms.append(Term([p[j] for j in term.order],term.alpha,
                              diag_permute(term.left),diag_permute(term.right),term.coeff))
    return Layer(terms,diag_permute(layer.diag))
