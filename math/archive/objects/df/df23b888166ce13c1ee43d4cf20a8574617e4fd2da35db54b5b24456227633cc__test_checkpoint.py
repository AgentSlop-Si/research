#!/usr/bin/env python3
from __future__ import annotations

import math
import unittest

import numpy as np

from projector_certificate import certify_case
from composite_modulus_audit import covariance as composite_covariance

from prototype import (
    ChirpState,
    balanced_exclusive_scan,
    compress_blocks,
    covariance_matrix_formula,
    covariance_projector_spectrum,
    decode_balanced_scan,
    decode_sequential,
    direct_row_estimate,
    draw_state,
    exact_arithmetic_uniform_bound,
    finite_precision_row_bound,
    finite_precision_uniform_bound,
    majority_failure_bound,
    one_row_estimate,
    prime_power,
    required_rows,
    sufficient_mantissa_bits,
    unit_character_mean_prime_power,
    unitary_fft,
    validate_dimensions,
    worst_case_signal,
)


class UnitStepChirpTests(unittest.TestCase):
    def test_prime_power_validation(self) -> None:
        self.assertEqual(prime_power(1024), (2, 10))
        self.assertEqual(prime_power(729), (3, 6))
        self.assertEqual(prime_power(625), (5, 4))
        with self.assertRaises(ValueError):
            prime_power(12)
        self.assertEqual(validate_dimensions(256, 8), (2, 32, 8))
        self.assertEqual(validate_dimensions(729, 9), (3, 81, 9))

    def test_balanced_scan(self) -> None:
        rng = np.random.default_rng(1)
        for n in [1, 2, 3, 8, 31, 64, 257]:
            x = rng.normal(size=n) + 1j * rng.normal(size=n)
            got = balanced_exclusive_scan(x)
            ref = np.concatenate([[0.0 + 0.0j], np.cumsum(x)[:-1]])
            self.assertLess(float(np.max(np.abs(got - ref))), 3e-12)

    def test_decoder_matches_materialized_projection(self) -> None:
        rng = np.random.default_rng(2)
        for n, m in [(64, 4), (81, 3), (125, 5), (256, 8), (729, 9)]:
            for _ in range(3):
                x = rng.normal(size=n) + 1j * rng.normal(size=n)
                state = draw_state(n, rng)
                d = compress_blocks(x, m, state)
                ref = direct_row_estimate(x, m, state)
                bal = decode_balanced_scan(d, n, m, state)
                seq = decode_sequential(d, n, m, state)
                self.assertLess(float(np.max(np.abs(bal - ref))), 3e-10)
                self.assertLess(float(np.max(np.abs(seq - ref))), 3e-10)

    def test_unit_character_identity(self) -> None:
        for n in [8, 9, 25, 27]:
            p, _ = prime_power(n)
            units = [a for a in range(n) if math.gcd(a, n) == 1]
            zeta = np.exp(2j * np.pi / n)
            for c in range(n):
                empirical = sum(zeta ** (a * c) for a in units) / len(units)
                theory = unit_character_mean_prime_power(n, c)
                self.assertLess(abs(empirical - theory), 2e-12)

    def test_exhaustive_covariance_small(self) -> None:
        # Exhaustively enumerate every unit a and every beta and compare the
        # resulting output-0 covariance with the closed formula.
        for n, m in [(8, 2), (9, 3)]:
            units = [a for a in range(1, n) if math.gcd(a, n) == 1]
            q = np.zeros((n, n), dtype=np.complex128)
            eye = np.eye(n, dtype=np.complex128)
            exact = unitary_fft(eye[:, 0])  # only used for shape/convention
            del exact
            for a in units:
                for beta in range(n):
                    state = ChirpState(a, beta)
                    h = np.empty(n, dtype=np.complex128)
                    for j in range(n):
                        row = direct_row_estimate(eye[:, j], m, state)
                        h[j] = row[0] - 1.0 / math.sqrt(n)
                    q += np.outer(np.conj(h), h)
            q /= len(units) * n
            ref = covariance_matrix_formula(n, m, 0)
            self.assertLess(float(np.max(np.abs(q - ref))), 3e-12)

    def test_covariance_is_scaled_projector(self) -> None:
        for n, m in [(16, 2), (16, 4), (27, 3), (81, 9), (125, 5)]:
            q = covariance_matrix_formula(n, m)
            eig = np.linalg.eigvalsh(q)
            zero_mult, nonzero_mult, lam = covariance_projector_spectrum(n, m)
            self.assertEqual(zero_mult + nonzero_mult, n)
            self.assertLess(float(np.max(np.abs(eig[:zero_mult]))), 2e-11)
            self.assertLess(float(np.max(np.abs(eig[zero_mult:] - lam))), 2e-11)
            self.assertLess(float(np.linalg.norm(q @ q - lam * q)), 2e-10)
            self.assertAlmostEqual(float(np.trace(q).real), m - 1, places=10)

    def test_output_covariance_spectrum_invariant(self) -> None:
        n, m = 81, 9
        ref = np.linalg.eigvalsh(covariance_matrix_formula(n, m, 0))
        for output in [1, 2, 17, 80]:
            got = np.linalg.eigvalsh(covariance_matrix_formula(n, m, output))
            self.assertLess(float(np.max(np.abs(got - ref))), 2e-11)

    def test_explicit_extremizer(self) -> None:
        for n, m in [(64, 4), (81, 3), (125, 5)]:
            q = covariance_matrix_formula(n, m)
            x = worst_case_signal(n, m)
            value = float(np.vdot(x, q @ x).real)
            self.assertAlmostEqual(value, m / n, places=11)

    def test_unbiasedness_empirical(self) -> None:
        rng = np.random.default_rng(3)
        n, m = 81, 3
        x = rng.normal(size=n) + 1j * rng.normal(size=n)
        target = unitary_fft(x)
        acc = np.zeros(n, dtype=np.complex128)
        trials = 3000
        for _ in range(trials):
            acc += one_row_estimate(x, m, draw_state(n, rng))
        # Monte Carlo tolerance is deliberately loose; exact unbiasedness is
        # proved algebraically and the exhaustive covariance test is stronger.
        self.assertLess(float(np.max(np.abs(acc / trials - target))), 0.18 * np.linalg.norm(x))

    def test_finite_precision_bridge(self) -> None:
        rng = np.random.default_rng(4)
        x = rng.normal(size=4096) + 1j * rng.normal(size=4096)
        m, g = 16, 4.0
        u = np.finfo(np.float32).eps / 2
        eta = finite_precision_row_bound(x, m, u)
        exact = exact_arithmetic_uniform_bound(x, m, g)
        inflated = finite_precision_uniform_bound(x, m, g, u)
        self.assertGreater(eta, 0.0)
        self.assertGreater(inflated, exact)
        bits = sufficient_mantissa_bits(2**30, g)
        self.assertLess(bits, 64)
        self.assertGreater(bits, 30)



    def test_seed_from_cycle_closure_all_prime_powers(self) -> None:
        rng = np.random.default_rng(2026)
        for n, m in [(64, 4), (81, 3), (125, 5), (256, 8), (729, 9)]:
            x = rng.normal(size=n) + 1j * rng.normal(size=n)
            state = draw_state(n, rng)
            d = compress_blocks(x, m, state)
            d_fft = np.fft.fft(d)
            from prototype import _cycle_arrays, pairwise_sum, seed_value
            _, gauge, terms = _cycle_arrays(d_fft, n, m, state)
            closure_seed = pairwise_sum(terms) / 2.0
            direct_seed = seed_value(d, n, m, state)
            self.assertLess(abs(closure_seed - direct_seed), 2e-10)
            # A_N/A_0 is the omitted endpoint of the gauge cycle and equals -1.
            h = n & 1
            endpoint_phase_2n = (2 * (state.a * (n * (n - 1) // 2) + state.beta * n) + h * n) % (2*n)
            endpoint = np.exp(1j * np.pi * endpoint_phase_2n / n)
            self.assertLess(abs(endpoint + 1), 2e-12)

    def test_exact_combinatorial_certificate(self) -> None:
        for p, ell, mu in [(2, 12, 5), (3, 8, 4), (5, 6, 3), (7, 4, 2)]:
            record = certify_case(p, ell, mu)
            self.assertEqual(record["nonzero_multiplicity"], record["N"] - record["K"])
            self.assertEqual(record["trace"], f"{record['M'] - 1}/1")

    def test_composite_projector_shortcut_is_false(self) -> None:
        n, m = 12, 3
        eig = np.linalg.eigvalsh(composite_covariance(n, m))
        positive = eig[eig > 1e-10]
        self.assertGreater(float(positive.max()), m / n + 0.1)
        self.assertGreater(float(positive.max() - positive.min()), 0.2)

    def test_probability_and_asymptotics(self) -> None:
        n, g, delta = 2**20, 4.0, 1e-3
        rows = required_rows(n, g, delta)
        self.assertEqual(rows % 2, 1)
        self.assertLessEqual(majority_failure_bound(n, rows, g), delta)
        # One row is linear when M is a power of p comparable to log N.
        for n, m in [(2**24, 32), (3**15, 27), (5**10, 25)]:
            _, k, _ = validate_dimensions(n, m)
            ratio = (n + k * math.log2(k)) / (n * math.log2(n))
            self.assertLess(ratio, 0.2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
