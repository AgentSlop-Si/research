import unittest
import random
import numpy as np
from sparse_defect import (sparse_fourier_minor,check_telescoping,minimal_depth,
                           root_of_unity,fourier_mod)
from green_woodbury import check_green
from interleaved_separation import check,banded_separation


def bitrev(i,logn):
    return int(f'{i:0{logn}b}'[::-1],2)


def butterfly_product(n,p):
    assert n&(n-1)==0
    logn=n.bit_length()-1
    w=root_of_unity(p,n)
    x=np.eye(n,dtype=np.int64)[[bitrev(i,logn) for i in range(n)],:]
    max_row_support=0
    m=2
    while m<=n:
        S=np.zeros((n,n),dtype=np.int64)
        for start in range(0,n,m):
            for j in range(m//2):
                i=start+j;k=i+m//2
                tw=pow(w,j*(n//m),p)
                S[i,i]=1;S[i,k]=tw
                S[k,i]=1;S[k,k]=(-tw)%p
        max_row_support=max(max_row_support,int(np.count_nonzero(S,axis=1).max()))
        x=S@x%p
        m*=2
    return x,max_row_support


class TestSparseDefectGate(unittest.TestCase):
    def test_fourier_vandermonde_minors_both_fields(self):
        for p in (12289,65537):
            for n in (8,16,32,64,128):
                for q in (0,1,2,3):
                    w=sparse_fourier_minor(n,q,p)
                    self.assertEqual(w.m,n//(q+1))
                    self.assertNotEqual(w.pivot_determinant,0)
                    self.assertEqual(w.pivot_determinant,w.vandermonde_determinant)

    def test_rank_error_telescope(self):
        for p in (12289,65537):
            for n,t,s,r in ((8,1,3,1),(8,3,2,2),(16,2,3,1),
                            (32,2,3,2),(32,3,2,1)):
                w=check_telescoping(n,t,s,r,p)
                self.assertLessEqual(w['rank_difference'],t*r)
                self.assertLessEqual(w['max_sparse_base_row_support'],s**t)

    def test_woodbury_exact_dense_green_stages(self):
        for p in (12289,65537):
            for n,r in ((8,1),(8,2),(16,1),(16,2),(32,1),(32,2),(64,1)):
                    w=check_green(n,r,p)
                    self.assertEqual(w['zero_entries_of_global_stage'],0)
                    self.assertEqual(w['vectors_verified'],20)
                    self.assertLessEqual(w['rank_E'],r)

    def test_explicit_scan_inverse(self):
        for p in (12289,65537):
            for n in (8,16,32,64,128):
                w=check(n,p)
                self.assertEqual(w['minimum_rank_defect'],(n+1)//4)
                self.assertNotEqual(w['minor_determinant'],0)

    def test_all_bandwidths_separation(self):
        for p in (12289,65537):
            for n in (16,32,64,128):
                for b in (0,1,2,3,7):
                    w=banded_separation(n,b,p)
                    self.assertEqual(w['rank_lower_bound'],(n+b)//(2*b+2))
                    self.assertNotEqual(w['det_mod_p'],0)

    def test_depth_cannot_be_constant(self):
        # Smallest t not rejected by the necessary inequality, not a construction.
        for n,d in ((16,2),(64,3),(256,4),(1024,5),(65536,9)):
            self.assertEqual(minimal_depth(n,3,1),d)
            self.assertLess(d-1,n//(3**(d-1)+1))
            self.assertTrue(d>=1)
        self.assertEqual(minimal_depth(65536,3,2),8)

    def test_classical_ntt_positive_control(self):
        for p in (12289,65537):
            for n in (8,16,32,64):
                got,s=butterfly_product(n,p)
                self.assertEqual(s,2)
                self.assertTrue(np.array_equal(got,fourier_mod(n,p)))

if __name__=='__main__':unittest.main(verbosity=2)
