#!/usr/bin/env python3
from __future__ import annotations

import math
import unittest

import numpy as np
from scipy.special import jv

import v11_fused_reference as p
import unit_step_core as core


class FusedAllLengthTests(unittest.TestCase):
    def setUp(self) -> None:
        self.rng = np.random.default_rng(20261009)

    def test_exact_nearest_grid_map(self) -> None:
        for n in range(2, 300):
            q = p.next_power_of_two(n)
            idx, num, theta = p.exact_nearest_grid_map(n, q)
            self.assertEqual(np.unique(idx).size, n)
            self.assertTrue(np.all(2 * np.abs(num) <= n))
            for k in range(n):
                self.assertEqual(int(idx[k]), math.floor(k * q / n + 0.5))
                self.assertLess(abs(theta[k] - (k * q / n - idx[k])), 1e-12)

    def test_selected_decoder_matches_full(self) -> None:
        for q, block in [(64, 4), (128, 8), (256, 8)]:
            state = core.draw_state(q, self.rng)
            k = q // block
            d = self.rng.normal(size=k) + 1j * self.rng.normal(size=k)
            selected = np.sort(self.rng.choice(q, q // 2, replace=False))
            plan = p.SelectedDecoderPlan.build(q, block, state, selected)
            got = plan.decode_selected(d)
            ref = core.decode_balanced_scan(d, q, block, state)[selected]
            self.assertLess(np.max(np.abs(got - ref)), 1e-12)

    def test_streamed_clenshaw_matches_v10_reference(self) -> None:
        for n in [31, 61, 97, 127, 257]:
            q = p.next_power_of_two(n)
            block = p.choose_dyadic_block(q)
            x = self.rng.normal(size=n) + 1j * self.rng.normal(size=n)
            state = core.draw_state(q, self.rng)
            ref = p.reference_bessel_chirp_row(x, 10, block, state)
            got = p.streamed_bessel_chirp_row(x, 10, block, state)
            self.assertLess(np.max(np.abs(ref - got)), 5e-12)

    def test_neumann_addition_tail_bound_pointwise(self) -> None:
        for halfwidth in [0, 1, 2]:
            for _ in range(300):
                z = float(self.rng.uniform(0.0, math.pi))
                delta = float(self.rng.uniform(0.0, 0.2))
                r = int(self.rng.integers(0, 15))
                approx = sum(
                    jv(r - h, z) * jv(h, delta)
                    for h in range(-halfwidth, halfwidth + 1)
                )
                err = abs(jv(r, z + delta) - approx)
                self.assertLessEqual(
                    err,
                    p.small_argument_bessel_tail(delta, halfwidth) * (1 + 2e-13),
                )

    def test_addition_center_bound(self) -> None:
        for n in [31, 61, 127, 257]:
            q = p.next_power_of_two(n)
            block = p.choose_dyadic_block(q)
            x = self.rng.normal(size=n) + 1j * self.rng.normal(size=n)
            rank = 10
            ref = p.exact_truncated_lift(x, rank)
            for halfwidth in [0, 1]:
                got = p.exact_lift_with_addition_fusion(x, rank, block, halfwidth)
                bound = (
                    p.addition_kernel_error_bound(n, rank, block, halfwidth)
                    * np.linalg.norm(x)
                )
                self.assertLessEqual(np.max(np.abs(got - ref)), bound * (1 + 1e-11))

    def test_halfwidth_zero_is_asymptotically_negligible(self) -> None:
        alpha = 1 / 3
        ratios = []
        for exp in [20, 30, 40, 60, 80, 120]:
            n = (1 << exp) - 1
            q = 1 << exp
            block = p.choose_dyadic_block(q)
            rank = p.bessel_rank_for_tail(n ** (-alpha))
            extra = p.addition_kernel_error_bound(n, rank, block, 0)
            ratios.append(extra / n ** (-alpha))
        self.assertLess(ratios[-1], ratios[0])
        self.assertLess(ratios[-1], 1e-15)

    def test_fused_variance_bound_seeded(self) -> None:
        n = 61
        q = p.next_power_of_two(n)
        block = p.choose_dyadic_block(q)
        rank = 10
        x = np.exp(2j * np.pi * self.rng.random(n))
        center = p.exact_lift_with_addition_fusion(x, rank, block, 0)
        rows = []
        for _ in range(250):
            rows.append(
                p.fused_addition_bessel_chirp_row(
                    x, rank, block, core.draw_state(q, self.rng), 0
                )
            )
        empirical = np.mean(np.abs(np.asarray(rows) - center[None, :]) ** 2, axis=0)
        bound = p.fused_one_row_variance_bound(x, rank, block, 0)
        self.assertLess(np.max(empirical), bound)

    def test_streaming_fused_end_to_end_bound(self) -> None:
        n = 61
        rank = 10
        rows = 9
        g = (2.0 * n * math.comb(rows, (rows + 1) // 2) / 0.1) ** (
            1.0 / (rows + 1)
        )
        x = np.exp(2j * np.pi * self.rng.random(n))
        got = p.streaming_fused_all_length_fft(x, rank, rows, g, self.rng, 0)
        ref = p.normalized_dft(x)
        err = np.max(np.abs(got - ref))
        self.assertLess(err, p.fused_total_uniform_error_bound(x, rank, g, 0))

    def test_finite_precision_model_dominates_stress(self) -> None:
        n = 257
        q = p.next_power_of_two(n)
        block = p.choose_dyadic_block(q)
        x = self.rng.normal(size=n) + 1j * self.rng.normal(size=n)
        state = core.draw_state(q, self.rng)
        for rank in [4, 8, 12]:
            ref = p.streamed_bessel_chirp_row(x, rank, block, state, np.complex128)
            got = p.streamed_bessel_chirp_row(x, rank, block, state, np.complex64)
            err = np.max(np.abs(got - ref))
            u = np.finfo(np.float32).eps / 2
            self.assertLess(err, p.finite_precision_lift_bound(x, rank, block, u))

    def test_bit_budget_has_theta_log_n_growth(self) -> None:
        vals = []
        for exp in [20, 40, 80, 120]:
            n = (1 << exp) - 1
            block = p.choose_dyadic_block(1 << exp)
            rank = p.bessel_rank_for_tail(n ** (-1 / 3))
            bits = p.sufficient_mantissa_bits(n, rank, block, n ** (1 / 6))
            vals.append(bits / exp)
        self.assertTrue(all(0.8 < v < 2.0 for v in vals))
        self.assertLess(vals[-1], vals[0])

    def test_allocation_model_removes_rank_times_n_storage(self) -> None:
        model = p.allocation_model((1 << 30) - 1, 9, 16, 0)
        self.assertEqual(model["v11_rank_dependent_full_length_scalars"], 0)
        self.assertEqual(model["v10_chebyshev_full_length_scalars"], 9 * ((1 << 30) - 1))
        self.assertLess(model["v11_local_channel_scalars"], 1 << 30)

    def test_fusion_input_work_is_o_rank_n(self) -> None:
        ratios = []
        for exp in [20, 40, 80, 120]:
            n = (1 << exp) - 1
            q = 1 << exp
            block = p.choose_dyadic_block(q)
            rank = p.bessel_rank_for_tail(n ** (-1 / 3))
            old = rank * q
            new = q + rank * (q // block)
            ratios.append(new / old)
        self.assertLess(ratios[-1], ratios[0])
        self.assertLess(ratios[-1], 0.1)

    def test_zero_signal(self) -> None:
        n = 127
        q = p.next_power_of_two(n)
        block = p.choose_dyadic_block(q)
        state = core.draw_state(q, self.rng)
        got = p.fused_addition_bessel_chirp_row(
            np.zeros(n, dtype=np.complex128), 10, block, state, 0
        )
        self.assertTrue(np.all(got == 0))


if __name__ == "__main__":
    unittest.main(verbosity=2)
