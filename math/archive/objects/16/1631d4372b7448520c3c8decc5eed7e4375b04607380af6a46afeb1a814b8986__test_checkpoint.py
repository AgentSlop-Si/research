from __future__ import annotations
import json
import unittest

from primitive_phase_embedding import (
    classify_fourier_submatrix,
    coefficient_field,
    direct_sum_weyl,
    exhaustive_embedding_audit_q3_n2,
    fourier_matrix,
    identity,
    is_ordered_fourier_embedding,
    kronecker,
    matmul,
    matrix_equal,
    matrix_inverse,
    nilpotent_lift_embedding,
    operation_ledger,
    shift_matrix,
    modulation_matrix,
    swap_operator,
    verify_swap_covariance,
    weyl_algebra_rank,
)


class PrimitivePhaseTests(unittest.TestCase):
    def test_weyl_algebra_is_full(self):
        for n in (3, 5, 7, 9):
            mod, zeta = coefficient_field(n)
            self.assertEqual(weyl_algebra_rank(n, mod, zeta), n * n)

    def test_swap_covariance_and_solution_dimension(self):
        for n, m in ((3, 2), (5, 2), (7, 2), (9, 2), (3, 3)):
            row = verify_swap_covariance(n, m)
            self.assertTrue(row["covariance_ok"])
            self.assertEqual(row["commutant_dimension"], m * m)
            self.assertEqual(row["swap_solution_dimension"], m * m)

    def test_standard_fourier_conjugation(self):
        for n in (3, 5, 9):
            mod, zeta = coefficient_field(n)
            x = shift_matrix(n)
            z = modulation_matrix(n, mod, zeta)
            f = fourier_matrix(n, mod, zeta)
            fi = matrix_inverse(f, mod)
            self.assertTrue(matrix_equal(matmul(matmul(f, x, mod), fi, mod), z, mod))
            self.assertTrue(matrix_equal(matmul(matmul(f, z, mod), fi, mod), matrix_inverse(x, mod), mod))

    def test_direct_sum_swap_formula(self):
        n, m = 5, 3
        mod, zeta = coefficient_field(n)
        x, z = direct_sum_weyl(n, m, mod, zeta)
        u = [[1 if i == j else (i + 2 * j + 1) % mod if i < j else 0 for j in range(m)] for i in range(m)]
        j = swap_operator(n, m, mod, zeta, u)
        ji = matrix_inverse(j, mod)
        self.assertTrue(matrix_equal(matmul(matmul(j, x, mod), ji, mod), z, mod))

    def test_exhaustive_q3_embedding_classification(self):
        row = exhaustive_embedding_audit_q3_n2()
        self.assertGreater(row["fourier_embeddings"], 0)
        self.assertEqual(row["classified_embeddings"], row["fourier_embeddings"])

    def test_nilpotent_spectator_lifts(self):
        for q in (9, 25):
            rows, cols = nilpotent_lift_embedding(q)
            self.assertTrue(is_ordered_fourier_embedding(rows, cols, q))
            cert = classify_fourier_submatrix(rows, cols, q)
            self.assertEqual(cert.primitive_pairing, 1)
            self.assertTrue(cert.direct_factor_ok)
            self.assertTrue(cert.row_spectator_ok)
            self.assertTrue(cert.col_spectator_ok)
            self.assertTrue(cert.spectator_pairing_ok)
            self.assertGreater(sum(any(v for v in row[1:]) for row in rows), 0)
            self.assertGreater(sum(any(v for v in col[1:]) for col in cols), 0)

    def test_operation_ledger_exposes_full_core(self):
        for n, r in ((9, 2), (25, 2), (9, 3)):
            row = operation_ledger(n, r)
            self.assertEqual(row["minimal_primitive_weyl_block_dimension"], n)
            self.assertEqual(row["restricted_core"], f"one full F_{n}")
            self.assertGreaterEqual(row["ambient_dimension"], n)

    def test_tensor_slice_is_exact_fourier(self):
        n, m = 5, 2
        mod, zeta = coefficient_field(n)
        f = fourier_matrix(n, mod, zeta)
        j = kronecker(f, identity(m), mod)
        # Slice multiplicity coordinate 0 on input and output.
        sub = [[j[i * m][k * m] for k in range(n)] for i in range(n)]
        self.assertTrue(matrix_equal(sub, f, mod))

    def test_saved_results_schema(self):
        with open("results.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(len(data["covariance_normal_forms"]), 5)
        self.assertEqual(data["exhaustive_q3_n2"]["fourier_embeddings"], data["exhaustive_q3_n2"]["classified_embeddings"])
        self.assertTrue(all(x["ordered_fourier"] for x in data["nilpotent_lifts"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
