import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from galois_gate import (cycle_count_multiplier,cycle_count_formula,
                         field_automorphism_rank,phase_projective_rank,
                         all_orders_cyclotomic_coefficient,fourier_galois_diff_rank_mod,
                         stage_kind)
from spectral_gate import permutation_spectrum,phase_ratio_spectrum,invariant,cycle_lengths
from field_descent import P,Z8,cycles,exact_single_mask_factor
from conductor_tradeoff import explicit_sparse_galois_factor,cycle_count_formula as cycle_count_general
from two_mask_control import verify as verify_two_mask
from three_stage_probe import (control_fourier,candidate_rank_gates,
                               sparse_phase_rank_control)


class Phase14FieldTheoryTests(unittest.TestCase):
    def test_one_stage_spectral_proximity_rational_threshold(self):
        delta=129/512
        self.assertLess(delta,1-(1/2)**0.5)
        self.assertGreater((1-delta)**2,0.5)

    def test_exact_galois_orbit_count_formula(self):
        for m in range(4,15):
            n=1<<m
            self.assertEqual(cycle_count_multiplier(n),cycle_count_formula(n))
            self.assertEqual(field_automorphism_rank(n),n-4*m+4)

    def test_exact_primitive_eigenvalue_multiplicity(self):
        for n in (16,32,64,128,256,512,1024):
            L=n//8
            p=permutation_spectrum(n)
            self.assertEqual(p[1],4)
            self.assertEqual(sum(p.values()),n)
            self.assertEqual(sum(1 for d in cycle_lengths(n) if d==L),4)

    def test_polynomial_mask_spectral_obstruction(self):
        for n in (16,32,64,128,256,1024):
            for kind in ('linear','quadratic','cubic','quintic','large_coeff'):
                self.assertTrue(invariant(n,kind)['impossible_single_polynomial_mask_sandwich'])

    def test_phase_rank_examples(self):
        for n in (16,32,64,128,256,1024):
            self.assertEqual(phase_projective_rank(n,lambda j:j),n-8)
            self.assertLess(phase_projective_rank(n,lambda j:0),1)
        for n in (64,128,256,512,1024):
            self.assertLess(phase_projective_rank(n,lambda j:j*j),field_automorphism_rank(n))

    def test_exact_fourier_galois_rank_direct_matrix(self):
        for n in (16,32,64,128):
            self.assertEqual(fourier_galois_diff_rank_mod(n),field_automorphism_rank(n))

    def test_exact_nonbase_cyclotomic_coefficient_tree_and_haar(self):
        # Different stages and seeds; verifies genuine non-K certificate.
        for n in (16,32,64):
            for kind in ('tree','haar','strong'):
                d=all_orders_cyclotomic_coefficient(n,stage_kind(n,kind,seed=1414+n))
                self.assertTrue(d['cyclotomic_reconstruction_matches'])
                self.assertTrue(d['class_coefficient_nonzero'])
                self.assertEqual(d['class_residue'],1)


class Phase14FieldDescentTests(unittest.TestCase):
    def test_correct_extension_prime_roots(self):
        self.assertEqual((P-1)%8,0)
        self.assertNotEqual((P-1)%16,0)
        self.assertEqual((P-9)%512,0)
        self.assertEqual(pow(Z8,8,P),1)
        self.assertEqual(pow(Z8,4,P),P-1)

    def test_three_exact_constructive_countercontrols(self):
        for n in (16,32,64):
            a=exact_single_mask_factor(n)
            self.assertTrue(a['possible_over_zeta8'])
            self.assertTrue(a['all_A_rows_single_character'])
            self.assertTrue(a['all_fourier_entries_reconstructed'])
            self.assertEqual(a['A_base_field_coefficients'],n*n)

    def test_general_conductor_threshold_and_sparse_residual(self):
        for n,B in ((16,8),(32,8),(64,8),(128,16),(256,16),(256,32),(512,32),(1024,32)):
            d=explicit_sparse_galois_factor(n,B)
            self.assertTrue(d['one_mask_over_KB'])
            self.assertTrue(d['all_phase_exponents_verified'])
            self.assertEqual(d['cycles'],cycle_count_general(n,B))
            self.assertEqual(d['nonzero_residual_A'],n*d['cycles'])
        for n,B in ((128,8),(1024,16),(256,8)):
            self.assertFalse(explicit_sparse_galois_factor(n,B)['one_mask_over_KB'])

    def test_absolute_large_size_obstruction(self):
        for n in (128,256,512,1024):
            result=exact_single_mask_factor(n)
            self.assertFalse(result['possible_over_zeta8'])


class Phase14BlackBoxTests(unittest.TestCase):
    def test_two_mask_positive_exact_fourier(self):
        self.assertTrue(verify_two_mask(128,all_basis=True)['dense_input_direct_DFT_match'])
        self.assertTrue(verify_two_mask(256)['dense_input_direct_DFT_match'])
        self.assertTrue(verify_two_mask(512)['dense_input_direct_DFT_match'])

    def test_exact_true_fourier_control(self):
        for n in (16,32,64):
            c=control_fourier(n)
            self.assertTrue(c['covariance_zero'])
            self.assertTrue(c['galois_zero'])

    def test_sparse_phase_telescope(self):
        for n in (16,32,64):
            d=sparse_phase_rank_control(n)
            self.assertTrue(d['rank_budget_holds'])
            self.assertLessEqual(d['galois_difference_rank'],7)

    def test_exact_three_stage_failure_is_only_sampled(self):
        for n in (16,32,64):
            a=candidate_rank_gates(n,('tree','tree','tree'),('linear','quadratic'))
            b=candidate_rank_gates(n,('haar','haar','haar'),('quadratic','neg_quadratic'))
            for d in (a,b):
                self.assertEqual(d['covariance_rank'],n)
                self.assertGreater(d['galois_defect_rank'],0)

if __name__=='__main__':unittest.main()
