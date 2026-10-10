from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence
import random

from common import (
    dft_matrix, diag_left_right_permute_fourier, inverse_permutation, mod_inverse, mod_matmul, mod_rank,
    random_nonzero, random_permutation, submatrix,
)


@dataclass(frozen=True)
class GreenWitness:
    n: int
    rows_I: tuple[int, int]
    cols_J: tuple[int, int]
    support_R: tuple[int, ...]
    support_C: tuple[int, ...]
    forbidden_columns: tuple[int, ...]


def choose_parallel_sum_witness(sigma_a: Sequence[int], sigma_b: Sequence[int]) -> GreenWitness:
    """Construct the 2x2 zero-rectangle witness used in the theorem.

    A row i is supported in {i, sigma_a[i]}; B row i in {i, sigma_b[i]}.
    B column j is supported in {j, tau_b[j]} with tau_b=sigma_b^{-1}.
    For n>=11, the construction always succeeds.
    """
    n = len(sigma_a)
    if len(sigma_b) != n or sorted(sigma_a) != list(range(n)) or sorted(sigma_b) != list(range(n)):
        raise ValueError("invalid permutations")
    if n < 11:
        raise ValueError("the universal construction is stated for n>=11")

    i0 = next((i for i in range(n) if sigma_a[i] != i), 0)
    if sigma_a[i0] != i0:
        I = [i0, sigma_a[i0]]
    else:
        I = [0, 1]
    I = list(dict.fromkeys(I))
    if len(I) != 2:
        raise AssertionError("failed to construct two rows")

    R = sorted(set(I) | {sigma_a[i] for i in I})
    forbidden = sorted(set(I) | {sigma_a[i] for i in I} | {sigma_b[i] for i in I})
    S = [j for j in range(n) if j not in set(forbidden)]
    if len(S) <= n / 2:
        raise AssertionError("complement is not a strict majority")

    tau = inverse_permutation(sigma_b)
    j0 = next((j for j in S if tau[j] in set(S)), None)
    if j0 is None:
        raise AssertionError("strict-majority intersection failed")
    if tau[j0] != j0:
        J = [j0, tau[j0]]
    else:
        j1 = next(j for j in S if j != j0)
        J = [j0, j1]
    C = sorted(set(J) | {tau[j] for j in J})

    if len(R) > 3 or len(C) > 3:
        raise AssertionError("support compression failed")
    if set(J) & set(forbidden):
        raise AssertionError("not a zero rectangle")
    return GreenWitness(n, tuple(I), tuple(J), tuple(R), tuple(C), tuple(forbidden))


def weighted_diagonal_plus_permutation(
    sigma: Sequence[int], diag: Sequence[int], off: Sequence[int], p: int
) -> list[list[int]]:
    """Matrix whose row i has diagonal weight diag[i] and monomial weight at sigma[i]."""
    n = len(sigma)
    out = [[0] * n for _ in range(n)]
    for i in range(n):
        out[i][i] = (out[i][i] + diag[i]) % p
        out[i][sigma[i]] = (out[i][sigma[i]] + off[i]) % p
    return out


def sample_invertible_sparse_inverse(sigma: Sequence[int], p: int, rng: random.Random) -> list[list[int]]:
    for _ in range(500):
        diag = [random_nonzero(p, rng) for _ in sigma]
        off = [random_nonzero(p, rng) for _ in sigma]
        a = weighted_diagonal_plus_permutation(sigma, diag, off, p)
        if mod_rank(a, p) == len(sigma):
            return a
    raise RuntimeError("failed to sample an invertible sparse inverse")


def contradiction_block(
    target: Sequence[Sequence[int]],
    a: Sequence[Sequence[int]],
    b: Sequence[Sequence[int]],
    sigma_a: Sequence[int],
    sigma_b: Sequence[int],
    p: int,
) -> dict:
    """Return the exact block quantities behind A F B = A+B.

    If target=A^{-1}+B^{-1}, then A target B=A+B. The witness makes the
    corresponding A+B block zero, while the Fourier full-minor property forces
    the A target B block to be nonzero.
    """
    w = choose_parallel_sum_witness(sigma_a, sigma_b)
    I, J, R, C = list(w.rows_I), list(w.cols_J), list(w.support_R), list(w.support_C)
    u = submatrix(a, I, R)
    v = submatrix(b, C, J)
    f_rc = submatrix(target, R, C)
    lhs = mod_matmul(mod_matmul(u, f_rc, p), v, p)
    rhs = submatrix([[ (a[i][j] + b[i][j]) % p for j in range(len(a))]
                     for i in range(len(a))], I, J)
    return {
        "witness": w,
        "rank_u": mod_rank(u, p),
        "rank_v": mod_rank(v, p),
        "rank_f_rc": mod_rank(f_rc, p),
        "rank_lhs": mod_rank(lhs, p),
        "rhs_zero": all(x % p == 0 for row in rhs for x in row),
        "lhs": lhs,
        "rhs": rhs,
    }


def exact_random_audit(n: int, p: int, omega: int, trials: int = 50, seed: int = 1701) -> dict:
    rng = random.Random(seed + n)
    f0 = dft_matrix(n, p, omega)
    min_lhs_rank = 10
    max_r = max_c = 0
    for _ in range(trials):
        sa = random_permutation(n, rng)
        sb = random_permutation(n, rng)
        a = sample_invertible_sparse_inverse(sa, p, rng)
        b = sample_invertible_sparse_inverse(sb, p, rng)
        rp = random_permutation(n, rng)
        cp = random_permutation(n, rng)
        dl = [random_nonzero(p, rng) for _ in range(n)]
        dr = [random_nonzero(p, rng) for _ in range(n)]
        f = diag_left_right_permute_fourier(f0, rp, cp, dl, dr, p)
        report = contradiction_block(f, a, b, sa, sb, p)
        assert report["rhs_zero"]
        assert report["rank_u"] == 2 and report["rank_v"] == 2
        assert report["rank_f_rc"] == min(len(report["witness"].support_R), len(report["witness"].support_C))
        assert report["rank_lhs"] >= 1
        min_lhs_rank = min(min_lhs_rank, report["rank_lhs"])
        max_r = max(max_r, len(report["witness"].support_R))
        max_c = max(max_c, len(report["witness"].support_C))
    return {
        "n": n,
        "trials": trials,
        "min_contradiction_block_rank": min_lhs_rank,
        "max_support_R": max_r,
        "max_support_C": max_c,
    }


def green_term_from_sparse_inverse(a: Sequence[Sequence[int]], p: int) -> list[list[int]]:
    return mod_inverse(a, p)
