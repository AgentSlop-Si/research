#!/usr/bin/env python3
"""Automated consistency tests for predecode-median v6."""
from __future__ import annotations

import math
import unittest

import numpy as np

from prototype import (
    build_compressed_rows,
    compressed_memory_proxy,
    decode_local_spectra,
    draw_randomness,
    exact_local_spectra,
    exact_unitary_dft,
    local_estimate_from_row,
    local_sparse_failure_bound,
    local_variance_vector,
    make_local_sparse_signal,
    one_row_full_estimate,
    postdecode_cost_proxy,
    predecode_cost_proxy,
    predecode_median_fft,
    predecode_median_from_compressed,
    predecode_median_uniform_bound,
    simulate_tone_moments,
    tone_moment_theory,
    unitary_ifft,
)


class PredecodeMedianTests(unittest.TestCase):
    def test_exact_local_decoder(self) -> None:
        rng = np.random.default_rng(1)
        for k, m in [(7, 3), (16, 8), (31, 5)]:
            x = rng.normal(size=k * m) + 1j * rng.normal(size=k * m)
            got = decode_local_spectra(exact_local_spectra(x, m))
            ref = exact_unitary_dft(x)
            self.assertLess(float(np.max(np.abs(got - ref))), 1e-11)

    def test_one_row_deferred_path(self) -> None:
        from prototype import compress_one_row

        rng = np.random.default_rng(2)
        k, m = 32, 8
        x = rng.normal(size=k * m) + 1j * rng.normal(size=k * m)
        state = draw_randomness(k, m, rng)
        direct = one_row_full_estimate(x, m, state)
        matched = decode_local_spectra(
            local_estimate_from_row(compress_one_row(x, m, state), state)
        )
        self.assertLess(float(np.max(np.abs(direct - matched))), 1e-12)

    def test_local_variance_identity(self) -> None:
        from prototype import compress_one_row

        rng = np.random.default_rng(3)
        k, m = 48, 8
        x = rng.normal(size=k * m) + 1j * rng.normal(size=k * m)
        ref = exact_local_spectra(x, m)
        predicted = local_variance_vector(x, m)
        observed = np.zeros(m)
        trials = 400
        for _ in range(trials):
            state = draw_randomness(k, m, rng)
            est = local_estimate_from_row(compress_one_row(x, m, state), state)
            observed += np.mean(np.abs(est - ref) ** 2, axis=0)
        observed /= trials
        self.assertLess(float(np.max(np.abs(observed / predicted - 1.0))), 0.12)

    def test_exhaustive_small_local_variance(self) -> None:
        from itertools import product
        from prototype import SketchRandomness, compress_one_row

        k, m = 3, 2
        x = np.asarray([1+2j, -1+0.5j, 0.25-0.75j, 2-1j, -0.5+0.25j, 1.5+0j])
        ref = exact_local_spectra(x, m)
        accum = np.zeros((k, m), dtype=float)
        count = 0
        roots = [1.0, -1.0, 1.0j, -1.0j]
        for q in product(range(k), repeat=m):
            for phases in product(roots, repeat=m):
                state = SketchRandomness(
                    shifts=np.asarray(q, dtype=np.int64),
                    phases=np.asarray(phases, dtype=np.complex128),
                )
                est = local_estimate_from_row(compress_one_row(x, m, state), state)
                accum += np.abs(est - ref) ** 2
                count += 1
        exact_average = accum / count
        predicted = np.broadcast_to(local_variance_vector(x, m), (k, m))
        self.assertLess(float(np.max(np.abs(exact_average - predicted))), 1e-12)

    def test_m_equals_one_is_exact(self) -> None:
        rng = np.random.default_rng(4)
        x = rng.normal(size=128) + 1j * rng.normal(size=128)
        got = predecode_median_fft(x, 1, 5, rng)
        self.assertLess(float(np.max(np.abs(got - exact_unitary_dft(x)))), 1e-11)

    def test_compressed_interface_and_bound(self) -> None:
        rng = np.random.default_rng(5)
        x = rng.normal(size=512) + 1j * rng.normal(size=512)
        rows = build_compressed_rows(x, 8, 5, rng)
        got = predecode_median_from_compressed(rows)
        self.assertEqual(got.shape, x.shape)
        bound = predecode_median_uniform_bound(x, 8, 5, 0.05)
        self.assertTrue(math.isfinite(bound) and bound > 0.0)

    def test_local_sparse_exact_recovery(self) -> None:
        rng = np.random.default_rng(6)
        k, m, h = 2048, 8, 1
        x, a = make_local_sparse_signal(k, m, h, rng)
        # Construction really has h local Fourier entries per column.
        recovered_a = exact_local_spectra(x, m)
        self.assertLess(float(np.max(np.abs(recovered_a - a))), 1e-11)
        got = predecode_median_fft(x, m, 7, rng)
        self.assertLess(float(np.max(np.abs(got - exact_unitary_dft(x)))), 1e-10)
        self.assertLess(local_sparse_failure_bound(k * m, m, 7, h), 0.01)

    def test_tone_fourth_moment_formula(self) -> None:
        theory = tone_moment_theory(256, 16)
        self.assertAlmostEqual(theory["kurtosis"], theory["closed_form_kurtosis"], places=12)
        empirical = simulate_tone_moments(256, 16, 80000, np.random.default_rng(7))
        self.assertLess(abs(empirical["empirical_kurtosis"] / theory["kurtosis"] - 1.0), 0.08)

    def test_deferred_decoder_cost_and_memory(self) -> None:
        n, m, rows = 1 << 20, 32, 101
        self.assertLess(predecode_cost_proxy(n, m, rows), postdecode_cost_proxy(n, m, rows))
        # Store compressed K-spectra rather than R full N-vectors.
        self.assertLess(compressed_memory_proxy(n, m, rows), 5 * n)

    def test_asymptotic_ratio_decreases(self) -> None:
        ratios = []
        memory = []
        for l in [64, 128, 256, 512, 1024, 2048, 4096]:
            ll = math.log2(l)
            rows = int(math.ceil(l / ll)) | 1
            m = 1 << int(math.floor(math.log2(l)))
            per_n = rows * (2.0 + (l - math.log2(m)) / m) + math.log2(m)
            ratios.append(per_n / l)
            # N itself is symbolic; R*K/N = R/M.
            memory.append(1.0 + rows / m)
        self.assertLess(ratios[-1], ratios[0])
        self.assertLess(memory[-1], 2.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
