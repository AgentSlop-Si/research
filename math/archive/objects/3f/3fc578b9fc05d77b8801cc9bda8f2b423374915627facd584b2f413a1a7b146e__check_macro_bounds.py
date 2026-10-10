"""Independent exact checks for the boundary-aware scan/broadcast bound.

No imports from submitted packages; Python standard library only. Matrix
materialization here is a verifier, not a proposed fast Fourier algorithm.
"""
from itertools import combinations
import json
from pathlib import Path
import random


def identity(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def mul(a, b, p):
    return [[sum(x*y for x, y in zip(row, col)) % p
             for col in zip(*b)] for row in a]


def rank(a, p):
    a = [list(row) for row in a]
    if not a:
        return 0
    r = 0
    for j in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][j] % p), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        inv = pow(a[r][j] % p, -1, p)
        a[r] = [x*inv % p for x in a[r]]
        for i in range(r+1, len(a)):
            v = a[i][j] % p
            a[i] = [(x-v*y) % p for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def inverse(a, p):
    n = len(a)
    b = [[x % p for x in row]+identity(n)[i] for i, row in enumerate(a)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if b[i][j]), None)
        if pivot is None:
            raise ValueError('singular matrix')
        b[j], b[pivot] = b[pivot], b[j]
        inv = pow(b[j][j], -1, p)
        b[j] = [x*inv % p for x in b[j]]
        for i in range(n):
            if i != j:
                v = b[i][j]
                b[i] = [(x-v*y) % p for x, y in zip(b[i], b[j])]
    return [row[n:] for row in b]


def fourier(n, p, generator):
    assert (p-1) % n == 0
    w = pow(generator, (p-1)//n, p)
    assert len({pow(w, j, p) for j in range(n)}) == n
    return [[pow(w, i*j, p) for j in range(n)] for i in range(n)]


def subtract(a, b, p):
    return [[(x-y) % p for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def random_monomial(n, p, rng):
    order = list(range(n))
    rng.shuffle(order)
    a = [[0]*n for _ in range(n)]
    for i, j in enumerate(order):
        a[i][j] = rng.randrange(1, p)
    return a


def random_bidiagonal(n, p, rng):
    a = [[0]*n for _ in range(n)]
    reverse = rng.randrange(2)
    for i in range(n):
        a[i][i] = rng.randrange(1, p)
        j = i+1 if reverse else i-1
        if 0 <= j < n:
            a[i][j] = rng.randrange(p)
    return a


def random_broadcast(n, p, rng):
    while True:
        u = [rng.randrange(p) for _ in range(n)]
        v = [rng.randrange(p) for _ in range(n)]
        if (1+sum(x*y for x, y in zip(u, v))) % p:
            return [[(int(i == j)+u[i]*v[j]) % p
                     for j in range(n)] for i in range(n)]


def support_sizes(a):
    return [sum(bool(x) for x in row) for row in a]


def lower_budget(n, t):
    if t == 0:
        return n//2
    small = 1 << (t-1)
    denominator = (1 << t)+1
    return max(0, (n-small+denominator-1)//denominator)


def check_words():
    rng = random.Random(238891)
    count = 0
    for n, p, generator in [(4, 97, 5), (8, 97, 5), (16, 97, 5), (8, 17, 3)]:
        f = fourier(n, p, generator)
        for t in range(1, 6):
            for budget in range(4):
                for repeat in range(3):
                    factors = [('scan', random_bidiagonal(n, p, rng)) for _ in range(t)]
                    factors += [('broadcast', random_broadcast(n, p, rng)) for _ in range(budget)]
                    rng.shuffle(factors)
                    all_product = sparse_product = identity(n)
                    for kind, a in factors:
                        shuffle = random_monomial(n, p, rng)
                        all_product = mul(mul(all_product, shuffle, p), a, p)
                        sparse_product = mul(sparse_product, shuffle, p)
                        if kind == 'scan':
                            sparse_product = mul(sparse_product, a, p)
                    supports = support_sizes(sparse_product)
                    assert max(supports) <= 1 << t
                    assert min(supports) <= 1 << (t-1)
                    assert rank(subtract(all_product, sparse_product, p), p) <= budget
                    r = rank(subtract(f, sparse_product, p), p)
                    # Stronger data-dependent inequality, with measured supports.
                    assert n <= min(supports)+r*(max(supports)+1)
                    count += 1
    return count


def check_sparse_rigidity():
    """Exhaust all row-sparse patterns/values at a small non-dyadic length."""
    p, n, g = 7, 3, 3
    f = fourier(n, p, g)
    # Each row has zero or one entry. Full 7-value alphabet gives 19 options.
    options = [[0]*n]
    for j in range(n):
        for value in range(1, p):
            options.append([value if i == j else 0 for i in range(n)])
    count = 0
    for a in options:
        for b in options:
            for c in options:
                s = [a,b,c]
                supports = support_sizes(s)
                r = rank(subtract(f, s, p), p)
                assert n <= min(supports)+r*(max(supports)+1)
                count += 1
    return count


def check_cyclic_witnesses():
    count = 0
    for n, p, g in [(3,7,3), (4,17,3), (8,17,3), (8,97,5)]:
        f = fourier(n,p,g)
        for q in range(1,n+1):
            for start in range(n):
                rows = [(start+i)%n for i in range(q)]
                for cols in combinations(range(n), q):
                    assert rank([[f[i][j] for j in cols] for i in rows],p) == q
                    count += 1
    return count


def check_f8():
    count = 0
    order = [0,2,4,6,1,3,5,7]
    inventories = []
    for p,g in [(17,3), (97,5)]:
        f = fourier(8,p,g)
        for rows in combinations(range(8),3):
            for cols in combinations(range(8),5):
                assert rank([[f[i][j] for j in cols] for i in rows],p) == 3
                count += 1
        cuts = []
        for k in range(1,8):
            up = rank([[f[i][j] for j in order[k:]] for i in order[:k]],p)
            down = rank([[f[i][j] for j in order[:k]] for i in order[k:]],p)
            cuts.append([up,down])
        assert max(max(pair) for pair in cuts) == 3
        inventories.append({'prime':p,'parity_order_cut_ranks':cuts})
    return count, inventories


def check_representation_gap():
    # Every strict off-diagonal cut has rank <=1. Yet this cannot be the strict
    # lower part of one literal scalar weighted scan: H21,H32 nonzero force H31
    # nonzero. It CAN be represented by a state-space scan with independent
    # output weights; the distinction concerns the stated literal primitive.
    a = [[1,0,0],[1,1,0],[0,1,1]]
    for k in [1,2]:
        assert rank([row[:k] for row in a[k:]], 7) == 1
    # Exhaust b0,b1,a1,a2 over F7 to verify the three relevant equations fail.
    solutions = 0
    for b0 in range(7):
        for b1 in range(7):
            for a1 in range(7):
                for a2 in range(7):
                    if a1*b0%7 == 1 and a2*b1%7 == 1 and a2*a1*b0%7 == 0:
                        solutions += 1
    assert solutions == 0
    return {'counterexample':a,'scalar_scan_solutions_over_F7':solutions,
            'parameter_tuples_checked':7**4}


def main():
    f8_count, f8_inventories = check_f8()
    results = {
        'status':'PASS',
        'scope':'Independent finite-field consistency checks; analytic proofs in README.md',
        'random_scan_broadcast_words':check_words(),
        'exhaustive_sparse_F3_rigidity_cases':check_sparse_rigidity(),
        'cyclic_consecutive_vandermonde_minors':check_cyclic_witnesses(),
        'F8_three_by_five_submatrices':f8_count,
        'F8_parity_witnesses':f8_inventories,
        'quasiseparable_rank_vs_literal_scan_gap':check_representation_gap(),
        'N64_broadcast_bounds':[{'t':t,'old':64//((1<<t)+1),'new':lower_budget(64,t)}
                               for t in range(8)],
    }
    Path(__file__).with_name('results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))


if __name__ == '__main__':
    main()
