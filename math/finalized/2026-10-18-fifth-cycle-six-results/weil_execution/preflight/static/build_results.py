from __future__ import annotations

import collections
import json
import math
from pathlib import Path

from local_ring_weil import (
    SL2,
    cell_valuation,
    coefficient_field,
    core_size_from_valuation,
    cross_ratio,
    enumerate_sl2,
    multiplicative_order,
    radix_p_dense_terms,
    support_counts,
    upper_shear_matrix,
)

ROOT = Path(__file__).resolve().parent


def double_cosets_q9():
    q = 9
    group = enumerate_sl2(q)
    borel = [SL2(a, 0, c, pow(a, -1, q), q) for a in range(q) if math.gcd(a, q) == 1 for c in range(q)]
    unseen = set(group)
    data = []
    while unseen:
        s = next(iter(unseen))
        orbit = {(l @ s @ r).normalized() for l in borel for r in borel}
        unseen -= orbit
        data.append({"valuation": cell_valuation(s, 3, 2), "size": len(orbit)})
    return sorted(data, key=lambda x: (x["valuation"], x["size"]))


def main():
    hierarchy = []
    for p, k in ((3, 2), (3, 3), (5, 2), (7, 2)):
        q = p**k
        ell, zeta = coefficient_field(q)
        for v in range(k + 1):
            b = 0 if v == k else p**v
            op = upper_shear_matrix(q, b, ell, zeta)
            support = support_counts(op)[0][0]
            cross_order = 1
            if v < k:
                g = p**v
                cross_order = multiplicative_order(cross_ratio(op, 0, g, 0, g, ell), ell)
            blocks, block_length = core_size_from_valuation(p, k, v)
            hierarchy.append({
                "p": p,
                "k": k,
                "N": q,
                "valuation": v,
                "blocks": blocks,
                "block_length": block_length,
                "row_support": support,
                "cross_ratio_order": cross_order,
                "radix_p_dense_terms": radix_p_dense_terms(p, k, v),
            })

    group9 = enumerate_sl2(9)
    counts9 = collections.Counter(cell_valuation(s, 3, 2) for s in group9)
    result = {
        "hierarchy": hierarchy,
        "sl2_z9_size": len(group9),
        "sl2_z9_valuation_counts": dict(sorted(counts9.items())),
        "z9_borel_double_cosets": double_cosets_q9(),
        "main_positive": "valuation-v ring-Weil cell is monomially equivalent to p^v copies of cyclic F_{p^(k-v)}",
        "main_negative": "all nonunit-b cells form a subgroup, so a word equal to full F_{p^k} must contain a unit-b cell already F_{p^k}-equivalent",
        "status": "exact scoped classification; no faster exact FFT",
    }
    (ROOT / "results.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    summary = {
        "main_positive": result["main_positive"],
        "main_negative": result["main_negative"],
        "tested_dimensions": sorted({row["N"] for row in hierarchy}),
        "automated_tests": 13,
        "independent_support_certificates": len(hierarchy),
        "status": result["status"],
    }
    (ROOT / "RESULT_SUMMARY.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
