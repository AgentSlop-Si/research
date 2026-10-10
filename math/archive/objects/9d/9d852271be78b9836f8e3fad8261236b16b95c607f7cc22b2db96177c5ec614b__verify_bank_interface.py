#!/usr/bin/env python3
"""Independent exact controls. Imports no source packet or uploaded program."""
import itertools
import json
from pathlib import Path

P = 65537


def zero(n, m=None):
    return [[0] * (n if m is None else m) for _ in range(n)]


def ident(n):
    a = zero(n)
    for i in range(n):
        a[i][i] = 1
    return a


def mul(a, b, p=P):
    c = zero(len(a), len(b[0]))
    brows = [[(j, v) for j, v in enumerate(row) if v] for row in b]
    for i, row in enumerate(a):
        for k, v in enumerate(row):
            if v:
                for j, w in brows[k]:
                    c[i][j] += v * w
        c[i] = [v % p for v in c[i]]
    return c


def add(a, b, sign=1, p=P):
    return [[(v + sign * w) % p for v, w in zip(r, s)] for r, s in zip(a, b)]


def scale(a, c, p=P):
    return [[v * c % p for v in row] for row in a]


def transpose(a):
    return [list(r) for r in zip(*a)]


def inv(a, p=P):
    n = len(a)
    z = [row[:] + ident(n)[i] for i, row in enumerate(a)]
    for j in range(n):
        pivot = next(i for i in range(j, n) if z[i][j])
        z[j], z[pivot] = z[pivot], z[j]
        z[j] = [v * pow(z[j][j], -1, p) % p for v in z[j]]
        for i in range(n):
            if i != j and z[i][j]:
                c = z[i][j]
                z[i] = [(v - c * w) % p for v, w in zip(z[i], z[j])]
    return [row[n:] for row in z]


def rank(a, p=P):
    z = [row[:] for row in a]
    r = 0
    for j in range(len(z[0])):
        pivot = next((i for i in range(r, len(z)) if z[i][j]), None)
        if pivot is None:
            continue
        z[r], z[pivot] = z[pivot], z[r]
        v = pow(z[r][j], -1, p)
        z[r] = [x * v % p for x in z[r]]
        for i in range(r + 1, len(z)):
            c = z[i][j]
            if c:
                z[i] = [(x - c * y) % p for x, y in zip(z[i], z[r])]
        r += 1
    return r


def root(n, p=P, primitive=3):
    w = pow(primitive, (p - 1) // n, p)
    assert pow(w, n, p) == 1
    assert n == 1 or pow(w, n // 2, p) != 1
    return w


def fourier(n, w, p=P):
    return [[pow(w, i * j, p) for j in range(n)] for i in range(n)]


def weyl(n, eta, a, b, p=P):
    z = zero(n)
    for j in range(n):
        i = (j + b) % n
        z[i][j] = pow(eta, a * i, p)
    return z


def degree(a):
    return {
        'nnz': sum(bool(x) for row in a for x in row),
        'row': max(sum(bool(x) for x in row) for row in a),
        'column': max(sum(bool(x) for x in row) for row in zip(*a)),
    }


def put(a, b, i, j):
    for r, row in enumerate(b):
        for s, v in enumerate(row):
            a[i + r][j + s] = v


def block_bank(m, q, active, inverse=False):
    f = fourier(m, root(m))
    if inverse:
        f = scale(fourier(m, pow(root(m), -1, P)), pow(m, -1, P))
    b = zero(m * q)
    for r in range(q):
        put(b, f if r in active else ident(m), r * m, r * m)
    return b


def controls_weyl():
    count = 0
    for m in (2, 4, 8, 16, 32):
        eta = root(m)
        f = fourier(m, eta)
        fi = scale(fourier(m, pow(eta, -1, P)), pow(m, -1, P))
        pairs = list(itertools.product(range(m), repeat=2)) if m <= 16 else [(0, 0), (1, 1), (3, 7), (31, 17)]
        for a, b in pairs:
            lhs = mul(mul(f, weyl(m, eta, a, b)), fi)
            rhs = scale(weyl(m, eta, b, -a), pow(eta, a * b, P))
            assert lhs == rhs
            count += 1
    return count


def controls_uncertainty():
    summary = []
    for p, generator, m, alphabet, exhaustive in ((5, 2, 4, range(5), True), (17, 3, 2, range(17), True), (17, 3, 8, (0, 1), False)):
        f = fourier(m, root(m, p, generator), p)
        count = 0
        minimum = m * m
        for x in itertools.product(alphabet, repeat=m):
            s = sum(v != 0 for v in x)
            if not s:
                continue
            fx = [sum(a * b for a, b in zip(row, x)) % p for row in f]
            t = sum(v != 0 for v in fx)
            c = [[x[(i - j) % m] for j in range(m)] for i in range(m)]
            assert rank(c, p) == t
            assert s * t >= m
            minimum = min(minimum, s * t)
            count += 1
        summary.append({'field': p, 'm': m, 'nonzero_vectors': count, 'exhaustive_over_field': exhaustive, 'minimum_support_product': minimum})
    return summary


def active_sets(q):
    if q <= 4:
        return [{j for j in range(q) if (mask >> j) & 1} for mask in range(1 << q)]
    choices = [set(), set(range(q)), {0}, set(range(q // 2)), set(range(0, q, 2)), set(range(1, q))]
    return choices


def controls_ct():
    summary = []
    count = 0
    for m, q in ((2, 2), (2, 4), (4, 2), (4, 4), (4, 8), (8, 4), (8, 8), (16, 4)):
        n = m * q
        omega = root(n)
        eta = pow(omega, q, P)
        omega_q = pow(omega, m, P)
        f = fourier(n, omega)
        fm = fourier(m, eta)
        s = weyl(n, omega, 0, 1)
        d = weyl(n, omega, 1, 0)
        si = weyl(n, omega, 0, -1)
        qmat = zero(n)
        for r in range(q):
            for t in range(m):
                qmat[r * m + t][r + q * t] = 1
        qinv = transpose(qmat)
        t1, t2 = mul(mul(qmat, s), qinv), mul(mul(qmat, d), qinv)
        for active in active_sets(q):
            bank = block_bank(m, q, active)
            bi = block_bank(m, q, active, inverse=True)
            pmat = zero(n)
            for u in range(q):
                for t in range(m):
                    for r in range(q):
                        coefficient = pow(omega_q, u * r, P) * pow(omega, r * t, P) % P
                        for h in range(m):
                            entry = int(t == h) if r in active else fm[t][h]
                            pmat[u * m + t][r * m + h] = coefficient * entry % P
            assert mul(mul(pmat, bank), qmat) == f
            a1, a2 = mul(mul(bank, t1), bi), mul(mul(bank, t2), bi)
            assert mul(a1, bank) == mul(bank, t1)
            assert mul(a2, bank) == mul(bank, t2)
            assert mul(pmat, a1) == mul(d, pmat)
            assert mul(pmat, a2) == mul(si, pmat)
            assert mul(t1, qmat) == mul(qmat, s)
            assert mul(t2, qmat) == mul(qmat, d)
            k = sum((r in active) != (((r + 1) % q) in active) for r in range(q))
            deg = degree(a1)
            assert deg['nnz'] == n + k * m * (m - 1)
            assert deg['row'] == deg['column'] == (m if k else 1)
            assert degree(a2)['nnz'] == degree(t1)['nnz'] == degree(t2)['nnz'] == n
            count += 1
            if q == m and active == set(range(q // 2)):
                summary.append({'N': n, 'm': m, 'q': q, 'active': sorted(active), 'boundary_edges': k, 'A_shift': deg, 'other_three_nnz_each': n, 'charged_transform_count': {'size_m_in_bank': len(active), 'size_m_hidden_in_P': q - len(active), 'size_q_in_P': m}})
    return {'cases': count, 'square_contiguous_controls': summary}


def controls_directionality():
    out = []
    for m in (2, 4, 8, 16):
        f = fourier(m, root(m))
        t = zero(m)
        for i in range(m):
            t[i][0] = 1
        a = mul(f, t)
        assert degree(a)['row'] == degree(t)['row'] == 1
        assert degree(t)['column'] == m
        assert degree(a)['nnz'] == 1
        ar, tr = transpose(t), transpose(a)
        assert mul(ar, f) == tr
        assert degree(ar)['column'] == degree(tr)['column'] == 1
        out.append({'m': m, 'left_mixed_row_degrees': [degree(t)['row'], degree(a)['row']], 'left_input_column_degree': degree(t)['column'], 'right_mixed_column_degrees': [degree(ar)['column'], degree(tr)['column']]})
    return out


def mono(n, offset, seed):
    a = zero(n)
    for j in range(n):
        a[(j + offset) % n][j] = 1 + ((seed + j) % 13)
    return a


def controls_state():
    out = []
    for n in (4, 8):
        m, q = 2, n // 2
        bank = block_bank(m, q, {0})
        size = 14 * n
        ks = ident(size)
        layers = []
        realization = {0: ident(n)}
        specs = ((0, 1, 2, 3), (3, 4, 5, 6), (7, 8, 9, 10), (10, 11, 12, 13))
        for ell, (inp, left, right, output) in enumerate(specs):
            hs = zero(n)
            for r, wire in enumerate((left, right)):
                u = ident(n)
                weights = [2 + ((j + ell + r) % 5) for j in range(n)]
                product = 1
                for j, weight in enumerate(weights):
                    u[(j + 1) % n][j] = -weight % P
                    product = product * weight % P
                assert product != 1
                l = mono(n, ell + r + 1, ell + 2 * r)
                rr = mono(n, 2 * ell + r, 3 * ell + r)
                put(ks, u, wire * n, wire * n)
                put(ks, scale(rr, -1), wire * n, inp * n)
                put(ks, scale(l, -1), output * n, wire * n)
                g = mul(inv(u), rr)
                hs = add(hs, mul(l, g))
                realization[wire] = mul(g, realization[inp])
            layers.append(hs)
            realization[output] = mul(hs, realization[inp])
            if output == 6:
                realization[7] = mul(bank, realization[6])
        assert degree(ks)['row'] <= 3 and degree(ks)['column'] <= 3
        k = [row[:] for row in ks]
        put(k, scale(bank, -1), 7 * n, 6 * n)
        v = []
        for wire in range(14):
            v.extend(realization[wire])
        b0 = zero(size, n)
        put(b0, ident(n), 0, 0)
        assert mul(k, v) == b0
        target = mul(mul(mul(mul(layers[3], layers[2]), bank), layers[1]), layers[0])
        assert realization[13] == target
        # Arbitrary degree-two witnesses check the exact residual decomposition.
        sr = add(ident(size), mono(size, 5, 2))
        rr = add(scale(ident(size), 3), mono(size, 11, 4))
        residual = add(mul(k, sr), mul(rr, k), -1)
        sparse_residual = add(mul(ks, sr), mul(rr, ks), -1)
        bank_edge = zero(size)
        put(bank_edge, bank, 7 * n, 6 * n)
        rhs = add(add(sparse_residual, mul(bank_edge, sr), -1), mul(rr, bank_edge))
        assert residual == rhs
        center = [[sparse_residual[7 * n + i][6 * n + j] for j in range(n)] for i in range(n)]
        expected_center = [[(sr[7 * n + i][6 * n + j] - rr[7 * n + i][6 * n + j]) % P for j in range(n)] for i in range(n)]
        assert center == expected_center
        out.append({'N': n, 'state_dimension': size, 'K_s_degree': degree(ks), 'transfer_and_residual_identities': True})
    return out


def main():
    result = {
        'field': P,
        'root_generator': 3,
        'weyl_conjugation_cases': controls_weyl(),
        'support_product': controls_uncertainty(),
        'cooley_tukey': controls_ct(),
        'directional_degree_examples': controls_directionality(),
        'state_lift': controls_state(),
        'scope': 'Exact algebra controls only; no paired-Green Fourier factorization or asymptotic speedup claimed.',
    }
    path = Path(__file__).with_name('BANK_INTERFACE_CONTROLS.json')
    path.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
