import unittest
import random
from wide_scan import *

class MulticutTests(unittest.TestCase):
    def test_fourier_potential(self):
        for n in (4,8,16,32):
            self.assertEqual(cut_rank_potential(dft(n)),n*n//2)
    def test_scan_potential(self):
        for n in (4,8,16):
            x=forward([3]*n,[2]*n)
            y=backward([7]*n,[5]*n)
            self.assertEqual(cut_rank_potential(x),n-1)
            self.assertEqual(cut_rank_potential(y),n-1)
    def test_permutation_footrule(self):
        for n in (4,8,16,32):
            for order in (bit_reverse_order(n),parity_order(n),gray_order(n),list(reversed(range(n)))):
                self.assertEqual(cut_rank_potential(permutation_matrix(order)),footrule(order))
    def test_multichannel_cut_bounds(self):
        for n in (4,8,16):
            for rf,rb in ((0,1),(1,0),(1,2),(2,3)):
                m=multichannel(n,rf,rb,101)
                for cut in range(1,n):
                    up,lo=offdiag_ranks(m,cut)
                    self.assertLessEqual(up,rb)
                    self.assertLessEqual(lo,rf)
    def test_subadditive_product(self):
        for n in (4,8,16):
            a=multichannel(n,1,1,111)
            b=multichannel(n,2,1,222)
            c=matmul(a,b)
            self.assertLessEqual(cut_rank_potential(c),cut_rank_potential(a)+cut_rank_potential(b))
    def test_any_endpoint_reorder_balanced(self):
        for n in (4,8,16):
            rng=random.Random(n)
            m=dft(n)
            for _ in range(32):
                r=list(range(n));c=list(range(n))
                rng.shuffle(r);rng.shuffle(c)
                ur,lr=offdiag_ranks(permute(m,r,c),n//2)
                self.assertGreaterEqual(ur,n//4)
                self.assertGreaterEqual(lr,n//4)
                self.assertGreaterEqual(cut_rank_potential(permute(m,r,c)),(n*n-1)//3)
    def test_exact_all_4900(self):
        result=independent_balanced_bound_check()
        self.assertEqual(result['pairs'],4900)
        self.assertEqual(result['min_excess_over_bound'],0)

if __name__=='__main__':unittest.main()

class RoutingTests(unittest.TestCase):
    def test_shuffled_cut_budget(self):
        from routing_budget import cut_budget_experiment
        result=cut_budget_experiment(16,12)
        self.assertEqual(result['violations'],0)
        self.assertEqual(result['randomized_factorizations_checked'],96)
    def test_bitrev_cut_crossing(self):
        for n in (8,16,32,64):
            self.assertEqual(crossing_count(bit_reverse_order(n),n//2),n//4)
    def test_parity_optimal_rank_lower_bound(self):
        for n in (8,16,32,64):
            self.assertEqual(offdiag_ranks(permute(dft(n),parity_order(n),parity_order(n)),n//2),(n//4,n//4))
