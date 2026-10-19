"""Exact, fresh C13 integration adapter. Standard library only.

Scope: fixed row/column directions, two prescribed Hamiltonian relative routes,
free endpoint scales, invertible branches, Q or an explicitly supplied prime
field. No direction discovery, singular endpoints, or target invertibility
certification. The accepted iff theorem is a dependency, not a new result here.
"""
from fractions import Fraction
from math import isqrt


class Field:
    def __init__(self, p=None):
        self.p = p
        self.operations = 0
        # Explicit setup cost, outside matrix-size arithmetic accounting.
        if p is not None:
            if not isinstance(p, int) or p < 2:
                raise ValueError("The modulus must be a prime integer")
            if any(p % d == 0 for d in range(2, isqrt(p) + 1)):
                raise ValueError("The modulus must be prime")

    def value(self, a):
        if not isinstance(a, (int, Fraction)):
            raise TypeError("Exact integer or Fraction input required")
        if self.p is None:
            return Fraction(a)
        if isinstance(a, int):
            return a % self.p
        a = Fraction(a)
        return a.numerator * pow(a.denominator, -1, self.p) % self.p

    def add(self, a, b):
        self.operations += 1
        return a + b if self.p is None else (a + b) % self.p

    def sub(self, a, b):
        self.operations += 1
        return a - b if self.p is None else (a - b) % self.p

    def mul(self, a, b):
        self.operations += 1
        return a * b if self.p is None else (a * b) % self.p

    def div(self, a, b):
        self.operations += 1
        if not b:
            raise ZeroDivisionError
        return a / b if self.p is None else a * pow(b, -1, self.p) % self.p

    def candidates(self, component_size):
        # At most m forbidden roots, so the first m+1 distinct field values
        # suffice. Small fields are enumerated in full, without extending them.
        stop = component_size + 1
        if self.p is not None:
            stop = min(stop, self.p)
        return (self.value(t) for t in range(stop))


class CountingOracle:
    """Counts every call; optional trace storage is diagnostic, not required."""
    def __init__(self, get, trace=False):
        self.get, self.calls = get, 0
        self.trace = [] if trace else None

    def __call__(self, i, j):
        self.calls += 1
        if self.trace is not None:
            self.trace.append((i, j))
        return self.get(i, j)


def inverse_permutation(p):
    if sorted(p) != list(range(len(p))):
        raise ValueError("Not a permutation")
    result = [0] * len(p)
    for i, j in enumerate(p):
        result[j] = i
    return result


def cycle_decomposition(p):
    seen, result = set(), []
    for start in range(len(p)):
        if start in seen:
            continue
        c, v = [], start
        while v not in seen:
            seen.add(v)
            c.append(v)
            v = p[v]
        result.append(c)
    return result


def affine_nonzero_solve(nvars, equations, f):
    """Solve A*z[u] + B*z[v] = k; emit component certificate or obstruction.

    The graph field-operation stage is linear in variables plus equations.
    Forbidden-root deduplication uses explicit comparisons, at most quadratic.
    """
    zero, one = f.value(0), f.value(1)
    equations = [(u, v, f.value(a), f.value(b), f.value(k))
                 for u, v, a, b, k in equations]
    if any(not 0 <= u < nvars or not 0 <= v < nvars
           for u, v, _, _, _ in equations):
        raise ValueError("Equation variable outside the supplied range")
    adjacency = [[] for _ in range(nvars)]
    for number, (u, v, a, b, k) in enumerate(equations):
        if a and b:
            adjacency[u].append((v, f.div(-a, b), f.div(k, b), number))
            adjacency[v].append((u, f.div(-b, a), f.div(k, a), number))
        elif not a and not b and k:
            return {"ok": False, "reason": "zero_equation", "equation": number}
    component = [-1] * nvars
    alpha, beta, members = [zero] * nvars, [zero] * nvars, []
    for root in range(nvars):
        if component[root] >= 0:
            continue
        cid = len(members)
        members.append([])
        component[root], alpha[root], beta[root] = cid, one, zero
        todo = [root]
        while todo:
            u = todo.pop()
            members[cid].append(u)
            for v, slope, intercept, _ in adjacency[u]:
                if component[v] < 0:
                    component[v] = cid
                    alpha[v] = f.mul(slope, alpha[u])
                    beta[v] = f.add(f.mul(slope, beta[u]), intercept)
                    todo.append(v)
    fixed, fixed_by = [None] * len(members), [None] * len(members)
    for number, (u, v, a, b, k) in enumerate(equations):
        if not a and not b:
            continue
        cid = component[u if a else v]
        coefficient = f.add(f.mul(a, alpha[u]), f.mul(b, alpha[v]))
        rhs = f.sub(f.sub(k, f.mul(a, beta[u])), f.mul(b, beta[v]))
        if not coefficient:
            if rhs:
                return {"ok": False, "reason": "affine_contradiction",
                        "equation": number, "residual": rhs}
            continue
        forced = f.div(rhs, coefficient)
        if fixed[cid] is not None and fixed[cid] != forced:
            return {"ok": False, "reason": "conflicting_pins",
                    "equations": [fixed_by[cid], number],
                    "forced_values": [fixed[cid], forced]}
        fixed[cid], fixed_by[cid] = forced, number
    roots, comparisons = [], 0
    for cid, vertices in enumerate(members):
        forbidden = []
        for v in vertices:
            bad = f.div(-beta[v], alpha[v])
            found = False
            for old in forbidden:
                comparisons += 1
                if bad == old:
                    found = True
                    break
            if not found:
                forbidden.append(bad)
        if fixed[cid] is not None:
            choice = fixed[cid]
            for bad in forbidden:
                comparisons += 1
                if choice == bad:
                    return {"ok": False, "reason": "forced_zero_scale",
                            "component": cid, "forced_value": choice}
        else:
            choice = None
            for candidate in f.candidates(len(vertices)):
                permitted = True
                for bad in forbidden:
                    comparisons += 1
                    if candidate == bad:
                        permitted = False
                        break
                if permitted:
                    choice = candidate
                    break
            if choice is None:
                return {"ok": False, "reason": "field_exhaustion",
                        "component": cid, "forbidden": forbidden,
                        "field_order": f.p}
        roots.append(choice)
    values = [f.add(f.mul(alpha[v], roots[component[v]]), beta[v])
              for v in range(nvars)]
    # Cheap independent residual pass; never accept a zero scale.
    assert all(values)
    assert all(f.add(f.mul(a, values[u]), f.mul(b, values[v])) == k
               for u, v, a, b, k in equations)
    return {"ok": True, "values": values, "component": component,
            "alpha": alpha, "beta": beta, "parameters": roots,
            "forbidden_comparisons": comparisons}


def complete(data, target_entry, f):
    """Decision/construction adapter, streaming K=UBV without dense K storage.

    data has r0,r1,s0,s1 (row-action permutations), a,b (U row values),
    d,e (V column values). Inputs have O(N) size. All computations are exact.
    The caller supplies a coherent, unchanging exact target-entry oracle.
    """
    n = len(data["a"])
    if n < 2 or any(len(data[k]) != n for k in ("a", "b", "d", "e", "r0", "r1", "s0", "s1")):
        return {"ok": False, "reason": "input_shape"}
    try:
        r0, r1, s0, s1 = [list(data[k]) for k in ("r0", "r1", "s0", "s1")]
        r0i, _, s0i, s1i = map(inverse_permutation, (r0, r1, s0, s1))
    except ValueError:
        return {"ok": False, "reason": "invalid_permutation"}
    a, b, d, e = [[f.value(v) for v in data[k]] for k in ("a", "b", "d", "e")]
    if not all(a) or not all(d):
        return {"ok": False, "reason": "zero_base_coordinate"}
    tau0 = [r0i[r1[i]] for i in range(n)]
    tau1 = [s1[s0i[i]] for i in range(n)]
    cycles0, cycles1 = cycle_decomposition(tau0), cycle_decomposition(tau1)
    if len(cycles0) != 1 or len(cycles1) != 1:
        return {"ok": False, "reason": "non_hamiltonian_prescribed_route"}
    w0 = [f.div(-b[i], a[i]) for i in range(n)]
    w1 = [f.div(-e[tau1[i]], d[tau1[i]]) for i in range(n)]
    products = []
    for branch, (cycles, weights) in enumerate(((cycles0, w0), (cycles1, w1))):
        for cycle in cycles:
            product = f.value(1)
            for i in cycle:
                product = f.mul(product, weights[i])
            if product == f.value(1):
                return {"ok": False, "reason": "singular_denominator", "branch": branch}
            products.append(product)
    urows = [{r0[i]: a[i], r1[i]: b[i]} for i in range(n)]
    vcols = [{s0i[j]: d[j], s1i[j]: e[j]} for j in range(n)]
    urows = [{j: value for j, value in row.items() if value} for row in urows]
    vcols = [{i: value for i, value in col.items() if value} for col in vcols]
    start_ops = f.operations
    equations, support, entries, queries = [], [], 0, 0
    for i in range(n):
        for j in range(n):
            k = f.value(0)
            for r, ur in urows[i].items():
                for s, vs in vcols[j].items():
                    k = f.add(k, f.mul(f.mul(ur, f.value(target_entry(r, s))), vs))
                    queries += 1
            entries += 1
            u, v = urows[i].get(j, 0), vcols[j].get(i, 0)
            if u or v:
                equations.append((i, n + j, v, u, k))
                support.append((i, j))
            elif k:
                return {"ok": False, "reason": "off_support_residual",
                        "position": [i, j], "residual": k,
                        "target_queries": queries, "sandwich_entries": entries}
    sandwich_ops = f.operations - start_ops
    solve_start = f.operations
    solved = affine_nonzero_solve(2 * n, equations, f)
    solve_ops = f.operations - solve_start
    stats = {"target_queries": queries, "sandwich_entries": entries,
             "supported_equations": len(equations), "sandwich_field_operations": sandwich_ops,
             "graph_field_operations": solve_ops, "target_invertibility_checked": False}
    if not solved["ok"]:
        return {**solved, **stats, "stage": "scale_system"}
    x, y = solved["values"][:n], solved["values"][n:]
    return {**stats, "ok": True, "x": x, "y": y,
            "plans": {"tau0": tau0, "tau1": tau1, "w0": w0, "w1": w1,
                      "r0_inverse": r0i, "s0_inverse": s0i,
                      "right_scale0": [f.div(x[i], a[i]) for i in range(n)],
                      "left_scale1": [f.div(y[j], d[j]) for j in range(n)]},
            "graph_certificate": solved, "cycle_products": products}
