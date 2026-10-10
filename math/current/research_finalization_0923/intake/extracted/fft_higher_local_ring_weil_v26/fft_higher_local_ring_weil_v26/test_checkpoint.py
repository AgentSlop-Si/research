from __future__ import annotations

import hashlib
import json
import os
import random
import unittest
import zipfile

from higher_local_ring_weil import (
    certificate_from_valuations,
    coefficient_field,
    congruence_transform,
    coordinate_swap,
    cyclic_equivalence_exponent_gate,
    cyclic_fourier_witness,
    diagonal_upper_shear,
    direct_upper_shear_nd,
    full_fourier_operator,
    full_weyl,
    gl_operator,
    gl_symplectic,
    heisenberg_support_constraint,
    identity,
    image_set,
    kernel_vectors,
    lower_shear_operator,
    lower_shear_symplectic,
    matmul,
    matrices_projectively_equal,
    partial_fourier_operator,
    predicted_core_stats,
    representation_from_dense_bruhat,
    sample_nonzero_cross_ratio_orders,
    split_blocks,
    support_counts,
    symplectic_multiply,
    unit_rank,
    upper_shear_operator_nd,
    upper_shear_symplectic,
    all_vectors,
    is_unit_det,
)


ROOT = os.path.dirname(__file__)


class HigherLocalRingWeilTests(unittest.TestCase):
    def test_diagonal_mixed_valuation_hierarchy(self) -> None:
        p, s, q = 3, 2, 9
        mod, zeta = coefficient_field(q)
        profiles = [(0, 0), (0, 1), (1, 1), (0, 2), (1, 2), (2, 2)]
        for vals in profiles:
            diagonal = [p**v if v < s else 0 for v in vals]
            op = diagonal_upper_shear(q, p, s, diagonal, mod, zeta)
            rows, cols = support_counts(op)
            stats = predicted_core_stats(p, s, vals)
            self.assertEqual(set(rows), {stats["row_support"]})
            self.assertEqual(set(cols), {stats["row_support"]})
            self.assertEqual(stats["block_count"] * stats["row_support"], q ** len(vals))

    def test_direct_gauss_kernel_equals_tensor_core(self) -> None:
        p, s, q = 3, 2, 9
        mod, zeta = coefficient_field(q)
        E = [[1, 0], [0, 3]]
        direct = direct_upper_shear_nd(q, E, mod, zeta)
        factored = diagonal_upper_shear(q, p, s, [1, 3], mod, zeta)
        self.assertEqual(direct, factored)

    def test_congruence_mixing_preserves_image_support(self) -> None:
        p, s, q = 3, 2, 9
        mod, zeta = coefficient_field(q)
        E = [[1, 0], [0, 3]]
        A = [[1, 1], [0, 1]]
        Ep = congruence_transform(E, A, q)
        op = direct_upper_shear_nd(q, Ep, mod, zeta)
        image_size = len(image_set(Ep, q))
        rows, cols = support_counts(op)
        self.assertEqual(set(rows), {image_size})
        self.assertEqual(set(cols), {image_size})
        self.assertTrue(all(q % o == 0 for o in sample_nonzero_cross_ratio_orders(op, mod, 400)))

    def test_dense_bruhat_and_sparse_support_dichotomy_field_case(self) -> None:
        p, s, q, n = 3, 1, 3, 2
        mod, zeta = coefficient_field(q)
        sym_id = identity(2 * n)
        op_id = identity(q**n)
        generators = []
        for C in ([[1, 1], [1, 2]], [[0, 1], [1, 1]]):
            generators.append((lower_shear_symplectic(C, q), lower_shear_operator(q, C, mod, zeta)))
        for A in ([[1, 1], [0, 1]], [[1, 0], [1, 1]], [[0, 1], [1, 0]]):
            generators.append((gl_symplectic(A, q), gl_operator(q, A, mod)))
        generators.append((full_weyl(n, q), full_fourier_operator(q, n, mod, zeta)))
        for idx in range(n):
            generators.append((coordinate_swap(n, [idx], q), partial_fourier_operator(q, n, [idx], mod, zeta)))

        rng = random.Random(2601)
        dense_seen = sparse_seen = 0
        for _ in range(30):
            smat, op = sym_id, op_id
            for _ in range(rng.randint(1, 5)):
                S, O = rng.choice(generators)
                smat = symplectic_multiply(S, smat, q)
                op = matmul(O, op, mod)
            _, B, _, D = split_blocks(smat)
            image_size = len(image_set(B, q))
            rows, _ = support_counts(op)
            self.assertEqual(set(rows), {image_size})
            if is_unit_det(B, q):
                dense_seen += 1
                predicted = representation_from_dense_bruhat(smat, q, mod, zeta)
                equal, _ = matrices_projectively_equal(op, predicted, mod)
                self.assertTrue(equal)
            else:
                sparse_seen += 1
                kernels = kernel_vectors(B, q)
                if len(kernels) > 1:
                    v = next(v for v in kernels if any(v))
                    pts = all_vectors(q, n)
                    for xi, x in enumerate(pts):
                        for yi, y in enumerate(pts):
                            if op[xi][yi]:
                                self.assertTrue(heisenberg_support_constraint(B, D, q, x, y, v))
        self.assertGreater(dense_seen, 0)
        self.assertGreater(sparse_seen, 0)

    def test_local_ring_partial_supports_in_general_words(self) -> None:
        p, s, q, n = 3, 2, 9, 2
        mod, zeta = coefficient_field(q)
        cases = [
            ([[3, 0], [0, 0]], 0),
            ([[3, 0], [0, 1]], 1),
            ([[3, 0], [0, 3]], 0),
            ([[1, 0], [0, 0]], 1),
            ([[3, 3], [3, 3]], 0),
        ]
        for B, expected_rank in cases:
            smat = upper_shear_symplectic(B, q)
            op = upper_shear_operator_nd(q, B, mod, zeta)
            image_size = len(image_set(B, q))
            rows, cols = support_counts(op)
            self.assertEqual(set(rows), {image_size})
            self.assertEqual(set(cols), {image_size})
            self.assertEqual(unit_rank(smat, p), expected_rank)

    def test_cross_ratio_exponent_obstruction(self) -> None:
        p, s, q, n = 3, 2, 9, 2
        mod, zeta = coefficient_field(q)
        tensor = full_fourier_operator(q, n, mod, zeta)
        orders = sample_nonzero_cross_ratio_orders(tensor, mod, 500)
        self.assertTrue(orders)
        self.assertTrue(all(q % o == 0 for o in orders))
        Q = q**n
        _, _, cyclic_order = cyclic_fourier_witness(Q)
        self.assertEqual(cyclic_order, Q)
        self.assertGreater(cyclic_order, q)

    def test_finite_abelian_group_exponent_gate(self) -> None:
        p = 3
        # Order p^6: only the cyclic partition (6) has exponent equal to group order.
        partitions = [(6,), (5, 1), (4, 2), (3, 3), (3, 2, 1), (2, 2, 2), (1, 1, 1, 1, 1, 1)]
        passing = [parts for parts in partitions if cyclic_equivalence_exponent_gate(p, parts)]
        self.assertEqual(passing, [(6,)])

    def test_mod_p_rank_budget_and_coordinate_fft(self) -> None:
        p, q, n = 3, 9, 3
        parts = [coordinate_swap(n, [i], q) for i in range(n)]
        product_s = identity(2 * n)
        total = 0
        for stage in parts:
            total += unit_rank(stage, p)
            product_s = symplectic_multiply(stage, product_s, q)
        self.assertEqual(product_s, full_weyl(n, q))
        self.assertEqual(total, n)
        self.assertEqual(unit_rank(full_weyl(n, q), p), n)
        # Subadditivity on all subset pairs.
        subsets = [[], [0], [1], [2], [0, 1], [0, 2], [1, 2], [0, 1, 2]]
        for a in subsets:
            for b in subsets:
                S, T = coordinate_swap(n, a, q), coordinate_swap(n, b, q)
                ST = symplectic_multiply(S, T, q)
                self.assertLessEqual(unit_rank(ST, p), unit_rank(S, p) + unit_rank(T, p))

    def test_operation_ledger_formula(self) -> None:
        p, s, n = 3, 4, 3
        Q = p ** (s * n)
        profiles = [(0, 0, 0), (0, 1, 4), (1, 2, 3), (3, 3, 4), (4, 4, 4)]
        for vals in profiles:
            cert = certificate_from_valuations(p, s, vals)
            expected_terms = p * Q * sum(s - v for v in vals)
            self.assertGreaterEqual(expected_terms, 0)
            self.assertEqual(cert.block_count * cert.row_support, cert.dimension)

    def test_predecessor_zip_integrity(self) -> None:
        path = os.path.join(ROOT, "PRIOR_v25_COMPLETE.zip")
        self.assertTrue(os.path.exists(path))
        with zipfile.ZipFile(path) as zf:
            self.assertEqual(zf.testzip(), None)
        with open(path, "rb") as fh:
            digest = hashlib.sha256(fh.read()).hexdigest()
        self.assertEqual(digest, "f8fbf4c58e95202665326bc7e66bc2da859502d38225a4d5ce3b42c043a00d15")


if __name__ == "__main__":
    unittest.main(verbosity=2)
