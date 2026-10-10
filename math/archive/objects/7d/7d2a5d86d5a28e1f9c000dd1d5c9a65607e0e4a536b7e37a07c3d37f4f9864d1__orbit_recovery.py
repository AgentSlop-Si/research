"""Exact cyclotomic/orbit certificates for fresh binary-input DFTs.

All vector FFT values are represented in Z[zeta_N], in the power basis
1,zeta,...,zeta^(N/2-1) with zeta^(N/2)=-1 for N=2^L.
No numerical FFT, complex-roundoff, parallel execution or prior transform cache.
"""
from __future__ import annotations
from itertools import product


def validate_n(n: int) -> None:
    if n < 2 or n & (n-1):
        raise ValueError('N must be a power of two >= 2')


def frequency_conductor(n: int, k: int) -> int:
    validate_n(n)
    if not (0 <= k < n):
        raise ValueError('bad frequency')
    return 1 if k == 0 else n // (k & -k)


def orbits(n: int) -> dict[int, tuple[int, ...]]:
    validate_n(n)
    return {m: tuple(k for k in range(n) if frequency_conductor(n, k) == m)
            for m in [1] + [1 << j for j in range(1, n.bit_length())]}


def representatives(n: int) -> tuple[int, ...]:
    """One frequency per cyclotomic orbit: 0 and the powers of two below N."""
    validate_n(n)
    return (0,) + tuple(n//m for m in (1 << j for j in range(1,n.bit_length())))


def root_power(n: int, exponent: int) -> tuple[int, ...]:
    """Exactly zeta_N**exponent in the cyclotomic integer power basis."""
    validate_n(n)
    m = n // 2
    exponent %= n
    out = [0]*m
    out[exponent % m] = 1 if exponent < m else -1
    return tuple(out)


def dft_bin_exact(x: list[int] | tuple[int, ...], k: int) -> tuple[int, ...]:
    n = len(x)
    validate_n(n)
    if not (0 <= k < n):
        raise ValueError('bad frequency')
    m=n//2
    y=[0]*m
    for j,value in enumerate(x):
        exponent=(j*k)%n
        y[exponent % m] += int(value) * (1 if exponent < m else -1)
    return tuple(y)


def dft_selected_exact(x, qs):
    return tuple(dft_bin_exact(x, k) for k in qs)


def binary_collision_family(n: int, conductor: int, mask: int) -> list[int]:
    """2^phi(conductor) different binary inputs indistinguishable off that orbit.

    m=1: zero or all-one vectors; otherwise periodic swapped pairs:
    x[r] = bit, x[r+m/2]=1-bit, repeated every m positions.
    """
    validate_n(n)
    if conductor < 1 or conductor > n or conductor & (conductor - 1):
        raise ValueError('conductor must divide N and be a power of two')
    if conductor == 1:
        if mask not in (0,1):
            raise ValueError('one bit for conductor 1')
        return [mask]*n
    m=conductor
    half=m//2
    if not 0 <= mask < 1<<half:
        raise ValueError('invalid mask')
    pattern = [0]*m
    for j in range(half):
        bit=(mask>>j)&1
        pattern[j]=bit
        pattern[j+half]=1-bit
    return pattern*(n//m)


def binary_coset_collision_witness(n: int, conductor: int):
    """Explicit pair of distinct binary vectors whose FFT difference lives
    solely in one conductor orbit."""
    a=binary_collision_family(n,conductor,0)
    b=binary_collision_family(n,conductor,1)
    assert a!=b
    return a,b


def orbit_support_of_difference(a,b):
    if len(a)!=len(b):
        raise ValueError('unequal lengths')
    n=len(a)
    v=[x-y for x,y in zip(a,b)]
    return tuple(k for k in range(n) if any(dft_bin_exact(v,k)))


def subset_sum_cyclotomic_coeffs(n: int, mask: int):
    """Alpha(mask) = sum_{j < N/2} mask_j * zeta_N^j."""
    validate_n(n)
    m=n//2
    if not 0<=mask<1<<m:
        raise ValueError('invalid mask')
    return tuple((mask>>j)&1 for j in range(m))


def target_conjugate_coeffs(n: int, u: int, mask: int):
    validate_n(n)
    m=n//2
    if u%2!=1 or u%n==1:
        raise ValueError('use nontrivial odd u')
    y=[0]*m
    for j in range(m):
        if (mask>>j)&1:
            e=(u*j)%n
            y[e%m]+=1 if e<m else -1
    return tuple(y)


def lower_bounds(n: int) -> dict:
    """Lower bounds for P(alpha) or P(alpha)/Q(alpha) = beta,
    based on 2^(m-1) distinct subsets of the other m-1 coordinates."""
    validate_n(n)
    if n<4:
        raise ValueError('N >= 4 required')
    m=n//2
    return {'N':n,'m':m,
            'poly_degree_lower_bound':(1<<(m-1))+1,
            'rational_num_den_degree_lower_bound':1<<(m-2),
            'rational_circuit_gate_lower_bound':m-2}
