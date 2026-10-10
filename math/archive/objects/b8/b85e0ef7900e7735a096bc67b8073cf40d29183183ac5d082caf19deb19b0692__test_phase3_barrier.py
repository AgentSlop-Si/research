import random
import unittest
from phase3_barrier import (
    choose_ntt_prime, ntt_root, direct_ntt, radix2_ntt, inverse_ntt,
    tabulate_butterfly, hadamard_matrix, rank_one_sign_sparse,
    apply_rank_one_sparse
)


class NTTTests(unittest.TestCase):
    def test_roots_exactly_requested_order(self):
        for n in (2,4,8,16,32,64,128):
            q=choose_ntt_prime(n)
            w=ntt_root(n,q)
            self.assertEqual(pow(w,n,q),1)
            self.assertNotEqual(pow(w,n//2,q),1)
            self.assertGreaterEqual(q,n+1)

    def test_direct_iterative_and_inverse_random(self):
        random.seed(7)
        for n in (2,4,8,16,32,64):
            q=choose_ntt_prime(n)
            w=ntt_root(n,q)
            for _ in range(3):
                a=[random.randrange(q) for j in range(n)]
                X=radix2_ntt(a,q,w)
                self.assertEqual(X,direct_ntt(a,q,w))
                self.assertEqual(inverse_ntt(X,q,w),a)

    def test_two_point_table(self):
        for q in (3,5,17):
            t=tabulate_butterfly(q)
            self.assertEqual(len(t),q*q)
            for a in range(q):
                for b in range(q):
                    self.assertEqual(t[a*q+b],((a+b)%q,(a-b)%q))

    def test_table_barrier(self):
        for n in (8,16,32,64,128,256,512):
            q=choose_ntt_prime(n)
            self.assertGreater(q*q, n*n)


class RankSparseTests(unittest.TestCase):
    def test_rank1_sign_sparse_wht_identity(self):
        random.seed(22)
        for n in (2,4,8):
            cert=rank_one_sign_sparse(n)
            H=hadamard_matrix(n)
            self.assertLess(cert['nonzero'], n*n)
            for _ in range(20):
                x=[random.randrange(3) for _ in range(n)]
                expected=[sum(row[j]*x[j] for j in range(n))%3 for row in H]
                self.assertEqual(apply_rank_one_sparse(cert,x),expected)

    def test_input_independent(self):
        cert=rank_one_sign_sparse(8)
        # Decomposition depends only on transform, not on x.
        self.assertEqual(cert['n'],8)
        self.assertEqual(len(cert['u']),8)
        self.assertEqual(len(cert['v']),8)
        self.assertEqual(len(cert['sparse']),cert['nonzero'])


if __name__ == '__main__':
    unittest.main()
