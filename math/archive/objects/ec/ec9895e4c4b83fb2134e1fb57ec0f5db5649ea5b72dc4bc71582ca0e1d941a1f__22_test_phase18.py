"""Phase 18 exact algebra and positive/negative control regression tests."""
import unittest
from harper_certificate import audit as harper_audit,components,reconstruct_polynomial,null_eigenvector,P
from commutant_dimension import audit as commutant_audit
from dual_intertwiner import control as dual_control,negative as dual_negative
from weyl_gate import audit as weyl_audit,positive_control
from spectral_basis_control import audit as spectral_control

class Phase18(unittest.TestCase):
    def test_fourier_parity_degree_N4(self):self.assertEqual(harper_audit(4)['odd_polynomial_degree'],0)
    def test_fourier_parity_degree_N8(self):self.assertEqual(harper_audit(8)['even_polynomial_degree'],4)
    def test_fourier_parity_degree_N16(self):self.assertEqual(harper_audit(16)['odd_polynomial_degree'],6)
    def test_fourier_parity_degree_N32(self):self.assertEqual(harper_audit(32)['even_polynomial_degree'],16)
    def test_fourier_parity_degree_N64(self):self.assertEqual(harper_audit(64)['odd_polynomial_degree'],30)
    def test_fourier_parity_degree_N128(self):self.assertEqual(harper_audit(128)['even_polynomial_degree'],64)
    def test_zero_modes_separate_eigenphase(self):
        for n in (8,16,32,64):
            e,o=components(n)
            _,le=null_eigenvector(e);_,lo=null_eigenvector(o)
            self.assertNotEqual(le,lo)
            self.assertEqual(le*le%P,1)
            self.assertEqual(lo*lo%P,P-1)
    def test_joint_commutant_N4(self):self.assertEqual(commutant_audit(4)['joint_commutant_dimension'],2)
    def test_joint_commutant_N8(self):self.assertEqual(commutant_audit(8)['joint_commutant_dimension'],2)
    def test_joint_commutant_N16(self):self.assertEqual(commutant_audit(16)['joint_commutant_dimension'],2)
    def test_joint_commutant_N32(self):self.assertEqual(commutant_audit(32)['joint_commutant_dimension'],2)
    def test_joint_commutant_N64(self):self.assertEqual(commutant_audit(64)['joint_commutant_dimension'],2)
    def test_dual_intertwiners_N8(self):self.assertTrue(dual_control(8)['one_probe_column_separates_Fourier'])
    def test_dual_intertwiners_N32(self):self.assertTrue(dual_control(32)['one_probe_column_separates_Fourier'])
    def test_dual_intertwiners_N128(self):self.assertTrue(dual_control(128)['one_probe_column_separates_Fourier'])
    def test_green_product_phase_obstruction_N8(self):self.assertTrue(weyl_audit(8)['all_permutations_and_diagonal_masks_excluded'])
    def test_green_product_phase_obstruction_N16(self):self.assertTrue(weyl_audit(16)['all_permutations_and_diagonal_masks_excluded'])
    def test_green_product_phase_obstruction_N32(self):self.assertTrue(weyl_audit(32)['all_permutations_and_diagonal_masks_excluded'])
    def test_green_product_phase_obstruction_N64(self):self.assertTrue(weyl_audit(64)['all_permutations_and_diagonal_masks_excluded'])
    def test_recover_nontrivial_phase_mask(self):
        for n in (8,16,32):self.assertTrue(positive_control(n)['recovered_mask_up_to_scalar'])
    def test_green_product_fails_dual_intertwiners(self):
        for n in (8,16,32):self.assertGreater(dual_negative(n)['green_sums_product_first_sparse_defect_nonzeros'],0)
    def test_real_spectral_four_phase_positive_control(self):
        for n in (8,16,32,64):self.assertLess(spectral_control(n)['max_abs_reconstruction_error'],1e-10)

if __name__=='__main__': unittest.main()
