#!/usr/bin/env python3
from __future__ import annotations

import math
import unittest

import numpy as np

import prototype as p
import unit_step_core as core


class OffsetClassJointTests(unittest.TestCase):
    def setUp(self) -> None:
        self.rng = np.random.default_rng(20261009)

    def test_class_count_formula(self) -> None:
        for n in range(2, 200):
            for prime in (2, 3, 5, 7):
                q = p.next_prime_power(n, prime)
                self.assertEqual(len(p.offset_classes(n, q)), n // math.gcd(n, q))

    def test_exact_modulation_identity(self) -> None:
        for n, prime in [(12, 2), (18, 3), (35, 5), (47, 2)]:
            q = p.next_prime_power(n, prime)
            x = self.rng.normal(size=n) + 1j * self.rng.normal(size=n)
            target = p.normalized_dft(x)
            selected, _, _ = p.exact_nearest_grid_map(n, q)
            for num, targets in p.offset_classes(n, q).items():
                padded = p.phase_modulated_padded_input(x, q, num)
                lifted = math.sqrt(q / n) * p.normalized_dft(padded)[selected[targets]]
                self.assertLess(np.max(np.abs(lifted - target[targets])), 2e-12)

    def test_exhaustive_unbiasedness_small(self) -> None:
        for n, prime in [(12, 2), (18, 3), (20, 2)]:
            q = p.next_prime_power(n, prime)
            block = p.choose_prime_power_block(q, prime)
            x = self.rng.normal(size=n) + 1j * self.rng.normal(size=n)
            rows = []
            for a in range(1, q):
                if math.gcd(a, q) != 1:
                    continue
                for beta in range(q):
                    rows.append(p.offset_class_row(x, prime, core.ChirpState(a, beta), block))
            mean = np.mean(np.asarray(rows), axis=0)
            self.assertLess(np.max(np.abs(mean - p.normalized_dft(x))), 5e-12)

    def test_exhaustive_variance_bound_small(self) -> None:
        for n, prime in [(12, 2), (18, 3), (20, 2)]:
            q = p.next_prime_power(n, prime)
            block = p.choose_prime_power_block(q, prime)
            x = self.rng.normal(size=n) + 1j * self.rng.normal(size=n)
            target = p.normalized_dft(x)
            rows = []
            for a in range(1, q):
                if math.gcd(a, q) != 1:
                    continue
                for beta in range(q):
                    rows.append(p.offset_class_row(x, prime, core.ChirpState(a, beta), block))
            variance = np.mean(np.abs(np.asarray(rows) - target[None, :]) ** 2, axis=0)
            self.assertLessEqual(
                np.max(variance),
                p.offset_class_variance_bound(x, prime, block) * (1 + 5e-12),
            )

    def test_batched_small_class_row_matches_streaming(self) -> None:
        for n, prime in [(48, 2), (80, 2), (45, 3)]:
            q = p.next_prime_power(n, prime)
            block = p.choose_prime_power_block(q, prime)
            state = core.draw_state(q, self.rng)
            x = self.rng.normal(size=n) + 1j * self.rng.normal(size=n)
            stream = p.offset_class_row(x, prime, state, block)
            batch = p.offset_class_row_batched(x, prime, state, block)
            self.assertLess(np.max(np.abs(stream - batch)), 3e-12)

    def test_reusable_plan_matches_core_for_even_and_odd_prime_powers(self) -> None:
        for q, block in [(64, 4), (81, 3)]:
            state = core.draw_state(q, self.rng)
            x = self.rng.normal(size=q) + 1j * self.rng.normal(size=q)
            plan = p.PrimePowerRowPlan.build(q, block, state)
            got = plan.apply(x)
            ref = core.one_row_estimate(x, block, state)
            self.assertLess(np.max(np.abs(got - ref)), 2e-12)

    def test_same_state_across_classes_is_valid(self) -> None:
        n, prime = 48, 2
        q = p.next_prime_power(n, prime)
        block = p.choose_prime_power_block(q, prime)
        x = self.rng.normal(size=n) + 1j * self.rng.normal(size=n)
        state = core.draw_state(q, self.rng)
        got = p.offset_class_row(x, prime, state, block)
        self.assertEqual(got.shape, (n,))
        self.assertTrue(np.all(np.isfinite(got)))

    def test_robust_seeded_error_inside_radius(self) -> None:
        n, prime = 48, 2
        q = p.next_prime_power(n, prime)
        block = p.choose_prime_power_block(q, prime)
        x = np.exp(2j * np.pi * self.rng.random(n))
        g = 3.0
        got = p.streaming_offset_class_fft(x, prime, 9, g, self.rng, block)
        err = np.max(np.abs(got - p.normalized_dft(x)))
        self.assertLess(err, p.robust_uniform_radius(x, block, g))

    def test_scan_fusion_rank_gate_exact(self) -> None:
        for n, rank in [(127, 8), (255, 10), (511, 12)]:
            cert = p.scan_fusion_rank_certificate(n, rank)
            self.assertEqual(cert["exact_chebyshev_rank"], rank)
            self.assertEqual(cert["state_dimension_lower_bound"], rank)

    def test_offset_repetition_caps_effective_rank(self) -> None:
        n = 3 * (1 << 8)
        q = p.next_prime_power(n, 2)
        self.assertEqual(p.offset_class_count(n, q), 3)
        with self.assertRaises(ValueError):
            p.scan_fusion_rank_certificate(n, 4, q)

    def test_adaptive_planner_uses_class_route_when_profitable(self) -> None:
        plan = p.choose_adaptive_plan(3 * (1 << 20))
        self.assertEqual(plan.method, "offset_classes")
        self.assertEqual(plan.prime, 2)
        self.assertEqual(plan.classes, 3)

    def test_adaptive_planner_retains_bessel_worst_case(self) -> None:
        plan = p.choose_adaptive_plan((1 << 24) - 1)
        self.assertEqual(plan.method, "bessel_rank")

    def test_linear_family_scaling_for_fixed_cofactor(self) -> None:
        ratios = []
        for exponent in [12, 16, 20, 24]:
            n = 3 * (1 << exponent)
            work = p.offset_class_work_proxy(n, 2)
            ratios.append(work / n)
        # Q/N and the number of classes stay bounded; only the conservative
        # FFT constant drifts mildly through the selected block size.
        self.assertLess(max(ratios), 4 * min(ratios))

    def test_zero_signal(self) -> None:
        n, prime = 48, 2
        q = p.next_prime_power(n, prime)
        block = p.choose_prime_power_block(q, prime)
        got = p.offset_class_row(
            np.zeros(n, dtype=np.complex128),
            prime,
            core.draw_state(q, self.rng),
            block,
        )
        self.assertTrue(np.all(got == 0))


if __name__ == "__main__":
    unittest.main(verbosity=2)
