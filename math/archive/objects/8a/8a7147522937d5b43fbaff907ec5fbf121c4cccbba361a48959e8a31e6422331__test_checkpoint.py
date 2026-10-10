#!/usr/bin/env python3
"""Automated consistency tests for the v5 frequency-shift sketch checkpoint."""
from __future__ import annotations

import math
import unittest

import numpy as np

from prototype import (
    arithmetic_cost_proxy,
    balanced_bucket_per_bin_variance,
    balanced_bucket_sketch,
    direct_expansion_estimate,
    draw_randomness,
    exact_unitary_dft,
    frequency_shift_sketch,
    frequency_shift_sketch_with_state,
    median_frequency_shift_fft,
    median_uniform_bound,
    per_bin_variance,
)


class FrequencyShiftSketchTests(unittest.TestCase):
    def test_fast_evaluator_matches_direct_expansion(self) -> None:
        rng = np.random.default_rng(101)
        for k, m in [(5, 3), (8, 4), (12, 5)]:
            x = rng.normal(size=k * m) + 1j * rng.normal(size=k * m)
            state = draw_randomness(k, m, rng)
            fast = frequency_shift_sketch_with_state(x, m, state)
            direct = direct_expansion_estimate(x, m, state)
            self.assertLess(np.max(np.abs(fast - direct)), 1e-11)

    def test_m_equals_one_is_exact(self) -> None:
        rng = np.random.default_rng(102)
        x = rng.normal(size=128) + 1j * rng.normal(size=128)
        estimate = frequency_shift_sketch(x, 1, rng)
        exact = exact_unitary_dft(x)
        self.assertLess(np.max(np.abs(estimate - exact)), 1e-11)
        self.assertEqual(per_bin_variance(x, 1), 0.0)

    def test_variance_identity_empirically(self) -> None:
        rng = np.random.default_rng(103)
        k, m = 32, 8
        x = rng.normal(size=k * m) + 1j * rng.normal(size=k * m)
        exact = exact_unitary_dft(x)
        predicted = per_bin_variance(x, m)
        trials = 300
        observed = 0.0
        for _ in range(trials):
            error = frequency_shift_sketch(x, m, rng) - exact
            observed += float(np.mean(np.abs(error) ** 2))
        observed /= trials
        self.assertLess(abs(observed / predicted - 1.0), 0.08)

    def test_balanced_bucket_variance_and_exact_limit(self) -> None:
        rng = np.random.default_rng(106)
        k, m = 32, 8
        x = rng.normal(size=k * m) + 1j * rng.normal(size=k * m)
        exact = exact_unitary_dft(x)

        # One column per bucket has no collisions and is algebraically exact.
        no_collision = balanced_bucket_sketch(x, m, m, rng)
        self.assertLess(np.max(np.abs(no_collision - exact)), 1e-11)
        self.assertEqual(balanced_bucket_per_bin_variance(x, m, m), 0.0)

        # A nontrivial collision size follows the exact variance formula.
        bucket_count = 2
        predicted = balanced_bucket_per_bin_variance(x, m, bucket_count)
        trials = 300
        observed = 0.0
        for _ in range(trials):
            err = balanced_bucket_sketch(x, m, bucket_count, rng) - exact
            observed += float(np.mean(np.abs(err) ** 2))
        observed /= trials
        self.assertLess(abs(observed / predicted - 1.0), 0.08)

    def test_median_interface_and_finite_bound(self) -> None:
        rng = np.random.default_rng(104)
        x = rng.normal(size=512) + 1j * rng.normal(size=512)
        estimate = median_frequency_shift_fft(x, 8, 5, rng)
        self.assertEqual(estimate.shape, x.shape)
        bound = median_uniform_bound(x, 8, 5, 0.05)
        self.assertTrue(math.isfinite(bound) and bound > 0.0)

    def test_sub_fft_cost_regimes(self) -> None:
        # For powers of two N, choose power-of-two M near log N or log log N.
        # The normalized cost must trend to zero along both regimes.
        ratios_fast = []
        ratios_trade = []
        for log2_n in [32, 64, 128, 256, 512, 1024]:
            m_fast = 1 << int(math.floor(math.log2(log2_n)))
            m_trade = 1 << max(1, int(math.floor(math.log2(math.log2(log2_n)))))
            # Divide the proxy by N before evaluating, avoiding gigantic integers.
            fast_per_n = 1.0 + math.log2(m_fast) + (log2_n - math.log2(m_fast)) / m_fast
            trade_per_n = 1.0 + math.log2(m_trade) + (log2_n - math.log2(m_trade)) / m_trade
            ratios_fast.append(fast_per_n / log2_n)
            ratios_trade.append(trade_per_n / log2_n)
        self.assertLess(ratios_fast[-1], ratios_fast[0])
        self.assertLess(ratios_trade[-1], ratios_trade[0])
        self.assertLess(ratios_fast[-1], 0.03)
        self.assertLess(ratios_trade[-1], 0.2)

    def test_rows_must_be_odd(self) -> None:
        rng = np.random.default_rng(105)
        x = np.ones(64, dtype=np.complex128)
        with self.assertRaises(ValueError):
            median_frequency_shift_fft(x, 8, 4, rng)


if __name__ == "__main__":
    unittest.main(verbosity=2)
