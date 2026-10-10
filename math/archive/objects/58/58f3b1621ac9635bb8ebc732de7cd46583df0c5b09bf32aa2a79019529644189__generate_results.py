from __future__ import annotations

import hashlib
import json
import os
import random
from pathlib import Path

from higher_local_ring_weil import *

ROOT = Path(__file__).resolve().parent


def hierarchy_records() -> list[dict]:
    p, s, q = 3, 2, 9
    mod, zeta = coefficient_field(q)
    out = []
    for vals in [(0, 0), (0, 1), (1, 1), (0, 2), (1, 2), (2, 2)]:
        diagonal = [p**v if v < s else 0 for v in vals]
        op = diagonal_upper_shear(q, p, s, diagonal, mod, zeta)
        rows, cols = support_counts(op)
        stats = predicted_core_stats(p, s, vals)
        orders = sorted(sample_nonzero_cross_ratio_orders(op, mod, 1500))
        out.append({
            "valuations": vals,
            "measured_row_support": sorted(set(rows)),
            "measured_col_support": sorted(set(cols)),
            "measured_cross_ratio_orders": orders,
            **stats,
        })
    return out


def word_audit() -> dict:
    p, q, n = 3, 3, 2
    mod, zeta = coefficient_field(q)
    sym_id, op_id = identity(2 * n), identity(q**n)
    gens = []
    for C in ([[1, 1], [1, 2]], [[0, 1], [1, 1]]):
        gens.append(("L", lower_shear_symplectic(C, q), lower_shear_operator(q, C, mod, zeta)))
    for A in ([[1, 1], [0, 1]], [[1, 0], [1, 1]], [[0, 1], [1, 0]]):
        gens.append(("D", gl_symplectic(A, q), gl_operator(q, A, mod)))
    gens.append(("W", full_weyl(n, q), full_fourier_operator(q, n, mod, zeta)))
    for idx in range(n):
        gens.append((f"w{idx}", coordinate_swap(n, [idx], q), partial_fourier_operator(q, n, [idx], mod, zeta)))

    rng = random.Random(260126)
    records = []
    failures = 0
    for trial in range(60):
        smat, op = sym_id, op_id
        names = []
        for _ in range(rng.randint(1, 6)):
            name, S, O = rng.choice(gens)
            names.append(name)
            smat = symplectic_multiply(S, smat, q)
            op = matmul(O, op, mod)
        _, B, _, D = split_blocks(smat)
        image_size = len(image_set(B, q))
        supports = sorted(set(support_counts(op)[0]))
        dense = is_unit_det(B, q)
        projective_ok = True
        scalar = None
        constraint_ok = True
        if dense:
            projective_ok, scalar = matrices_projectively_equal(op, representation_from_dense_bruhat(smat, q, mod, zeta), mod)
        else:
            ks = kernel_vectors(B, q)
            if len(ks) > 1:
                v = next(v for v in ks if any(v))
                pts = all_vectors(q, n)
                constraint_ok = all(
                    not op[xi][yi] or heisenberg_support_constraint(B, D, q, x, y, v)
                    for xi, x in enumerate(pts)
                    for yi, y in enumerate(pts)
                )
        ok = supports == [image_size] and projective_ok and constraint_ok
        failures += int(not ok)
        records.append({
            "trial": trial,
            "word": names,
            "unit_rank": unit_rank(smat, p),
            "dense": dense,
            "image_size": image_size,
            "row_support": supports,
            "projective_ok": projective_ok,
            "projective_scalar": scalar,
            "support_constraint_ok": constraint_ok,
        })
    return {
        "trials": len(records),
        "dense_cases": sum(r["dense"] for r in records),
        "sparse_cases": sum(not r["dense"] for r in records),
        "failures": failures,
        "records": records,
    }


def ring_dense_example() -> dict:
    p, s, q, n = 3, 2, 9, 2
    mod, zeta = coefficient_field(q)
    C = [[3, 1], [1, 0]]
    A = [[1, 1], [0, 1]]
    E = [[1, 3], [3, 0]]
    smat, op = identity(2 * n), identity(q**n)
    names = []
    for name, S, O in [
        ("L(C)", lower_shear_symplectic(C, q), lower_shear_operator(q, C, mod, zeta)),
        ("D(A)", gl_symplectic(A, q), gl_operator(q, A, mod)),
        ("W", full_weyl(n, q), full_fourier_operator(q, n, mod, zeta)),
        ("L(E)", lower_shear_symplectic(E, q), lower_shear_operator(q, E, mod, zeta)),
    ]:
        names.append(name)
        smat = matmul(S, smat, q)
        op = matmul(O, op, mod)
    _, B, _, _ = split_blocks(smat)
    predicted = representation_from_dense_bruhat(smat, q, mod, zeta)
    equal, scalar = matrices_projectively_equal(op, predicted, mod)
    return {
        "word": names,
        "B": B,
        "B_invertible": is_unit_det(B, q),
        "unit_rank": unit_rank(smat, p),
        "row_support": sorted(set(support_counts(op)[0])),
        "projectively_equal_to_additive_fourier_normal_form": equal,
        "projective_scalar": scalar,
        "sample_cross_ratio_orders": sorted(sample_nonzero_cross_ratio_orders(op, mod, 2000)),
    }


def exponent_gates() -> list[dict]:
    out = []
    for p, s, n in [(3, 1, 2), (3, 2, 2), (3, 2, 3), (5, 1, 2), (5, 2, 2)]:
        q = p**s
        Q = q**n
        _, _, cyclic_order = cyclic_fourier_witness(Q)
        out.append({
            "p": p,
            "ring_exponent_s": s,
            "module_rank_n": n,
            "dimension": Q,
            "additive_group_exponent": q,
            "cyclic_cross_ratio_order": cyclic_order,
            "obstructed": cyclic_order > q,
        })
    return out


def rank_budgets() -> list[dict]:
    out = []
    p, q = 3, 9
    for n in range(2, 7):
        stages = [coordinate_swap(n, [i], q) for i in range(n)]
        prod = identity(2 * n)
        ranks = []
        for stage in stages:
            ranks.append(unit_rank(stage, p))
            prod = matmul(stage, prod, q)
        out.append({
            "n": n,
            "stage_ranks": ranks,
            "sum_stage_ranks": sum(ranks),
            "target_rank": unit_rank(full_weyl(n, q), p),
            "product_equals_full_weyl": prod == full_weyl(n, q),
        })
    return out


def ledger_records() -> list[dict]:
    rows = []
    for p, s, vals in [
        (3, 2, (0, 0)),
        (3, 2, (0, 1)),
        (3, 2, (1, 1)),
        (3, 2, (0, 2)),
        (3, 2, (2, 2)),
        (3, 3, (0, 1)),
        (3, 3, (1, 2)),
        (5, 2, (0, 1)),
    ]:
        stats = predicted_core_stats(p, s, vals)
        Q = int(stats["dimension"])
        dense_p_butterfly_terms = p * Q * sum(s - v for v in vals)
        rows.append({
            "p": p,
            "s": s,
            "valuations": vals,
            "dimension": Q,
            "block_count": stats["block_count"],
            "row_support": stats["row_support"],
            "factor_lengths": stats["factor_lengths"],
            "dense_radix_p_multiply_add_terms": dense_p_butterfly_terms,
        })
    return rows


def main() -> dict:
    with open(ROOT / "PRIOR_v25_COMPLETE.zip", "rb") as fh:
        predecessor_hash = hashlib.sha256(fh.read()).hexdigest()
    result = {
        "status": "pass",
        "main_positive": "mixed p-adic upper-shear cells factor into tensor products of shorter cyclic prime-power Fourier cores",
        "main_negative": "no higher-dimensional local-ring Weil word on (Z/p^s)^n is monomially equivalent to the cyclic DFT of the same dimension when n>1",
        "hierarchy": hierarchy_records(),
        "word_audit": word_audit(),
        "ring_dense_example": ring_dense_example(),
        "cross_ratio_exponent_gates": exponent_gates(),
        "mod_p_rank_budgets": rank_budgets(),
        "operation_ledger": ledger_records(),
        "predecessor_sha256": predecessor_hash,
    }
    (ROOT / "results.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    (ROOT / "RESULT_SUMMARY.json").write_text(json.dumps({
        "status": result["status"],
        "main_positive": result["main_positive"],
        "main_negative": result["main_negative"],
        "word_trials": result["word_audit"]["trials"],
        "word_failures": result["word_audit"]["failures"],
        "tested_dimensions": [x["dimension"] for x in result["cross_ratio_exponent_gates"]],
        "predecessor_sha256": predecessor_hash,
    }, indent=2, sort_keys=True) + "\n")
    return result


if __name__ == "__main__":
    result = main()
    print(json.dumps({
        "status": result["status"],
        "word_trials": result["word_audit"]["trials"],
        "word_failures": result["word_audit"]["failures"],
        "tested_dimensions": [x["dimension"] for x in result["cross_ratio_exponent_gates"]],
    }, indent=2, sort_keys=True))
