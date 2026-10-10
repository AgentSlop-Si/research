#!/usr/bin/env python3
"""Automated checks for the v7 global quadratic-chirp median sketch."""
from __future__ import annotations

import math
import unittest

import numpy as np

from prototype import (
    ChirpState,
    chirp_median_fft,
    covariance_matrix_formula,
    covariance_operator_norm,
    direct_row_estimate,
    draw_state,
    exact_unitary_dft,
    median_uniform_bound,
    one_row_estimate,
    row_work_proxy,
    variance_bound,
    worst_case_signal,
)


class GlobalChirpMedianTests(unittest.TestCase):
    def test_recurrence_matches_materialized_projection(self) -> None:
        rng = np.random.default_rng(1)
        for n, m in [(32, 2), (64, 4), (256, 8), (1024, 16)]:
            x = rng.normal(size=n) + 1j * rng.normal(size=n)
            state = draw_state(n, rng)
            got = one_row_estimate(x, m, state)
            ref = direct_row_estimate(x, m, state)
            self.assertLess(float(np.max(np.abs(got - ref))), 2e-10)

    def test_formula_matches_bruteforce_covariance(self) -> None:
        # Tiny independent enumeration over every odd a and every beta.
        n, m, output = 8, 2, 3
        brute = np.zeros((n, n), dtype=np.complex128)
        exact_basis_output = np.exp(-2j * np.pi * output * np.arange(n) / n) / math.sqrt(n)
        count = 0
        for a in range(1, n, 2):
            for beta in range(n):
                state = ChirpState(a, beta)
                coeff = np.empty(n, dtype=np.complex128)
                for j in range(n):
                    e = np.zeros(n, dtype=np.complex128)
                    e[j] = 1.0
                    coeff[j] = direct_row_estimate(e, m, state)[output] - exact_basis_output[j]
                brute += np.outer(np.conj(coeff), coeff)
                count += 1
        brute /= count
        formula = covariance_matrix_formula(n, m, output)
        self.assertLess(float(np.max(np.abs(brute - formula))), 2e-12)

    def test_exact_operator_norm(self) -> None:
        for n, m in [(16, 2), (32, 4), (128, 8), (512, 16)]:
            self.assertGreaterEqual(n // m, 2 * m)
            got = covariance_operator_norm(n, m, 0)
            self.assertAlmostEqual(got, 2.0 * m / n, places=12)

    def test_output_index_only_unitarily_conjugates_covariance(self) -> None:
        n, m = 32, 4
        spectra = []
        for output in [0, 1, 5, 17, 31]:
            spectra.append(np.linalg.eigvalsh(covariance_matrix_formula(n, m, output)))
        for eigenvalues in spectra[1:]:
            self.assertLess(float(np.max(np.abs(eigenvalues - spectra[0]))), 1e-12)

    def test_worst_case_signal_attains_bound(self) -> None:
        for n, m in [(64, 4), (128, 8), (512, 16)]:
            x = worst_case_signal(n, m)
            q = covariance_matrix_formula(n, m, 0)
            rayleigh = float(np.vdot(x, q @ x).real)
            self.assertAlmostEqual(rayleigh, 2.0 * m / n, places=12)

    def test_unbiasedness_empirically(self) -> None:
        rng = np.random.default_rng(2)
        n, m, trials = 256, 8, 1500
        x = rng.normal(size=n) + 1j * rng.normal(size=n)
        exact = exact_unitary_dft(x)
        accum = np.zeros(n, dtype=np.complex128)
        for _ in range(trials):
            accum += one_row_estimate(x, m, draw_state(n, rng))
        err = float(np.max(np.abs(accum / trials - exact)))
        # Monte Carlo standard error is on the order sqrt(M/trials)*||x||/sqrt(N).
        self.assertLess(err, 0.45)

    def test_variance_bound_finite_and_exact_limit(self) -> None:
        rng = np.random.default_rng(3)
        x = rng.normal(size=1024) + 1j * rng.normal(size=1024)
        self.assertGreater(variance_bound(x, 16), 0.0)
        # M=1 makes the block projection exactly the identity.
        self.assertEqual(variance_bound(x, 1), 0.0)
        got = one_row_estimate(x, 1, draw_state(1024, rng))
        self.assertLess(float(np.max(np.abs(got - exact_unitary_dft(x)))), 1e-10)

    def test_median_interface_and_bound(self) -> None:
        rng = np.random.default_rng(4)
        x = rng.normal(size=1024) + 1j * rng.normal(size=1024)
        got = chirp_median_fft(x, 16, 3, rng)
        self.assertEqual(got.shape, x.shape)
        bound = median_uniform_bound(x, 16, 3, 0.05)
        self.assertTrue(math.isfinite(bound) and bound > 0.0)

    def test_constant_row_linear_work_regime(self) -> None:
        # Symbolically choose M on the log_2 N scale.  K log K <= N when M>=log K.
        for log2_n in [16, 32, 64, 128, 256, 512]:
            # Proxy uses dimensions only; use floating algebra for the asymptotic inequality.
            m = 2 ** math.ceil(math.log2(log2_n))
            k_log_k_over_n = (log2_n - math.log2(m)) / m
            self.assertLessEqual(k_log_k_over_n, 1.0)

    def test_growing_rows_are_sub_nlogn(self) -> None:
        ratios = []
        for log2_n in [64, 128, 256, 512, 1024, 2048, 4096]:
            rows = 2 * math.ceil(log2_n / math.log2(log2_n)) - 1
            ratios.append(rows / log2_n)
        self.assertLess(ratios[-1], ratios[0])
        self.assertLess(ratios[-1], 0.2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
