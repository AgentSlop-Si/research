"""Independent finite-field checks; authored from scratch for this audit.

Only Python standard-library modules are imported. No supplied program is read,
imported, compiled, or parsed. All arithmetic is exact modulo a small prime.
"""
from itertools import permutations, product, combinations
from random import Random
import json
import time
from pathlib import Path

OUT = Path(__file__).parent


def rank(a, p):
    if not a:
        return 0
    a = [list(row) for row in a]
    m, n = len(a), len(a[0])
    r = 0
    for j in range(n):
        pivot = next((i for i in range(r, m) if a[i][j] % p), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        scale = pow(a[r][j] % p, -1, p)
        a[r] = [(x * scale) % p for x in a[r]]
        for i in range(r + 1, m):
            f = a[i][j] % p
            if f:
                a[i] = [(x - f * y) % p for x, y in zip(a[i], a[r])]
        r += 1
        if r == m:
            break
    return r


def inverse(a, p):
    n = len(a)
    b = [[x % p for x in a[i]] + [int(i == j) for j in range(n)]
         for i in range(n)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if b[i][j]), None)
        if pivot is None:
            return None
        b[j], b[pivot] = b[pivot], b[j]
        z = pow(b[j][j], -1, p)
        b[j] = [(x * z) % p for x in b[j]]
        for i in range(n):
            f = b[i][j]
            if i != j and f:
                b[i] = [(x - f * y) % p for x, y in zip(b[i], b[j])]
    return [row[n:] for row in b]


def multiply(a, b, p):
    return [[sum(x * y for x, y in zip(row, col)) % p
             for col in zip(*b)] for row in a]


def directions(a, p):
    ans = set()
    zero = False
    for col in zip(*a):
        first = next((x for x in col if x), None)
        if first is None:
            zero = True
        else:
            z = pow(first, -1, p)
            ans.add(tuple((x * z) % p for x in col))
    return ans, zero


def make_q(perm, d, e, p):
    # Convention P e_j = e_perm[j], hence (E P)_{perm[j],j}=e_perm[j].
    n = len(perm)
    q = [[0] * n for _ in range(n)]
    for j in range(n):
        q[j][j] = d[j] % p
        q[perm[j]][j] = (q[perm[j]][j] + e[perm[j]]) % p
    return q


def check_graph(q, inv, perm, rows, p):
    n = len(q)
    keep = [j for j in range(n) if j not in rows]
    adjacency = [set() for _ in range(n)]
    for j in keep:
        adjacency[j].add(perm[j])
        adjacency[perm[j]].add(j)
    seen, path_count, cycle_count = set(), 0, 0
    a = [inv[i] for i in rows]
    assert not any(x for row in multiply(a, [[q[i][j] for j in keep]
                                             for i in range(n)], p) for x in row)
    for seed in range(n):
        if seed in seen:
            continue
        component, todo = set(), [seed]
        while todo:
            v = todo.pop()
            if v in component:
                continue
            component.add(v)
            todo.extend(adjacency[v] - component)
        seen.update(component)
        verts = sorted(component)
        # Do not collapse parallel edges, and count a loop as one constraint.
        edges = [j for j in keep if j in component]
        b = [[q[i][j] for j in edges] for i in verts]
        assert rank(b, p) == len(edges)
        if len(edges) == len(verts):
            cycle_count += 1
            assert all(a[i][j] == 0 for i in range(len(rows)) for j in verts)
        else:
            assert len(edges) == len(verts) - 1
            path_count += 1
            assert rank([[a[i][j] for j in verts] for i in range(len(rows))], p) == 1
    assert path_count == len(rows)
    return cycle_count


def exhaustive(p, n):
    t0 = time.time()
    counts = dict(p=p, n=n, pattern_matrices=0, invertible=0,
                  row_restrictions=0, with_zero_column=0)
    subsets = [s for k in range(1, n + 1) for s in combinations(range(n), k)]
    # Every D+E P is generated: at fixed points the two coefficients add to
    # one arbitrary field value, so enumerate distinct actual matrix entries.
    for perm in permutations(range(n)):
        slots = sorted({(j, j) for j in range(n)} |
                       {(perm[j], j) for j in range(n)})
        for coeff in product(range(p), repeat=len(slots)):
            q = [[0] * n for _ in range(n)]
            for (i, j), value in zip(slots, coeff):
                q[i][j] = value
            counts['pattern_matrices'] += 1
            qi = inverse(q, p)
            if qi is None:
                continue
            counts['invertible'] += 1
            assert multiply(q, qi, p) == [[int(i == j) for j in range(n)] for i in range(n)]
            for rows in subsets:
                ds, zero = directions([qi[i] for i in rows], p)
                # Stronger exact statement before endpoint scaling: k directions.
                assert len(ds) == len(rows), (p, perm, q, rows, ds)
                counts['row_restrictions'] += 1
                counts['with_zero_column'] += zero
    counts['seconds'] = round(time.time() - t0, 3)
    print(json.dumps(counts), flush=True)
    return counts


def random_cases():
    rng = Random(43901010)
    counts = dict(attempts=0, invertible=0, routed_restrictions=0,
                  graph_deletions=0, retained_cycles=0, all_zero_branches=0,
                  sum_refinements=0)
    for p in (2, 3, 5, 7, 17):
        for n in range(1, 15):
            for repetition in range(100):
                perm = list(range(n)); rng.shuffle(perm)
                q = make_q(perm, [rng.randrange(p) for _ in range(n)],
                           [rng.randrange(p) for _ in range(n)], p)
                counts['attempts'] += 1
                qi = inverse(q, p)
                if qi is None:
                    continue
                counts['invertible'] += 1
                for _ in range(4):
                    k = rng.randrange(1, n + 1)
                    rows = sorted(rng.sample(range(n), k))
                    counts['retained_cycles'] += check_graph(q, qi, perm, rows, p)
                    counts['graph_deletions'] += 1
                    lp = list(range(n)); rng.shuffle(lp)
                    rp = list(range(n)); rng.shuffle(rp)
                    ls = [rng.randrange(p) for _ in range(n)]
                    rs = [rng.randrange(p) for _ in range(n)]
                    routed = [[ls[i] * qi[lp[i]][rp[j]] * rs[j] % p
                               for j in range(n)] for i in rows]
                    ds, zero = directions(routed, p)
                    assert len(ds) <= k
                    counts['all_zero_branches'] += not ds
                    # Absorb zero columns into any one line. If no nonzero
                    # column exists, all columns get one dummy class.
                    ds = list(ds)
                    labels = []
                    for col in zip(*routed):
                        pivot = next((x for x in col if x), None)
                        labels.append(0 if pivot is None else ds.index(tuple(
                            x * pow(pivot, -1, p) % p for x in col)))
                    assert len(set(labels)) <= k
                    for label in set(labels):
                        assert rank([[row[j] for j in range(n) if labels[j] == label]
                                     for row in routed], p) <= 1
                    counts['routed_restrictions'] += 1
    # Independent branch permutations and endpoint permutations, with nonzero
    # D guaranteeing enough invertible samples at large n.
    p = 101
    for r in (1, 2, 3, 4):
        k, n = r + 1, 40
        for _ in range(100):
            branches, signatures = [], [[] for _ in range(n)]
            for branch in range(r):
                while True:
                    perm = list(range(n)); rng.shuffle(perm)
                    q = make_q(perm, [rng.randrange(1, p) for _ in range(n)],
                               [rng.randrange(p) for _ in range(n)], p)
                    qi = inverse(q, p)
                    if qi is not None:
                        break
                lp = list(range(n)); rng.shuffle(lp)
                rp = list(range(n)); rng.shuffle(rp)
                ls = [rng.randrange(p) for _ in range(k)]
                rs = [rng.randrange(p) for _ in range(n)]
                a = [[ls[i] * qi[lp[i]][rp[j]] * rs[j] % p for j in range(n)]
                     for i in range(k)]
                ds = list(directions(a, p)[0])
                assert len(ds) <= k
                for j, col in enumerate(zip(*a)):
                    pivot = next((x for x in col if x), None)
                    label = 0 if pivot is None else ds.index(tuple(
                        x * pow(pivot, -1, p) % p for x in col))
                    signatures[j].append(label)
                branches.append(a)
            signatures = [tuple(s) for s in signatures]
            assert len(set(signatures)) <= k ** r
            total = [[sum(a[i][j] for a in branches) % p for j in range(n)]
                     for i in range(k)]
            for signature in set(signatures):
                columns = [j for j in range(n) if signatures[j] == signature]
                assert rank([[row[j] for j in columns] for row in total], p) <= r
            counts['sum_refinements'] += 1
    print(json.dumps(counts), flush=True)
    return counts


def fourier_tests():
    count = 0
    cases = []
    # Includes composite N and positive characteristic, with all square
    # minors having consecutive (possibly wrapping) rows and distinct columns.
    for p, n in ((7, 3), (5, 4), (7, 6), (17, 8), (13, 12)):
        omega = next(x for x in range(1, p)
                     if pow(x, n, p) == 1 and
                     all(pow(x, d, p) != 1 for d in range(1, n)))
        local = 0
        for k in range(1, min(n, 5) + 1):
            for start in range(n):
                for cols in combinations(range(n), k):
                    a = [[pow(omega, ((start + i) % n) * j, p) for j in cols]
                         for i in range(k)]
                    assert rank(a, p) == k
                    count += 1; local += 1
        cases.append(dict(p=p, n=n, omega=omega, minors=local))
    result = dict(minors=count, cases=cases)
    print(json.dumps(result), flush=True)
    return result


if __name__ == '__main__':
    began = time.time()
    result = dict(status='PASS', independent=True,
                  exhaustive=[exhaustive(p, n) for p, top in ((2, 5), (3, 4))
                              for n in range(1, top + 1)],
                  random=random_cases(), fourier=fourier_tests())
    result['total_seconds'] = round(time.time() - began, 3)
    (OUT / 'exact_results.json').write_text(json.dumps(result, indent=2) + '\n')
    print('ALL CHECKS PASSED', flush=True)
