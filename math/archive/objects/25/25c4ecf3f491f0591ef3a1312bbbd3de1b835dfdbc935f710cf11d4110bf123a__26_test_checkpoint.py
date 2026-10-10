#!/usr/bin/env python3
from __future__ import annotations

import math
import unittest
import numpy as np

import arbitrary_block_core as core
import covariance as cov
import exact_field_certificate as field_cert
from prototype import analytic_covariance


class TestV14(unittest.TestCase):
    def test_balanced_partition(self):
        for n in range(7, 100):
            for b in range(3, min(n, 15) + 1):
                starts, lengths, ends = core.balanced_partition(n, b)
                self.assertEqual(int(lengths.sum()), n)
                self.assertLessEqual(int(lengths.max()) - int(lengths.min()), 1)
                self.assertEqual(int(starts[0]), 0)
                self.assertEqual(int(ends[-1]), n)

    def test_exponential_recurrence(self):
        rng = np.random.default_rng(7)
        for n in [17, 31, 64, 97, 127]:
            for b in [3, 4, 7, 11]:
                starts, _, _ = core.balanced_partition(n, b)
                nodes = np.exp(-2j * np.pi * starts / n)
                weights = rng.normal(size=(2, b)) + 1j * rng.normal(size=(2, b))
                got = core.exponential_sequences_recurrence(nodes, weights, n)
                ref = core.exponential_sequences_direct(nodes, weights, n)
                self.assertLess(np.max(np.abs(got - ref)), 1e-8)

    def test_decoder_against_materialization(self):
        rng = np.random.default_rng(11)
        for n in [17, 31, 61, 97, 127]:
            for b in [3, 5, 7, 11]:
                state = core.draw_state(n, rng)
                x = rng.normal(size=n) + 1j * rng.normal(size=n)
                got = core.one_row_estimate(x, b, state, "recurrence")
                ref = core.reference_row(x, b, state)
                self.assertLess(np.max(np.abs(got - ref)), 5e-8)

    def test_direct_and_recurrence_forcing_agree(self):
        rng = np.random.default_rng(12)
        for n, b in [(29, 4), (60, 7), (101, 9), (257, 16)]:
            state = core.draw_state(n, rng)
            x = rng.normal(size=n) + 1j * rng.normal(size=n)
            a = core.one_row_estimate(x, b, state, "direct")
            c = core.one_row_estimate(x, b, state, "recurrence")
            self.assertLess(np.max(np.abs(a - c)), 5e-8)

    def test_covariance_bound(self):
        for n in [17, 19, 23, 30, 35, 42]:
            for b in [3, 4, 5]:
                q = analytic_covariance(n, b)
                actual = np.linalg.eigvalsh(q).max().real
                _, lengths, _ = core.balanced_partition(n, b)
                bound = float(cov.overlap_variance_factor_lengths(n, lengths))
                self.assertLessEqual(actual, bound + 2e-12)

    def test_overlap_improves_triangle(self):
        for n in [17, 30, 35, 42, 60]:
            for b in [3, 4, 5, 7]:
                _, lengths, _ = core.balanced_partition(n, b)
                new = cov.overlap_variance_factor_lengths(n, lengths)
                old = cov.old_triangle_variance_factor(n, int(lengths.max()))
                self.assertLessEqual(new, old)

    def test_prime_closed_form(self):
        for n in [17, 19, 23, 29, 31, 101, 1009]:
            for b in [3, 4, 7, 11]:
                if b > n:
                    continue
                got = cov.balanced_overlap_variance_factor(n, b)
                ref = cov.prime_balanced_closed_form(n, b)
                self.assertEqual(got, ref)

    def test_least_prime_factor_half_constant(self):
        for n in [15, 21, 35, 55, 77, 143, 221]:
            p, ref = cov.least_prime_equal_block_closed_form(n)
            got = cov.equal_block_overlap_variance_factor(n, p)
            self.assertEqual(got, ref)

    def test_exact_field_certificate(self):
        rows = field_cert.run_suite()
        self.assertGreaterEqual(len(rows), 20)
        self.assertTrue(all(row["passed"] for row in rows))

    def test_bulk_fraction_bound(self):
        self.assertAlmostEqual(cov.bulk_bad_fraction_expectation_bound(0.01, 0.5), 0.04)

    def test_variance_only_amplification_cost_conservation(self):
        # For prime N and B growing, the certified row count times log B is
        # asymptotically comparable to log N.  Check representative values.
        for n in [1009, 10007, 100003]:
            for b in [math.ceil(math.log2(n)), math.ceil(math.sqrt(n))]:
                v = float(cov.prime_balanced_closed_form(n, b))
                rows = cov.variance_only_rows_for_union(n, v, 1.0, 0.1)
                if rows > 0:
                    self.assertGreater(rows * math.log2(max(2, b)), 0.2 * math.log2(n))


if __name__ == "__main__":
    unittest.main(verbosity=2)
