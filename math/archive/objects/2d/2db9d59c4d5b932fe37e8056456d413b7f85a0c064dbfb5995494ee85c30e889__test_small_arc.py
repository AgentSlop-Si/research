"""Independent checks of the all-length small-arc and cyclotomic-degree gates."""
import unittest
from small_arc_gate import (top_left_fourier_full_minors_threshold,
                            green_sum_no_go_threshold,numerical_audit,
                            three_minor_schur_lower_bound)
from independent_exact_gate import full_minors_by_degree,euler_phi
from power_two_witness import compute_witness

class AllLengthGates(unittest.TestCase):
    def test_exact_2300_threshold(self):
        self.assertEqual(top_left_fourier_full_minors_threshold(26,3),2300)
        self.assertEqual(green_sum_no_go_threshold(2)['smallest_excluded_N'],2301)
        self.assertEqual(green_sum_no_go_threshold(3)['smallest_excluded_N'],34545589)

    def test_arbitrary_row_sparse_correction(self):
        # 2 Green sums + one nonzero per row may not equal F_N for N>15872.
        self.assertEqual(green_sum_no_go_threshold(2,sparse_row_degree=1)['all_N_strict_threshold'],15872)
        self.assertEqual(green_sum_no_go_threshold(2,rank_correction=1)['required_minor_size'],4)

    def test_independent_cyclotomic_gate_at_pow2(self):
        self.assertEqual(euler_phi(4096),2048)
        gate=full_minors_by_degree(4096,26,3)
        self.assertEqual(gate['max_formal_degree'],1875)
        self.assertTrue(gate['all_minors_proved_nonzero'])
        self.assertFalse(full_minors_by_degree(2301,26,3)['all_minors_proved_nonzero'])

    def test_independent_high_precision_bounds(self):
        for n in [2301,4096,8192]:
            audit=numerical_audit(n,samples=30)
            self.assertGreaterEqual(audit['min_measured_over_analytical_lower_bound'],0.999999999)

    def test_phase13_two_layer_block_gate(self):
        from two_layer_polynomial_gate import cert
        for n in [4,8,16]:
            witness=cert(n)
            self.assertTrue(witness['schur_equivalence_checked'])
            self.assertEqual(witness['factorization_success'],witness['block_rank_gate_passes'])
            self.assertFalse(witness['factorization_success'])
            self.assertEqual(witness['block_polynomial_matrix_rank'],2*n)

    def test_fully_modular_powers_of_two(self):
        w=compute_witness(4096)
        self.assertEqual(w['sum_green_rank'],2)
        self.assertEqual(w['dft_rank'],3)
        self.assertNotEqual(w['dft_minor'],0)

if __name__=='__main__':
    unittest.main(verbosity=2)
