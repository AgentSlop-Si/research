import copy
from fractions import Fraction as Q
import unittest
import experiment as e
from verify_results import replay


class ExactExperimentTests(unittest.TestCase):
    def test_smallest_exact_and_exhaustive(self):
        r,a=e.run_case(4,2,0,True)
        self.assertEqual(r['baseline_add_sub'],16)
        self.assertEqual(r['pair_partition_enumeration']['assignments_examined'],6561)
        self.assertEqual(r['pair_partition_enumeration']['minimum_pairs'],8)
        self.assertEqual(r['dirty_lift']['complete_word_shears'],160)
        self.assertEqual(r['dirty_lift']['scratch_roles'],24)

    def test_twiddle_negative_exponent(self):
        self.assertEqual(e.monomial_refs([(0,1),(1,1)],-1),[(1,1),(0,-1)])

    def test_forbidden_cancellation_rejected(self):
        d=e.DAG(2)
        with self.assertRaises(AssertionError):
            d.add((0,1),(0,-1))

    def test_truncation_is_not_linear(self):
        c=e.rounding_counterexample()
        self.assertNotEqual(c['staged_rounded_outputs_in_grid_units'],
                            c['fused_once_rounded_outputs_in_grid_units'])

    def test_missing_cleanup_is_detected(self):
        r,a=e.run_case(4,2)
        dim=r['dirty_lift']['full_state_dimension']
        correct=replay(a['baseline_word'],dim)
        bad=replay(a['baseline_word'][:-1],dim)
        self.assertNotEqual(bad,correct)

    def test_wrong_injection_sign_is_detected(self):
        r,a=e.run_case(4,2)
        dim=r['dirty_lift']['full_state_dimension']
        word=copy.deepcopy(a['baseline_word'])
        index=next(i for i,g in enumerate(word) if g[3] in ('1/4','-1/4'))
        word[index][3]=str(-Q(word[index][3]))
        self.assertNotEqual(replay(word,dim),replay(a['baseline_word'],dim))

    def test_signed_repeated_output_invalidates_lower_bound(self):
        row={0:Q(1),1:Q(1),2:Q(1),3:Q(1)}
        cert,_=e.lower_bound_certificate([row,row])
        self.assertIsNone(cert['cancellation_free_addition_lower_bound'])


if __name__=='__main__':
    unittest.main()
