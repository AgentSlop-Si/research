#!/usr/bin/env python3
"""Independently authored finite audit; imports no target/predecessor code.
Exact cyclotomic sums certify tested complex Gram entries. Field controls only
check algebraic circuits and are not used to infer magnitude lower bounds.
"""
import hashlib
import itertools
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
STATS = Counter()


def word(k, t):
    return f'{k:0{t}b}'


def valid(k, t, b):
    w = word(k, t)
    return w[0] == '1' and w[-1] == '1' and '0' * b not in w


def frequency(k, t):
    return int(word(k, t)[::-1], 2)


def path_exponent(start, k, t, size):
    s, exponent = start, 0
    for bit in word(k, t):
        if bit == '1':
            exponent += s
        s = (2 * s + int(bit)) % size
    return s, exponent % size


def cyclo(terms, order):
    """Exact Z[X]/(X^(order/2)+1), appropriate for primitive 2-power roots."""
    half = order // 2
    out = Counter()
    for exponent, coefficient in terms:
        exponent %= order
        out[exponent % half] += coefficient if exponent < half else -coefficient
    return {e: c for e, c in out.items() if c}


def multiply(a, b, order):
    return cyclo(((e + f, c * d) for e, c in a.items() for f, d in b.items()), order)


def conjugate(a, order):
    return cyclo(((-e, c) for e, c in a.items()), order)


def rows(n, b, T):
    N, d = 1 << n, n - b
    r = 1 << d
    bank = []
    used = set()
    for t in range(1, T + 1):
        R = 1 << (d - b - t)
        count = 0
        for k in range(1 << (t - 1), 1 << t):
            if not valid(k, t, b):
                continue
            f = frequency(k, t)
            gamma = path_exponent(0, k, t, N)[1]
            for q in range(R):
                i = (q << (b + t)) + k
                assert i < r and i not in used
                used.add(i)
                bits = word(i, d)
                assert d - (bits.rfind('0' * b) + b) == t
                exponents = {s: (gamma + (1 << b) * s * f) % N for s in range(q, r, R)}
                assert len(exponents) == 1 << (b + t)
                bank.append((t, q, k, i, exponents))
                count += 1
        expected_words = 1 if t == 1 else sum('0' * b not in word(k, t - 2) for k in range(1 << (t - 2))) if t > 2 else 1
        assert count == R * expected_words
        STATS['support_cardinality_checks'] += 1
    return bank


def graph_step(vector, root, p):
    size = len(vector)
    out = [0] * size
    # Group incoming edges by destination pair, rather than enumerate paths.
    for h in range(size // 2):
        a, c = vector[h], vector[h + size // 2]
        out[2 * h] = (a + c) % p
        out[2 * h + 1] = pow(root, h, p) * (a - c) % p
    return out


def routed_step(vector, age, b, omega, eta, p):
    r = len(vector)
    out = [0] * r
    for a, value in enumerate(vector):
        suffix = a & ((1 << age) - 1)
        if valid(suffix, age, b):
            exponent = path_exponent(0, suffix, age, 1 << (r.bit_length() - 1 + b))[1]
            factor = pow(omega, exponent, p) * pow(eta, -exponent, p) % p
            out[((a - suffix) << b | suffix) % r] = (out[((a - suffix) << b | suffix) % r] + factor * value) % p
    return out


def bank_apply(bank, vector, omega, p, r, T):
    out = [[0] * r for _ in range(T)]
    for t, q, k, i, row in bank:
        out[t - 1][i] = sum(pow(omega, e, p) * vector[s] for s, e in row.items()) % p
    return out


def killed_returns(vector, n, b, T, omega, p):
    N = 1 << n
    v = [0] * N
    for s, value in enumerate(vector):
        v[s << b] = value
    retained = [s for s in range(N) if not (s & ((1 << b) - 1)) or '0' * b not in word(s, n)]
    out = []
    for ell in range(1, b + T + 1):
        v = graph_step(v, omega, p)
        if ell > b:
            out.append(v[::1 << b])
        for s in retained:
            v[s] = 0
    return out


def rank_mod(matrix, p):
    a = [list(row) for row in matrix]
    if not a:
        return 0
    h = 0
    for j in range(len(a[0])):
        pivot = next((i for i in range(h, len(a)) if a[i][j]), None)
        if pivot is None:
            continue
        a[h], a[pivot] = a[pivot], a[h]
        inv = pow(a[h][j], -1, p)
        a[h] = [v * inv % p for v in a[h]]
        for i in range(h + 1, len(a)):
            scale = a[i][j]
            if scale:
                a[i] = [(v - scale * w) % p for v, w in zip(a[i], a[h])]
        h += 1
        if h == len(a):
            break
    return h


def determinant_mod(matrix, p):
    a = [row[:] for row in matrix]
    det = 1
    for j in range(len(a)):
        pivot = next((i for i in range(j, len(a)) if a[i][j]), None)
        if pivot is None:
            return 0
        if pivot != j:
            a[j], a[pivot] = a[pivot], a[j]
            det = -det
        det = det * a[j][j] % p
        inv = pow(a[j][j], -1, p)
        for i in range(j + 1, len(a)):
            scale = a[i][j] * inv % p
            for k in range(j + 1, len(a)):
                a[i][k] = (a[i][k] - scale * a[j][k]) % p
            a[i][j] = 0
    return det % p


def cyclo_minor(row_exponents, columns, order):
    m = len(row_exponents)
    terms = []
    for perm in itertools.permutations(range(m)):
        entries = [row_exponents[i].get(columns[perm[i]]) for i in range(m)]
        if any(e is None for e in entries):
            continue
        inversions = sum(perm[i] > perm[j] for i in range(m) for j in range(i + 1, m))
        terms.append((sum(entries), -1 if inversions % 2 else 1))
    return cyclo(terms, order)


def test_complex_gram():
    cases = []
    params = [(n, b, min(1 << (b - 1), n - 2 * b)) for n in range(3, 12) for b in range(1, n // 2 + 1) if n - 2 * b > 0]
    params += [(10, 2, 6), (12, 3, 6), (14, 4, 6)]
    for n, b, T in params:
        N = 1 << n
        bank = rows(n, b, T)
        branches = Counter()
        for a, left in enumerate(bank):
            t, q, k, i, v = left
            for right in bank[a:]:
                tp, qp, kp, ip, w = right
                common = v.keys() & w.keys()
                result = cyclo(((v[s] - w[s], 1) for s in common), N)
                expected = {0: 1 << (b + t)} if left is right else {}
                assert result == expected
                STATS['exact_complex_gram_pairs'] += 1
                if t != tp and common:
                    assert q % (1 << (n - 2 * b - tp)) == qp
                    assert (frequency(k, t) - frequency(kp, tp)) % (1 << (b + t)) != 0
                    branches['below_t_plus_b' if tp < t + b else 'equal_t_plus_b' if tp == t + b else 'above_t_plus_b'] += 1
        STATS['complex_cases'] += 1
        STATS['complex_rows'] += len(bank)
        cases.append({'n': n, 'b': b, 'T': T, 'rows': len(bank), 'cross_age_branches': dict(branches)})
    return cases


def test_field_circuits():
    cases = []
    for p, max_n in [(257, 8), (65537, 11)]:
        assert all(p % k for k in range(2, int(p ** .5) + 1))
        for n in range(3, max_n + 1):
            for b in range(1, (n - 1) // 2 + 1):
                N, r = 1 << n, 1 << (n - b)
                T = min(1 << (b - 1), n - 2 * b)
                primitive = pow(3, (p - 1) // N, p)
                # Check a second primitive embedding, avoiding reliance on one root.
                omega = pow(primitive, 3 if (n + b) % 2 else 1, p)
                assert pow(omega, N, p) == 1 and pow(omega, N // 2, p) == p - 1
                eta = pow(omega, 1 << b, p)
                bank = rows(n, b, T)
                samples = [[((s + 5) ** 3 + 17 * s + n + b) % p for s in range(r)]]
                if n <= 6:
                    samples.extend([[int(s == j) for s in range(r)] for j in range(r)])
                    STATS['basis_vectors'] += r
                for vector in samples:
                    expected = bank_apply(bank, vector, omega, p, r, T)
                    current = vector[:]
                    actual = []
                    for age in range(1, T + 1):
                        current = graph_step(current, eta, p)
                        actual.append(routed_step(current, age, b, omega, eta, p))
                    assert actual == expected == killed_returns(vector, n, b, T, omega, p)
                    STATS['routed_and_killed_vectors'] += 1
                # Stream independent u_j into future slots and compare with direct packet placement.
                jets = [[(s * s + 13 * j * s + 7 * j + 2) % p for s in range(r)] for j in range(n + 1)]
                causal = [[0] * r for _ in range(n + 1)]
                selected = [[0] * r for _ in range(n + 1)]
                locations = set()
                for j, vector in enumerate(jets):
                    current = vector[:]
                    for age in range(1, min(T, n - b - j) + 1):
                        current = graph_step(current, eta, p)
                        k = j + b + age
                        assert k > j
                        output = routed_step(current, age, b, omega, eta, p)
                        causal[k] = [(a + c) % p for a, c in zip(causal[k], output)]
                    for age, q, suffix, i, row in bank:
                        k = j + b + age
                        if k <= n:
                            assert (k, i) not in locations
                            locations.add((k, i))
                            selected[k][i] = sum(pow(omega, e, p) * vector[s] for s, e in row.items()) % p
                assert causal == selected
                J = n - b - T + 1
                assert all((j + b + age, i) in locations for j in range(J) for age, q, suffix, i, row in bank)
                STATS['batch_output_coordinates'] += r * (n + 1)
                STATS['field_cases'] += 1
                cases.append({'p': p, 'n': n, 'b': b, 'T': T, 'J': J, 'samples': len(samples)})
    return cases


def test_cauchy_binet():
    cases = []
    for d, b, T in [(2, 1, 1), (3, 1, 2), (3, 2, 1), (4, 2, 2)]:
        r, n = 1 << d, d + b
        bank = rows(n, b, T)
        phase_free = [{s: s * frequency(k, t) % r for s in exponents} for t, q, k, i, exponents in bank]
        m = len(bank)
        S = sum(b + t for t, q, k, i, exponents in bank)
        total = Counter()
        p = 65537
        eta = pow(3, (p - 1) // r, p)
        full_rows = [[pow(eta, row[s], p) if s in row else 0 for s in range(r)] for row in phase_free]
        for columns in itertools.combinations(range(r), m):
            determinant = cyclo_minor(phase_free, columns, r)
            norm = multiply(determinant, conjugate(determinant, r), r)
            total.update(norm)
            value = sum(c * pow(eta, e, p) for e, c in determinant.items()) % p
            # Complementary coordinate rows keep every input dimension in the potential.
            complement = [s for s in range(r) if s not in columns]
            completed = full_rows + [[int(i == s) for i in range(r)] for s in complement]
            signed = determinant_mod(completed, p)
            assert signed in (value, -value % p)
            STATS['exact_cauchy_binet_minors'] += 1
            STATS['full_dimension_completions'] += 1
        assert {e: c for e, c in total.items() if c} == {0: 1 << S}
        cases.append({'d': d, 'b': b, 'T': T, 'r': r, 'm': m, 'S': S, 'sum_squared_minors': 1 << S})
    return cases


def test_counts():
    cases = []
    for b in range(2, 15):
        L = 1 << (b - 1)
        # Finite-state word DP, not the predecessor's b-term scalar recurrence.
        states = [1] + [0] * (b - 1)
        counts = [1]
        for ell in range(1, L + 1):
            states = [sum(states)] + states[:-1]
            counts.append(sum(states))
        fractions = [Fraction(1, 1 << (b + 1))]
        for t in range(2, L + 1):
            c = counts[t - 2]
            assert Fraction(c, 1 << (t - 2)) >= 1 - Fraction(t - 2, 1 << b)
            frac = Fraction(c, 1 << (b + t))
            assert frac >= Fraction(1, 16 * L)
            fractions.append(frac)
            STATS['symbolic_count_inequalities'] += 1
        mass = sum(fractions)
        half_S_over_r = sum(Fraction(b + t, 2) * value for t, value in enumerate(fractions, 1))
        assert mass <= 1
        assert sum(range(2, L + 1)) >= Fraction(L * L, 2)
        assert half_S_over_r >= Fraction(L, 64)
        if b >= 7:
            assert Fraction(L, 64) - Fraction(1, 2) >= Fraction(L, 128)
            assert half_S_over_r - Fraction(1, 2) >= Fraction(L, 128)
        cases.append({'b': b, 'L': L, 'm_over_r': float(mass), 'half_S_over_r': float(half_S_over_r), 'coarse_minor_log_per_r': float(half_S_over_r - Fraction(1, 2))})
    return cases


def test_source_constraints():
    cases = []
    p = 65537
    for n, b in [(4, 1), (5, 1), (6, 1), (6, 2), (7, 2)]:
        N, r = 1 << n, 1 << (n - b)
        T = min(1 << (b - 1), n - 2 * b)
        J = n - b - T + 1
        omega = pow(3, (p - 1) // N, p)
        columns = []
        for source in range(N):
            v = [int(s == source) for s in range(N)]
            column = []
            for j in range(J):
                column.extend(v[::1 << b])
                v = graph_step(v, omega, p)
            columns.append(column)
        matrix = list(map(list, zip(*columns)))
        rank = rank_mod(matrix, p)
        assert rank <= min(N, J * r)
        if J * r > N:
            assert rank < J * r
        cases.append({'n': n, 'b': b, 'J': J, 'N_original_inputs': N, 'Jr_arbitrary_inputs': J * r, 'actual_selected_solution_jet_rank': rank})
        STATS['source_constraint_rank_cases'] += 1
    return cases


def negative_control():
    n, b, t, tp, k, kp, q = 8, 2, 1, 4, 1, 9, 1
    d, N = n - b, 1 << n
    r = 1 << d
    assert not valid(kp, tp, b)
    assert (q << (b + t)) + k == kp
    R = 1 << (d - b - t)
    difference = frequency(k, t) - frequency(kp, tp)
    result = cyclo((((1 << b) * s * difference, 1) for s in range(q, r, R)), N)
    assert result and sum(abs(c) for c in result.values()) == 1 << (b + t)
    return {'b': b, 'short_age': t, 'long_age': tp, 'forbidden_word': word(kp, tp), 'colliding_output_index': kp, 'phase_free_cyclotomic_pairing': result}


def main():
    result = {
        'complex_gram_cases': test_complex_gram(),
        'field_circuit_cases': test_field_circuits(),
        'cauchy_binet_cases': test_cauchy_binet(),
        'symbolic_count_cases': test_counts(),
        'source_constraint_cases': test_source_constraints(),
        'forbidden_word_negative_control': negative_control(),
    }
    result.update(status='PASS', totals=dict(STATS), scope='Independent finite controls plus exact cyclotomic identities; asymptotic theorem requires the written all-size proof.')
    (HERE / 'INDEPENDENT_CONTROLS.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'status': 'PASS', 'totals': dict(STATS), 'source_constraint_cases': result['source_constraint_cases']}, sort_keys=True))


if __name__ == '__main__':
    main()
