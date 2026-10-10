from __future__ import annotations
import json
from primitive_phase_embedding import (
    classify_fourier_submatrix,
    exhaustive_embedding_audit_q3_n2,
    is_ordered_fourier_embedding,
    nilpotent_lift_embedding,
    operation_ledger,
    verify_swap_covariance,
    weyl_algebra_rank,
    coefficient_field,
)


def main() -> None:
    covariance = [verify_swap_covariance(n, m) for n, m in [(3, 2), (5, 2), (7, 2), (9, 2), (3, 3)]]
    algebra = []
    for n in (3, 5, 7, 9):
        mod, zeta = coefficient_field(n)
        algebra.append({"n": n, "field": mod, "weyl_algebra_rank": weyl_algebra_rank(n, mod, zeta), "expected": n * n})
    exhaustive = exhaustive_embedding_audit_q3_n2()
    lifts = []
    for q in (9, 25):
        rows, cols = nilpotent_lift_embedding(q)
        cert = classify_fourier_submatrix(rows, cols, q)
        lifts.append({
            "q": q,
            "ordered_fourier": is_ordered_fourier_embedding(rows, cols, q),
            "certificate": cert.__dict__,
            "nonzero_row_spectators": sum(any(v for v in row[1:]) for row in rows),
            "nonzero_col_spectators": sum(any(v for v in col[1:]) for col in cols),
        })
    ledgers = [operation_ledger(n, r) for n, r in [(9, 2), (25, 2), (9, 3)]]
    result = {
        "status": "primitive-phase invariant-subspace rigidity; no faster exact FFT",
        "covariance_normal_forms": covariance,
        "weyl_algebra": algebra,
        "exhaustive_q3_n2": exhaustive,
        "nilpotent_lifts": lifts,
        "operation_ledgers": ledgers,
    }
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, sort_keys=True)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
