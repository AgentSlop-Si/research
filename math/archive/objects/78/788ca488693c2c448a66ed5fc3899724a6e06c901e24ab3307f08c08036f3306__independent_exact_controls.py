#!/usr/bin/env python3
"""Fresh independent controls. Standard library only; never reads/imports target files."""
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, permutations
from math import comb, prod
from pathlib import Path
import json

OUT = Path(__file__).resolve().parent

def gamma(k):
    prefix = val = 0
    for bit in bin(k)[2:]:
        if bit == '1':
            val += prefix
        prefix = 2 * prefix + int(bit)
    return val

def rev(k, width):
    return int(format(k, f'0{width}b')[::-1], 2) if width else 0

def admissible(k, t, b):
    s = format(k, f'0{t}b')
    return len(s) == t and s[0] == s[-1] == '1' and '0' * b not in s

def ages(n, b):
    return range(1, min(2 ** (b - 1), n - 2 * b) + 1)

def supports(n, b):
    r = 2 ** (n - b)
    ans = {}
    occupied = set()
    for t in ages(n, b):
        row = {a for a in range(r) if a % (2 ** (b + t)) < 2 ** t
               and admissible(a % (2 ** t), t, b)}
        assert not occupied & row
        occupied |= row
        ans[t] = row
    return ans

def step(v, root, p):
    size = len(v)
    w = [0] * size
    z = 1
    for s, x in enumerate(v):
        w[(2 * s) % size] = (w[(2 * s) % size] + x) % p
        w[(2 * s + 1) % size] = (w[(2 * s + 1) % size] + z * x) % p
        z = z * root % p
    return w

def route(v, n, b, t, root, p, omit_phase=False):
    eta = pow(root, 2 ** b, p)
    ratio = root * pow(eta, -1, p) % p
    ans = [0] * len(v)
    for a, x in enumerate(v):
        k = a % (2 ** t)
        if admissible(k, t, b):
            dest = (2 ** b * (a - k) + k) % len(v)
            phase = 1 if omit_phase else pow(ratio, gamma(k), p)
            ans[dest] = (ans[dest] + phase * x) % p
    return ans

def first_return(u, n, b, length, root, p):
    size = 2 ** n
    v = [0] * size
    for a, val in enumerate(u):
        v[2 ** b * a] = val
    retained = {s for s in range(size)
                if s % (2 ** b) == 0 or '0' * b not in format(s, f'0{n}b')}
    for h in range(1, length + 1):
        v = step(v, root, p)
        if h < length:
            for s in retained:
                v[s] = 0
    return v[::2 ** b]

def primitive(n, p, odd):
    root = pow(3, ((p - 1) // (2 ** n)) * odd, p)
    assert pow(root, 2 ** n, p) == 1 and pow(root, 2 ** (n - 1), p) != 1
    return root

def source_controls():
    cases = []
    phase_witness = None
    params = [(n, b, 65537, odd) for n in range(3, 11)
              for b in range(1, min(4, (n - 1) // 2) + 1)
              for odd in ([1, 3] if n <= 6 else [3])]
    params += [(n, b, 257, 5) for n, b in [(4, 1), (5, 2), (6, 2), (7, 3), (8, 3)]]
    for n, b, p, odd in params:
        size = 2 ** n
        root = primitive(n, p, odd)
        eta = pow(root, 2 ** b, p)
        tests = [[(13 * s * s + 29 * s + 7) % p for s in range(size)]]
        if n <= 6:
            tests += [[int(s == i) for s in range(size)] for i in range(size)]
        supp = supports(n, b)
        checks = Counter()
        for x in tests:
            orbit = [x]
            for h in range(n):
                orbit.append(step(orbit[-1], root, p))
            jets = [v[::2 ** b] for v in orbit]
            # All actual retained coordinates, not just H's later selections.
            for h in range(b, n + 1):
                m = 2 ** (n - h)
                for a, expected in enumerate(jets[h]):
                    q, c = divmod(a, 2 ** (h - b))
                    f = rev(c, h - b)
                    got = pow(root, gamma(c), p) * sum(
                        x[s] * pow(root, s * f, p) for s in range(q, size, m)) % p
                    assert got == expected, ('packet', n, b, h, a)
                    checks['all_source_packet_values'] += 1
            batch = [[0] * len(jets[0]) for _ in range(n + 1)]
            for t, support in supp.items():
                for j in range(n - b - t + 1):
                    v = jets[j]
                    for _ in range(t):
                        v = step(v, eta, p)
                    got = route(v, n, b, t, root, p)
                    direct = first_return(jets[j], n, b, b + t, root, p)
                    assert got == direct, ('first-return', n, b, j, t)
                    wanted = [jets[j + b + t][a] if a in support else 0
                              for a in range(len(got))]
                    assert got == wanted, ('alias', n, b, j, t)
                    checks['alias_coordinates'] += len(got)
                    checks['direct_first_return_coordinates'] += len(got)
                    for a, val in enumerate(got):
                        batch[j + b + t][a] = (batch[j + b + t][a] + val) % p
                    if phase_witness is None and route(v, n, b, t, root, p, True) != got:
                        phase_witness = {'n': n, 'b': b, 't': t, 'j': j, 'field': p, 'odd': odd}
            for h in range(n + 1):
                active = set().union(*(s for t, s in supp.items() if b + t <= h))
                assert batch[h] == [jets[h][a] if a in active else 0 for a in range(len(jets[h]))]
                checks['summed_batch_coordinates'] += len(jets[h])
        cases.append({'n': n, 'b': b, 'field': p, 'odd_embedding': odd,
                      'inputs': len(tests), **checks})
    assert phase_witness is not None
    return cases, phase_witness

# Exact primitive 2^n root representation: Z[z]/(z^(2^(n-1))+1).
def radd(a, exponent, value, size):
    exponent %= size
    if exponent >= size // 2:
        exponent -= size // 2
        value = -value
    a[exponent] = a.get(exponent, 0) + value
    if not a[exponent]:
        del a[exponent]

def rmul(a, b, size):
    c = {}
    for i, x in a.items():
        for j, y in b.items():
            radd(c, i + j, x * y, size)
    return c

def rconj(a, size):
    c = {}
    for i, x in a.items():
        radd(c, -i, x, size)
    return c

def literal_path_rows(n):
    size = 2 ** n
    layers = [[{} for _ in range(size)] for _ in range(n + 1)]
    for source in range(size):
        paths = {source: 0}
        layers[0][source][source] = 0
        for h in range(1, n + 1):
            new = {}
            for state, exponent in paths.items():
                for bit in (0, 1):
                    target = (2 * state + bit) % size
                    assert target not in new  # Unique appended word for h <= n.
                    new[target] = (exponent + bit * state) % size
            paths = new
            for target, exponent in paths.items():
                layers[h][target][source] = exponent
    return layers

def packet_events(n, b, ell):
    ans = []
    for h in range(1, n + 1):
        word = format(ell % (2 ** h), f'0{h}b')
        for t in ages(n, b):
            if h < 2 * b + t:
                continue
            middle = word[b:b + t]
            if word[:b] == '0' * b and word[b + t:2 * b + t] == '0' * b \
                    and middle[0] == middle[-1] == '1' and '0' * b not in middle:
                ans.append((h, t))
    return ans

def selected_rows(n, b, layers):
    answer = []
    for t, support in supports(n, b).items():
        for h in range(2 * b + t, n + 1):
            banks = defaultdict(set)
            for a in sorted(support):
                q, c = divmod(a, 2 ** (h - b))
                f = rev(c, h - b)
                banks[f].add(q)
                row = layers[h][2 ** b * a]
                assert set(row) == set(range(q, 2 ** n, 2 ** (n - h)))
                assert all(e == (gamma(c) + s * f) % (2 ** n) for s, e in row.items())
                answer.append((h, t, a, row))
            expected_f = {
                rev(k, t) * 2 ** (h - b - t) + v
                for k in range(2 ** t) if admissible(k, t, b)
                for v in range(2 ** (h - 2 * b - t))}
            assert set(banks) == expected_f
            assert all(qs == set(range(2 ** (n - h))) for qs in banks.values())
    return answer

def rank_mod(matrix, p):
    a = [r[:] for r in matrix]
    if not a:
        return 0
    rank = 0
    for j in range(len(a[0])):
        pivot = next((i for i in range(rank, len(a)) if a[i][j] % p), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        inv = pow(a[rank][j], -1, p)
        a[rank] = [x * inv % p for x in a[rank]]
        for i in range(rank + 1, len(a)):
            factor = a[i][j]
            if factor:
                a[i] = [(x - factor * y) % p for x, y in zip(a[i], a[rank])]
        rank += 1
        if rank == len(a):
            break
    return rank

def spectral_controls():
    cases = []
    row_cache = {}
    for n in range(3, 8):
        layers = literal_path_rows(n)
        size = 2 ** n
        for b in range(1, (n - 1) // 2 + 1):
            rows = selected_rows(n, b, layers)
            lambdas = [sum(2 ** h for h, t in packet_events(n, b, ell)) for ell in range(size)]
            mus = [len(packet_events(n, b, ell)) for ell in range(size)]
            gram = [[{} for _ in range(size)] for _ in range(size)]
            normalized_scaled_gram = [[{} for _ in range(size)] for _ in range(size)]
            for h, t, a, row in rows:
                for i, ei in row.items():
                    for j, ej in row.items():
                        radd(gram[i][j], ej - ei, 1, size)
                        radd(normalized_scaled_gram[i][j], ej - ei, 2 ** (n - h), size)
            spectra = []
            normalized_spectra = []
            for delta in range(size):
                val, normalized = {}, {}
                for ell in range(size):
                    radd(val, ell * delta, lambdas[ell], size)
                    radd(normalized, ell * delta, size * mus[ell], size)
                spectra.append(val)
                normalized_spectra.append(normalized)
            for i in range(size):
                for j in range(size):
                    assert {e: size * v for e, v in gram[i][j].items()} == spectra[(j - i) % size]
                    assert {e: size * v for e, v in normalized_scaled_gram[i][j].items()} == normalized_spectra[(j - i) % size]
            root = primitive(n, 65537, 3)
            dense = [[pow(root, row[s], 65537) if s in row else 0 for s in range(size)]
                     for h, t, a, row in rows]
            rank = rank_mod(dense, 65537)
            assert rank == sum(v > 0 for v in lambdas)
            stack = [[pow(root, row[s], 65537) if s in row else 0 for s in range(size)]
                     for h in range(b, n + 1) for row in layers[h][::2 ** b]]
            stack_rank = rank_mod(stack, 65537)
            assert stack_rank == sum('0' * b in format(ell, f'0{n}b') for ell in range(size))
            assert sum(mus) == len(rows) and max(mus) <= n
            cases.append({'n': n, 'b': b, 'rows': len(rows), 'rank': rank,
                          'complete_stack_rank': stack_rank, 'exact_gram_entries': size ** 2,
                          'exact_normalized_gram_entries': size ** 2,
                          'spectral_weight_histogram': dict(sorted(Counter(lambdas).items())),
                          'normalized_spectral_histogram': dict(sorted(Counter(mus).items()))})
            if (n, b) in [(3, 1), (4, 1), (5, 2)]:
                row_cache[n, b] = (rows, lambdas, mus)
    return cases, row_cache

def permutation_sign(p):
    return -1 if sum(p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p))) % 2 else 1

def minor(rows, cols, size):
    k = len(rows)
    if k == 0:
        return {0: 1}
    ans = {}
    for permutation in permutations(range(k)):
        terms = [rows[i].get(cols[permutation[i]]) for i in range(k)]
        if all(t is not None for t in terms):
            radd(ans, sum(terms), permutation_sign(permutation), size)
    return ans

def minor_controls(cache):
    cases = []
    for (n, b), (rows, lambdas, mus) in sorted(cache.items()):
        size = 2 ** n
        total, normalized_total = {}, {}
        count = 0
        for k in range(min(size, len(rows)) + 1):
            for selected in combinations(rows, k):
                scale = Fraction(1, 2 ** sum(row[0] for row in selected))
                for cols in combinations(range(size), k):
                    determinant = minor([row[3] for row in selected], cols, size)
                    square = rmul(rconj(determinant, size), determinant, size)
                    for e, value in square.items():
                        radd(total, e, value, size)
                        radd(normalized_total, e, scale * value, size)
                    count += 1
        assert count == comb(size + len(rows), size)
        assert total == {0: prod(1 + v for v in lambdas)}
        assert normalized_total == {0: prod(1 + v for v in mus)}
        cases.append({'n': n, 'b': b, 'N': size, 'D': len(rows), 'all_augmented_minors': count,
                      'det_I_plus_gram': total[0], 'det_I_plus_normalized_gram': int(normalized_total[0])})
    return cases

def compatible_probability(b, shift):
    pattern = '1' + '0' * b + '1'
    positions = {}
    for start in (0, shift):
        for i, value in enumerate(pattern):
            if start + i in positions and positions[start + i] != value:
                return Fraction(0)
            positions[start + i] = value
    return Fraction(1, 2 ** len(positions))

def marker_controls():
    for b in range(1, 65):
        p = Fraction(1, 2 ** (b + 2))
        for shift in range(1, 2 * b + 5):
            expected = 0 if shift <= b else 2 * p * p if shift == b + 1 else p * p
            assert compatible_probability(b, shift) == expected
    moments = []
    for b in range(7, 513):
        m = 2 ** (b - 2)
        a = m - b - 1
        p = Fraction(1, 2 ** (b + 2))
        mean = a * p
        edge_overlap_pairs = max(0, a - b - 1)
        q = max(0, a - b - 2)
        second = mean + 4 * edge_overlap_pairs * p * p + q * (q + 1) * p * p
        loose = mean + mean * mean + 4 * mean * p
        assert Fraction(1, 32) <= mean <= Fraction(1, 16)
        assert second <= loose < 2 * mean
        assert mean * mean / second >= Fraction(1, 64)
        assert (mean * mean / second) ** 2 >= Fraction(1, 4096)
        if b <= 10:
            moments.append({'b': b, 'mean': str(mean), 'second_moment': str(second),
                            'one_half_probability_lower_bound': str(mean * mean / second)})
    top_cases = []
    for b, width in [(1, 8), (2, 10), (3, 12), (4, 14), (5, 16)]:
        qualifying = 0
        witnesses = 0
        pattern = '1' + '0' * b + '1'
        for block in range(2 ** width):
            word = format(block, f'0{width}b')
            occurrences = [i for i in range(width - len(pattern) + 1) if word[i:i + len(pattern)] == pattern]
            if len(occurrences) < 2:
                continue
            qualifying += 1
            # Extract maximal zero runs; pick successive long runs, not arbitrary occurrences.
            runs = []
            i = 0
            while i < width:
                if word[i] == '1':
                    i += 1
                    continue
                end = i
                while end < width and word[end] == '0':
                    end += 1
                if end - i >= b:
                    runs.append((i, end))
                i = end
            assert len(runs) >= 2
            left, right = runs[0], runs[1]
            start = left[1] - b
            middle = word[left[1]:right[0]]
            t = len(middle)
            assert 1 <= t <= width and middle[0] == middle[-1] == '1' and '0' * b not in middle
            for tail in ('', '10101'):
                whole = word + tail
                n = len(whole)
                h = n - start
                assert h >= n - width and h >= 2 * b + t
                assert whole[start:start + 2 * b + t] == '0' * b + middle + '0' * b
                # Direct unrestricted-t event test; short exhaustive widths need not be 2^(b-1).
                low = format(int(whole, 2) % (2 ** h), f'0{h}b')
                assert low[:b] == low[b + t:2 * b + t] == '0' * b
                witnesses += 1
        top_cases.append({'b': b, 'top_window_width': width, 'qualifying_blocks': qualifying,
                          'top_position_witnesses': witnesses})
    return {'overlap_b_values': 64, 'moment_b_values': 506,
            'sample_exact_moments': moments, 'exhaustive_top_position_cases': top_cases}

def main():
    source, phase = source_controls()
    spectral, cache = spectral_controls()
    minors = minor_controls(cache)
    markers = marker_controls()
    summary = {'source_cases': len(source), 'source_inputs': sum(c['inputs'] for c in source),
               **{key: sum(c[key] for c in source) for key in ['all_source_packet_values', 'alias_coordinates',
                    'direct_first_return_coordinates', 'summed_batch_coordinates']},
               'cyclotomic_gram_cases': len(spectral),
               'cyclotomic_gram_entries': sum(c['exact_gram_entries'] for c in spectral),
               'cyclotomic_normalized_gram_entries': sum(c['exact_normalized_gram_entries'] for c in spectral),
               'exact_augmented_minors': sum(c['all_augmented_minors'] for c in minors),
               'moment_b_values': markers['moment_b_values']}
    payload = {'scope': 'Fresh exact controls; no target program is read, imported, or executed. Cyclotomic tests are exact complex-root identities; finite-field tests do not prove a finite-field lower bound.',
               'summary': summary, 'source_cases': source, 'phase_omission_negative_control': phase,
               'spectral_cases': spectral, 'minor_cases': minors, 'marker_controls': markers}
    encoded = json.dumps(payload, indent=2, sort_keys=True) + '\n'
    (OUT / 'INDEPENDENT_CONTROLS.json').write_text(encoded)
    print(json.dumps(summary, sort_keys=True))
    print('PASS: source aliases, first returns, phases, complete q banks, exact cyclotomic Gram, normalized Gram, ranks, all selected augmented minors, overlap moments, and top-window positioning.')

if __name__ == '__main__':
    main()
