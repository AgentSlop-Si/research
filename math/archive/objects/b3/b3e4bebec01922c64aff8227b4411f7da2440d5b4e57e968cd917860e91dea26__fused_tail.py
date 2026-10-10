"""Exact high-degree q-Weyl tail fusion, using only the standard library.

The root q is supplied. This is an exact-field operation audit, not a bit-cost
claim. The full-degree case remains quadratic.
"""
from collections import Counter
from dataclasses import dataclass


class Field:
    def __init__(self, prime):
        self.prime = prime
        self.count = Counter()

    def mul(self, a, b):
        self.count['mul'] += 1
        return a*b % self.prime

    def sub(self, a, b):
        self.count['sub'] += 1
        return (a-b) % self.prime

    def add(self, a, b):
        self.count['add'] += 1
        return (a+b) % self.prime

    def neg(self, a):
        self.count['neg'] += 1
        return -a % self.prime

    def inv(self, a):
        self.count['constant_inverse'] += 1
        return pow(a, -1, self.prime)


@dataclass
class Plan:
    prime: int
    n: int
    r: int
    q: int
    kernel: list
    tail_coefficients: list
    tail_matrix: list
    preparation: dict
    inverse_n: int
    root_powers: list
    upper: list
    rank_one_kernel: list | None = None


def prepare(prime, n, r, q, tail_coefficients=None):
    """Prepare p supported on degrees N-r,...,N-1. None selects the H_q tail.

    Primitive-root validity is a precondition, checked by the independent audit.
    Every actual preparation field operation is counted below.
"""
    if n < 2 or n & (n-1) or not 1 <= r <= n:
        raise ValueError('require power-of-two N >= 2 and 1 <= r <= N')
    f = Field(prime)
    powers = [1]
    for _ in range(1,n):
        powers.append(f.mul(powers[-1],q))
    factors = [1] + [f.sub(1,powers[j]) for j in range(1,n)]
    factorial = [1]
    for j in range(1,n):
        factorial.append(f.mul(factorial[-1],factors[j]))
    half, inverse_n = f.inv(2), 1
    for _ in range(n.bit_length()-1):
        inverse_n = f.mul(inverse_n,half)
    kernel, suffix = [0]*n, 1
    for j in reversed(range(n)):
        kernel[j] = f.mul(suffix,inverse_n)
        if j:
            suffix = f.mul(suffix,factors[j])
    chirp, inverse_prefix = 1, []
    for j in range(n):
        inverse_prefix.append(f.mul(chirp,kernel[j]))
        if j+1 < n:
            chirp = f.neg(f.mul(chirp,powers[j]))
    upper = [f.sub(q,powers[(-j)%n]) for j in range(n-1)]
    prefix = [1]
    for edge in upper:
        prefix.append(f.mul(prefix[-1],edge))
    coefficients = kernel[n-r:] if tail_coefficients is None else list(tail_coefficients)
    if len(coefficients) != r:
        raise ValueError('tail coefficient list must have length r')
    matrix = []
    for i in range(r):
        row = []
        for ell in range(i,r):
            j = n-r+ell
            weight = f.mul(prefix[j],inverse_prefix[i])
            row.append(f.mul(coefficients[ell-i],weight))
        matrix.append(row)
    return Plan(prime,n,r,q,kernel,coefficients,matrix,dict(f.count),
                inverse_n,powers,upper)


def apply(plan,x):
    """p(C)H_q(A)x = H_q(A)p(B)x, with complete N-entry output."""
    if len(x) != plan.n:
        raise ValueError('wrong input length')
    n,r = plan.n,plan.r
    f = Field(plan.prime)
    intermediate = []
    for i in range(r):
        value = f.mul(plan.tail_matrix[i][0],x[n-r+i])
        for ell in range(i+1,r):
            value = f.add(value,f.mul(plan.tail_matrix[i][ell-i],x[n-r+ell]))
        intermediate.append(value)
    out = []
    for i in range(n):
        value = f.mul(plan.kernel[i],intermediate[0])
        for j in range(1,min(i+1,r)):
            value = f.add(value,f.mul(plan.kernel[i-j],intermediate[j]))
        out.append(value)
    inner_terms = r*(r+1)//2
    output_terms = n*r-r*(r-1)//2
    return out, {'field_operations':dict(f.count),
        'input_reads':inner_terms,'input_coordinates_used':r,
        'prepared_coefficient_reads':inner_terms+output_terms,
        'intermediate_reads':output_terms,'intermediate_writes':r,
        'output_writes':n}


def prepare_rank_one(plan):
    if plan.r != 1:
        raise ValueError('rank-one specialization needs r=1')
    f = Field(plan.prime)
    plan.rank_one_kernel = [f.mul(t,plan.tail_matrix[0][0]) for t in plan.kernel]
    return dict(f.count)


def apply_rank_one(plan,x):
    if len(x) != plan.n or plan.rank_one_kernel is None:
        raise ValueError('wrong input length or unprepared specialization')
    f = Field(plan.prime)
    scalar = x[-1]
    out = [f.mul(value,scalar) for value in plan.rank_one_kernel]
    return out, {'field_operations':dict(f.count),'input_reads':1,
                 'coefficient_reads':plan.n,'output_writes':plan.n}


def oracle_h_a(plan,x):
    """Quadratic independent lower-convolution oracle; no FFT backend."""
    return [sum(plan.kernel[i-j]*x[j] for j in range(i+1)) % plan.prime
            for i in range(plan.n)]


def oracle_c(plan,x):
    n,p = plan.n,plan.prime
    out = [(plan.root_powers[(-i)%n]*x[i]+plan.upper[i]*x[i+1]) % p
           for i in range(n-1)]
    out.append((plan.q*x[-1]-plan.q*plan.inverse_n*x[0]) % p)
    return out


def oracle_fused_tail(plan,x):
    """Literal degree-(N-1) polynomial in C after a full H_q(A) action."""
    y = oracle_h_a(plan,x)
    coefficients = [0]*(plan.n-plan.r)+plan.tail_coefficients
    out = [coefficients[-1]*entry % plan.prime for entry in y]
    for coefficient in reversed(coefficients[:-1]):
        out = [(a+coefficient*b) % plan.prime
               for a,b in zip(oracle_c(plan,out),y)]
    return out
