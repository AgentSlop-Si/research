#!/usr/bin/env python3
"""New exact oracles. Does not import or execute any predecessor program."""
from fractions import Fraction
import json
from pathlib import Path
import random


def reverse_bits(k, t):
    ans = 0
    for _ in range(t):
        ans = 2 * ans + (k & 1)
        k >>= 1
    return ans


def gamma(k):
    # Independently sum the state just before every appended 1 bit.
    state = ans = 0
    for bit in bin(k)[2:]:
        if bit == '1':
            ans += state
        state = 2 * state + int(bit)
    return ans


def allowed(k, t, b):
    bits = format(k, f'0{t}b')
    return bits[0] == bits[-1] == '1' and '0' * b not in bits


def q_step(v, root, p):
    size = len(v)
    ans = [0] * size
    phase = 1
    for s, value in enumerate(v):
        a = 2 * s % size
        ans[a] = (ans[a] + value) % p
        ans[a + 1] = (ans[a + 1] + phase * value) % p
        phase = phase * root % p
    return ans


def route_after_q(v, t, b, omega, eta, p):
    r = len(v)
    ans = [0] * r
    ratio = omega * pow(eta, -1, p) % p
    for a, value in enumerate(v):
        k = a % (1 << t)
        if allowed(k, t, b):
            i = ((1 << b) * (a - k) + k) % r
            ans[i] = (ans[i] + pow(ratio, gamma(k), p) * value) % p
    return ans


def packet_bank(r, d, b, T, omega, eta, p):
    # Explicit independent source-row definition (3).
    rows = []
    support_seen = set()
    sizes = []
    for t in range(1, T + 1):
        R = 1 << (d - b - t)
        count = 0
        for q in range(R):
            for k in range(1 << t):
                if not allowed(k, t, b):
                    continue
                i = (1 << (b + t)) * q + k
                assert i not in support_seen
                support_seen.add(i)
                f = reverse_bits(k, t)
                phase = pow(omega, gamma(k), p)
                vals = {j: phase * pow(eta, j * f, p) % p
                        for j in range(q, r, R)}
                rows.append((t, i, vals))
                count += 1
        sizes.append(count)
    return rows, sizes


def packets_apply(rows, u, r, p):
    ans = [0] * r
    for _t, i, row in rows:
        ans[i] = sum(c * u[j] for j, c in row.items()) % p
    return ans


def direct_first_returns(u, n, b, T, omega, p):
    # Full-N graph, retained states killed after each time. No compressed route.
    N = 1 << n
    r = len(u)
    retained = [s % (1 << b) == 0 or '0' * b not in format(s, f'0{n}b')
                for s in range(N)]
    v = [0] * N
    for j in range(r):
        v[j << b] = u[j]
    ans = {}
    for ell in range(1, b + T + 1):
        v = q_step(v, omega, p)
        if ell > b:
            ans[ell - b] = [v[j << b] for j in range(r)]
        v = [0 if retained[s] else value for s, value in enumerate(v)]
    return ans


def avoid_counts(b, length):
    counts = [1]
    for h in range(1, length + 1):
        if h < b:
            counts.append(1 << h)
        else:
            counts.append(sum(counts[h - q] for q in range(1, b + 1)))
    return counts


def is_prime(p):
    if p < 2:
        return False
    q = 2
    while q * q <= p:
        if p % q == 0:
            return False
        q += 1
    return True


def main():
    rng = random.Random(202610100253)
    totals = {'parameter_field_cases': 0, 'routed_rows': 0,
              'gram_pairs': 0, 'direct_first_return_vectors': 0,
              'batch_scalar_outputs': 0, 'small_basis_vectors': 0,
              'count_inequalities': 0}
    case_log = []
    params = [(n, b) for n in range(3, 11)
              for b in range(1, n) if n - 2 * b >= 1]
    params += [(12, 3), (12, 4), (14, 4)]
    for p in (65537, 998244353):
        assert is_prime(p)
        for n, b in params:
            N, d = 1 << n, n - b
            r, L = 1 << d, 1 << (b - 1)
            T = min(L, d - b)
            omega = pow(3, (p - 1) // N, p)
            assert (p - 1) % N == 0
            assert pow(omega, N, p) == 1 and pow(omega, N // 2, p) != 1
            eta = pow(omega, 1 << b, p)
            rows, sizes = packet_bank(r, d, b, T, omega, eta, p)
            counts = avoid_counts(b, max(0, T - 2))
            expected = [(1 << (d - b - t)) * (1 if t == 1 else counts[t - 2])
                        for t in range(1, T + 1)]
            assert sizes == expected
            totals['routed_rows'] += len(rows)
            # Exact finite-field analog of conjugation sends root to its inverse.
            # Every row coefficient is a root power, so reciprocal is correct.
            inv_rows = [{j: pow(c, -1, p) for j, c in row.items()}
                        for _t, _i, row in rows]
            for a, (t, _i, row) in enumerate(rows):
                for z in range(a, len(rows)):
                    dual = inv_rows[z]
                    if len(row) <= len(dual):
                        val = sum(c * dual.get(j, 0) for j, c in row.items()) % p
                    else:
                        val = sum(row.get(j, 0) * c for j, c in dual.items()) % p
                    assert val == ((1 << (b + t)) % p if a == z else 0)
                    totals['gram_pairs'] += 1
            vectors = [[rng.randrange(p) for _ in range(r)] for _ in range(2)]
            if n <= 6:
                vectors += [[int(j == a) for j in range(r)] for a in range(r)]
                totals['small_basis_vectors'] += r
            for u in vectors:
                packet = packets_apply(rows, u, r, p)
                q = list(u)
                direct = direct_first_returns(u, n, b, T, omega, p)
                for t in range(1, T + 1):
                    q = q_step(q, eta, p)
                    routed = route_after_q(q, t, b, omega, eta, p)
                    selected = [0] * r
                    for age, i, _row in rows:
                        if age == t:
                            selected[i] = packet[i]
                    assert routed == selected == direct[t]
                totals['direct_first_return_vectors'] += 1
            # Full arbitrary-jet temporal batch, not just one u vector.
            inputs = [[rng.randrange(p) for _ in range(r)] for _ in range(n + 1)]
            batch_q = [[0] * r for _ in range(n + 1)]
            batch_rows = [[0] * r for _ in range(n + 1)]
            for j, u in enumerate(inputs):
                q = list(u)
                for t in range(1, T + 1):
                    q = q_step(q, eta, p)
                    out_time = j + b + t
                    if out_time <= n:
                        routed = route_after_q(q, t, b, omega, eta, p)
                        for i, val in enumerate(routed):
                            batch_q[out_time][i] = (batch_q[out_time][i] + val) % p
                for t, i, row in rows:
                    out_time = j + b + t
                    if out_time <= n:
                        # Age supports are disjoint, hence this is assignment.
                        assert batch_rows[out_time][i] == 0
                        batch_rows[out_time][i] = sum(c * u[s] for s, c in row.items()) % p
            assert batch_q == batch_rows
            totals['batch_scalar_outputs'] += r * (n + 1)
            totals['parameter_field_cases'] += 1
            case_log.append({'p': p, 'n': n, 'b': b, 'T': T, 'rows': len(rows),
                             'row_counts': sizes})
    # Large symbolic count checks without enumerating exponentially large banks.
    volume_log = []
    for b in range(2, 13):
        L = 1 << (b - 1)
        counts = avoid_counts(b, L)
        scaled_sizes = [Fraction(1, 1 << (b + 1))]
        for t in range(2, L + 1):
            v = Fraction(counts[t - 2], 1 << (b + t))
            assert v >= Fraction(1, 16 * L)
            scaled_sizes.append(v)
            totals['count_inequalities'] += 1
        mass = sum(scaled_sizes)
        half_volume = sum(Fraction(b + t, 2) * v
                          for t, v in enumerate(scaled_sizes, 1))
        assert mass <= 1
        assert half_volume >= Fraction(L, 64)
        if b >= 7:
            assert half_volume - Fraction(1, 2) >= Fraction(L, 128)
        volume_log.append({'b': b, 'L': L, 'row_fraction': float(mass),
                           'half_log_volume_per_r': float(half_volume),
                           'guaranteed_log_minor_per_r': float(half_volume - Fraction(1, 2))})
    # Negative control: a forbidden word makes the age-1 and age-6 rows coincide
    # in frequency on the smaller support; their routes collide at index 33.
    p, n, b, d = 65537, 14, 4, 10
    omega = pow(3, (p - 1) // (1 << n), p)
    eta = pow(omega, 1 << b, p)
    t, k, tp, kp = 1, 1, 6, 33
    assert '0' * b in format(kp, f'0{tp}b')
    R = 1 << (d - b - t)
    q = 1
    assert (1 << (b + t)) * q + k == kp
    f, fp = reverse_bits(k, t), reverse_bits(kp, tp)
    raw_pairing = sum(pow(eta, j * (f - fp), p) for j in range(q, 1 << d, R)) % p
    assert raw_pairing != 0
    result = {'status': 'PASS', 'totals': totals, 'cases': case_log,
              'symbolic_volume_checks': volume_log,
              'negative_control': {'invalid_word': '100001', 'route_collision': 33,
                                   'reciprocal_root_pairing': raw_pairing,
                                   'field': p},
              'scope': 'Exact finite-field identities only; complex lower bound proved in report.'}
    Path(__file__).with_name('YOUNG_FEEDBACK_CONTROLS.json').write_text(
        json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'status': 'PASS', 'totals': totals,
                      'negative_control_pairing': raw_pairing}, sort_keys=True))


if __name__ == '__main__':
    main()
