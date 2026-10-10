"""Fresh exact modular checks for the twisted-displacement obstruction.

Written independently for this review; no supplied code is imported/executed.
Run: python independent_checks.py > results.json
"""
import itertools
import json
import math
import random

P = 2521  # prime, and N | P-1 for all tested lengths

def mat(n, diagonal=0):
    return [[diagonal if i == j else 0 for j in range(n)] for i in range(n)]

def add(a, b, scale=1):
    return [[(x + scale*y) % P for x, y in zip(r, s)] for r, s in zip(a, b)]

def mul(a, b):
    n = len(a)
    return [[sum(a[i][k]*b[k][j] for k in range(n)) % P for j in range(n)] for i in range(n)]

def scale(a, c):
    return [[c*x % P for x in row] for row in a]

def power(a, k):
    out = mat(len(a), 1)
    while k:
        if k & 1:
            out = mul(out, a)
        a = mul(a, a)
        k >>= 1
    return out

def rank(a):
    a = [row[:] for row in a]
    n = len(a)
    r = 0
    for j in range(n):
        pivot = next((i for i in range(r, n) if a[i][j] % P), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        z = pow(a[r][j], -1, P)
        a[r] = [x*z % P for x in a[r]]
        for i in range(r+1, n):
            c = a[i][j]
            a[i] = [(x-c*y) % P for x, y in zip(a[i], a[r])]
        r += 1
    return r

def inv(a):
    n = len(a)
    a = [row[:] + [int(i == j) for j in range(n)] for i, row in enumerate(a)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if a[i][j] % P), None)
        if pivot is None:
            raise ValueError('singular')
        a[j], a[pivot] = a[pivot], a[j]
        z = pow(a[j][j], -1, P)
        a[j] = [x*z % P for x in a[j]]
        for i in range(n):
            if i == j:
                continue
            c = a[i][j]
            a[i] = [(x-c*y) % P for x, y in zip(a[i], a[j])]
    return [row[n:] for row in a]

def primitive(n):
    for w in range(1, P):
        if pow(w, n, P) == 1 and all(pow(w, k, P) != 1 for k in range(1, n)):
            return w
    raise ValueError(n)

def shift(n):
    z = mat(n)
    for j in range(n):
        z[(j+1) % n][j] = 1
    return z

def twist(a):
    n = len(a)
    return [[a[(i+1) % n][(j+1) % n] for j in range(n)] for i in range(n)]

def affine_conjugate(a, u, v):
    n = len(a)
    out = mat(n)
    for i in range(n):
        for j in range(n):
            out[(u*i+v) % n][(u*j+v) % n] = a[i][j]
    return out

def path(n, a, b, c):
    out = mat(n, a)
    for i in range(n-1):
        out[i+1][i] = b
        out[i][i+1] = c
    return out

def poly_from_roots(roots):
    coeffs = [1]
    for root in roots:
        out = [0]*(len(coeffs)+1)
        for k, c in enumerate(coeffs):
            out[k] = (out[k] - root*c) % P
            out[k+1] = (out[k+1] + c) % P
        coeffs = out
    return coeffs

def apply_poly(coeffs, a, op):
    out = mat(len(a))
    term = a
    for c in coeffs:
        out = add(out, term, c)
        term = op(term)
    return out

def check(n):
    w = primitive(n)
    z = shift(n)
    d = [[pow(w, i, P) if i == j else 0 for j in range(n)] for i in range(n)]
    f = [[pow(w, i*j, P) for j in range(n)] for i in range(n)]
    weyl = mul(power(z, n-1), d)
    assert rank(f) == n
    tf = f
    for k in range(n+2):
        assert tf == scale(mul(power(weyl, k), f), pow(w, k*(k-1)//2, P))
        tf = twist(tf)
    assert power(weyl, n) == mat(n, pow(w, -n*(n-1)//2, P))
    polys = 0
    root_subsets = itertools.chain.from_iterable(itertools.combinations(range(n), s) for s in range(n+1)) if n <= 8 else [tuple(range(s)) for s in range(n+1)]
    for exponents in root_subsets:
        coeffs = poly_from_roots([pow(w, a, P) for a in exponents])
        assert rank(apply_poly(coeffs, f, twist)) >= n-len(exponents)
        polys += 1
    denom = path(n, 4, 2, 3)
    while rank(denom) != n:
        denom = add(denom, mat(n, 1))
    green = inv(denom)
    assert rank(add(twist(denom), denom, -1)) <= 2
    assert rank(add(twist(green), green, -1)) <= 2
    affine_ranks = []
    for u in range(1, n):
        if math.gcd(u, n) != 1:
            continue
        for v in range(n):
            g = affine_conjugate(green, u, v)
            r = rank(add(twist(g), g, -1))
            assert r <= 4
            affine_ranks.append(r)
    rng = random.Random(1000+n)
    # Products of 3 two-term stage sums, 8 expanded branches.
    stages = []
    units = [u for u in range(1, n) if math.gcd(u, n) == 1]
    for j in range(3):
        terms = []
        for ell in range(2):
            a = rng.randrange(n)
            g = affine_conjugate(green, rng.choice(units), rng.randrange(n))
            terms.append((mul(power(d, a), g), pow(w, a, P)))
        stages.append(terms)
    branches = []
    for choice in itertools.product(range(2), repeat=3):
        b, lam = mat(n, 1), 1
        for j, ell in enumerate(choice):
            term, eig = stages[j][ell]
            b, lam = mul(b, term), lam*eig % P
        assert rank(add(twist(b), b, -lam)) <= 12
        branches.append((b, lam))
    target = mat(n, 1)
    for terms in stages:
        target = mul(target, add(terms[0][0], terms[1][0]))
    assert target == sum_matrices([b for b, _ in branches])
    roots = sorted(set(lam for _, lam in branches))
    coeffs = poly_from_roots(roots)
    assert rank(apply_poly(coeffs, target, twist)) <= len(roots)*8*12
    return {'N': n, 'fourier_phase_checks': n+2, 'polynomials_checked': polys, 'affine_paths_checked': len(affine_ranks), 'max_affine_displacement_rank': max(affine_ranks), 'branch_count': 8, 'distinct_phase_classes': len(roots)}

def sum_matrices(matrices):
    out = mat(len(matrices[0]))
    for a in matrices:
        out = add(out, a)
    return out

def scope_counterexample(n=9, u=2):
    # A bare affine multiplier is not a low-displacement conjugated path.
    perm = mat(n)
    for j in range(n):
        perm[(u*j) % n][j] = 1
    return {'N': n, 'multiplier': u, 'bare_affine_permutation_displacement_rank': rank(add(twist(perm), perm, -1))}

if __name__ == '__main__':
    assert all(P % k for k in range(2, math.isqrt(P)+1))
    records = [check(n) for n in [2,3,4,5,6,7,8,9,10,12,14,18,20]]
    print(json.dumps({'field_prime': P, 'all_checks_passed': True, 'checks': records, 'scope_counterexample': scope_counterexample()}, indent=2))
