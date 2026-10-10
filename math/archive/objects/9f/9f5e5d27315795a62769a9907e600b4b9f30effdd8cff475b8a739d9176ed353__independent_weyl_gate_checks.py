"""Independent bounded exact-field controls. No uploaded program is imported.

This is an audit checker, not a fast Fourier implementation or search program.
"""
import json
import random
from pathlib import Path

P = 20161


def eye(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def mul(a, b):
    n = len(a)
    return [[sum(a[i][k] * b[k][j] for k in range(n)) % P
             for j in range(n)] for i in range(n)]


def inv(a):
    n = len(a)
    c = [a[i][:] + eye(n)[i] for i in range(n)]
    for k in range(n):
        r = next((r for r in range(k, n) if c[r][k]), None)
        if r is None:
            raise ValueError("singular")
        c[k], c[r] = c[r], c[k]
        z = pow(c[k][k], -1, P)
        c[k] = [(z * x) % P for x in c[k]]
        for r in range(n):
            if r != k and c[r][k]:
                z = c[r][k]
                c[r] = [(u - z * v) % P for u, v in zip(c[r], c[k])]
    return [r[n:] for r in c]


def scale(a, c):
    return [[x * c % P for x in r] for r in a]


def root(n):
    for z in range(2, P):
        w = pow(z, (P - 1) // n, P)
        if pow(w, n, P) == 1 and all(pow(w, d, P) != 1
                for d in range(1, n) if n % d == 0):
            return w
    raise AssertionError("no primitive root")


def canonical(n):
    w = root(n)
    d = [[pow(w, i, P) if i == j else 0 for j in range(n)] for i in range(n)]
    z = [[int(i == (j + 1) % n) for j in range(n)] for i in range(n)]
    f = [[pow(w, i * j, P) for j in range(n)] for i in range(n)]
    assert mul(f, z) == mul(d, f)
    assert mul(f, d) == mul(inv(z), f)
    return w, d, z, f


def powers(a):
    out = [eye(len(a))]
    for _ in range(1, len(a)):
        out.append(mul(out[-1], a))
    return out


def signatures(x, y):
    n = len(x)
    xx, yy = powers(x), powers(y)
    return [tuple(sum(xx[a][i][k] * yy[b][k][i] for k in range(n)) % P
                  for a in range(n) for b in range(n)) for i in range(n)]


def short_signatures(x, y):
    words = [x, y, mul(x, x), mul(x, y), mul(y, x), mul(y, y)]
    return [tuple(w[i][i] for w in words) for i in range(len(x))]


def recover_monomial(x, y, u, v):
    n = len(x)
    sx, su = signatures(x, y), signatures(u, v)
    assert len(set(sx)) == n and len(set(su)) == n
    lookup = {s: i for i, s in enumerate(su)}
    if set(sx) != set(su):
        return None, "full-fingerprint mismatch"
    pi = [lookup[s] for s in sx]
    uu = [[u[pi[i]][pi[j]] for j in range(n)] for i in range(n)]
    vv = [[v[pi[i]][pi[j]] for j in range(n)] for i in range(n)]
    edges = [[] for _ in range(n)]
    for a, b in ((x, uu), (y, vv)):
        for i in range(n):
            for j in range(n):
                assert bool(a[i][j]) == bool(b[i][j])
                if a[i][j]:
                    r = b[i][j] * pow(a[i][j], -1, P) % P
                    edges[i].append((j, r))
                    edges[j].append((i, pow(r, -1, P)))
    q = [None] * n
    q[0] = 1
    queue = [0]
    for i in queue:
        for j, r in edges[i]:
            value = q[i] * r % P
            if q[j] is None:
                q[j] = value
                queue.append(j)
            else:
                assert q[j] == value
    assert len(queue) == n
    c = [[q[i] if j == pi[i] else 0 for j in range(n)] for i in range(n)]
    assert mul(x, c) == mul(c, u) and mul(y, c) == mul(c, v)
    return c, "unique monomial up to scalar"


def random_invertible(n, rng):
    while True:
        a = [[rng.randrange(P) for _ in range(n)] for _ in range(n)]
        try:
            inv(a)
            return a
        except ValueError:
            pass


def is_monomial(a):
    n = len(a)
    return (all(sum(x != 0 for x in r) == 1 for r in a)
            and all(sum(a[i][j] != 0 for i in range(n)) == 1 for j in range(n)))


def main():
    rng = random.Random(202610092020)
    positive, negative, collision = [], [], []
    for n in (2, 3, 4, 5, 6, 7, 8, 9, 10, 12):
        w, d, z, f = canonical(n)
        a = random_invertible(n, rng)
        ai = inv(a)
        pi = list(range(n))
        rng.shuffle(pi)
        q = [rng.randrange(1, P) for _ in range(n)]
        c = [[q[i] if j == pi[i] else 0 for j in range(n)] for i in range(n)]
        b = mul(mul(inv(c), ai), f)
        bi = inv(b)
        x, y = mul(mul(ai, d), a), mul(mul(ai, inv(z)), a)
        u, v = mul(mul(b, z), bi), mul(mul(b, d), bi)
        assert mul(x, y) == scale(mul(y, x), pow(w, -1, P))
        found, status = recover_monomial(x, y, u, v)
        assert found == scale(c, pow(q[0], -1, P))
        m = mul(mul(a, found), b)
        calibrated = scale(found, pow(m[0][0], -1, P))
        assert mul(mul(a, calibrated), b) == f
        positive.append({"N": n, "status": status, "all_entries_exact": True,
                         "fingerprint_entries_per_pair": n ** 3})

        bn = random_invertible(n, rng)
        bni = inv(bn)
        un, vn = mul(mul(bn, z), bni), mul(mul(bn, d), bni)
        truth = mul(mul(ai, f), bni)
        cn, reason = recover_monomial(x, y, un, vn)
        assert (cn is not None) == is_monomial(truth)
        assert cn is None
        negative.append({"N": n, "status": reason,
                         "independent_dense_intertwiner_nonmonomial": True})

    for n in (5, 7, 9):
        w, d, z, _ = canonical(n)
        x, y = z, mul(d, z)
        u, v = z, mul(d, mul(z, z))
        assert mul(x, y) == scale(mul(y, x), pow(w, -1, P))
        assert mul(u, v) == scale(mul(v, u), pow(w, -1, P))
        for t in (x, y, u, v):
            assert mul(powers(t)[-1], t) == eye(n)
        assert short_signatures(x, y) == [(0,) * 6] * n
        assert short_signatures(u, v) == [(0,) * 6] * n
        sx, su = signatures(x, y), signatures(u, v)
        assert len(set(sx)) == len(set(su)) == n
        assert set(sx) != set(su)
        extra_x, extra_u = mul(inv(x), y), mul(inv(u), v)
        assert all(extra_x[i][i] for i in range(n))
        assert all(extra_u[i][i] == 0 for i in range(n))
        found, reason = recover_monomial(x, y, u, v)
        assert found is None
        collision.append({"N": n, "all_six_short_fingerprints_zero": True,
                          "full_fingerprints_distinct": True,
                          "inverse_word_rejects": True, "status": reason})

    result = {"field_prime": P, "seed": 202610092020,
              "no_uploaded_code_executed": True,
              "positive_fixed_factor_controls": positive,
              "negative_fixed_factor_controls": negative,
              "short_fingerprint_collision_controls": collision,
              "scope": "Exact finite controls; general theorem has a separate proof."}
    path = Path(__file__).with_name("CHECK_RESULTS.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"positive": len(positive), "negative": len(negative),
                      "collision": len(collision), "passed": True}))


if __name__ == "__main__":
    main()
