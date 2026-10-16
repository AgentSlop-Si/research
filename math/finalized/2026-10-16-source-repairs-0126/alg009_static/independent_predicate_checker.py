"""Fresh, standard-library-only mathematical controls, authored 2026-10-16.

No research file is read, loaded, imported, compiled, or executed. This checks
the mathematical predicate and reconstructs small controls, not the patched
historical implementation or its performance. Output is deterministic JSON.
"""
import json
from itertools import permutations
from math import gcd, isqrt


def prime(p):
    return p >= 2 and all(p % d for d in range(2, isqrt(p) + 1))


def order(a, p):
    z = 1
    for k in range(1, p):
        z = z * a % p
        if z == 1:
            return k
    return None


def root(n, p):
    return next(a for a in range(1, p) if order(a, p) == n)


def direct_poles(n, delta, alpha, omega, p):
    """Enumerate all Fourier denominators; independent of the gcd formula."""
    step = pow(omega, delta, p)
    z = 1
    zeros = []
    for k in range(n):
        if (1 - alpha * z) % p == 0:
            zeros.append(k)
        z = z * step % p
    return zeros


def corrected_rejection(n, delta, alpha, p):
    g = gcd(n, delta)
    return g > 1 and pow(alpha, n // g, p) == 1


def guard_domain(n, delta, alpha, omega, p):
    # Fresh checker preconditions, NOT new validation added to historical code.
    if n < 8 or p <= 55 or not prime(p):
        raise ValueError('unsupported size or field')
    if (p - 1) % n or order(omega % p, p) != n:
        raise ValueError('root must have exact order N')
    if not 1 <= delta < n or alpha % p == 0:
        raise ValueError('invalid delay or zero multiplier')


def dft(r, omega, p):
    n = len(r)
    return [sum(r[j] * pow(omega, j * k, p) for j in range(n)) % p
            for k in range(n)]


def defect(r, delta, alpha, p):
    n = len(r)
    return [(r[j] - alpha * r[(j - delta) % n]) % p for j in range(n)]


def certify_and_reconstruct(r, delta, alpha, omega, p):
    n = len(r)
    guard_domain(n, delta, alpha, omega, p)
    if corrected_rejection(n, delta, alpha, p):
        return None, 'multipole-budget'
    h = defect(r, delta, alpha, p)
    if not 1 <= sum(bool(v) for v in h) <= 2:
        return None, 'full-coordinate-support'
    forcing = dft(h, omega, p)
    out = []
    repairs = 0
    for k in range(n):
        denominator = (1 - alpha * pow(omega, delta * k, p)) % p
        if denominator:
            out.append(forcing[k] * pow(denominator, -1, p) % p)
        else:
            repairs += 1
            out.append(sum(r[j] * pow(omega, j * k, p) for j in range(n)) % p)
    assert repairs <= 1
    return out, {'defect': h, 'direct_repairs': repairs}


def trim(a, p):
    a = [x % p for x in a]
    while a and a[-1] == 0:
        a.pop()
    return a


def multiply(a, b, p):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] = (out[i + j] + x * y) % p
    return trim(out, p)


def polynomial_gcd(a, b, p):
    a, b = trim(a, p), trim(b, p)
    while b:
        r = a[:]
        while len(r) >= len(b):
            c = r[-1] * pow(b[-1], -1, p) % p
            offset = len(r) - len(b)
            for j, v in enumerate(b):
                r[offset + j] = (r[offset + j] - c * v) % p
            r = trim(r, p)
        a, b = b, r
    return [v * pow(a[-1], -1, p) % p for v in a] if a else []


def sign(sigma):
    return -1 if sum(sigma[i] > sigma[j] for i in range(len(sigma))
                     for j in range(i + 1, len(sigma))) % 2 else 1


def hankel_polynomial(R, w, offset, p):
    out = [0] * 4
    for sigma in permutations(range(3)):
        term = [1]
        for i in range(3):
            k = offset + i + sigma[i]
            term = multiply(term, [R[k], -R[k] * pow(w, k, p)], p)
        for i, v in enumerate(term):
            out[i] = (out[i] + sign(sigma) * v) % p
    return trim(out, p)


def resultant_by_permutations(a, b, p):
    """Fixed-cubic 6x6 determinant, using 720 signed terms."""
    rows = []
    for c in (a, b):
        c = list(reversed(c + [0] * (4 - len(c))))
        for offset in range(3):
            rows.append([0] * offset + c + [0] * (2 - offset))
    out = 0
    for sigma in permutations(range(6)):
        term = sign(sigma)
        for i in range(6):
            term = term * rows[i][sigma[i]] % p
        out = (out + term) % p
    return out


def numerical_hankel(R, offset, p):
    return sum(sign(sigma) * R[offset + sigma[0]]
               * R[offset + 1 + sigma[1]] * R[offset + 2 + sigma[2]]
               for sigma in permutations(range(3))) % p


def dense_solve(A, b, p):
    n = len(b)
    M = [[x % p for x in row] + [b[i] % p] for i, row in enumerate(A)]
    for c in range(n):
        pivot = next(i for i in range(c, n) if M[i][c])
        M[c], M[pivot] = M[pivot], M[c]
        inv = pow(M[c][c], -1, p)
        M[c] = [v * inv % p for v in M[c]]
        for i in range(n):
            if i != c:
                factor = M[i][c]
                M[i] = [(x - factor * y) % p for x, y in zip(M[i], M[c])]
    return [row[-1] for row in M]


def full_gate_control(p, omega, r, delta, alpha, expected_resultant, expected_higher_gcd):
    n = len(r)
    R = dft(r, omega, p)
    witness = resultant_by_permutations(hankel_polynomial(R, 2, 0, p),
                                       hankel_polynomial(R, 2, 1, p), p)
    assert witness == expected_resultant != 0
    accepted, higher_gcd = [], []
    for d in range(1, n):
        w = pow(omega, d, p)
        A, B = [hankel_polynomial(R, w, j, p) for j in (0, 1)]
        G = polynomial_gcd(A, B, p)
        if len(G) > 2:
            higher_gcd.append({'delta': d, 'gcd': G})
        if len(G) != 2:
            continue
        a = -G[0] % p
        if not a:
            continue
        adjusted = [v * (1 - a * pow(w, k, p)) % p for k, v in enumerate(R)]
        if any(numerical_hankel(adjusted, j, p) for j in (2, 3)):
            continue
        out, details = certify_and_reconstruct(r, d, a, omega, p)
        if out is not None:
            assert out == R
            accepted.append({'delta': d, 'alpha': a, 'gcd': G,
                             'old_reject': pow(a, n, p) == 1 and gcd(d, n) != 1,
                             'poles': direct_poles(n, d, a, omega, p),
                             'reconstruction': details, 'outputs_checked': n})
    assert any(c['delta'] == delta and c['alpha'] == alpha for c in accepted)
    assert all(c['old_reject'] and not c['poles'] for c in accepted)
    assert [c['delta'] for c in accepted] == [2, 6]
    assert [c['delta'] for c in higher_gcd] == expected_higher_gcd
    return {'p': p, 'N': n, 'omega': omega, 'r': r, 'direct_DFT': R,
            'nonzero_resultant_witness': [2, witness],
            'accepted_candidates': accepted, 'higher_gcd_declines': higher_gcd}


def main():
    totals = {'triples': 0, 'nonzero_alpha_triples': 0,
              'corrected_false_rejections': 0, 'corrected_false_admissions': 0,
              'old_false_rejections': 0, 'old_false_admissions': 0}
    grids = []
    for p in range(3, 258):
        if not prime(p):
            continue
        for n in range(2, min(64, p - 1) + 1):
            if (p - 1) % n:
                continue
            omega = root(n, p)
            cases = false_old = 0
            for delta in range(1, n):
                g = gcd(n, delta)
                for alpha in range(p):
                    count = len(direct_poles(n, delta, alpha, omega, p))
                    formula = g if pow(alpha, n // g, p) == 1 else 0
                    assert count == formula
                    new_reject = corrected_rejection(n, delta, alpha, p)
                    old_reject = pow(alpha, n, p) == 1 and g > 1
                    assert new_reject == (count > 1)
                    totals['triples'] += 1
                    totals['nonzero_alpha_triples'] += bool(alpha)
                    cases += 1
                    false_old += old_reject and count <= 1
                    totals['old_false_rejections'] += old_reject and count <= 1
                    totals['old_false_admissions'] += not old_reject and count > 1
            grids.append({'p': p, 'N': n, 'omega': omega,
                          'triples': cases, 'old_false_rejections': false_old})
    controls = [
        full_gate_control(73, 10, [37, 37, 5, 5, 50, 50, 62, 62], 2, 10, 62, [4]),
        full_gate_control(97, 33, [49, 49, 65, 65, 11, 11, 72, 72], 2, 33, 48, [4]),
        full_gate_control(97, 64, [1, 50, 64, 96, 22, 33, 50, 75], 2, 64, 95, [])]
    r, p, omega = controls[1]['r'], 97, 33
    n = len(r)
    P = [[0] * n for _ in range(n)]
    L = [[0] * n for _ in range(n)]
    for j in range(n):
        P[j][j] = (7 + 2 * pow(omega, -j, p)) % p
        L[j][j] = (7 + pow(omega, j, p)) % p
        P[j][(j - 1) % n] = 1
        L[j][(j - 1) % n] = 2
    assert all(P[j][j] and L[j][j] for j in range(n))
    assert order(21, 97) == 96 and order(79, 97) == 16 and 79 ** 2 % 97 == omega
    x = dense_solve(P, r, p)
    Fx = dense_solve(L, controls[1]['direct_DFT'], p)
    assert Fx == dft(x, omega, p)
    outer = {'p': p, 'N': n, 'primitive_generator': 21, 'sqrt_omega': 79,
             'convolution_length': 16, 'x': x, 'Fx': Fx, 'all_outputs_checked': n}
    # One repaired pole is admitted; genuine two-pole case stays declined.
    single = [1] * 7 + [0]
    out, details = certify_and_reconstruct(single, 1, 1, 33, 97)
    assert out == dft(single, 33, 97) and details['direct_repairs'] == 1
    multi = [3, 7, 3, 7, 5, 7, 5, 7]
    out_multi, multi_reason = certify_and_reconstruct(multi, 2, 1, 33, 97)
    assert out_multi is None and multi_reason == 'multipole-budget'
    assert direct_poles(8, 2, 1, 33, 97) == [0, 4]
    # Fresh adversary: exact first eight probes preserved at N=16, while a
    # dense inverse Fourier character at bin 8 breaks the raw certificate.
    n, p, omega, alpha, delta = 16, 97, root(16, 97), 2, 2
    h = [1, 1] + [0] * 14
    A = [[int(i == j) for j in range(n)] for i in range(n)]
    for i in range(n):
        A[i][(i - delta) % n] = (A[i][(i - delta) % n] - alpha) % p
    r = dense_solve(A, h, p)
    perturbation = [pow(omega, -8 * j, p) * pow(n, -1, p) % p for j in range(n)]
    mutant = [(a + b) % p for a, b in zip(r, perturbation)]
    assert dft(r, omega, p)[:8] == dft(mutant, omega, p)[:8]
    out, reason = certify_and_reconstruct(mutant, delta, alpha, omega, p)
    assert out is None and reason == 'full-coordinate-support'
    assert dft(r, omega, p)[8] != dft(mutant, omega, p)[8]
    # Identically zero resultants are not promoted to a certificate.
    zero_resultants = [resultant_by_permutations(hankel_polynomial([0] * 8, w, 0, 97),
                                               hankel_polynomial([0] * 8, w, 1, 97), 97)
                       for w in range(46)]
    assert zero_resultants == [0] * 46
    out, zero_reason = certify_and_reconstruct([0] * 8, 1, 2, 33, 97)
    assert out is None and zero_reason == 'full-coordinate-support'
    rejected_domains = []
    for args in [(4, 1, 1, 22, 97), (8, 1, 1, 2, 17), (8, 1, 1, 2, 65),
                 (8, 1, 1, 1, 97), (8, 0, 1, 33, 97), (8, 8, 1, 33, 97),
                 (8, 1, 0, 33, 97)]:
        try:
            guard_domain(*args)
        except ValueError as e:
            rejected_domains.append({'arguments': args, 'reason': str(e)})
        else:
            raise AssertionError('invalid domain admitted')
    print(json.dumps({'status': 'PASS', 'execution_scope': 'fresh mathematical checker only',
                      'scope_note': 'Predicate grids include smaller fields/lengths; source branch still requires N>=8, p>55 and every original guard.',
                      'totals': totals, 'predicate_grids': grids,
                      'two_defect_controls': controls, 'outer_green_control': outer,
                      'one_pole_application': details,
                      'multi_pole_rejection': {'poles': [0, 4], 'reason': multi_reason},
                      'eight_probe_mutant': {'N': 16, 'unchanged_samples': 8, 'rejected_by_full_support': True},
                      'zero_resultant_evaluations': len(zero_resultants),
                      'invalid_domains_rejected': rejected_domains,
                      'historical_or_patched_program_executed': False}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
