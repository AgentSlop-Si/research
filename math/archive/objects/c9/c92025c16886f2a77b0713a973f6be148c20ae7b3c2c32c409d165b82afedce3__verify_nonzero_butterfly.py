#!/usr/bin/env python3
"""Standalone exact nonzero-mask butterfly controls."""
import json
from pathlib import Path

P = 65537
ALPHA = pow(3, (P - 1) // 4, P)
assert ALPHA not in (0, 1, P - 1)


def eye(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def mm(a, b):
    n = len(a)
    return [[sum(a[i][k] * b[k][j] for k in range(n)) % P for j in range(n)] for i in range(n)]


def masked_cycle(n, order, destinations, weight):
    assert sorted(order) == list(range(n))
    w = [[0] * n for _ in range(n)]
    masks = [0] * n
    for i, src in enumerate(order):
        dst = order[(i + 1) % n]
        if dst in destinations:
            masks[dst] = weight
            w[dst][src] = weight
    product = 1
    for value in masks:
        product = product * value % P
    assert product == 0
    u = [[(int(i == j) - w[i][j]) % P for j in range(n)] for i in range(n)]
    ui = [[(int(i == j) + w[i][j]) % P for j in range(n)] for i in range(n)]
    assert mm(w, w) == [[0] * n for _ in range(n)]
    assert mm(u, ui) == mm(ui, u) == eye(n)
    return ui, sum(bool(v) for v in masks)


def check(n, kind):
    pairs = [(i, i + 1) for i in range(0, n, 2)] if kind == 'adjacent' else [(i, i + n // 2) for i in range(n // 2)]
    top, bottom = {a for a, _ in pairs}, {b for _, b in pairs}
    upper_order = [v for a, b in pairs for v in (b, a)]
    lower_order = [v for a, b in pairs for v in (a, b)]
    upper, unz = masked_cycle(n, upper_order, top, pow(ALPHA, -1, P))
    beta = (-1 - ALPHA) % P
    lower, lnz = masked_cycle(n, lower_order, bottom, pow(beta, -1, P))
    endpoint = [(1 - ALPHA) % P if i in top else beta for i in range(n)]
    assert all(endpoint) and ALPHA
    h = [[(ALPHA * upper[i][j] + endpoint[i] * lower[i][j]) % P for j in range(n)] for i in range(n)]
    expected = [[0] * n for _ in range(n)]
    for a, b in pairs:
        expected[a][a] = expected[a][b] = expected[b][a] = 1
        expected[b][b] = P - 1
    assert h == expected
    return {'N': n, 'pairing': kind, 'nonzero_edges_per_green': [unz, lnz],
            'hamiltonian_cycles': 2, 'denominator_guards': [1, 1],
            'exact_butterfly_identity': True}


def main():
    result = {'field': P, 'alpha': ALPHA,
              'cases': [check(n, kind) for n in (4, 16, 64) for kind in ('adjacent', 'halves')],
              'all_exact_assertions_passed': True,
              'scope': 'Known butterfly layers realized with nonzero matching masks; no growing-size Fourier compression.'}
    Path(__file__).with_name('NONZERO_BUTTERFLY_CONTROLS.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
