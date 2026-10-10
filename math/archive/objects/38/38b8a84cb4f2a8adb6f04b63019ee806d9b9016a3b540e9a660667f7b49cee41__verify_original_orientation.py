#!/usr/bin/env python3
"""New standalone exact controls for the original q=r*m bank orientation."""
import json
from pathlib import Path

FIELD = 65537


def zero(n):
    return [[0] * n for _ in range(n)]


def eye(n):
    a = zero(n)
    for j in range(n):
        a[j][j] = 1
    return a


def mm(a, b):
    n = len(a)
    c = zero(n)
    sb = [[(j, v) for j, v in enumerate(row) if v] for row in b]
    for i, row in enumerate(a):
        for k, v in enumerate(row):
            if v:
                for j, w in sb[k]:
                    c[i][j] += v * w
        c[i] = [v % FIELD for v in c[i]]
    return c


def root(n):
    return pow(3, (FIELD - 1) // n, FIELD)


def fourier(n):
    return [[pow(root(n), i * j, FIELD) for j in range(n)] for i in range(n)]


def bank(m, q, active):
    a = zero(m * q)
    for b in range(q):
        for t in range(m):
            for s in range(m):
                a[b * m + t][b * m + s] = pow(root(m), t * s, FIELD) if b in active else int(t == s)
    return a


def batch(m, q):
    a = zero(m * q)
    for t in range(q):
        for s in range(q):
            for g in range(m):
                a[t * m + g][s * m + g] = pow(root(q), t * s, FIELD)
    return a


def twiddle(m, q, inverse=False):
    a = zero(m * q)
    w = pow(root(m * q), -1, FIELD) if inverse else root(m * q)
    for b in range(q):
        for s in range(m):
            a[b * m + s][b * m + s] = pow(w, b * s, FIELD)
    return a


def conversion(m, r):
    q, n = r * m, r * m * m
    packing, recovery = zero(n), zero(n)
    ir = pow(r, -1, FIELD)
    for g in range(m):
        for h in range(r):
            for s in range(m):
                packing[(h + r * s) * m + g][(g * r + h) * m + s] = 1
            for t in range(m):
                for u in range(r):
                    recovery[(g * r + h) * m + t][(t + m * u) * m + g] = ir * pow(root(q), (-t * h) % q, FIELD) * pow(root(r), (-h * u) % r, FIELD) % FIELD
    assert all(sum(row) == 1 for row in packing)
    assert all(sum(row) == 1 for row in zip(*packing))
    assert sum(bool(x) for row in recovery for x in row) == r * n
    return packing, recovery


def cover(pmat, m, q, start, length):
    n = m * q
    recovered = zero(n)
    inverse_delta = twiddle(m, q, True)
    count = (q + length - 1) // length
    for part in range(count):
        low, high = part * length, min((part + 1) * length, q)
        a = (start - low) % q
        masked_shift = zero(n)
        for b in range(low, high):
            for s in range(m):
                masked_shift[((b + a) % q) * m + s][b * m + s] = 1
        term = mm(pmat, mm(inverse_delta, masked_shift))
        for u in range(q):
            phase = pow(root(q), (-a * u) % q, FIELD)
            for s in range(m):
                i = u * m + s
                recovered[i] = [(v + phase * w) % FIELD for v, w in zip(recovered[i], term[i])]
    return recovered, count


def check(m, radix):
    q, n = radix * m, radix * m * m
    ell = batch(m, q)
    packing, recovery = conversion(m, radix)
    expected_bank = bank(m, q, set(range(q)))
    assert mm(recovery, mm(ell, packing)) == expected_bank
    stride = zero(n)
    for b in range(q):
        for s in range(m):
            stride[b * m + s][b + q * s] = 1
    cases = []
    for start, length in sorted({(0, q), (0, q // 2), (q - 1, q // 2), (q - 1, max(1, q // 2 - 1))}):
        active = {(start + h) % q for h in range(length)}
        c = bank(m, q, set(range(q)) - active)
        pmat = mm(ell, mm(twiddle(m, q), c))
        recovered_ell, calls = cover(pmat, m, q, start, length)
        assert recovered_ell == ell
        recovered_bank = mm(recovery, mm(recovered_ell, packing))
        assert recovered_bank == expected_bank
        active_bank = eye(n)
        for b in active:
            for t in range(m):
                active_bank[b * m + t] = recovered_bank[b * m + t][:]
        assert mm(pmat, mm(active_bank, stride)) == fourier(n)
        cases.append({'active_start': start, 'active_length': length, 'batch_P_calls': calls,
                      'full_F_N_P_calls': calls + 1})
    return {'m': m, 'q': q, 'N': n, 'inverse_small_radix': radix,
            'inverse_small_radix_transform_count': n // radix,
            'unchanged_bank_dimensions': [q, m], 'packing_nonzeros': n,
            'recovery_nonzeros': radix * n, 'cases': cases}


def main():
    rows = [check(m, radix) for m, radix in ((2, 2), (4, 2), (8, 2), (2, 4), (4, 4))]
    result = {'field': FIELD, 'bank_conversion_cases': len(rows),
              'full_F_N_reconstruction_cases': sum(len(r['cases']) for r in rows),
              'all_exact_assertions_passed': True, 'results': rows,
              'scope': 'Original q=r*m orientation retained; no P evaluator or FFT speedup constructed.'}
    Path(__file__).with_name('ORIGINAL_ORIENTATION_CONTROLS.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
