"""Exact, dependency-free checks of one FFT phase-state architecture.

This is an algebraic audit, not a fast transform implementation or benchmark.
Run: python verify_phase_states.py
"""
from __future__ import annotations

import json
from pathlib import Path

PRIMES = (65537, 998244353)


def bit_reverse(value: int, width: int) -> int:
    result = 0
    for _ in range(width):
        result = 2 * result + (value & 1)
        value >>= 1
    return result


def root(n: int, prime: int) -> int:
    assert n & (n - 1) == 0 and (prime - 1) % n == 0
    value = pow(3, (prime - 1) // n, prime)
    assert pow(value, n, prime) == 1
    assert n == 1 or pow(value, n // 2, prime) != 1
    return value


def rank_mod(matrix: list[list[int]], prime: int) -> int:
    a = [row[:] for row in matrix]
    rows, columns = len(a), len(a[0])
    pivot_row = 0
    for col in range(columns):
        pivot = next((r for r in range(pivot_row, rows) if a[r][col]), None)
        if pivot is None:
            continue
        a[pivot], a[pivot_row] = a[pivot_row], a[pivot]
        inv = pow(a[pivot_row][col], -1, prime)
        a[pivot_row] = [(entry * inv) % prime for entry in a[pivot_row]]
        for r in range(pivot_row + 1, rows):
            scale = a[r][col]
            if scale:
                a[r] = [(x - scale * y) % prime for x, y in zip(a[r], a[pivot_row])]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def determinant_mod(matrix: list[list[int]], prime: int) -> int:
    a = [row[:] for row in matrix]
    n = len(a)
    assert all(len(row) == n for row in a)
    determinant = 1
    for col in range(n):
        pivot = next((r for r in range(col, n) if a[r][col]), None)
        if pivot is None:
            return 0
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            determinant = -determinant
        value = a[col][col]
        determinant = determinant * value % prime
        inv = pow(value, -1, prime)
        for r in range(col + 1, n):
            scale = a[r][col] * inv % prime
            for j in range(col + 1, n):
                a[r][j] = (a[r][j] - scale * a[col][j]) % prime
    return determinant % prime


def direct_entry(j: int, b: int, length: int, w: int, prime: int) -> int:
    return pow(w, j * bit_reverse(b, length), prime)


def factored_entry(j_left: int, b_left: int, j_right: int, b_right: int,
                   length: int, cut: int, prime: int) -> int:
    q = length - cut
    n = 1 << length
    a = direct_entry(j_left, b_left, cut, root(1 << cut, prime), prime)
    b = direct_entry(j_right, b_right, q, root(1 << q, prime), prime)
    cross = pow(root(n, prime), j_left * bit_reverse(b_right, q), prime)
    return a * b * cross % prime


def unfolding(length: int, cut: int, prime: int, correction: bool = False):
    """Rows (j_left,b_left), columns (j_right,b_right): retain BOTH indices."""
    q = length - cut
    n = 1 << length
    w = root(n, prime)
    rows = []
    for j_left in range(1 << cut):
        for b_left in range(1 << cut):
            row = []
            for j_right in range(1 << q):
                for b_right in range(1 << q):
                    j = j_left + (j_right << cut)
                    b = b_left + (b_right << cut)
                    value = direct_entry(j, b, length, w, prime)
                    assert value == factored_entry(j_left, b_left, j_right, b_right,
                                                   length, cut, prime)
                    if correction:
                        walsh = -1 if (j & b).bit_count() % 2 else 1
                        value = (value - walsh) % prime
                    row.append(value)
            rows.append(row)
    return rows


def run():
    full_checks = []
    cross_checks = []
    for prime in PRIMES:
        for length in range(2, 7):
            for cut in range(1, length):
                predicted = 1 << min(cut, length - cut)
                full_rank = rank_mod(unfolding(length, cut, prime), prime)
                correction_rank = rank_mod(unfolding(length, cut, prime, True), prime)
                assert full_rank == predicted
                assert predicted - 1 <= correction_rank <= predicted + 1
                interior = min(cut, length - cut) >= 2
                if interior:
                    assert correction_rank == predicted + 1
                full_checks.append(dict(prime=prime, n=1 << length, cut=cut,
                                        fourier_rank=full_rank, correction_rank=correction_rank,
                                        interior_cut=interior))
        for length in range(2, 11):
            n = 1 << length
            w = root(n, prime)
            for cut in range(1, length):
                a_size, c_size = 1 << cut, 1 << (length - cut)
                matrix = [[pow(w, a * c, prime) for c in range(c_size)]
                          for a in range(a_size)]
                size = min(a_size, c_size)
                actual_rank = rank_mod(matrix, prime)
                assert actual_rank == size
                square = [row[:size] for row in matrix[:size]]
                determinant = determinant_mod(square, prime)
                vandermonde = 1
                nodes = [pow(w, c, prime) for c in range(size)]
                for hi in range(size):
                    for lo in range(hi):
                        vandermonde = vandermonde * (nodes[hi] - nodes[lo]) % prime
                assert determinant == vandermonde != 0
                # Exact prefix phase-state extension: phi_(a+u*2^cut)(c).
                for a in range(a_size):
                    for u in (0, 1):
                        for c in range(c_size):
                            lhs = pow(w, (a + u * a_size) * c, prime)
                            rhs = pow(w, a * c, prime) * pow(w, u * a_size * c, prime) % prime
                            assert lhs == rhs
                cross_checks.append(dict(prime=prime, n=n, cut=cut, rank=actual_rank,
                                         leading_minor_size=size,
                                         determinant=determinant,
                                         vandermonde_product=vandermonde))
    result = dict(description="Exact phase-state architecture audit; no timing claim",
                  full_unfolding_checks=full_checks,
                  cross_matrix_checks=cross_checks,
                  summary=dict(full_unfolding_cases=len(full_checks),
                               cross_matrix_and_minor_cases=len(cross_checks),
                               all_checks_passed=True))
    output = Path(__file__).with_name("results.json")
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result["summary"], indent=2))


if __name__ == "__main__":
    run()
