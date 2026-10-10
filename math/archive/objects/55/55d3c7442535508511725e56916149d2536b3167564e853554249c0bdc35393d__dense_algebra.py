"""Phase 12: exact, fresh-input polynomial convolution methods.

Three algorithms are deliberately separated:
- schoolbook: n^2 input-dependent coefficient multiplications;
- Karatsuba: 3^(log_2 n) products for power-of-two length, for ALL inputs;
- evaluation/interpolation: 2n-1 input-dependent bilinear products, and
  O(n^2) surrounding field operations. This is multiplication-count optimal
  but it is NOT a sub-nlogn algorithm.

All algorithms calculate linear (not circular) convolution modulo a prime.
No caches, threads, input structure assumptions, or approximate arithmetic.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import comb
from typing import Sequence

DEFAULT_P = 998244353

@dataclass(frozen=True)
class ArithmeticResult:
    coeffs: tuple[int, ...]
    bilinear_products: int
    method: str


def schoolbook(a: Sequence[int], b: Sequence[int], p: int = DEFAULT_P) -> ArithmeticResult:
    if not a or not b:
        raise ValueError('nonempty polynomials required')
    out = [0] * (len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] = (out[i+j] + int(x)*int(y)) % p
    return ArithmeticResult(tuple(out),len(a)*len(b),'schoolbook')


def karatsuba(a: Sequence[int], b: Sequence[int], p: int = DEFAULT_P,
              threshold: int = 1) -> ArithmeticResult:
    """Works on any nonempty lengths. Counts products at schoolbook leaves."""
    if not a or not b or threshold < 1:
        raise ValueError('nonempty polynomials and threshold>=1 required')
    n=1<<(max(len(a),len(b))-1).bit_length()
    x=[int(v)%p for v in a]+[0]*(n-len(a))
    y=[int(v)%p for v in b]+[0]*(n-len(b))
    def recurse(x, y):
        z=len(x)
        if z<=threshold:
            prod=[0]*(2*z-1)
            for i,u in enumerate(x):
                for j,v in enumerate(y):
                    prod[i+j]=(prod[i+j]+u*v)%p
            return prod,z*z
        mid=z//2
        low,lowcost=recurse(x[:mid],y[:mid])
        high,highcost=recurse(x[mid:],y[mid:])
        sx=[(x[i]+x[i+mid])%p for i in range(mid)]
        sy=[(y[i]+y[i+mid])%p for i in range(mid)]
        middle,midcost=recurse(sx,sy)
        for i in range(len(middle)):
            middle[i]=(middle[i]-low[i]-high[i])%p
        out=[0]*(2*z-1)
        for i in range(len(low)):
            out[i]=(out[i]+low[i])%p
            out[i+mid]=(out[i+mid]+middle[i])%p
            out[i+z]=(out[i+z]+high[i])%p
        return out,lowcost+highcost+midcost
    product,count=recurse(x,y)
    return ArithmeticResult(tuple(product[:len(a)+len(b)-1]),count,'karatsuba')


def interpolation_product(a: Sequence[int], b: Sequence[int],
                          p: int = DEFAULT_P) -> ArithmeticResult:
    """Exact evaluation/interpolation using 2n-1 distinct field points.

    Bilinear multiplication count is m=len(a)+len(b)-1, and is optimal
    for two n-coefficient inputs (when lengths equal n) in bilinear rank.
    Evaluation/interpolation add O(m^2) scalar arithmetic; counted separately
    conceptually, not in bilinear_products.
    """
    if not a or not b:
        raise ValueError('nonempty polynomials required')
    m=len(a)+len(b)-1
    if not 1 < p or m > p:
        raise ValueError('prime modulus must provide at least m evaluation points')
    aa=[int(x)%p for x in a];bb=[int(x)%p for x in b]
    def eval_horner(c,t):
        v=0
        for ci in reversed(c):
            v=(v*t+ci)%p
        return v
    # m input-dependent products, one for each evaluation point.
    values=[(eval_horner(aa,t)*eval_horner(bb,t))%p for t in range(m)]
    # For consecutive points x_i=i, denominators x_i-x_(i-order)=order.
    # A single inverse is needed for each order. The standard O(m) recurrence
    # builds those inverses when m<p and p is prime.
    inv=[0]*max(2,m)
    inv[1]=1
    for z in range(2,m):
        inv[z]=(p-(p//z)*inv[p%z]%p)%p
    # Newton divided differences computed in place, descending index.
    d=values[:]
    for order in range(1,m):
        inverse=inv[order]
        for i in range(m-1,order-1,-1):
            d[i]=(d[i]-d[i-1])*inverse%p
    # Convert Newton form to monomial coefficients using Horner in x.
    coefficients=[d[-1]]
    for j in range(m-2,-1,-1):
        new=[0]*(len(coefficients)+1)
        for i,v in enumerate(coefficients):
            new[i]=(new[i]-j*v)%p
            new[i+1]=(new[i+1]+v)%p
        new[0]=(new[0]+d[j])%p
        coefficients=new
    return ArithmeticResult(tuple(coefficients),m,'evaluation-interpolation')


def operation_counts(n:int)->dict[str,int]:
    if n<1 or n&(n-1):
        raise ValueError('n must be a positive power of two')
    m=2*n-1
    return {'n':n,'schoolbook_bilinear':n*n,
            'karatsuba_bilinear':3**(n.bit_length()-1),
            'evaluation_bilinear':m,
            'radix2_ntt_bilinear':1<<(m-1).bit_length(),
            'naive_eval_linear_ops_order':m*n,
            'naive_interpolation_linear_ops_order':m*m}


def coverage_bound(n:int, r:int, k:int, families:int)->dict[str,int|float]:
    """Union bound for M affine subspaces, each of dimension <=r,
    plus residual vectors of Hamming weight <=k in F2^n."""
    if not (0<=r<=n and 0<=k<=n and families>=1):
        raise ValueError('invalid parameters')
    ball=sum(comb(n,j) for j in range(k+1))
    covered_upper=min(1<<n,families*(1<<r)*ball)
    return {'n':n,'r':r,'k':k,'families':families,
            'hamming_ball':ball,'covered_upper':covered_upper,
            'uncovered_lower':(1<<n)-covered_upper,
            'covered_fraction_upper':covered_upper/(1<<n)}
