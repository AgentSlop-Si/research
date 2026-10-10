#!/usr/bin/env python3
"""Independent exact finite-field controls for character-profile compression.

No constructor or uploaded code is imported. All arithmetic is over F_65537.
"""
import argparse
import json
from pathlib import Path
import random

P = 65537
GENERATOR = 3


def inverse(x):
    assert x % P
    return pow(x, -1, P)


def root(n):
    assert (P-1) % n == 0
    w = pow(GENERATOR, (P-1)//n, P)
    assert pow(w, n, P) == 1
    if n > 1:
        assert pow(w, n//2, P) != 1
    return w


def rev(i, n):
    value = 0
    for _ in range(n.bit_length()-1):
        value = 2*value+(i & 1)
        i >>= 1
    return value


def identity(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def multiply(a, b):
    bt = list(zip(*b))
    return [[sum(x*y for x, y in zip(row, col)) % P for col in bt] for row in a]


def weighted_green(n, s, c):
    assert s % P and c % P != 1
    powers = {d: pow(s, d, P) for d in range(1-n, n)}
    den = inverse(1-c)
    return [[powers[i-j]*den*(1 if i >= j else c) % P
             for j in range(n)] for i in range(n)]


def reversed_green(n, r, h):
    t = weighted_green(n, r, h)
    order = [rev(i, n) for i in range(n)]
    return [[t[i][j] for j in order] for i in order]


def profiles(k, m):
    omega = root(m)
    x = [[pow(omega, a*rev(i, m), P) for i in range(m)] for a in range(k)]
    y = [[pow(omega, -a*rev(i, m), P)*inverse(m) % P
          for i in range(m)] for a in range(k)]
    return x, y


def project(bmat, k, m, x, y):
    # Direct V L B M U expansion; physical blocks remain separate.
    return [[sum(x[a][i]*bmat[a*m+i][b*m+j]*y[b][j]
                 for i in range(m) for j in range(m)) % P
             for b in range(k)] for a in range(k)]


def transpose(x):
    return [list(row) for row in zip(*x)]


def compressed_reversed_formula(k, m, r, h, x, y):
    e = reversed_green(m, pow(r, k, P), h)
    gram = multiply(x, transpose(y))
    local = multiply(multiply(x, e), transpose(y))
    rho = [rev(a, k) for a in range(k)]
    return [[pow(r, rho[a]-rho[b], P) *
             (local[a][b]-(gram[a][b] if rho[a] < rho[b] else 0)) % P
             for b in range(k)] for a in range(k)]


def fourier_conjugate_t(m, v, h):
    w = root(m)
    f = [[pow(w, a*i, P) for i in range(m)] for a in range(m)]
    fi = [[pow(w, -i*a, P)*inverse(m) % P for a in range(m)] for i in range(m)]
    return multiply(multiply(f, weighted_green(m, v, h)), fi)


def verify_nonresonant(m, v, h):
    assert pow(v, m, P) != 1
    omega = root(m)
    actual = fourier_conjugate_t(m, v, h)
    kappa = (h-pow(v, m, P))*inverse(1-h)*inverse(1-pow(v, m, P)) % P
    left = [sum(pow(omega, a*i, P)*pow(v, i, P) for i in range(m)) % P
            for a in range(m)]
    right = [sum(pow(v, -i, P)*pow(omega, -a*i, P) for i in range(m))*inverse(m) % P
             for a in range(m)]
    predicted = [[((inverse(1-v*pow(omega, a, P)) if a == b else 0)
                   + kappa*left[a]*right[b]) % P for b in range(m)] for a in range(m)]
    assert actual == predicted


def verify_resonant(m, v, h):
    assert pow(v, m, P) == 1 and h % P != 1
    omega = root(m)
    z = [pow(omega, a, P) for a in range(m)]
    d = [(1-v*za) % P for za in z]
    a0 = d.index(0)
    assert d.count(0) == 1
    wrap = h*pow(v, 1-m, P) % P
    tau = (wrap-v)*inverse(m) % P
    assert tau
    columns = []
    for j in range(m):
        rhs = [int(a == j) for a in range(m)]
        sol = [(rhs[a]-rhs[a0])*inverse(d[a]) % P if a != a0 else 0
               for a in range(m)]
        sol[a0] = (-rhs[a0]*inverse(tau)-sum(z[a]*sol[a] for a in range(m) if a != a0))*inverse(z[a0]) % P
        assert all((d[a]*sol[a]-tau*sum(za*xa for za, xa in zip(z, sol))) % P == rhs[a]
                   for a in range(m))
        columns.append(sol)
    assert transpose(columns) == fourier_conjugate_t(m, v, h)


def direct_natural_coefficients(m, s):
    omega = root(m)
    f = [sum(pow(s, i, P)*pow(omega, a*rev(i, m), P) for i in range(m)) % P
         for a in range(m)]
    fi = [sum(pow(s, -i, P)*pow(omega, a*rev(i, m), P) for i in range(m)) % P
          for a in range(m)]
    d = [sum(pow(s, i-j, P)*pow(omega, a*(rev(i, m)-rev(j, m)), P)
             for i in range(m) for j in range(i+1, m)) % P for a in range(m)]
    return f, fi, d


def recurrent_natural_coefficients(m, s):
    if m == 1:
        return [1], [1], [0]
    ell = m//2
    f, fi, d = recurrent_natural_coefficients(ell, s)
    omega = root(m)
    out_f, out_fi, out_d = [0]*m, [0]*m, [0]*m
    for a in range(ell):
        z = pow(s, ell, P)*pow(omega, a, P) % P
        zi = pow(s, -ell, P)*pow(omega, a, P) % P
        cross = inverse(z)*f[a]*fi[(-a) % ell] % P
        out_f[a] = (1+z)*f[a] % P
        out_f[a+ell] = (1-z)*f[a] % P
        out_fi[a] = (1+zi)*fi[a] % P
        out_fi[a+ell] = (1-zi)*fi[a] % P
        out_d[a] = (2*d[a]+cross) % P
        out_d[a+ell] = (2*d[a]-cross) % P
    return out_f, out_fi, out_d


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='VERIFIED_RESULTS.json')
    args = parser.parse_args()
    assert pow(GENERATOR, (P-1)//2, P) == P-1
    rows = []
    rng = random.Random(581024)
    for m in (2, 4, 8):
        for k in (m, 2*m):
            n = k*m
            x, y = profiles(k, m)
            gram = multiply(x, transpose(y))
            assert gram == [[int(a % m == b % m) for b in range(k)] for a in range(k)]
            theta_identity = project(identity(n), k, m, x, y)
            assert theta_identity == identity(k)
            if k == 2*m:
                assert theta_identity != gram
            custom_x = [[rng.randrange(P) for _ in range(m)] for _ in range(k)]
            custom_y = [[rng.randrange(P) for _ in range(m)] for _ in range(k)]
            custom_direct = project(reversed_green(n, 3, 11), k, m, custom_x, custom_y)
            assert custom_direct == compressed_reversed_formula(k, m, 3, 11, custom_x, custom_y)
            custom_identity = project(identity(n), k, m, custom_x, custom_y)
            assert custom_identity == [[(sum(a*b for a, b in zip(custom_x[i], custom_y[i])) % P
                                          if i == j else 0) for j in range(k)] for i in range(k)]
            tests = []
            for name, r, h in [('homogeneous', 3, pow(3, n, P)),
                               ('nonresonant', 3, 7),
                               ('zero_wrap_nonzero_edge', 3, 0),
                               ('resonant', root(n), 7)]:
                direct = project(reversed_green(n, r, h), k, m, x, y)
                assert direct == compressed_reversed_formula(k, m, r, h, x, y)
                v = pow(r, k, P)
                if name == 'homogeneous':
                    omega = root(m)
                    lambdas = [inverse(1-v*pow(omega, a, P)) for a in range(m)]
                    expected = [[0]*k for _ in range(k)]
                    for a in range(m):
                        expected[a][a] = lambdas[a]
                        if k == 2*m:
                            expected[a+m][a+m] = lambdas[a]
                            expected[a][a+m] = (lambdas[a]-1)*inverse(r) % P
                            expected[a+m][a] = r*lambdas[a] % P
                    assert direct == expected
                if name == 'resonant':
                    verify_resonant(m, v, h)
                else:
                    verify_nonresonant(m, v, h)
                tests.append(name)
            for s, c in [(5, 11), (5, 0)]:
                actual = project(weighted_green(n, s, c), k, m, x, y)
                f, fi, d = direct_natural_coefficients(m, s)
                coarse = weighted_green(k, pow(s, m, P), c)
                expected = [[(f[a % m]*coarse[a][b]*fi[(-b) % m]*inverse(m)
                              - (d[a % m]*inverse(m) if a == b else 0)) % P
                             for b in range(k)] for a in range(k)]
                assert actual == expected
            rows.append({'m':m,'k':k,'N':n,'identity_projection':'I_k',
                         'identity_differs_from_repeated_Gram':k == 2*m,
                         'arbitrary_profile_compression_checked':True,
                         'reversed_cases':tests,'natural_cases':2})
    recurrence_rows = []
    for m in (1, 2, 4, 8, 16, 32, 64):
        for s in (1, 3, 5, P-1):
            assert direct_natural_coefficients(m, s) == recurrent_natural_coefficients(m, s)
        recurrence_rows.append({'m':m,'edges_checked':[1,3,5,P-1]})
    result = {'status':'PASS','field':P,'primitive_generator':GENERATOR,
              'projection_controls':rows,'recurrence_controls':recurrence_rows,
              'correction':'Theta(I_N)=I_k for these masks, including k=2m; it is not X Y^T.',
              'scope':'Projected middle paths and coefficient recurrences only; no full Fourier synthesis.'}
    Path(args.output).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','projection_shapes':len(rows),'reversed_cases':sum(len(x['reversed_cases']) for x in rows),
                      'natural_cases':sum(x['natural_cases'] for x in rows),'recurrence_parameter_pairs':4*len(recurrence_rows)},sort_keys=True))


if __name__ == '__main__':
    main()
