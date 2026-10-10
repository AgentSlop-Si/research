from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence
import random

from common import (
    dft_matrix, mod_matmul, mod_rank, mod_transpose, random_nonzero,
    random_permutation, submatrix,
)


@dataclass
class SemiseparableStage:
    lower_row: list[int]
    lower_col: list[int]
    diagonal: list[int]
    upper_row: list[int]
    upper_col: list[int]
    modulus: int

    def matrix(self) -> list[list[int]]:
        n = len(self.diagonal)
        p = self.modulus
        out = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i > j:
                    out[i][j] = self.lower_row[i] * self.lower_col[j] % p
                elif i < j:
                    out[i][j] = self.upper_row[i] * self.upper_col[j] % p
                else:
                    out[i][j] = self.diagonal[i] % p
        return out

    def input_adjacent_minors(self) -> list[int]:
        p = self.modulus
        b, e = self.lower_col, self.upper_col
        return [(b[j] * e[j + 1] - b[j + 1] * e[j]) % p for j in range(len(b) - 1)]

    def output_adjacent_minors(self) -> list[int]:
        p = self.modulus
        a, c = self.lower_row, self.upper_row
        return [(a[j] * c[j + 1] - a[j + 1] * c[j]) % p for j in range(len(a) - 1)]


def cross3(u: Sequence[int], v: Sequence[int], p: int) -> list[int]:
    return [
        (u[1] * v[2] - u[2] * v[1]) % p,
        (u[2] * v[0] - u[0] * v[2]) % p,
        (u[0] * v[1] - u[1] * v[0]) % p,
    ]


def input_annihilator(stage: SemiseparableStage, start: int) -> list[int]:
    j = start
    return cross3(stage.lower_col[j:j + 3], stage.upper_col[j:j + 3], stage.modulus)


def output_annihilator(stage: SemiseparableStage, start: int) -> list[int]:
    i = start
    return cross3(stage.lower_row[i:i + 3], stage.upper_row[i:i + 3], stage.modulus)


def embedded_annihilator_bank(n: int, starts: Sequence[int], vectors: Sequence[Sequence[int]]) -> list[list[int]]:
    out = [[0] * len(starts) for _ in range(n)]
    for c, (s, v) in enumerate(zip(starts, vectors)):
        for t in range(3):
            out[s + t][c] = v[t]
    return out


def find_length_five_gap(n: int, forbidden: set[int]) -> int:
    for start in range(n - 4):
        if all((start + t) not in forbidden for t in range(5)):
            return start
    raise ValueError("no length-five gap")


def permutation_apply_matrix(perm: Sequence[int]) -> list[list[int]]:
    n = len(perm)
    out = [[0] * n for _ in range(n)]
    for j, i in enumerate(perm):
        out[i][j] = 1
    return out


def random_fully_nondegenerate_stage(n: int, p: int, rng: random.Random) -> SemiseparableStage:
    for _ in range(1000):
        s = SemiseparableStage(
            [random_nonzero(p, rng) for _ in range(n)],
            [random_nonzero(p, rng) for _ in range(n)],
            [random_nonzero(p, rng) for _ in range(n)],
            [random_nonzero(p, rng) for _ in range(n)],
            [random_nonzero(p, rng) for _ in range(n)],
            p,
        )
        if all(s.input_adjacent_minors()) and all(s.output_adjacent_minors()):
            m = s.matrix()
            if mod_rank(m, p) == n:
                return s
    raise RuntimeError("could not sample a fully nondegenerate invertible stage")


def endpoint_monomial_fourier(
    f: Sequence[Sequence[int]], p: int, rng: random.Random
) -> tuple[list[list[int]], dict]:
    n = len(f)
    rp = random_permutation(n, rng)
    cp = random_permutation(n, rng)
    dl = [random_nonzero(p, rng) for _ in range(n)]
    dr = [random_nonzero(p, rng) for _ in range(n)]
    m = [[dl[i] * f[rp[i]][cp[j]] % p * dr[j] % p for j in range(n)] for i in range(n)]
    return m, {"row_perm": rp, "col_perm": cp, "left": dl, "right": dr}


def annihilator_contradiction(
    s1: SemiseparableStage,
    s2: SemiseparableStage,
    internal_perm: Sequence[int],
    target: Sequence[Sequence[int]],
) -> dict:
    """Build the 3-window/5-coordinate contradiction certificate."""
    n = len(internal_perm)
    p = s1.modulus
    if n < 30:
        raise ValueError("universal interval argument requires n>=30")
    if s2.modulus != p:
        raise ValueError("modulus mismatch")
    if not all(s1.input_adjacent_minors()) or not all(s2.output_adjacent_minors()):
        raise ValueError("stage is outside the fully nondegenerate branch")

    input_start = 0
    input_starts = [0, 1, 2]
    input_vectors = [input_annihilator(s1, j) for j in input_starts]
    X = embedded_annihilator_bank(n, input_starts, input_vectors)
    input_union = set(range(5))
    mapped = {internal_perm[j] for j in input_union}
    output_start = find_length_five_gap(n, mapped)
    output_starts = [output_start, output_start + 1, output_start + 2]
    output_vectors = [output_annihilator(s2, i) for i in output_starts]
    Y = embedded_annihilator_bank(n, output_starts, output_vectors)
    output_union = set(range(output_start, output_start + 5))

    S1 = s1.matrix()
    S2 = s2.matrix()
    P = permutation_apply_matrix(internal_perm)
    S1X = mod_matmul(S1, X, p)
    YtS2 = mod_matmul(mod_transpose(Y), S2, p)
    rhs = mod_matmul(mod_matmul(YtS2, P, p), S1X, p)
    lhs = mod_matmul(mod_matmul(mod_transpose(Y), target, p), X, p)

    outside_input = [i for i in range(n) if i not in input_union]
    outside_output = [j for j in range(n) if j not in output_union]
    support_ok_input = all(S1X[i][j] % p == 0 for i in outside_input for j in range(3))
    support_ok_output = all(YtS2[i][j] % p == 0 for i in range(3) for j in outside_output)

    return {
        "input_start": input_start,
        "output_start": output_start,
        "mapped_input_union": sorted(mapped),
        "input_union": sorted(input_union),
        "output_union": sorted(output_union),
        "rank_X": mod_rank(X, p),
        "rank_Y": mod_rank(Y, p),
        "rank_S1X": mod_rank(S1X, p),
        "rank_YtS2": mod_rank(YtS2, p),
        "support_ok_input": support_ok_input,
        "support_ok_output": support_ok_output,
        "rhs_rank": mod_rank(rhs, p),
        "lhs_rank": mod_rank(lhs, p),
        "rhs": rhs,
        "lhs": lhs,
    }


def exact_random_audit(n: int, p: int, omega: int, trials: int = 25, seed: int = 1717) -> dict:
    rng = random.Random(seed + n)
    f = dft_matrix(n, p, omega)
    min_lhs_rank = 99
    for _ in range(trials):
        s1 = random_fully_nondegenerate_stage(n, p, rng)
        s2 = random_fully_nondegenerate_stage(n, p, rng)
        perm = random_permutation(n, rng)
        target, _ = endpoint_monomial_fourier(f, p, rng)
        report = annihilator_contradiction(s1, s2, perm, target)
        assert report["rank_X"] == 3 and report["rank_Y"] == 3
        assert report["rank_S1X"] == 3 and report["rank_YtS2"] == 3
        assert report["support_ok_input"] and report["support_ok_output"]
        assert report["rhs_rank"] == 0
        assert report["lhs_rank"] >= 1
        min_lhs_rank = min(min_lhs_rank, report["lhs_rank"])
    return {"n": n, "trials": trials, "min_fourier_bilinear_rank": min_lhs_rank}
