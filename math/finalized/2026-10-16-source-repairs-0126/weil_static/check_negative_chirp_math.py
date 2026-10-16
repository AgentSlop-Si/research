"""Fresh bounded formula checker; imports no original or repaired research code.

This is an independent arithmetic derivation/check, not a run of the v25 suite.
No SL2 enumeration, subprocesses, network, or package installation is used.
"""
from pathlib import Path
from math import gcd, isqrt
import hashlib
import json

COUNTS = {'assertions': 0, 'entry_equalities': 0, 'wrong_sign_rejections': 0,
          'covariance_entry_equalities': 0, 'matrix_products': 0}

def require(condition, label):
    COUNTS['assertions'] += 1
    if not condition:
        raise AssertionError(label)

def multiply(A, B, ell):
    COUNTS['matrix_products'] += 1
    return [[sum(a * b for a, b in zip(row, col)) % ell
             for col in zip(*B)] for row in A]

def matrix_equal(A, B, label):
    for i, (r, s) in enumerate(zip(A, B)):
        for j, (a, b) in enumerate(zip(r, s)):
            require(a == b, (label, i, j, a, b))
            COUNTS['entry_equalities'] += 1

def check_case(q, p, b, ell, zeta, F, FI):
    roots = [pow(zeta, j, ell) for j in range(q)]
    half = pow(2, -1, q)
    scale = pow(q, -1, ell)
    diagonal = [roots[-b * t * t * half % q] for t in range(q)]
    # A full matrix product, distinct from the scalar Gauss evaluator below.
    cf = [[diagonal[i] * a % ell for a in row] for i, row in enumerate(F)]
    spectral = multiply(FI, cf, ell)
    gauss = [[scale * sum(roots[(-b * t * t * half + (y - x) * t) % q]
                         for t in range(q)) % ell
              for y in range(q)] for x in range(q)]
    matrix_equal(spectral, gauss, ('DFT/Gauss', q, b))
    if b == 0:
        predicted = [[int(x == y) for y in range(q)] for x in range(q)]
        g, m = q, 1
    else:
        g = gcd(b, q)
        m = q // g
        u = b // g
        eta = pow(zeta, g, ell)
        redhalf = pow(2, -1, m)
        G = sum(pow(eta, (-u * t * t * redhalf) % m, ell) for t in range(m)) % ell
        require(G != 0, ('nonzero Gauss factor', q, b))
        kappa = G * pow(m, -1, ell) % ell
        inv2u = pow(2 * u, -1, m)
        predicted = [[0 if (y - x) % g else
                      kappa * pow(eta, (((y - x) // g) ** 2 * inv2u) % m, ell) % ell
                      for y in range(q)] for x in range(q)]
        for r in range(g):
            ratio = (spectral[r][r] * spectral[r+g][r+g] *
                     pow(spectral[r][r+g] * spectral[r+g][r] % ell, -1, ell)) % ell
            require(ratio == pow(eta, (-pow(u, -1, m)) % m, ell),
                    ('signed ratio', q, b, r))
            require(pow(ratio, m, ell) == 1 and pow(ratio, m // p, ell) != 1,
                    ('exact prime-power order', q, b, r))
    matrix_equal(spectral, predicted, ('completed square', q, b))
    for x in range(q):
        require(sum(v != 0 for v in spectral[x]) == m, ('row support', q, b, x))
        require(sum(spectral[y][x] != 0 for y in range(q)) == m, ('column support', q, b, x))
        for y in range(q):
            require((spectral[x][y] != 0) == ((x - y) % g == 0), ('support locus', q, b, x, y))
    if b:
        wrong_cf = [[roots[b * i * i * half % q] * a % ell for a in row]
                    for i, row in enumerate(F)]
        wrong = multiply(FI, wrong_cf, ell)
        require(spectral != wrong, ('positive-chirp rejection', q, b))
        COUNTS['wrong_sign_rejections'] += 1
    # D(a,c)f(x)=psi(c*(x-a/2))*f(x-a); test U_b D(a,c)=D(a+bc,c) U_b.
    for a, c in ((1, 0), (0, 1), (2, 3)):
        aprime = (a + b * c) % q
        for x in range(q):
            for y in range(q):
                left = spectral[x][(y + a) % q] * roots[c * (y + a * half) % q] % ell
                right = roots[c * (x - aprime * half) % q] * spectral[(x - aprime) % q][y] % ell
                require(left == right, ('upper-shear covariance', q, b, a, c, x, y))
                COUNTS['covariance_entry_equalities'] += 1
    # Exact 2x2 conjugation; does not enumerate SL2.
    W = [[0, -1], [1, 0]]
    WI = [[0, 1], [-1, 0]]
    Lminus = [[1, 0], [-b, 1]]
    matrix_equal(multiply(multiply(WI, Lminus, q), W, q), [[1, b], [0, 1]], ('group label', q, b))
    return {'q': q, 'p': p, 'b': b, 'blocks': g, 'core_length': m,
            'negative_chirp': 'PASS', 'completed_square': 'PASS',
            'signed_cross_ratio': 'PASS' if b else 'identity',
            'wrong_sign': 'rejected' if b else 'identical identity',
            'weyl_covariance': 'PASS'}

def main():
    cases = []
    fields = []
    for p, k, ell in ((3, 1, 7), (3, 2, 19), (5, 2, 101), (3, 3, 109), (7, 2, 197)):
        q = p ** k
        require(all(ell % d for d in range(2, isqrt(ell)+1)), ('prime coefficient field', ell))
        zeta = next(z for z in range(2, ell) if pow(z, q, ell) == 1 and pow(z, q//p, ell) != 1)
        require(pow(zeta, q, ell) == 1 and pow(zeta, q//p, ell) != 1, ('primitive root', q))
        F = [[pow(zeta, x*y % q, ell) for y in range(q)] for x in range(q)]
        FI = [[pow(q, -1, ell) * pow(zeta, -x*y % q, ell) % ell for y in range(q)] for x in range(q)]
        matrix_equal(multiply(FI, F, ell), [[int(x == y) for y in range(q)] for x in range(q)], ('Fourier inverse', q))
        fields.append({'p': p, 'k': k, 'q': q, 'coefficient_prime': ell, 'primitive_root': zeta})
        for b in range(q):
            cases.append(check_case(q, p, b, ell, zeta, F, FI))
    result = {'status': 'PASS', 'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'scope': 'All scalar b at q=3,9,25,27,49; exact bounded arithmetic only',
              'historical_source_imported': False, 'patched_source_imported': False,
              'historical_or_patched_source_executed': False, 'sl2_enumeration': False,
              'scalar_cases': len(cases), 'fields': fields, 'counts': COUNTS, 'cases': cases}
    Path(__file__).with_name('BOUNDED_MATH_CHECKS.json').write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'cases'}, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
