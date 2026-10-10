from __future__ import annotations

from dataclasses import dataclass, asdict
from random import Random

from tensor_weil import (
    bilinear_fourier,
    coefficient_field,
    column_permutation_for_linear,
    cross_ratio,
    cyclic_fourier,
    permute_columns,
    random_invertible,
    random_word,
    tensor_fourier,
    upper_right_rank,
)


def multiplicative_order(x: int, mod: int) -> int:
    if x % mod == 0:
        raise ValueError("zero has no multiplicative order")
    cur = 1
    for k in range(1, mod):
        cur = cur * x % mod
        if cur == 1:
            return k
    raise RuntimeError("order not found")


@dataclass
class CrossRatioCase:
    p: int
    n: int
    dimension: int
    coefficient_prime: int
    cyclic_witness_order: int
    tensor_random_checks: int
    dense_weil_checks: int


def audit_case(p: int, n: int, seed: int = 2402) -> CrossRatioCase:
    q = p ** n
    ell, zeta = coefficient_field(q)
    omega = pow(zeta, q // p, ell)
    cyclic = cyclic_fourier(q, ell, zeta)
    tensor = tensor_fourier(p, n, ell, omega)
    witness = cross_ratio(cyclic, 0, 1, 0, 1, ell)
    order = multiplicative_order(witness, ell)
    if order != q:
        raise AssertionError((p, n, order, q))
    rng = Random(seed + p * 100 + n)
    tensor_checks = 0
    for _ in range(250):
        i, k = rng.sample(range(q), 2)
        j, l = rng.sample(range(q), 2)
        cr = cross_ratio(tensor, i, k, j, l, ell)
        if pow(cr, p, ell) != 1:
            raise AssertionError("tensor cross ratio escaped p-th roots")
        tensor_checks += 1
    dense_checks = 0
    while dense_checks < 80:
        s, u, _ = random_word(p, n, ell, omega, rng.randrange(3, 12), rng)
        if upper_right_rank(s, p) != n:
            continue
        i, k = rng.sample(range(q), 2)
        j, l = rng.sample(range(q), 2)
        cr = cross_ratio(u, i, k, j, l, ell)
        if pow(cr, p, ell) != 1:
            raise AssertionError("dense Weil cross ratio escaped p-th roots")
        dense_checks += 1
    # Any nondegenerate bilinear additive Fourier form is a column permutation
    # of the standard tensor Fourier matrix.
    for _ in range(12):
        m = random_invertible(n, p, rng)
        bf = bilinear_fourier(m, p, ell, omega)
        perm = column_permutation_for_linear(m, p)
        if bf != permute_columns(tensor, perm):
            raise AssertionError("bilinear additive Fourier did not reduce to tensor Fourier")
    return CrossRatioCase(p, n, q, ell, order, tensor_checks, dense_checks)


def run_audit() -> dict:
    cases = [audit_case(3, 2), audit_case(3, 3), audit_case(5, 2)]
    return {"cases": [asdict(c) for c in cases]}


if __name__ == "__main__":
    import json
    print(json.dumps(run_audit(), indent=2, sort_keys=True))
