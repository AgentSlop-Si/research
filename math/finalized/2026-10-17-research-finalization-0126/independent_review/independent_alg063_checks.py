"""Independent finite-field controls. Does not import or execute supplied research code."""
from itertools import product
from random import Random
from pathlib import Path
import json


def direct(x, p, w):
    n = len(x)
    return [sum(x[j] * pow(w, j * k, p) for j in range(n)) % p for k in range(n)]


def batch_inverse(xs, p):
    if not xs:
        return [], 0
    products = [1]
    for x in xs:
        assert x % p
        products.append(products[-1] * x % p)
    tail = pow(products[-1], p - 2, p)
    answer = [0] * len(xs)
    for j in range(len(xs) - 1, -1, -1):
        answer[j] = tail * products[j] % p
        tail = tail * xs[j] % p
    return answer, 1


def recover(x, r, p, w):
    n = len(x)
    m = sum(v != 0 for v in x)
    if m <= 2 * r:
        return direct(x, p, w), 'direct_sparse', 0, None
    candidate = None
    count = 0
    for j in range(n):
        b, a = x[(j - 1) % n], x[j]
        if not b:
            continue
        if count == 0:
            candidate = (a, b)
            count = 1
        elif candidate[0] * b % p == a * candidate[1] % p:
            count += 1
        else:
            count -= 1
    a, b = candidate
    d = [(b * x[j] - a * x[(j - 1) % n]) % p for j in range(n)]
    if sum(v != 0 for v in d) > r:
        return None, 'reject', 0, candidate
    D = direct(d, p, w)
    den = [(b - a * pow(w, k, p)) % p for k in range(n)]
    regular = [k for k in range(n) if den[k]]
    singular = [k for k in range(n) if not den[k]]
    assert len(singular) <= 1
    inverses, inv_count = batch_inverse([den[k] for k in regular], p)
    y = [0] * n
    for k, reciprocal in zip(regular, inverses):
        y[k] = D[k] * reciprocal % p
    for k in singular:
        assert D[k] == 0
        y[k] = sum(x[j] * pow(w, j * k, p) for j in range(n)) % p
    return y, 'resonant' if singular else 'regular', inv_count, candidate


def check(x, r, p, w, counts):
    n = len(x)
    y, mode, invs, pair = recover(x, r, p, w)
    promised = any(sum((x[j] - z * x[(j - 1) % n]) % p != 0
                       for j in range(n)) <= r for z in range(p))
    if promised:
        assert y is not None, (x, r, p, 'false_negative')
    if y is not None:
        assert y == direct(x, p, w), (x, r, p, mode, y)
        assert invs <= 1
        if mode != 'direct_sparse':
            assert promised
    counts['total'] += 1
    counts[mode] = counts.get(mode, 0) + 1
    counts['promised'] += promised


counts = {'total': 0, 'promised': 0}
for p, n, w in [(2, 1, 1), (7, 3, 2), (5, 4, 2)]:
    assert len({pow(w, k, p) for k in range(n)}) == n
    for x in product(range(p), repeat=n):
        for r in range(n + 1):
            check(x, r, p, w, counts)
rng = Random(170126)
for p, n, w in [(13, 6, 4), (17, 8, 2), (97, 16, 8)]:
    assert len({pow(w, k, p) for k in range(n)}) == n
    for unused in range(500):
        x = tuple(rng.randrange(p) for _ in range(n))
        check(x, rng.randrange(n + 1), p, w, counts)
    for z in range(1, p):
        x = tuple(pow(z, j, p) for j in range(n))
        for r in [0, 1, 2]:
            check(x, r, p, w, counts)
result = {'verdict': 'PASS', 'description': 'Independent exact finite-field controls, not a universal proof',
          'counts': counts, 'source_programs_executed': False}
Path(__file__).with_name('ALG063_INDEPENDENT_CHECKS.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
