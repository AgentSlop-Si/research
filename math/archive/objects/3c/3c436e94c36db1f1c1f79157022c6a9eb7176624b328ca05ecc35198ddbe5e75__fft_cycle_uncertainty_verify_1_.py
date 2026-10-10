#!/usr/bin/env python3
"""Exact, independently reproducible checks for Fourier-Cycle Uncertainty Theory.

THEOREM PROOF IS IN THE COMPANION MARKDOWN. This script checks finite examples
without relying on floating-point arithmetic or finite-field minors. For prime
p it works in the integer cyclotomic quotient Z[zeta_p], representing values by
coefficient vectors in Z[z]/(z^p-1), and reducing zero tests modulo Phi_p.

Python 3, standard library only.
"""
from __future__ import annotations

from collections import Counter
from itertools import combinations
from math import ceil, gcd
from random import Random


def cycle_from_order(order):
    n = len(order)
    assert sorted(order) == list(range(n))
    return [next(order[(t+1) % n] for t in range(n) if order[t] == i)
            for i in range(n)]


def random_cycle(n, rng):
    order = list(range(n))
    rng.shuffle(order)
    return cycle_from_order(order)


def cycle_segments(beta, cut_destinations):
    """Remove the incoming beta-edge of every marked destination."""
    n = len(beta)
    J = set(cut_destinations)
    if not J:
        return [list(range(n))]
    components = []
    for start in sorted(J):
        arc = [start]
        x = beta[start]
        while x not in J:
            arc.append(x)
            x = beta[x]
            assert len(arc) <= n
        components.append(arc)
    assert sorted(t for arc in components for t in arc) == list(range(n))
    assert len(components) == len(J)
    return components


def potential_sum_supports(alpha, beta, i):
    """Union of row supports of A+B for rows i and alpha(i)."""
    k = alpha[i]
    return {i, alpha[i], beta[i], k, alpha[k], beta[k]}


def det_3x3_cyclotomic_monomials(p, freq, cols):
    """Return coefficients of det(z^(frequency*column mod p)) mod z^p-1."""
    out = [0] * p
    signs = { (0,1,2):1, (1,2,0):1, (2,0,1):1,
              (0,2,1):-1, (2,1,0):-1, (1,0,2):-1 }
    for perm, sign in signs.items():
        exponent = sum(freq[i]*cols[perm[i]] for i in range(3)) % p
        out[exponent] += sign
    return out


def is_cyclotomic_zero_prime(coeff):
    """For prime p, polynomial degree <p vanishes at primitive root iff
    coefficients are all identical (multiple of 1+x+...+x^(p-1))."""
    return len(set(coeff)) == 1


def exact_sandwich_coeff(p, alpha, beta, row_perm, col_perm,
                         left_scales, right_scales, a, b, i, j):
    """Integer coefficients of (A (monomial F monomial) B)[i,j] at zeta_p.

    All weights/scalings are integers; arithmetic is exact in Q(zeta_p).
    H[u,v] = left_scales[u]*right_scales[v]*zeta^(row_perm[u]*col_perm[v]).
    A = I - diag(a) P_alpha; B = I - diag(b) P_beta.
    """
    prev = beta.index(j)
    terms = [
      (+left_scales[i]*right_scales[j], row_perm[i]*col_perm[j]),
      (-a[i]*left_scales[alpha[i]]*right_scales[j], row_perm[alpha[i]]*col_perm[j]),
      (-b[prev]*left_scales[i]*right_scales[prev], row_perm[i]*col_perm[prev]),
      (+a[i]*b[prev]*left_scales[alpha[i]]*right_scales[prev],
       row_perm[alpha[i]]*col_perm[prev]),
    ]
    coeff = [0]*p
    for weight, exponent in terms:
        coeff[exponent % p] += weight
    return coeff


def test_exhaustive_3x3_minors():
    """Exhaustively verify the external full-spark ingredient at small primes."""
    for p in (7, 11, 13):
        triples=list(combinations(range(p),3))
        count=0
        for freq in triples:
            for cols in triples:
                coeff=det_3x3_cyclotomic_monomials(p, freq, cols)
                assert not is_cyclotomic_zero_prime(coeff), (p, freq, cols)
                count+=1
        print(f'exhaustive 3x3 prime Fourier minors p={p:2d}: {count} nonzero')


def test_prime_certificates():
    rng = Random(20261010)
    checks = 0
    for p in (11, 13, 17, 19, 23, 29, 31):
        for trial in range(40):
            alpha = random_cycle(p, rng)
            beta = random_cycle(p, rng)
            i = rng.randrange(p)
            s = [i, alpha[i], alpha[alpha[i]]]
            J = potential_sum_supports(alpha,beta,i)
            assert len(J) <= 5
            components = cycle_segments(beta,J)
            longest = max(components, key=len)
            assert len(longest)>=3, (p,i,J,longest)
            T = longest[:3]
            v = det_3x3_cyclotomic_monomials(p,s,T)
            assert not is_cyclotomic_zero_prime(v), (p,s,T,v)
            checks += 1
        print(f'prime p={p:2d}: 40 non-affine cycle-pair certificates; '
              f'two-sum maximum marks=5, minimum required marks={ceil(p/2)}')
    print('symbolic_cyclotomic_3x3_certificates', checks)


def test_exact_support():
    rng = Random(80210)
    checks = 0
    for p in (5,7,11,13,17):
        for trial in range(20):
            alpha,beta = random_cycle(p,rng),random_cycle(p,rng)
            rr, cc = list(range(p)),list(range(p))
            rng.shuffle(rr); rng.shuffle(cc)
            ls=[rng.randint(1,5) for _ in range(p)]
            rs=[rng.randint(1,5) for _ in range(p)]
            a=[rng.randint(1,5) for _ in range(p)]
            b=[rng.randint(1,5) for _ in range(p)]
            nonzero=[]
            for i in range(p):
                support=set()
                for j in range(p):
                    v=exact_sandwich_coeff(p,alpha,beta,rr,cc,ls,rs,a,b,i,j)
                    if not is_cyclotomic_zero_prime(v): support.add(j)
                nonzero.append(support)
            assert all(len(nonzero[i]|nonzero[alpha[i]])>=ceil(p/2)
                       for i in range(p))
            count=sum(map(len,nonzero))
            assert count >= ceil(p*ceil(p/2)/2)
            checks += 1
        print(f'exact cyclotomic sandwich p={p:2d}: 20 cases passed; '
              f'lower bound nnz={ceil(p*ceil(p/2)/2)}')
    print('exact_cyclotomic_sandwich_cases',checks)


def test_composite_vandermonde():
    rng = Random(16)
    for n in (12,16,24,32,64,128):
        for d in range(1,n):
            if gcd(d,n)!=1: continue
            alpha=[(i+d)%n for i in range(n)]
            beta=random_cycle(n,rng)
            J=potential_sum_supports(alpha,beta,0)
            T=max(cycle_segments(beta,J),key=len)[:3]
            assert len(T)==3
            # F_N on {0,d,2d} is 3x3 Vandermonde with nodes zeta^(dj),
            # which are distinct for distinct j because gcd(d,n)==1.
            assert len({d*t%n for t in T})==3
        print(f'composite n={n:3d}: every coprime-stride row triple verified')


if __name__=='__main__':
    test_exhaustive_3x3_minors()
    test_prime_certificates()
    test_exact_support()
    test_composite_vandermonde()
    print('ALL CHECKS PASSED. These are finite audits, not replacements for the proof.')
