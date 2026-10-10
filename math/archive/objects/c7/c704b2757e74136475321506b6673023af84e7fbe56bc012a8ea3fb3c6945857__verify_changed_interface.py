#!/usr/bin/env python3
"""New exact changed-interface checks; imports no uploaded or prior program."""
import json
from pathlib import Path

P = 65537


def z(n, m=None):
    return [[0] * (n if m is None else m) for _ in range(n)]


def eye(n):
    a = z(n)
    for i in range(n):
        a[i][i] = 1
    return a


def add(a, b, sign=1):
    return [[(v + sign * w) % P for v, w in zip(r, s)] for r, s in zip(a, b)]


def scale(a, c):
    return [[v * c % P for v in row] for row in a]


def mm(a, b):
    c = z(len(a), len(b[0]))
    sb = [[(j, v) for j, v in enumerate(row) if v] for row in b]
    for i, row in enumerate(a):
        for k, v in enumerate(row):
            if v:
                for j, w in sb[k]:
                    c[i][j] += v * w
        c[i] = [v % P for v in c[i]]
    return c


def kron(a, b):
    out = z(len(a) * len(b), len(a[0]) * len(b[0]))
    for i, row in enumerate(a):
        for j, v in enumerate(row):
            if v:
                for r, br in enumerate(b):
                    for s, w in enumerate(br):
                        out[i * len(b) + r][j * len(b[0]) + s] = v * w % P
    return out


def root(n):
    return pow(3, (P - 1) // n, P)


def fourier(n, inverse=False):
    w = pow(root(n), -1, P) if inverse else root(n)
    norm = pow(n, -1, P) if inverse else 1
    return [[norm * pow(w, i * j, P) % P for j in range(n)] for i in range(n)]


def shift(n, step=1):
    a = z(n)
    for j in range(n):
        a[(j + step) % n][j] = 1
    return a


def diag(values):
    a = z(len(values))
    for i, v in enumerate(values):
        a[i][i] = v % P
    return a


def transpose_grid(m):
    a = z(m * m)
    for r in range(m):
        for s in range(m):
            a[s * m + r][r * m + s] = 1
    return a


def degree(a):
    return {'nnz': sum(bool(v) for row in a for v in row),
            'row': max(sum(bool(v) for v in row) for row in a),
            'column': max(sum(bool(v) for v in row) for row in zip(*a))}


def basic(m):
    n = m * m
    k = transpose_grid(m)
    b, bi = kron(eye(m), fourier(m)), kron(eye(m), fourier(m, True))
    ell = kron(fourier(m), eye(m))
    delta = diag([pow(root(n), r * s, P) for r in range(m) for s in range(m)])
    qmat = mm(delta, ell)
    return n, k, b, bi, ell, delta, qmat


def relocated_controls():
    rows = []
    for m in (2, 4, 8, 16):
        n, k, b, bi, ell, delta, qmat = basic(m)
        f, s, d, si = fourier(n), shift(n), diag([pow(root(n), j, P) for j in range(n)]), shift(n, -1)
        assert mm(k, mm(b, qmat)) == f
        actions = []
        for x, y in ((s, d), (d, si)):
            a = mm(k, mm(y, k))
            t = mm(bi, mm(a, b))
            assert mm(a, b) == mm(b, t)
            assert mm(t, qmat) == mm(qmat, x)
            assert mm(k, a) == mm(y, k)
            assert degree(a)['row'] == degree(a)['column'] == 1
            assert degree(t)['row'] == degree(t)['column'] == 1
            actions.append((a, t))
        expected_t1 = z(n)
        expected_t2 = z(n)
        for bank_index in range(m):
            for j in range(m):
                expected_t1[bank_index * m + (j + 1) % m][bank_index * m + j] = pow(root(n), bank_index, P)
                out_bank = (bank_index - 1) % m
                expected_t2[out_bank * m + j][bank_index * m + j] = pow(root(m), j, P) if bank_index == 0 else 1
        assert actions[0][1] == expected_t1
        assert actions[1][1] == expected_t2
        rows.append({'M': m, 'N': n, 'P_degree': degree(k), 'Q_degree': degree(qmat), 'all_four_action_degrees': 1,
                     'Q_possible_as_two_zero_mask_layers_by_support': m <= 4})
    return rows


def swap_controls():
    rows = []
    for m in (2, 4, 8, 16):
        n, k, b, bi, ell, delta, unused = basic(m)
        baseline_p = mm(ell, delta)
        a, bb = 0, m
        g = eye(n)
        g[a][a] = g[bb][bb] = 0
        g[a][bb] = g[bb][a] = 1
        c = mm(b, mm(g, bi))
        u = [(b[i][a] - b[i][bb]) % P for i in range(n)]
        w = [(bi[a][j] - bi[bb][j]) % P for j in range(n)]
        rank_one = [[(int(i == j) - u[i] * w[j]) % P for j in range(n)] for i in range(n)]
        assert c == rank_one and mm(c, c) == eye(n)
        assert sum(bool(v) for v in u) == sum(bool(v) for v in w) == 2 * m
        new_p, new_q = mm(baseline_p, c), mm(g, k)
        assert mm(new_p, mm(b, new_q)) == fourier(n)
        action_stats = []
        for x in (shift(n), diag([pow(root(n), j, P) for j in range(n)])):
            t0 = mm(k, mm(x, k))
            t = mm(g, mm(t0, g))
            amat = mm(b, mm(t, bi))
            assert mm(amat, b) == mm(b, t)
            action_stats.append(degree(amat))
        assert action_stats[1]['row'] > 1
        rows.append({'M': m, 'N': n, 'gauge_nontrivial_vector_supports': [2 * m, 2 * m],
                     'gauge_matrix_degree': degree(c), 'changed_A_degrees': action_stats,
                     'involution_and_exact_factorization': True})
    return rows


def clock_coset_controls():
    rows = []
    for m in (2, 4, 8):
        n, _, b, bi, _, _, _ = basic(m)
        exponents = []
        for bank_index in range(m):
            residue = m - 1 - bank_index
            slope = 2 * bank_index + 1
            for j in range(m):
                exponents.append((residue + m * slope * j) % n)
        assert len(set(exponents)) == n
        t = diag([pow(root(n), e, P) for e in exponents])
        a = mm(b, mm(t, bi))
        assert degree(a)['row'] == degree(a)['column'] == 1
        rows.append({'M': m, 'all_active_blocks_monomial': True, 'raw_coset_permutation_verified': True})
    return rows


def sixteen_point_factors():
    m = 4
    n, k, b, _, ell, delta, qmat = basic(m)
    eh, el = diag([1, 1, -1, -1]), diag([1, -1, 1, -1])
    ph, pl = z(4), z(4)
    for j in range(4):
        ph[j ^ 2][j] = 1
        pl[j ^ 1][j] = 1
    d4, k2 = diag([1, 1, 1, root(4)]), transpose_grid(2)
    a4, c4 = mm(add(eh, ph), d4), mm(add(el, pl), k2)
    assert mm(a4, c4) == fourier(4)
    h1terms = [kron(mm(term, k2), eye(4)) for term in (el, pl)]
    h2terms = [mm(delta, kron(mm(term, d4), eye(4))) for term in (eh, ph)]
    half = pow(2, -1, P)
    h3terms, h4terms = [scale(eye(n), half)] * 2, [scale(k, half)] * 2
    terms = [h1terms, h2terms, h3terms, h4terms]
    for pair in terms:
        for term in pair:
            assert degree(term) == {'nnz': n, 'row': 1, 'column': 1}
    h1, h2, h3, h4 = [add(*pair) for pair in terms]
    assert mm(h2, h1) == qmat
    assert mm(h4, h3) == k
    assert mm(h4, mm(h3, mm(b, mm(h2, h1)))) == fourier(n)
    return {'N': n, 'M': m, 'paired_layers': 4, 'nonsingular_monomial_summands': 8,
            'zero_mask_denominator_guards': [1] * 8,
            'exact_F_16_identity': True,
            'bank_transforms_charged': {'count': 4, 'length': 4},
            'Q_butterfly_layers_charged': 2,
            'extension_to_M_greater_than_4_by_zero_mask_layers': False}


def main():
    result = {'field': P, 'relocated_interface': relocated_controls(),
              'coordinate_swap_gauges': swap_controls(),
              'clock_cosets': clock_coset_controls(),
              'explicit_admissible_control': sixteen_point_factors(),
              'all_exact_assertions_passed': True,
              'scope': 'Only the N=16 control is claimed as an explicit permitted four-layer construction; no growing-size speedup.'}
    Path(__file__).with_name('CHANGED_INTERFACE_CONTROLS.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
