#!/usr/bin/env python3
"""Fresh exact checks for batched Fourier reductions; no uploaded-code imports."""
import json
from pathlib import Path

P = 65537


def zeros(n):
    return [[0] * n for _ in range(n)]


def identity(n):
    z = zeros(n)
    for i in range(n):
        z[i][i] = 1
    return z


def mm(a, b):
    n = len(a)
    c = zeros(n)
    sb = [[(j, v) for j, v in enumerate(row) if v] for row in b]
    for i, row in enumerate(a):
        for k, v in enumerate(row):
            if v:
                for j, w in sb[k]:
                    c[i][j] += v * w
        c[i] = [v % P for v in c[i]]
    return c


def add(a, b):
    return [[(x + y) % P for x, y in zip(r, s)] for r, s in zip(a, b)]


def rt(n):
    if n == 1:
        return 1
    z = pow(3, (P - 1) // n, P)
    assert pow(z, n, P) == 1 and pow(z, n // 2, P) != 1
    return z


def fourier(n):
    w = rt(n)
    return [[pow(w, i * j, P) for j in range(n)] for i in range(n)]


def bank(m, q, active, inverse=False):
    z = zeros(m * q)
    eta = pow(rt(m), -1, P) if inverse else rt(m)
    norm = pow(m, -1, P) if inverse else 1
    for b in range(q):
        for i in range(m):
            for j in range(m):
                z[b * m + i][b * m + j] = norm * pow(eta, i * j, P) % P if b in active else int(i == j)
    return z


def batch(m, q):
    z = zeros(m * q)
    w = rt(q)
    for u in range(q):
        for r in range(q):
            for t in range(m):
                z[u * m + t][r * m + t] = pow(w, u * r, P)
    return z


def twiddle(m, q, inverse=False):
    z = zeros(m * q)
    w = pow(rt(m * q), -1, P) if inverse else rt(m * q)
    for r in range(q):
        for t in range(m):
            z[r * m + t][r * m + t] = pow(w, r * t, P)
    return z


def support_cover(pj, m, q, start, length):
    n = m * q
    dinv = twiddle(m, q, True)
    result = zeros(n)
    count = (q + length - 1) // length
    pieces = []
    for ell in range(count):
        low, high = ell * length, min((ell + 1) * length, q)
        shift = (start - low) % q
        masked_shift = zeros(n)
        for r in range(low, high):
            for t in range(m):
                masked_shift[((r + shift) % q) * m + t][r * m + t] = 1
        term = mm(pj, mm(dinv, masked_shift))
        for u in range(q):
            phase = pow(rt(q), (-shift * u) % q, P)
            for t in range(m):
                term[u * m + t] = [v * phase % P for v in term[u * m + t]]
        result = add(result, term)
        pieces.append({'input_interval': [low, high], 'shift': shift})
    return result, pieces


def bank_from_batch(ell, m, q):
    assert m % q == 0
    radix = m // q
    n = m * q
    pre, post = zeros(n), zeros(n)
    for b in range(q):
        for h in range(radix):
            for s in range(q):
                pre[s * m + (b * radix + h)][b * m + h + radix * s] = 1
    for b in range(q):
        for t in range(q):
            for u in range(radix):
                for h in range(radix):
                    post[b * m + t + q * u][t * m + b * radix + h] = pow(rt(m), h * t, P) * pow(rt(radix), h * u, P) % P
    return mm(post, mm(ell, pre)), radix


def check(m, q, start, length):
    n = m * q
    active = {(start + h) % q for h in range(length)}
    complement = set(range(q)) - active
    ell, delta, dinv = batch(m, q), twiddle(m, q), twiddle(m, q, True)
    c, ci = bank(m, q, complement), bank(m, q, complement, True)
    pj, pall = mm(ell, mm(delta, c)), mm(ell, delta)
    assert mm(pj, ci) == pall
    assert mm(pj, mm(ci, dinv)) == ell
    if length == q:
        assert mm(pj, dinv) == ell
    record = {'N': n, 'm': m, 'q': q, 'active_start': start, 'active_length': length,
              'inverse_bank_transforms_charged': q - length,
              'C_and_Delta_commute': mm(c, delta) == mm(delta, c),
              'incorrect_reordered_strip_happens_to_pass': mm(pj, mm(dinv, ci)) == ell}
    if length:
        recovered, pieces = support_cover(pj, m, q, start, length)
        assert recovered == ell
        record['support_cover_calls'] = len(pieces)
        record['cover_pieces'] = pieces
        if m % q == 0:
            full_bank, radix = bank_from_batch(recovered, m, q)
            assert full_bank == bank(m, q, set(range(q)))
            active_bank = identity(n)
            for r in active:
                for t in range(m):
                    active_bank[r * m + t] = full_bank[r * m + t][:]
            stride = zeros(n)
            for r in range(q):
                for t in range(m):
                    stride[r * m + t][r + q * t] = 1
            assert mm(pj, mm(active_bank, stride)) == fourier(n)
            record['full_F_N_calls_to_P_J'] = len(pieces) + 1
            record['paid_additional_small_radix'] = radix
            record['small_radix_transform_count'] = n // radix
            if m == q:
                complement_bank = identity(n)
                for r in complement:
                    for t in range(m):
                        complement_bank[r * m + t] = full_bank[r * m + t][:]
                assert mm(ell, mm(delta, complement_bank)) == pj
                record['reverse_P_J_from_L_calls'] = 1 if length == q else 2
    else:
        stride = zeros(n)
        for r in range(q):
            for t in range(m):
                stride[r * m + t][r + q * t] = 1
        assert mm(pj, stride) == fourier(n)
        record['full_F_N_calls_to_P_J'] = 1
    return record


def main():
    records = []
    for m, q in ((2, 2), (2, 4), (4, 4), (4, 8), (8, 8), (4, 2), (8, 4), (8, 2)):
        choices = {(0, 0), (0, q), (0, max(1, q // 2)), (q - 1, max(1, q // 2)), (q - 1, max(1, q // 2 - 1))}
        for start, length in sorted(choices):
            records.append(check(m, q, start, length))
    result = {'field': P, 'case_count': len(records),
              'noncommuting_C_Delta_controls': sum(not r['C_and_Delta_commute'] for r in records),
              'support_cover_controls': sum('support_cover_calls' in r for r in records),
              'full_F_N_reconstructions': sum('full_F_N_calls_to_P_J' in r for r in records),
              'all_exact_assertions_passed': True, 'cases': records,
              'scope': 'Exact reductions and cost accounting only; no evaluator for P_J is constructed.'}
    Path(__file__).with_name('BATCHED_EQUIVALENCE_CONTROLS.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({key: value for key, value in result.items() if key != 'cases'}, indent=2))


if __name__ == '__main__':
    main()
