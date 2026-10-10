import unittest
import random
from wide_scan import *

class RankAndScanTests(unittest.TestCase):
    def test_transform_field_roots(self):
        for n in (2,4,8,16,32,64):
            m=dft(n)
            self.assertEqual(rank(m),n)
            for i in range(n):
                for j in range(n):
                    self.assertEqual(m[i][j],m[j][i])
    def test_vandermonde_balanced(self):
        for n in (4,8,16,32,64,128):
            self.assertEqual(offdiag_ranks(dft(n),n//2),(n//2,n//2))
    def test_scans_have_one_direction(self):
        for n in (4,8,16):
            a=[(3*i+2)%P for i in range(n)]
            b=[(5*i+1)%P for i in range(n)]
            for c in range(1,n):
                self.assertEqual(offdiag_ranks(forward(a,b),c)[0],0)
                self.assertLessEqual(offdiag_ranks(forward(a,b),c)[1],1)
                self.assertEqual(offdiag_ranks(backward(a,b),c)[1],0)
                self.assertLessEqual(offdiag_ranks(backward(a,b),c)[0],1)
    def test_matrix_product(self):
        rng=random.Random(172)
        for n in (2,4,7):
            x=[[rng.randrange(P) for _ in range(n)] for _ in range(n)]
            y=[[rng.randrange(P) for _ in range(n)] for _ in range(n)]
            prod=matmul(x,y)
            for i in range(n):
                for j in range(n):
                    self.assertEqual(prod[i][j],sum(x[i][k]*y[k][j] for k in range(n))%P)
    def test_general_scan_bound(self):
        out=random_scan_compositions(trials=12)
        self.assertEqual(out['max_violation'],0)
    def test_parity_cut_rank(self):
        for n in (8,16,32,64,128):
            f=dft(n); o=parity_order(n)
            self.assertEqual(offdiag_ranks(permute(f,o,o),n//2),(n//4,n//4))
    def test_bit_reverse_cut_rank(self):
        for n in (8,16,32,64):
            f=dft(n); o=bit_reverse_order(n)
            self.assertEqual(offdiag_ranks(permute(f,o,o),n//2),(n//4,n//4))
    def test_8_exhaustive(self):
        report=exact_min_balanced_submatrix_rank(8)
        self.assertEqual(report['submatrix_count'],4900)
        self.assertEqual(report['minimum_rank'],2)
    def test_permutation_invalid(self):
        with self.assertRaises(ValueError):
            permute(dft(8),[0]*8,list(range(8)))
        with self.assertRaises(ValueError):
            crossing_count([0]*8,4)
    def test_primitive_backward_example(self):
        n=6
        F=forward([0]+[1]*(n-1),[1]*n)
        B=backward([1]*n,[1]*n)
        x=[0,2,1,3,0,7]
        self.assertEqual([sum(a*b for a,b in zip(row,x))%P for row in F],[0,2,3,6,6,13])
        self.assertEqual([sum(a*b for a,b in zip(row,x))%P for row in B],[13,13,11,10,7,7])

if __name__=='__main__':unittest.main()
