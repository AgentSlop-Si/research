"""Independent exact arithmetic used only to challenge the fresh ALG-034 contract.

This does not run, emulate, certify, or authenticate a numerical producer.
It recomputes the already accepted finite policy for small test cases.
"""

from functools import lru_cache
from math import comb, gcd, lcm


def trim(a):
    a = list(a)
    while a and a[-1] == 0:
        a.pop()
    return a


def quotient_remainder(a, b):
    a, b = trim(a), trim(b)
    assert b and b[-1] == 1
    q = [0] * max(0, len(a) - len(b) + 1)
    while len(a) >= len(b):
        k = len(a) - len(b)
        c = a[-1]
        q[k] = c
        for j, bj in enumerate(b):
            a[j + k] -= c * bj
        a = trim(a)
    return trim(q), a


@lru_cache(None)
def cyclotomic(n):
    a = [-1] + [0] * (n - 1) + [1]
    for d in range(1, n):
        if n % d == 0:
            a, r = quotient_remainder(a, cyclotomic(d))
            assert not r
    return tuple(a)


def canonical_dyadics(real, imag, exponent):
    assert type(exponent) is int
    assert type(real) is list and type(imag) is list and len(real) == len(imag)
    assert all(type(x) is int for x in real + imag)
    nonzero = [abs(x) for x in real + imag if x]
    if not nonzero:
        return list(real), list(imag), 0
    trailing = min((x & -x).bit_length() - 1 for x in nonzero)
    return [x >> trailing for x in real], [x >> trailing for x in imag], exponent - trailing


def policy(real, imag, exponent, n, blocks, a, beta, t, q):
    assert type(n) is int and n >= 3
    assert type(blocks) is int and 3 <= blocks <= n
    assert type(a) is int and 0 < a < n and gcd(a, n) == 1
    assert type(beta) is int and 0 <= beta < n
    assert type(t) is int and t >= 0
    assert type(q) is int and q >= (n - 1).bit_length()
    assert len(real) == len(imag) == n
    assert type(exponent) is int
    assert all(type(x) is int for x in real + imag)
    width = max(abs(x).bit_length() for x in real + imag)
    lengths = [n // blocks + (i < n % blocks) for i in range(blocks)]
    starts = []
    s = 0
    for length in lengths:
        starts.append(s)
        s += length
    common = dict(N=n, B=blocks, a=a, beta=beta, F=exponent, W=width,
                  t=t, q=q, lengths=lengths, starts=starts)
    if width == 0:
        return dict(common, branch="EXACT_INPUT_ZERO")
    order = lcm(2 * n, 4)
    phi = cyclotomic(order)
    masses = []
    remainders = []
    polynomials = []
    for start, length in zip(starts, lengths):
        polynomial = [0] * order
        for offset in range(length):
            phase = (a * offset * (offset - 1) +
                     2 * (a * start + beta) * offset + (n % 2) * offset) % (2 * n)
            j = ((order // (2 * n)) * phase) % order
            polynomial[j] += real[start + offset]
            polynomial[(j + order // 4) % order] += imag[start + offset]
        remainder = quotient_remainder(polynomial, phi)[1]
        polynomials.append(polynomial)
        remainders.append(remainder)
        masses.append(sum(map(abs, polynomial)))
    common.update(L=order, D=len(phi) - 1, phi=list(phi),
                  polynomials=polynomials, remainders=remainders, masses=masses)
    eligible = [(masses[i], i) for i, r in enumerate(remainders) if r]
    if not eligible:
        return dict(common, branch="EXACT_PROJECTED_ZERO")
    mass, witness = min(eligible)
    k = (mass - 1).bit_length()
    g = width + (len(phi) - 2) * k
    h = min(comb(n + blocks - 1, blocks), 1 << (n - blocks))
    c_full = 64 * h * blocks * (1 << blocks) * n * n
    c = (c_full - 1).bit_length()
    p_min = max(width, c + t + 1, c + q + g + 2)
    return dict(common, branch="NONZERO_PLAN", A=mass, selected_block=witness,
                K=k, G=g, H=h, C=c_full, c=c, p_min=p_min)
