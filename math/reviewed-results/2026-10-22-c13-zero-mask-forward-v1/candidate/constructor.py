"""Fresh exact one-sided prescribed-mask constructor; no historical imports.

Runtime: Python standard library. Reference fields: Q and supplied prime F_p.
Certificates are ordinary exact Python objects (Fraction for Q). No endpoint
mask is ever inverted. A malformed/unsupported input is not an infeasible target.
"""
from fractions import Fraction
from math import isqrt


class Field:
    def __init__(self, p=None):
        if p is not None:
            if type(p) is not int or p < 2 or any(p % d == 0 for d in range(2, isqrt(p) + 1)):
                raise ValueError("field setup requires a prime modulus")
        self.p = p
        self.ops = 0
        self.comparisons = 0
        self.z = Fraction(0) if p is None else 0
        self.o = Fraction(1) if p is None else 1

    def elem(self, x):
        if not isinstance(x, (int, Fraction)):
            raise TypeError("exact scalar input must be an integer or Fraction; floats are not coerced")
        if self.p is None:
            return Fraction(x)
        if isinstance(x, Fraction):
            return self.div(x.numerator % self.p, x.denominator % self.p)
        return int(x) % self.p

    def add(self, a, b):
        self.ops += 1
        return a + b if self.p is None else (a + b) % self.p

    def neg(self, a):
        self.ops += 1
        return -a if self.p is None else (-a) % self.p

    def sub(self, a, b):
        return self.add(a, self.neg(b))

    def mul(self, a, b):
        self.ops += 1
        return a * b if self.p is None else (a * b) % self.p

    def div(self, a, b):
        if self.eq(b, self.z):
            raise ZeroDivisionError("only nonzero field divisors are allowed")
        self.ops += 1
        return a / b if self.p is None else a * pow(b, -1, self.p) % self.p

    def eq(self, a, b):
        self.comparisons += 1
        return a == b

    def candidates(self, count):
        # At most count distinct elements; F_p enumeration never leaves F_p.
        stop = count if self.p is None else min(self.p, count)
        return (self.elem(i) for i in range(stop))


def inverse_perm(p):
    n = len(p)
    q = [None] * n
    for i, j in enumerate(p):
        if type(j) is not int or not 0 <= j < n or q[j] is not None:
            raise ValueError("not a permutation")
        q[j] = i
    return q


def cycles(route):
    inverse_perm(route)
    seen, out = [False] * len(route), []
    for start in range(len(route)):
        if seen[start]:
            continue
        cyc, v = [], start
        while not seen[v]:
            seen[v] = True
            cyc.append(v)
            v = route[v]
        out.append(cyc)
    return out


def affine_mask_solve(field, variable_count, equations, zero_indices):
    """Solve A*z[u]+B*z[v]=k, zeros exactly at zero_indices.

    Every variable outside zero_indices must be nonzero. Returned certificate
    gives tree equations, affine forms, root constraints and excluded roots.
    The caller already holds equations, so certificate indices refer to them.
    """
    f, m = field, variable_count
    zeros = set(zero_indices)
    if not zeros <= set(range(m)):
        raise ValueError("zero-mask index out of range")
    eqs, adjacency = [], [[] for _ in range(m)]
    for index, raw in enumerate(equations):
        u, A, v, B, k = raw
        if not (0 <= u < m and 0 <= v < m):
            raise ValueError("equation index out of range")
        A, B, k = map(f.elem, (A, B, k))
        if u == v:
            A, B = f.add(A, B), f.z
        eqs.append((u, A, v, B, k))
        if not f.eq(A, f.z) and not f.eq(B, f.z):
            adjacency[u].append((v, f.div(f.neg(A), B), f.div(k, B), index))
            adjacency[v].append((u, f.div(f.neg(B), A), f.div(k, A), index))

    alpha, beta, comp = [None] * m, [None] * m, [None] * m
    certificates = []
    for root in range(m):
        if comp[root] is not None:
            continue
        cid = len(certificates)
        alpha[root], beta[root], comp[root] = f.o, f.z, cid
        vertices, tree, queue = [], [], [root]
        for u in queue:
            vertices.append(u)
            for v, a, b, eid in adjacency[u]:
                if comp[v] is None:
                    alpha[v] = f.mul(a, alpha[u])
                    beta[v] = f.add(f.mul(a, beta[u]), b)
                    comp[v] = cid
                    tree.append((eid, u, v))
                    queue.append(v)
        certificates.append({"root": root, "vertices": vertices, "tree": tree,
                             "constraints": [], "forbidden": []})

    def failure(kind, evidence):
        return {"feasible": False, "kind": kind, "evidence": evidence,
                "alpha": alpha, "beta": beta, "component": comp,
                "components": certificates}

    # Constraints are triples (C, R, source), meaning C*t=R in one component.
    for eid, (u, A, v, B, k) in enumerate(eqs):
        nzA, nzB = not f.eq(A, f.z), not f.eq(B, f.z)
        if not nzA and not nzB:
            if not f.eq(k, f.z):
                return failure("linear-contradiction", {"equation": eid, "zero_equals": k})
            continue
        owner = u if nzA else v
        c = f.add(f.mul(A, alpha[u]), f.mul(B, alpha[v]))
        r = f.sub(k, f.add(f.mul(A, beta[u]), f.mul(B, beta[v])))
        # If both coefficients are nonzero, this edge joined the two variables.
        assert not (nzA and nzB) or comp[u] == comp[v]
        certificates[comp[owner]]["constraints"].append((c, r, ("equation", eid)))
    for v in sorted(zeros):
        certificates[comp[v]]["constraints"].append((alpha[v], f.neg(beta[v]), ("zero-pin", v)))

    values = [None] * m
    for cid, cert in enumerate(certificates):
        forced, forcing = None, None
        for c, r, source in cert["constraints"]:
            if f.eq(c, f.z):
                if not f.eq(r, f.z):
                    return failure("linear-contradiction", {"component": cid, "constraint": (c, r, source)})
            else:
                t = f.div(r, c)
                if forced is not None and not f.eq(t, forced):
                    return failure("conflicting-root-pins", {"component": cid, "first": forcing,
                                                              "second": (c, r, source)})
                forced, forcing = t, (c, r, source)
        for v in cert["vertices"]:
            if v not in zeros:
                cert["forbidden"].append((f.div(f.neg(beta[v]), alpha[v]), v))
        if forced is not None:
            for root_value, v in cert["forbidden"]:
                if f.eq(forced, root_value):
                    return failure("forced-nonzero-violation", {"component": cid, "forcing": forcing,
                                                               "parameter": forced, "variable": v})
            t = forced
            cert["forced_by"] = forcing
        else:
            roots = [t for t, _ in cert["forbidden"]]
            t = None
            for trial in f.candidates(len(roots) + 1):
                if not any(f.eq(trial, bad) for bad in roots):
                    t = trial
                    break
            if t is None:
                assert f.p is not None
                # The generated field is exactly {0,...,p-1}; all have a witness.
                cover = [(a, next(v for bad, v in cert["forbidden"] if f.eq(a, bad)))
                         for a in f.candidates(f.p)]
                return failure("field-exhaustion", {"component": cid, "field_order": f.p, "cover": cover})
        cert["parameter"] = t
        for v in cert["vertices"]:
            values[v] = f.add(f.mul(alpha[v], t), beta[v])
    return {"feasible": True, "values": values, "alpha": alpha, "beta": beta,
            "component": comp, "components": certificates}


def prepare_skeleton(field, r0, r1, s0, s1, a, b, d, e, cycle_type0=None, cycle_type1=None):
    """The source's separated base/edge convention, N>=2, exact fixed routes.

    A cycle type is the list of permitted cycle lengths for this supplied route.
    Default: one Hamiltonian N-cycle. The exact route is never replaced.
    """
    f, n = field, len(r0)
    if n < 2 or any(len(z) != n for z in (r1, s0, s1, a, b, d, e)):
        raise ValueError("requires consistent N>=2 skeleton data")
    ir0, ir1, is0, is1 = map(inverse_perm, (r0, r1, s0, s1))
    if any(r0[i] == r1[i] or is0[i] == is1[i] for i in range(n)):
        raise ValueError("source base/edge supports must be distinct")
    a, b, d, e = ([f.elem(v) for v in z] for z in (a, b, d, e))
    if any(f.eq(v, f.z) for v in a + d):
        raise ValueError("zero base coordinate")
    rho = [ir0[r1[i]] for i in range(n)]
    sigma = [s1[is0[i]] for i in range(n)]
    c0, c1 = cycles(rho), cycles(sigma)
    expected0 = [n] if cycle_type0 is None else list(cycle_type0)
    expected1 = [n] if cycle_type1 is None else list(cycle_type1)
    if sorted(map(len, c0)) != sorted(expected0) or sorted(map(len, c1)) != sorted(expected1):
        raise ValueError("fixed structural cycle type is not legal")
    w0 = [f.neg(f.div(b[i], a[i])) for i in range(n)]
    w1 = [f.neg(f.div(e[sigma[i]], d[sigma[i]])) for i in range(n)]
    denominators = []
    for route_cycles, w in ((c0, w0), (c1, w1)):
        ds = []
        for cyc in route_cycles:
            product = f.o
            for i in cyc:
                product = f.mul(product, w[i])
            delta = f.sub(f.o, product)
            if f.eq(delta, f.z):
                raise ValueError("singular prescribed cycle denominator")
            ds.append(delta)
        denominators.append(ds)
    return {"n": n, "r0": list(r0), "r1": list(r1), "s0": list(s0), "s1": list(s1),
            "ir0": ir0, "ir1": ir1, "is0": is0, "is1": is1,
            "a": a, "b": b, "d": d, "e": e,
            "rho": rho, "sigma": sigma, "w0": w0, "w1": w1,
            "cycles0": c0, "cycles1": c1, "denominators": denominators}


def construct(field, skeleton, target_entry, zero_x=(), zero_y=()):
    """Complete scan followed by the exact affine-mask feasibility solver."""
    f, s = field, skeleton
    n = s["n"]
    zx, zy = set(zero_x), set(zero_y)
    if not zx <= set(range(n)) or not zy <= set(range(n)):
        raise ValueError("zero-mask index out of range")
    equations, queries, normalization_ops, start_ops = [], 0, 0, f.ops
    for i in range(n):
        for j in range(n):
            k = f.z
            for row, u in ((s["r0"][i], s["a"][i]), (s["r1"][i], s["b"][i])):
                for col, v in ((s["is0"][j], s["d"][j]), (s["is1"][j], s["e"][j])):
                    # Count every callback, including terms with zero edge weights.
                    before_normalization = f.ops
                    bij = f.elem(target_entry(row, col))
                    normalization_ops += f.ops - before_normalization
                    queries += 1
                    k = f.add(k, f.mul(f.mul(u, bij), v))
            Uij = s["a"][i] if j == s["r0"][i] else (s["b"][i] if j == s["r1"][i] else f.z)
            Vij = s["d"][j] if i == s["is0"][j] else (s["e"][j] if i == s["is1"][j] else f.z)
            if f.eq(Uij, f.z) and f.eq(Vij, f.z):
                if not f.eq(k, f.z):
                    return {"feasible": False, "kind": "off-support", "position": (i, j), "residual": k,
                            "target_calls": queries, "sandwich_field_ops": f.ops - start_ops - normalization_ops,
                            "target_normalization_field_ops": normalization_ops}
            else:
                equations.append((i, Vij, n + j, Uij, k))
    scan_ops = f.ops - start_ops - normalization_ops
    ans = affine_mask_solve(f, 2 * n, equations, zx | {n + j for j in zy})
    ans.update({"target_calls": queries, "sandwich_field_ops": scan_ops,
                "target_normalization_field_ops": normalization_ops, "equations": equations})
    if ans["feasible"]:
        x, y = ans["values"][:n], ans["values"][n:]
        ans["x"], ans["y"] = x, y
        ans["plans"] = {
            "T0": {"left_inverse_permutation": s["r0"], "route": s["rho"], "weights": s["w0"],
                   "right_diagonal": [f.div(x[i], s["a"][i]) for i in range(n)]},
            "T1": {"left_diagonal": [f.div(y[i], s["d"][i]) for i in range(n)],
                   "route": s["sigma"], "weights": s["w1"], "right_inverse_permutation": s["s0"]}}
    return ans


def green_apply(field, route, weights, rhs):
    """Solve h_i-w_i*h_route(i)=rhs_i in O(N), with no edge inverses.

    The cycle denominator is the only division, even when edge weights vanish.
    """
    f, n = field, len(route)
    h = [f.z] * n
    for cyc in cycles(route):
        total, product = f.z, f.o
        for i in cyc:
            total = f.add(total, f.mul(product, rhs[i]))
            product = f.mul(product, weights[i])
        h[cyc[0]] = f.div(total, f.sub(f.o, product))
        for j in range(len(cyc) - 1, 0, -1):
            i = cyc[j]
            h[i] = f.add(rhs[i], f.mul(weights[i], h[route[i]]))
    return h


def apply_plans(field, plans, vector):
    f, n = field, len(vector)
    p0, p1 = plans["T0"], plans["T1"]
    if len(p0["route"]) != n or len(p1["route"]) != n:
        raise ValueError("vector length does not match prepared plans")
    vector = [f.elem(v) for v in vector]
    z = [f.mul(p0["right_diagonal"][i], vector[i]) for i in range(n)]
    z = green_apply(f, p0["route"], p0["weights"], z)
    t0 = [z[i] for i in inverse_perm(p0["left_inverse_permutation"])]
    z = [vector[i] for i in inverse_perm(p1["right_inverse_permutation"])]
    z = green_apply(f, p1["route"], p1["weights"], z)
    t1 = [f.mul(p1["left_diagonal"][i], z[i]) for i in range(n)]
    return [f.add(a, b) for a, b in zip(t0, t1)]
