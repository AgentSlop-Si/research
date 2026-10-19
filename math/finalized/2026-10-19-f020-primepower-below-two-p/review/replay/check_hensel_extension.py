#!/usr/bin/env python3
"""Fresh exact transcription controls; no prior research code is imported.

Bivariate dict keys (X degree, T degree) represent Z[X,T]. Mixed valuation
weights use v(T)=1, v(p)=e, and p/T**e -> -1. These checks supplement the
unlimited proof; they do not certify a census of characteristic-zero orders.
"""
from collections import defaultdict
from fractions import Fraction
from math import comb, factorial
from pathlib import Path
import json
import sympy as sp

ROOT = Path(__file__).resolve().parent
checks = []


def check(name, condition, detail=None):
    if not condition:
        raise AssertionError(name + (': ' + str(detail) if detail is not None else ''))
    row = {'name': name, 'passed': True}
    if detail is not None:
        row['detail'] = detail
    checks.append(row)


def clean(a):
    return {key: val for key, val in a.items() if val}


def add(a, b, scale=1):
    ans = defaultdict(int, a)
    for key, val in b.items():
        ans[key] += scale * val
    return clean(ans)


def mul(a, b):
    ans = defaultdict(int)
    for (i, j), c in a.items():
        for (k, l), d in b.items():
            ans[i+k, j+l] += c*d
    return clean(ans)


def shiftx(a):
    return {(i+1, j): c for (i, j), c in a.items()}


def edge(j):
    return {(0, k): -comb(j, k) for k in range(1, j+1)}


def cont(n, start=1):
    """n vertices, first internal edge u_start."""
    a, b = {(0, 0): 1}, {(1, 0): 1}
    if n == 0:
        return a
    for k in range(1, n):
        a, b = b, add(shiftx(b), mul(edge(start+k-1), a), -1)
    return b


def v_p(c, p):
    k = 0
    while c % p == 0:
        c //= p
        k += 1
    return k, c


def lead(poly, p, e, alpha):
    """Actual mixed-characteristic first weight and residue in X."""
    alpha = Fraction(alpha)
    best = min(Fraction(j + e*v_p(c, p)[0]) + alpha*i
               for (i, j), c in poly.items())
    residue = defaultdict(int)
    for (i, j), c in poly.items():
        k, unit = v_p(c, p)
        if Fraction(j+e*k) + alpha*i == best:
            residue[i] = (residue[i] + unit*((-1)**k)) % p
    return best, {i: c for i, c in residue.items() if c}


def resadd(a, b, p):
    out = defaultdict(int, a)
    for k, c in b.items():
        out[k] += c
    return {k: c % p for k, c in out.items() if c % p}


def hermite(n, p):
    a, b = {0: 1}, {1: 1}
    if n == 0:
        return a
    for k in range(1, n):
        new = resadd({j+1: c for j, c in b.items()},
                     {j: k*c for j, c in a.items()}, p)
        a, b = b, new
    return b


def odd_df(n):
    ans = 1
    for k in range(1, n+1, 2):
        ans *= k
    return ans


Y = sp.Symbol('Y')


def sf(poly, p):
    f = sp.Poly(sum(c*Y**j for j, c in poly.items()), Y, modulus=p)
    return sp.gcd(f, f.diff()).degree() == 0


def gaussian(n):
    """Independent q-Pascal construction with q=1+T."""
    row = [{(0, 0): 1}]
    for j in range(1, n+1):
        nxt = [{(0, 0): 1}]
        for k in range(1, j):
            power = {(0, a): comb(j-k, a) for a in range(j-k+1)}
            nxt.append(add(row[k], mul(power, row[k-1])))
        nxt.append({(0, 0): 1})
        row = nxt
    return row


PRIMES = [3, 5, 7, 11]
for p in PRIMES:
    h = (p-1)//2
    c = (-1)**(h+1) % p
    Ps = [cont(n) for n in range(2*p+1)]
    hp = hermite(p, p)
    check(f'h_p=Y^p, p={p}', hp == {p: 1})
    check(f'additive residual squarefree, p={p}', sf({p: 1, 1: c}, p))
    for r in range(p):
        hr = hermite(r, p)
        check(f'h_r squarefree, p={p}, r={r}', sf(hr, p))
        check(f'h_(p+r)=Y^p h_r, p={p}, r={r}',
              hermite(p+r, p) == {j+p: a for j, a in hr.items()})
    gs = gaussian(p)
    for k in range(1, p):
        poly = gs[k]
        check(f'Gaussian order p-1, p={p}, k={k}',
              all(a % p == 0 for (i, j), a in poly.items() if j < p-1))
        actual = poly.get((0, p-1), 0) % p
        expected = ((-1)**(k-1)*pow(k, -1, p)) % p
        check(f'Gaussian leading residue, p={p}, k={k}', actual == expected)
    hd = {}
    for k in range(1, p+1):
        hd = add(hd, gs[k], k*((-1)**(k-1)))
    plinear = {(0, j): a for (i, j), a in Ps[p].items() if i == 1}
    check(f'Exact P derivative versus H derivative, p={p}',
          plinear == {key: ((-1)**h)*val for key, val in hd.items()})
    check(f'P_p lower coefficient divisibility, p={p}',
          all(a % p == 0 for (i, j), a in Ps[p].items()
              if i < p and j < p-1))
    check(f'P_p leading linear residue, p={p}',
          Ps[p].get((1, p-1), 0) % p == c)

    for s in [2, 3]:
        e = p**(s-1)*(p-1)
        check(f'Exact p-block mixed reduction, p={p}, s={s}',
              lead(Ps[p], p, e, 1) == (Fraction(p), {p: 1, 1: c}))
        check(f'Joining edge has valuation p, p={p}, s={s}',
              lead(edge(p), p, e, 0) == (Fraction(p), {0: p-1}))
        for r in range(p):
            b = p+r
            hr = hermite(r, p)
            outer = lead(Ps[b], p, e, Fraction(1, 2))
            check(f'Outer exact mixed reduction, p={p}, s={s}, r={r}',
                  outer == (Fraction(b, 2), {j+p: a for j, a in hr.items()}))
            F = cont(r, p+1)
            if r:
                G = cont(r-1, p+2)
                rhs = add(mul(F, Ps[p]), mul(mul(edge(p), G), Ps[p-1]), -1)
                check(f'Exact joining-edge identity, p={p}, s={s}, r={r}',
                      rhs == Ps[b])
            else:
                check(f'Empty block identity, p={p}, s={s}', F == {(0, 0): 1})
            m = r//2
            if r % 2 == 0:
                a = odd_df(2*m-1) % p
                expected = {p: a, 1: a*c % p}
                check(f'Even central mixed reduction, p={p}, s={s}, r={r}',
                      lead(Ps[b], p, e, 1) == (Fraction(p+m), expected))
                check(f'Even central simple residual, p={p}, s={s}, r={r}',
                      sf(expected, p))
            elif p >= 5:
                a = odd_df(2*m+1) % p
                expected = {p+1: a, 2: a*c % p}
                check(f'Odd central mixed reduction, p={p}, s={s}, r={r}',
                      lead(Ps[b], p, e, 1) == (Fraction(p+m+1), expected))
                reduced = {p-1: a, 0: a*c % p}
                check(f'Odd nonzero central residual simple, p={p}, s={s}, r={r}',
                      sf(reduced, p) and reduced[0] != 0)
                constant = (2**m*factorial(m)*odd_df(p-2)) % p
                deep = {2: a*c % p, 0: constant}
                alpha = Fraction(p+1, 4)
                check(f'Deep quadratic mixed reduction, p={p}, s={s}, r={r}',
                      lead(Ps[b], p, e, alpha) == (Fraction(p+m+h), deep))
                check(f'Deep quadratic separable, p={p}, s={s}, r={r}',
                      sf(deep, p) and deep[0] != 0 and deep[2] != 0)
            else:
                check(f'Explicit p=3 overlap control, s={s}',
                      lead(Ps[4], p, e, 1) == (Fraction(4), {4: 1, 2: 1, 0: 1}))
                check(f'p=3 overlap deliberately inseparable, s={s}',
                      not sf({4: 1, 2: 1, 0: 1}, 3))

        alpha = Fraction(2*p-1, 2*p)
        boundary = {2*p: 1, 0: p-1}
        check(f'First subsequent boundary reduction, p={p}, s={s}',
              lead(Ps[2*p], p, e, alpha) == (Fraction(2*p-1), boundary))
        check(f'First boundary is inseparable, p={p}, s={s}', not sf(boundary, p))
        check(f'Boundary equals (Y^2-1)^p, p={p}, s={s}',
              sp.Poly((Y**2-1)**p-(Y**(2*p)-1), Y, modulus=p).is_zero)

    for s in ([1, 2, 3] if p <= 7 else [1, 2]):
        m = p**(s-1)
        e = m*(p-1)
        coeff = [sum(comb(j*m, k) for j in range(p) if j*m >= k)
                 for k in range(e+1)]
        check(f'Cyclotomic shift Eisenstein, p={p}, s={s}',
              coeff[0] == p and coeff[-1] == 1 and
              all(a % p == 0 for a in coeff[:-1]) and coeff[0] % (p*p) != 0)

q, X = sp.symbols('q X')
A = (1-q)*(q*q+2*q+3)
B = (1-q)**2*(q*q+q+1)
quartic = q**4+4*q**3+6*q*q+8*q+5
check('Exceptional quartic discriminant factor',
      sp.expand(A*A-4*B-(1-q)**2*quartic) == 0)
check('Exceptional quartic degree is below phi(9)', sp.degree(quartic, q) == 4 < 6)
check('Quartic P discriminant',
      sp.factor(sp.discriminant(X**4-A*X*X+B, X)-16*B*(A*A-4*B)**2) == 0)

payload = {
    'purpose': 'Exact proof-transcription controls, not a root-order census',
    'primes_in_formal_controls': PRIMES,
    'mixed_ramification_exponents': 'phi(p^s), s=2,3 in controls',
    'count': len(checks),
    'all_passed': True,
    'checks': checks,
}
(ROOT/'CHECKS.json').write_text(json.dumps(payload, indent=2)+'\n')
print(f'PASS: {len(checks)} exact formal and mixed-valuation controls')
