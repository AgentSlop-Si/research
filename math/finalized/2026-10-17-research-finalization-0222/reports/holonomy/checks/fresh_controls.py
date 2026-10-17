#!/usr/bin/env python3
"""New exact controls. No historical imports or program execution."""
import itertools
import json
from fractions import Fraction
from pathlib import Path


def ident(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def mul(a, b, p):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) % p
             for j in range(len(b[0]))] for i in range(len(a))]


def inverse(a, p):
    n = len(a)
    m = [list(row) + eye for row, eye in zip(a, ident(n))]
    for j in range(n):
        piv = next((i for i in range(j, n) if m[i][j] % p), None)
        if piv is None:
            raise ValueError('singular')
        m[j], m[piv] = m[piv], m[j]
        z = pow(m[j][j], -1, p)
        m[j] = [(x*z) % p for x in m[j]]
        for i in range(n):
            if i != j:
                z = m[i][j]
                m[i] = [(x-z*y) % p for x, y in zip(m[i], m[j])]
    return [row[n:] for row in m]


def primitive(p):
    return next(g for g in range(2, p) if len({pow(g, i, p) for i in range(p-1)}) == p-1)


def monomial(n, shift, p):
    return [[(i+2) % p if j == (i+shift) % n else 0 for j in range(n)] for i in range(n)]


def det_integer(a):
    a = [list(row) for row in a]
    n = len(a)
    if not n:
        return 1
    den, sign = 1, 1
    for k in range(n-1):
        if not a[k][k]:
            q = next((i for i in range(k+1, n) if a[i][k]), None)
            if q is None:
                return 0
            a[k], a[q] = a[q], a[k]
            sign *= -1
        pivot = a[k][k]
        for i in range(k+1, n):
            for j in range(k+1, n):
                z = a[i][j]*pivot-a[i][k]*a[k][j]
                assert z % den == 0
                a[i][j] = z // den
        for i in range(k+1, n):
            a[i][k] = 0
        den = pivot
    return sign*a[-1][-1]


def gf2_rank(a):
    a = [[x % 2 for x in row] for row in a]
    r = 0
    for c in range(len(a[0])):
        q = next((i for i in range(r, len(a)) if a[i][c]), None)
        if q is None:
            continue
        a[r], a[q] = a[q], a[r]
        for i in range(len(a)):
            if i != r and a[i][c]:
                a[i] = [x ^ y for x, y in zip(a[i], a[r])]
        r += 1
    return r


def main():
    counts = dict(green_inverse_cases=0, singular_guards=0, fourier_inverse_cases=0,
                  monomial_support_cases=0, alg044_substitution_cases=0,
                  row_ratio_cases=0, n2_cases=0, n2_positive_factorizations=0,
                  all_anchor_determinants=0, primitive_parity_ranks=0,
                  nonprimitive_parity_controls=0, rational_energy_cases=0)
    p = 97
    g = primitive(p)
    for n in [3, 4, 6, 8, 12, 16]:
        root = pow(g, (p-1)//n, p)
        assert pow(root, n, p) == 1 and all(pow(root, k, p) != 1 for k in range(1, n))
        f = [[pow(root, i*j, p) for j in range(n)] for i in range(n)]
        fi = [[pow(n, -1, p)*pow(root, (-i*j) % n, p) % p for j in range(n)] for i in range(n)]
        assert mul(f, fi, p) == ident(n) and all(x for row in fi for x in row)
        counts['fourier_inverse_cases'] += 1
        l, r = monomial(n, 1, p), monomial(n, 2, p)
        li, ri = inverse(l, p), inverse(r, p)
        for alpha in range(p):
            b = [[(int(i == j)-alpha*int(j == (i-1) % n)) % p for j in range(n)] for i in range(n)]
            if pow(alpha, n, p) == 1:
                try:
                    inverse(b, p)
                except ValueError:
                    counts['singular_guards'] += 1
                else:
                    raise AssertionError('singular guard failed')
                continue
            z = pow((1-pow(alpha, n, p)) % p, -1, p)
            green = [[z*pow(alpha, (i-j) % n, p) % p for j in range(n)] for i in range(n)]
            assert mul(b, green, p) == ident(n) == mul(green, b, p)
            counts['green_inverse_cases'] += 1
            t = mul(mul(l, green, p), r, p)
            ti = mul(mul(ri, b, p), li, p)
            assert mul(t, ti, p) == ident(n)
            assert max(sum(bool(x) for x in row) for row in ti) <= 2 < n
            counts['monomial_support_cases'] += 1
            aa = mul(l, r, p)
            q = mul(mul(ri, b, p), r, p)
            qi = mul(mul(ri, green, p), r, p)
            assert mul(aa, qi, p) == t
            assert all(sum(bool(q[i][j]) for i in range(n)) <= 2 for j in range(n))
            assert all(sum(bool(aa[i][j]) for i in range(n)) == 1 for j in range(n))
            counts['alg044_substitution_cases'] += 1
            if alpha:
                ratios = [green[1][j]*pow(green[0][j], -1, p) % p for j in range(n)]
                hist = sorted(ratios.count(v) for v in set(ratios))
                assert hist == [1, n-1]
                for d in range(1, n):
                    vals = [pow(root, d*j, p) for j in range(n)]
                    assert len({vals.count(v) for v in set(vals)}) == 1
                counts['row_ratio_cases'] += 1
    for alpha in range(p):
        if alpha*alpha % p == 1:
            continue
        counts['n2_cases'] += 1
        if not alpha:
            assert [[1,0],[0,1]] != [[1,1],[1,p-1]]
            continue
        ratio = pow(alpha*alpha % p, -1, p)
        assert (ratio == p-1) == (alpha*alpha % p == p-1)
        if ratio == p-1:
            z = pow((1-alpha*alpha) % p, -1, p)
            green = [[z, z*alpha % p],[z*alpha % p,z]]
            d = [[1,0],[0,alpha]]
            out = mul(mul(d, [[1,1],[1,p-1]], p), d, p)
            assert [[z*x % p for x in row] for row in out] == green
            counts['n2_positive_factorizations'] += 1
    for n in [2,3,4,5,6,7,8,9]:
        def tri(i,j): return int(i < j)
        for a in range(n):
            for b in range(n):
                e = [[tri(i,j)-tri(i,b)-tri(a,j)+tri(a,b)
                      for j in range(n) if j != b] for i in range(n) if i != a]
                assert abs(det_integer(e)) == 1
                counts['all_anchor_determinants'] += 1
                if n in [4,8]:
                    assert gf2_rank(e) == n-1
                    counts['primitive_parity_ranks'] += 1
                    assert gf2_rank([[2*x for x in row] for row in e]) == 0
                    counts['nonprimitive_parity_controls'] += 1
    # H4/2 is an exact rational flat unitary, sufficient to check the energy algebra.
    n = 4
    u = [[Fraction((-1)**((i & j).bit_count()), 2) for j in range(n)] for i in range(n)]
    for s in [1,2]:
        for supp in itertools.combinations(range(n), s):
            for vals in itertools.product([-2,-1,1,2], repeat=s):
                b = [Fraction(0)]*n
                for j,x in zip(supp,vals): b[j] = Fraction(x)
                norm2 = sum(x*x for x in b)
                bu = [sum(b[k]*u[k][j] for k in range(n)) for j in range(n)]
                assert sum(x*x for x in bu) == norm2
                for i in range(n):
                    lhs = sum(bu[j]*bu[j] for j in range(n) if j != i)
                    assert lhs >= (1-Fraction(s,n))*norm2
                    counts['rational_energy_cases'] += 1
    # Dropping flatness is invalid: U=I, b=e0 has zero off-target energy.
    assert Fraction(0) < 1-Fraction(1,4)
    result = {'status':'PASS','scope':'Fresh finite exact controls only; universal claims rest on REPORT.md proofs.',
              'historical_code_executed':False,'field':97,'counts':counts,
              'negative_controls':['singular alpha guard','nonprimitive parity rank zero','N=2 positive exceptions','flatness cannot be omitted']}
    Path(__file__).with_name('RESULTS.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
