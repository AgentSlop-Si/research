#!/usr/bin/env python3
"""Fresh exact controls; predecessor code is never imported or executed."""
import hashlib
import json
import random
from pathlib import Path

from operator_cores import prepare, evaluate, apply_dense

HERE = Path(__file__).resolve().parent


def direct_order(n):
    return [k // 2 if k % 2 == 0 else n - 1 - k // 2 for k in range(n)]


def subset(code, positions):
    return sum(((code >> i) & 1) << p for i, p in enumerate(positions))


def chirp(t, w, N, p):
    return pow(w, (-t * (t + 1) // 2) % N, p)


def rank(matrix, p):
    A = [r[:] for r in matrix]
    r = 0
    for c in range(len(A[0])):
        pivot = next((i for i in range(r, len(A)) if A[i][c]), None)
        if pivot is None:
            continue
        A[r], A[pivot] = A[pivot], A[r]
        inverse = pow(A[r][c], -1, p)
        A[r] = [(v * inverse) % p for v in A[r]]
        for i in range(r + 1, len(A)):
            f = A[i][c]
            if f:
                A[i] = [(a - f * b) % p for a, b in zip(A[i], A[r])]
        r += 1
        if r == len(A):
            break
    return r


def unfold(n, k, w, p, fourier=False, header_mask=None):
    N = 1 << n
    positions = direct_order(n)
    left = [subset(i, positions[:k]) for i in range(1 << k)]
    right = [subset(i, positions[k:]) for i in range(1 << (n - k))]
    f = (lambda ell, s: pow(w, ell * s % N, p)) if fourier else (
        lambda ell, s: chirp(ell - s, w, N, p))
    def masked(ell, source):
        if header_mask is not None:
            K, headers = header_mask
            if ell >> (n - K) not in headers:
                return 0
        return f(ell, source)
    return [[masked(lp + lr, sp + sr) for lr in right for sr in right]
            for lp in left for sp in left]


def expected_frontier(n, k, bridge, x, w, p):
    """Independent closed forms for every materialized intermediate."""
    N = 1 << n
    pi = direct_order(n)
    j, m = (k + 1) // 2, n - k
    r = 1 if k == n else 2 ** (min(j, m) + 1) - 1
    radius = (r - 1) // 2
    left = [subset(c, pi[:k]) for c in range(1 << k)]
    right = [subset(c, pi[k:]) for c in range(1 << m)]
    out, feasible = [], 0
    for lp in left:
        for sr in right:
            for state in range(-radius, radius + 1):
                if k < bridge:
                    al = lp % (1 << j)
                    a_source = al - state
                    ok = 0 <= a_source < (1 << j)
                    z = sum(x[sp + sr] * chirp(lp - sp, w, N, p)
                            for sp in left if sp % (1 << j) == a_source) if ok else 0
                else:
                    output_middle = (sr >> j) + state
                    ok = 0 <= output_middle < (1 << m)
                    ell = lp + (output_middle << j)
                    z = sum(x[sp + sr] * chirp(ell - sp - sr, w, N, p)
                            for sp in left)
                out.append(z % p)
                feasible += int(ok)
    assert feasible == N * 2 ** min(j, m)
    return out, feasible


def main():
    rng = random.Random(430318)
    results = {'constructor_instances': [], 'rank_controls': [],
               'selected_mask_rank_controls': [],
               'application_controls': [], 'integer_controls': 0,
               'coefficient_checks': 0, 'pair_evaluations': 0,
               'frontier_entry_checks': 0, 'negative_controls': []}
    # Multiple supplied fields, varied primitive embeddings, small exhaustive cases.
    specifications = [(3, 2, 1), (5, 2, 2), (17, 3, 4), (97, 5, 5),
                      (257, 3, 6), (65537, 3, 8)]
    for prime, generator, max_n in specifications:
        for n in range(1, max_n + 1):
            N = 1 << n
            base = pow(generator, (prime - 1) // N, prime)
            for u in sorted({a % N for a in (1, 3, 5)}):
                w = pow(base, u, prime)
                assert pow(w, N, prime) == 1 and pow(w, N // 2, prime) != 1
                cores, bill = prepare(n, w, prime)
                W = 1 << ((n + 1) // 3)
                assert bill['width'] == (1 if n == 1 else 2 * W - 1)
                assert bill['scalar_core_slots'] <= 16 * W * W + 32 * W
                assert bill['bridge_table_slots'] <= 8 * W * W
                # Every individual coefficient and transition, including signed differences.
                for k, core in enumerate(cores, 1):
                    pos = direct_order(n)[k - 1]
                    for a, lb, sb, b, value in core:
                        delta = lb - sb
                        if k < bill['bridge']:
                            v = (1 << pos) * delta
                            wanted = chirp(v, w, N, prime) * pow(w, (-a * v) % N, prime) % prime
                            assert b == (a + v if k % 2 else a)
                        elif k == bill['bridge']:
                            v = (1 << pos) * delta + (b << ((k + 1) // 2))
                            wanted = chirp(v, w, N, prime) * pow(w, (-a * v) % N, prime) % prime
                        else:
                            wanted = 1
                            assert a == (delta + 2 * b if k % 2 else delta * (1 << (n - k)) + b)
                        assert value == wanted
                        results['coefficient_checks'] += 1
                pairs = [(ell, s) for ell in range(N) for s in range(N)] if n <= 5 else [
                    (rng.randrange(N), rng.randrange(N)) for _ in range(128)]
                for ell, source in pairs:
                    assert evaluate(cores, n, ell, source, prime) == chirp(ell - source, w, N, prime)
                    results['pair_evaluations'] += 1
                results['constructor_instances'].append({'prime': prime, 'embedding': u, **bill})
                if n <= 5 and (prime in (17, 97, 65537)):
                    for k in range(1, n):
                        j, m = (k + 1) // 2, n - k
                        want_c = min(2 ** (j + 1) - 1, 2 ** (m + 1) - 1, 2 ** (n - j))
                        want_f = 4 ** min(j, m)
                        rc = rank(unfold(n, k, w, prime), prime)
                        rf = rank(unfold(n, k, w, prime, True), prime)
                        assert (rc, rf) == (want_c, want_f)
                        results['rank_controls'].append(dict(prime=prime, n=n, embedding=u,
                                                             cut=k, chirp_rank=rc, dft_rank=rf))
    # A larger operator-only case verifies paid construction without building N^2 data.
    for n in (12, 16):
        prime, N = 65537, 1 << n
        w = pow(3, (prime - 1) // N, prime)
        cores, bill = prepare(n, w, prime)
        for _ in range(128):
            ell, source = rng.randrange(N), rng.randrange(N)
            assert evaluate(cores, n, ell, source, prime) == chirp(ell - source, w, N, prime)
            results['pair_evaluations'] += 1
        results['constructor_instances'].append({'prime': prime, 'embedding': 1, **bill})
    # Full all-input application and DFT conversion, including selected header blocks.
    for n in range(1, 10):
        prime, N = 65537, 1 << n
        w = pow(3, (prime - 1) // N, prime)
        cores, construction = prepare(n, w, prime)
        x = [rng.randrange(prime) for _ in range(N)]
        K = min(3, n)
        headers = [a for a in range(1 << K) if a % 3 != 1]
        selected = [ell for ell in range(N) if ell >> (n - K) in headers]
        seen = []

        def observe(k, actual):
            if n <= 6:
                expected, feasible = expected_frontier(n, k, construction['bridge'], x, w, prime)
                assert actual == expected
                results['frontier_entry_checks'] += len(actual)
                seen.append(feasible)

        actual, application = apply_dense(cores, n, x, prime, selected, observe)
        expected = [sum(x[s] * chirp(ell - s, w, N, prime) for s in range(N)) % prime
                    for ell in selected]
        assert actual == expected
        updates = (N // 2) * construction['scalar_core_slots']
        assert application['multiplications'] == application['additions'] == updates
        assert application['zero_initializations'] == N * sum(construction['ranks'][1:])
        # Convert dense DFT input using only diagonal chirps already present in the field.
        diagonal_input = [x[s] * pow(w, s * (s - 1) // 2 % N, prime) % prime for s in range(N)]
        via_c, _ = apply_dense(cores, n, diagonal_input, prime, selected)
        fourier = [v * pow(w, ell * (ell + 1) // 2 % N, prime) % prime
                   for ell, v in zip(selected, via_c)]
        direct_f = [sum(x[s] * pow(w, ell * s % N, prime) for s in range(N)) % prime
                    for ell in selected]
        assert fourier == direct_f
        results['application_controls'].append(dict(n=n, outputs=len(selected),
                                                    frontier_feasible_counts=seen, **application))
    # All-size combinatorial identities, including the exceptional n=2 MPO minimum.
    for n in (4, 5, 6):
        prime, N = 65537, 1 << n
        w = pow(3, (prime - 1) // N, prime)
        for k in range(2, n):
            j, m = (k + 1) // 2, n - k
            mask = (1, {0})
            rc = rank(unfold(n, k, w, prime, header_mask=mask), prime)
            rf = rank(unfold(n, k, w, prime, fourier=True, header_mask=mask), prime)
            assert rc == 2 ** (min(j, m) + 1) - 1
            assert rf == 4 ** min(j, m)
            results['selected_mask_rank_controls'].append(
                dict(n=n, cut=k, K=1, headers=[0], chirp_rank=rc, dft_rank=rf))
    for n in range(1, 1001):
        W = 1 << ((n + 1) // 3)
        rs = [min(2 ** (((k + 1) // 2) + 1) - 1,
                  2 ** (n - k + 1) - 1, 2 ** (n - (k + 1) // 2)) for k in range(1, n)]
        max_rank = max(rs, default=1)
        assert max_rank == (1 if n == 1 else 2 if n == 2 else 2 * W - 1)
        assert max([4 ** min((k + 1) // 2, n - k) for k in range(1, n)], default=1) == W * W
        bridge = next(k for k in range(1, n + 1) if (k + 1) // 2 >= n - k)
        A, M = 1 << (bridge // 2), 1 << (n - bridge)
        assert W // 2 <= A <= W and W // 2 <= M <= W
        uniform = [1] + [2 ** (min((k + 1) // 2, n - k) + 1) - 1
                         for k in range(1, n)] + [1]
        slots = (4 * sum(uniform[k - 1] for k in range(1, bridge))
                 + 4 * uniform[bridge - 1] * uniform[bridge]
                 + 4 * sum(uniform[k] for k in range(bridge + 1, n + 1)))
        assert W * W <= slots <= 16 * W * W + 32 * W
        assert sum(uniform[1:]) <= 16 * W
        results['integer_controls'] += 1
    # These controls must fail, not quietly pass under a wrong transfer of width/error.
    try:
        prepare(5, 1, 65537)
        raise AssertionError('nonprimitive root accepted')
    except ValueError:
        results['negative_controls'].append('nonprimitive root rejected')
    n, N, p = 5, 32, 65537
    w = pow(3, (p - 1) // N, p)
    cores, bill = prepare(n, w, p)
    bad = [[(a, l, s, b, 1 if k == bill['bridge'] else value)
            for a, l, s, b, value in core] for k, core in enumerate(cores, 1)]
    assert any(evaluate(bad, n, ell, s, p) != chirp(ell - s, w, N, p)
               for ell in range(4) for s in range(4))
    results['negative_controls'].append('dropping bridge phase changes the operator')
    assert rank(unfold(5, 3, w, p, True), p) == 16 > 7
    results['negative_controls'].append('DFT paired MPO cannot inherit chirp width 7 at n=5')
    w4 = pow(3, (p - 1) // 4, p)
    assert rank(unfold(2, 1, w4, p), p) == 2 != 3
    results['negative_controls'].append('n=2 root-order cap prevents false chirp rank 3')
    x = list(range(N))
    y, _ = apply_dense(cores, n, x, p)
    dft = [sum(x[s] * pow(w, ell * s % N, p) for s in range(N)) % p for ell in range(N)]
    assert y != dft
    results['negative_controls'].append('omitting input/output chirp diagonals fails DFT conversion')
    results['summary'] = {key: len(results[key]) for key in
                          ('constructor_instances', 'rank_controls', 'application_controls', 'negative_controls')}
    results['summary']['selected_mask_rank_controls'] = len(results['selected_mask_rank_controls'])
    results['summary'].update({key: results[key] for key in
                               ('integer_controls', 'coefficient_checks', 'pair_evaluations', 'frontier_entry_checks')})
    data = json.dumps(results, indent=2, sort_keys=True) + '\n'
    (HERE / 'CHECK_RESULTS.json').write_text(data)
    print(json.dumps(results['summary'], sort_keys=True))
    print('CHECK_RESULTS.json sha256=' + hashlib.sha256(data.encode()).hexdigest())


if __name__ == '__main__':
    main()
