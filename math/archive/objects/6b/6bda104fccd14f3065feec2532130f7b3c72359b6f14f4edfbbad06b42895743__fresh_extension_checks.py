"""Fresh extension checks using only the auditor's own newly authored helpers."""
from fresh_exact_checks import inverse, directions, rank, multiply
from itertools import product, combinations
from random import Random
from pathlib import Path
import json
import time


def column_options(n, p):
    options = []
    for weight in (1, 2):
        for support in combinations(range(n), weight):
            for values in product(range(1, p), repeat=weight):
                col = [0] * n
                for i, x in zip(support, values):
                    col[i] = x
                options.append(tuple(col))
    return options


def graph_check(q, qi, selected, p):
    n = len(q)
    cols = list(zip(*q))
    support = [[i for i, x in enumerate(col) if x] for col in cols]
    keep = [j for j in range(n) if j not in selected]
    adjacent = [set() for _ in range(n)]
    for j in keep:
        assert 1 <= len(support[j]) <= 2
        if len(support[j]) == 2:
            a, b = support[j]
            adjacent[a].add(b); adjacent[b].add(a)
    seen, trees, cycles = set(), 0, 0
    a = [qi[i] for i in selected]
    for v in range(n):
        if v in seen:
            continue
        component, todo = set(), [v]
        while todo:
            w = todo.pop()
            if w not in component:
                component.add(w); todo.extend(adjacent[w] - component)
        seen.update(component)
        verts = sorted(component)
        edges = [j for j in keep if support[j][0] in component]
        local = [[q[i][j] for j in edges] for i in verts]
        assert rank(local, p) == len(edges)
        degree = len(verts) - len(edges)
        assert degree in (0, 1)
        assert rank([[row[j] for j in verts] for row in a], p) == degree
        trees += degree; cycles += 1 - degree
    assert trees == len(selected)
    assert len(directions(a, p)[0]) == len(selected)
    return cycles


def exhaustive(p, n):
    totals = dict(p=p, n=n, matrices=0, invertible=0, restrictions=0,
                  row_degree_above_two=0)
    subsets = [s for k in range(1, n + 1) for s in combinations(range(n), k)]
    for cols in product(column_options(n, p), repeat=n):
        totals['matrices'] += 1
        q = [list(row) for row in zip(*cols)]
        qi = inverse(q, p)
        if qi is None:
            continue
        totals['invertible'] += 1
        totals['row_degree_above_two'] += any(sum(x != 0 for x in row) > 2 for row in q)
        assert multiply(q, qi, p) == [[int(i == j) for j in range(n)] for i in range(n)]
        for rows in subsets:
            assert len(directions([qi[i] for i in rows], p)[0]) == len(rows)
            totals['restrictions'] += 1
    print(json.dumps(totals), flush=True)
    return totals


def random_checks():
    rng = Random(4392026)
    totals = dict(invertible=0, deletions=0, surviving_unicyclic=0,
                  surviving_unicyclic_after_bridge_deletion=0)
    # Rooted trees plus one loop give deliberately high-degree, nonsingular
    # column-two patterns. A column permutation decouples inverse row indices
    # from graph vertices and thus checks the deletion orientation.
    for p in (2, 3, 5, 7, 17):
        for n in range(2, 26):
            for repetition in range(30):
                q = [[0] * n for _ in range(n)]
                q[0][0] = rng.randrange(1, p)
                for v in range(1, n):
                    parent = rng.randrange(v)
                    q[parent][v] = rng.randrange(1, p)
                    q[v][v] = rng.randrange(1, p)
                permutation = list(range(n)); rng.shuffle(permutation)
                q = [[row[j] for j in permutation] for row in q]
                qi = inverse(q, p)
                assert qi is not None
                totals['invertible'] += 1
                loop_column = permutation.index(0)
                # Deleting a tree edge while preserving the loop always leaves
                # a surviving unicyclic component with fewer original vertices.
                edge_column = rng.choice([j for j in range(n) if j != loop_column])
                cycles = graph_check(q, qi, (edge_column,), p)
                assert cycles == 1
                totals['surviving_unicyclic_after_bridge_deletion'] += 1
                for _ in range(3):
                    rows = tuple(sorted(rng.sample(range(n), rng.randrange(1, n + 1))))
                    totals['surviving_unicyclic'] += graph_check(q, qi, rows, p)
                    totals['deletions'] += 1
    print(json.dumps(totals), flush=True)
    return totals


if __name__ == '__main__':
    started = time.time()
    result = dict(status='PASS', exhaustive=[exhaustive(p, n)
                  for p, top in ((2, 4), (3, 3)) for n in range(1, top + 1)],
                  random=random_checks())
    result['seconds'] = round(time.time() - started, 3)
    Path(__file__).with_name('extension_results.json').write_text(
        json.dumps(result, indent=2) + '\n')
    print('ALL EXTENSION CHECKS PASSED', flush=True)
