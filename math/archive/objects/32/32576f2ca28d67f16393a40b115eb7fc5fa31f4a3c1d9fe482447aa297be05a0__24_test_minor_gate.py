import unittest
from minor_certificate import (
    MOD, rank_mod, stage, cut_bound, chosen_interval,
    fourier_minor, permutation, run_case
)


class ExactMinorGateTest(unittest.TestCase):
    def test_interval_selection_pigeonhole(self):
        for n in (16,32,64,128,256):
            for kind in ('identity','reverse','bitrev','random'):
                p=permutation(n,kind)
                m,s,c=chosen_interval(p)
                self.assertLessEqual(c,1)
                self.assertEqual(s%m,0)

    def test_stage_cut_ranks(self):
        for n,r in ((8,1),(16,2),(32,2),(64,3)):
            cut_bound(stage(n,r,seed=5),r)

    def test_fourier_vandermonde_full_rank(self):
        for n in (8,16,32,64,128,256):
            m=int(n**0.5)
            for s in (0,n//2,n-m):
                self.assertEqual(rank_mod(fourier_minor(n,m,s)),m)

    def test_exact_certificate_all_shuffles(self):
        for n,r in ((32,1),(64,2),(128,3)):
            for shuf in ('identity','reverse','bitrev','random'):
                result = run_case(n,r,r,shuf)
                self.assertTrue(result['theorem_rejects_all_permutations'])
                self.assertTrue(result['local_certificate_passed'])
                self.assertLess(result['rank_composed_minor'],result['rank_fourier_minor'])

    def test_asymmetric_channel_bound(self):
        for kind in ('identity','random'):
            result=run_case(64,r1=1,r2=2,shuffle=kind)
            self.assertLessEqual(result['rank_composed_minor'],2+2*1+1)
            self.assertEqual(result['rank_fourier_minor'],8)

    def test_arbitrary_nonunit_gains_between_stages(self):
        for shuffle in ('random','bitrev'):
            result = run_case(64,2,2,shuffle,weighted=True)
            self.assertLess(result['rank_composed_minor'],result['rank_fourier_minor'])

    def test_mod_rank_controls(self):
        self.assertEqual(rank_mod([[0,0],[0,0]]),0)
        self.assertEqual(rank_mod([[1,2],[2,4]]),1)
        self.assertEqual(rank_mod([[1,2],[2,5]]),2)


if __name__=='__main__':
    unittest.main()

class SuppliedGreenFamilyTest(unittest.TestCase):
    def test_concrete_two_green_stages(self):
        from green_sum_audit import actual_green_case
        for shuf in ('identity','reverse','bitrev','random'):
            result = actual_green_case(64, shuf)
            self.assertLess(result['rank_product'],result['rank_fourier'])
