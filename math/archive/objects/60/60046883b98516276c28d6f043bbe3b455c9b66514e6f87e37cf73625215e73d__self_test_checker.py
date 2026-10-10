#!/usr/bin/env python3
"""Small exact-integer determinant cross-checks for the audit eliminator."""
from itertools import combinations, permutations
from pathlib import Path
import json
import random

import numpy as np
from check_bitrev import elimination


def determinant_leibniz(matrix):
    n = len(matrix)
    total = 0
    for perm in permutations(range(n)):
        term = 1
        for i, j in enumerate(perm):
            term *= int(matrix[i][j])
        inversions = sum(perm[i] > perm[j] for i in range(n) for j in range(i+1, n))
        total += (-1 if inversions % 2 else 1) * term
    return total


def main():
    rng = random.Random(981273)
    tests = []
    for p in (2, 3, 17, 12289, 65537):
        for nr, nc in ((2, 3), (3, 2), (4, 4), (3, 5)):
            for kind in ("random", "duplicated_rows", "zero", "rank_one"):
                a = np.array([[rng.randrange(p) for _ in range(nc)] for _ in range(nr)], dtype=np.int64)
                if kind == "duplicated_rows":
                    a[-1] = a[0]
                elif kind == "zero":
                    a[:] = 0
                elif kind == "rank_one":
                    a = np.outer(a[:, 0], a[0]) % p
                exact_rank = 0
                for r in range(min(nr, nc), 0, -1):
                    found = any(determinant_leibniz(a[np.ix_(rows, cols)]) % p
                                for rows in combinations(range(nr), r)
                                for cols in combinations(range(nc), r))
                    if found:
                        exact_rank = r
                        break
                checked = elimination(a, p)
                assert checked["rank"] == exact_rank
                minor = a[np.ix_(checked["pivot_rows_in_selection_order"], checked["pivot_columns"])]
                assert determinant_leibniz(minor) % p == checked["selected_minor_determinant"]
                if nr == nc == exact_rank:
                    assert determinant_leibniz(a) % p == checked["original_order_determinant"]
                tests.append({"prime": p, "shape": [nr, nc], "kind": kind, "rank": exact_rank})
    out = {"status": "PASS", "tests": tests,
           "method": "Exact Python-integer Leibniz determinants and exhaustive minors on small matrices"}
    (Path(__file__).resolve().parent / "checks" / "self_tests.json").write_text(json.dumps(out, indent=2)+"\n")
    print(f"PASS {len(tests)} exact-integer cross-checks")


if __name__ == "__main__":
    main()
