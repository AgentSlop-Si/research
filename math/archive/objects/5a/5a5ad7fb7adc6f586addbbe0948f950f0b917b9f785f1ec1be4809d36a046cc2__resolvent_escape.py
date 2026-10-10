"""A charged, exact condition-budget escape mixer; not a Fourier transform.

K(M)=I+(I-M)^-1 for a weighted full cycle M with M^N=-I.
All field calls below are counted; addressing/cycle verification is O(N).
"""
from dataclasses import dataclass
from collections import Counter


class Counted:
    def __init__(self, field):
        self.field = field
        self.zero, self.one = field.zero, field.one
        self.count = Counter()
    def add(self, a, b):
        self.count['add'] += 1
        return self.field.add(a, b)
    def sub(self, a, b):
        self.count['sub'] += 1
        return self.field.sub(a, b)
    def mul(self, a, b):
        self.count['mul'] += 1
        return self.field.mul(a, b)
    def inv(self, a):
        self.count['inverse'] += 1
        return self.field.inv(a)


def cycle_order(permutation):
    n = len(permutation)
    if n < 1 or any(not isinstance(j,int) or j < 0 or j >= n for j in permutation):
        raise ValueError('not a permutation')
    order, seen, j = [], [False]*n, 0
    while not seen[j]:
        seen[j] = True; order.append(j); j = permutation[j]
    if j != 0 or len(order) != n:
        raise ValueError('one full cycle required')
    return tuple(order)


def cycle_solve(c, order, coefficients, rhs, closure_inverse):
    """Solve y_j=rhs_j+coefficients[j]*y_perm(j), exactly4N+1 gates."""
    value = c.zero
    for j in reversed(order):
        value = c.add(rhs[j], c.mul(coefficients[j], value))
    value = c.mul(value, closure_inverse)
    out = [c.zero]*len(order)
    for j in reversed(order):
        value = c.add(rhs[j], c.mul(coefficients[j], value))
        out[j] = value
    return out


@dataclass
class EscapePlan:
    n: int
    source: tuple
    target: tuple
    source_order: tuple
    target_order: tuple
    source_coefficients: tuple
    target_coefficients: tuple
    source_half_coefficients: tuple
    target_half_coefficients: tuple
    half: object
    half_closure_inverse: object
    preparation_counts: dict

    def apply(self, field, values, *, target=False, inverse=False):
        if len(values) != self.n:
            raise ValueError('wrong vector length')
        c = Counted(field)
        order = self.target_order if target else self.source_order
        if inverse:
            coefficients = self.target_half_coefficients if target else self.source_half_coefficients
            z = cycle_solve(c, order, coefficients, values, self.half_closure_inverse)
            result = [c.sub(x, c.mul(self.half, y)) for x,y in zip(values,z)]
        else:
            coefficients = self.target_coefficients if target else self.source_coefficients
            z = cycle_solve(c, order, coefficients, values, self.half)
            result = [c.add(x,y) for x,y in zip(values,z)]
        return result, dict(c.count)


def prepare_affine(field, n, q, a=5, b=1, shift=1):
    """Prepare source/target K and inverses:2N+log2(N)+4 field gates.

    Exact complex theorem; modular prototype rejects singular numerator.
    N>=2 dyadic. Descriptor is supplied as bounded integer words.
    """
    if n < 2 or n & (n-1):
        raise ValueError('dyadic N>=2 required')
    if any(not isinstance(x,int) for x in (a,b,shift)) or a%4 != 1 or b%2 != 1 or shift%2 != 1:
        raise ValueError('a=1 mod4 and odd b,shift required')
    a,b,shift = a%n,b%n,shift%n
    c = Counted(field)
    roots = [c.one]
    for _ in range(1,n): roots.append(c.mul(roots[-1],q))
    if c.mul(roots[-1],q) != c.one or roots[n//2] == c.one:
        raise ValueError('primitive Nth root required')
    two = c.add(c.one,c.one)
    if two == c.zero: raise ValueError('characteristic two excluded')
    half = c.inv(two)
    power = half
    for _ in range(n.bit_length()-1): power = c.mul(power,power)
    denominator = c.add(c.one,power)
    if denominator == c.zero:
        raise ValueError('singular numerator:2^N+1 vanishes in this field')
    half_closure_inverse = c.inv(denominator)
    half_roots = [c.mul(half,x) for x in roots]
    source = tuple((a*j+shift)%n for j in range(n))
    ai = pow(a,-1,n)
    target = tuple(ai*(k+b)%n for k in range(n))
    source_order, target_order = cycle_order(source), cycle_order(target)
    source_indices = [(b*j)%n for j in range(n)]
    target_indices = [(-shift*j)%n for j in target]
    return EscapePlan(n,source,target,source_order,target_order,
                      tuple(roots[e] for e in source_indices),tuple(roots[e] for e in target_indices),
                      tuple(half_roots[e] for e in source_indices),tuple(half_roots[e] for e in target_indices),
                      half,half_closure_inverse,dict(c.count))


def signed_cycle_forward(field, values):
    """K(C)x for C(x)=(x1,...,xN-1,-x0), including N=1.

    Cold cost is3N+1 gates:two setup gates plus3N-1 application gates.
    Uses only scalar1/2; no2^N coefficient is needed in this direction.
    """
    n = len(values)
    if not n: raise ValueError('nonempty vector required')
    c = Counted(field)
    two = c.add(c.one,c.one)
    if two == c.zero: raise ValueError('characteristic two excluded')
    half = c.inv(two)
    setup = dict(c.count)
    total = values[0]
    for x in values[1:]: total = c.add(total,x)
    z = c.mul(half,total)
    out = [c.add(values[0],z)]
    for i in range(1,n):
        z = c.sub(z,values[i-1])
        out.append(c.add(values[i],z))
    return out, dict(c.count), setup


def varying_rank_one_gauge_recognize(field, base, dressed, mm, inverse, rank):
    """Offline dense audit of layer-dependent rank<=1 intermediate gauges.

    This certifies only equivalence to supplied same-length baseline stages.
    Dense audit work is O(tN^3), explicitly not part of an O(N) evaluator.
    """
    if not base or len(base) != len(dressed):
        raise ValueError('matching nonempty stage lists required')
    n = len(base[0])
    identity = [[field.one if i==j else field.zero for j in range(n)] for i in range(n)]
    h = identity
    ranks = []
    for i,(b,g) in enumerate(zip(base,dressed)):
        try:
            h = mm(field,mm(field,g,h),inverse(field,b))
            inverse(field,h)
        except ValueError:
            return dict(match=False,reason='singular stage or gauge',stage=i)
        delta = [[field.sub(x,y) for x,y in zip(row,ident)] for row,ident in zip(h,identity)]
        r = rank(field,delta)
        ranks.append(r)
        if i+1 < len(base) and r > 1:
            return dict(match=False,reason='intermediate gauge rank exceeds one',stage=i,ranks=ranks)
    return dict(match=h==identity,reason='verified' if h==identity else 'final gauge does not cancel',ranks=ranks)
