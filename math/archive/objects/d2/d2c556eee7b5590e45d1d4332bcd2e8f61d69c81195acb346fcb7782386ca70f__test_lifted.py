import unittest
from random import Random
from cut_capacity import random_green,rank_mod,fourier_mod
from lifted_sandwich_gate import block_matrix,direct_product,rank_identity

class LiftedTests(unittest.TestCase):
    def test_rank_identity_for_random_fourier_targets(self):
        for n,r,s in [(4,2,2),(8,2,3),(8,3,2),(16,2,2)]:
            rng=Random(n*107+r*7+s)
            A=[random_green(n,rng,zero_prob=.2) for _ in range(r)]
            B=[random_green(n,rng,zero_prob=.2) for _ in range(s)]
            a=rank_identity(A,B)
            self.assertFalse(a['factorization_success'])

    def test_exact_positive_factorization_for_constructed_target(self):
        for n,r,s in [(4,1,1),(4,2,2),(8,3,2)]:
            rng=Random(101*n+r*7+s)
            A=[random_green(n,rng,zero_prob=.2) for _ in range(r)]
            B=[random_green(n,rng,zero_prob=.2) for _ in range(s)]
            exact_target=direct_product(A,B)
            H=block_matrix(A,B,exact_target)
            base=(r+s)*n
            self.assertEqual(rank_mod(H),base)
            exact_target[1][2]=(exact_target[1][2]+1)%65537
            self.assertEqual(rank_mod(block_matrix(A,B,exact_target)),base+1)

    def test_singular_resolvent_not_certified(self):
        from cut_capacity import GreenGraph,exact_green
        with self.assertRaises(ValueError):
            exact_green(GreenGraph([1,0],[1,1]))

if __name__=='__main__':unittest.main()
