"""Fresh audit controls. No candidate or inherited program is imported or run."""
from fractions import Fraction
from itertools import permutations
from random import Random
import json
from pathlib import Path

OUT = Path(__file__).parent

def rank(a, p=None):
    if not a or not a[0]:
        return 0
    b = [[Fraction(x) if p is None else x % p for x in row] for row in a]
    m, n, k = len(b), len(b[0]), 0
    for j in range(n):
        pivot = next((i for i in range(k, m) if b[i][j]), None)
        if pivot is None:
            continue
        b[k], b[pivot] = b[pivot], b[k]
        inv = 1 / b[k][j] if p is None else pow(b[k][j], -1, p)
        b[k] = [x * inv if p is None else (x * inv) % p for x in b[k]]
        for i in range(k + 1, m):
            if b[i][j]:
                v = b[i][j]
                b[i] = [x - v*y if p is None else (x-v*y) % p for x, y in zip(b[i], b[k])]
        k += 1
        if k == m:
            break
    return k

def sub(a, rows, cols):
    return [[a[i][j] for j in cols] for i in rows]

def family(h):
    n = 2**(h+1)-1
    q = [[int(i == j) for j in range(n)] for i in range(n)]
    b = [[0]*n for _ in range(n)]
    for v in range(n):
        if v:
            q[(v-1)//2][v] = -1
        u = v
        while True:
            b[u][v] = 1
            if not u:
                break
            u = (u-1)//2
    g = [[0]*(2*n) for _ in range(2*n)]
    for i in range(n):
        for j in range(n):
            if q[i][j]:
                g[i][n+j] = g[n+j][i] = 1
    return q, b, g

def frontier_width(adjacency):
    n = len(adjacency)
    masks = [sum((1 << j) for j, x in enumerate(row) if x) for row in adjacency]
    allv = (1 << n)-1
    dp = [0]*(1 << n)
    for s in range(1, 1 << n):
        outside = allv ^ s
        boundary = sum(bool(s & (1 << i)) and bool(masks[i] & outside) for i in range(n))
        dp[s] = max(boundary, min(dp[s ^ (1 << i)] for i in range(n) if s & (1 << i)))
    return dp[-1]

def optimized_sr(q):
    n = len(q)
    masks_by_size = [[s for s in range(1 << n) if s.bit_count() == k] for k in range(n+1)]
    indices = {s: [i for i in range(n) if s & (1 << i)] for s in range(1 << n)}
    full = (1 << n)-1
    dp = {(0, 0): 0}
    for k in range(1, n+1):
        for r in masks_by_size[k]:
            for c in masks_by_size[k]:
                width = max(rank(sub(q, indices[r], indices[full ^ c]), 2),
                            rank(sub(q, indices[full ^ r], indices[c]), 2))
                prev = min(dp[(r ^ (1 << i), c ^ (1 << j))] for i in indices[r] for j in indices[c])
                dp[r, c] = max(width, prev)
    return {"sr": dp[full, full], "paired_prefix_states": len(dp)}

rng = Random(202610100548)
result = {"method": "New independent exact rational/finite-field eliminations; all small order pairs or seeded samples; exact subset dynamic programming", "families": []}
for h in range(5):
    q, b, g = family(h)
    n = len(q)
    assert all(sum(q[i][k]*b[k][j] for k in range(n)) == int(i == j) for i in range(n) for j in range(n))
    assert all(sum(b[i][k]*q[k][j] for k in range(n)) == int(i == j) for i in range(n) for j in range(n))
    if n <= 3:
        pp = list(permutations(range(n)))
        pairs = [(r, c) for r in pp for c in pp]
    else:
        pairs = []
        for _ in range(32):
            r, c = list(range(n)), list(range(n))
            rng.shuffle(r)
            rng.shuffle(c)
            pairs.append((r,c))
    max_observed_s = 0
    for r, c in pairs:
        s = 0
        for k in range(n+1):
            cuts = [(r[:k], c[k:], c[:k], r[k:]), (r[k:], c[:k], c[k:], r[:k])]
            for rr, cc, ii, jj in cuts:
                qblock, bblock = sub(q,rr,cc), sub(b,ii,jj)
                rq = rank(qblock)
                assert rq == rank(qblock,2) == rank(qblock,3)
                assert rq == rank(bblock) == rank(bblock,2) == rank(bblock,3)
                s = max(s,rq)
        layout = [v for rc in zip(r,[n+j for j in c]) for v in rc]
        for k in range(1,2*n):
            cutrank = rank(sub(g,layout[:k],layout[k:]),2)
            assert cutrank <= 2*s + k%2
        max_observed_s = max(max_observed_s,s)
    entry = {"h":h,"N":n,"order_pairs_checked":len(pairs),"maximum_sampled_width":max_observed_s,
             "identity_and_rank_checks_passed":True}
    if n <= 7:
        entry["exact_independent_order_optimization"] = optimized_sr(q)
        entry["exact_lift_pathwidth"] = frontier_width(g)
    if n <= 15:
        t = [[0]*n for _ in range(n)]
        for v in range(1,n):
            t[v][(v-1)//2]=t[(v-1)//2][v]=1
        entry["exact_tree_pathwidth"] = frontier_width(t)
        assert entry["exact_tree_pathwidth"] == (h+1)//2
    result["families"].append(entry)
result["all_checks_passed"] = True
(OUT / "INDEPENDENT_CONTROLS.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
