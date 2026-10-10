"""Regression tests for the new window-rank research. Run: python -m unittest -v test_window_gate."""
import unittest
from window_gate import (old_bilateral_required_rank_sum, check_windows,
                         combinatorial_ceiling, enumerate_n8,
                         inequalities_for_window)
from finite_field_audit import (ct_endpoint_control, row_permuted_fourier_tests,
                                affine_input_tests, random_positive_controls)

class TestWindowGate(unittest.TestCase):
    def test_exhaustive_n8(self):
        report=enumerate_n8()
        self.assertEqual(report['number_of_permutations'],40320)
        self.assertEqual(report['old_only_survivors'],28584)
        self.assertEqual(report['survived_both'],15728)
        self.assertEqual(report['rejected_new_beyond_old'],12856)
        self.assertEqual(report['new_pass_old_fail'],0)

    def test_identity_witness_n8(self):
        p=list(range(8))
        self.assertLessEqual(old_bilateral_required_rank_sum(p),2)
        v=inequalities_for_window(p,0,2)
        self.assertEqual(v[1]['type'],'tail')
        self.assertEqual((v[1]['required'],v[1]['budget']),(3,2))
        self.assertTrue(check_windows(p))

    def test_combinatorial_ceiling(self):
        self.assertEqual(combinatorial_ceiling(1,1,1,1)['necessary_maximum_n'],21)
        self.assertEqual(combinatorial_ceiling(2,2,2,2)['necessary_maximum_n'],57)
        self.assertEqual(combinatorial_ceiling(3,3,3,3)['necessary_maximum_n'],111)
        self.assertEqual(combinatorial_ceiling(4,4,4,4)['necessary_maximum_n'],183)
        self.assertEqual(combinatorial_ceiling(0,1,0,1)['maximum_length_by_tail'],13)

    def test_N16_surviving_necessary_screen(self):
        p=[8,0,13,4,9,3,15,5,6,1,12,11,10,2,14,7]
        self.assertEqual(old_bilateral_required_rank_sum(p),1)
        self.assertEqual(check_windows(p),[])

    def test_ct_exact_factorization_no_false_rejection(self):
        v=ct_endpoint_control()
        self.assertEqual([x['n'] for x in v],[8,16])
        self.assertTrue(all(x['stage_qs_ranks']==[1,1] for x in v))
        self.assertTrue(all(x['corrected_gate_lower']==2 for x in v))
        self.assertTrue(all(x['naive_gate_lower']==3 for x in v))
        self.assertTrue(all(x['actual_endpoint_reordered_rank']+1==x['naive_vandermonde_rank'] for x in v))

    def test_output_permuted_fourier_vandermonde_exact(self):
        counts=row_permuted_fourier_tests()
        self.assertEqual(len(counts),8)
        self.assertEqual(sum(x['rank_checks'] for x in counts),64)

    def test_affine_input_and_any_output_permutations(self):
        counts=affine_input_tests()
        self.assertEqual(len(counts),8)
        self.assertEqual(sum(x['tests'] for x in counts),128)

    def test_structured_positive_controls_general_rank(self):
        self.assertEqual(random_positive_controls(),3096)

if __name__=='__main__':unittest.main(verbosity=2)
