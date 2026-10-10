#!/usr/bin/env python3
"""Fresh exact controls for the explicit infinite chirp restriction theorem.
Standard library only; no predecessor program is imported or executed.
Writes its deterministic result only to the specified output directory.
"""
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path


def invmat(a, p):
    n = len(a)
    b = [[x % p for x in row] + [int(i == j) for j in range(n)] for i, row in enumerate(a)]
    for j in range(n):
        k = next((i for i in range(j, n) if b[i][j]), None)
        if k is None:
            raise ValueError('singular matrix')
        b[j], b[k] = b[k], b[j]
        t = pow(b[j][j], -1, p)
        b[j] = [x * t % p for x in b[j]]
        for i in range(n):
            if i != j and b[i][j]:
                t = b[i][j]
                b[i] = [(x - t * y) % p for x, y in zip(b[i], b[j])]
    return [row[n:] for row in b]


def cycle(traversal):
    a = [0] * len(traversal)
    for i, j in zip(traversal, traversal[1:] + traversal[:1]):
        a[i] = j
    return a


def induced(sigma, weights, selected, p):
    labels = {x: i for i, x in enumerate(selected)}
    tau, arcs, lengths = [], [], []
    for start in selected:
        x, product, length = start, 1, 0
        while True:
            product = product * weights[x] % p
            x = sigma[x]
            length += 1
            if x in labels:
                tau.append(labels[x]); arcs.append(product); lengths.append(length)
                break
    return tau, arcs, lengths


def green(sigma, weights, p):
    n = len(sigma)
    a = [[int(i == j) for j in range(n)] for i in range(n)]
    for i in range(n):
        a[i][sigma[i]] = (a[i][sigma[i]] - weights[i]) % p
    return invmat(a, p)


def principal(a, selected):
    return [[a[i][j] for j in selected] for i in selected]


def endpoint(a, left, right, p):
    return [[left[i] * x * right[j] % p for j, x in enumerate(row)] for i, row in enumerate(a)]


def restriction_controls():
    p, cases, entries, masked, illegal = 241, 0, 0, 0, 0
    singleton, reordered = 0, 0
    for n in range(1, 8):
        traversals = [list(range(n))]
        if n >= 3:
            traversals += [[0] + list(reversed(range(1, n)))]
        for traversal in traversals:
            sigma = cycle(traversal)
            for mode in ('varied', 'one_zero', 'all_zero', 'unit_product'):
                weights = [(2 * i + 3) % p for i in range(n)]
                if mode == 'one_zero': weights[n // 2] = 0
                if mode == 'all_zero': weights = [0] * n
                if mode == 'unit_product': weights = [1] * n
                rho = math.prod(weights) % p
                legal = rho != 1
                g = green(sigma, weights, p) if legal else None
                left = [0 if i % 2 == 0 else i + 2 for i in range(n)]
                right = [0 if i % 3 == 0 else i + 5 for i in range(n)]
                ended = endpoint(g, left, right, p) if legal else None
                for size in range(1, n + 1):
                    for subset in itertools.combinations(range(n), size):
                        selected = list(reversed(subset))
                        tau, arcs, lengths = induced(sigma, weights, selected, p)
                        assert sum(lengths) == n
                        assert math.prod(arcs) % p == rho
                        assert sorted(tau) == list(range(size))
                        seen, v = set(), 0
                        for _ in range(size): seen.add(v); v = tau[v]
                        assert len(seen) == size and v == 0
                        if not legal:
                            illegal += 1
                            try: green(tau, arcs, p)
                            except ValueError: pass
                            else: raise AssertionError('illegal Green guard admitted')
                            continue
                        small = green(tau, arcs, p)
                        assert small == principal(g, selected)
                        assert endpoint(small, [left[i] for i in selected], [right[i] for i in selected], p) == principal(ended, selected)
                        cases += 1; entries += size * size; masked += size * size
                        singleton += int(size == 1); reordered += int(size > 1)
    # A two-summand positive control with different structural cycles.
    n, selected = 11, [7, 0, 4, 9, 2]
    total = [[0] * n for _ in range(n)]
    small_total = [[0] * len(selected) for _ in selected]
    for branch, traversal in enumerate([list(range(n)), [0, 3, 8, 2, 9, 1, 5, 10, 7, 4, 6]]):
        sigma = cycle(traversal)
        weights = [0 if i == 3 + branch else (i + 2 + branch) for i in range(n)]
        left = [0 if i % 3 == branch else i + 3 for i in range(n)]
        right = [0 if i % 4 == branch else i + 7 for i in range(n)]
        g = endpoint(green(sigma, weights, p), left, right, p)
        tau, arcs, _ = induced(sigma, weights, selected, p)
        small = endpoint(green(tau, arcs, p), [left[i] for i in selected], [right[i] for i in selected], p)
        total = [[(a + b) % p for a, b in zip(r, s)] for r, s in zip(total, g)]
        small_total = [[(a + b) % p for a, b in zip(r, s)] for r, s in zip(small_total, small)]
    assert principal(total, selected) == small_total
    return {'prime': p, 'legal_cases': cases, 'Green_entries': entries, 'masked_entries': masked,
            'illegal_guard_cases_rejected': illegal, 'singleton_cases': singleton,
            'reordered_cases': reordered, 'distinct_cycle_two_sum_entries': 25}


def factors(n):
    out, t = [], 2
    while t * t <= n:
        if n % t == 0:
            out.append(t)
            while n % t == 0: n //= t
        t += 1
    if n > 1: out.append(n)
    return out


def prime(p):
    return p >= 2 and all(p % j for j in range(2, math.isqrt(p) + 1))


def root_field(n):
    mult = 2
    while not prime(mult * n + 1): mult += 1
    p = mult * n + 1
    for x in range(2, p):
        w = pow(x, mult, p)
        if all(pow(w, n // d, p) != 1 for d in factors(n)):
            return p, w
    raise AssertionError('no root')


def block(n, w, p):
    h = (n + 1) // 2
    g = sum(pow(w, h * j * j, p) for j in range(n)) % p
    denominator = (1 + n * g) % p
    if not denominator: raise ValueError('resonant feedback')
    m, eta = n // 5, pow(w, (n // 5) ** 2, p)
    answer = [[(pow(eta, a * b, p) - g * pow(eta, -3 * (a + b) ** 2, p)
               + (n * g * pow(eta, -3 * a * a, p) if a == b else 0))
              * pow(denominator, -1, p) % p for b in range(5)] for a in range(5)]
    return g, eta, denominator, answer


def direct_inverse_control(n, w, p):
    h = (n + 1) // 2
    ni = pow(n, -1, p)
    target_inv = [[(ni * pow(w, -i * j, p) + (pow(w, h * i * i, p) if i == j else 0)) % p
                   for j in range(n)] for i in range(n)]
    g, eta, guard, expected = block(n, w, p)
    actual = principal(invmat(target_inv, p), [a * (n // 5) for a in range(5)])
    assert actual == expected
    return {'N': n, 'p': p, 'omega': w, 'eta': eta, 'G': g, 'denominator': guard, 'direct_inverse_entries': 25}


def arithmetic_controls():
    crt, inverses, rejections = [], [], []
    for q in (1, 3, 7, 9, 11, 13, 21, 27):
        n = 5 * q * q
        p, root = root_field(n)
        for exponent in (1, 2, 4):
            w, h = pow(root, exponent, p), (n + 1) // 2
            assert pow(w, n, p) == 1
            assert all(pow(w, n // d, p) != 1 for d in factors(n))
            eta, xi = pow(w, q ** 4, p), pow(w, 5, p)
            assert pow(eta, 5, p) == 1 and eta != 1
            residues = {(q * q * u + 5 * v) % n for u in range(5) for v in range(q * q)}
            assert len(residues) == n
            g = sum(pow(w, h * j * j, p) for j in range(n)) % p
            g5 = sum(pow(eta, 3 * j * j, p) for j in range(5)) % p
            square = sum(pow(xi, 5 * h * v * v, p) for v in range(q * q)) % p
            assert square == q % p and g == q * g5 % p
            assert g5 * g5 % p == 5 and g * g % p == n % p
            # Exact character-sum cancellation, including composite q.
            inner_sums = [sum(pow(xi, q * 2 * 5 * h * s * t, p) for t in range(q)) % p for s in range(q)]
            assert inner_sums == [q % p] + [0] * (q - 1)
            guard = (1 + n * g) % p
            crt.append({'q': q, 'N': n, 'p': p, 'omega': w, 'eta': eta, 'G': g, 'g5': g5,
                        'square_factor': square, 'denominator': guard, 'CRT_residues': len(residues)})
            if n <= 45 and guard:
                inverses.append(direct_inverse_control(n, w, p))
    for n in (15, 35, 65):
        p, w = root_field(n)
        if (1 + n * sum(pow(w, ((n + 1) // 2) * j * j, p) for j in range(n))) % p:
            inverses.append(direct_inverse_control(n, w, p))
    for w in (4, 8):
        assert pow(w, 5, 31) == 1 and w != 1
        assert (1 + 5 * sum(pow(w, 3 * j * j, 31) for j in range(5))) % 31 == 0
        try: block(5, w, 31)
        except ValueError: rejections.append({'N': 5, 'p': 31, 'omega': w, 'denominator': 0})
        else: raise AssertionError('resonance admitted')
    return {'CRT_square_Gauss_cases': crt, 'direct_inverse_cases': inverses, 'resonances_rejected': rejections}


def reduce_phi5(poly):
    a = list(poly)
    while len(a) > 4:
        c, d = a[-1], len(a) - 1
        for j in range(5): a[d - 4 + j] -= c
        a.pop()
    return a + [0] * (4 - len(a))


def coefficient_controls():
    g = [1, 0, 2, 2]
    gsq = [sum(g[i] * g[j] for i in range(4) for j in range(4) if i + j == d) for d in range(7)]
    assert reduce_phi5(gsq) == [5, 0, 0, 0]
    p, eta = 241, 91
    assert pow(eta, 5, p) == 1 and eta != 1
    assert sum(pow(eta, j, p) for j in range(5)) % p == 0
    g5 = (1 + 2 * (eta * eta + eta ** 3)) % p
    assert g5 == 103 and (1 + 5 * g5) % p == 34
    expected = [[161,20,102,102,20],[20,182,62,26,92],[102,62,236,28,26],
                [102,26,28,236,62],[20,92,26,62,182]]
    assert block(5, eta, p)[3] == expected
    tests = []
    for k in (0, 1, 2, 7, 241, 10**6):
        q, n = 2410 * k + 1, 5 * (2410 * k + 1) ** 2
        assert q % 2 == 1 and math.gcd(q, 5) == 1 and q % p == 1 and n % p == 5
        den = (1 + 5 * q ** 3 * g5) % p
        b = [[(pow(eta, a * c, p) - q * g5 * pow(eta, -3 * (a + c) ** 2, p)
             + (5 * q ** 3 * g5 * pow(eta, -3 * a * a, p) if a == c else 0))
              * pow(den, -1, p) % p for c in range(5)] for a in range(5)]
        assert den == 34 and b == expected
        assert 1 - 125 * q ** 6 != 0
        tests.append({'k': k, 'q': q, 'N': n, 'denominator_mod_241': den, 'target_entries': 25})
    # Congruence is universal in k: (1+2410k)^3-1 has every positive coefficient divisible by 241.
    cubic_minus_one = [0, 3 * 2410, 3 * 2410**2, 2410**3]
    assert all(c % p == 0 for c in cubic_minus_one)
    return {'g5_squared_remainder': reduce_phi5(gsq), 'eta': eta, 'g5': g5, 'denominator': 34,
            'B5_mod_241': expected, 'universal_cubic_congruence_coefficients': cubic_minus_one,
            'sequence_controls': tests, 'quadratic_conjugate_denominator_product': '1-125*q^6'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out-dir', default='.')
    args = parser.parse_args()
    result = {'status': 'PASS', 'restriction': restriction_controls(),
              'arithmetic': arithmetic_controls(), 'coefficients': coefficient_controls(),
              'scope': 'Exact controls supporting the written all-length proof; the accepted N5 exclusion is a dependency, not rerun here.'}
    output = Path(args.out_dir); output.mkdir(parents=True, exist_ok=True)
    path = output / 'EXACT_RESULTS.json'
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'status': result['status'], 'Green_cases': result['restriction']['legal_cases'],
                      'Green_entries': result['restriction']['Green_entries'],
                      'CRT_cases': len(result['arithmetic']['CRT_square_Gauss_cases']),
                      'direct_inverse_cases': len(result['arithmetic']['direct_inverse_cases']),
                      'result_sha256': hashlib.sha256(path.read_bytes()).hexdigest()}, sort_keys=True))


if __name__ == '__main__': main()
