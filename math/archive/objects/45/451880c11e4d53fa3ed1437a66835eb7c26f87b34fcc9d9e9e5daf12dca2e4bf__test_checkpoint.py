from __future__ import annotations

import random
import unittest

from finite_field import field_for_length, mat_vec, matrix_inverse
from krylov_gate import (
    cycle_denominator,
    directed_diameter,
    max_outdegree,
    minimal_inverse_polynomial_degree,
    multishift_denominator,
    support_radius_gate,
)
from weyl_packet import (
    affine_fourier_minor,
    character_packet_apply,
    green_apply_cycle,
    green_matrix,
    literal_character_packet_apply,
    literal_weighted_packet_matrix,
    noncommutator_witness,
    packet_fiber_minor,
    weighted_packet_matrix,
)


class WeylPacketTests(unittest.TestCase):
    def _params(self, n: int):
        p, omega = field_for_length(n)
        alpha = 2
        while pow(alpha, n, p) == 1:
            alpha += 1
        return p, omega, alpha

    def test_green_cycle_matches_dense_inverse(self):
        rng = random.Random(2001)
        for n in (5, 7, 11, 13):
            p, omega, alpha = self._params(n)
            for h in (1, 2):
                for r in range(min(n, 5)):
                    x = [rng.randrange(p) for _ in range(n)]
                    dense = mat_vec(green_matrix(n, p, omega, alpha, r, h), x, p)
                    fast = green_apply_cycle(x, p, omega, alpha, r, h)
                    self.assertEqual(dense, fast)

    def test_character_packet_identity(self):
        rng = random.Random(2002)
        for n in (5, 7, 11, 13, 17):
            p, omega, alpha = self._params(n)
            x = [rng.randrange(p) for _ in range(n)]
            for h in (1, 2):
                for s in range(n):
                    self.assertEqual(
                        character_packet_apply(x, p, omega, alpha, s, h),
                        literal_character_packet_apply(x, p, omega, alpha, s, h),
                    )

    def test_character_packet_linear_sparsity(self):
        for n in (5, 7, 11, 17):
            p, omega, alpha = self._params(n)
            for s in range(n):
                cols = []
                for j in range(n):
                    e = [0] * n
                    e[j] = 1
                    cols.append(character_packet_apply(e, p, omega, alpha, s))
                nonzero = sum(v != 0 for col in cols for v in col)
                self.assertEqual(nonzero, 2 * n - 1 if s == 0 else n - 1)

    def test_weighted_packet_entry_formula(self):
        rng = random.Random(2003)
        for n in (5, 7, 11, 13):
            p, omega, alpha = self._params(n)
            for h in (1, 2):
                weights = [rng.randrange(p) for _ in range(n)]
                self.assertEqual(
                    weighted_packet_matrix(weights, p, omega, alpha, h),
                    literal_weighted_packet_matrix(weights, p, omega, alpha, h),
                )

    def test_packet_fiber_minor_gate(self):
        rng = random.Random(2004)
        for n in (5, 7, 11, 13, 17, 19):
            p, omega, alpha = self._params(n)
            weights = [rng.randrange(p) for _ in range(n)]
            for h in (1, 2):
                det, indices = packet_fiber_minor(weights, p, omega, alpha, h)
                self.assertEqual(det, 0)
                # Independent affine row/column reorderings of Fourier preserve nonzero 2x2 minor.
                fdet = affine_fourier_minor(
                    n,
                    p,
                    omega,
                    indices,
                    row_slope=2 % n,
                    row_shift=1,
                    col_slope=3 % n if n != 3 else 1,
                    col_shift=2,
                )
                self.assertNotEqual(fdet, 0)

    def test_weyl_orders_are_projectively_noncommuting(self):
        for n in (5, 7, 11, 17):
            p, omega, _ = self._params(n)
            for h in (1, 2):
                lam = noncommutator_witness(n, p, omega, 1, 3 % n, h)
                self.assertNotEqual(lam, 1)


class KrylovGateTests(unittest.TestCase):
    def test_cycle_green_krylov_degree(self):
        p = 1009
        for n in (5, 7, 9, 11, 13):
            alpha = 2
            while pow(alpha, n, p) == 1:
                alpha += 1
            a = cycle_denominator(n, p, alpha)
            inverse = matrix_inverse(a, p)
            info = support_radius_gate(a, inverse)
            degree = minimal_inverse_polynomial_degree(a, p)
            self.assertTrue(info["dense_inverse"])
            self.assertEqual(info["directed_diameter"], n - 1)
            self.assertEqual(degree, n - 1)
            self.assertGreaterEqual(degree, info["directed_diameter"])

    def test_multigraph_krylov_distance_gate(self):
        p = 1009
        cases = [
            (7, [1, 3], [2, 5]),
            (11, [1, 3], [2, 5]),
            (13, [1, 2], [3, 7]),
            (17, [1, 4], [2, 9]),
        ]
        for n, shifts, weights in cases:
            a = multishift_denominator(n, p, shifts, weights)
            inverse = matrix_inverse(a, p)
            info = support_radius_gate(a, inverse)
            degree = minimal_inverse_polynomial_degree(a, p)
            self.assertTrue(info["dense_inverse"])
            self.assertGreaterEqual(degree, info["directed_diameter"])
            self.assertGreaterEqual(degree, info["size_lower_bound"])
            self.assertEqual(info["max_outdegree"], len(shifts) + 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
