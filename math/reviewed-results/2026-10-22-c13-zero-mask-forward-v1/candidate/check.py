"""Fresh exact controls. Imports only the fresh constructor and standard library.

Dense inversion/multiplication and exhaustive assignment checks are independently
implemented here; no supplied/historical program is read, imported, or executed.
"""
import itertools
import json
import random
from fractions import Fraction
from pathlib import Path
from constructor import Field, affine_mask_solve, prepare_skeleton, construct, apply_plans


class Dense:
    def __init__(self, p):
        self.p = p

    def c(self, x):
        return Fraction(x) if self.p is None else x % self.p

    def add(self, a, b):
        return a + b if self.p is None else (a + b) % self.p

    def sub(self, a, b):
        return a - b if self.p is None else (a - b) % self.p

    def mul(self, a, b):
        return a * b if self.p is None else a * b % self.p

    def div(self, a, b):
        assert b != 0
        return a / b if self.p is None else a * pow(b, -1, self.p) % self.p

    def eye(self, n):
        return [[self.c(i == j) for j in range(n)] for i in range(n)]

    def matmul(self, A, B):
        return [[self.c(sum(self.mul(a, b) for a, b in zip(row, col)))
                 for col in zip(*B)] for row in A]

    def inverse(self, A):
        n = len(A)
        aug = [row[:] + eye for row, eye in zip(A, self.eye(n))]
        for j in range(n):
            pivot = next((i for i in range(j, n) if aug[i][j]), None)
            if pivot is None:
                raise ValueError("singular matrix")
            aug[pivot], aug[j] = aug[j], aug[pivot]
            d = aug[j][j]
            aug[j] = [self.div(v, d) for v in aug[j]]
            for i in range(n):
                if i != j:
                    c = aug[i][j]
                    aug[i] = [self.sub(a, self.mul(c, b)) for a, b in zip(aug[i], aug[j])]
        return [row[n:] for row in aug]

    def rank(self, A):
        A = [row[:] for row in A]
        r = 0
        for j in range(len(A[0])):
            pivot = next((i for i in range(r, len(A)) if A[i][j]), None)
            if pivot is None:
                continue
            A[pivot], A[r] = A[r], A[pivot]
            d = A[r][j]
            A[r] = [self.div(a, d) for a in A[r]]
            for i in range(r + 1, len(A)):
                c = A[i][j]
                A[i] = [self.sub(a, self.mul(c, b)) for a, b in zip(A[i], A[r])]
            r += 1
        return r


def dense_skeleton(dense, s):
    n = s["n"]
    U, V = ([[dense.c(0) for _ in range(n)] for _ in range(n)] for _ in range(2))
    for i in range(n):
        U[i][s["r0"][i]], U[i][s["r1"][i]] = s["a"][i], s["b"][i]
        V[s["is0"][i]][i], V[s["is1"][i]][i] = s["d"][i], s["e"][i]
    return U, V


def make_target(d, U, V, x, y):
    ui, vi = d.inverse(U), d.inverse(V)
    n = len(x)
    T0 = [[d.mul(ui[i][j], x[j]) for j in range(n)] for i in range(n)]
    T1 = [[d.mul(y[i], vi[i][j]) for j in range(n)] for i in range(n)]
    return [[d.add(T0[i][j], T1[i][j]) for j in range(n)] for i in range(n)], T0, T1


def direct_check_affine(p, m, eqs, zeros):
    values = [(0,) if i in zeros else tuple(range(1, p)) for i in range(m)]
    for assignment in itertools.product(*values):
        if all((A * assignment[u] + B * assignment[v] - k) % p == 0 for u, A, v, B, k in eqs):
            return assignment
    return None


def verify_affine_certificate(p, m, equations, zeros, result):
    """Check derivations, positive witness, or the exact negative witness.

    This verifier evaluates the emitted tree equations and root constraints; it
    does not rerun the constructor's spanning-forest algorithm.
    """
    d = Dense(p)
    a, b, comp = result["alpha"], result["beta"], result["component"]
    eqs = []
    for u, A, v, B, k in equations:
        A, B, k = map(d.c, (A, B, k))
        if u == v:
            A, B = d.add(A, B), d.c(0)
        eqs.append((u, A, v, B, k))
    for cid, c in enumerate(result["components"]):
        root = c["root"]
        assert a[root] == 1 and b[root] == 0
        seen = {root}
        for eid, u, v in c["tree"]:
            assert u in seen and v not in seen
            i, A, j, B, k = eqs[eid]
            assert {u, v} == {i, j} and A and B
            assert d.add(d.mul(A, a[i]), d.mul(B, a[j])) == 0
            assert d.add(d.mul(A, b[i]), d.mul(B, b[j])) == k
            seen.add(v)
        assert seen == set(c["vertices"])
        assert all(a[v] != 0 and comp[v] == cid for v in seen)
        for C, R, source in c["constraints"]:
            kind, ix = source
            if kind == "zero-pin":
                assert ix in zeros and C == a[ix] and R == d.sub(0, b[ix])
            else:
                i, A, j, B, k = eqs[ix]
                assert C == d.add(d.mul(A, a[i]), d.mul(B, a[j]))
                assert R == d.sub(k, d.add(d.mul(A, b[i]), d.mul(B, b[j])))
        for t, v in c["forbidden"]:
            assert v not in zeros and t == d.div(d.sub(0, b[v]), a[v])
    if result["feasible"]:
        z = result["values"]
        assert all((z[v] == 0) == (v in zeros) for v in range(m))
        assert all(d.add(d.mul(A, z[u]), d.mul(B, z[v])) == k for u, A, v, B, k in eqs)
        return
    kind, e = result["kind"], result["evidence"]
    if kind == "linear-contradiction":
        if "equation" in e:
            _, A, _, B, k = eqs[e["equation"]]
            assert A == B == 0 and k != 0
        else:
            C, R, source = e["constraint"]
            assert (C, R, source) in result["components"][e["component"]]["constraints"]
            assert C == 0 and R != 0
    elif kind == "conflicting-root-pins":
        c = result["components"][e["component"]]
        C, R, _ = e["first"]
        D, S, _ = e["second"]
        assert e["first"] in c["constraints"] and e["second"] in c["constraints"]
        assert C and D and d.div(R, C) != d.div(S, D)
    elif kind == "forced-nonzero-violation":
        c = result["components"][e["component"]]
        C, R, _ = e["forcing"]
        v, t = e["variable"], e["parameter"]
        assert e["forcing"] in c["constraints"] and C and t == d.div(R, C)
        assert v not in zeros and d.add(d.mul(a[v], t), b[v]) == 0
    elif kind == "field-exhaustion":
        c = result["components"][e["component"]]
        assert p is not None and e["field_order"] == p
        assert all(C == R == 0 for C, R, _ in c["constraints"])
        assert sorted(t for t, _ in e["cover"]) == list(range(p))
        for t, v in e["cover"]:
            assert v in c["vertices"] and v not in zeros
            assert d.add(d.mul(a[v], t), b[v]) == 0
    else:
        raise AssertionError(kind)


def random_cycle(n, rng, lengths):
    order = list(range(n))
    rng.shuffle(order)
    out, offset = [None] * n, 0
    for length in lengths:
        cyc = order[offset:offset + length]
        for i, j in zip(cyc, cyc[1:] + cyc[:1]):
            out[i] = j
        offset += length
    assert offset == n
    return out


def sample_skeleton(p, n, rng, lengths=None):
    f = Field(p)
    lengths = [n] if lengths is None else lengths
    r0, s0 = list(range(n)), list(range(n))
    rng.shuffle(r0)
    rng.shuffle(s0)
    rho, sigma = random_cycle(n, rng, lengths), random_cycle(n, rng, lengths)
    r1 = [r0[rho[i]] for i in range(n)]
    s1 = [sigma[s0[i]] for i in range(n)]
    nz = lambda: rng.choice([-3, -2, -1, 1, 2, 3]) if p is None else rng.randrange(1, p)
    elem = lambda: rng.randrange(-3, 4) if p is None else rng.randrange(p)
    while True:
        a, d = [nz() for _ in range(n)], [nz() for _ in range(n)]
        b, e = [elem() for _ in range(n)], [elem() for _ in range(n)]
        try:
            return f, prepare_skeleton(f, r0, r1, s0, s1, a, b, d, e, lengths, lengths)
        except ValueError as exc:
            assert "denominator" in str(exc)


def expect_bad_guard(fn, word):
    try:
        fn()
    except ValueError as exc:
        assert word in str(exc), str(exc)
    else:
        raise AssertionError("guard did not reject")


def main():
    rng = random.Random(20261022013)
    counts = {"exhaustive_affine_mask_systems": 0, "dense_positive_targets": 0,
              "gauge_controls": 0, "off_support_rejections": 0,
              "basis_output_vectors": 0, "dense_target_entries": 0,
              "negative_certificate_kinds": [], "explicit_guards": 0}
    kinds = set()
    for p in (2, 3, 5):
        for _ in range(24):
            m = 4
            equations = [(rng.randrange(m), rng.randrange(p), rng.randrange(m), rng.randrange(p), rng.randrange(p))
                         for _ in range(rng.randrange(0, 7))]
            for bits in range(1 << m):
                zeros = {i for i in range(m) if bits >> i & 1}
                ans = affine_mask_solve(Field(p), m, equations, zeros)
                witness = direct_check_affine(p, m, equations, zeros)
                assert ans["feasible"] == (witness is not None)
                verify_affine_certificate(p, m, equations, zeros, ans)
                if not ans["feasible"]:
                    kinds.add(ans["kind"])
                counts["exhaustive_affine_mask_systems"] += 1

    for p in (None, 2, 3, 5, 7):
        for n in range(2, 11):
            for trial in range(5):
                lengths = [n] if n < 4 or trial < 3 else [2, n - 2]
                f, s = sample_skeleton(p, n, rng, lengths)
                d = Dense(p)
                U, V = dense_skeleton(d, s)
                # Include all-zero, one-zero-branch, mixed, and all-nonzero masks.
                if trial == 0:
                    zx, zy = set(range(n)), set(range(n))
                elif trial == 1:
                    zx, zy = set(range(n)), {i for i in range(n) if i % 2}
                elif trial == 2:
                    zx, zy = {i for i in range(n) if i % 2 == 0}, {i for i in range(n) if i % 3 == 0}
                elif trial == 3:
                    zx, zy = set(), set()
                else:
                    zx, zy = {n - 1}, {0}
                nz = lambda: d.c(rng.choice([1, 2, 3])) if p is None else rng.randrange(1, p)
                x = [d.c(0) if i in zx else nz() for i in range(n)]
                y = [d.c(0) if i in zy else nz() for i in range(n)]
                B, T0, T1 = make_target(d, U, V, x, y)
                assert d.rank(T0) == n - len(zx) and d.rank(T1) == n - len(zy)
                ans = construct(f, s, lambda i, j: B[i][j], zx, zy)
                assert ans["feasible"] and ans["target_calls"] == 4 * n * n
                assert ans["sandwich_field_ops"] == 12 * n * n
                verify_affine_certificate(p, 2*n, ans["equations"], zx | {n+j for j in zy}, ans)
                for j in range(n):
                    unit = [d.c(i == j) for i in range(n)]
                    out = apply_plans(f, ans["plans"], unit)
                    assert out == [B[i][j] for i in range(n)]
                    counts["basis_output_vectors"] += 1
                counts["dense_positive_targets"] += 1
                counts["dense_target_entries"] += n*n
                # Projective rescaling keeps fixed routes and actual mask locations.
                lam, mu = [nz() for _ in range(n)], [nz() for _ in range(n)]
                sg = prepare_skeleton(f, s["r0"], s["r1"], s["s0"], s["s1"],
                        [d.mul(lam[i], s["a"][i]) for i in range(n)],
                        [d.mul(lam[i], s["b"][i]) for i in range(n)],
                        [d.mul(mu[i], s["d"][i]) for i in range(n)],
                        [d.mul(mu[i], s["e"][i]) for i in range(n)], lengths, lengths)
                ag = construct(f, sg, lambda i, j: B[i][j], zx, zy)
                assert ag["feasible"]
                for j in range(n):
                    assert apply_plans(f, ag["plans"], [d.c(i == j) for i in range(n)]) == [B[i][j] for i in range(n)]
                # A particular original witness scales as lam*x, mu*y.
                Ug, Vg = dense_skeleton(d, sg)
                Bg, _, _ = make_target(d, Ug, Vg, [d.mul(lam[i], x[i]) for i in range(n)],
                                      [d.mul(mu[i], y[i]) for i in range(n)])
                assert Bg == B
                counts["gauge_controls"] += 1
                forbidden = next(((i,j) for i in range(n) for j in range(n) if U[i][j] == V[i][j] == 0), None)
                if forbidden is not None:
                    K = d.matmul(d.matmul(U, B), V)
                    i, j = forbidden
                    K[i][j] = d.add(K[i][j], d.c(1))
                    bad = d.matmul(d.matmul(d.inverse(U), K), d.inverse(V))
                    rejected = construct(f, s, lambda i,j: bad[i][j], zx, zy)
                    assert not rejected["feasible"] and rejected["kind"] == "off-support"
                    assert rejected["position"] == forbidden and rejected["residual"] == 1
                    counts["off_support_rejections"] += 1

    n, f = 5, Field(2)
    ident, shift = list(range(n)), [(i+1) % n for i in range(n)]
    s = prepare_skeleton(f, ident, shift, ident, shift, [1]*n, [0]*n, [1]*n, [0]*n)
    I = Dense(2).eye(n)
    no = construct(f, s, lambda i,j:I[i][j])
    assert not no["feasible"] and no["kind"] == "field-exhaustion"
    verify_affine_certificate(2, 2*n, no["equations"], set(), no)
    yes = construct(f, s, lambda i,j:I[i][j], range(n), ())
    assert yes["feasible"] and yes["x"] == [0]*n and yes["y"] == [1]*n
    badmask = construct(f, s, lambda i,j:I[i][j], [0], [0])
    assert not badmask["feasible"] and badmask["kind"] == "conflicting-root-pins"
    verify_affine_certificate(2, 2*n, badmask["equations"], {0,n}, badmask)
    counts["explicit_guards"] += 3
    fq = Field()
    args = (ident, shift, ident, shift)
    expect_bad_guard(lambda:prepare_skeleton(fq, *args, [0]+[1]*(n-1), [2]*n, [1]*n, [3]*n), "base")
    expect_bad_guard(lambda:prepare_skeleton(fq, *args, [1]*n, [-1]*n, [1]*n, [0]*n), "denominator")
    expect_bad_guard(lambda:prepare_skeleton(fq, *args, [1]*n, [0]*n, [1]*n, [0]*n, [2,3], [n]), "cycle type")
    expect_bad_guard(lambda:prepare_skeleton(fq, ident, ident, ident, shift, [1]*n, [0]*n, [1]*n, [0]*n), "distinct")
    expect_bad_guard(lambda:Field(4), "prime")
    counts["explicit_guards"] += 5
    for fp in (Field(), Field(3)):
        try:
            fp.elem(0.5)
        except TypeError:
            pass
        else:
            raise AssertionError("lossy scalar coercion was accepted")
    f3 = Field(3)
    s3 = prepare_skeleton(f3, ident, shift, ident, shift, [1]*n, [0]*n, [1]*n, [0]*n)
    normalized = construct(f3, s3, lambda i,j:Fraction(i == j, 2), range(n), ())
    assert normalized["feasible"] and normalized["y"] == [2]*n
    assert normalized["sandwich_field_ops"] == 12*n*n
    assert normalized["target_normalization_field_ops"] == 4*n*n
    assert apply_plans(f3, normalized["plans"], [Fraction(1,2)]*n) == [1]*n
    counts["explicit_guards"] += 3
    # Zero base can coexist with invertibility, so that guard is genuinely extra.
    U = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        U[i][i], U[i][shift[i]] = Fraction(i != 0), Fraction(2)
    Dense(None).inverse(U)
    # Explicit prescribed-zero branch may sum to a singular target; no target guard is implied.
    z = construct(f, s, lambda i,j:0, range(n), range(n))
    assert z["feasible"] and all(v == 0 for v in z["values"])
    counts["explicit_guards"] += 2
    fscope = Field()
    scopesk = prepare_skeleton(fscope, [0,1,2], [1,2,0], [0,1,2], [1,2,0],
                               [1]*3, [-2]*3, [1]*3, [0]*3)
    two_sided = [[Fraction(-2,7) if (i,j)==(0,1) else Fraction(0) for j in range(3)] for i in range(3)]
    ds = Dense(None)
    us, vs = dense_skeleton(ds, scopesk)
    usi = ds.inverse(us)
    assert usi[0][1] == Fraction(-2,7) and usi[2][1] == Fraction(-4,7)
    for bits in range(64):
        sx = [i for i in range(3) if bits >> i & 1]
        sy = [i for i in range(3) if bits >> (3+i) & 1]
        rejected = construct(fscope, scopesk, lambda i,j:two_sided[i][j], sx, sy)
        assert not rejected["feasible"] and rejected["kind"] == "off-support"
    counts["explicit_guards"] += 1
    counts["negative_certificate_kinds"] = sorted(kinds)
    assert kinds == {"linear-contradiction", "conflicting-root-pins", "forced-nonzero-violation", "field-exhaustion"}
    report = {"status": "PASS", "seed": 20261022013, "counts": counts,
              "historical_program_execution": False,
              "proof_not_inferred_from_controls": True,
              "reference_fields": ["Q", "F2", "F3", "F5", "F7"]}
    print(json.dumps(report, indent=2))
    Path(__file__).with_name("CHECK_RESULTS.json").write_text(json.dumps(report, indent=2)+"\n")


if __name__ == "__main__":
    main()
