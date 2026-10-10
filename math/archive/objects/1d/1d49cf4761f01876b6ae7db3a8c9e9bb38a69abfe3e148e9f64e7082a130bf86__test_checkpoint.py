#!/usr/bin/env python3
import math
import random
import unittest

from permutation_displacement import (
    cycles_of, predicted_rank, explicit_minimizer, theoretical_min_rank,
    exhaustive_minimum, d_minus_p_rank, fourier_displacement_rank, verify_random,
)
from measurement_transcript_gate import (
    transcript_certificate, adaptive_zero_path_certificate,
    separate_execution_lower_bound, shift_polynomial_gate,
    complete_local_fourier_measurements,
)
from permutation_displacement import rank_mod
from moment_state_gate import hankel_moment_rank, recurrence_polynomial_impossibility
from reversal_split import verify as verify_reversal_split


class PermutationDisplacementTests(unittest.TestCase):
    def test_cycle_formula_random(self):
        rng = random.Random(12345)
        for n in (5, 8, 11, 16, 25):
            perms = []
            for _ in range(8):
                p = list(range(n)); rng.shuffle(p); perms.append(tuple(p))
            verify_random(n, perms)

    def test_exhaustive_minima(self):
        for n in range(2, 10):
            rec = exhaustive_minimum(n)
            self.assertEqual(rec['minimum_rank'], n // 2)

    def test_explicit_minimizer(self):
        for n in range(2, 65):
            p = explicit_minimizer(n)
            self.assertEqual(predicted_rank(p), theoretical_min_rank(n))
            self.assertEqual(d_minus_p_rank(n, p), n // 2)

    def test_fourier_displacement_exact(self):
        for n in (7, 8, 12, 16, 25):
            p = explicit_minimizer(n)
            self.assertEqual(fourier_displacement_rank(n, p), n // 2)


class TranscriptTests(unittest.TestCase):
    def test_rank_upper_bound_and_witness(self):
        rec = transcript_certificate(32, [4] * 7)
        self.assertLessEqual(rec['rank'], 28)
        self.assertTrue(rec['has_common_kernel_witness'])
        self.assertTrue(rec['witness_dft_nonzero'])

    def test_overlapping_partitions_do_not_evade_dimension(self):
        rec = transcript_certificate(60, [15, 15, 15], shifts=[0, 7, 19])
        self.assertLessEqual(rec['rank'], 45)
        self.assertTrue(rec['has_common_kernel_witness'])

    def test_adaptive_zero_branch(self):
        rec = adaptive_zero_path_certificate(64, [8] * 7)
        self.assertTrue(rec['has_common_kernel_witness'])
        self.assertTrue(rec['witness_dft_nonzero'])

    def test_complete_local_frame_reaches_full_rank(self):
        p = 97  # 96 divisible by n=24 and m=4
        a = complete_local_fourier_measurements(24, 4, p)
        self.assertEqual(rank_mod(a, p), 24)

    def test_separate_execution_proxy(self):
        n = 2**20
        vals = [separate_execution_lower_bound(n, r) for r in range(1, 65)]
        best = min(vals, key=lambda x: x['lower_bound_proxy'])
        self.assertIn(best['rows'], (1, 2))
        self.assertGreaterEqual(best['lower_bound_proxy'], n * (math.log2(n) + 1) - 1e-7)

    def test_moment_state_rank(self):
        for n in (5, 7, 8, 9, 16, 25):
            self.assertEqual(hankel_moment_rank(n)['hankel_rank'], n)
            self.assertTrue(recurrence_polynomial_impossibility(n, n-1))

    def test_reversal_split_is_two_full_halves(self):
        for n in (7, 8, 9, 16, 25, 32):
            rec=verify_reversal_split(n)
            self.assertEqual(rec['combined_rank'], n)
            self.assertEqual(rec['kernel_transform_rank'], (n+1)//2)
            self.assertEqual(rec['complement_transform_rank'], n//2)
            self.assertLess(rec['max_cosine_formula_error'], 1e-10)
            self.assertLess(rec['max_sine_formula_error'], 1e-10)

    def test_shift_polynomial_collapse(self):
        for n in (8, 9, 16, 25):
            self.assertTrue(shift_polynomial_gate(n, [2, 3, 5, 7])['verified'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
