from __future__ import annotations

import hashlib
import json
import random
import unittest
from pathlib import Path

from cross_ratio_gate import audit_case
from group_audit import exhaustive_sp4_3_rank_distribution, random_support_audit
from tensor_weil import (
    bilinear_fourier,
    coefficient_field,
    column_permutation_for_linear,
    cross_ratio,
    cyclic_fourier,
    direct_partial_fft_cost,
    identity,
    mat_mul,
    partial_fourier_operator,
    partial_weyl_symplectic,
    permute_columns,
    random_invertible,
    random_word,
    rank_mod,
    support_counts,
    symplectic_identity,
    tensor_fourier,
    upper_right_rank,
    vectors,
)

PREDECESSOR_SHA = "cf7570b1afd956fded5c5353fb01b0716a2c73c480ebcd64c1f51a8363d9b962"


class TensorWeilRankTests(unittest.TestCase):
    def test_canonical_partial_support(self):
        for p, n in ((3, 2), (3, 3), (5, 2)):
            q = p ** n
            ell, zeta = coefficient_field(q)
            omega = pow(zeta, q // p, ell)
            for r in range(n + 1):
                u = partial_fourier_operator(n, range(r), p, ell, omega)
                rows, cols = support_counts(u, ell)
                self.assertEqual(set(rows), {p ** r})
                self.assertEqual(set(cols), {p ** r})

    def test_random_word_support_equals_rank_B(self):
        for p, n, trials in ((3, 2, 70), (3, 3, 40), (5, 2, 40)):
            audit = random_support_audit(p, n, trials=trials, seed=2410)
            self.assertEqual(audit.trials, trials)

    def test_exhaustive_sp4_3_distribution(self):
        self.assertEqual(
            exhaustive_sp4_3_rank_distribution(),
            {0: 1296, 1: 15552, 2: 34992},
        )

    def test_rank_B_subadditivity(self):
        rng = random.Random(2411)
        for p, n in ((3, 2), (3, 3), (5, 2)):
            q = p ** n
            ell, zeta = coefficient_field(q)
            omega = pow(zeta, q // p, ell)
            for _ in range(100):
                s, _, _ = random_word(p, n, ell, omega, rng.randrange(1, 8), rng)
                t, _, _ = random_word(p, n, ell, omega, rng.randrange(1, 8), rng)
                st = mat_mul(s, t, p)
                self.assertLessEqual(
                    upper_right_rank(st, p),
                    upper_right_rank(s, p) + upper_right_rank(t, p),
                )

    def test_coordinate_partial_factorization_is_tensor_fft(self):
        for p, n in ((3, 2), (3, 3), (5, 2)):
            q = p ** n
            ell, zeta = coefficient_field(q)
            omega = pow(zeta, q // p, ell)
            op = identity(q)
            symp = symplectic_identity(n)
            for j in range(n):
                op = mat_mul(partial_fourier_operator(n, [j], p, ell, omega), op, ell)
                symp = mat_mul(partial_weyl_symplectic(n, [j], p), symp, p)
            self.assertEqual(op, tensor_fourier(p, n, ell, omega))
            self.assertEqual(upper_right_rank(symp, p), n)

    def test_cross_ratio_exponent_obstruction(self):
        for p, n in ((3, 2), (3, 3), (5, 2)):
            case = audit_case(p, n, seed=2412)
            self.assertEqual(case.cyclic_witness_order, p ** n)

    def test_rank_deficient_weil_has_zeros(self):
        rng = random.Random(2413)
        p, n = 3, 3
        q = p ** n
        ell, zeta = coefficient_field(q)
        omega = pow(zeta, q // p, ell)
        seen = 0
        while seen < 30:
            s, u, _ = random_word(p, n, ell, omega, rng.randrange(1, 10), rng)
            r = upper_right_rank(s, p)
            if r == n:
                continue
            rows, _ = support_counts(u, ell)
            self.assertEqual(set(rows), {p ** r})
            self.assertLess(p ** r, q)
            seen += 1

    def test_extension_field_additive_dft_is_tensor_after_linear_relabeling(self):
        rng = random.Random(2414)
        for p, n in ((3, 2), (3, 3), (5, 2)):
            q = p ** n
            ell, zeta = coefficient_field(q)
            omega = pow(zeta, q // p, ell)
            standard = tensor_fourier(p, n, ell, omega)
            for _ in range(20):
                m = random_invertible(n, p, rng)
                got = bilinear_fourier(m, p, ell, omega)
                perm = column_permutation_for_linear(m, p)
                self.assertEqual(got, permute_columns(standard, perm))

    def test_explicit_operation_ledger_scales_with_rank(self):
        for p, n in ((3, 4), (5, 3)):
            N = p ** n
            full = direct_partial_fft_cost(p, n, n)
            self.assertEqual(full["dense_terms"], n * p * N)
            for r in range(n + 1):
                row = direct_partial_fft_cost(p, n, r)
                self.assertEqual(row["dense_terms"], r * p * N)

    def test_predecessor_hash(self):
        path = Path(__file__).with_name("PRIOR_v23_COMPLETE.zip")
        self.assertTrue(path.is_file())
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), PREDECESSOR_SHA)


if __name__ == "__main__":
    unittest.main(verbosity=2)
