#!/usr/bin/env python3
from __future__ import annotations

import math
import unittest

import numpy as np

import prototype as v10
import unit_step_core as core


class AllLengthLiftTests(unittest.TestCase):
    def setUp(self) -> None:
        self.rng = np.random.default_rng(20261009)

    def test_nearest_grid_is_injective_and_close(self) -> None:
        for n in range(2, 200):
            q = v10.next_power_of_two(n)
            j, theta = v10.nearest_grid_map(n, q)
            self.assertEqual(np.unique(j).size, n)
            self.assertLessEqual(float(np.max(np.abs(theta))), 0.5 + 1e-12)

    def test_bessel_lift_matches_independent_kernel(self) -> None:
        for n in [7, 10, 15, 17, 31]:
            x = self.rng.normal(size=n) + 1j * self.rng.normal(size=n)
            a = v10.lifted_exact_bessel(x, 10)
            b = v10.lifted_direct_bessel_kernel(x, 10)
            self.assertLess(float(np.max(np.abs(a - b))), 1e-11)

    def test_taylor_lift_matches_independent_kernel(self) -> None:
        for n in [7, 15, 23]:
            x = self.rng.normal(size=n) + 1j * self.rng.normal(size=n)
            a = v10.lifted_exact_taylor(x, 12)
            b = v10.lifted_direct_kernel(x, 12)
            self.assertLess(float(np.max(np.abs(a - b))), 1e-11)

    def test_bessel_tail_controls_actual_kernel(self) -> None:
        for rank in [6, 8, 10, 12]:
            tail = v10.bessel_tail_bound(rank)
            s = np.linspace(0.0, 1.0, 129)
            theta = np.linspace(-0.5, 0.5, 131)
            ss, tt = np.meshgrid(s, theta, indexing="ij")
            x = 2.0 * tt
            vals = v10._chebyshev_values(x, rank)
            approx = np.zeros_like(ss, dtype=np.complex128)
            from scipy.special import jv
            for r in range(rank):
                coeff = 1.0 if r == 0 else 2.0 * ((-1j) ** r)
                approx += coeff * jv(r, math.pi * ss) * vals[r]
            exact = np.exp(-2j * math.pi * ss * tt)
            self.assertLessEqual(float(np.max(np.abs(approx - exact))), tail * (1 + 1e-10))

    def test_deterministic_truncation_bound(self) -> None:
        for n in [7, 15, 17, 31, 61]:
            for x in v10.make_cases(n, self.rng).values():
                rank = 10
                got = v10.lifted_exact_bessel(x, rank)
                ref = v10.normalized_dft(x)
                err = float(np.max(np.abs(got - ref)))
                bound = v10.deterministic_lift_error_bound(x, rank)
                self.assertLessEqual(err, bound * (1 + 1e-10))

    def test_exact_enumerated_unbiasedness(self) -> None:
        n = 7
        q = v10.next_power_of_two(n)
        block = v10.choose_dyadic_block(q)
        rank = 8
        x = self.rng.normal(size=n) + 1j * self.rng.normal(size=n)
        rows = []
        for a in range(1, q):
            if math.gcd(a, q) != 1:
                continue
            for beta in range(q):
                rows.append(v10.lifted_bessel_chirp_row(x, rank, block, core.ChirpState(a, beta)))
        mean = np.mean(rows, axis=0)
        center = v10.lifted_exact_bessel(x, rank)
        self.assertLess(float(np.max(np.abs(mean - center))), 2e-12)

    def test_exact_enumerated_variance_bound(self) -> None:
        n = 7
        q = v10.next_power_of_two(n)
        block = v10.choose_dyadic_block(q)
        rank = 8
        x = self.rng.normal(size=n) + 1j * self.rng.normal(size=n)
        center = v10.lifted_exact_bessel(x, rank)
        rows = []
        for a in range(1, q):
            if math.gcd(a, q) != 1:
                continue
            for beta in range(q):
                rows.append(v10.lifted_bessel_chirp_row(x, rank, block, core.ChirpState(a, beta)))
        var = np.mean(np.abs(np.asarray(rows) - center[None, :]) ** 2, axis=0)
        bound = v10.one_row_variance_bound(x, rank, block)
        self.assertLessEqual(float(np.max(var)), bound * (1 + 1e-10))

    def test_streaming_bound_seeded(self) -> None:
        n = 61
        x = self.rng.normal(size=n) + 1j * self.rng.normal(size=n)
        rank = 12
        rows = 9
        g = v10.fixed_row_g(n, rows, 0.1)
        got = v10.streaming_all_length_fft(x, rank, rows, g, self.rng)
        ref = v10.normalized_dft(x)
        err = float(np.max(np.abs(got - ref)))
        self.assertLessEqual(err, v10.total_uniform_error_bound(x, rank, g))

    def test_fixed_accuracy_linear_regime(self) -> None:
        # Formal large-N accounting; no large allocation occurs.
        n = (1 << 80) - 59
        eps = 0.1
        rank = v10.bessel_rank_for_tail(eps / 2)
        self.assertLessEqual(v10.bessel_tail_bound(rank), eps / 2)
        q = v10.next_power_of_two(n)
        block = v10.choose_dyadic_block(q)
        tail = v10.bessel_tail_bound(rank)
        g = eps * math.sqrt(n / block) / (5.0 * math.sqrt(2.0) * (1.0 + tail))
        self.assertGreater(g, math.sqrt(2.0))
        failure = v10.fixed_row_failure_bound(n, 3, g)
        self.assertLess(failure, 1e-6)
        self.assertLess(rank, 20)  # independent of N for fixed epsilon

    def test_shrinking_error_sub_nlogn_regime(self) -> None:
        n = (1 << 120) - 1
        rows = 5
        a = 0.0
        s = (rows + 1) // 2
        alpha = 0.5 - (1.0 + a) / (2.0 * s)
        rank = v10.asymptotic_rank(n, alpha, 0.08)
        self.assertLessEqual(v10.bessel_tail_bound(rank), n ** (-(alpha + 0.08)))
        ratio = rows * v10.row_work_proxy(n, rank) / (n * math.log2(n))
        # Finite proxy is already below a modest constant and asymptotically ->0.
        self.assertLess(ratio, 4.0)

    def test_rank_has_log_over_loglog_growth(self) -> None:
        alpha = 1 / 3
        ratios = []
        for exp in [40, 80, 160, 320]:
            n = (1 << exp) - 1
            rank = v10.asymptotic_rank(n, alpha, 0.05)
            ratios.append(rank / (math.log(n) / math.log(math.log(n))))
        self.assertLess(max(ratios), 1.5)

    def test_zero_signal(self) -> None:
        x = np.zeros(31, dtype=np.complex128)
        got = v10.streaming_all_length_fft(x, 8, 3, 3.0, self.rng)
        self.assertTrue(np.array_equal(got, x))


if __name__ == "__main__":
    unittest.main(verbosity=2)
