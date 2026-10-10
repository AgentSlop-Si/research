import unittest
import numpy as np
from phase11_gate import *
from green_sum_linear import WeightedPermutationGreen, TwoGreenSum, find_weighted_escape, find_escape_layer

class EscapeTests(unittest.TestCase):
    def test_weighted_cycle_linear_executor_matches_dense_matrix(self):
        rng=np.random.default_rng(105)
        for n in (4,16,32,64):
            for k in range(5):
                while True:
                    try:
                        g=WeightedPermutationGreen(rng.permutation(n),rng.integers(2,P,size=n,dtype=np.int64))
                        break
                    except ValueError: pass
                inv=g.explicit_inverse_sparse()
                mat=g.explicit_dense()
                self.assertTrue(np.array_equal(matmul(mat,inv),eye(n)))
                for j in range(3):
                    x=rng.integers(0,P,size=n,dtype=np.int64)
                    self.assertTrue(np.array_equal(g.apply(x),matmul(mat,x)))

    def test_weighted_sums_survive_both_gates(self):
        for n in (4,16,64,256):
            data=find_weighted_escape(n)
            self.assertNotIn('not_found',data)
            self.assertEqual(data['inverse_row_support_min'],n)
            self.assertEqual(data['schmidt_rank'],n)
            self.assertTrue(data['one_vector_output_not_constant'])

    def test_scalar_weighted_permutations_have_shared_constant_eigenvector(self):
        n=16
        rng=np.random.default_rng(11)
        p1,p2=rng.permutation(n),rng.permutation(n)
        g1=WeightedPermutationGreen(p1,np.full(n,3,dtype=np.int64))
        g2=WeightedPermutationGreen(p2,np.full(n,5,dtype=np.int64))
        layer=TwoGreenSum(g1,g2)
        const=layer.apply(np.ones(n,dtype=np.int64))
        self.assertEqual(len(set(map(int,const))),1)
        fw=matmul(fourier(n),np.ones(n,dtype=np.int64))
        self.assertNotEqual(len(set(map(int,fw))),1)

    def test_sparseness_of_each_inverse_does_not_survive_sum(self):
        for n in (4,16,64):
            z=find_escape_layer(n)
            self.assertNotIn('not_found',z)
            self.assertEqual(z['row_support_min'],n)
            self.assertEqual(z['schmidt_rank'],n)

if __name__=='__main__':unittest.main(verbosity=2)
