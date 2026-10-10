"""Finite-field regression tests for Phase 11 theorem."""
import unittest
import numpy as np
from phase11_gate import *

class TestPhase11(unittest.TestCase):
    def test_roots_and_fourier_inverse(self):
        for n in [2,4,8,16,32,64]:
            f=fourier(n)
            inv=fourier(n,inverse=True)
            self.assertTrue(np.array_equal(matmul(f,inv),eye(n)))

    def test_vandermonde_certificate(self):
        rng=np.random.default_rng(1101)
        for n in [8,16,32,64]:
            f=fourier(n,inverse=True)
            for s in [1,2,3,4]:
                for j in range(5):
                    sparse=random_row_sparse(n,s,rng)
                    cert=rank_witness(f,sparse)
                    self.assertEqual(cert['minor_rank'],n//(s+1))
                    if n<=32:
                        self.assertGreaterEqual(mod_rank((f-sparse)%P),cert['minor_rank'])

    def test_arbitrary_endpoint_permutations(self):
        rng=np.random.default_rng(1202)
        n=32
        f=fourier(n,inverse=True)
        rowpi=rng.permutation(n)
        colpi=rng.permutation(n)
        t=f[np.ix_(rowpi,colpi)]
        for s in [1,2,4,7]:
            sparse=random_row_sparse(n,s,rng)
            c=rank_witness(t,sparse,original_row_order=rowpi)
            self.assertEqual(c['minor_rank'],n//(s+1))

    def test_product_sparse_plus_rank(self):
        for n,l in [(16,2),(32,2),(64,3),(128,4)]:
            for seed in range(3):
                res=factor_audit(n,l,rank_per_layer=1,seed=seed)
                self.assertTrue(res['forbidden_by_theorem'])
                self.assertLessEqual(res['correction_rank'],l)

    def test_pure_inverse_sparse(self):
        for n,l in [(16,2),(32,3),(64,4)]:
            res=factor_audit(n,l,rank_per_layer=0,seed=42)
            self.assertTrue(res['forbidden_by_theorem'])
            self.assertEqual(res['correction_rank'],0)

    def test_green_plus_rank_woodbury_scope(self):
        rng=np.random.default_rng(1323)
        for n in [4,8,16]:
            for r in [1,2]:
                s=green_inverse_sparse(n,rng)
                g=mod_inverse(s)
                u=rng.integers(0,P,size=(n,r),dtype=np.int64)
                v=rng.integers(0,P,size=(r,n),dtype=np.int64)
                t=(g+matmul(u,v))%P
                inv=mod_inverse(t)
                self.assertLessEqual(mod_rank((inv-s)%P),r)

    def test_not_stronger_n_minus_s(self):
        f=fourier(4)
        e=np.tile(np.array([1,1,P-1,P-1],dtype=np.int64),(4,1))
        s=(f-e)%P
        self.assertEqual(mod_rank(e),1)
        self.assertTrue(np.array_equal(np.count_nonzero(s,axis=1),np.full(4,2)))
        self.assertEqual(mod_rank((f-s)%P),1)

    def test_high_schmidt_rank_sparse_inverse_permutation(self):
        a=4
        swap=swap_permutation(a)
        self.assertEqual(mod_rank(matrix_realignment(swap,a,a)),a*a)
        self.assertEqual(int(np.count_nonzero(swap,axis=1).max()),1)
        self.assertTrue(np.array_equal(matmul(swap,swap),eye(a*a)))

    def test_sum_of_two_green_escape(self):
        for n in [8,16,32]:
            res=green_sum_escape(n,seed=77)
            self.assertNotIn('failure_to_find_dense_inverse',res)
            self.assertEqual(min(res['inverse_nnz_per_row']),n)

if __name__=='__main__': unittest.main(verbosity=2)
