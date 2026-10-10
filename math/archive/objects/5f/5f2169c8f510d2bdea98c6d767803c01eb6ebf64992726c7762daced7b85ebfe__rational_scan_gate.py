from __future__ import annotations
import random
from algebra_utils import (
    MOD, cycle_shift, inv_mod, mat_mul, poly_matrix, rank_mod, submatrix,
    primitive_root_of_order,
)


def rational_scan_matrix(n: int, q: list[int], pcoef: list[int], mod: int = MOD):
    c = cycle_shift(n)
    qmat = poly_matrix(q, c, mod)
    pmat = poly_matrix(pcoef, c, mod)
    return mat_mul(inv_mod(qmat, mod), pmat, mod)


def gate_rectangle(n: int, numerator_degree: int):
    m = (n - numerator_degree) // 2
    cols = list(range(m))
    rows = list(range(m + numerator_degree, m + numerator_degree + m))
    return rows, cols


def fourier_matrix(n: int, mod: int = MOD):
    w = primitive_root_of_order(n, mod)
    return [[pow(w, i * j, mod) for j in range(n)] for i in range(n)]


def random_gate_cases(seed: int = 1902):
    rng = random.Random(seed)
    records = []
    for n in (13, 17, 21, 25):
        for d in (1, 2, 3, 4):
            for e in (0, 1, 2):
                m = (n - e) // 2
                if d >= m:
                    continue
                for _ in range(100):
                    q = [rng.randrange(1, MOD)] + [rng.randrange(MOD) for _ in range(d-1)] + [rng.randrange(1, MOD)]
                    pcoef = [rng.randrange(MOD) for _ in range(e+1)]
                    if pcoef[-1] == 0:
                        pcoef[-1] = 1
                    try:
                        t = rational_scan_matrix(n, q, pcoef)
                        break
                    except ValueError:
                        continue
                else:
                    raise RuntimeError("no invertible q(P)")
                rows, cols = gate_rectangle(n, e)
                r = rank_mod(submatrix(t, rows, cols))
                if r > d:
                    raise AssertionError((n, d, e, r))
                records.append({"n": n, "denominator_degree": d, "numerator_degree": e,
                                "rectangle_size": m, "rectangle_rank": r})
    # Exact Fourier contradiction at N=17, supported by the package field.
    n = 17
    f = fourier_matrix(n)
    for e in (0, 1, 2, 3):
        rows, cols = gate_rectangle(n, e)
        r = rank_mod(submatrix(f, rows, cols))
        if r != len(rows):
            raise AssertionError("selected Fourier Vandermonde block lost rank")
        records.append({"fourier_n": n, "numerator_degree": e,
                        "rectangle_size": len(rows), "fourier_rank": r})
    return records


if __name__ == "__main__":
    import json
    print(json.dumps(random_gate_cases(), indent=2))
