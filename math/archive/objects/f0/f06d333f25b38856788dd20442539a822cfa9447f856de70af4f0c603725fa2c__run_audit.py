"""Exact full-basis certificates for the new sparse decimation identities."""
from collections import Counter
import json
from pathlib import Path

from prior_exact_arithmetic import PrimeField, CyclotomicField
from fixed_kernel import Counted, prepare
from operators import prepare_sparse, apply_sparse_c, horner_c
from decimation import (prepare_decimation, apply_family, split_coordinates,
                         merge_coordinates, apply_minus, apply_full_h,
                         apply_polynomial)


def basis(field, n, j):
    return [field.one if i == j else field.zero for i in range(n)]


def check_case(field, n, label):
    q = field.root(n)
    plan = prepare_decimation(field, n, q)
    sparse = prepare_sparse(field, n, q)
    full_basis, split_basis = 0, 0
    h_count = None
    arbitrary = [field.integer(j*j-3*j+2) for j in range(n)]
    for j in range(n):
        x = basis(field, n, j)
        # Independent sparse-C oracle has the original finite corner.
        expected, reference_count = horner_c(field, sparse, plan.kernel, x)
        actual, this_count = apply_full_h(field, plan, x)
        assert actual == expected, (label, n, j, "full H")
        if h_count is not None:
            assert this_count == h_count
        h_count = this_count
        expected_p, _ = horner_c(field, sparse, arbitrary, x)
        actual_p, _ = apply_polynomial(field, plan, arbitrary, x)
        assert actual_p == expected_p, (label, n, j, "general polynomial")
        gauged = [field.mul(a, b) for a, b in zip(plan.sigma, x)]
        cx = apply_sparse_c(field, sparse, gauged)
        normalized_cx = [field.mul(a, b) for a, b in zip(plan.sigma_inverse, cx)]
        assert normalized_cx == apply_family(field, plan.levels[0], x)
        # J^(N/2) is an exact monomial anti-commuter after the gauge.
        shift = x[n//2:] + x[:n//2]
        right = apply_family(field, plan.levels[0], shift)
        cx = apply_family(field, plan.levels[0], x)
        left = cx[n//2:] + cx[:n//2]
        assert left == [field.neg(a) for a in right]
        full_basis += 1
    for index, level in enumerate(plan.levels[:-1]):
        size, h = level.n, level.n//2
        for j in range(size):
            x = basis(field, size, j)
            u, v = split_coordinates(field, plan, index, x)
            assert merge_coordinates(field, plan, index, u, v) == x
            dx = apply_family(field, level, x)
            top, bottom = split_coordinates(field, plan, index, dx)
            assert top == apply_family(field, plan.levels[index+1], v)
            assert bottom == u
            split_basis += 1
        for j in range(h):
            x = basis(field, h, j)
            y = apply_minus(field, level, x)
            assert apply_minus(field, level, y, inverse=True) == x

    negative_controls = {}
    if n >= 8:
        # D_2 has three nonzero entries in every row, while a monomial
        # conjugate of the original (I+J)U form has only two.
        m = n//2
        columns = [apply_family(field, plan.levels[1], basis(field, m, j))
                   for j in range(m)]
        row_supports = [sum(columns[j][i] != field.zero for j in range(m))
                        for i in range(m)]
        assert row_supports == [3]*m
        negative_controls["first_reduced_row_support"] = row_supports
        # Even coefficients are not H_(q^2) with merely a scalar z rescaling.
        half_kernel = prepare(field, m, field.mul(q, q)).kernel
        scale = field.mul(plan.kernel[2], field.inv(half_kernel[1]))
        mismatch = field.sub(plan.kernel[4],
                             field.mul(field.mul(scale, scale), half_kernel[2]))
        assert mismatch != field.zero
        negative_controls["even_coefficients_not_rescaled_H_q_squared"] = True
    expected_nodes = {d: 3**d for d in range(n.bit_length()-1)}
    assert h_count["recursive_nodes_by_depth"] == expected_nodes
    return dict(field=label, n=n, status="PASS", full_basis_vectors=full_basis,
                normalized_split_basis_vectors=split_basis,
                full_H_count=h_count,
                sparse_Horner_comparison=reference_count["field_operations"],
                preparation=plan.preparation,
                negative_controls=negative_controls)


def main():
    rows = []
    for p in (65537, 998244353):
        field = PrimeField(p)
        for n in (2, 4, 8, 16, 32):
            rows.append(check_case(field, n, f"F_{p}"))
    for n in (2, 4, 8):
        rows.append(check_case(CyclotomicField(n), n, f"Q(zeta_{n})"))
    # Counts at larger N are deterministic gate ledgers on one dense input,
    # not numerical timing comparisons or extra full-basis proof claims.
    count_rows = []
    field = PrimeField(65537)
    for n in (64, 128, 256, 512):
        plan = prepare_decimation(field, n, field.root(n))
        _, counts = apply_full_h(field, plan, [field.integer(j+1) for j in range(n)])
        online_total = sum(counts["field_operations"].values())
        prep_total = sum(sum(c.values()) for c in plan.preparation.values())
        count_rows.append(dict(n=n, online_field_operations=online_total,
                               preparation_field_operations=prep_total,
                               sparse_Horner_online_operations=5*n*n-4*n,
                               ordinary_FFT_calls=0))
    result = dict(status="PASS", cases=len(rows),
                  full_basis_vectors=sum(r["full_basis_vectors"] for r in rows),
                  normalized_split_basis_vectors=sum(r["normalized_split_basis_vectors"] for r in rows),
                  all_size_scope="Proof in README; finite exact checks audit the implementation",
                  complexity="Theta(N^(1+log_2(3)/2)) online; O(N log N) preparation; O(N) storage",
                  verdict="Slower than the available O(N log N) complete-operator comparator; not an FFT improvement",
                  rows=rows, larger_gate_ledgers=count_rows)
    destination = Path(__file__).parent / "results" / "decimation_audit.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({k: result[k] for k in ("status", "cases", "full_basis_vectors",
                     "normalized_split_basis_vectors", "larger_gate_ledgers")}, indent=2))


if __name__ == "__main__":
    main()
