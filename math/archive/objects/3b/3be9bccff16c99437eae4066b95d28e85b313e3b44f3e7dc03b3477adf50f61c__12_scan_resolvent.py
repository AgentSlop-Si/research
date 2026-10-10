"""Exact field implementation of homogeneous global scans, their cyclic bidiagonal
intertwiners, and Fourier control vectors. Only the Python standard library is used.
"""
from dataclasses import dataclass
from math import gcd

@dataclass(frozen=True)
class Scan:
    a: int  # strict lower constant
    b: int  # strict upper constant
    d: int  # diagonal constant


def apply_scan(s: Scan, x: list[int], p: int) -> list[int]:
    total = sum(x) % p
    prefix = 0
    y=[]
    for xi in x:
        suffix = (total-prefix-xi) % p
        y.append((s.a*prefix+s.d*xi+s.b*suffix) % p)
        prefix = (prefix+xi) % p
    return y


def orientation(s: Scan, p: int) -> str:
    if s.b % p:
        return '+'
    if s.a % p:
        return '-'
    return 'scalar'


def apply_K(s: Scan, x: list[int], p: int, direction: str) -> list[int]:
    n=len(x)
    if direction=='+':
        return [(s.b*x[i+1])%p for i in range(n-1)] + [s.a*x[0]%p]
    if direction=='-':
        return [s.b*x[-1]%p] + [(s.a*x[i-1])%p for i in range(1,n)]
    raise ValueError('orientation required')


def apply_B(s: Scan, x: list[int], p: int, direction: str=None) -> list[int]:
    direction=direction or orientation(s,p)
    weight = s.b if direction=='+' else s.a
    return [(ki-weight*xi)%p for ki,xi in zip(apply_K(s,x,p,direction),x)]


def apply_A(s: Scan, x: list[int], p: int, direction: str=None) -> list[int]:
    direction=direction or orientation(s,p)
    weight = s.b if direction=='+' else s.a
    other = s.a if direction=='+' else s.b
    return [((s.d-weight)*ki+weight*(other-s.d)*xi)%p for ki,xi in zip(apply_K(s,x,p,direction),x)]


def permute(x: list[int], order: list[int]):
    return [x[j] for j in order]


def inverse_perm(order):
    inv=[None]*len(order)
    for i,j in enumerate(order): inv[j]=i
    return inv


def primitive_root(p):
    factors=[]
    m=p-1
    for i in range(2,int(m**.5)+2):
        if m%i==0:
            factors.append(i)
            while m%i==0: m//=i
    if m>1: factors.append(m)
    return next(g for g in range(2,p) if all(pow(g,(p-1)//r,p)!=1 for r in factors))


def nth_root_of_unity(p, n):
    assert (p-1)%n==0
    return pow(primitive_root(p),(p-1)//n,p)


def apply_dft(x, w, p):
    n=len(x)
    return [sum(x[j]*pow(w,(i*j)%n,p) for j in range(n))%p for i in range(n)]


def e(n,j):
    result=[0]*n
    result[j]=1
    return result


def witness_column(s, n, p):
    # Special column of B that is a difference of adjacent coordinate impulses.
    direction=orientation(s,p)
    if direction=='+': return 1
    if direction=='-': return 0
    raise ValueError('scalar stage has no nonzero selected difference')


def interior(y, direction):
    return y[:-1] if direction=='+' else y[1:]


def two_stage_witness(s1,s2,n,p,w,permutation):
    src=e(n,witness_column(s1,n,p))
    lhs=apply_B(s2,apply_dft(apply_B(s1,src,p),w,p),p)
    rhs=apply_A(s2,permute(apply_A(s1,src,p),permutation),p)
    return {
        'lhs_interior_nonzero':sum(v%p!=0 for v in interior(lhs,orientation(s2,p))),
        'rhs_support':sum(v%p!=0 for v in rhs),
        'lhs':lhs,'rhs':rhs
    }


def three_stage_witness(s1,s2,s3,n,p,w,perm1,perm2):
    src=e(n,witness_column(s1,n,p))
    lhs=apply_B(s3,apply_dft(apply_B(s1,src,p),w,p),p)
    middle_input=permute(apply_A(s1,src,p),perm1)
    middle_output=apply_scan(s2,middle_input,p)
    toward_last=permute(middle_output,perm2)
    rhs=apply_A(s3,toward_last,p)
    inter=interior(rhs,orientation(s3,p))
    return {
        'lhs_interior_distinct':len(set(interior(lhs,orientation(s3,p)))),
        'rhs_interior_distinct':len(set(inter)),
        'middle_support':sum(x%p!=0 for x in middle_input),
        'middle_baseline_distinct':len(set(middle_output[i] for i,x in enumerate(middle_input) if x%p==0)),
        'lhs':lhs,'rhs':rhs,
    }


def circulant_gauge_test(s: Scan, q: int, p: int, n: int, w: int):
    """Check S D_q Fourier-column = lambda_k D_q Fourier-column.
       Requires a/b=q**n, q**n != 1, and b != 0.
    """
    assert s.b % p and (s.a - s.b)%p and s.a%p == (s.b*pow(q,n,p))%p
    out=[]
    for k in range(n):
        z=q*pow(w,k,p)%p
        assert z!=1
        lam=((s.d-s.b)*z+(s.a-s.d))*pow(z-1,-1,p)%p
        v=[pow(z,i,p) for i in range(n)]
        assert apply_scan(s,v,p)==[(lam*vi)%p for vi in v]
        out.append(lam)
    assert len(set(out))==n  # simple spectrum iff a != b
    return out
